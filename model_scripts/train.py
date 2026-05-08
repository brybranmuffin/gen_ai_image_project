import argparse
import os
from pathlib import Path

import torch
from torch.utils.data import DataLoader

from config import VAEConfig, get_config
from dataset import PokemonDataset, SampledPokemonDataset
from vae import VAE, vae_loss


def parse_args() -> VAEConfig:
    cfg = get_config()
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default=cfg.data_dir)
    p.add_argument("--checkpoint_dir", default=cfg.checkpoint_dir)
    p.add_argument("--log_dir", default=cfg.log_dir)
    p.add_argument("--latent_dim", type=int, default=cfg.latent_dim)
    p.add_argument("--hidden_dim", type=int, default=cfg.hidden_dim)
    p.add_argument("--beta", type=float, default=cfg.beta)
    p.add_argument("--batch_size", type=int, default=cfg.batch_size)
    p.add_argument("--epochs", type=int, default=cfg.epochs)
    p.add_argument("--learning_rate", type=float, default=cfg.learning_rate)
    p.add_argument("--weight_decay", type=float, default=cfg.weight_decay)
    p.add_argument("--num_workers", type=int, default=cfg.num_workers)
    p.add_argument("--save_every", type=int, default=cfg.save_every)
    p.add_argument("--resume_from", default=cfg.resume_from)
    p.add_argument("--log_interval", type=int, default=cfg.log_interval)
    p.add_argument("--encoder_dropout", type=float, default=cfg.encoder_dropout)
    p.add_argument("--lr_patience", type=int, default=cfg.lr_patience)
    p.add_argument("--lr_factor", type=float, default=cfg.lr_factor)
    p.add_argument("--lr_min", type=float, default=cfg.lr_min)
    p.add_argument("--sprites_dir", default=cfg.sprites_dir)
    p.add_argument("--samples_per_pokemon", type=int, default=cfg.samples_per_pokemon)
    p.add_argument("--exclude_sprites", nargs="*", default=cfg.exclude_sprites)
    args = p.parse_args()
    for k, v in vars(args).items():
        setattr(cfg, k, v)
    return cfg


def build_train_loader(cfg: VAEConfig) -> DataLoader:
    dataset = SampledPokemonDataset(cfg.sprites_dir, cfg.image_size, cfg.samples_per_pokemon,
                                    exclude=cfg.exclude_sprites)
    return DataLoader(
        dataset,
        batch_size=cfg.batch_size,
        shuffle=True,
        num_workers=cfg.num_workers,
        pin_memory=cfg.pin_memory,
        drop_last=True,
    )


def build_val_loader(cfg: VAEConfig) -> DataLoader:
    path = os.path.join(cfg.data_dir, "validation")
    dataset = PokemonDataset(path, image_size=cfg.image_size)
    return DataLoader(
        dataset,
        batch_size=cfg.batch_size,
        shuffle=False,
        num_workers=cfg.num_workers,
        pin_memory=cfg.pin_memory,
    )


def save_checkpoint(model: VAE, optimizer: torch.optim.Optimizer,
                    scheduler: torch.optim.lr_scheduler.ReduceLROnPlateau,
                    epoch: int, loss: float, path: str) -> None:
    torch.save({
        "epoch": epoch,
        "model_state": model.state_dict(),
        "optimizer_state": optimizer.state_dict(),
        "scheduler_state": scheduler.state_dict(),
        "loss": loss,
    }, path)


def load_checkpoint(path: str, model: VAE, optimizer: torch.optim.Optimizer,
                    scheduler: torch.optim.lr_scheduler.ReduceLROnPlateau,
                    device: torch.device) -> int:
    ckpt = torch.load(path, map_location=device)
    model.load_state_dict(ckpt["model_state"])
    optimizer.load_state_dict(ckpt["optimizer_state"])
    if "scheduler_state" in ckpt:
        scheduler.load_state_dict(ckpt["scheduler_state"])
    print(f"Resumed from epoch {ckpt['epoch']} (loss={ckpt['loss']:.4f})")
    return ckpt["epoch"]


def train_epoch(model: VAE, loader: DataLoader, optimizer: torch.optim.Optimizer,
                device: torch.device, cfg: VAEConfig, epoch: int) -> float:
    model.train()
    total_loss = 0.0
    for i, batch in enumerate(loader):
        batch = batch.to(device)
        optimizer.zero_grad()
        recon, mu, log_var = model(batch)
        loss, recon_l, kl_l = vae_loss(recon, batch, mu, log_var, cfg.beta)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        if (i + 1) % cfg.log_interval == 0:
            print(f"  [epoch {epoch} batch {i+1}/{len(loader)}] "
                  f"loss={loss.item():.4f}  recon={recon_l.item():.4f}  kl={kl_l.item():.4f}")
    return total_loss / len(loader)


@torch.no_grad()
def eval_epoch(model: VAE, loader: DataLoader,
               device: torch.device, cfg: VAEConfig) -> float:
    model.eval()
    total_loss = 0.0
    for batch in loader:
        batch = batch.to(device)
        recon, mu, log_var = model(batch)
        loss, _, _ = vae_loss(recon, batch, mu, log_var, cfg.beta)
        total_loss += loss.item()
    return total_loss / len(loader)


def main() -> None:
    cfg = parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    Path(cfg.checkpoint_dir).mkdir(parents=True, exist_ok=True)
    Path(cfg.log_dir).mkdir(parents=True, exist_ok=True)

    train_loader = build_train_loader(cfg)
    val_loader = build_val_loader(cfg)

    model = VAE(
        channels=cfg.channels,
        hidden_dim=cfg.hidden_dim,
        latent_dim=cfg.latent_dim,
        dropout=cfg.encoder_dropout,
    ).to(device)

    optimizer = torch.optim.Adam(
        model.parameters(), lr=cfg.learning_rate, weight_decay=cfg.weight_decay
    )

    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode="min", factor=cfg.lr_factor,
        patience=cfg.lr_patience, min_lr=cfg.lr_min,
    )

    start_epoch = 0
    if cfg.resume_from:
        start_epoch = load_checkpoint(cfg.resume_from, model, optimizer, scheduler, device)

    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    print(f"Training samples: {len(train_loader.dataset)}, "
          f"Validation samples: {len(val_loader.dataset)}")

    log_path = os.path.join(cfg.log_dir, "train_log.csv")
    with open(log_path, "w") as f:
        f.write("epoch,train_loss,val_loss,lr\n")

    val_loss = float("inf")
    for epoch in range(start_epoch + 1, cfg.epochs + 1):
        train_loss = train_epoch(model, train_loader, optimizer, device, cfg, epoch)
        val_loss = eval_epoch(model, val_loader, device, cfg)
        scheduler.step(val_loss)

        current_lr = optimizer.param_groups[0]["lr"]
        print(f"Epoch {epoch}/{cfg.epochs}  train={train_loss:.4f}  val={val_loss:.4f}  lr={current_lr:.2e}")

        with open(log_path, "a") as f:
            f.write(f"{epoch},{train_loss:.6f},{val_loss:.6f},{current_lr:.2e}\n")

        if epoch % cfg.save_every == 0:
            ckpt_path = os.path.join(cfg.checkpoint_dir, f"vae_epoch_{epoch:04d}.pt")
            save_checkpoint(model, optimizer, scheduler, epoch, val_loss, ckpt_path)
            print(f"  Saved checkpoint: {ckpt_path}")

    final_path = os.path.join(cfg.checkpoint_dir, "vae_final.pt")
    save_checkpoint(model, optimizer, scheduler, cfg.epochs, val_loss, final_path)
    print(f"Training complete. Final model saved to {final_path}")


if __name__ == "__main__":
    main()

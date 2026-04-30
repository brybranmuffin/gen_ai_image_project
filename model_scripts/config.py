from dataclasses import dataclass


@dataclass
class VAEConfig:
    # Paths (relative to project root; override on cluster with absolute paths)
    data_dir: str = "../data"
    checkpoint_dir: str = "../checkpoints"
    log_dir: str = "../logs"

    # Image
    image_size: int = 96
    channels: int = 4          # RGBA

    # Model
    latent_dim: int = 128
    hidden_dim: int = 512
    beta: float = 1.0           # KL weight (beta-VAE; 1.0 = standard VAE)

    # Training
    batch_size: int = 64
    epochs: int = 100
    learning_rate: float = 1e-3
    weight_decay: float = 1e-5
    num_workers: int = 4
    pin_memory: bool = True

    # Checkpointing
    save_every: int = 10        # save checkpoint every N epochs
    resume_from: str = ""       # path to checkpoint to resume from

    # Logging
    log_interval: int = 50      # log every N batches


def get_config() -> VAEConfig:
    return VAEConfig()

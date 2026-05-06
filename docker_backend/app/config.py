from dataclasses import dataclass


@dataclass
class VAEConfig:
    # Paths — relative to the project root (where this notebook lives)
    data_dir: str = drive_path + "data"
    checkpoint_dir: str = drive_path + "checkpoint_v2"
    log_dir: str = drive_path + "logs"

    # Image
    image_size: int = 96
    channels: int = 4           # RGBA

    # Model
    latent_dim: int = 128
    hidden_dim: int = 512
    beta: float = 1.0           # KL weight; 1.0 = standard VAE
    encoder_dropout: float = 0.3

    # LR scheduler (ReduceLROnPlateau)
    lr_patience: int = 15
    lr_factor: float = 0.5
    lr_min: float = 1e-6

    # Training
    batch_size: int = 64
    epochs: int = 200
    learning_rate: float = 1e-3
    weight_decay: float = 1e-5
    num_workers: int = 4
    pin_memory: bool = True

    # Checkpointing
    save_every: int = 10
    resume_from: str = ""       # set to a .pt path to resume training

    # Logging
    log_interval: int = 50      # print loss every N batches


def get_config() -> VAEConfig:
    return VAEConfig()

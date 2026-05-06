from dataclasses import dataclass


@dataclass
class VAEConfig:
    channels: int = 4
    latent_dim: int = 128
    hidden_dim: int = 512
    encoder_dropout: float = 0.3


def get_config() -> VAEConfig:
    return VAEConfig()

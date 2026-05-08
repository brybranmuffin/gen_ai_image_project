import torch
import torch.nn as nn


"""
Encoder class
"""
class Encoder(nn.Module):
    def __init__(self, channels: int, hidden_dim: int, latent_dim: int, dropout: float = 0.3):
        super().__init__()
        # 96 -> 48 -> 24 -> 12 -> 6
        self.conv = nn.Sequential(
            nn.Conv2d(channels, 32, 4, stride=2, padding=1),   # 48x48
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(32, 64, 4, stride=2, padding=1),          # 24x24
            nn.BatchNorm2d(64),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(64, 128, 4, stride=2, padding=1),         # 12x12
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(128, 256, 4, stride=2, padding=1),        # 6x6
            nn.BatchNorm2d(256),
            nn.LeakyReLU(0.2, inplace=True),
        )
        self.flat_dim = 256 * 6 * 6
        self.fc = nn.Linear(self.flat_dim, hidden_dim)
        self.dropout = nn.Dropout(dropout)
        self.fc_mu = nn.Linear(hidden_dim, latent_dim)
        self.fc_log_var = nn.Linear(hidden_dim, latent_dim)

    def forward(self, x):
        x = self.conv(x).flatten(1)
        x = self.dropout(torch.relu(self.fc(x)))
        return self.fc_mu(x), self.fc_log_var(x)


"""
Decoder class
"""
class Decoder(nn.Module):
    def __init__(self, channels: int, hidden_dim: int, latent_dim: int):
        super().__init__()
        self.flat_dim = 256 * 6 * 6
        self.fc = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_dim, self.flat_dim),
            nn.ReLU(inplace=True),
        )
        # 6 -> 12 -> 24 -> 48 -> 96
        self.deconv = nn.Sequential(
            nn.ConvTranspose2d(256, 128, 4, stride=2, padding=1),  # 12x12
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(128, 64, 4, stride=2, padding=1),   # 24x24
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(64, 32, 4, stride=2, padding=1),    # 48x48
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(32, channels, 4, stride=2, padding=1),  # 96x96
            nn.Sigmoid(),
        )

    def forward(self, z):
        x = self.fc(z).view(-1, 256, 6, 6)
        return self.deconv(x)


"""
VAE class
"""
class VAE(nn.Module):
    def __init__(self, channels: int = 4, hidden_dim: int = 512, latent_dim: int = 128,
                 dropout: float = 0.3):
        super().__init__()
        self.encoder = Encoder(channels, hidden_dim, latent_dim, dropout)
        self.decoder = Decoder(channels, hidden_dim, latent_dim)

    """
    Reparameterization trick
    """
    def reparameterize(self, mu: torch.Tensor, log_var: torch.Tensor) -> torch.Tensor:
        std = torch.exp(0.5 * log_var)
        eps = torch.randn_like(std)
        return mu + eps * std

    def forward(self, x):
        mu, log_var = self.encoder(x)
        z = self.reparameterize(mu, log_var)
        recon = self.decoder(z)
        return recon, mu, log_var

    def sample(self, n: int, device: torch.device) -> torch.Tensor:
        z = torch.randn(n, self.encoder.fc_mu.out_features, device=device)
        return self.decoder(z)


"""
VAE loss function. Calculates reconstruction loss and KL divergence
"""
def vae_loss(recon: torch.Tensor, target: torch.Tensor,
             mu: torch.Tensor, log_var: torch.Tensor,
             beta: float = 1.0) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    recon_loss = nn.functional.mse_loss(recon, target, reduction="sum") / target.size(0)
    kl_loss = -0.5 * torch.sum(1 + log_var - mu.pow(2) - log_var.exp()) / target.size(0)
    return recon_loss + beta * kl_loss, recon_loss, kl_loss

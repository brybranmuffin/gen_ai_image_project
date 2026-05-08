import random as _random
from pathlib import Path

import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms

from process_data_utils import augment_image


def get_train_transforms(image_size: int) -> transforms.Compose:
    return transforms.Compose([
        transforms.Lambda(augment_image),
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
    ])


def get_eval_transforms(image_size: int) -> transforms.Compose:
    return transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
    ])


def split_sprites(
    sprites_dir: str,
    val_split: float,
    seed: int,
    exclude: list | None = None,
) -> tuple[list, list]:
    """Return (train_paths, val_paths) from sprites_dir, excluding bad sprites."""
    all_paths = sorted(Path(sprites_dir).glob("*.png"))
    exclude_set = set(exclude or [])
    paths = [p for p in all_paths if not any(ex in p.stem for ex in exclude_set)]
    rng = _random.Random(seed)
    shuffled = paths[:]
    rng.shuffle(shuffled)
    n_val = max(1, round(len(shuffled) * val_split))
    return shuffled[n_val:], shuffled[:n_val]   # train, val


class SampledPokemonDataset(Dataset):
    """Draws samples_per_pokemon augmented views of each sprite per epoch."""

    def __init__(self, paths: list, image_size: int, samples_per_pokemon: int):
        if not paths:
            raise ValueError("paths list is empty")
        self.paths = paths
        self.samples_per_pokemon = samples_per_pokemon
        self.transform = get_train_transforms(image_size)

    def __len__(self) -> int:
        return len(self.paths) * self.samples_per_pokemon

    def __getitem__(self, idx: int) -> torch.Tensor:
        img = Image.open(self.paths[idx % len(self.paths)]).convert("RGBA")
        return self.transform(img)


class PokemonDataset(Dataset):
    """Loads raw sprites without augmentation (used for validation/test)."""

    def __init__(self, paths: list, image_size: int = 96):
        if not paths:
            raise ValueError("paths list is empty")
        self.paths = paths
        self.transform = get_eval_transforms(image_size)

    def __len__(self) -> int:
        return len(self.paths)

    def __getitem__(self, idx: int) -> torch.Tensor:
        img = Image.open(self.paths[idx]).convert("RGBA")
        return self.transform(img)

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


class SampledPokemonDataset(Dataset):
    """Draws samples_per_pokemon augmented views of each raw sprite per epoch."""

    def __init__(self, sprites_dir: str, image_size: int, samples_per_pokemon: int,
                 exclude: list | None = None):
        all_paths = sorted(Path(sprites_dir).glob("*.png"))
        exclude_set = set(exclude or [])
        self.paths = [p for p in all_paths if not any(ex in p.stem for ex in exclude_set)]
        if not self.paths:
            raise FileNotFoundError(f"No PNG files found in {sprites_dir}")
        self.samples_per_pokemon = samples_per_pokemon
        self.transform = get_train_transforms(image_size)

    def __len__(self) -> int:
        return len(self.paths) * self.samples_per_pokemon

    def __getitem__(self, idx: int) -> torch.Tensor:
        img = Image.open(self.paths[idx % len(self.paths)]).convert("RGBA")
        return self.transform(img)


class PokemonDataset(Dataset):
    """Loads pre-existing PNGs from a directory (used for validation/test)."""

    def __init__(self, data_dir: str, image_size: int = 96):
        self.paths = sorted(Path(data_dir).glob("*.png"))
        if not self.paths:
            raise FileNotFoundError(f"No PNG files found in {data_dir}")
        self.transform = get_eval_transforms(image_size)

    def __len__(self) -> int:
        return len(self.paths)

    def __getitem__(self, idx: int) -> torch.Tensor:
        img = Image.open(self.paths[idx]).convert("RGBA")
        return self.transform(img)

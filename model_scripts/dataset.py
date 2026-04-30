from pathlib import Path

import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms


def get_transforms(image_size: int, augment: bool = False) -> transforms.Compose:
    ops = []
    if augment:
        ops.append(transforms.RandomHorizontalFlip())
    ops += [
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),          # scales to [0, 1]
    ]
    return transforms.Compose(ops)


class PokemonDataset(Dataset):
    def __init__(self, data_dir: str, image_size: int = 96, augment: bool = False):
        self.paths = sorted(Path(data_dir).glob("*.png"))
        if not self.paths:
            raise FileNotFoundError(f"No PNG files found in {data_dir}")
        self.transform = get_transforms(image_size, augment)

    def __len__(self) -> int:
        return len(self.paths)

    def __getitem__(self, idx: int) -> torch.Tensor:
        img = Image.open(self.paths[idx]).convert("RGBA")
        return self.transform(img)

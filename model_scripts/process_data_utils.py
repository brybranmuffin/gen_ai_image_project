"""
This script is used to process the Pokemon dataset.
For each image in the base directory, it does the following:
1. reduce image size to 96x96 pixels
2. convert the image into a 96x96x4 numpy array (RGBA, float values between 0 and 1)
3. add Gaussian noise to the image and random rotation
4. create N copies of the image and split them into training and validation sets
5. convert the arrays back into images,
6. save the processed images into the data directory under test, training, and validation

"""

import argparse
import numpy as np
import os
from pathlib import Path
from PIL import Image, ImageOps
import torch
from torchvision import transforms
from torchvision.transforms import ColorJitter
from torchvision.transforms.functional import rotate
import random


IMAGE_SIZE = 96
NUM_COPIES_PER_IMAGE = 10
TEST_PROPORTION = 0.2
VAL_PROPORTION = 0.1
TRAIN_PROPORTION = 1.0 - TEST_PROPORTION - VAL_PROPORTION

# Resolve paths relative to the project root (one level above this script)
_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
BASE_DATA_DIR = str(_PROJECT_ROOT / "pokemon_sprites")
DATA_DIR = str(_PROJECT_ROOT / "data")

# data augmentation parameters
salt_and_pepper_prob = 0.05
gaussian_noise_std = 0.1
color_jitter_brightness = 0.5
color_jitter_contrast = 0.5
color_jitter_saturation = 0.5
color_jitter_hue = 0.05
rotation_max_angle = 30


def salt_and_pepper(img, p=salt_and_pepper_prob):
    noisy = img.copy()
    rand = np.random.rand(*img.shape)
    noisy[rand < p / 2] = 0.0
    noisy[(rand >= p / 2) & (rand < p)] = 1.0
    return noisy


def gaussian_noise(img, std=gaussian_noise_std):
    noise = np.random.normal(0, std, img.shape)
    noisy = img + noise
    return np.clip(noisy, 0.0, 1.0)


def gaussian_noise_tensor(img, std=gaussian_noise_std):
    noise = torch.randn_like(img) * std
    noisy = img + noise
    return torch.clamp(noisy, 0.0, 1.0)


def apply_random_color_jitter(img, brightness=color_jitter_brightness,
                               contrast=color_jitter_contrast,
                               saturation=color_jitter_saturation,
                               hue=color_jitter_hue):
    jitter = ColorJitter(brightness=brightness, contrast=contrast,
                         saturation=saturation, hue=hue)
    return jitter(img)


def apply_random_rotation(img, max_angle=rotation_max_angle):
    angle = random.uniform(-max_angle, max_angle)
    rotation = rotate(img, angle, fill=255)
    return rotation


# ---------------------------------------------------------------------------
# Core augmentation pipeline
# ---------------------------------------------------------------------------

def augment_image(img: Image.Image) -> Image.Image:
    """Apply random augmentation to a PIL RGBA image, keeping the alpha channel intact."""
    # 1. Random horizontal flip
    if random.random() < 0.5:
        img = ImageOps.mirror(img)

    # 2. Random rotation over the full RGBA tensor; fill=0 keeps background transparent
    tensor = transforms.ToTensor()(img)          # (4, H, W), range [0, 1]
    angle = random.uniform(-rotation_max_angle, rotation_max_angle)
    tensor = rotate(tensor, angle, fill=0.0)
    img = transforms.ToPILImage()(tensor)        # back to RGBA PIL

    # 3. Color jitter on RGB only so alpha is untouched
    r, g, b, a = img.split()
    rgb = Image.merge("RGB", (r, g, b))
    rgb = apply_random_color_jitter(rgb)
    r, g, b = rgb.split()
    img = Image.merge("RGBA", (r, g, b, a))

    # 4. Noise on RGB channels only; alpha stays clean
    arr = np.array(img).astype(np.float32) / 255.0   # (H, W, 4)
    arr[:, :, :3] = gaussian_noise(arr[:, :, :3])
    arr[:, :, :3] = salt_and_pepper(arr[:, :, :3])
    arr = np.clip(arr * 255, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGBA")


# ---------------------------------------------------------------------------
# Split calculation
# ---------------------------------------------------------------------------

def compute_split_counts(n: int) -> tuple[int, int, int]:
    """Return (n_test, n_val, n_train) that sum to n."""
    n_test = max(1, round(n * TEST_PROPORTION))
    n_val = max(1, round(n * VAL_PROPORTION))
    n_train = max(1, n - n_test - n_val)
    # Re-clamp if rounding pushed us over
    total = n_test + n_val + n_train
    if total > n:
        n_train -= (total - n)
    return n_test, n_val, n_train


# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------

def already_processed(name: str, out_dir: Path, split_labels: list[str]) -> bool:
    """Return True if every expected output file for this sprite already exists."""
    return all(
        (out_dir / split / f"{name}_{i:03d}.png").exists()
        for i, split in enumerate(split_labels)
    )


def process_sprites(base_dir: str, out_dir: str, limit: int | None = None) -> None:
    sprite_paths = sorted(Path(base_dir).glob("*.png"))
    if not sprite_paths:
        raise FileNotFoundError(f"No PNG files found in {base_dir}")

    if limit is not None:
        sprite_paths = sprite_paths[:limit]

    out_dir_path = Path(out_dir)
    for split in ("training", "validation", "test"):
        (out_dir_path / split).mkdir(parents=True, exist_ok=True)

    n_test, n_val, n_train = compute_split_counts(NUM_COPIES_PER_IMAGE)
    split_labels = (["test"] * n_test + ["validation"] * n_val + ["training"] * n_train)

    print(f"Processing {len(sprite_paths)} sprites → "
          f"{n_train} train / {n_val} val / {n_test} test copies each")

    skipped = 0
    corrupted = []
    for sprite_path in sprite_paths:
        name = sprite_path.stem   # e.g. "train_abomasnow"

        if already_processed(name, out_dir_path, split_labels):
            skipped += 1
            continue

        try:
            img = Image.open(sprite_path).convert("RGBA")
            img.verify()                # catches truncated / corrupted data
            img = Image.open(sprite_path).convert("RGBA")  # reopen after verify
            img = img.resize((IMAGE_SIZE, IMAGE_SIZE), Image.LANCZOS)
        except Exception as e:
            print(f"  WARNING: skipping {sprite_path.name} — {e}")
            corrupted.append(sprite_path.name)
            continue

        for i, split in enumerate(split_labels):
            # Test copies stay clean; train/val copies are augmented
            processed = img if split == "test" else augment_image(img)
            out_path = out_dir_path / split / f"{name}_{i:03d}.png"
            processed.save(out_path)

        print(f"  Saved {NUM_COPIES_PER_IMAGE} copies for {name}")

    processed_count = len(sprite_paths) - skipped - len(corrupted)
    print(f"\nDone. {processed_count} sprites processed, {skipped} skipped (already existed).")
    if corrupted:
        print(f"Corrupted/unreadable files skipped ({len(corrupted)}): {', '.join(corrupted)}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Process Pokemon sprites into train/val/test splits.")
    p.add_argument("--base_dir", default=BASE_DATA_DIR,
                   help="Directory containing raw sprite PNGs")
    p.add_argument("--data_dir", default=DATA_DIR,
                   help="Output directory (training/validation/test subdirs will be created)")
    p.add_argument("--limit", type=int, default=None,
                   help="Only process the first N sprites (useful for testing)")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    process_sprites(args.base_dir, args.data_dir, args.limit)

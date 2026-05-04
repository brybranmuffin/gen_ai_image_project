"""
This script is used to process the Pokemon dataset.
For each image in the base directory, it does the following:
1. reduce image size to 64x64 pixels
2. convert the image into a 64x64x3 numpy array (float values between -1 and 1)
3. add Gaussian noise to the image and random rotation
4. create N copies of the image and split them into training and validation sets
5. convert the arrays back into images, 
6. save the processed images into the data directory under test, training, and validation
"""

import cv2
import numpy as np
import os
from PIL import Image, ImageOps, ImageDraw
import matplotlib.pyplot as plt
import torch
from torchvision.transforms import ColorJitter
from torchvision.transforms.functional import rotate
import random


NUM_COPIES_PER_IMAGE = 10
TEST_PROPORTION = 0.2
VAL_PROPORTION = 0.1
TRAIN_PROPORTION = 1.0 - TEST_PROPORTION - VAL_PROPORTION

BASE_DATA_DIR = "pokemon_sprites"
DATA_DIR = "data"

# data augmentation parameters and functions

salt_and_pepper_prob = 0.05
gausian_noise_std = 0.1
color_jitter_brightness = 0.5
color_jitter_contrast = 0.5
color_jitter_saturation = 0.5
color_jitter_hue = 0.05
rotation_max_angle = 30

def salt_and_pepper(img, p=salt_and_pepper_prob):
    noisy = img.copy()
    rand = np.random.rand(*img.shape)
    noisy[rand < p/2] = 0.0
    noisy[(rand >= p/2) & (rand < p)] = 1.0

    return noisy

def gaussian_noise(img, std=gaussian_noise_std):
    noise = np.random.normal(0, std, img.shape)
    noisy = img + noise
    return np.clip(noisy, 0.0, 1.0)

def gaussian_noise_tensor(img, std=gaussian_noise_std):
    noise = torch.randn_like(img) * std
    noisy = img + noise
    return torch.clamp(noisy, 0.0, 1.0)

def apply_random_color_jitter(img, brightness=color_jitter_brightness, contrast=color_jitter_contrast, saturation=color_jitter_saturation, hue=color_jitter_hue):
    jitter = ColorJitter(brightness=brightness, contrast=contrast, saturation=saturation, hue=hue)
    return jitter(img)

def apply_random_rotation(img, max_angle = rotation_max_angle):
    angle = random.uniform(-max_angle, max_angle)
    rotation = rotate(img, angle, fill = 255)
    return rotation




import random

import cv2
import albumentations as A
import numpy as np
from albumentations.pytorch import ToTensorV2


class HairAugmentation(A.ImageOnlyTransform):
    """Simulates hair artifacts common in dermoscopic images."""

    def __init__(self, num_hairs=(2, 6), p=0.3):
        super().__init__(p=p)
        self.num_hairs = num_hairs

    def apply(self, img, **params):
        img = img.copy()
        h, w = img.shape[:2]
        n = random.randint(*self.num_hairs)

        for _ in range(n):
            pt1 = (random.randint(0, w), random.randint(0, h))
            pt2 = (random.randint(0, w), random.randint(0, h))
            color = (random.randint(0, 60),) * 3
            thickness = random.randint(1, 2)
            cv2.line(img, pt1, pt2, color, thickness, lineType=cv2.LINE_AA)

        return img

    def get_transform_init_args_names(self):
        return ("num_hairs",)


def get_train_transforms(image_size=224):

    return A.Compose([

        A.RandomResizedCrop(
            size=(image_size, image_size),
            scale=(0.8, 1.0),
            p=1.0
        ),

        A.HorizontalFlip(p=0.5),

        A.VerticalFlip(p=0.5),

        A.SafeRotate(
            limit=180,
            p=0.7,
            border_mode=cv2.BORDER_CONSTANT,
        ),

        A.RandomBrightnessContrast(
            brightness_limit=0.12,
            contrast_limit=0.12,
            p=0.5
        ),

        A.CLAHE(clip_limit=2.0, p=0.3),

        A.GaussNoise(std_range=(0.02, 0.08), p=0.2),

        A.GaussianBlur(blur_limit=(3, 5), p=0.2),

        HairAugmentation(num_hairs=(2, 6), p=0.3),

        A.ElasticTransform(alpha=1, sigma=20, p=0.1),

        A.CoarseDropout(
            num_holes_range=(1, 4),
            hole_height_range=(0.05, 0.15),
            hole_width_range=(0.05, 0.15),
            p=0.3
        ),

        A.Normalize(

            mean=(0.485, 0.456, 0.406),

            std=(0.229, 0.224, 0.225)

        ),

        ToTensorV2()

    ])


def get_valid_transforms(image_size=224):

    return A.Compose([

        A.Resize(image_size, image_size),

        A.Normalize(

            mean=(0.485, 0.456, 0.406),

            std=(0.229, 0.224, 0.225)

        ),

        ToTensorV2()

    ])
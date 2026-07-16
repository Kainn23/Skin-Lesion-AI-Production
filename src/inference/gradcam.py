import uuid
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
import torch
from PIL import Image
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image


class GradCAMGenerator:
    def __init__(self, model: torch.nn.Module, device: torch.device, output_dir: Optional[Path] = None) -> None:
        self.model = model
        self.device = device
        self.project_root = Path(__file__).resolve().parents[2]
        self.output_dir = output_dir or self.project_root / "outputs" / "gradcam"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.cam = GradCAM(
            model=self.model,
            target_layers=[self.model.blocks[-1][-1]],
        )

    def generate(self, image_tensor: torch.Tensor, original_image: Image.Image) -> str:
        tensor = image_tensor.to(self.device)
        grayscale_cam = self.cam(input_tensor=tensor, targets=None)[0]

        cam_height, cam_width = grayscale_cam.shape
        resized_image = original_image.resize((cam_width, cam_height))
        rgb_image = np.array(resized_image.convert("RGB")).astype(np.float32) / 255.0
        visualization = show_cam_on_image(rgb_image, grayscale_cam, use_rgb=True)

        file_name = f"{uuid.uuid4().hex}.png"
        output_path = self.output_dir / file_name
        Image.fromarray(visualization).save(output_path)
        return str(output_path.relative_to(self.project_root))

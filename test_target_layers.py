import torch
from PIL import Image
import numpy as np
import timm
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from src.inference.preprocess import preprocess_image
import os

# Create dummy image
image = Image.fromarray(np.uint8(np.random.rand(224, 224, 3) * 255))
tensor = preprocess_image(image)

model = timm.create_model("efficientnet_b0", pretrained=True)
model.eval()

for name, target in [("conv_head", [model.conv_head]), ("blocks", [model.blocks[-1][-1]])]:
    cam = GradCAM(model=model, target_layers=target)
    grayscale_cam = cam(input_tensor=tensor, targets=None)[0]
    
    rgb_image = np.array(image.convert("RGB")).astype(np.float32) / 255.0
    vis = show_cam_on_image(rgb_image, grayscale_cam, use_rgb=True)
    Image.fromarray(vis).save(f"test_cam_{name}.png")
    print(f"Generated test_cam_{name}.png")

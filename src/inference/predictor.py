import os
from pathlib import Path
from typing import Any, Dict, List

import torch

from src.inference.gradcam import GradCAMGenerator
from src.inference.postprocess import postprocess_logits
from src.models.factory import create_model


class Predictor:
    def __init__(self) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.class_names: List[str] = [
            "akiec",
            "bcc",
            "bkl",
            "df",
            "mel",
            "nv",
            "vasc",
        ]
        default_weights_path = Path(__file__).resolve().parents[2] / "weights" / "best_model.pth"
        self.weights_path = Path(os.environ.get("MODEL_WEIGHTS_PATH", default_weights_path))
        self.model = self._load_model()
        self.gradcam = GradCAMGenerator(self.model, self.device)

    def _load_model(self) -> torch.nn.Module:
        if not self.weights_path.exists():
            raise FileNotFoundError(f"Weights not found at {self.weights_path}")

        checkpoint = torch.load(self.weights_path, map_location=self.device)
        state_dict = checkpoint

        if isinstance(checkpoint, dict):
            if isinstance(checkpoint.get("model_state_dict"), dict):
                state_dict = checkpoint["model_state_dict"]
            elif isinstance(checkpoint.get("state_dict"), dict):
                state_dict = checkpoint["state_dict"]

        if not isinstance(state_dict, dict):
            raise TypeError("Checkpoint does not contain a state dict")

        cleaned_state_dict = {k.replace("module.", ""): v for k, v in state_dict.items()}

        for model_name in ("efficientnet_b0", "efficientnet_b3"):
            model = create_model(
                model_name=model_name,
                num_classes=len(self.class_names),
                pretrained=False,
            ).to(self.device)

            model_state = model.state_dict()
            compatible_state = {}
            for key, value in cleaned_state_dict.items():
                if key in model_state and model_state[key].shape == value.shape:
                    compatible_state[key] = value

            if len(compatible_state) == len(model_state):
                model.load_state_dict(compatible_state, strict=False)
                model.eval()
                return model

        raise RuntimeError("No compatible weights were found for the current model architecture")

    def predict(self, image_tensor: torch.Tensor) -> Dict[str, Any]:
        if not isinstance(image_tensor, torch.Tensor):
            raise TypeError("image_tensor must be a torch.Tensor")

        tensor = image_tensor.to(self.device)
        with torch.inference_mode():
            logits = self.model(tensor)

        return postprocess_logits(logits, self.class_names)

    def generate_gradcam(self, image_tensor: torch.Tensor, original_image) -> str:
        if not isinstance(image_tensor, torch.Tensor):
            raise TypeError("image_tensor must be a torch.Tensor")

        return self.gradcam.generate(image_tensor, original_image)

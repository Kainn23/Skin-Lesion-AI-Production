import torch
from pathlib import Path
from src.models.factory import create_model
from src.inference.predictor import Predictor

predictor = Predictor()

weights_path = Path("weights/best_model.pth")
checkpoint = torch.load(weights_path, map_location="cpu")
state_dict = checkpoint.get("model_state_dict", checkpoint.get("state_dict", checkpoint))
cleaned_state_dict = {k.replace("module.", ""): v for k, v in state_dict.items()}

for model_name in ("efficientnet_b0", "efficientnet_b3"):
    model = create_model(model_name=model_name, num_classes=7, pretrained=False)
    model_state = model.state_dict()
    
    matched_keys = []
    for key, value in cleaned_state_dict.items():
        if key in model_state and model_state[key].shape == value.shape:
            matched_keys.append(key)
            
    print(f"[{model_name}] Model keys: {len(model_state)} | Checkpoint keys: {len(cleaned_state_dict)} | Matched: {len(matched_keys)}")

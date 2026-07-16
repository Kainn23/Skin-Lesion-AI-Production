import torch
from pathlib import Path
from src.inference.predictor import Predictor

predictor = Predictor()
model = predictor.model
print(f"Loaded model architecture: {model.default_cfg['architecture']}")

# Let's count how many parameters are actually from the checkpoint vs randomly initialized
weights_path = Path("weights/best_model.pth")
if weights_path.exists():
    checkpoint = torch.load(weights_path, map_location="cpu")
    if "model_state_dict" in checkpoint:
        state_dict = checkpoint["model_state_dict"]
    elif "state_dict" in checkpoint:
        state_dict = checkpoint["state_dict"]
    else:
        state_dict = checkpoint
        
    cleaned_state_dict = {k.replace("module.", ""): v for k, v in state_dict.items()}
    
    model_state = model.state_dict()
    matched_keys = []
    for key, value in cleaned_state_dict.items():
        if key in model_state and model_state[key].shape == value.shape:
            matched_keys.append(key)
            
    print(f"Total keys in checkpoint: {len(cleaned_state_dict)}")
    print(f"Total keys in instantiated model: {len(model_state)}")
    print(f"Keys matched and loaded: {len(matched_keys)}")

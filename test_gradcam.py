import torch
from PIL import Image
import numpy as np
from src.inference.predictor import Predictor
from src.inference.preprocess import preprocess_image

try:
    predictor = Predictor()
    print("Predictor initialized.")
    
    # Create a dummy image
    image = Image.fromarray(np.uint8(np.random.rand(224, 224, 3) * 255))
    tensor = preprocess_image(image)
    
    print("Generating GradCAM...")
    gradcam_path = predictor.generate_gradcam(tensor, image)
    print("Success:", gradcam_path)
except Exception as e:
    import traceback
    traceback.print_exc()

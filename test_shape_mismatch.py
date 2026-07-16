import torch
from PIL import Image
import numpy as np
from src.inference.predictor import Predictor
from src.inference.preprocess import preprocess_image

try:
    predictor = Predictor()
    
    # Create an image that is NOT 224x224
    image = Image.fromarray(np.uint8(np.random.rand(600, 450, 3) * 255))
    tensor = preprocess_image(image)
    
    print("Calling generate_gradcam()...")
    gradcam_path = predictor.generate_gradcam(tensor, image)
    print("Success:", gradcam_path)
except Exception as e:
    import traceback
    traceback.print_exc()

import torch
from PIL import Image
import numpy as np
from src.inference.predictor import Predictor
from src.inference.preprocess import preprocess_image

try:
    predictor = Predictor()
    
    image = Image.fromarray(np.uint8(np.random.rand(224, 224, 3) * 255))
    tensor = preprocess_image(image)
    
    print("Calling predict()...")
    prediction_dict = predictor.predict(tensor)
    
    print("Calling generate_gradcam()...")
    gradcam_path = predictor.generate_gradcam(tensor, image)
    
    print("Success:", gradcam_path)
except Exception as e:
    import traceback
    traceback.print_exc()

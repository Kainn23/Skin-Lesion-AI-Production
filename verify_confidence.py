import torch
from PIL import Image
import numpy as np
from src.inference.predictor import Predictor
from src.inference.preprocess import preprocess_image

predictor = Predictor()
print(f"Loaded Architecture: {predictor.model.default_cfg['architecture']}")

image = Image.fromarray(np.uint8(np.random.rand(224, 224, 3) * 255))
tensor = preprocess_image(image)

prediction_dict = predictor.predict(tensor)
print(f"Prediction: {prediction_dict['prediction']}")
print(f"Confidence: {prediction_dict['confidence']:.4f}")
print("Top 3:")
for p in prediction_dict['top3']:
    print(f"  {p['class']}: {p['confidence']:.4f}")

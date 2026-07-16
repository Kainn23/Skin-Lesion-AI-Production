import io
import numpy as np
from PIL import Image
from fastapi.testclient import TestClient

from src.api.main import app

with TestClient(app) as client:
    # Create a dummy image
    image = Image.fromarray(np.uint8(np.random.rand(224, 224, 3) * 255))
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_bytes = img_byte_arr.getvalue()

    print("Testing /predict...")
    resp_predict = client.post("/predict", files={"file": ("test.jpg", img_bytes, "image/jpeg")})
    print("predict status:", resp_predict.status_code)
    if resp_predict.status_code != 200:
        print(resp_predict.json())

    print("Testing /gradcam...")
    try:
        resp_gradcam = client.post("/gradcam", files={"file": ("test.jpg", img_bytes, "image/jpeg")})
        print("gradcam status:", resp_gradcam.status_code)
        if resp_gradcam.status_code != 200:
            print("gradcam error:", resp_gradcam.text)
    except Exception as e:
        import traceback
        traceback.print_exc()

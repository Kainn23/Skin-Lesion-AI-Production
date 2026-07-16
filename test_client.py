import requests
import numpy as np
from PIL import Image
import io
import time

def test():
    image = Image.fromarray(np.uint8(np.random.rand(224, 224, 3) * 255))
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_bytes = img_byte_arr.getvalue()
    
    print("Testing /gradcam...")
    try:
        resp = requests.post("http://127.0.0.1:8000/gradcam", files={"file": ("test.jpg", img_bytes, "image/jpeg")})
        print("Status:", resp.status_code)
        if resp.status_code != 200:
            print("Error:", resp.text)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    time.sleep(3) # Wait for server to start
    test()

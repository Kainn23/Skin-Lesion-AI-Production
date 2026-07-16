import requests
import os
from pathlib import Path

def test_live_server():
    print("Downloading a sample image...")
    # Download a sample image (e.g., a generic skin texture or a cat for testing)
    img_url = "https://images.unsplash.com/photo-1612441804231-77a36b284856?auto=format&fit=crop&w=600&q=80"
    resp = requests.get(img_url)
    
    if resp.status_code == 200:
        with open("sample.jpg", "wb") as f:
            f.write(resp.content)
        print("Sample image downloaded as 'sample.jpg'")
    else:
        print("Failed to download image.")
        return

    print("\nSending 'sample.jpg' to the /gradcam endpoint...")
    try:
        with open("sample.jpg", "rb") as img_file:
            response = requests.post(
                "http://127.0.0.1:8000/gradcam", 
                files={"file": ("sample.jpg", img_file, "image/jpeg")}
            )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Response JSON:")
            print(f"  Prediction: {data.get('prediction')}")
            print(f"  Confidence: {data.get('confidence'):.4f}")
            print(f"  GradCAM Path: {data.get('gradcam_path')}")
            
            # Check if the output file actually exists
            out_path = Path(data.get('gradcam_path'))
            if out_path.exists():
                print(f"\nSuccess! The GradCAM visualization has been saved at: {out_path.absolute()}")
            else:
                print(f"\nWarning: The file {out_path} was returned by the API but does not exist on disk.")
        else:
            print("Error:", response.text)
            
    except Exception as e:
        print("Request failed:", e)

if __name__ == "__main__":
    test_live_server()

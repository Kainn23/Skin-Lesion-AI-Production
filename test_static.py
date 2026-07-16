import requests

# Test a POST to /gradcam to get a path
with open("sample.jpg", "rb") as f:
    res = requests.post("http://127.0.0.1:8000/gradcam", files={"file": f})
    data = res.json()
    print("GradCAM Response:", data)
    
    if "gradcam_path" in data:
        path = data["gradcam_path"].replace("\\", "/")
        print("Generated path:", path)
        
        # Test if FastAPI serves it
        url = f"http://127.0.0.1:8000/{path}"
        img_res = requests.get(url)
        print("GET", url, "->", img_res.status_code)

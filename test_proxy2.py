import requests
import time

url = "http://localhost:5173/api/predict"
with open("sample.jpg", "rb") as f:
    files = {"file": f}
    try:
        response = requests.post(url, files=files)
        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())
    except Exception as e:
        print("Error connecting to Vite proxy:", e)

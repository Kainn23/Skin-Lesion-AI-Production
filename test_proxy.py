import requests
import time

# Give the server a second to boot up
time.sleep(2)

url = "http://127.0.0.1:5173/api/predict"
# Let's send sample.jpg
with open("sample.jpg", "rb") as f:
    files = {"file": f}
    try:
        response = requests.post(url, files=files)
        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())
    except Exception as e:
        print("Error connecting to Vite proxy:", e)

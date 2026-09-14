import urllib.request
import json
try:
    req = urllib.request.Request("http://127.0.0.1:8000/api/products/")
    with urllib.request.urlopen(req, timeout=5) as response:
        data = response.read()
        print(f"Status: {response.status}")
        print("Response:", data[:200])
except Exception as e:
    print("Error:", e)

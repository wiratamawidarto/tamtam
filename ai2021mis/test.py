import requests
import json

res = requests.get("https://christopher0908.pythonanywhere.com/api/yolo/")
            # Convert data to dict
data = json.loads(res.text)
print(data)
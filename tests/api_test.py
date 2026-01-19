import requests

response = requests.post(
    "http://127.0.0.1:8000/ask",
    json={"question": "Quels événements culturels à Bordeaux ?"}
)

print("Status code:", response.status_code)
print("Response JSON:", response.json())

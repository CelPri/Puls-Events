import requests

BASE_URL = "http://localhost:8000"

def test_health():
    r = requests.get(f"{BASE_URL}/health", timeout=10)
    print("health:", r.status_code, r.json())

def test_metadata():
    r = requests.get(f"{BASE_URL}/metadata", timeout=10)
    print("metadata:", r.status_code, r.json())

def test_ask():
    payload = {"question": "Quels événements culturels à Bordeaux ce week-end ?"}
    r = requests.post(f"{BASE_URL}/ask", json=payload, timeout=60)
    print("ask:", r.status_code, r.json())

if __name__ == "__main__":
    test_health()
    test_metadata()
    test_ask()

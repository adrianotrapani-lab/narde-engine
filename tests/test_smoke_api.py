import requests

BASE_URL = "http://127.0.0.1:8000"

def test_root_endpoint():
    r = requests.get(BASE_URL + "/")
    assert r.status_code == 200
    assert "message" in r.json()

def test_health_endpoint():
    r = requests.get(BASE_URL + "/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


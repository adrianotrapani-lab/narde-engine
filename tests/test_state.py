from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_roll_dice():
    response = client.get("/roll")
    assert response.status_code == 200
    data = response.json()
    assert "dice" in data
    assert len(data["dice"]) == 2

def test_get_state():
    response = client.get("/state")
    assert response.status_code == 200
    data = response.json()
    assert "board" in data
    assert "current_player" in data

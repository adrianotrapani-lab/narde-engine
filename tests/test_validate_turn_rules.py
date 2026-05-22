from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_invalid_move_wrong_turn():
    payload = {
        "session_id": "s1",
        "board": [
            ["B","B","B","B","B","B","B","B"],
            ["B","B","B","B","B","B","B","B"],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            ["W","W","W","W","W","W","W","W"],
            ["W","W","W","W","W","W","W","W"]
        ],
        "turn": "W",
        "move": {
            "from": {"r": 1, "c": 0},  # contains "B" in this board
            "to": {"r": 2, "c": 0}
        }
    }
    resp = client.post("/api/narde/validate-turn", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("valid") is False
    assert "piece" in data.get("reason", "").lower() or "turn" in data.get("reason", "").lower()


def test_invalid_move_destination_occupied_by_same_color():
    payload = {
        "session_id": "s2",
        "board": [
            ["B","B","B","B","B","B","B","B"],
            ["B","B","B","B","B","B","B","B"],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            ["W","W","W","W","W","W","W","W"],
            ["W","W","W","W","W","W","W","W"]
        ],
        "turn": "W",
        "move": {
            "from": {"r": 6, "c": 0},  # "W"
            "to": {"r": 7, "c": 0}     # also "W"
        }
    }
    resp = client.post("/api/narde/validate-turn", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("valid") is False
    assert "piece" in data.get("reason", "").lower() or "occupied" in data.get("reason", "").lower()

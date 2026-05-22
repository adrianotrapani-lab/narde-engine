from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_validate_turn_endpoint_exists():
    # Try GET first (some APIs return 405 Method Not Allowed if only POST is supported)
    resp = client.get("/api/narde/validate-turn")
    # If GET returned 404, try POST with an empty JSON payload
    if resp.status_code == 404:
        resp = client.post("/api/narde/validate-turn", json={})
    # Accept any response that is not 404 (endpoint exists)
    assert resp.status_code != 404, "Expected endpoint to exist (not return 404)"
    # If the endpoint returns 200, ensure the body is JSON (basic sanity check)
    if resp.status_code == 200:
        assert resp.headers.get("content-type", "").startswith("application/json")
        try:
            data = resp.json()
            assert isinstance(data, (dict, list))
        except ValueError:
            assert False, "Endpoint returned 200 but body is not valid JSON"


def test_validate_turn_with_sample_move():
    payload = {
        "session_id": "test-session-1",
        "board": [
            # simple 8x8-like representation; adapt keys to your engine if different
            # use 0 for empty, "W" for white piece, "B" for black piece
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
            "from": {"r": 6, "c": 0},
            "to": {"r": 5, "c": 0}
        }
    }

    resp = client.post("/api/narde/validate-turn", json=payload)
    assert resp.status_code in (200, 400, 422), "Unexpected status code"
    # If the endpoint accepts the payload, it should return JSON with a boolean 'valid'
    if resp.status_code == 200:
        data = resp.json()
        assert "valid" in data and isinstance(data["valid"], bool)
        # If invalid, a reason string is helpful
        if data["valid"] is False:
            assert "reason" in data and isinstance(data["reason"], str)

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_state_structure_and_board_dimensions():
    resp = client.get("/state")
    assert resp.status_code == 200
    data = resp.json()
    assert "board" in data
    board = data["board"]
    assert board["width"] == 3
    assert board["height"] == 3
    assert isinstance(board["cells"], list)
    assert len(board["cells"]) == 9

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_state_persistence_roundtrip():
    new_state = {
        "state": "running",
        "board": {"width": 2, "height": 2, "cells": [{"x":0,"y":0,"value":"A"}]},
        "turn": 1,
        "players": [{"id":1,"name":"Alice","score":0}],
        "current_player": 1
    }
    resp = client.post("/state", json=new_state)
    assert resp.status_code == 200
    data = resp.json()
    assert data["state"] == "running"
    resp2 = client.get("/state")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["state"] == "running"
    assert data2["board"]["width"] == 2
    assert data2["current_player"] == 1

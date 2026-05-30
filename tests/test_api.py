import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_rules_endpoint():
    response = client.get("/api/rules")
    assert response.status_code == 200
    assert "rules" in response.json()

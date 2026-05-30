import requests

def test_health_endpoint():
    r = requests.get("http://127.0.0.1:8000/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_board_js_exists():
    r = requests.get("http://127.0.0.1:8000/assets/js/board.js")
    assert r.status_code == 200

def test_dice_css_exists():
    r = requests.get("http://127.0.0.1:8000/static/components/dice.css")
    assert r.status_code == 200

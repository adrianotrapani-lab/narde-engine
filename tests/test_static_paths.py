import requests

def test_assets_paths():
    assert requests.get('http://127.0.0.1:8000/assets/js/board.js').status_code == 200
    assert requests.get('http://127.0.0.1:8000/assets/static/js/board.js').status_code == 200

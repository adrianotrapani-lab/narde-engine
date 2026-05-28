import requests

def test_assets_headers():
    r = requests.get('http://127.0.0.1:8000/assets/static/js/board.js')
    assert r.status_code == 200
    assert 'ETag' in r.headers
    assert r.headers.get('content-type','').startswith('text/javascript')

import subprocess
import time
import requests
import os
import atexit
import pytest

UVICORN_CMD = ['python', '-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '8000']

@pytest.fixture(scope='session', autouse=True)
def uvicorn_server():
    env = os.environ.copy()
    proc = subprocess.Popen(UVICORN_CMD, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    atexit.register(lambda: proc.kill())
    for _ in range(30):
        try:
            r = requests.get('http://127.0.0.1:8000/health', timeout=1)
            if r.status_code == 200:
                break
        except Exception:
            time.sleep(0.2)
    else:
        proc.kill()
        pytest.exit('uvicorn failed to start for tests')
    yield
    try:
        proc.terminate()
        proc.wait(timeout=5)
    except Exception:
        proc.kill()

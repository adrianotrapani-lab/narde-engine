# narde-engine

[![Python tests](https://github.com/adrianotrapani-lab/narde-engine/actions/workflows/python-tests.yml/badge.svg)](https://github.com/adrianotrapani-lab/narde-engine/actions/workflows/python-tests.yml)

Minimal FastAPI project for dice and game state.

## Install
Create and activate a virtual environment, then:
pip install -r requirements.txt

## Run tests
pytest -q

## Run locally
python -m uvicorn main:app --host 127.0.0.1 --port 8000

## Endpoints
- GET /state
- GET /roll?count=2&sides=6

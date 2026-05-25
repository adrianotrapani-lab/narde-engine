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

## Previewing the site (GitHub Pages)

Open the project Pages URL in a browser to preview the live site:
https://adrianotrapani-lab.github.io/narde-engine/

If you want to preview changes locally:
- Edit files under `docs/` and commit to `main`.
- The workflow on `main` will run a smoke test and deploy `docs/` to Pages.
- To force a fresh preview, open the Pages URL in an incognito/private window and hard‑reload (DevTools → Network → Disable cache → hard reload).

Notes:
- Keep static assets under `docs/static/` so Pages serves them correctly.
- For quick UI checks, commit small placeholder assets to `docs/static/` and verify the Pages URL above.

## Running the model selector smoke test locally

A simple script is included to verify the local runner or the presence of a cloud adapter.

Run the smoke test:
- Ensure any local runner you want to test is running on `http://localhost:8000`.
- From the repo root run:

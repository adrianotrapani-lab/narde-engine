from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title='Narde Engine Docs Server')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'docs'))
ASSETS_STATIC_DIR = os.path.join(BASE_DIR, 'assets', 'static')

if os.path.isdir(BASE_DIR):
    app.mount('/static', StaticFiles(directory=BASE_DIR), name='static')

if os.path.isdir(ASSETS_STATIC_DIR):
    app.mount('/assets/static', StaticFiles(directory=ASSETS_STATIC_DIR), name='assets_static')
    app.mount('/assets', StaticFiles(directory=ASSETS_STATIC_DIR), name='assets')

@app.get('/', include_in_schema=False)
def root():
    return RedirectResponse(url='/static/index.html')

@app.get('/health')
def health():
    return JSONResponse({'status': 'ok'})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)

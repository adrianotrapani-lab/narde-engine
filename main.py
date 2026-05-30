from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from middleware import add_cors

app = FastAPI()

# Add CORS middleware
add_cors(app)

# Mount static and assets directories
app.mount("/static", StaticFiles(directory="docs/static"), name="static")
app.mount("/assets", StaticFiles(directory="docs/assets"), name="assets")

@app.get("/")
async def root():
    return FileResponse("docs/index.html")

@app.get("/health")
async def health():
    return {"status": "ok"}

# Example API route
@app.get("/api/rules")
async def get_rules():
    return {"rules": "Narde rules engine is active"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Mount static and assets directories
static_path = os.path.join(os.path.dirname(__file__), "docs", "static")
assets_path = os.path.join(os.path.dirname(__file__), "docs", "assets")

if os.path.isdir(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

if os.path.isdir(assets_path):
    app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

@app.get("/")
def root():
    return {"message": "Welcome to the Narde rules engine API"}

@app.get("/health")
def health():
    return {"status": "ok"}

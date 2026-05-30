from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static and assets
app.mount("/assets", StaticFiles(directory="docs/assets"), name="assets")
app.mount("/static", StaticFiles(directory="docs/assets/static"), name="static")

@app.get("/")
async def root():
    return {"message": "Narde engine running"}

@app.get("/health")
async def health():
    return {"status": "ok"}

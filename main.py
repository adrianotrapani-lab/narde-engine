from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# Mount both static and assets paths
app.mount("/assets", StaticFiles(directory="docs/assets"), name="assets")
app.mount("/static", StaticFiles(directory="docs/assets/static"), name="static")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Narde engine running"}

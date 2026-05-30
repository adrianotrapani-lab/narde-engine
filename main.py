from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Add CORS middleware
# This allows browser clients (like your UI) to call the API without cross-origin errors.
# Adjust `allow_origins` if you want to restrict to specific domains later.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],  # allow all HTTP methods
    allow_headers=["*"],  # allow all headers
)

@app.get("/")
def root():
    return {"message": "Welcome to the Narde rules engine API"}

@app.get("/health")
def health():
    return {"status": "ok"}

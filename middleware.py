from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

def add_cors(app: FastAPI) -> None:
    """
    Attach CORS middleware to the FastAPI app.
    Allows all origins, methods, and headers for integration readiness.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],        # Allow all origins
        allow_credentials=True,     # Allow cookies/authorization headers
        allow_methods=["*"],        # Allow all HTTP methods
        allow_headers=["*"],        # Allow all headers
    )

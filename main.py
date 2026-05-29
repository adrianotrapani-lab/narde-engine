from fastapi.staticfiles import StaticFiles

# Serve docs/assets at /assets
app.mount("/assets", StaticFiles(directory="docs/assets"), name="assets")

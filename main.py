from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from xer.api import router as api_router
from xer.logger import logger

# Define project paths
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    - Registers the API router.
    - Mounts static files.
    - Adds a startup event that logs when the app starts.
    """
    app = FastAPI(title="Xer API", version="0.1.0")

    # Mount static files
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    app.include_router(api_router)

    @app.on_event("startup")
    async def startup_event() -> None:
        logger.info("🚀 Xer API started")

    return app


app = create_app()

# When executed directly, run the development server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("xer.main:app", host="0.0.0.0", port=8000, reload=True)

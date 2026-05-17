from fastapi import FastAPI

from .config import get_settings
from .middleware.cors import setup_cors
from .routers.missions import router as missions_router

settings = get_settings()

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="MissionForge Backend",
        version="0.1.0",
        docs_url="/docs/api",
        redoc_url=None,
    )

    setup_cors(app, allow_origins=["*"]) # Accept all origins for local dev

    app.include_router(missions_router)

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    return app

app = create_app()

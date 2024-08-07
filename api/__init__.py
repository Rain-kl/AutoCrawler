# api/__init__.py

from fastapi import FastAPI
from .endpoints import router as api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Crawling Service API",
        description="API for monitoring and controlling the crawling service",
        version="1.0.0"
    )

    # Include the API router
    app.include_router(api_router, prefix="/api")

    return app


app = create_app()
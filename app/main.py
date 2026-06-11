"""FastAPI application entrypoint.

Run locally with:  uvicorn app.main:app --reload
"""

from fastapi import FastAPI

from app import __version__
from app.config import get_settings
from app.core.logging import configure_logging
from app.routers import health, hello

configure_logging()
settings = get_settings()

app = FastAPI(
    title="Agentic AI on Azure — Master Class",
    description="Starter FastAPI service for the 12-week enterprise agentic-AI course.",
    version=__version__,
)

app.include_router(health.router)
app.include_router(hello.router)


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {
        "service": settings.app_name,
        "version": __version__,
        "docs": "/docs",
        "week1_endpoint": "/api/v1/hello",
    }

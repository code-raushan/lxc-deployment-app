from fastapi import FastAPI

from app.api.routes import items
from app.core.config import get_settings


def create_application() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
    )
    app.include_router(items.router, prefix="/api")
    return app


app = create_application()



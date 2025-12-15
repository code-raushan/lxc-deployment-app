from fastapi import FastAPI

from app.api.routes import items
from app.api.routes import health
from app.core.config import get_settings


def create_application() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
    )
    @app.get("/", tags=["info"])
    async def root() -> dict[str, str]:
        return {"message": "Welcome to LXC Deployment Demo App"}

    app.include_router(health.router, prefix="/api")
    app.include_router(items.router, prefix="/api")
    return app


app = create_application()



"""FastAPI application entrypoint."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.routes import router
from app.core.config import get_settings
from app.core.logging import configure_logging, log
from app.core.security import limiter


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()

    app = FastAPI(
        title="Lead Intelligence AI",
        version="0.1.0",
        description="AI-powered lead scoring service (hybrid rules + Claude).",
    )

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    @app.on_event("startup")
    async def _startup() -> None:
        log.info("app.startup", fixture_mode=settings.fixture_mode, model=settings.anthropic_model)

    return app


app = create_app()

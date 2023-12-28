import contextlib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

from entities.bookings.router import router as router_bookings
from entities.users.router import router as router_users
from settings import app_settings


@contextlib.asynccontextmanager
async def _lifespan(app: FastAPI) -> None:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield  # место работы приложения
    # await redis.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=_lifespan)
    _include_routers(app)
    _add_middlewares(app)
    return app


def _include_routers(app: FastAPI) -> None:
    app.include_router(router_users)
    app.include_router(router_bookings)


def _add_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.ALLOW_ORIGINS,
        allow_credentials=True,  # Cookie
        allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
        allow_headers=[
            "Content-Type",
            "Set-Cookie",
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Origin",
            "Authorization",
        ],
    )

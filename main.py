import contextlib
import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

sys.path.insert(1, os.path.join(sys.path[0], "src"))

from entities.bookings.router import router as router_bookings  # noqa: E402
from entities.users.router import router as router_users  # noqa: E402


@contextlib.asynccontextmanager
async def _lifespan(app: FastAPI):
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield  # место работы приложения
    # await redis.close()


app = FastAPI(lifespan=_lifespan)
app.include_router(router_users)
app.include_router(router_bookings)


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]  # https://api.mysite.com


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
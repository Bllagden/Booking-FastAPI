import contextlib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

from src.bookings.router import router as router_bookings
from src.users.router import router as users_bookings


@contextlib.asynccontextmanager
async def _lifespan(app: FastAPI):
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield  # место работы приложения
    # await redis.close()


app = FastAPI(lifespan=_lifespan)
app.include_router(users_bookings)
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

import contextlib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from admin import create_admin
from entities.bookings.router import router_bookings
from entities.hotels.router import router_hotels
from entities.rooms.router import router_rooms
from entities.users.router import router_users
from settings import AppSettings, RedisSettings, get_settings

_app_settings = get_settings(AppSettings)
_redis_settings = get_settings(RedisSettings)


@contextlib.asynccontextmanager
async def _lifespan(app: FastAPI):
    """'lifespan' заменяет 'startup' и 'shutdown'.
    'yield' - место работы приложения. Соответственно,
    все до и после 'yield' - это процессы в начале работы приложения и в его конце."""
    redis = aioredis.from_url(
        f"redis://{_redis_settings.host}:{_redis_settings.port}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    # await redis.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=_lifespan)
    _include_routers(app)
    _add_middlewares(app)
    admin = create_admin(app)  # noqa: F841
    # app.mount("/static", StaticFiles(directory="/static"), name="static")
    return app


def _include_routers(app: FastAPI) -> None:
    """Добавление роутеров в приложение."""
    app.include_router(router_users)
    app.include_router(router_bookings)
    app.include_router(router_hotels)
    app.include_router(router_rooms)


def _add_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        # CORS (Cross-Origin Resource Sharing) - обмен ресурсами между разными источниками.
        # Набор правил для браузеров, мобильных приложений и серверов, по которым они
        # могут взаимодействовать с API.
        CORSMiddleware,
        allow_origins=_app_settings.allow_origins,  # допущенные к API домены
        allow_credentials=True,  # позволяет передавать куки
        allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
        allow_headers=[  # HTTP-заголовки
            "Content-Type",
            "Set-Cookie",
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Origin",
            "Authorization",
        ],
    )

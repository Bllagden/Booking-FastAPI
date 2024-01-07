from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings import db_settings

if db_settings.MODE == "TEST":
    DATABASE_PARAMS = {"poolclass": NullPool}
elif db_settings.MODE == "DEV":
    DATABASE_PARAMS = {}


async_engine = create_async_engine(
    url=db_settings.URL,
    echo=True,
    **DATABASE_PARAMS,
)


async_session_factory = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)

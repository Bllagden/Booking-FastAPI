from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings import db_settings

async_engine = create_async_engine(
    url=db_settings.url,
    echo=True,
)


async_session_factory = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)

test_async_engine = create_async_engine(
    url=db_settings.url,
    echo=True,
    poolclass=NullPool,
)


test_async_session_factory = async_sessionmaker(
    bind=test_async_engine,
    expire_on_commit=False,
)

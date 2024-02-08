# from sqlalchemy import NullPool
# from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
#
# from settings import db_settings
#
# if db_settings.MODE == "TEST":
#     DATABASE_PARAMS = {"poolclass": NullPool}
# elif db_settings.MODE == "DEV":
#     DATABASE_PARAMS = {}
# elif db_settings.MODE == "PROD":
#     DATABASE_PARAMS = {}
#
# async_engine = create_async_engine(
#     url=db_settings.url,
#     echo=True,
#     **DATABASE_PARAMS,
# )
#
#
# async_session_factory = async_sessionmaker(
#     bind=async_engine,
#     expire_on_commit=False,
# )


from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings import DatabaseSettings, get_settings

_settings = get_settings(DatabaseSettings)

async_engine = create_async_engine(
    url=_settings.url,
    pool_size=20,
    pool_pre_ping=True,
    pool_use_lifo=True,
    echo=_settings.echo,
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)

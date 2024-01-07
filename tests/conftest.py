import asyncio

import pytest

from db import Base, async_engine, async_session_factory  # noqa: F401
from db.models import Bookings, Hotels, Rooms, Users  # noqa: F401
from settings import db_settings


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    assert db_settings.MODE == "TEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all())
        await conn.run_sync(Base.metadata.create_all())


# Взято из документации к pytest-asyncio
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

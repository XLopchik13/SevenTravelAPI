from asyncio import get_event_loop_policy
import pytest
from httpx import AsyncClient, ASGITransport

from app.database import async_engine, async_session, Base
from app.main import app


@pytest.fixture(scope="module")
async def test_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield async_session

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session")
def event_loop():
    loop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

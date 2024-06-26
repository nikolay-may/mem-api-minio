import asyncio
import sys
import os
from typing import AsyncGenerator
from fastapi import Depends
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool
from public_api.main import app
from db_service.models import Base, Meme
from db_service.repository import MemeRepository
from public_api.routes.memes import get_meme_repository

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


SQLITE_DATABASE_URL = "sqlite+aiosqlite:///./test_db.db"

engine = create_async_engine(
    SQLITE_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

test_async_sessionmaker = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


async def get_test_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_sessionmaker() as session:
        yield session


def override_get_meme_repository(
    session: AsyncSession = Depends(get_test_async_session),
) -> MemeRepository:
    return MemeRepository(session)


app.dependency_overrides[get_meme_repository] = override_get_meme_repository


@pytest.fixture(autouse=True, scope="session")
async def initialize_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True)
async def setup_database(initialize_database):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        async with test_async_sessionmaker() as session:
            # Добавьте тестовые данные в базу данных здесь
            session.add(Meme(title="Funny Cat", description="Test Meme"))
            session.add(Meme(title="Funny God", description="Test Meme"))
            session.add(Meme(title="Funny Gun", description="Test Meme"))
            await session.commit()
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


client = TestClient(app)


@pytest.fixture()
def sync_client():
    return client


@pytest.fixture()
def get_app():
    return app


@pytest.fixture()
async def ac_client(get_app):
    async with AsyncClient(
        transport=ASGITransport(app=get_app), base_url="http://test"
    ) as async_client:
        yield async_client


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

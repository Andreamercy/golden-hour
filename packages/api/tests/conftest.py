"""Test configuration and fixtures for the Golden Hour API."""
import asyncio
import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

# Set test environment before importing app modules
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://golden_hour:testpassword@localhost:5432/golden_hour_test")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("JWT_SECRET", "test_secret_at_least_32_characters_long_for_testing")
os.environ.setdefault("ENVIRONMENT", "test")

from src.main import app
from src.database.db import get_db, Base


@pytest.fixture(scope="session")
def event_loop_policy():
    return asyncio.DefaultEventLoopPolicy()


@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Async test client for the FastAPI app."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
def sync_client():
    """Synchronous test client for simple tests."""
    with TestClient(app) as c:
        yield c

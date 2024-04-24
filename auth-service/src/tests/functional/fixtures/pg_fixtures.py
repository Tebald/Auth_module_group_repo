import pytest_asyncio
from redis.asyncio import Redis
import backoff
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.models.db_entity import (
    User,
    Role, 
    Permission, 
    RolePermission
)
from src.db.postgres import Base
from src.tests.functional.settings import test_base_settings


@pytest_asyncio.fixture(name="pg_engine")
async def get_pg_engine():
    dsn = f"postgresql+asyncpg://{test_base_settings.pg_user}:{test_base_settings.pg_password}@{test_base_settings.pg_host}:{test_base_settings.pg_port}/{test_base_settings.pg_db}"
    engine = create_async_engine(dsn, echo=True, future=True)
    return engine


@pytest_asyncio.fixture(name="pg_async_session")
async def get_pg_session(pg_engine) -> AsyncSession:
    async_session = async_sessionmaker(
        pg_engine, class_=AsyncSession, expire_on_commit=False
    )

    return async_session()


@pytest_asyncio.fixture(name="super_user")
async def super_user(pg_async_session):
    user = User(email="su@example.com", hashed_password="qwerty", is_superuser=True)
    pg_async_session.add(user)
    await pg_async_session.commit()
    await pg_async_session.refresh(user)
    yield user
    await pg_async_session.delete(user)
    await pg_async_session.commit()

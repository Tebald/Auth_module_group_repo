from core.api_settings import settings
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

# Base class for all further models
Base = declarative_base()

# Add DB engine
dsn = f'postgresql+asyncpg://{settings.user}:{settings.password}@{settings.host}:{settings.port}/{settings.db}'
engine = create_async_engine(dsn, echo=True, future=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_pg_session() -> AsyncSession:
    async with async_session() as session:
        yield session

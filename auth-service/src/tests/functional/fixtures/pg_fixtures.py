import pytest_asyncio
import backoff
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
import uuid
from datetime import UTC, datetime

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, String,
                        UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import DeclarativeBase

from tests.functional.settings import test_base_settings as settings


dsn = f'postgresql+asyncpg://{settings.pg_user}:{settings.pg_password}@{settings.pg_host}:{settings.pg_port}/{settings.pg_db}'
engine = create_async_engine(dsn, echo=True, future=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(name='postgres_session', scope='session')
@backoff.on_exception(backoff.expo, Exception, max_time=30, jitter=backoff.random_jitter)
async def get_pg_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(name='pg_create_tables')
@backoff.on_exception(backoff.expo, Exception, max_time=30, jitter=backoff.random_jitter)
async def create_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(name='pg_clear_all')
@backoff.on_exception(backoff.expo, Exception, max_time=30, jitter=backoff.random_jitter)
async def purge_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


class Base(DeclarativeBase):
    pass


class UUIDMixin:
    # Points that we should not create such table in DB.
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)


class User(UUIDMixin, Base):
    """
    Class to represent DB 'users' table data model
    """
    __tablename__ = 'users'
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    registered_at = Column(DateTime(timezone=True), default=datetime.now(UTC))

    def __init__(self, email: str,
                 hashed_password: str,
                 is_active: bool | None = None,
                 is_superuser: bool | None = None,
                 is_verified: bool | None = None,
                 registered_at: datetime | None = None) -> None:
        super().__init__()
        self.email = email
        self.hashed_password = self.hashed_password = generate_password_hash(hashed_password)
        self.is_active = is_active
        self.is_superuser = is_superuser
        self.is_verified = is_verified
        self.registered_at = registered_at

    async def check_password(self, password: str) -> bool:
        return check_password_hash(self.hashed_password, password)

    @staticmethod
    async def get_password_hashed(password) -> str:
        return generate_password_hash(password)

    def __repr__(self) -> str:
        return f'<User {self.email}>'


class Role(UUIDMixin, Base):
    """
    Class to represent DB 'roles' table data model
    """
    __tablename__ = 'roles'

    name = Column(String(1024), unique=True, nullable=False)


class Permission(UUIDMixin, Base):
    """
    Class to represent DB 'permissions' table data model
    """
    __tablename__ = 'permissions'

    name = Column(String(1024), unique=True, nullable=False)


class RolePermission(UUIDMixin, Base):
    """
    Class to represent DB 'role_permissions' table data model
    """
    __tablename__ = 'role_permissions'

    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    permission_id = Column(UUID(as_uuid=True), ForeignKey("permissions.id"), nullable=False)
    __table_args__ = (UniqueConstraint('role_id', 'permission_id', name='_role_permission_unic'),)


class UserRole(UUIDMixin, Base):
    """
    Class to represent DB 'user_roles' table data model
    """
    __tablename__ = 'user_roles'

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    __table_args__ = (UniqueConstraint('user_id', 'role_id', name='_user_role_unic'),)


class LoginHistory(UUIDMixin, Base):
    """
    Class to represent DB 'login_history' table data model
    """
    __tablename__ = 'login_history'

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime)
    ip_address = Column(String(15))
    location = Column(String(255))
    user_agent = Column(String(255))

import uuid
from datetime import UTC, datetime

from sqlalchemy import (JSON, Boolean, Column, DateTime, ForeignKey, String,
                        UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash

from src.db.postgres import Base, engine


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

    def __repr__(self) -> str:
        return f'<User {self.email}>'


class Role(UUIDMixin, Base):
    """
    Class to represent DB 'roles' table data model
    """
    __tablename__ = 'roles'

    name = Column(String(1024), unique=True, nullable=False)
    permissions = Column(JSON, default={}, nullable=False)


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


async def create_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def purge_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

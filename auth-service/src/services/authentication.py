from functools import lru_cache
from src.db.redis_db import get_redis
from fastapi import Depends
from sqlalchemy.sql import select

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.db_entity import User
from .helper import AsyncCache


class AuthenticationService:
    def __init__(self, cache: AsyncCache):
        self.cache = cache

    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str) -> [User | None]:
        """
        Searching for a user in the DB
        """
        statement = select(User).where(User.email == email)
        statement_result = await db.execute(statement=statement)
        user = statement_result.scalar_one_or_none()
        if not user:
            return None
        if not await user.check_password(password):
            return None
        return user


@lru_cache()
def get_authentication_service(
        cache: AsyncCache = Depends(get_redis),
) -> AuthenticationService:
    return AuthenticationService(cache=cache)

from functools import lru_cache
from src.db.redis_db import get_redis
from fastapi import Depends
from sqlalchemy.sql import select
from sqlalchemy import text, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.schema.model import (
    UserRegistrationReq,
    UserRegisteredResp,
    ValidationErrorResp
)
from src.models.db_entity import User
from .helper import AsyncCache


class RegistrationService:
    def __init__(self, cache: AsyncCache):
        self.cache = cache

    async def register_user(
        self,
        db: AsyncSession,
        user_info: UserRegistrationReq
    ) -> (UserRegisteredResp | ValidationErrorResp):
        user_exists = await self.check_user_exists(db=db, email=user_info.email)
        if user_exists:
            return ValidationErrorResp(result="Пользователь уже существует")
        result = await self.add_user(db, user_info)
        return result

    # TODO: check password validity
    async def check_user_exists(self, db: AsyncSession, email: str) -> bool:
        statement = select(User).where(User.email == email)
        statement_result = await db.execute(statement=statement)
        user = statement_result.scalar_one_or_none()
        return user is not None

    async def add_user(
        self, 
        db: AsyncSession,
        user_info: UserRegistrationReq
    ) -> (UserRegisteredResp | ValidationErrorResp):
        user = User(email=user_info.email, hashed_password=user_info.password)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return UserRegisteredResp(
            result="TBD",
            user_id=str(user.id),
            email=user.email,
            is_active=user.is_active
        )


@lru_cache()
def get_registration_service(
        cache: AsyncCache = Depends(get_redis),
) -> RegistrationService:
    return RegistrationService(cache=cache)
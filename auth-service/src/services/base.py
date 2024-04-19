import logging
import uuid
from datetime import datetime
from functools import lru_cache
from typing import List

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from sqlalchemy import insert

from src.db.redis_db import get_redis
from src.models.db_entity import User, LoginHistory
from src.schema.model import RefreshTokenData, UserLoginHistory
from src.services.jwt_token import JWTService, get_jwt_service
from src.services.redis import RedisService, get_redis_service

from .helper import AsyncCache


class BaseService:

    @staticmethod
    async def get_user_by_uuid(db: AsyncSession, user_id: str) -> [User | None]:
        """
        Searching for a user in the DB by email field.
        Returns DB User representation.
        """
        statement = select(User).where(User.id == user_id)
        statement_result = await db.execute(statement=statement)
        user = statement_result.scalar_one_or_none()
        if not user:
            return None

        return user

    @staticmethod
    async def get_user_login_history(db: AsyncSession, user_id: str, limit: int = 50) -> [List[LoginHistory] | None]:
        """
        Searching for a user login history in DB.
        Returns last 50 search results.
        """
        statement = select(LoginHistory).where(LoginHistory.user_id == user_id).limit(limit)
        statement_result = await db.execute(statement=statement)
        login_history = statement_result.scalars()
        if not login_history:
            return None

        # Получили из базы список из LoginHistory (схема БД)
        # берем каждый объект списка, декодируем в dict
        # dict распаковываем в UserLoginHistory - модель которую мы отдаем пользователю.
        return [UserLoginHistory(**jsonable_encoder(login)) for login in login_history]


@lru_cache()
def get_base_service() -> BaseService:
    return BaseService()

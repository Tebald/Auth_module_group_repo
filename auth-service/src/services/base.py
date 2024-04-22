from functools import lru_cache
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, update

from src.models.db_entity import User, LoginHistory, UserRole, Role
from src.schema.model import UserLoginHistory, ResetCredentialsResp, ResetPasswordResp, UserRoles
import logging


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
    async def get_user_roles(db: AsyncSession, user_id: str) -> [List[UserRoles] | List]:
        """
        Searching for a user roles.
        Returns DB User representation.
        """
        statement = select(Role.id, Role.name).where(UserRole.user_id == user_id, UserRole.role_id == Role.id)
        statement_result = await db.execute(statement=statement)
        user_roles = statement_result.all()
        if not user_roles:
            return []

        # Возможно, я делаю это странным образом, но не нашел другого, чтобы конвертнуть
        # объект sqlalchemy.engine.row.Row возвращаемый statement_result.all()
        # в словарик.
        return [UserRoles(**jsonable_encoder(role._mapping)) for role in user_roles]

    @staticmethod
    async def check_email_exists(db: AsyncSession, email: str) -> bool:
        statement = select(User).where(User.email == email)
        statement_result = await db.execute(statement=statement)
        user = statement_result.scalar_one_or_none()
        return user is not None

    @staticmethod
    async def get_user_login_history(db: AsyncSession, user_id: str, limit: int = 30) -> [List[LoginHistory] | None]:
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

    @staticmethod
    async def update_user_email(db: AsyncSession, email: str, user_id: str) -> ResetCredentialsResp:
        statement = update(User).values(email=email).where(User.id == user_id)

        await db.execute(statement=statement)
        await db.commit()

        statement = select(User.email).where(User.id == user_id)
        statement_result = await db.execute(statement=statement)

        result_email = statement_result.scalar_one_or_none()

        return ResetCredentialsResp(user_id=str(user_id), field='email', value=result_email)

    @staticmethod
    async def update_user_password(db: AsyncSession, password: str, user_id: str) -> ResetPasswordResp:
        hashed_password = await User.get_password_hashed(password)
        statement = update(User).values(hashed_password=hashed_password).where(User.id == user_id)

        await db.execute(statement=statement)
        await db.commit()

        return ResetPasswordResp(user_id=str(user_id))


@lru_cache()
def get_base_service() -> BaseService:
    return BaseService()

from functools import lru_cache
from src.db.redis_db import get_redis
from fastapi import Depends, HTTPException, status
from sqlalchemy.sql import select
from sqlalchemy import text, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.schema.model import (
    RoleCreateReq,
    RoleCreateResp,
    RolesListResp,
    RoleInfoResp
)
from src.models.db_entity import Role
from .helper import AsyncCache


class AdminRolesService:
    def __init__(self):
        ...

    async def create_role(self, db: AsyncSession, role_data: RoleCreateReq):
        role_exists = await self.check_role_exists(db=db, name=role_data.name)
        if role_exists:
             raise HTTPException(
                 status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                 detail="Роль уже существует"
             )
        result = await self.add_role(db, role_data)
        return result
    
    async def check_role_exists(self, db: AsyncSession, name: str) -> bool:
        statement = select(Role).where(Role.name == name)
        statement_result = await db.execute(statement=statement)
        role = statement_result.scalar_one_or_none()
        return role is not None

    async def add_role(
        self, 
        db: AsyncSession,
        role_data: RoleCreateReq
    ) -> RoleCreateResp:
        role = Role(name = role_data.name)
        db.add(role)
        await db.commit()
        await db.refresh(role)
        return RoleCreateResp(
            role_id = str(role.id),
            name = role.name,
            permissions = []
        )

    async def get_all_roles(self, db: AsyncSession):
        statement = select(Role)
        statement_result = await db.execute(statement=statement)
        roles = statement_result.scalars()
        roles_data = []
        for role in roles:
            roles_data.append(
                RoleInfoResp(
                    role_id = str(role.id),
                    name = role.name,
                    permissions = [] # TODO: parse Role.permissions
                )
            )
        return RolesListResp(data=roles_data)


@lru_cache()
def get_admin_roles_service() -> AdminRolesService:
    return AdminRolesService()
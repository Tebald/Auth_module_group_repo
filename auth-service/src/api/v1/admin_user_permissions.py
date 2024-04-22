from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.authentication import get_superuser
from src.db.postgres import get_pg_session
from src.schema.model import UserRolesResp
from src.services.base import BaseService, get_base_service
from src.models.db_entity import User

router = APIRouter()


@router.get('/admin/users{user_id}/roles',
            status_code=status.HTTP_200_OK,
            response_model=UserRolesResp,
            description='Details regarding user permissions')
async def get_user_roles_list(
        user_id: UUID4,
        db: AsyncSession = Depends(get_pg_session),
        base_service: BaseService = Depends(get_base_service),
        db_user: User = Depends(get_superuser)):
    """
    Returns details regarding user roles.
    """
    user = await base_service.get_user_by_uuid(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    user_roles = await base_service.get_user_roles(db, user_id)

    return UserRolesResp(
        user_id=str(user.id),
        user_name=user.email,
        roles=user_roles
    )

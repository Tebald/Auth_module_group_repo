from fastapi import APIRouter, status, Depends, Cookie, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.postgres import get_pg_session
from src.services.admin_roles import AdminRolesService, get_admin_roles_service
from src.schema.model import (
    RoleCreateReq,
    RolesListResp,
    RoleCreateResp
)


router = APIRouter()


def get_access_token(access_token: str = Cookie(None, alias="my_cookie")):
    if access_token is None:
         HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail= "Отказано в доступе. Не найден access token."
        )
    return access_token


# TODO: Do we need access token here?
@router.get(
    "/admin/roles", 
    response_model=RolesListResp, 
    status_code=status.HTTP_200_OK
)
async def get_roles(
    db: AsyncSession = Depends(get_pg_session),
    admin_roles_service: AdminRolesService = Depends(get_admin_roles_service)
) -> RolesListResp:
    # Your logic to get the list of roles
    #return RolesListResp(roles=[RoleItem(name="Admin"), RoleItem(name="User")])
    result = await admin_roles_service.get_all_roles(db=db)
    return result


@router.post(
    "/admin/roles", 
    response_model=RoleCreateResp,
    status_code=status.HTTP_201_CREATED
)
async def create_role(
    role_data: RoleCreateReq,
    access_token: str = Depends(get_access_token),
    db: AsyncSession = Depends(get_pg_session),
    admin_roles_service: AdminRolesService = Depends(get_admin_roles_service)
) -> RoleCreateResp:
    # TODO: check access token
    is_access_token_valid = True
    if is_access_token_valid:
        result = await admin_roles_service.create_role(db=db, role_data=role_data)
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Отказано в доступе. Access Token не действителен."
        )




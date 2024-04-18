from fastapi import APIRouter, status, Depends, Cookie, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.postgres import get_pg_session
from src.services.admin_roles import AdminRolesService, get_admin_roles_service
from src.schema.model import (
    RoleCreateReq,
    RolesListResp,
    RoleCreateResp,
    PermissionCreateReq,
    PermissionsListResp,
    PermissionCreateResp
)
from typing import List


router = APIRouter()


def get_access_token(access_token: str = Cookie(None, alias="my_cookie")):
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail= "Отказано в доступе. Не найден access token."
        )
    return access_token


def check_access_token(access_token: str, db: AsyncSession):
    # TODO: write logic here
    is_access_token_valid = True
    if not is_access_token_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Отказано в доступе. Access Token не действителен."
        )


@router.get(
    "/admin/permissions", 
    response_model=PermissionsListResp, 
    status_code=status.HTTP_200_OK
)
async def get_permissions(
    access_token: str = Depends(get_access_token),
    db: AsyncSession = Depends(get_pg_session),
    admin_roles_service: AdminRolesService = Depends(get_admin_roles_service)
) -> RolesListResp:
    check_access_token(access_token=access_token, db=db)
    return await admin_roles_service.get_all_permissions(db=db)


@router.post(
    "/admin/permissions", 
    response_model=PermissionCreateResp,
    status_code=status.HTTP_201_CREATED
)
async def create_permission(
    permission_data: PermissionCreateReq,
    access_token: str = Depends(get_access_token),
    db: AsyncSession = Depends(get_pg_session),
    admin_roles_service: AdminRolesService = Depends(get_admin_roles_service)
) -> RoleCreateResp:
    check_access_token(access_token=access_token, db=db)
    return await admin_roles_service.create_permission(db=db, permission_data=permission_data)


@router.delete("/admin/permissions/{permission_name}")
async def delete_permission(
    permission_name: str,
    access_token: str = Depends(get_access_token),
    db: AsyncSession = Depends(get_pg_session),
    admin_roles_service: AdminRolesService = Depends(get_admin_roles_service)
) -> None:
    check_access_token(access_token=access_token, db=db)
    return await admin_roles_service.delete_permission(db=db, permission_name=permission_name)


@router.get(
    "/admin/roles", 
    response_model=RolesListResp, 
    status_code=status.HTTP_200_OK
)
async def get_roles(
    access_token: str = Depends(get_access_token),
    db: AsyncSession = Depends(get_pg_session),
    admin_roles_service: AdminRolesService = Depends(get_admin_roles_service)
) -> RolesListResp:
    check_access_token(access_token=access_token, db=db)
    return await admin_roles_service.get_all_roles(db=db)


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
    check_access_token(access_token=access_token, db=db)
    return await admin_roles_service.create_role(db=db, role_data=role_data)


@router.get(
    "/admin/roles/{role_name}",
    response_model=PermissionsListResp, 
    status_code=status.HTTP_200_OK
)
async def get_role_permissions(
    role_name: str,
    access_token: str = Depends(get_access_token),
    db: AsyncSession = Depends(get_pg_session),
    admin_roles_service: AdminRolesService = Depends(get_admin_roles_service)
):
    check_access_token(access_token=access_token, db=db)
    return await admin_roles_service.get_permissions_by_role(db=db, role_name=role_name)


@router.put("/admin/roles/{role_name}")
async def update_role_permissions(
    role_name: str, 
    permissions: List[str],
    access_token: str = Depends(get_access_token),
    db: AsyncSession = Depends(get_pg_session),
    admin_roles_service: AdminRolesService = Depends(get_admin_roles_service)
) -> RoleCreateResp:
    check_access_token(access_token=access_token, db=db)
    return await admin_roles_service.update_role_permissions(db=db, role_name=role_name, permissions=permissions)


@router.delete("/admin/roles/{role_name}")
async def delete_permission(
    role_name: str,
    access_token: str = Depends(get_access_token),
    db: AsyncSession = Depends(get_pg_session),
    admin_roles_service: AdminRolesService = Depends(get_admin_roles_service)
) -> None:
    check_access_token(access_token=access_token, db=db)
    return await admin_roles_service.delete_role(db=db, role_name=role_name)

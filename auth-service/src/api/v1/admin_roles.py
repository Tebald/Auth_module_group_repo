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
         HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail= "Отказано в доступе. Не найден access token."
        )
    return access_token


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
    # TODO: check access token
    is_access_token_valid = True
    if is_access_token_valid:
        result = await admin_roles_service.get_all_permissions(db=db)
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Отказано в доступе. Access Token не действителен."
        )


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
    # TODO: check access token
    is_access_token_valid = True
    if is_access_token_valid:
        result = await admin_roles_service.create_permission(db=db, permission_data=permission_data)
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Отказано в доступе. Access Token не действителен."
        )


@router.delete("/admin/permissions/{permission_name}")
async def delete_permission(
    permission_name: str,
    access_token: str = Depends(get_access_token),
    db: AsyncSession = Depends(get_pg_session),
    admin_roles_service: AdminRolesService = Depends(get_admin_roles_service)
) -> None:
    # TODO: check access token
    is_access_token_valid = True
    if is_access_token_valid:
        result = await admin_roles_service.delete_permission(
            db=db, permission_name=permission_name)
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Отказано в доступе. Access Token не действителен."
        )


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
    # TODO: check access token
    is_access_token_valid = True
    if is_access_token_valid:
        result = await admin_roles_service.get_all_roles(db=db)
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Отказано в доступе. Access Token не действителен."
        )


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
    # TODO: check access token
    is_access_token_valid = True
    if is_access_token_valid:
        result = await admin_roles_service.get_permissions_by_role(db=db, role_name=role_name)
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Отказано в доступе. Access Token не действителен."
        )


@router.put("/admin/roles/{role_name}")
async def update_role_permissions(
    role_name: str, 
    permissions: List[str],
    access_token: str = Depends(get_access_token),
    db: AsyncSession = Depends(get_pg_session),
    admin_roles_service: AdminRolesService = Depends(get_admin_roles_service)
) -> RoleCreateResp:
    # TODO: check access token
    is_access_token_valid = True
    if is_access_token_valid:
        result = await admin_roles_service.update_role_permissions(
            db=db, role_name=role_name, permissions=permissions)
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Отказано в доступе. Access Token не действителен."
        )


@router.delete("/admin/roles/{role_name}")
async def delete_permission(
    role_name: str,
    access_token: str = Depends(get_access_token),
    db: AsyncSession = Depends(get_pg_session),
    admin_roles_service: AdminRolesService = Depends(get_admin_roles_service)
) -> None:
    # TODO: check access token
    is_access_token_valid = True
    if is_access_token_valid:
        result = await admin_roles_service.delete_role(
            db=db, role_name=role_name)
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Отказано в доступе. Access Token не действителен."
        )



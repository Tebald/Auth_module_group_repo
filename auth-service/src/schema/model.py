import datetime
import uuid
from typing import List

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator


class UserRegistrationReq(BaseModel):
    email: str
    password: str


class UserLoginReq(BaseModel):
    email: str
    password: str


# TODO: review schema, use version in auth-service/docs/openapi_auth_api_doc.yaml
class UserRegisteredResp(BaseModel):
    result: str
    user_id: str
    email: str
    is_active: bool


class BadRequestLoginResp(BaseModel):
    result: str
    error: str


class BadRequestResp(BaseModel):
    detail: str


class InternalServerErrResp(BaseModel):
    detail: str


class ResetCredentialsBadReqResp(BaseModel):
    result: str
    message: str


class UserLoginCookie(BaseModel):
    access_token: str
    refresh_token: str


class UnauthorisedResp(BaseModel):
    detail: str


class UserAccountInfoResp(BaseModel):
    result: str
    data: str
    id: str
    email: str


class UserLoginHistoryResp(BaseModel):
    result: str
    data: List[dict]


class UserPermissionsResp(BaseModel):
    result: str
    data: str
    user_id: str
    roles: str


class UserAddRoleResp(BaseModel):
    result: str
    user_id: str
    roles: List[dict]

class PermissionInfoResp(BaseModel):
    permission_id: str
    name: str

class PermissionsListResp(BaseModel):
    data: List[PermissionInfoResp]

class PermissionCreateResp(PermissionInfoResp):
    ...

class PermissionCreateReq(BaseModel):
    name: str

      
class RoleInfoResp(BaseModel):
    role_id: str
    name: str
    permissions: List[PermissionInfoResp]


class AccessTokenData(BaseModel):
    user_id: str
    iat: datetime.datetime
    exp: datetime.datetime
    roles: list | None

    # The following two functions are necessary
    # to remove Timezone info from the timestamps
    # since pydantic automatically adds it.
    @field_validator('iat', mode='after')
    def iat_validate(cls, iat):
        return iat.replace(tzinfo=None)

    @field_validator('exp', mode='after')
    def exp_validate(cls, exp):
        return exp.replace(tzinfo=None)


class RefreshTokenData(BaseModel):
    user_id: str
    iat: datetime.datetime
    exp: datetime.datetime
    roles: list | None
    session_id: str

    @field_validator('iat', mode='after')
    def iat_validate(cls, iat):
        return iat.replace(tzinfo=None)

    @field_validator('exp', mode='after')
    def exp_validate(cls, exp):
        return exp.replace(tzinfo=None)


class RolesListResp(BaseModel):
    data: List[RoleInfoResp]

class RoleCreateResp(RoleInfoResp):
    ...

class RoleCreateReq(BaseModel):
    name: str

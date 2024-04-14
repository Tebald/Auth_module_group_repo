from pydantic import BaseModel, Field
from typing import List

class UserRegistrationReq(BaseModel):
    email: str
    password: str

class UserRegisteredResp(BaseModel):
    result: str
    data: str
    user_id: str
    email: str
    is_active: bool

class ValidationErrorResp(BaseModel):
    result: str

class BadRequestRegResp(BaseModel):
    result: str
    error: str

class BadRequestLoginResp(BaseModel):
    result: str
    error: str

class BadRequestResp(BaseModel):
    result: str

class ResetCredentialsBadReqResp(BaseModel):
    result: str
    message: str

class UserLoginCookie(BaseModel):
    access_token: str
    refresh_token: str

class UnauthorisedResp(BaseModel):
    result: str

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

class RolesListResp(BaseModel):
    result: str
    data: List[dict]

class RoleInfoResp(BaseModel):
    result: str
    id: str
    name: str
    permissions: List[str]

class RoleCreateResp(BaseModel):
    result: str
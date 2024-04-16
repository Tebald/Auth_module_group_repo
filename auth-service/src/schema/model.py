from pydantic import BaseModel, Field
from typing import List

class UserRegistrationReq(BaseModel):
    email: str
    password: str

# TODO: review schema, use version in auth-service/docs/openapi_auth_api_doc.yaml
class UserRegisteredResp(BaseModel):
    data: str
    user_id: str
    email: str
    is_active: bool

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

class RoleInfoResp(BaseModel):
    role_id: str
    name: str
    permissions: List[str]

class RolesListResp(BaseModel):
    data: List[RoleInfoResp]

class RoleCreateReq(BaseModel):
    name: str

class RoleCreateResp(BaseModel):
    role_id: str
    name: str
    permissions: List[str]
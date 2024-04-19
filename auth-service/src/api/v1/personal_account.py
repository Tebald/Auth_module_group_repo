from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from src.api.v1.authentication import check_access_token, get_current_active_user
from src.db.postgres import get_pg_session
from src.schema.cookie import AccessTokenCookie, RefreshTokenCookie
from src.schema.model import UserAccountInfoResp, AccessTokenData, UserLoginHistory, UserLoginHistoryResp
from src.services.authentication import AuthenticationService, get_authentication_service
from src.services.base import BaseService, get_base_service
from src.models.db_entity import User
from src.services.jwt_token import JWTService, get_jwt_service

router = APIRouter()


async def check_user_id(user_id: UUID4, access_token_dict: dict) -> None:
    """
    Checks if user_id from access token and path parameter match.
    """
    access_token = AccessTokenData(**access_token_dict)
    if access_token.user_id != str(user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/account/{user_id}',
            status_code=status.HTTP_200_OK,
            response_model=UserAccountInfoResp,
            description='Details regarding user account')
async def get_user_account_info(
        user_id: UUID4,
        db_user: User = Depends(get_current_active_user),
        access_token_dic: dict = Depends(check_access_token)):
    """
    Returns details regarding user account.
    """

    await check_user_id(user_id, access_token_dic)

    # This is where pydantic magic shines:
    # DB model 'db_user' automatically transorms into
    # response_model=UserAccountInfoResp
    return db_user


@router.get('/account/{user_id}/history',
            status_code=status.HTTP_200_OK,
            response_model=UserLoginHistoryResp,
            description='Details regarding user login history')
async def get_user_login_history_info(
        user_id: UUID4,
        db: AsyncSession = Depends(get_pg_session),

        base_service: BaseService = Depends(get_base_service),

        db_user: User = Depends(get_current_active_user),
        access_token_dic: dict = Depends(check_access_token)):
    """
    Returns details regarding user account
    """
    await check_user_id(user_id, access_token_dic)
    login_history = await base_service.get_user_login_history(db, db_user.id)

    logging.info('TYPE: %s. Value: %s', type(login_history), login_history)

    return UserLoginHistoryResp(data=login_history)




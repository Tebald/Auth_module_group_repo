from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_pg_session
from src.schema.cookie import AccessTokenCookie, RefreshTokenCookie
from src.services.authentication import (AuthenticationService,
                                         get_authentication_service)
from src.services.jwt_token import JWTService, get_jwt_service

router = APIRouter()


@router.post('/login')
async def login_user_for_access_token_cookie(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_pg_session),
    authentication_service: AuthenticationService = Depends(get_authentication_service)
):
    """
    User login endpoint
    """
    try:
        user = await authentication_service.authenticate_user(db, form_data.username, form_data.password)

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='internal server error')

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='wrong credentials')

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user is inactive')

    access_token, refresh_token = await authentication_service.get_tokens(user_id=str(user.id), user_roles=[])

    # In production, when you have https certificate, add secure=True to the methods below.
    response.set_cookie(key=AccessTokenCookie.name, value=access_token, httponly=True)
    response.set_cookie(key=RefreshTokenCookie.name, value=refresh_token, httponly=True)

    return


@router.post('/logout', status_code=204)
async def logout_user(
    response: Response,
    rt_input: str = Cookie(alias=RefreshTokenCookie.name),
    jwt_service: JWTService = Depends(get_jwt_service),
    authentication_service: AuthenticationService = Depends(get_authentication_service)
):
    """
    User logout endpoint
    """
    if not rt_input:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorised')

    token_input_dict = await jwt_service.verify_token(token=rt_input)

    if not token_input_dict:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorised')

    try:
        await authentication_service.logout_user(token_input_dict)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='internal server error')

    response.delete_cookie(key=AccessTokenCookie.name)
    response.delete_cookie(key=RefreshTokenCookie.name)

    return


@router.post('/token-refresh')
async def refresh_user_tokens_cookie_pair(
    response: Response,
    authentication_service: AuthenticationService = Depends(get_authentication_service),
    rt_input: str = Cookie(alias=RefreshTokenCookie.name),
    jwt_service: JWTService = Depends(get_jwt_service),
):
    """
    User jwt token pair refresh endpoint
    """

    rt_input_dict = await jwt_service.verify_token(token=rt_input)

    if not rt_input_dict:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorised')

    access_token, refresh_token = await authentication_service.refresh_tokens(rt_input_dict)

    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorised')

    response.set_cookie(key=AccessTokenCookie.name, value=access_token, httponly=True)
    response.set_cookie(key=RefreshTokenCookie.name, value=refresh_token, httponly=True)

    return

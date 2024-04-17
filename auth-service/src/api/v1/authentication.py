from fastapi import APIRouter, status, Depends, HTTPException, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.postgres import get_pg_session
from src.services.authentication import AuthenticationService, get_authentication_service
from src.services.token_provider import JWTService, get_jwt_service
from src.services.redis import RedisService, get_redis_service

from src.schema.cookie import AccessTokenCookie, RefreshTokenCookie

from typing import Annotated

import logging

router = APIRouter()


@router.post('/login')
async def login_user_for_access_token_cookie(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_pg_session),
    authentication_service: AuthenticationService = Depends(get_authentication_service),
    jwt_service: JWTService = Depends(get_jwt_service),
    redis_service: RedisService = Depends(get_redis_service)
):
    """
    User login endpoint
    """
    try:
        user = await authentication_service.authenticate_user(db, form_data.username, form_data.password)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='internal server error')
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="wrong credentials",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user is inactive",
        )

    at_payload = await jwt_service.get_access_token_payload(user_id=str(user.id))
    logging.debug('access_token payload: %s', at_payload)

    rt_payload = await jwt_service.get_refresh_token_payload(user_id=str(user.id))
    access_token = await jwt_service.generate_token(at_payload, token_expire=JWTService.access_token_expire)
    refresh_token = await jwt_service.generate_token(rt_payload, token_expire=JWTService.refresh_token_expire)

    await redis_service.redis.setex(
        name=f'{user.id}_refresh',
        value=refresh_token,
        time=JWTService.refresh_token_expire*60
    )

    response.set_cookie(key=AccessTokenCookie.name, value=access_token, httponly=True)
    response.set_cookie(key=RefreshTokenCookie.name, value=refresh_token, httponly=True)

    return


@router.post('/logout', status_code=204)
async def logout_user(
    response: Response,
    access_token_jwt: str = Cookie(alias=AccessTokenCookie.name),
    jwt_service: JWTService = Depends(get_jwt_service),
    redis_service: RedisService = Depends(get_redis_service),
):
    """
    User logout endpoint
    """
    if not access_token_jwt:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="unauthorised",
        )

    access_token = await jwt_service.verify_access_token(token=access_token_jwt)

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="unauthorised",
        )

    logging.debug('access_token: %s', access_token)

    await redis_service.redis.expire(
        name=f'{access_token.user_id}_refresh',
        time=0
    )

    response.delete_cookie(key=AccessTokenCookie.name)
    response.delete_cookie(key=RefreshTokenCookie.name)

    return

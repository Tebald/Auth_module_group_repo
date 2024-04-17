from functools import lru_cache

from schema.model import AccessTokenData, RefreshTokenData
from src.db.redis_db import get_redis
from datetime import timedelta, datetime, timezone
from fastapi import Depends

from jose import jwt, JWTError
from src.core.api_settings import settings

from .helper import AsyncCache
import logging


class JWTService:
    def __init__(self, cache: AsyncCache):
        self.cache = cache

    secret_key = settings.jwt_secret_key
    algorithm = settings.jwt_algorithm
    access_token_expire = settings.jwt_at_expire_minutes
    refresh_token_expire = settings.jwt_rt_expire_minutes

    async def generate_token(self, token_data: [AccessTokenData or RefreshTokenData], token_expire: int) -> str:

        token_data.exp = datetime.utcnow() + timedelta(minutes=token_expire)
        to_encode = dict(token_data)

        logging.info('Issued token: %s', to_encode)
        encoded_jwt = jwt.encode(to_encode, self.secret_key, self.algorithm)

        return encoded_jwt

    @staticmethod
    async def get_access_token_payload(user_id: str) -> AccessTokenData:
        return AccessTokenData(
            user_id=user_id,
            iat=datetime.utcnow(),
            exp=datetime.utcnow(),
            roles=None
        )

    @staticmethod
    async def get_refresh_token_payload(user_id: str) -> RefreshTokenData:
        return RefreshTokenData(
            user_id=user_id,
            iat=datetime.utcnow(),
            exp=datetime.utcnow(),
        )

    async def verify_access_token(self, token: str) -> [AccessTokenData or False]:
        try:
            payload = jwt.decode(token, self.secret_key, self.algorithm)
            # We do not check token expiration time since it happens during
            # token decoding.

            user_id: str = payload.get('user_id')

            if user_id is None:
                logging.error('Unable to find "user_id" in the "access_token". Received payload: %s', payload)
                return False

            token_data = AccessTokenData(**payload)

        except JWTError as excp:
            logging.error('The following error occured during access token decoding: %s', excp)
            return False

        return token_data


@lru_cache()
def get_jwt_service(cache: AsyncCache = Depends(get_redis),) -> JWTService:
    return JWTService(cache=cache)


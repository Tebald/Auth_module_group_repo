from datetime import timedelta, datetime, UTC
from jose import JWTError, jwt
import pytest_asyncio
from redis.asyncio import Redis
from src.tests.functional.settings import test_base_settings
from src.schema.model import AccessTokenData


@pytest_asyncio.fixture(name='get_access_token')
async def get_access_token():
    async def _get_access_token(user_id: str) -> str:
        at_payload = AccessTokenData(
            user_id=user_id,
            iat=datetime.now(UTC),
            exp=datetime.now(UTC),
            roles=[]
        )
        at_payload.exp = datetime.now(UTC) + timedelta(minutes=test_base_settings.jwt_at_expire_minutes)
        to_encode = dict(at_payload)
        encoded_jwt = jwt.encode(to_encode, test_base_settings.jwt_secret_key, test_base_settings.jwt_algorithm)
        return encoded_jwt

    return _get_access_token

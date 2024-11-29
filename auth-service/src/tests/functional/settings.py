"""
Module to store all test settings in one place.
"""
import os

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings

DOTENV = os.path.join(os.path.dirname(__file__), 'test.env')


class TestBaseSettings(BaseSettings):
    model_config = ConfigDict(extra='ignore')
    # Postgres
    pg_db: str = Field('', alias='PG_DB')
    pg_user: str = Field('', alias='PG_USER')
    pg_password: str = Field('', alias='PG_PASSWORD')
    pg_host: str = Field('127.0.0.1', alias='PG_HOST')
    pg_port: int = Field(5433, alias='PG_PORT')
    # Redis
    redis_host: str = Field('127.0.0.1', alias='REDIS_HOST')
    redis_port: int = Field(6379, alias='REDIS_PORT')

    service_host: str = Field('0.0.0.0', alias='API_HOST')
    service_port: int = Field(8000, alias='API_PORT')
    # JWT token
    jwt_secret_key: str = Field(alias='JWT_SECRET_KEY')
    jwt_algorithm: str = Field(alias='JWT_ALGORITHM')
    jwt_at_expire_minutes: int = Field(alias='JWT_AT_EXPIRE_MINUTES')


test_base_settings = TestBaseSettings(_env_file=DOTENV, _env_file_encoding='utf-8')

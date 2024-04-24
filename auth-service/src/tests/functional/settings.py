"""
Module to store all test settings in one place.
"""
import os
from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings

current_dir = os.path.dirname(os.path.abspath(__file__))


class TestBaseSettings(BaseSettings):
    model_config = ConfigDict(extra='ignore')
    # Postgres
    pg_db: str = Field('', env='PG_DB')
    pg_user: str = Field('', env='PG_USER')
    pg_password: str = Field('', env='PG_PASSWORD')
    pg_host: str = Field('127.0.0.1', env='PG_HOST')
    pg_port: int = Field(5433, env='PG_PORT')
    # Redis
    redis_host: str = Field('127.0.0.1', env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')

    service_host: str = Field('0.0.0.0', env='API_HOST')
    service_port: int = Field(8000, env='API_PORT')
    # JWT token
    jwt_secret_key: str = Field(env='JWT_SECRET_KEY')

    current_folder: str = Field(current_dir)


test_base_settings = TestBaseSettings(_env_file='../../../../.env', _env_file_encoding='utf-8')
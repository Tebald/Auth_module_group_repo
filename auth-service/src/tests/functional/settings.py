"""
Module to store all test settings in one place.
"""
import os
from pydantic import Field
from pydantic_settings import BaseSettings

current_dir = os.path.dirname(os.path.abspath(__file__))


class TestBaseSettings(BaseSettings):
    # Postgres
    pg_db: str = Field('auth_database', env='PG_DB')
    pg_user: str = Field('app', env='PG_USER')
    pg_password: str = Field('123qwe', env='PG_PASSWORD')
    pg_host: str = Field('127.0.0.1', env='PG_HOST')
    pg_port: int = Field(5433, env='PG_PORT')
    # Redis
    redis_host: str = Field('127.0.0.1', env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')

    service_host: str = Field('0.0.0.0', env='API_HOST')
    service_port: int = Field(8000, env='API_PORT')


test_base_settings = TestBaseSettings(_env_file='.env', _env_file_encoding='utf-8')

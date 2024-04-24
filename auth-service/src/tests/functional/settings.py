"""
Module to store all test settings in one place.
"""
import os
from pydantic import BaseSettings, Field

current_dir = os.path.dirname(os.path.abspath(__file__))


class TestBaseSettings(BaseSettings):
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

    class Config:
        env_file = '../.env'


test_base_settings = TestBaseSettings()

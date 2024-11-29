import os

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings

DOTENV = os.path.join(os.path.dirname(__file__), '.env')


class Settings(BaseSettings):
    """
    Class to store fastapi project settings.
    """
    model_config = ConfigDict(extra='ignore')
    project_name: str = Field('Auth API', alias='API_PROJECT_NAME')
    # Redis
    redis_host: str = Field('127.0.0.1', alias='REDIS_HOST')
    redis_port: int = Field(6380, alias='REDIS_PORT')
    # Postgres
    pg_db: str = Field('', alias='PG_DB')
    pg_user: str = Field('', alias='PG_USER')
    pg_password: str = Field('', alias='PG_PASSWORD')
    pg_host: str = Field('127.0.0.1', alias='PG_HOST')
    pg_port: int = Field(5433, alias='PG_PORT')
    # Logging
    log_format: str = Field('%(asctime)s - %(name)s - %(levelname)s - %(message)s', alias='API_LOG_FORMAT')
    log_default_handlers: list = Field(['console', ], alias='API_LOG_DEFAULT_HANDLERS')
    console_log_lvl: str = Field('DEBUG', alias='API_CONSOLE_LOG_LVL')
    loggers_handlers_log_lvl: str = Field('INFO', alias='API_LOGGERS_HANDLERS_LOG')
    unicorn_error_log_lvl: str = Field('INFO', alias='API_UNICORN_ERROR_LOG_LVL')
    unicorn_access_log_lvl: str = Field('INFO', alias='API_UNICORN_ACCESS_LOG_LVL')
    root_log_lvl: str = Field('INFO', alias='API_ROOT_LOG_LVL')
    # JWT token settings
    jwt_secret_key: str = Field('', alias='JWT_SECRET_KEY')
    jwt_algorithm: str = Field('HS256', alias='JWT_ALGORITHM')
    jwt_at_expire_minutes: int = Field(30, alias='JWT_ACCESS_TOKEN_EXPIRE_MINUTES')
    jwt_rt_expire_minutes: int = Field(1440, alias='JWT_REFRESH_TOKEN_EXPIRE_MINUTES')


settings = Settings(_env_file=DOTENV, _env_file_encoding='utf-8')

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Class to store fastapi project settings.
    """
    project_name: str = Field('Auth API', env='API_PROJECT_NAME')
    # Redis
    redis_host: str = Field('127.0.0.1', env='REDIS_HOST')
    redis_port: int = Field(6380, env='REDIS_PORT')
    # Postgres
    pg_user = Field('', env='PG_USER')
    pg_password = Field('', env='PG_PASSWORD')
    pg_host = Field('127.0.0.1', env='PG_HOST')
    pg_port = Field(5433, env='PG_PORT')
    # Logging
    log_format: str = Field('%(asctime)s - %(name)s - %(levelname)s - %(message)s', env='API_LOG_FORMAT')
    log_default_handlers: list = Field(['console', ], env='API_LOG_DEFAULT_HANDLERS')
    console_log_lvl: str = Field('DEBUG', env='API_CONSOLE_LOG_LVL')
    loggers_handlers_log_lvl: str = Field('INFO', env='API_LOGGERS_HANDLERS_LOG')
    unicorn_error_log_lvl: str = Field('INFO', env='API_UNICORN_ERROR_LOG_LVL')
    unicorn_access_log_lvl: str = Field('INFO', env='API_UNICORN_ACCESS_LOG_LVL')
    root_log_lvl: str = Field('INFO', env='API_ROOT_LOG_LVL')

    class Config:
        env_file = '../.env'


settings = Settings()

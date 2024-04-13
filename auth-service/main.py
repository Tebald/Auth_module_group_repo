import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
import logging
from contextlib import asynccontextmanager

from src.core.logger import setup_logging
from src.core.api_settings import settings
from src.db import redis_db


setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup events
    logging.info('Config: %s', vars(settings))
    redis_db.redis = Redis(host=settings.redis_host, port=settings.redis_port)
    yield
    # On shutdown events
    await redis_db.redis.close()

app = FastAPI(
    lifespan=lifespan,
    title=settings.project_name,
    docs_url='/auth_api/openapi',
    openapi_url='/auth_api/openapi.json',
    default_response_class=ORJSONResponse,
    description='Auth API endpoints',
    version='1.0.0'
)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )

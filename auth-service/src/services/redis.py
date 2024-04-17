from functools import lru_cache

from fastapi import Depends
from redis.asyncio import Redis
from src.db.redis_db import get_redis


class RedisService:
    """
    A class to combine all the Redis operations in the one place.
    """

    def __init__(self, redis: Redis):
        self.redis = redis


@lru_cache()
def get_redis_service(
    redis: Redis = Depends(get_redis),
) -> RedisService:
    """Provider of RedisService.

    :param redis: An async Redis exemplar which represents async connection to Redis.
    :return: A Singleton of RedisService.
    """
    return RedisService(redis)

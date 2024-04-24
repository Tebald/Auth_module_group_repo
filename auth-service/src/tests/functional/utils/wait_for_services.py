import asyncio

import backoff
from redis.asyncio import Redis


from tests.functional.settings import test_base_settings

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)


#
# # Add DB engine
# dsn = f'postgresql+asyncpg://{settings.pg_user}:{settings.pg_password}@{settings.pg_host}:{settings.pg_port}/{settings.pg_db}'
# engine = create_async_engine(dsn, echo=True, future=True)
# async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
#
#
# async def get_pg_session() -> AsyncSession:
#     async with async_session() as session:
#         yield session


@backoff.on_exception(backoff.expo, Exception, max_time=300, max_tries=10)
async def wait_for_redis() -> None:
    print("Pinging Redis...")
    client = Redis(host=test_base_settings.redis_host, port=test_base_settings.redis_port)
    try:
        await client.ping()
        print("Redis is up!")
    finally:
        await client.close()


# @backoff.on_exception(backoff.expo, Exception, max_time=300, max_tries=10)
# async def wait_for_postgres() -> None:
#     print("Pinging Postgres...")
#     db = get_pg_session()
#     try:
#         await db.
#         print("Elasticsearch is up!")
#     finally: await db.close()


async def main():
    await asyncio.gather(
        wait_for_redis(),
        # wait_for_postgres(),
    )

if __name__ == '__main__':
    print("Waiting for Redis to start...")
    print("Waiting for Postgres to start...")
    asyncio.run(main())

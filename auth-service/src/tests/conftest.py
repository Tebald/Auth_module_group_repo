import asyncio
import pytest_asyncio


pytest_plugins = [
    "tests.functional.fixtures.redis_fixtures",
    "tests.functional.fixtures.client_fixtures"
]


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

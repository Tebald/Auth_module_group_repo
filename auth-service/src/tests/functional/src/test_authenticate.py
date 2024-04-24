import json
import time
import uuid
from http import HTTPStatus


from src.tests.functional.fixtures.client_fixtures import api_make_post_request
from src.tests.functional.fixtures.pg_fixtures import User, pg_create_tables, pg_clear_all, pg_insert_table_data
from src.tests.functional.testdata.pg_db_data_input import user_login_data  # noqa: F401

import pytest


@pytest.mark.parametrize('query_data, expected_status', [
    ({'username': 'admin@mail.com', 'password': '123qwe'}, HTTPStatus.OK),
    ({'username': 'admin@mail.com', 'password': 'lalalala'}, HTTPStatus.UNAUTHORIZED),
    ({'username': 'admin@mail.com', 'password': ''}, HTTPStatus.UNPROCESSABLE_ENTITY),
    ({'username': 'billy@mail.com', 'password': '123qwe'}, HTTPStatus.UNAUTHORIZED),
    ({'username': 'admin@mail.com'}, HTTPStatus.UNPROCESSABLE_ENTITY),
    ({'password': '123qwe'}, HTTPStatus.UNPROCESSABLE_ENTITY),

])
@pytest.mark.asyncio
async def test_login_endpoint(
        pg_create_tables,
        pg_clear_all,
        user_login_data,
        pg_insert_table_data,
        api_make_post_request, query_data, expected_status):
    """
    Test for /api/v1/login endpoint.
    Adding one valid user into the DB and then trying to log in
    with different credentials.
    Cookie logic is not tested there.
    """

    await pg_create_tables()

    try:
        data = await user_login_data()
        await pg_insert_table_data(table_name=User, data=data)

        status, body = await api_make_post_request(
            query_data=query_data,
            endpoint='/api/v1/login',
            )

        assert status == expected_status
    finally:
        await pg_clear_all()

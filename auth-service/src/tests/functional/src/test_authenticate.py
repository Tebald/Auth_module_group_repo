import json
import time
import uuid
from http import HTTPStatus


from src.tests.functional.fixtures.client_fixtures import api_make_post_request
from src.tests.functional.fixtures.pg_fixtures import User, pg_create_tables, pg_clear_all, pg_insert_table_data
from src.tests.functional.testdata.pg_db_data_input import user_login_data  # noqa: F401

import pytest

from src.tests.functional.testdata.jwt_tokens import JWTtokens


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

        status, _, _ = await api_make_post_request(
            query_data=query_data,
            endpoint='/api/v1/login',
            )

        assert status == expected_status
    finally:
        await pg_clear_all()


@pytest.mark.parametrize('query_data, expected_status', [
    ({'username': 'admin@mail.com', 'password': '123qwe'}, HTTPStatus.OK),

])
@pytest.mark.asyncio
async def test_response_cookies_login_endpoint(
        pg_create_tables,
        pg_clear_all,
        user_login_data,
        pg_insert_table_data,
        api_make_post_request, query_data, expected_status):
    """
    Test for /api/v1/login endpoint.
    Adding one valid user into the DB and then trying to log in.
    Checking if we received necessary Cookie in the response.
    """

    await pg_create_tables()

    try:
        data = await user_login_data()
        await pg_insert_table_data(table_name=User, data=data)

        status, _, headers = await api_make_post_request(
            query_data=query_data,
            endpoint='/api/v1/login',
            )

        assert status == expected_status

        set_cookies = headers.getall('Set-Cookie')
        # Cheking if there are two Set-Cookie headers in the response
        assert len(set_cookies) == 2
        for cookie in set_cookies:
            # Cheking if Set-Cookie headers contain apropriate token names
            assert 'auth-app-access-key' in cookie or 'auth-app-refresh-key' in cookie
            # Cheking if Cookie configured as HttpOnly.
            assert 'HttpOnly' in cookie

    finally:
        await pg_clear_all()


@pytest.mark.parametrize('query_data, expected_status', [
    ({'username': 'admin@mail.com', 'password': '123qwe'}, HTTPStatus.NO_CONTENT),

])
@pytest.mark.asyncio
async def test_response_cookies_logout_endpoint(
        pg_create_tables,
        pg_clear_all,
        user_login_data,
        pg_insert_table_data,
        api_make_post_request, query_data, expected_status):
    """
    Test for /api/v1/logout endpoint.
    Adding one valid user into the DB and then trying to log out.
    Checking if we received necessary Cookie in the response.
    """

    await pg_create_tables()

    try:
        data = await user_login_data()
        await pg_insert_table_data(table_name=User, data=data)

        jwt = JWTtokens()

        access_token, refresh_token = await jwt.get_token_pair(
            user_id='8ab71a54-7b99-4322-a07e-0b2a0c40ff44',
            session_id='22bd63b2-3d33-45b7-991b-d2e37662426a'
        )

        status, _, headers = await api_make_post_request(
            query_data=query_data,
            endpoint='/api/v1/logout',
            headers={'Cookie': f'auth-app-access-key={access_token} ; auth-app-refresh-key={refresh_token}'}
            )

        assert status == expected_status

        set_cookies = headers.getall('Set-Cookie')
        # Cheking if there are two Set-Cookie headers in the response
        assert len(set_cookies) == 2
        for cookie in set_cookies:
            # Cheking if Set-Cookie headers contain apropriate token names
            assert 'auth-app-access-key' in cookie or 'auth-app-refresh-key' in cookie
            # Cheking if Cookie configured to expire.
            assert 'expires' in cookie

    finally:
        await pg_clear_all()

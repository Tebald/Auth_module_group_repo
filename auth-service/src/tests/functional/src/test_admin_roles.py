import json
import time
import uuid
from http import HTTPStatus

from src.tests.functional.settings import test_base_settings

import pytest

from src.tests.functional.fixtures.client_fixtures import *
from src.tests.functional.fixtures.jwt_fixtures import *
from src.tests.functional.fixtures.pg_fixtures import *
from src.tests.functional.fixtures.redis_fixtures import *


@pytest.mark.asyncio
async def test_dummy():
    assert True


@pytest.mark.asyncio
async def test_add_permission1(client_session, super_user, get_access_token):
    url = f"http://{test_base_settings.service_host}:{test_base_settings.service_port}" \
          "/api/v1/admin/permissions"
    permission_name = "permission.1"
    access_token = await get_access_token(str(super_user.id))

    response = await client_session.post(
        url, 
        json={"name": permission_name}, 
        headers={"cookie": f"auth-app-access-key={access_token}"}
    )

    body = await response.read()
    headers = response.headers
    status = response.status
    res = json.loads(body.decode())

    assert status == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_add_permission2(client_session, super_user, get_access_token):
    url = f"http://{test_base_settings.service_host}:{test_base_settings.service_port}" \
          "/api/v1/admin/permissions"
    permission_name = "permission.2"
    access_token = await get_access_token(str(super_user.id))

    response = await client_session.post(
        url, 
        json={"name": permission_name}, 
        headers={"cookie": f"auth-app-access-key={access_token}"}
    )

    body = await response.read()
    headers = response.headers
    status = response.status
    res = json.loads(body.decode())

    assert status == HTTPStatus.CREATED
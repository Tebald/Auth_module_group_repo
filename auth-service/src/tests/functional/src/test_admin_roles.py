import json
import time
import uuid
from http import HTTPStatus

from src.tests.functional.settings import test_base_settings

from src.models.db_entity import (
    User,
    Role, 
    Permission, 
    RolePermission
)

import pytest


@pytest.mark.asyncio
async def test_add_permission(client_session, super_user, get_access_token):
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
async def test_get_permissions(client_session, 
                               super_user, 
                               get_access_token, 
                               pg_insert_table_data,
                               pg_drop_table_data):
    url = f"http://{test_base_settings.service_host}:{test_base_settings.service_port}" \
          "/api/v1/admin/permissions"
    access_token = await get_access_token(str(super_user.id))
    permission_name = "permission.ABC"

    await pg_drop_table_data(table_name=Permission)
    await pg_insert_table_data(table_name=Permission, data={"name": permission_name})

    response = await client_session.get(
        url,
        headers={"cookie": f"auth-app-access-key={access_token}"}
    )

    body = await response.read()
    headers = response.headers
    status = response.status
    res = json.loads(body.decode())

    assert status == HTTPStatus.OK
    assert res['data'][0]['name'] == permission_name


@pytest.mark.asyncio
async def test_add_role(client_session, super_user, get_access_token):
    url = f"http://{test_base_settings.service_host}:{test_base_settings.service_port}" \
          "/api/v1/admin/roles"
    role_name = "role.1"
    access_token = await get_access_token(str(super_user.id))

    response = await client_session.post(
        url, 
        json={"name": role_name}, 
        headers={"cookie": f"auth-app-access-key={access_token}"}
    )

    body = await response.read()
    headers = response.headers
    status = response.status
    res = json.loads(body.decode())

    assert status == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_get_roles(client_session, 
                         super_user, 
                         get_access_token, 
                         pg_insert_table_data,
                         pg_drop_table_data):
    url = f"http://{test_base_settings.service_host}:{test_base_settings.service_port}" \
          "/api/v1/admin/roles"
    access_token = await get_access_token(str(super_user.id))
    role_name = "role.ABC"

    await pg_drop_table_data(table_name=Role)
    await pg_insert_table_data(table_name=Role, data={"name": role_name})

    response = await client_session.get(
        url,
        headers={"cookie": f"auth-app-access-key={access_token}"}
    )

    body = await response.read()
    headers = response.headers
    status = response.status
    res = json.loads(body.decode())

    assert status == HTTPStatus.OK
    assert res['data'][0]['name'] == role_name
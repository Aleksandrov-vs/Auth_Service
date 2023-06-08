import os
import sys
from http import HTTPStatus

import pytest

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from settings import test_settings

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'query_data, expected_answer, expected_status',
    [
        (
            {'name': 'admin'}, 'admin', HTTPStatus.OK
        )
    ]
)
async def test_role_create(make_get_request, query_data, expected_answer, expected_status):
    url = test_settings.service_url + '/api/v1/auth/roles'

    body, status = await make_get_request(
        url,
        method='POST',
        data=query_data
    )

    assert body['name'] == expected_answer
    assert status == expected_status


@pytest.mark.parametrize(
    'query_data, expected_answer, expected_status',
    [
        (
            {'name': 'admin', 'new_name': 'admin'}, {'message': 'Role already exists.'}, HTTPStatus.OK
        )
    ]
)
async def test_role_update_exists(make_get_request, query_data, expected_answer, expected_status):
    url = test_settings.service_url + '/api/v1/auth/roles/update'

    body, status = await make_get_request(
        url,
        method='PUT',
        data=query_data
    )

    assert body == expected_answer
    assert status == expected_status


@pytest.mark.parametrize(
    'query_data, expected_answer, expected_status',
    [
        (
            {'name': 'admin'}, {'message': 'Role already exists.'}, HTTPStatus.OK
        )
    ]
)
async def test_role_create_replay(make_get_request, query_data, expected_answer, expected_status):
    url = test_settings.service_url + '/api/v1/auth/roles'

    body, status = await make_get_request(
        url,
        method='POST',
        data=query_data
    )

    assert body == expected_answer
    assert status == expected_status


@pytest.mark.parametrize(
    'query_data, expected_answer, expected_status',
    [
        (
            {'name': 'admin', 'new_name': 'like a boss'}, 'like a boss', HTTPStatus.OK
        )
    ]
)
async def test_role_update(make_get_request, query_data, expected_answer, expected_status):
    url = test_settings.service_url + '/api/v1/auth/roles/update'

    body, status = await make_get_request(
        url,
        method='PUT',
        data=query_data
    )

    assert body['name'] == expected_answer
    assert status == expected_status


@pytest.mark.parametrize(
    'expected_answer, expected_status',
    [
        (
            'like a boss', HTTPStatus.OK
        )
    ]
)
async def test_role_viewing(make_get_request, expected_answer, expected_status):
    url = test_settings.service_url + '/api/v1/auth/roles/view'

    body, status = await make_get_request(
        url,
        method='GET'
    )

    assert body['name'] == expected_answer
    assert status == expected_status


@pytest.mark.parametrize(
    'query_data, expected_answer, expected_status',
    [
        (
            {'name': 'like a boss'}, {'message': 'Role successfully deleted.'}, HTTPStatus.OK
        ),
        (
            {'name': 'admin'}, {'message': 'Role does not exists.'}, HTTPStatus.OK
        )
    ]
)
async def test_role_delete(make_get_request, query_data, expected_answer, expected_status):
    url = test_settings.service_url + '/api/v1/auth/roles/delete'

    body, status = await make_get_request(
        url,
        method='DELETE',
        data=query_data
    )

    assert body == expected_answer
    assert status == expected_status


@pytest.mark.parametrize(
    'expected_answer, expected_status',
    [
        (
            {'message': 'No roles was found.'}, HTTPStatus.OK
        )
    ]
)
async def test_role_viewing_reply(make_get_request, expected_answer, expected_status):
    url = test_settings.service_url + '/api/v1/auth/roles/view'

    body, status = await make_get_request(
        url,
        method='GET'
    )

    assert body == expected_answer
    assert status == expected_status

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

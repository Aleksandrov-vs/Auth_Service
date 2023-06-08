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
            {'login': 'not_exist',
             'reg_request_body': {
                 "login": "login",
                 "password": "pass"
             }
             },
            {"message": "User not found."}, HTTPStatus.OK
        ),
(
            {'login': 'login_valid',
             'reg_request_body': {
                 "login": "login_valid",
                 "password": "pass"
             }
             },
            {"login": "login_valid"}, HTTPStatus.OK
        )
    ]
)
async def test_user_find(make_get_request, delete_all_pg_data, query_data, expected_answer, expected_status):
    # регистрация пользователя
    _, reg_status = await make_get_request(
        test_settings.service_url + '/api/v1/auth/register',
        method='POST',
        data=query_data['reg_request_body']
    )
    assert reg_status == HTTPStatus.OK, 'ошибка регистрации'

    # логин
    body, status = await make_get_request(
        test_settings.service_url + '/api/v1/auth/login',
        method='POST',
        data=query_data['reg_request_body']
    )

    if status == HTTPStatus.OK:
        assert 'access_token' in body
        assert 'refresh_token' in body

    token = body['access_token']

    if not query_data.get('headers'):
        headers = {
            "Authorization": f"Bearer {token}"
        }

    url = test_settings.service_url + f'/api/v1/auth/users/{query_data["login"]}'

    body, status = await make_get_request(
        url,
        method='GET',
        headers=headers
    )

    if 'User not found.' != body.get('message'):
        assert expected_answer['login'] in body.get('login')
    else:
        assert body == expected_answer
    assert status == expected_status



# @pytest.mark.parametrize(
#     'query_data, expected_answer, expected_status',
#     [
#         (
#             {'name': 'admin', 'new_name': 'admin'}, {'message': 'Role already exists.'}, HTTPStatus.OK
#         )
#     ]
# )
# async def test_role_update_exists(make_get_request, query_data, expected_answer, expected_status):
#     url = test_settings.service_url + '/api/v1/auth/roles/update'
#
#     body, status = await make_get_request(
#         url,
#         method='PUT',
#         data=query_data
#     )
#
#     assert body == expected_answer
#     assert status == expected_status
#
#
# @pytest.mark.parametrize(
#     'query_data, expected_answer, expected_status',
#     [
#         (
#             {'name': 'admin'}, {'message': 'Role already exists.'}, HTTPStatus.OK
#         )
#     ]
# )
# async def test_role_create_replay(make_get_request, query_data, expected_answer, expected_status):
#     url = test_settings.service_url + '/api/v1/auth/roles'
#
#     body, status = await make_get_request(
#         url,
#         method='POST',
#         data=query_data
#     )
#
#     assert body == expected_answer
#     assert status == expected_status
#
#
# @pytest.mark.parametrize(
#     'query_data, expected_answer, expected_status',
#     [
#         (
#             {'name': 'admin', 'new_name': 'like a boss'}, 'like a boss', HTTPStatus.OK
#         )
#     ]
# )
# async def test_role_update(make_get_request, query_data, expected_answer, expected_status):
#     url = test_settings.service_url + '/api/v1/auth/roles/update'
#
#     body, status = await make_get_request(
#         url,
#         method='PUT',
#         data=query_data
#     )
#
#     assert body['name'] == expected_answer
#     assert status == expected_status
#
#
# @pytest.mark.parametrize(
#     'expected_answer, expected_status',
#     [
#         (
#             'like a boss', HTTPStatus.OK
#         )
#     ]
# )
# async def test_role_viewing(make_get_request, expected_answer, expected_status):
#     url = test_settings.service_url + '/api/v1/auth/roles/view'
#
#     body, status = await make_get_request(
#         url,
#         method='GET'
#     )
#
#     assert body['name'] == expected_answer
#     assert status == expected_status
#
#
# @pytest.mark.parametrize(
#     'query_data, expected_answer, expected_status',
#     [
#         (
#             {'name': 'like a boss'}, {'message': 'Role successfully deleted.'}, HTTPStatus.OK
#         ),
#         (
#             {'name': 'admin'}, {'message': 'Role does not exists.'}, HTTPStatus.OK
#         )
#     ]
# )
# async def test_role_delete(make_get_request, query_data, expected_answer, expected_status):
#     url = test_settings.service_url + '/api/v1/auth/roles/delete'
#
#     body, status = await make_get_request(
#         url,
#         method='DELETE',
#         data=query_data
#     )
#
#     assert body == expected_answer
#     assert status == expected_status
#
#
# @pytest.mark.parametrize(
#     'expected_answer, expected_status',
#     [
#         (
#             {'message': 'No roles was found.'}, HTTPStatus.OK
#         )
#     ]
# )
# async def test_role_viewing_reply(make_get_request, expected_answer, expected_status):
#     url = test_settings.service_url + '/api/v1/auth/roles/view'
#
#     body, status = await make_get_request(
#         url,
#         method='GET'
#     )
#
#     assert body == expected_answer
#     assert status == expected_status

import asyncio
import json

import aiohttp
import pytest
import pytest_asyncio
import sqlalchemy
from redis.asyncio import Redis
from sqlalchemy import create_engine, text

from functional.settings import test_settings


@pytest.fixture(scope='session')
def pg_engine():
    engine = create_engine(f"postgresql://{test_settings.pg_user}:"
                           f"{test_settings.pg_password}@{test_settings.pg_host}"
                           f":{test_settings.pg_port}/{test_settings.dbname}")
    yield engine


@pytest.fixture(scope="session", autouse=True)
def delete_all_pg_data(pg_engine: sqlalchemy.Engine):
    def delete(engine):
        table_names = [
            "auth_history",
            "user_role",
            "roles",
            "users",
        ]

        with engine.begin() as connection:
            for table in table_names:
                query = text(f"TRUNCATE {table} RESTART IDENTITY CASCADE;")
                connection.execute(
                    query
                )

    delete(pg_engine)
    yield
    delete(pg_engine)


# @pytest.fixture(scope="session", autouse=True)
# def super_user(session_client: aiohttp.ClientSession, pg_engine: sqlalchemy.Engine):
#
#     pass



@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='function')
async def session_client():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(scope="session")
async def redis_client():
    client = Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    yield client
    await client.close()


@pytest.fixture(scope='function')
def make_get_request(session_client: aiohttp.ClientSession):
    async def inner(
            url: str, params: dict = None,
            method: str = 'GET', data: dict = None, headers: dict = None):

        if method == 'GET':
            async with session_client.get(url, params=params, headers=headers) as response:
                body = await response.json()
                status = response.status
                return body, status

        if method == 'POST':
            async with session_client.post(url, json=data, headers=headers) as response:
                body = await response.json()
                status = response.status
                return body, status

        if method == 'DELETE':
            async with session_client.delete(url, json=data) as response:
                body = await response.json()
                status = response.status
                return body, status

        if method == 'PUT':
            async with session_client.put(url, json=data) as response:
                body = await response.json()
                status = response.status
                return body, status


    return inner

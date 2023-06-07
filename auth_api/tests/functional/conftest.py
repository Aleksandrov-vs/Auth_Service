import asyncio
import aiohttp
import pytest
import pytest_asyncio


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


@pytest.fixture(scope='function')
def make_get_request(session_client: aiohttp.ClientSession):
    async def inner(
            url: str, params: dict = None, method: str = None, data: dict = None):

        if method == 'GET' or method == None:
            async with session_client.get(url, params=params) as response:
                body = await response.json()
                status = response.status
                return body, status

        if method == 'POST':
            async with session_client.post(url, json=data) as response:
                body = await response.json()
                status = response.status
                return body, status


    return inner

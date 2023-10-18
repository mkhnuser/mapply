import asyncio

import pytest
from pytest_aiohttp.plugin import AiohttpClient
from aiohttp.test_utils import TestClient

from logic.app import create_app


@pytest.fixture
def client(
    event_loop: asyncio.AbstractEventLoop,
    aiohttp_client: AiohttpClient
) -> TestClient:
    return event_loop.run_until_complete(aiohttp_client(create_app()))

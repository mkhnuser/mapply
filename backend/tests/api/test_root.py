from http import HTTPStatus

from aiohttp.test_utils import TestClient

from logic.routes import Routes


async def test_root(client: TestClient) -> None:
    response = await client.get(Routes.ROOT.value.route)
    assert response.status == HTTPStatus.NOT_FOUND.value

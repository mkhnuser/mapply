import asyncio
import random
from typing import cast, Any
from http import HTTPStatus
from collections.abc import (
    Generator,
    AsyncGenerator,
    MutableMapping
)

import pytest
import asyncpg
from aiohttp import web
from aiohttp.test_utils import TestClient
from pytest_aiohttp.plugin import AiohttpClient

from logic.app import create_app
from logic.routes import Routes
from logic.services import (
    create_map_event, delete_map_event, prepare_map_event_record
)
from logic.validation import MapEventModel


@pytest.fixture
def client(
    event_loop: asyncio.AbstractEventLoop,
    aiohttp_client: AiohttpClient
) -> TestClient:
    return event_loop.run_until_complete(aiohttp_client(create_app()))


@pytest.fixture
def random_map_event_model() -> Generator[MapEventModel, None, None]:
    random_map_event_model = MapEventModel(**{
        "title": "_" * random.randint(1, 64),
        "description": "_" * random.randint(1, 512),
        "position": {
            "lat": random.randint(-90, 90),
            "lng": random.randint(-180, 180),
        }
    })
    yield random_map_event_model


@pytest.fixture
async def database_map_event_model(
    client: TestClient,
    random_map_event_model: MapEventModel
) -> AsyncGenerator[MapEventModel, None]:
    pool: asyncpg.Pool = cast(
        web.Application,
        client.app
    )["database_connection_pool"]
    map_event_model = MapEventModel(
        **prepare_map_event_record(
            await create_map_event(pool, random_map_event_model)
        )
    )
    yield map_event_model
    await delete_map_event(pool, cast(int, map_event_model.id))


async def test_root(client: TestClient) -> None:
    response = await client.get(Routes.ROOT.value.route)
    assert response.status == HTTPStatus.NOT_FOUND.value


async def test_get_map_event(
    client: TestClient,
    database_map_event_model: MapEventModel
) -> None:
    response = await client.get(
        Routes.GET_MAP_EVENT.value.route.format(
            id=cast(int, database_map_event_model.id)
        )
    )
    assert response.status == HTTPStatus.OK.value
    assert database_map_event_model.model_dump(mode="json") == (
        MapEventModel(**(await response.json())).model_dump(mode="json")
    )


async def test_get_non_existing_map_event(client: TestClient) -> None:
    response = await client.get(
        Routes.GET_MAP_EVENT.value.route.format(id="-1")
    )
    assert response.status == HTTPStatus.NOT_FOUND.value
    assert not (await response.text())


async def test_get_map_event_passing_invalid_id(client: TestClient) -> None:
    for coro in asyncio.as_completed(
        tuple(
            client.get(Routes.GET_MAP_EVENT.value.route.format(id=id))
            for id in ("_", "-inf", "inf", "NaN", "1e+2", "1e-2", "0.1")
        )
    ):
        response = await coro
        assert response.status == HTTPStatus.BAD_REQUEST.value
        assert not (await response.text())


async def test_post_map_event(
    client: TestClient,
    random_map_event_model: MapEventModel
) -> None:
    response = await client.post(
        Routes.POST_MAP_EVENT.value.route,
        json=random_map_event_model.model_dump(mode="json")
    )

    assert response.status == HTTPStatus.OK.value
    data: MutableMapping[str, Any] = await response.json()
    data.pop("id")
    assert random_map_event_model.model_dump(mode="json") == (
        MapEventModel(**data).model_dump(mode="json")
    )


async def test_post_map_event_not_passing_payload(client: TestClient) -> None:
    response = await client.post(Routes.POST_MAP_EVENT.value.route)
    assert response.status == HTTPStatus.BAD_REQUEST.value
    assert not (await response.text())


async def test_put_map_event(
    client: TestClient,
    database_map_event_model: MapEventModel,
    random_map_event_model: MapEventModel
) -> None:
    response = await client.put(
        Routes.PUT_MAP_EVENT.value.route.format(id=database_map_event_model.id),
        json=random_map_event_model.model_dump(mode="json")
    )
    assert response.status == HTTPStatus.OK.value
    data: MutableMapping[str, Any] = await response.json()
    assert data.pop("id") == database_map_event_model.id
    assert random_map_event_model.model_dump(mode="json") == (
        MapEventModel(**data).model_dump(mode="json")
    )


async def test_put_map_event_not_passing_payload(
    client: TestClient,
    database_map_event_model: MapEventModel
) -> None:
    response = await client.put(
        Routes.PUT_MAP_EVENT.value.route.format(id=database_map_event_model.id),
    )
    assert response.status == HTTPStatus.BAD_REQUEST.value
    assert not (await response.text())


async def test_put_non_existing_map_event(
    client: TestClient,
    random_map_event_model: MapEventModel
) -> None:
    response = await client.put(
        Routes.PUT_MAP_EVENT.value.route.format(id="-1"),
        json=random_map_event_model.model_dump(mode="json")
    )
    assert response.status == HTTPStatus.BAD_REQUEST.value
    assert not (await response.text())


async def test_delete_map_event(
    client: TestClient,
    database_map_event_model: MapEventModel
) -> None:
    response = await client.delete(
        Routes.DELETE_MAP_EVENT.value.route.format(id=database_map_event_model.id)
    )
    assert response.status == HTTPStatus.OK.value
    data: MutableMapping[str, Any] = await response.json()
    assert data.pop("id") == database_map_event_model.id


async def test_delete_non_existing_map_event(client: TestClient) -> None:
    response = await client.delete(
        Routes.DELETE_MAP_EVENT.value.route.format(id="-1")
    )
    assert response.status == HTTPStatus.BAD_REQUEST.value
    assert not (await response.text())

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

from logic.routes import Routes
from logic.services import create_map_event, prepare_map_event_record
from logic.validation import MapEventModel


@pytest.fixture(autouse=True)
async def empty_map_events_table(
    client: TestClient
) -> AsyncGenerator[None, None]:
    await cast(
        asyncpg.Pool,
        client.app["database_connection_pool"]
    ).execute("DELETE FROM map_events;")
    yield


@pytest.fixture
def map_event_model() -> Generator[MapEventModel, None, None]:
    yield MapEventModel(**{
        "title": "_" * random.randint(1, 64),
        "description": "_" * random.randint(1, 512),
        "position": {
            "lat": random.randint(-90, 90),
            "lng": random.randint(-180, 180),
        }
    })


@pytest.fixture
async def map_event_model_which_is_saved_in_the_database(
    client: TestClient,
    map_event_model: MapEventModel
) -> AsyncGenerator[MapEventModel, None]:
    pool: asyncpg.Pool = cast(
        web.Application,
        client.app
    )["database_connection_pool"]
    yield MapEventModel(
        **prepare_map_event_record(
            await create_map_event(pool, map_event_model)
        )
    )


async def test_get_map_event(
    client: TestClient,
    map_event_model_which_is_saved_in_the_database: MapEventModel
) -> None:
    assert (
        await client.get(
            Routes.GET_MAP_EVENT.value.route.format(
                id=cast(int, map_event_model_which_is_saved_in_the_database.id)
            )
        )
    ).status == HTTPStatus.OK.value


@pytest.mark.parametrize(
    "invalid_id",
    ("-inf", "inf", "NaN", "1e+2", "1e-2", "0.1", "_", "ＵＮＩＣＯＤＥ")
)
async def test_get_map_event_passing_invalid_id(
    client: TestClient,
    invalid_id: str
) -> None:
    response = await client.get(
        Routes.GET_MAP_EVENT.value.route.format(id=invalid_id)
    )
    assert response.status == HTTPStatus.BAD_REQUEST.value
    assert not (await response.text())


async def test_get_map_event_returns_valid_payload(
    client: TestClient,
    map_event_model_which_is_saved_in_the_database: MapEventModel
) -> None:
    response = await client.get(
        Routes.GET_MAP_EVENT.value.route.format(
            id=cast(int, map_event_model_which_is_saved_in_the_database.id)
        )
    )
    assert map_event_model_which_is_saved_in_the_database.model_dump(
        mode="json"
    ) == MapEventModel(**(await response.json())).model_dump(mode="json")


async def test_get_non_existing_map_event(client: TestClient) -> None:
    response = await client.get(
        Routes.GET_MAP_EVENT.value.route.format(id="-1")
    )
    assert response.status == HTTPStatus.NOT_FOUND.value
    assert not (await response.text())


async def test_get_map_events(client: TestClient) -> None:
    response = await client.get(Routes.GET_MAP_EVENTS.value.route)
    assert response.status == HTTPStatus.OK.value


async def test_get_map_events_returns_valid_payload(
    client: TestClient,
    map_event_model_which_is_saved_in_the_database: MapEventModel
) -> None:
    response = await client.get(Routes.GET_MAP_EVENTS.value.route)
    data: list[MutableMapping[str, Any]] = await response.json()
    for map_event_json_representation in data:
        map_event_model = MapEventModel(**map_event_json_representation)
        for field in MapEventModel.model_fields.keys():
            assert getattr(map_event_model, field) == getattr(
                map_event_model_which_is_saved_in_the_database,
                field
            )


async def test_post_map_event(
    client: TestClient,
    map_event_model: MapEventModel
) -> None:
    assert (
        await client.post(
            Routes.POST_MAP_EVENT.value.route,
            json=map_event_model.model_dump(mode="json")
        )
    ).status == HTTPStatus.OK.value


async def test_post_map_event_returns_valid_payload(
    client: TestClient,
    map_event_model: MapEventModel
) -> None:
    response = await client.post(
        Routes.POST_MAP_EVENT.value.route,
        json=map_event_model.model_dump(mode="json")
    )
    data: MutableMapping[str, Any] = await response.json()
    assert data.pop("id") > 0
    assert map_event_model.model_dump(mode="json") == (
        MapEventModel(**data).model_dump(mode="json")
    )


@pytest.mark.parametrize("invalid_payload", ("", {}, None, "_", "ＵＮＩＣＯＤＥ"))
async def test_post_map_event_passing_invalid_payload(
    client: TestClient,
    invalid_payload: Any
) -> None:
    response = await client.post(
        Routes.POST_MAP_EVENT.value.route,
        json=invalid_payload
    )
    assert response.status == HTTPStatus.BAD_REQUEST.value
    assert not (await response.text())


async def test_post_map_event_not_passing_payload(client: TestClient) -> None:
    response = await client.post(Routes.POST_MAP_EVENT.value.route)
    assert response.status == HTTPStatus.BAD_REQUEST.value
    assert not (await response.text())


async def test_put_map_event(
    client: TestClient,
    map_event_model_which_is_saved_in_the_database: MapEventModel,
    map_event_model: MapEventModel
) -> None:
    assert (
        await client.put(
            Routes.PUT_MAP_EVENT.value.route.format(
                id=map_event_model_which_is_saved_in_the_database.id
            ),
            json=map_event_model.model_dump(mode="json")
        )
    ).status == HTTPStatus.OK.value


async def test_put_map_event_returns_valid_payload(
    client: TestClient,
    map_event_model_which_is_saved_in_the_database: MapEventModel,
    map_event_model: MapEventModel
) -> None:
    response = await client.put(
        Routes.PUT_MAP_EVENT.value.route.format(
            id=map_event_model_which_is_saved_in_the_database.id
        ),
        json=map_event_model.model_dump(mode="json")
    )
    data: MutableMapping[str, Any] = await response.json()
    assert data.pop("id") == map_event_model_which_is_saved_in_the_database.id
    assert map_event_model.model_dump(mode="json") == (
        MapEventModel(**data).model_dump(mode="json")
    )


@pytest.mark.parametrize("invalid_payload", ("", {}, None, "_", "ＵＮＩＣＯＤＥ"))
async def test_put_map_event_passing_invalid_payload(
    client: TestClient,
    map_event_model_which_is_saved_in_the_database: MapEventModel,
    invalid_payload: Any
) -> None:
    response = await client.put(
        Routes.PUT_MAP_EVENT.value.route.format(
            id=map_event_model_which_is_saved_in_the_database.id
        ),
        json=invalid_payload
    )
    assert response.status == HTTPStatus.BAD_REQUEST.value
    assert not (await response.text())


async def test_put_map_event_not_passing_payload(
    client: TestClient,
    map_event_model_which_is_saved_in_the_database: MapEventModel
) -> None:
    response = await client.put(
        Routes.PUT_MAP_EVENT.value.route.format(
            id=map_event_model_which_is_saved_in_the_database.id
        )
    )
    assert response.status == HTTPStatus.BAD_REQUEST.value
    assert not (await response.text())


async def test_put_non_existing_map_event(
    client: TestClient,
    map_event_model: MapEventModel
) -> None:
    response = await client.put(
        Routes.PUT_MAP_EVENT.value.route.format(id="-1"),
        json=map_event_model.model_dump(mode="json")
    )
    assert response.status == HTTPStatus.BAD_REQUEST.value
    assert not (await response.text())


async def test_delete_map_event(
    client: TestClient,
    map_event_model_which_is_saved_in_the_database: MapEventModel
) -> None:
    assert (
        await client.delete(
            Routes.DELETE_MAP_EVENT.value.route.format(
                id=map_event_model_which_is_saved_in_the_database.id
            )
        )
    ).status == HTTPStatus.OK.value


async def test_delete_map_event_returns_valid_payload(
    client: TestClient,
    map_event_model_which_is_saved_in_the_database: MapEventModel
) -> None:
    response = await client.delete(
        Routes.DELETE_MAP_EVENT.value.route.format(
            id=map_event_model_which_is_saved_in_the_database.id
        )
    )
    data: MutableMapping[str, Any] = await response.json()
    assert map_event_model_which_is_saved_in_the_database.model_dump(
        mode="json"
    ) == (
        MapEventModel(**data).model_dump(mode="json")
    )


async def test_delete_non_existing_map_event(client: TestClient) -> None:
    response = await client.delete(
        Routes.DELETE_MAP_EVENT.value.route.format(id="-1")
    )
    assert response.status == HTTPStatus.BAD_REQUEST.value
    assert not (await response.text())

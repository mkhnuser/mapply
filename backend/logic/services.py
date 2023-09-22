from typing import Optional
from collections.abc import MutableMapping

import asyncpg

from .validation import MapEventModel


async def retrieve_map_event(
    pool: asyncpg.Pool,
    map_event_id: int
) -> Optional[asyncpg.Record]:
    return await pool.fetchrow(
        "SELECT id, title, description, lat, lng FROM map_events WHERE id=$1;",
        map_event_id,
    )


async def create_map_event(
    pool: asyncpg.Pool,
    map_event_model: MapEventModel
) -> asyncpg.Record:
    return await pool.fetchrow(
        "INSERT INTO map_events(title, description, lat, lng)"
        " VALUES ($1, $2, $3, $4)"
        " RETURNING *;",
        map_event_model.title,
        map_event_model.description,
        map_event_model.position.lat,
        map_event_model.position.lng,
    )


async def update_map_event(
    pool: asyncpg.Pool,
    map_event_model: MapEventModel,
    id: int
) -> asyncpg.Record:
    return await pool.fetchrow(
        "UPDATE map_events"
        " SET title = $1, description = $2, lat = $3, lng = $4"
        " WHERE id = $5"
        " RETURNING *;",
        map_event_model.title,
        map_event_model.description,
        map_event_model.position.lat,
        map_event_model.position.lng,
        id,
    )


async def delete_map_event(pool: asyncpg.Pool, id: int) -> asyncpg.Record:
    return await pool.fetchrow(
        "DELETE FROM map_events WHERE id = $1 RETURNING *;",
        id
    )


def prepare_map_event_record(
    map_event_record: asyncpg.Record
) -> MutableMapping:
    map_event: MutableMapping = dict(map_event_record)
    position = {
        "position": {
            "lat": map_event.pop("lat"),
            "lng": map_event.pop("lng")
        }
    }
    return {**map_event, **position}

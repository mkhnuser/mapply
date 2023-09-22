import os
import logging
from collections.abc import AsyncGenerator

import asyncpg
from aiohttp import web


from .handlers import (
    handle_get_map_event,
    handle_post_map_event,
    handle_put_map_event,
    handle_delete_map_event
)
from .routes import Routes


async def init_db_connection_pool(
    app: web.Application
) -> AsyncGenerator[None, None]:
    async with asyncpg.create_pool(os.environ["MAPPLY_DATABASE_URL"]) as pool:
        app["database_connection_pool"] = pool
        yield


def create_app() -> web.Application:
    app = web.Application()
    app.add_routes([
        web.get(
            Routes.GET_MAP_EVENT.value.route,
            handle_get_map_event,
            name=Routes.GET_MAP_EVENT.value.name
        ),
        web.post(
            Routes.POST_MAP_EVENT.value.route,
            handle_post_map_event,
            name=Routes.POST_MAP_EVENT.value.name
        ),
        web.put(
            Routes.PUT_MAP_EVENT.value.route,
            handle_put_map_event,
            name=Routes.PUT_MAP_EVENT.value.name
        ),
        web.delete(
            Routes.DELETE_MAP_EVENT.value.route,
            handle_delete_map_event,
            name=Routes.DELETE_MAP_EVENT.value.name
        ),
    ])
    app.cleanup_ctx.append(init_db_connection_pool)
    return app


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(create_app())

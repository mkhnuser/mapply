import logging
from http import HTTPStatus
from json import JSONDecodeError

from aiohttp import web
from pydantic import ValidationError

from .validation import MapEventModel
from .services import (
    retrieve_map_event,
    retrieve_map_events,
    create_map_event,
    update_map_event,
    delete_map_event,
    prepare_map_event_record
)
from .exceptions import AsyncPGError


async def handle_get_map_event(request: web.Request) -> web.Response:
    try:
        map_event_record = await retrieve_map_event(
            request.app["database_connection_pool"],
            int(request.match_info["id"])
        )
    except ValueError:
        logging.error(
            "Error occured during type conversion."
            f""" Failed to convert {request.match_info["id"]} to int."""
        )
        return web.Response(status=HTTPStatus.BAD_REQUEST.value)
    except AsyncPGError:
        logging.error("Error occured during database operation.")
        return web.Response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value)

    if not map_event_record:
        return web.Response(status=HTTPStatus.NOT_FOUND.value)

    return web.json_response(
        prepare_map_event_record(map_event_record),
        headers={"Access-Control-Allow-Origin": "*"}
    )


async def handle_get_map_events(request: web.Request) -> web.Response:
    try:
        map_event_records = await retrieve_map_events(
            request.app["database_connection_pool"]
        )
    except AsyncPGError:
        logging.error("Error occured during database operation.")
        return web.Response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value)

    return web.json_response(
        [
            prepare_map_event_record(map_event_record) 
            for map_event_record in map_event_records
        ],
        headers={"Access-Control-Allow-Origin": "*"}
    )


async def handle_post_map_event(request: web.Request) -> web.Response:
    try:
        map_event_model = MapEventModel(**(await request.json()))
    except (JSONDecodeError, TypeError, ValidationError):
        # NOTE: Handle TypeError since (await request.json())
        # Might result in an object which cannot be used with **.
        logging.error("Error occured during validation.")
        return web.Response(status=HTTPStatus.BAD_REQUEST.value)

    try:
        map_event_record = await create_map_event(
            request.app["database_connection_pool"],
            map_event_model
        )
    except AsyncPGError:
        logging.error("Error occured during database operation.")
        return web.Response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value)

    return web.json_response(prepare_map_event_record(map_event_record))


async def handle_put_map_event(request: web.Request) -> web.Response:
    try:
        map_event_model = MapEventModel(**(await request.json()))
    except (JSONDecodeError, TypeError, ValidationError):
        # NOTE: Handle TypeError since (await request.json())
        # Might result in an object which cannot be used with **.
        logging.error("Error occured during validation.")
        return web.Response(status=HTTPStatus.BAD_REQUEST.value)

    try:
        map_event_record = await update_map_event(
            request.app["database_connection_pool"],
            map_event_model,
            int(request.match_info["id"])
        )
    except ValueError:
        logging.error(
            "Error occured during type conversion."
            f""" Failed to convert {request.match_info["id"]} to int."""
        )
        return web.Response(status=HTTPStatus.BAD_REQUEST.value)
    except AsyncPGError:
        logging.error("Error occured during database operation.")
        return web.Response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value)

    if not map_event_record:
        return web.Response(status=HTTPStatus.BAD_REQUEST.value)

    return web.json_response(prepare_map_event_record(map_event_record))


async def handle_delete_map_event(request: web.Request) -> web.Response:
    try:
        map_event_record = await delete_map_event(
            request.app["database_connection_pool"],
            int(request.match_info["id"])
        )
    except ValueError:
        logging.error(
            "Error occured during type conversion."
            f""" Failed to convert {request.match_info["id"]} to int."""
        )
        return web.Response(status=HTTPStatus.BAD_REQUEST.value)
    except AsyncPGError:
        logging.error("Error occured during database operation.")
        return web.Response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value)

    if not map_event_record:
        return web.Response(status=HTTPStatus.BAD_REQUEST.value)

    return web.json_response(prepare_map_event_record(map_event_record))

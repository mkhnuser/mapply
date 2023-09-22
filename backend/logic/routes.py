import enum
from typing import NamedTuple


class Route(NamedTuple):
    route: str
    name: str


class Routes(enum.Enum):
    ROOT = Route("/", "ROOT")
    GET_MAP_EVENT = Route("/api/v1/map/events/{id}", "GET_MAP_EVENT_ROUTE")
    POST_MAP_EVENT = Route("/api/v1/map/events", "POST_MAP_EVENT_ROUTE")
    PUT_MAP_EVENT = Route("/api/v1/map/events/{id}", "PUT_MAP_EVENT_ROUTE")
    DELETE_MAP_EVENT = Route("/api/v1/map/events/{id}", "DELETE_MAP_EVENT_ROUTE")

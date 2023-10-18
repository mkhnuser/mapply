export enum ClientRoutes {
  /* Defines client routes which are used for internal app navigation. */

  ROOT = "/",
  LOGIN = "/login",
  SIGNUP = "/singup",
}

export enum ServerRoutes {
  /* Defines API routes which are used for requests to the server. */

  // Will be used with a particular id.
  // For example, "http://localhost:8080/api/v1/map/events/1".
  MAP_EVENT = "http://localhost:8080/api/v1/map/events",
  // Will be used to retrieve all available map events.
  MAP_EVENTS = "http://localhost:8080/api/v1/map/events",
}

import { useQuery } from "react-query";

import ControlPanel from "../control_panel/ControlPanel";
import Map from "../map/Map";
import { ServerRoutes } from "../../routes";
import type { MapEvent } from "../../types";

export default function Content() {
  const {
    isLoading,
    error,
    data: mapEvents,
  } = useQuery<MapEvent[]>("mapEvents", () =>
    fetch(ServerRoutes.MAP_EVENTS).then((res) => res.json())
  );

  if (isLoading) return <h1>Loading...</h1>;
  if (error) return <h1>Error has happened.</h1>;

  return (
    <main className="flex flex-1">
      {mapEvents && <ControlPanel mapEvents={mapEvents} />}
      {mapEvents && <Map mapEvents={mapEvents} />}
    </main>
  );
}

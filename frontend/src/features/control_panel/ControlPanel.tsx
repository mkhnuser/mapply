import { LatLngLiteral } from "leaflet";

import EventItem from "./EventItem";
import { MapEvent } from "../../types";

export default function ControlPanel({ mapEvents }: { mapEvents: MapEvent[] }) {
  return (
    <aside className="w-1/4 bg-gray-100 h-full">
      <ul className="mx-4 my-4 flex flex-col gap-2">
        {mapEvents.map((mapEvent, i) => {
          return <EventItem position={mapEvent.position} key={i} />;
        })}
      </ul>
    </aside>
  );
}

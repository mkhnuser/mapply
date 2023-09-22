import { LatLngLiteral } from "leaflet";
import EventItem from "./EventItem";

export default function ControlPanel({
  positions,
}: {
  positions: LatLngLiteral[];
}) {
  return (
    <aside className="w-1/4 bg-gray-100 h-full">
      <ul className="mx-4 my-4 flex flex-col gap-2">
        {positions.map((pos, i) => {
          return <EventItem position={pos} key={i} />;
        })}
      </ul>
    </aside>
  );
}

import { LatLngLiteral } from "leaflet";

export default function EventItem({ position }: { position: LatLngLiteral }) {
  return (
    <li
      className="px-2 py-2 bg-gray-200"
      onMouseOver={(e) => {}}
    >{`${position.lat} - ${position.lng}`}</li>
  );
}

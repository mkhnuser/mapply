import ControlPanel from "../features/control_panel/ControlPanel";
import Map from "../features/map/Map";
import { LatLngLiteral } from "leaflet";

export default function Content({ positions }: { positions: LatLngLiteral[] }) {
  return (
    <main className="flex flex-1">
      <ControlPanel positions={positions} />
      <Map positions={positions} />
    </main>
  );
}

import { LatLngLiteral } from "leaflet";

export interface MapEvent {
  id: number;
  title: string;
  description: string;
  position: LatLngLiteral;
}

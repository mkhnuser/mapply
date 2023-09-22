import { LatLngLiteral } from "leaflet";

export interface MapEvent {
  title: string;
  description: string;
  position: LatLngLiteral;
}

export interface MapEventsResponse {
  events: MapEvent[];
}

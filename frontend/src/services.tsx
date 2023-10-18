import { Marker, Popup } from "react-leaflet";
import markerIconPng from "leaflet/dist/images/marker-icon.png";
import { Icon } from "leaflet";

import { MapEvent } from "./types";

export function createMapEventMarkers(mapEvents: MapEvent[]): JSX.Element[] {
  return mapEvents.map((mapEvent, i) => {
    return (
      <Marker
        key={i}
        position={mapEvent.position}
        icon={
          new Icon({
            iconUrl: markerIconPng,
            iconSize: [25, 41],
            iconAnchor: [12, 41],
          })
        }
      >
        <Popup>
          A pretty CSS3 popup. <br /> Easily customizable.
        </Popup>
      </Marker>
    );
  });
}

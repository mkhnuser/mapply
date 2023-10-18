import { useState } from "react";
import { MapContainer, TileLayer } from "react-leaflet";
import { Marker, Popup } from "react-leaflet";
import { useMapEvent } from "react-leaflet";
import { LeafletMouseEvent } from "leaflet";
import { Icon } from "leaflet";
import markerIconPng from "leaflet/dist/images/marker-icon.png";

import { createMapEventMarkers } from "../../services";
import { MapEvent } from "../../types";

function _Map({ mapEvents }: { mapEvents: MapEvent[] }) {
  const [mapEventsMarkers, _] = useState<JSX.Element[]>(
    createMapEventMarkers(mapEvents)
  );
  const [currentMapEventMarker, setCurrentMapEventMarker] =
    useState<JSX.Element | null>(null);

  const map = useMapEvent("click", (event: LeafletMouseEvent): void => {
    setCurrentMapEventMarker(
      <Marker
        key={event.latlng.toString()}
        position={event.latlng}
        icon={
          new Icon({
            iconUrl: markerIconPng,
            iconSize: [25, 41],
            iconAnchor: [12, 41],
          })
        }
      >
        <Popup>What would you like to add here?</Popup>
      </Marker>
    );
  });

  return (
    <>
      {mapEventsMarkers}
      {currentMapEventMarker}
    </>
  );
}

export default function Map({ mapEvents }: { mapEvents: MapEvent[] }) {
  return (
    <div id="map" className="w-full h-full">
      <MapContainer
        center={mapEvents[0].position}
        zoom={4}
        scrollWheelZoom={false}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <_Map mapEvents={mapEvents} />
      </MapContainer>
    </div>
  );
}

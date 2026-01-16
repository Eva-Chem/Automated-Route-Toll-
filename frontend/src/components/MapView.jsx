import { MapContainer, TileLayer, Marker, Polygon } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const DRIVER_POSITION = [-1.283, 36.82];

const ZONE_COORDS = [
  [-1.280, 36.818],
  [-1.280, 36.826],
  [-1.288, 36.826],
  [-1.288, 36.818]
];

const markerIcon = new L.Icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});

export default function MapView() {
  return (
    <MapContainer
      center={DRIVER_POSITION}
      zoom={14}
      style={{ height: "100%", width: "100%" }}
    >
      <TileLayer
        attribution="© OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <Marker position={DRIVER_POSITION} icon={markerIcon} />

      <Polygon
        positions={ZONE_COORDS}
        pathOptions={{
          color: "#2563EB",
          fillColor: "#93C5FD",
          fillOpacity: 0.4
        }}
      />
    </MapContainer>
  );
}

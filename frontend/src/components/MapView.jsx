import {
  MapContainer,
  TileLayer,
  Marker,
  Polygon,
  Popup,
  useMap
} from "react-leaflet";
import { useEffect, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

const driverIcon = new L.Icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});

const START_POSITION = [-1.3005, 36.7896];

const RecenterMap = ({ position }) => {
  const map = useMap();
  useEffect(() => {
    map.setView(position, 16);
  }, [position, map]);
  return null;
};

const MapView = ({ onTollTriggered }) => {
  const [position] = useState(START_POSITION);
  const [zones, setZones] = useState([]);

  useEffect(() => {
    fetch(`${API_BASE}/api/toll-zones`)
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          const formatted = data.data.map((z) => ({
            ...z,
            coordinates: z.coordinates.map((c) => [c.lat, c.lng])
          }));
          setZones(formatted);

          // Demo: trigger first zone
          onTollTriggered(formatted[0]);
        }
      })
      .catch(() => {
        console.warn("Failed to load toll zones");
      });
  }, [onTollTriggered]);

  return (
    <MapContainer
      center={position}
      zoom={16}
      style={{ height: "360px", width: "100%", zIndex: 1 }}
    >
      <RecenterMap position={position} />

      <TileLayer
        attribution="© OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <Marker position={position} icon={driverIcon}>
        <Popup>You are here</Popup>
      </Marker>

      {zones.map((zone) => (
        <Polygon
          key={zone.id}
          positions={zone.coordinates}
          pathOptions={{
            color: "#DC2626",
            fillColor: "#FCA5A5",
            fillOpacity: 0.5
          }}
        >
          <Popup>
            <strong>{zone.name}</strong>
            <br />
            KES {zone.charge_amount}
          </Popup>
        </Polygon>
      ))}
    </MapContainer>
  );
};

export default MapView;

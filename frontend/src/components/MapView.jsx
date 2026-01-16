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

/* ================= ICON ================= */

const driverIcon = new L.Icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});

const DRIVER_START_POSITION = [-1.283, 36.82];

/* ================= HELPERS ================= */

const RecenterToZones = ({ zones }) => {
  const map = useMap();

  useEffect(() => {
    if (!zones.length) return;

    const bounds = L.latLngBounds(
      zones.flatMap((zone) => zone.coordinates)
    );

    map.fitBounds(bounds, { padding: [80, 80] });
  }, [zones, map]);

  return null;
};

/* ================= COMPONENT ================= */

const MapView = ({ onTollTriggered }) => {
  const [zones, setZones] = useState([]);
  const [driverPosition] = useState(DRIVER_START_POSITION);

  useEffect(() => {
    const fetchZones = async () => {
      const res = await fetch("/api/toll-zones");
      const data = await res.json();

      if (data.success) {
        const formatted = data.data.map((z) => ({
          id: z.id,
          name: z.name,
          charge_amount: z.charge_amount,
          coordinates: z.coordinates.map((c) => [c.lat, c.lng])
        }));

        setZones(formatted);
        if (formatted.length) onTollTriggered(formatted[0]);
      }
    };

    fetchZones();
  }, [onTollTriggered]);

  return (
    <MapContainer
      center={driverPosition}
      zoom={14}
      style={{ height: "100%", width: "100%" }}
    >
      <RecenterToZones zones={zones} />

      <TileLayer
        attribution="© OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <Marker position={driverPosition} icon={driverIcon}>
        <Popup>You are here</Popup>
      </Marker>

      {zones.map((zone) => (
        <Polygon
          key={zone.id}
          positions={zone.coordinates}
          pathOptions={{
            color: "#DC2626",
            fillColor: "#FCA5A5",
            fillOpacity: 0.45
          }}
        />
      ))}
    </MapContainer>
  );
};

export default MapView;

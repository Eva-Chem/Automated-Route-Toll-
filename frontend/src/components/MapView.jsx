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

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5001";

const DRIVER_START_POSITION = [-1.283, 36.82];

const driverIcon = new L.Icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});

const RecenterToZones = ({ zones }) => {
  const map = useMap();

  useEffect(() => {
    if (!zones.length) return;
    const bounds = L.latLngBounds(zones.flatMap(z => z.coordinates));
    map.fitBounds(bounds, { padding: [80, 80] });
  }, [zones, map]);

  return null;
};

const MapView = ({ onTollTriggered }) => {
  const [zones, setZones] = useState([]);
  const [driverPosition] = useState(DRIVER_START_POSITION);

  useEffect(() => {
    const fetchZones = async () => {
      const res = await fetch(`${API_BASE}/toll-zones`);
      const json = await res.json();
      if (!json.success) return;

      const formatted = json.data.map(zone => ({
        zone_id: zone.zone_id,                 // ✅ KEEP ID
        zone_name: zone.zone_name,             // ✅ MATCH UI
        charge_amount: zone.charge_amount,
        coordinates: zone.polygon_coords.map(
          ([lng, lat]) => [lat, lng]
        )
      }));

      setZones(formatted);

      // ✅ Trigger first zone
      if (formatted.length) {
        onTollTriggered(formatted[0]);
      }
    };

    fetchZones();
  }, [onTollTriggered]);

  return (
    <MapContainer center={driverPosition} zoom={14} style={{ height: "100%", width: "100%" }}>
      <RecenterToZones zones={zones} />

      <TileLayer
        attribution="© OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <Marker position={driverPosition} icon={driverIcon}>
        <Popup>You are here</Popup>
      </Marker>

      {zones.map(zone => (
        <Polygon
          key={zone.zone_id}
          positions={zone.coordinates}
          pathOptions={{
            color: "#2563EB",
            fillColor: "#93C5FD",
            fillOpacity: 0.4
          }}
        >
          <Popup>
            <strong>{zone.zone_name}</strong><br />
            KES {zone.charge_amount}
          </Popup>
        </Polygon>
      ))}
    </MapContainer>
  );
};

export default MapView;

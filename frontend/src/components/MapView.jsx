import { MapContainer, TileLayer, Marker, Polygon, Popup } from "react-leaflet";
import { useEffect, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { API_BASE_URL } from "../config/api";

const DRIVER_POSITION = [-1.2805, 36.8155]; // safely inside Ngara

const markerIcon = new L.Icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});

export default function MapView({ onTollDetected }) {
  const [zones, setZones] = useState([]);

  useEffect(() => {
    const fetchZones = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/api/toll-zones`);
        const json = await res.json();

        if (!json.success || !Array.isArray(json.data)) return;

        const formatted = json.data
          .filter((z) => z?.polygon_coords?.coordinates?.[0])
          .map((zone) => ({
            zone_id: zone.zone_id,
            zone_name: zone.zone_name,
            charge_amount: zone.charge_amount,
            coordinates: zone.polygon_coords.coordinates[0].map(
              ([lng, lat]) => [lat, lng]
            )
          }));

        setZones(formatted);

        if (formatted.length && onTollDetected) {
          onTollDetected(formatted[0]);
        }
      } catch (err) {
        console.error("Failed to fetch zones", err);
      }
    };

    fetchZones();
  }, [onTollDetected]);

  return (
    <MapContainer center={DRIVER_POSITION} zoom={14} style={{ height: "100%", width: "100%" }}>
      <TileLayer
        attribution="© OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <Marker position={DRIVER_POSITION} icon={markerIcon}>
        <Popup>You are here</Popup>
      </Marker>

      {zones.map((zone) => (
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
}

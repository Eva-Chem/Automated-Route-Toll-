import { MapContainer, TileLayer, Polygon, Marker, Popup, FeatureGroup } from "react-leaflet";
import { EditControl } from "react-leaflet-draw";
import { useMemo } from "react";
import * as L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css";

const CENTER = [-1.286389, 36.817223];
const ZOOM = 12;

export default function MapCanvas({
  zones = [],
  mode = "admin",
  onCreateZone,
  onUpdateZone,
}) {
  // Pure renderer: takes zones from props and converts to Polygon positions
  // coordinates are expected as [[lat, lng], [lat, lng], ...]
  const polygons = useMemo(() => {
    return zones.map((z) => ({
      ...z,
      positions: z.coordinates, // Already in correct format [[lat, lng], ...]
    }));
  }, [zones]);

  return (
    <MapContainer center={CENTER} zoom={ZOOM} style={{ height: 500 }} preferCanvas>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution='&copy; OpenStreetMap contributors' />

      {mode === "operator" && (
        <FeatureGroup>
          <EditControl
            position="topright"
            draw={{ polygon: true, rectangle: false, marker: false, circle: false, polyline: false }}
            onCreated={(e) => {
              const coords = e.layer.getLatLngs()[0].map((p) => [p.lat, p.lng]);
              onCreateZone?.(coords);
            }}
            onEdited={(e) => {
              e.layers.eachLayer((layer) => {
                const id = layer.options.zoneId;
                const coords = layer.getLatLngs()[0].map((p) => [p.lat, p.lng]);
                onUpdateZone?.(id, coords);
              });
            }}
          />
        </FeatureGroup>
      )}

      {polygons.map((z) => (
        <Polygon
          key={z.id}
          positions={z.positions}
          pathOptions={{
            zoneId: z.id,
            color: mode === "operator" ? "#0d6efd" : "#198754",
            fillOpacity: 0.4,
          }}
        >
          <Popup>
            <strong>{z.name}</strong>
            <br />KES {z.charge_amount}
          </Popup>
        </Polygon>
      ))}

      {mode === "admin" &&
        polygons.map((z) => (
          <Marker
            key={`m-${z.id}`}
            position={L.polygon(z.positions).getBounds().getCenter()}
          >
            <Popup>{z.name}</Popup>
          </Marker>
        ))}
    </MapContainer>
  );
}

import { MapContainer, TileLayer, Marker, Popup, FeatureGroup, GeoJSON } from "react-leaflet";
import { EditControl } from "react-leaflet-draw";
import { useMemo } from "react";
import * as L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css";
import { geoJSONToLatLngArray, toGeoJSONPolygon } from "../utils/geo";

/**
 * MapCanvas
 *
 * Renders toll zones using GeoJSON as the source of truth.
 * Avoids mixing raw arrays with GeoJSON to prevent Leaflet isFlat errors.
 */

const CENTER = [-1.286389, 36.817223];
const ZOOM = 12;

export default function MapCanvas({
  zones = [],
  mode = "admin",
  onCreateZone,
  onUpdateZone,
}) {
  // Normalize zones into GeoJSON features and lat/lng arrays for marker centering
  const { featureCollection, latLngPolygons } = useMemo(() => {
    const features = [];
    const latLngsById = new Map();

    zones.forEach((z) => {
      const geometry = toGeoJSONPolygon(z.polygon_coords);
      if (!geometry) return; // skip invalid geometry

      features.push({
        type: "Feature",
        properties: {
          zone_id: z.zone_id,
          zone_name: z.zone_name,
          charge_amount: z.charge_amount,
        },
        geometry,
      });

      const latlngs = geoJSONToLatLngArray(z.polygon_coords);
      latLngsById.set(z.zone_id, latlngs);
    });

    return {
      featureCollection: {
        type: "FeatureCollection",
        features,
      },
      latLngPolygons: latLngsById,
    };
  }, [zones]);

  return (
    <MapContainer center={CENTER} zoom={ZOOM} style={{ height: 500 }} preferCanvas>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution='&copy; OpenStreetMap contributors' />

      {/* Operator mode: allow drawing and editing polygons */}
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
                const zoneId = layer.options.zoneId;
                const coords = layer.getLatLngs()[0].map((p) => [p.lat, p.lng]);
                onUpdateZone?.(zoneId, coords);
              });
            }}
          />
        </FeatureGroup>
      )}

      {/* Render GeoJSON polygons */}
      <GeoJSON
        data={featureCollection}
        style={{ color: mode === "operator" ? "#0d6efd" : "#198754", fillOpacity: 0.4 }}
        onEachFeature={(feature, layer) => {
          const { zone_name, charge_amount, zone_id } = feature.properties || {};
          // Attach zoneId to layer for potential edits
          layer.options.zoneId = zone_id;
          if (zone_name) {
            layer.bindPopup(`<strong>${zone_name}</strong><br/>KES ${charge_amount ?? "-"}`);
          }
        }}
      />

      {/* Admin mode: show zone center markers, guarded against invalid geometry */}
      {mode === "admin" &&
        zones.map((z) => {
          const latlngs = latLngPolygons.get(z.zone_id) || [];
          if (!latlngs || latlngs.length < 3) return null;
          try {
            const center = L.latLngBounds(latlngs).getCenter();
            return (
              <Marker key={`m-${z.zone_id}`} position={center}>
                <Popup>{z.zone_name}</Popup>
              </Marker>
            );
          } catch (error) {
            console.warn("Skipping marker for zone due to invalid coords:", z.zone_name, error);
            return null;
          }
        })}
    </MapContainer>
  );
}

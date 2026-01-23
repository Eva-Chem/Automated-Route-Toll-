/**
 * GeoJSON / LatLng utilities
 *
 * Backend returns polygon_coords possibly as GeoJSON Polygon or raw [[lat, lng]] arrays.
 * This helper normalizes them for Leaflet rendering and form editing.
 */

/**
 * Convert GeoJSON Polygon or [[lat, lng], ...] to Leaflet-friendly [[lat, lng], ...]
 * Safely handles invalid input by returning an empty array.
 */
export function geoJSONToLatLngArray(polygonCoords) {
  if (!polygonCoords) return [];

  // Case 1: Already an array of [lat, lng]
  if (Array.isArray(polygonCoords)) {
    // Validate shape: array of pairs
    const valid = polygonCoords.every(
      (p) => Array.isArray(p) && p.length === 2 && !Number.isNaN(p[0]) && !Number.isNaN(p[1])
    );
    if (valid) return polygonCoords.map(([lat, lng]) => [Number(lat), Number(lng)]);
  }

  // Case 2: GeoJSON Polygon
  if (polygonCoords.type === "Polygon" && Array.isArray(polygonCoords.coordinates)) {
    const ring = polygonCoords.coordinates[0];
    if (Array.isArray(ring)) {
      return ring
        .filter((pair) => Array.isArray(pair) && pair.length === 2)
        .map(([lng, lat]) => [Number(lat), Number(lng)]);
    }
  }

  return [];
}

/**
 * Normalize polygon_coords to a GeoJSON Polygon.
 * If input is already GeoJSON Polygon, return it as-is.
 * If input is [[lat, lng]], convert to GeoJSON Polygon with [lng, lat] order.
 */
export function toGeoJSONPolygon(polygonCoords) {
  if (!polygonCoords) return null;

  if (polygonCoords.type === "Polygon" && Array.isArray(polygonCoords.coordinates)) {
    return polygonCoords;
  }

  if (Array.isArray(polygonCoords)) {
    const ring = polygonCoords
      .filter((p) => Array.isArray(p) && p.length === 2)
      .map(([lat, lng]) => [Number(lng), Number(lat)]);
    if (ring.length >= 3) {
      return {
        type: "Polygon",
        coordinates: [ring],
      };
    }
  }

  return null;
}

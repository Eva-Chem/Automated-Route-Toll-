import { GoogleMap, LoadScript, DrawingManager, Polygon } from "@react-google-maps/api";

const center = { lat: -1.2675, lng: 36.8123 };

export default function GoogleMapCanvas({
  zones,
  selectedId,
  onSelect,
  onCreate,
  onUpdate,
}) {
  return (
    <LoadScript
      googleMapsApiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}
      libraries={["drawing"]}
    >
      <GoogleMap
        mapContainerStyle={{ height: "500px", width: "100%" }}
        center={center}
        zoom={13}
      >
        <DrawingManager
          onPolygonComplete={(poly) => {
            const coords = poly.getPath().getArray().map(p => ({
              lat: p.lat(),
              lng: p.lng(),
            }));
            poly.setMap(null);
            onCreate(coords);
          }}
        />

        {zones.map(z => (
          <Polygon
            key={z.id}
            paths={z.coordinates}
            editable={z.id === selectedId}
            onClick={() => onSelect(z)}
            onMouseUp={(e) =>
              z.id === selectedId &&
              onUpdate(z.id, {
                coordinates: e.getPath().getArray().map(p => ({
                  lat: p.lat(),
                  lng: p.lng(),
                })),
              })
            }
            options={{
              fillColor: z.id === selectedId ? "#198754" : "#0d6efd",
              fillOpacity: 0.35,
              strokeColor: "#0d6efd",
            }}
          />
        ))}
      </GoogleMap>
    </LoadScript>
  );
}

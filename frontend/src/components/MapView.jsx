import { MapContainer, TileLayer, Marker, Polygon, useMap } from "react-leaflet";
import { useEffect, useState } from "react";
import L from "leaflet";

// 🔵 Custom blue marker
const driverIcon = new L.Icon({
  iconUrl: "https://maps.gstatic.com/mapfiles/ms2/micons/blue-dot.png",
  iconSize: [32, 32],
  iconAnchor: [16, 32],
});

// 🔄 Auto-center map on driver
const RecenterMap = ({ position }) => {
  const map = useMap();

  useEffect(() => {
    if (position) {
      map.setView(position, 15);
    }
  }, [position, map]);

  return null;
};

// 🧪 Fallback mock data (used if backend is unavailable)
const mockTollZones = [
  {
    id: 1,
    name: "State House Toll Zone",
    charge_amount: 300,
    coordinates: [
      [-1.2925, 36.8075],
      [-1.2940, 36.8110],
      [-1.2905, 36.8130],
      [-1.2885, 36.8095],
    ],
  },
];

const MapView = () => {
  const [position, setPosition] = useState(null);
  const [tollZones, setTollZones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 📡 Live GPS tracking
  useEffect(() => {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by your browser");
      return;
    }

    const watchId = navigator.geolocation.watchPosition(
      (pos) => {
        setPosition([pos.coords.latitude, pos.coords.longitude]);
      },
      (err) => {
        console.error("Location error:", err);
        alert("Unable to retrieve your location");
      },
      { enableHighAccuracy: true }
    );

    return () => navigator.geolocation.clearWatch(watchId);
  }, []);

  // 🌐 Fetch toll zones from backend
  useEffect(() => {
    const fetchTollZones = async () => {
      try {
        const res = await fetch("http://127.0.0.1:5000/api/toll-zones");

        if (!res.ok) {
          throw new Error("Failed to fetch toll zones");
        }

        const json = await res.json();

        const formattedZones = json.data.map((zone) => ({
          id: zone.id,
          name: zone.name,
          charge_amount: zone.charge_amount,
          coordinates: zone.coordinates.map((point) => [
            point.lat,
            point.lng,
          ]),
        }));

        setTollZones(formattedZones);
        setError(null);
      } catch (err) {
        console.warn("Using mock toll zones:", err.message);
        setTollZones(mockTollZones);
        setError("Backend unavailable. Showing mock data.");
      } finally {
        setLoading(false);
      }
    };

    fetchTollZones();
  }, []);

  return (
    <MapContainer
      center={[-1.2921, 36.8219]}
      zoom={13}
      style={{ height: "100vh", width: "100%" }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {/* 🔄 Center map on driver */}
      {position && <RecenterMap position={position} />}

      {/* 🚗 Driver marker */}
      {position && <Marker position={position} icon={driverIcon} />}

      {/* 🔴 Toll zones */}
      {!loading &&
        tollZones.map((zone) => (
          <Polygon
            key={zone.id}
            positions={zone.coordinates}
            pathOptions={{
              color: "red",
              fillColor: "red",
              fillOpacity: 0.4,
            }}
          />
        ))}

      {/* ⚠️ Optional console-only feedback */}
      {error && console.warn(error)}
    </MapContainer>
  );
};

export default MapView;

import { useState } from "react";

export function useZones() {
  const [zones, setZones] = useState([]);

  return {
    zones,
    addZone: (z) => setZones([...zones, { id: Date.now(), ...z }]),
    updateZone: (id, data) =>
      setZones(zones.map(z => z.id === id ? { ...z, ...data } : z)),
    deleteZone: (id) =>
      setZones(zones.filter(z => z.id !== id)),
  };
}

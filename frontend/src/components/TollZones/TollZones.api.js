import api from "../../services/api";

/**
 * Toll Zones API
 * 
 * API responses are normalized at this boundary.
 * Backend response shapes are unwrapped here so Zustand store always receives clean domain objects.
 * 
 * Backend contracts:
 * - GET /api/toll-zones → { success, data: [...zones] }
 * - POST /api/toll-zones → { success, message, zone: {...} }
 * - PUT /api/toll-zones/:id → { success, message, zone: {...} }
 * - DELETE /api/toll-zones/:id → { success: true }
 */

export const getZones = async () => {
  const response = await api.get("/api/toll-zones");
  // Backend returns { success: true, data: [...] }
  // Normalize to array only
  return response.data?.data || [];
};

export const createZone = async (zone) => {
  const response = await api.post("/api/toll-zones", zone);
  // Backend returns { success: true, message, zone: {...} }
  // Normalize to zone object only
  return response.data?.zone || response.data;
};

export const updateZone = async (id, zone) => {
  const response = await api.put(`/api/toll-zones/${id}`, zone);
  // Backend returns { success: true, message, zone: {...} }
  // Normalize to zone object only
  return response.data?.zone || response.data;
};

export const deleteZone = async (id) => {
  await api.delete(`/api/toll-zones/${id}`);
  return true;
};

import api from "../../services/api";

export const getZones = async () => {
  const response = await api.get("/api/toll-zones");
  return response;
};

export const createZone = async (zone) => {
  const response = await api.post("/api/toll-zones", zone);
  return response.data;
};

export const updateZone = async (id, zone) => {
  const response = await api.put(`/api/toll-zones/${id}`, zone);
  return response.data;
};

export const deleteZone = async (id) => {
  await api.delete(`/api/toll-zones/${id}`);
};

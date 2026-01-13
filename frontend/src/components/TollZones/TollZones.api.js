import api from "../../services/api";

export const getZones = async () => {
  const response = await api.get("/toll_zones");
  return response.data;
};

export const createZone = async (zone) => {
  const response = await api.post("/toll_zones", zone);
  return response.data;
};

export const updateZone = async (id, zone) => {
  const response = await api.put(`/toll_zones/${id}`, zone);
  return response.data;
};

export const deleteZone = async (id) => {
  await api.delete(`/toll_zones/${id}`);
};
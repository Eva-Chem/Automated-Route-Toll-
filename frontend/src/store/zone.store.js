import { create } from "zustand";
import { getZones, createZone as apiCreate, updateZone as apiUpdate, deleteZone as apiDelete } from "../components/TollZones/tollZones.api";

export const useZoneStore = create((set, get) => ({
  zones: [],
  loading: false,
  error: null,

  // Fetch zones from API
  fetchZones: async () => {
    set({ loading: true, error: null });
    try {
      const response = await getZones();
      const data = response.data || response;
      set({ zones: data, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
      console.error("Failed to fetch zones:", error);
    }
  },

  // Add a new zone
  addZone: async (zone) => {
    try {
      const newZone = await apiCreate(zone);
      set((state) => ({
        zones: [...state.zones, newZone],
      }));
      return newZone;
    } catch (error) {
      set({ error: error.message });
      console.error("Failed to add zone:", error);
      throw error;
    }
  },

  // Update an existing zone
  updateZone: async (id, updates) => {
    try {
      const updatedZone = await apiUpdate(id, updates);
      set((state) => ({
        zones: state.zones.map((z) =>
          z.id === id ? { ...z, ...updatedZone } : z
        ),
      }));
      return updatedZone;
    } catch (error) {
      set({ error: error.message });
      console.error("Failed to update zone:", error);
      throw error;
    }
  },

  // Delete a zone
  deleteZone: async (id) => {
    try {
      await apiDelete(id);
      set((state) => ({
        zones: state.zones.filter((z) => z.id !== id),
      }));
    } catch (error) {
      set({ error: error.message });
      console.error("Failed to delete zone:", error);
      throw error;
    }
  },
}));

import { create } from "zustand";
import { getZones, createZone as apiCreate, updateZone as apiUpdate, deleteZone as apiDelete } from "../components/TollZones/TollZones.api";

/**
 * Zone Store
 * 
 * Single source of truth for toll zones state.
 * 
 * Key alignment rules (backend contract):
 * - zones is always an array (never wrapped in {success, data})
 * - zone identifiers are zone_id (not id)
 * - all filters, updates, and deletions use zone_id
 *
 * DELETE is supported by backend.
 */
export const useZoneStore = create((set) => ({
  zones: [],
  loading: false,
  error: null,

  // Fetch zones from API - API layer already normalizes to array
  fetchZones: async () => {
    set({ loading: true, error: null });
    try {
      const zones = await getZones();
      // getZones() API already returns normalized array
      set({ zones: Array.isArray(zones) ? zones : [], loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
      console.error("Failed to fetch zones:", error);
    }
  },

  // Add a new zone - API returns normalized zone object
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

  // Update an existing zone using zone_id (backend identifier)
  updateZone: async (zoneId, updates) => {
    try {
      const updatedZone = await apiUpdate(zoneId, updates);
      set((state) => ({
        zones: state.zones.map((z) =>
          z.zone_id === zoneId ? { ...z, ...updatedZone } : z
        ),
      }));
      return updatedZone;
    } catch (error) {
      set({ error: error.message });
      console.error("Failed to update zone:", error);
      throw error;
    }
  },

  // Delete a zone using backend DELETE support
  deleteZone: async (zoneId) => {
    try {
      await apiDelete(zoneId);
      set((state) => ({
        zones: state.zones.filter((z) => z.zone_id !== zoneId),
      }));
    } catch (error) {
      set({ error: error.message });
      console.error("Failed to delete zone:", error);
      throw error;
    }
  },
}));

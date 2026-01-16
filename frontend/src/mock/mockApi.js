import { mockZones } from "./zones.mock";

const delay = (ms) =>
  new Promise((resolve) => setTimeout(resolve, ms));

// Mutable copy for mock CRUD operations
let zones = JSON.parse(JSON.stringify(mockZones));

const mockApi = {
  post: async (url, payload) => {
    await delay(800);

    if (url === "/auth/login") {
      if (
        payload.username === "admin" &&
        payload.password === "admin123"
      ) {
        return {
          data: {
            token: "mock-admin-token",
          },
        };
      }
      throw new Error("Invalid credentials");
    }

    if (url === "/api/toll-zones") {
      const newZone = {
        ...payload,
        id: payload.id || Date.now(),
      };
      zones.push(newZone);
      return {
        data: newZone,
      };
    }
  },

  get: async (url) => {
    await delay(1000);

    if (url === "/api/toll-zones") {
      return {
        data: zones,
        success: true,
      };
    }
  },

  put: async (url, payload) => {
    await delay(800);
    const id = parseInt(url.split("/").pop());
    const index = zones.findIndex((z) => z.id === id);

    if (index !== -1) {
      zones[index] = { ...zones[index], ...payload };
      return {
        data: zones[index],
      };
    }

    throw new Error("Zone not found");
  },

  delete: async (url) => {
    await delay(800);
    const id = parseInt(url.split("/").pop());
    zones = zones.filter((z) => z.id !== id);
  },
};

export default mockApi;

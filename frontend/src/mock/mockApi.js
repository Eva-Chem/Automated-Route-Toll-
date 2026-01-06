import { mockTollsHistory } from "./mockData";

const delay = (ms) =>
  new Promise((resolve) => setTimeout(resolve, ms));

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
  },

  get: async (url) => {
    await delay(1000);

    if (url === "/tolls-history") {
      return {
        data: mockTollsHistory,
      };
    }
  },
};

export default mockApi;

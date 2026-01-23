import axios from "axios";
import mockApi from "../mock/mockApi";

const useMock = import.meta.env.VITE_USE_MOCK_API === "true";

const realApi = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

realApi.interceptors.request.use((config) => {
  const token = localStorage.getItem("auth_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add response interceptor to handle 401 errors
realApi.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid - clear storage and redirect to login
      localStorage.removeItem("auth_token");
      localStorage.removeItem("auth_user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default useMock ? mockApi : realApi;

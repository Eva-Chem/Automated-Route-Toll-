import axios from "axios";
import mockApi from "../mock/mockApi";

const useMock = import.meta.env.VITE_USE_MOCK_API === "true";

const realApi = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

realApi.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default useMock ? mockApi : realApi;

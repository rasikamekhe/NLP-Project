import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const login = (payload) => api.post("/login", payload);
export const predictThreat = (payload) => api.post("/predict", payload);
export const fetchMetrics = () => api.get("/metrics");
export const fetchHistory = () => api.get("/history");


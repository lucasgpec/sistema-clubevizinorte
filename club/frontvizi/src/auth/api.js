import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/";

export async function loginRequest(username, password) {
  const response = await axios.post(`${API_URL}token/`, { username, password });
  return response.data;
}

export async function refreshToken(refresh) {
  const response = await axios.post(`${API_URL}token/refresh/`, { refresh });
  return response.data;
}

// Adicione outras funções de integração conforme necessário

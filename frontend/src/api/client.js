import axios from 'axios';

// URL del backend local (FastAPI corre en el puerto 8000)
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: `${API_URL}/api`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: true // Necesario para el intercambio de cookies/sesiones CORS si se requiere
});

// Interceptor para inyectar de forma automatica el token Bearer JWT en cada peticion
client.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('smu_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor de respuesta para manejar sesiones expiradas (error 401)
client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Limpiar local storage y redirigir a login
      localStorage.removeItem('smu_authenticated');
      localStorage.removeItem('smu_token');
      localStorage.removeItem('smu_username');
      localStorage.removeItem('smu_role');
      localStorage.removeItem('smu_name');
      
      // Solo redirigir si no estamos ya en la ruta de login
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default client;

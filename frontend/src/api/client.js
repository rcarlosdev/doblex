import axios from 'axios';
import { isTokenExpired, clearSecuritySession } from '../lib/security';

// URL del backend local (FastAPI corre en el puerto 8000)
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: `${API_URL}/api`,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
  },
  withCredentials: true // Soporte seguro de sesiones CORS
});

// Interceptor de petición: valida expiración previa y añade token Bearer JWT
client.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('smu_token');
    if (token) {
      // Verificación proactiva de expiración de token en el cliente
      if (isTokenExpired(token)) {
        clearSecuritySession();
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
        return Promise.reject(new Error('Sesión expirada. Por favor inicie sesión nuevamente.'));
      }
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor de respuesta: manejo de 401 (No autorizado) y 403 (Prohibido)
client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const status = error.response.status;

      // 401: Token inválido, revocado o expirado
      if (status === 401) {
        clearSecuritySession();
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
      }

      // Sanitizar mensaje devuelto al usuario para no exponer detalles de base de datos
      const rawMsg = error.response.data?.message;
      if (rawMsg && typeof rawMsg === 'string' && (rawMsg.includes('Traceback') || rawMsg.includes('OperationalError') || rawMsg.includes('syntax error'))) {
        error.response.data.message = 'Ocurrió un error inesperado al procesar la solicitud.';
      }
    }
    return Promise.reject(error);
  }
);

export default client;


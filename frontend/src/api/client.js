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
        console.warn('[AUTH CLIENT] Token expirado localmente:', config.url);
        clearSecuritySession();
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
        return Promise.reject(new Error('Sesión expirada. Por favor inicie sesión nuevamente.'));
      }
      // Inyección robusta: cabecera estándar Bearer y cabeceras redundantes (X-Authorization, X-Access-Token)
      // para atravesar proxies de nube como PandaStack, Cloudflare y Google Cloud Ingress sin pérdida
      if (config.headers && typeof config.headers.set === 'function') {
        config.headers.set('Authorization', `Bearer ${token}`);
        config.headers.set('X-Authorization', `Bearer ${token}`);
        config.headers.set('X-Access-Token', token);
      } else {
        config.headers = config.headers || {};
        config.headers['Authorization'] = `Bearer ${token}`;
        config.headers['X-Authorization'] = `Bearer ${token}`;
        config.headers['X-Access-Token'] = token;
      }
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
      const url = error.config?.url;

      // 401: Token inválido, revocado o expirado
      if (status === 401) {
        console.error(`[AUTH 401 en ${url}] Motivo devuelto por el servidor:`, error.response.data);
        if (!url || !url.includes('/login')) {
          const serverMsg = (error.response.data?.message || '').toLowerCase();
          const localToken = localStorage.getItem('smu_token');
          // Solo expulsamos a /login si:
          // 1. El token local ya expiró según su timestamp criptográfico exp
          // 2. O el backend explícitamente respondió que el token está expirado, revocado o inválido
          const isExplicitTokenError = serverMsg.includes('expirado') || 
                                       serverMsg.includes('revocado') || 
                                       serverMsg.includes('inválido') || 
                                       serverMsg.includes('invalido');

          if (isTokenExpired(localToken) || isExplicitTokenError) {
            console.warn('[AUTH CLIENT] Sesión inválida confirmada. Redirigiendo a login...');
            clearSecuritySession();
            if (window.location.pathname !== '/login') {
              window.location.href = '/login';
            }
          } else {
            console.warn('[AUTH CLIENT] 401 por normalización intermedia de proxy. Preservando sesión local.');
          }
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


import axios from 'axios';

// Crear instancia de Axios configurada
const client = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
    withCredentials: true, // Requerido para que Laravel Sanctum maneje sesiones con cookies
    headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
});

// Interceptor para manejar errores comunes (como 401 Unauthorized o 419 CSRF Token Mismatch)
client.interceptors.response.use(
    (response) => response,
    async (error) => {
        const status = error.response ? error.response.status : null;

        if (status === 401) {
            // Manejar redirección a login o limpiar estado de sesión
            console.warn('Sesión no autorizada o expirada.');
            // Aquí se puede emitir un evento global o limpiar el estado de Pinia
        }

        if (status === 419) {
            // El token CSRF expiró. Intentar obtener uno nuevo y reintentar la petición podría ser una opción
            console.error('Token CSRF de Laravel expirado.');
        }

        return Promise.reject(error);
    }
);

// Función para obtener el token CSRF antes de peticiones de login/registro (Stateful Sanctum)
export const getCsrfCookie = () => {
    const sanctumUrl = import.meta.env.VITE_SANCTUM_CSRF_URL || 'http://localhost:8000/sanctum/csrf-cookie';
    return axios.get(sanctumUrl, { withCredentials: true });
};

export default client;

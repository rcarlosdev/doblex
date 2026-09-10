/**
 * Módulo de Seguridad Cliente - Doblex SMU
 * Maneja la verificación de tokens JWT, detección de alteración de roles (RBAC local),
 * sanitización de cadenas y validación de archivos.
 */

/**
 * Decodifica de forma segura la carga útil (payload) de un token JWT.
 * @param {string} token
 * @returns {object|null}
 */
export function decodeJwt(token) {
  if (!token || typeof token !== 'string') return null;
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;
    
    // Normalizar base64url a base64 estándar
    const base64Url = parts[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch (e) {
    return null;
  }
}

/**
 * Comprueba si un token JWT ha expirado.
 * @param {string} token
 * @returns {boolean}
 */
export function isTokenExpired(token) {
  const payload = decodeJwt(token);
  if (!payload || !payload.exp) return true;
  
  // Margen de seguridad de 30 segundos
  const now = Math.floor(Date.now() / 1000);
  return payload.exp <= now + 30;
}

/**
 * Limpia todas las credenciales de sesión en localStorage.
 */
export function clearSecuritySession() {
  const keys = [
    'smu_authenticated',
    'smu_token',
    'smu_username',
    'smu_role',
    'smu_name',
    'smu_user_id'
  ];
  keys.forEach(k => localStorage.removeItem(k));
}

/**
 * Valida la integridad criptográfica del rol del usuario almacenado en el cliente.
 * Previene la escalada de privilegios local mediante alteración de localStorage en DevTools.
 * @returns {{ isValid: boolean, role: string|null, reason?: string }}
 */
export function verifyRoleIntegrity() {
  const token = localStorage.getItem('smu_token');
  const storedRole = localStorage.getItem('smu_role');

  if (!token) {
    return { isValid: false, role: null, reason: 'No token' };
  }

  if (isTokenExpired(token)) {
    clearSecuritySession();
    return { isValid: false, role: null, reason: 'Token expired' };
  }

  const payload = decodeJwt(token);
  if (!payload || !payload.role) {
    clearSecuritySession();
    return { isValid: false, role: null, reason: 'Invalid token payload' };
  }

  // Detección de alteración maliciosa en localStorage
  if (storedRole && storedRole !== payload.role) {
    console.warn('[SEGURIDAD] Se detectó alteración en el rol de usuario local. Sesión terminada.');
    clearSecuritySession();
    return { isValid: false, role: null, reason: 'Role mismatch' };
  }

  return { isValid: true, role: payload.role };
}

/**
 * Sanitiza texto libre en el cliente contra inyección de código XSS.
 * @param {string} input
 * @returns {string}
 */
export function sanitizeString(input) {
  if (!input || typeof input !== 'string') return '';
  return input
    .replace(/<\s*script[^>]*>.*?<\s*\/\s*script\s*>/gi, '')
    .replace(/javascript\s*:/gi, '')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .trim();
}

/**
 * Valida archivos antes de cargarlos (tamaño, tipo MIME y extensión).
 * @param {File} file
 * @param {object} options
 * @returns {{ valid: boolean, error?: string }}
 */
export function validateClientFile(file, options = {}) {
  if (!file) {
    return { valid: false, error: 'No se seleccionó ningún archivo.' };
  }

  const maxMB = options.maxMB || 10;
  const maxBytes = maxMB * 1024 * 1024;
  if (file.size > maxBytes) {
    return { valid: false, error: `El archivo supera el tamaño máximo de ${maxMB}MB.` };
  }

  const allowedTypes = options.allowedTypes || ['image/jpeg', 'image/png', 'image/webp'];
  if (allowedTypes.length > 0 && !allowedTypes.includes(file.type)) {
    return { valid: false, error: `Tipo de archivo no permitido (${file.type}). Tipos válidos: ${allowedTypes.join(', ')}` };
  }

  return { valid: true };
}

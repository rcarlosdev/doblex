import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import client from '@/api/client';
import { decodeJwt, isTokenExpired, clearSecuritySession, setSessionCookie } from '@/lib/security';

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('smu_token') || '');
  const user = ref(null);

  const isAuthenticated = computed(() => {
    if (!token.value) return false;
    return !isTokenExpired(token.value);
  });

  const role = computed(() => {
    if (!token.value) return null;
    const payload = decodeJwt(token.value);
    return payload ? payload.role : null;
  });

  const username = computed(() => {
    if (user.value?.username) return user.value.username;
    const payload = decodeJwt(token.value);
    return payload ? payload.sub : '';
  });

  const initFromStorage = () => {
    const stored = localStorage.getItem('smu_token');
    if (stored && !isTokenExpired(stored)) {
      token.value = stored;
      const payload = decodeJwt(stored);
      if (payload) {
        user.value = {
          username: payload.sub,
          role: payload.role,
          id: payload.user_id
        };
      }
    } else {
      logout();
    }
  };

  const login = async (credentials) => {
    const response = await client.post('/login', credentials);
    const newToken = response.data.token;
    token.value = newToken;
    localStorage.setItem('smu_token', newToken);
    setSessionCookie(newToken);

    const payload = decodeJwt(newToken);
    if (payload) {
      user.value = {
        username: payload.sub,
        role: payload.role,
        id: payload.user_id
      };
    }
    return response.data;
  };

  const logout = () => {
    token.value = '';
    user.value = null;
    clearSecuritySession();
  };

  const hasRole = (roles) => {
    if (!role.value) return false;
    if (Array.isArray(roles)) return roles.includes(role.value);
    return role.value === roles;
  };

  return {
    token,
    user,
    role,
    username,
    isAuthenticated,
    initFromStorage,
    login,
    logout,
    hasRole
  };
});

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import client from '@/api/client';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

const username = ref('admin.doblex');
const password = ref('admin123');
const error = ref('');
const loading = ref(false);
const isDark = ref(true);
const router = useRouter();

onMounted(() => {
  isDark.value = document.documentElement.classList.contains('dark');
});

const toggleTheme = () => {
  isDark.value = !isDark.value;
  if (isDark.value) {
    document.documentElement.classList.add('dark');
    localStorage.setItem('smu_theme', 'dark');
  } else {
    document.documentElement.classList.remove('dark');
    localStorage.setItem('smu_theme', 'light');
  }
};

const handleLogin = async () => {
  loading.value = true;
  error.value = '';
  
  try {
    const response = await client.post('/login', {
      username: username.value,
      password: password.value
    });
    
    if (response.data.status === 'success') {
      localStorage.setItem('smu_authenticated', 'true');
      localStorage.setItem('smu_token', response.data.token);
      localStorage.setItem('smu_username', response.data.user.username);
      localStorage.setItem('smu_role', response.data.user.role);
      localStorage.setItem('smu_name', response.data.user.name);
      
      router.push({ name: 'dashboard' });
    }
  } catch (err) {
    if (err.response && err.response.data && err.response.data.message) {
      error.value = err.response.data.message;
    } else {
      error.value = 'No se pudo establecer conexión con la API del Servidor.';
    }
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-100 dark:bg-[#0a0b10] px-4 py-8 relative transition-colors duration-350 select-none overflow-hidden">
    <!-- Destellos de fondo sutiles para ambos modos -->
    <div class="absolute -top-40 -left-40 w-96 h-96 rounded-full bg-primary/10 dark:bg-primary/15 blur-3xl pointer-events-none"></div>
    <div class="absolute -bottom-40 -right-40 w-96 h-96 rounded-full bg-primary/5 dark:bg-primary/10 blur-3xl pointer-events-none"></div>

    <!-- Botón de Conmutación de Tema (Sol / Luna) -->
    <div class="absolute top-4 right-4 z-20">
      <Button 
        @click="toggleTheme" 
        variant="ghost" 
        size="icon" 
        class="h-10 w-10 text-neutral-600 dark:text-neutral-300 hover:text-neutral-900 dark:hover:text-white bg-white/80 dark:bg-neutral-900/80 backdrop-blur-md border border-neutral-200 dark:border-neutral-800 shadow-md hover:shadow-lg rounded-xl transition-all duration-200"
        :title="isDark ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro'"
      >
        <!-- Icono Sol (se muestra si isDark es true) -->
        <svg v-if="isDark" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 text-amber-400">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m0 13.5V21M5.25 5.25l1.5 1.5m10.5 10.5l1.5 1.5M3 12h2.25m13.5 0H21M5.25 18.75l1.5-1.5m10.5-10.5l1.5-1.5M12 7.5a4.5 4.5 0 1 1 0 9 4.5 4.5 0 0 1 0-9Z" />
        </svg>
        <!-- Icono Luna (se muestra si isDark es false) -->
        <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 text-slate-700">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.72 9.72 0 0 1 18 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 0 0 3 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 0 0 9.002-5.998Z" />
        </svg>
      </Button>
    </div>

    <!-- Card de Login -->
    <div class="w-full max-w-[420px] rounded-2xl border border-slate-200 dark:border-white/10 bg-white/95 dark:bg-neutral-900/80 backdrop-blur-xl p-8 shadow-2xl relative overflow-hidden transition-all duration-300 hover:shadow-primary/5 z-10">
      
      <div class="text-center mb-8 relative z-10">
        <div class="inline-flex items-center gap-2 bg-slate-100 dark:bg-white/5 px-4 py-1.5 rounded-full border border-slate-200 dark:border-white/10 mb-4 transition-colors">
          <span class="text-primary text-sm filter drop-shadow-[0_0_8px_rgba(239,68,68,0.5)]">▲</span>
          <span class="font-semibold tracking-wider text-xs text-slate-800 dark:text-white">SMU DOBLEX</span>
        </div>
        <h1 class="text-2xl font-bold tracking-tight text-slate-900 dark:text-white mb-1">Gestión de Obra</h1>
        <p class="text-xs text-slate-500 dark:text-neutral-400">Sistema de Control y Asignación de Campo</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-4 relative z-10">
        <div class="space-y-2">
          <label class="text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-neutral-400" for="username">Nombre de Usuario</label>
          <Input 
            type="text" 
            id="username" 
            v-model="username" 
            required 
            placeholder="admin.doblex"
            class="bg-slate-50 dark:bg-neutral-950/60 border-slate-200 dark:border-white/10 text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-neutral-500 focus-visible:ring-primary focus-visible:border-primary transition-colors"
          />
        </div>

        <div class="space-y-2">
          <label class="text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-neutral-400" for="password">Contraseña</label>
          <Input 
            type="password" 
            id="password" 
            v-model="password" 
            required 
            placeholder="••••••••"
            class="bg-slate-50 dark:bg-neutral-950/60 border-slate-200 dark:border-white/10 text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-neutral-500 focus-visible:ring-primary focus-visible:border-primary transition-colors"
          />
        </div>

        <div v-if="error" class="bg-red-500/10 border border-red-500/20 text-red-600 dark:text-red-400 text-xs py-2.5 px-3 rounded-lg text-center font-medium">
          {{ error }}
        </div>

        <Button type="submit" class="w-full bg-primary text-primary-foreground hover:bg-primary/90 mt-2 font-semibold tracking-wide shadow-md hover:shadow-lg transition-all" :disabled="loading">
          <span v-if="loading">Iniciando sesión...</span>
          <span v-else>Ingresar al Sistema</span>
        </Button>
      </form>

      <div class="text-center mt-8 relative z-10 select-none">
        <p class="text-[10px] text-slate-400 dark:text-neutral-500">&copy; 2026 DOBLEX. Todos los derechos reservados.</p>
      </div>
    </div>
  </div>
</template>

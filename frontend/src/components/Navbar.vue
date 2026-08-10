<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { Button } from '@/components/ui/button';

defineEmits(['toggle-sidebar']);

const router = useRouter();
const route = useRoute();
const username = ref('Usuario');
const isDark = ref(true);

onMounted(() => {
  username.value = localStorage.getItem('smu_username') || 'Administrador Doblex';
  // Verificar si la clase 'dark' está presente en el documento
  isDark.value = document.documentElement.classList.contains('dark');
});

const handleLogout = () => {
  localStorage.removeItem('smu_authenticated');
  localStorage.removeItem('smu_username');
  router.push({ name: 'login' });
};

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

const breadcrumbs = computed(() => {
  if (route.path === '/') {
    return [{ name: 'Dashboard', path: '/' }];
  }
  if (route.path.startsWith('/ordenes-trabajo')) {
    return [
      { name: 'Dashboard', path: '/' },
      { name: 'Órdenes de Trabajo', path: '/ordenes-trabajo' }
    ];
  }
  return [];
});
</script>

<template>
  <header class="h-16 border-b border-neutral-200 dark:border-neutral-900 bg-white dark:bg-neutral-950 px-4 md:px-6 flex items-center justify-between sticky top-0 z-30 select-none transition-colors duration-350">
    <!-- Lado Izquierdo: Botón Menú (móvil) + Migas de pan -->
    <div class="flex items-center gap-3">
      <!-- Botón hamburguesa siempre visible -->
      <Button 
        @click="$emit('toggle-sidebar')" 
        variant="ghost" 
        size="icon" 
        class="h-9 w-9 text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white hover:bg-neutral-100 dark:hover:bg-white/5"
        title="Alternar Menú"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
        </svg>
      </Button>

      <!-- Migas de Pan (Ocultas en pantallas muy pequeñas <= 480px) -->
      <div class="hidden xs:flex items-center gap-2 text-xs font-medium text-neutral-500 dark:text-neutral-400">
        <template v-for="(crumb, idx) in breadcrumbs" :key="crumb.path">
          <router-link 
            :to="crumb.path" 
            class="hover:text-neutral-900 dark:hover:text-white transition-colors duration-150"
            :class="{ 'text-neutral-900 dark:text-white font-semibold': idx === breadcrumbs.length - 1 }"
          >
            {{ crumb.name }}
          </router-link>
          <span v-if="idx < breadcrumbs.length - 1" class="text-neutral-300 dark:text-neutral-700">/</span>
        </template>
      </div>
    </div>

    <!-- Acciones Derecha -->
    <div class="flex items-center gap-3 sm:gap-6">
      <!-- Conmutador de Tema (Sol / Luna) -->
      <Button 
        @click="toggleTheme" 
        variant="ghost" 
        size="icon" 
        class="h-8 w-8 text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white hover:bg-neutral-100 dark:hover:bg-white/5 rounded-lg"
        title="Alternar Tema"
      >
        <!-- Icono Sol (se muestra si isDark es true) -->
        <svg v-if="isDark" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 text-amber-400">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m0 13.5V21M5.25 5.25l1.5 1.5m10.5 10.5l1.5 1.5M3 12h2.25m13.5 0H21M5.25 18.75l1.5-1.5m10.5-10.5l1.5-1.5M12 7.5a4.5 4.5 0 1 1 0 9 4.5 4.5 0 0 1 0-9Z" />
        </svg>
        <!-- Icono Luna (se muestra si isDark es false) -->
        <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 text-indigo-600">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.72 9.72 0 0 1 18 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 0 0 3 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 0 0 9.002-5.998Z" />
        </svg>
      </Button>

      <!-- Indicador API (Oculto en móviles pequeños) -->
      <div class="hidden sm:flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-[10px] font-bold uppercase tracking-wider px-3 py-1.5 rounded-full">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
        API Online
      </div>

      <!-- Divisor -->
      <div class="hidden sm:block w-px h-4 bg-neutral-200 dark:bg-neutral-900"></div>

      <!-- Badge de Usuario y Logout -->
      <div class="flex items-center gap-2 sm:gap-4">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-rose-600 text-white flex items-center justify-center font-bold text-[10px]">
            AD
          </div>
          <div class="hidden md:flex flex-col text-left">
            <span class="text-xs font-semibold text-neutral-800 dark:text-white leading-none">{{ username }}</span>
            <span class="text-[9px] text-neutral-500 mt-1">Super Admin</span>
          </div>
        </div>

        <Button 
          @click="handleLogout" 
          variant="ghost" 
          size="icon" 
          class="h-8 w-8 text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white hover:bg-neutral-100 dark:hover:bg-white/5 rounded-lg"
          title="Cerrar Sesión"
        >
          🚪
        </Button>
      </div>
    </div>
  </header>
</template>

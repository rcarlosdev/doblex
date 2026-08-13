<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { Button } from '@/components/ui/button';
import { IconMenu2, IconSun, IconMoon, IconDeviceMobile, IconLogout } from '@tabler/icons-vue';

defineEmits(['toggle-sidebar']);

const router = useRouter();
const route = useRoute();
const username = ref('Usuario');
const userRole = ref('admin');
const userInitials = ref('AD');
const isDark = ref(true);

onMounted(() => {
  const name = localStorage.getItem('smu_name') || localStorage.getItem('smu_username') || 'Administrador Doblex';
  username.value = name;
  userRole.value = localStorage.getItem('smu_role') || 'admin';
  
  // Calcular iniciales
  const parts = name.trim().split(' ');
  if (parts.length >= 2) {
    userInitials.value = (parts[0][0] + parts[1][0]).toUpperCase();
  } else if (parts[0]) {
    userInitials.value = parts[0].substring(0, 2).toUpperCase();
  }

  // Verificar si la clase 'dark' está presente en el documento
  isDark.value = document.documentElement.classList.contains('dark');
});

const handleLogout = () => {
  localStorage.removeItem('smu_authenticated');
  localStorage.removeItem('smu_username');
  localStorage.removeItem('smu_token');
  localStorage.removeItem('smu_role');
  localStorage.removeItem('smu_name');
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
  if (route.path.startsWith('/empleados')) {
    return [
      { name: 'Dashboard', path: '/' },
      { name: 'Gestión de Personal', path: '/empleados' }
    ];
  }
  return [{ name: 'Inicio', path: '/' }];
});
</script>

<template>
  <header class="h-16 border-b border-neutral-200 dark:border-neutral-800 bg-white/95 dark:bg-[#181d2c]/95 backdrop-blur-md px-4 md:px-6 flex items-center justify-between sticky top-0 z-30 select-none transition-colors duration-350 shadow-sm">
    <!-- Lado Izquierdo: Botón Menú + Migas de pan -->
    <div class="flex items-center gap-3">
      <!-- Botón hamburguesa -->
      <Button 
        @click="$emit('toggle-sidebar')" 
        variant="ghost" 
        size="icon" 
        class="h-9 w-9 text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-white/5 rounded-lg"
        title="Alternar Menú"
      >
        <IconMenu2 class="w-5 h-5 stroke-[1.75]" />
      </Button>

      <!-- Migas de Pan -->
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
        class="h-9 w-9 text-neutral-600 dark:text-neutral-300 hover:text-neutral-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-white/5 rounded-lg transition-all"
        :title="isDark ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro'"
      >
        <IconSun v-if="isDark" class="w-5 h-5 text-amber-400 stroke-[1.75]" />
        <IconMoon v-else class="w-5 h-5 text-slate-700 stroke-[1.75]" />
      </Button>

      <!-- Acceso a Vista Móvil Técnico -->
      <router-link
        to="/mobile/dashboard"
        class="flex items-center gap-1.5 bg-blue-600/10 hover:bg-blue-600/20 text-blue-600 dark:text-blue-400 border border-blue-500/30 text-xs font-bold px-3 py-1.5 rounded-full transition-all"
        title="Vista Mobile para Técnicos en Campo"
      >
        <IconDeviceMobile class="w-4 h-4 stroke-[2]" />
        <span class="hidden md:inline">Modo Técnico</span>
      </router-link>

      <!-- Indicador API -->
      <div class="hidden sm:flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-[10px] font-bold uppercase tracking-wider px-3 py-1.5 rounded-full">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
        API Online
      </div>

      <!-- Divisor -->
      <div class="hidden sm:block w-px h-4 bg-neutral-200 dark:bg-neutral-800"></div>

      <!-- Badge de Usuario y Logout -->
      <div class="flex items-center gap-2 sm:gap-4">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-rose-600 text-white flex items-center justify-center font-bold text-[10px] shadow-sm">
            {{ userInitials }}
          </div>
          <div class="hidden md:flex flex-col text-left">
            <span class="text-xs font-semibold text-neutral-800 dark:text-white leading-none">{{ username }}</span>
            <span class="text-[9px] text-neutral-500 mt-1 uppercase font-semibold tracking-wider">{{ userRole }}</span>
          </div>
        </div>

        <Button 
          @click="handleLogout" 
          variant="ghost" 
          size="icon" 
          class="h-8 w-8 text-neutral-500 dark:text-neutral-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-500/10 rounded-lg transition-colors"
          title="Cerrar Sesión"
        >
          <IconLogout class="w-4 h-4 stroke-[1.75]" />
        </Button>
      </div>
    </div>
  </header>
</template>

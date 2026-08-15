<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { Button } from '@/components/ui/button';
import { 
  IconLayoutDashboard, 
  IconClipboardList, 
  IconUsers, 
  IconDeviceMobile,
  IconPackages, 
  IconTruck, 
  IconCash, 
  IconShieldCheck, 
  IconScale,
  IconX
} from '@tabler/icons-vue';

const props = defineProps({
  open: { type: Boolean, default: false }
});

defineEmits(['close']);

const route = useRoute();
const userRole = ref('admin');

onMounted(() => {
  userRole.value = localStorage.getItem('smu_role') || 'admin';
});

const allMenuItems = [
  { name: 'Dashboard', path: '/', icon: IconLayoutDashboard, routeName: 'dashboard', roles: ['admin', 'administrativo'] },
  { name: 'Órdenes de Trabajo', path: '/ordenes-trabajo', icon: IconClipboardList, routeName: 'ots', roles: ['admin', 'administrativo'] },
  { name: 'Gestión de Campo', path: '/mobile/dashboard', icon: IconDeviceMobile, routeName: 'mobile-dashboard', roles: ['admin', 'administrativo', 'operativo'] },
  { name: 'Gestión de Empleados', path: '/empleados', icon: IconUsers, routeName: 'empleados', roles: ['admin', 'administrativo'] },
];

const menuItems = computed(() => {
  return allMenuItems.filter(item => item.roles.includes(userRole.value));
});

const logicItems = [
  { name: 'Inventarios', icon: IconPackages, phase: 'F2' },
  { name: 'Vehículos', icon: IconTruck, phase: 'F2' },
];

const financeItems = [
  { name: 'Viáticos', icon: IconCash, phase: 'F3' },
  { name: 'SST & Dotación', icon: IconShieldCheck, phase: 'F4' },
  { name: 'Jurídica & Pólizas', icon: IconScale, phase: 'F4' },
];

const isRouteActive = (item) => {
  if (item.routeName === 'dashboard') {
    return route.path === '/';
  }
  return route.path.startsWith(item.path);
};
</script>

<template>
  <aside 
    class="h-screen sticky top-0 bg-white dark:bg-[#121215] flex flex-col overflow-hidden transition-all duration-350 ease-in-out select-none border-neutral-200 dark:border-white/10"
    :class="[
      // Comportamiento responsivo móvil (flotante)
      'fixed z-50',
      open 
        ? 'translate-x-0 w-64 p-6 border-r opacity-100' 
        : '-translate-x-full w-0 p-0 border-r-0 opacity-0 pointer-events-none',
      // Comportamiento responsivo escritorio (empuja el contenido)
      'md:sticky md:z-20 md:translate-x-0',
      open
        ? 'md:w-64 md:p-6 md:border-r md:opacity-100'
        : 'md:w-0 md:p-0 md:border-r-0 md:opacity-0 md:pointer-events-none'
    ]"
  >
    <!-- Logotipo principal & Botón Cerrar (en móvil) -->
    <div class="min-w-[200px] flex items-center justify-between mb-10 pl-2">
      <div class="flex items-center gap-2">
        <span class="text-primary text-xl font-bold filter drop-shadow-[0_0_8px_rgba(239,68,68,0.5)]">▲</span>
        <span class="font-bold tracking-wider text-sm bg-gradient-to-r from-neutral-800 to-neutral-500 dark:from-white dark:to-neutral-400 bg-clip-text text-transparent">
          DOBLEX SAS
        </span>
      </div>
      <Button 
        @click="$emit('close')" 
        variant="ghost" 
        size="icon" 
        class="h-8 w-8 text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white hover:bg-neutral-100 dark:hover:bg-white/5 md:hidden"
        title="Cerrar Menú"
      >
        <IconX class="w-4 h-4" />
      </Button>
    </div>

    <!-- Menú Principal (Filtrado por Permisos de Rol) -->
    <nav class="min-w-[200px] flex-1 flex flex-col gap-1">
      <router-link 
        v-for="item in menuItems" 
        :key="item.path" 
        :to="item.path" 
        @click="$emit('close')"
        class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200"
        :class="isRouteActive(item) 
          ? 'bg-primary/10 border border-primary/20 text-primary dark:text-white font-semibold shadow-sm' 
          : 'text-neutral-600 dark:text-neutral-400 border border-transparent hover:text-neutral-900 dark:hover:text-white hover:bg-neutral-100 dark:hover:bg-white/5'"
      >
        <component :is="item.icon" class="w-5 h-5 stroke-[1.75]" />
        <span>{{ item.name }}</span>
      </router-link>

      <!-- Módulos de Logística y Recursos (Solo visible para Admin / Administrativo) -->
      <template v-if="userRole !== 'operativo'">
        <div class="text-[10px] font-bold text-neutral-400 dark:text-neutral-600 mt-6 mb-2 tracking-wider uppercase pl-2">
          Logística y Recursos
        </div>
        <div 
          v-for="item in logicItems" 
          :key="item.name" 
          class="flex items-center justify-between gap-3 px-3 py-2.5 rounded-lg text-sm font-medium opacity-60 cursor-not-allowed text-neutral-500 dark:text-neutral-400"
          title="Disponible en Fase 2"
        >
          <div class="flex items-center gap-3">
            <component :is="item.icon" class="w-5 h-5 stroke-[1.5]" />
            <span>{{ item.name }}</span>
          </div>
          <span class="text-[9px] bg-neutral-100 dark:bg-neutral-900 border border-neutral-200 dark:border-white/5 px-1.5 py-0.5 rounded text-neutral-550 dark:text-neutral-400">
            {{ item.phase }}
          </span>
        </div>

        <!-- Módulos de Finanzas y RRHH -->
        <div class="text-[10px] font-bold text-neutral-400 dark:text-neutral-600 mt-6 mb-2 tracking-wider uppercase pl-2">
          Finanzas y RRHH
        </div>
        <div 
          v-for="item in financeItems" 
          :key="item.name" 
          class="flex items-center justify-between gap-3 px-3 py-2.5 rounded-lg text-sm font-medium opacity-60 cursor-not-allowed text-neutral-500 dark:text-neutral-400"
          :title="`Disponible en Fase ${item.phase}`"
        >
          <div class="flex items-center gap-3">
            <component :is="item.icon" class="w-5 h-5 stroke-[1.5]" />
            <span>{{ item.name }}</span>
          </div>
          <span class="text-[9px] bg-neutral-100 dark:bg-neutral-900 border border-neutral-200 dark:border-white/5 px-1.5 py-0.5 rounded text-neutral-550 dark:text-neutral-400">
            {{ item.phase }}
          </span>
        </div>
      </template>
    </nav>

    <!-- Versión / Info Base -->
    <div class="min-w-[200px] border-t border-neutral-200 dark:border-neutral-900 pt-4 mt-auto">
      <div class="text-[10px] text-neutral-400 dark:text-neutral-600 text-center">
        Doblex v0.0.1
      </div>
    </div>
  </aside>
</template>

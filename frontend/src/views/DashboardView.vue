<script setup>
import { ref, onMounted, computed } from 'vue';
import client from '@/api/client';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import {
  IconClipboardList,
  IconChartBar,
  IconCircleCheck,
  IconTruck,
  IconDeviceMobile,
  IconArrowRight
} from '@tabler/icons-vue';

const ots = ref([]);
const loading = ref(false);
const userRole = ref('operativo');

const loadDashboardData = async () => {
  loading.value = true;
  try {
    const response = await client.get('/ots');
    if (response.data.status === 'success') {
      ots.value = response.data.data;
    }
  } catch (err) {
    console.error('Error al cargar datos del Dashboard:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  userRole.value = localStorage.getItem('smu_role') || 'operativo';
  loadDashboardData();
});

// KPIs Calculados en Base a Datos Reales de la API
const kpis = computed(() => {
  const total = ots.value.length;
  const activas = ots.value.filter(o => 
    ['asignada', 'en_camino', 'en_sitio', 'en_progreso', 'detenida_materiales', 'pendiente'].includes(o.estado)
  ).length;
  const finalizadas = ots.value.filter(o => 
    ['solucionada', 'finalizada', 'finalizado'].includes(o.estado)
  ).length;
  const enTerreno = ots.value.filter(o => 
    ['en_camino', 'en_sitio', 'en_progreso'].includes(o.estado)
  ).length;
  
  // Calcular progreso promedio
  const promedioProgreso = total > 0 
    ? Math.round(ots.value.reduce((acc, curr) => acc + (Number(curr.progreso) || 0), 0) / total) 
    : 0;

  return {
    activas,
    total,
    finalizadas,
    promedioProgreso,
    enTerreno
  };
});
</script>

<template>
  <div class="flex flex-col gap-6 select-none">
    <!-- Grid de KPIs (Tarjetas con shadcn-vue adaptativas Claro/Oscuro) -->
    <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <Card class="bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900 hover:border-neutral-300 dark:hover:border-neutral-800 transition-all duration-200 hover:-translate-y-1">
        <CardHeader class="flex flex-row items-center justify-between pb-2 space-y-0">
          <CardTitle class="text-xs font-semibold uppercase tracking-wider text-neutral-500 dark:text-neutral-400">Órdenes Activas</CardTitle>
          <div class="bg-primary/10 border border-primary/20 text-primary w-8 h-8 rounded-lg flex items-center justify-center">
            <IconClipboardList class="w-5 h-5 stroke-[1.75]" />
          </div>
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold text-neutral-900 dark:text-white mb-1">
            {{ loading ? '...' : kpis.activas }}
          </div>
          <p class="text-[10px] text-neutral-500">De un total de {{ kpis.total }} registradas</p>
        </CardContent>
      </Card>

      <Card class="bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900 hover:border-neutral-300 dark:hover:border-neutral-800 transition-all duration-200 hover:-translate-y-1">
        <CardHeader class="flex flex-row items-center justify-between pb-2 space-y-0">
          <CardTitle class="text-xs font-semibold uppercase tracking-wider text-neutral-500 dark:text-neutral-400">Progreso Promedio</CardTitle>
          <div class="bg-primary/10 border border-primary/20 text-primary w-8 h-8 rounded-lg flex items-center justify-center">
            <IconChartBar class="w-5 h-5 stroke-[1.75]" />
          </div>
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold text-neutral-900 dark:text-white mb-1">
            {{ loading ? '...' : kpis.promedioProgreso }}%
          </div>
          <p class="text-[10px] text-neutral-500">Rendimiento global operativo</p>
        </CardContent>
      </Card>

      <Card class="bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900 hover:border-neutral-300 dark:hover:border-neutral-800 transition-all duration-200 hover:-translate-y-1">
        <CardHeader class="flex flex-row items-center justify-between pb-2 space-y-0">
          <CardTitle class="text-xs font-semibold uppercase tracking-wider text-neutral-500 dark:text-neutral-400">Solucionadas / Finalizadas</CardTitle>
          <div class="bg-emerald-500/10 border border-emerald-500/20 text-emerald-500 w-8 h-8 rounded-lg flex items-center justify-center">
            <IconCircleCheck class="w-5 h-5 stroke-[1.75]" />
          </div>
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold text-neutral-900 dark:text-white mb-1">
            {{ loading ? '...' : kpis.finalizadas }}
          </div>
          <p class="text-[10px] text-emerald-500 font-medium">Atendidas satisfactoriamente</p>
        </CardContent>
      </Card>

      <Card class="bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900 hover:border-neutral-300 dark:hover:border-neutral-800 transition-all duration-200 hover:-translate-y-1">
        <CardHeader class="flex flex-row items-center justify-between pb-2 space-y-0">
          <CardTitle class="text-xs font-semibold uppercase tracking-wider text-neutral-500 dark:text-neutral-400">Cuadrillas en Terreno</CardTitle>
          <div class="bg-primary/10 border border-primary/20 text-primary w-8 h-8 rounded-lg flex items-center justify-center">
            <IconTruck class="w-5 h-5 stroke-[1.75]" />
          </div>
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold text-neutral-900 dark:text-white mb-1">
            {{ loading ? '...' : kpis.enTerreno }}
          </div>
          <p class="text-[10px] text-neutral-500">En ruta o en sitio telecom</p>
        </CardContent>
      </Card>
    </section>

    <!-- Banner de Acción Rápida para Perfil Operativo -->
    <div v-if="userRole === 'operativo'" class="bg-gradient-to-r from-blue-900/40 via-indigo-900/30 to-slate-900 border border-blue-500/30 rounded-2xl p-5 flex flex-col sm:flex-row items-center justify-between gap-4 shadow-xl">
      <div class="space-y-1">
        <div class="flex items-center gap-2">
          <span class="bg-blue-600 text-white text-[10px] font-black px-2 py-0.5 rounded uppercase tracking-wider">Perfil Operativo</span>
          <h2 class="text-sm font-extrabold text-white">Centro de Gestión e Intervención en Campo</h2>
        </div>
        <p class="text-xs text-slate-300">
          Registra la llegada a sitio, minutar avances PDT, insumos LPU consumidos y evidencias fotográficas obligatorias.
        </p>
      </div>
      <router-link
        to="/mobile/dashboard"
        class="bg-blue-600 hover:bg-blue-500 text-white font-extrabold text-xs px-5 py-3 rounded-xl shadow-lg active:scale-95 transition-all whitespace-nowrap flex items-center gap-2"
      >
        <IconDeviceMobile class="w-4 h-4 stroke-[1.75]" />
        <span>Abrir Gestión de Campo</span>
        <IconArrowRight class="w-4 h-4 stroke-[2]" />
      </router-link>
    </div>

    <!-- Cuerpo del Dashboard: Layout de Dos Columnas -->
    <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Panel de Avance de Obras Principales (Datos de Negocio reales de la API) -->
      <Card class="lg:col-span-2 bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900 p-6 flex flex-col gap-6">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-lg font-bold text-neutral-900 dark:text-white mb-1">Frentes de Obra en Ejecución</h2>
            <p class="text-xs text-neutral-500">Avance de las Órdenes de Trabajo registradas en tiempo real</p>
          </div>
          <router-link to="/ordenes-trabajo" class="text-xs font-bold text-red-600 dark:text-red-400 hover:text-red-500 hover:underline flex items-center gap-1">
            <span>Ver listado general</span>
            <IconArrowRight class="w-3.5 h-3.5 stroke-[2.2]" />
          </router-link>
        </div>
        
        <div class="space-y-5">
          <div
            v-for="ot in ots"
            :key="ot.id"
            @click="$router.push('/ordenes-trabajo')"
            class="space-y-2 p-3 rounded-xl hover:bg-slate-100 dark:hover:bg-white/5 cursor-pointer transition-all border border-transparent hover:border-red-500/20"
          >
            <div class="flex items-center justify-between text-xs text-neutral-700 dark:text-neutral-300">
              <div class="flex items-center gap-2 min-w-0">
                <span class="text-primary font-mono font-bold shrink-0">{{ ot.codigo }}</span>
                <span class="truncate font-semibold text-neutral-900 dark:text-white">{{ ot.sitio ? `[${ot.sitio}] ` : '' }}{{ ot.descripcion }}</span>
                <span class="px-1.5 py-0.2 rounded text-[9px] font-bold uppercase shrink-0" :class="{
                  'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400': ['finalizada', 'solucionada'].includes(ot.estado),
                  'bg-blue-500/10 text-blue-600 dark:text-blue-400': ot.estado === 'en_progreso',
                  'bg-amber-500/10 text-amber-600 dark:text-amber-400': ['asignada', 'en_camino', 'en_sitio'].includes(ot.estado),
                  'bg-rose-500/10 text-rose-600 dark:text-rose-400': ot.estado === 'detenida_materiales',
                }">
                  {{ ot.estado }}
                </span>
              </div>
              <span class="font-bold text-primary shrink-0 ml-2">{{ ot.progreso }}%</span>
            </div>
            <Progress :model-value="ot.progreso" />
          </div>
          <div v-if="ots.length === 0" class="text-center text-xs text-neutral-500 py-10">
            No hay órdenes de trabajo activas asignadas a tu cuenta.
          </div>
        </div>
      </Card>

      <!-- Panel Lateral: Actividades Recientes en Campo -->
      <Card class="bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900 p-6 flex flex-col gap-6">
        <div>
          <h2 class="text-lg font-bold text-neutral-900 dark:text-white mb-1">Actividades de Campo</h2>
          <p class="text-xs text-neutral-500">Historial y novedades en los frentes de obra</p>
        </div>

        <div class="flex-grow flex flex-col gap-5 relative pl-4 border-l border-neutral-200 dark:border-neutral-900">
          <div class="relative">
            <span class="absolute -left-[21px] top-1.5 w-2.5 h-2.5 rounded-full bg-primary border-2 border-white dark:border-neutral-950 ring-4 ring-primary/20"></span>
            <div class="space-y-0.5">
              <h4 class="text-xs font-semibold text-neutral-900 dark:text-white">Avance registrado en OT-2026-002</h4>
              <p class="text-[11px] text-neutral-600 dark:text-neutral-400">Ing. Carlos Pérez reportó el armado de vigas de amarre del sector A.</p>
              <span class="block text-[9px] text-neutral-400 dark:text-neutral-600">Hace 15 minutos</span>
            </div>
          </div>

          <div class="relative">
            <span class="absolute -left-[21px] top-1.5 w-2.5 h-2.5 rounded-full bg-amber-500 border-2 border-white dark:border-neutral-950"></span>
            <div class="space-y-0.5">
              <h4 class="text-xs font-semibold text-neutral-900 dark:text-white">Alerta: Novedad climatológica</h4>
              <p class="text-[11px] text-neutral-600 dark:text-neutral-400">Retraso reportado en vaciado de concreto en frente Norte por lluvias fuertes.</p>
              <span class="block text-[9px] text-neutral-400 dark:text-neutral-600">Hace 2 horas</span>
            </div>
          </div>

          <div class="relative">
            <span class="absolute -left-[21px] top-1.5 w-2.5 h-2.5 rounded-full bg-emerald-500 border-2 border-white dark:border-neutral-950"></span>
            <div class="space-y-0.5">
              <h4 class="text-xs font-semibold text-neutral-900 dark:text-white">OT-2026-001 finalizada</h4>
              <p class="text-[11px] text-neutral-600 dark:text-neutral-400">Ing. Luis Martínez completó la entrega del tramo vial y retiró maquinaria pesada.</p>
              <span class="block text-[9px] text-neutral-400 dark:text-neutral-600">Ayer, 17:30</span>
            </div>
          </div>
        </div>
      </Card>
    </section>
  </div>
</template>

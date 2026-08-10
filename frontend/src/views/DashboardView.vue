<script setup>
import { ref, onMounted, computed } from 'vue';
import client from '@/api/client';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';

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
  const activas = ots.value.filter(o => o.estado === 'en_progreso' || o.estado === 'pendiente').length;
  const finalizadas = ots.value.filter(o => o.estado === 'finalizado').length;
  
  // Calcular progreso promedio
  const promedioProgreso = total > 0 
    ? Math.round(ots.value.reduce((acc, curr) => acc + curr.progreso, 0) / total) 
    : 0;

  // Equipos asignados (simulado con base en total de OTs activas)
  const equipos = activas * 2;

  return {
    activas,
    total,
    finalizadas,
    promedioProgreso,
    equipos
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
          <div class="text-xl bg-primary/10 border border-primary/20 text-primary w-8 h-8 rounded-lg flex items-center justify-center">📋</div>
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
          <div class="text-xl bg-primary/10 border border-primary/20 text-primary w-8 h-8 rounded-lg flex items-center justify-center">📊</div>
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
          <CardTitle class="text-xs font-semibold uppercase tracking-wider text-neutral-500 dark:text-neutral-400">Obras Entregadas</CardTitle>
          <div class="text-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-500 w-8 h-8 rounded-lg flex items-center justify-center">✅</div>
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold text-neutral-900 dark:text-white mb-1">
            {{ loading ? '...' : kpis.finalizadas }}
          </div>
          <p class="text-[10px] text-emerald-500 font-medium">100% de ejecución</p>
        </CardContent>
      </Card>

      <Card class="bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900 hover:border-neutral-300 dark:hover:border-neutral-800 transition-all duration-200 hover:-translate-y-1">
        <CardHeader class="flex flex-row items-center justify-between pb-2 space-y-0">
          <CardTitle class="text-xs font-semibold uppercase tracking-wider text-neutral-500 dark:text-neutral-400">Maquinaria y Frentes</CardTitle>
          <div class="text-xl bg-primary/10 border border-primary/20 text-primary w-8 h-8 rounded-lg flex items-center justify-center">🚚</div>
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold text-neutral-900 dark:text-white mb-1">
            {{ loading ? '...' : kpis.equipos }}
          </div>
          <p class="text-[10px] text-neutral-500">Frentes activos operando</p>
        </CardContent>
      </Card>
    </section>

    <!-- Cuerpo del Dashboard: Layout de Dos Columnas -->
    <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Panel de Avance de Obras Principales (Datos de Negocio reales de la API) -->
      <Card class="lg:col-span-2 bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900 p-6 flex flex-col gap-6">
        <div>
          <h2 class="text-lg font-bold text-neutral-900 dark:text-white mb-1">Frentes de Obra en Ejecución</h2>
          <p class="text-xs text-neutral-500">Avance de las Órdenes de Trabajo registradas en tiempo real</p>
        </div>
        
        <div class="space-y-5">
          <div v-for="ot in ots" :key="ot.id" class="space-y-2">
            <div class="flex justify-between text-xs text-neutral-700 dark:text-neutral-300">
              <span><b>{{ ot.codigo }}</b>: {{ ot.descripcion }} ({{ ot.ubicacion }})</span>
              <span class="font-semibold text-primary">{{ ot.progreso }}%</span>
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

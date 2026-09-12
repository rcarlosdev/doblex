<template>
  <div class="space-y-5 max-w-4xl mx-auto pb-20 select-none transition-colors duration-300">
    <!-- Header Mobile Limpio para Campo -->
    <div class="flex items-center justify-between border-b border-slate-200 dark:border-white/10 pb-3">
      <div>
        <h1 class="text-lg font-extrabold text-slate-900 dark:text-white">Órdenes de Trabajo</h1>
        <p class="text-[11px] text-slate-500 dark:text-slate-400">Gestión de Campo & Mantenimiento</p>
      </div>
      <div class="flex items-center gap-2">
        <button 
          @click="fetchOts" 
          class="p-2 bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl text-slate-700 dark:text-slate-300 hover:text-red-600 dark:hover:text-red-400 active:scale-95 transition-all shadow-sm flex items-center justify-center" 
          title="Actualizar Órdenes de Trabajo"
        >
          <IconRefresh class="w-5 h-5 stroke-[2]" :class="{ 'animate-spin': loading }" />
        </button>
      </div>
    </div>

    <!-- Indicadores Rápidos Interactivos (Atajos) -->
    <div class="grid grid-cols-2 gap-3">
      <button 
        type="button"
        @click="activarFiltroActivas"
        class="text-left bg-white dark:bg-[#121215] border rounded-2xl p-4 shadow-sm transition-all duration-200 active:scale-[0.98]"
        :class="filtroActivo !== 'solucionadas' 
          ? 'border-amber-400/80 ring-2 ring-amber-500/20 shadow-md bg-amber-50/20 dark:bg-amber-950/10' 
          : 'border-slate-200 dark:border-white/10 hover:border-amber-300 dark:hover:border-amber-700/50'"
      >
        <div class="flex items-center justify-between">
          <div>
            <div class="text-[11px] text-slate-500 dark:text-slate-400 font-medium">Asignadas / En Sitio</div>
            <div class="text-2xl font-black text-amber-600 dark:text-amber-400 mt-0.5">{{ pendientesCount }}</div>
          </div>
          <div class="w-10 h-10 rounded-xl bg-amber-50 dark:bg-amber-950/50 border border-amber-200 dark:border-amber-800/40 text-amber-600 dark:text-amber-400 flex items-center justify-center">
            <IconClock class="w-5 h-5 stroke-[2]" />
          </div>
        </div>
        <div class="text-[10px] font-bold text-amber-700/80 dark:text-amber-400/80 mt-2 flex items-center gap-1">
          <span>{{ filtroActivo !== 'solucionadas' ? '● Viendo pendientes' : 'Ver pendientes →' }}</span>
        </div>
      </button>

      <button 
        type="button"
        @click="activarFiltroSolucionadas"
        class="text-left bg-white dark:bg-[#121215] border rounded-2xl p-4 shadow-sm transition-all duration-200 active:scale-[0.98]"
        :class="filtroActivo === 'solucionadas' 
          ? 'border-emerald-500 ring-2 ring-emerald-500/20 shadow-md bg-emerald-50/20 dark:bg-emerald-950/10' 
          : 'border-slate-200 dark:border-white/10 hover:border-emerald-300 dark:hover:border-emerald-700/50'"
      >
        <div class="flex items-center justify-between">
          <div>
            <div class="text-[11px] text-slate-500 dark:text-slate-400 font-medium">Solucionadas / Atendidas</div>
            <div class="text-2xl font-black text-emerald-600 dark:text-emerald-400 mt-0.5">{{ solucionadasCount }}</div>
          </div>
          <div class="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/50 border border-emerald-200 dark:border-emerald-800/40 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
            <IconCircleCheck class="w-5 h-5 stroke-[2]" />
          </div>
        </div>
        <div class="text-[10px] font-bold text-emerald-700/80 dark:text-emerald-400/80 mt-2 flex items-center gap-1">
          <span>{{ filtroActivo === 'solucionadas' ? '● Viendo historial' : 'Ver historial →' }}</span>
        </div>
      </button>
    </div>

    <!-- Barra de Filtros Segmentada con Contadores en tiempo real -->
    <div class="space-y-2">
      <div class="bg-slate-200/60 dark:bg-[#121215] p-1 rounded-2xl border border-slate-200/80 dark:border-white/10">
        <div class="grid grid-cols-5 gap-1 text-center">
          <button
            v-for="f in filtros"
            :key="f.id"
            @click="filtroActivo = f.id"
            class="flex flex-col sm:flex-row items-center justify-center gap-1 px-1 py-2 rounded-xl text-xs font-bold transition-all duration-200"
            :class="filtroActivo === f.id 
              ? (f.id === 'solucionadas' ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/20' : 'bg-red-600 text-white shadow-md shadow-red-600/20') 
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-white/40 dark:hover:bg-white/5'"
          >
            <div class="relative flex items-center">
              <component :is="f.icon" class="w-4 h-4 stroke-[2.2] shrink-0" />
              <!-- Punto de alerta si hay emergencias pendientes -->
              <span 
                v-if="f.id === 'emergencia' && f.count > 0 && filtroActivo !== 'emergencia'" 
                class="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full animate-ping"
              />
            </div>
            <div class="flex items-center gap-1">
              <span class="truncate text-[10px] sm:text-xs font-extrabold">
                <span class="sm:hidden">{{ f.shortLabel }}</span>
                <span class="hidden sm:inline">{{ f.label }}</span>
              </span>
              <!-- Badge contador -->
              <span 
                class="text-[9px] px-1 py-0.2 rounded-full font-black font-mono transition-colors"
                :class="filtroActivo === f.id 
                  ? 'bg-white/25 text-white' 
                  : (f.count > 0 ? (f.id === 'solucionadas' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-red-100 text-red-700 dark:bg-red-950 dark:text-red-300') : 'bg-slate-300/40 dark:bg-white/10 text-slate-400')"
              >
                {{ f.count }}
              </span>
            </div>
          </button>
        </div>
      </div>

      <!-- Subfiltro opcional dentro de Solucionadas -->
      <div 
        v-if="filtroActivo === 'solucionadas'" 
        class="flex items-center justify-between gap-2 px-2 py-1 text-xs bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-200/60 dark:border-emerald-800/30 rounded-xl"
      >
        <span class="text-[11px] font-bold text-emerald-800 dark:text-emerald-300 flex items-center gap-1">
          <IconCircleCheck class="w-3.5 h-3.5 stroke-[2.5]" />
          <span>Historial de órdenes atendidas</span>
        </span>
        <div class="flex items-center gap-1">
          <button 
            v-for="sub in [
              { id: 'todas', label: 'Todas' },
              { id: 'emergencia', label: 'MEE' },
              { id: 'preventivo', label: 'MP' },
              { id: 'correctivo', label: 'MC' }
            ]"
            :key="sub.id"
            @click="subfiltroSolucionadas = sub.id"
            class="px-2 py-0.5 rounded-md text-[10px] font-extrabold transition-all"
            :class="subfiltroSolucionadas === sub.id 
              ? 'bg-emerald-600 text-white shadow-xs' 
              : 'bg-white/80 dark:bg-white/5 text-slate-600 dark:text-slate-400 hover:bg-white dark:hover:bg-white/10 border border-slate-200/60 dark:border-white/5'"
          >
            {{ sub.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- Lista de OTs -->
    <div v-if="loading" class="text-center py-12 text-slate-500 dark:text-slate-400 text-sm flex flex-col items-center gap-2">
      <IconRefresh class="w-6 h-6 animate-spin text-red-600" />
      <span>Cargando Órdenes de Trabajo...</span>
    </div>

    <div v-else-if="filteredOts.length === 0" class="text-center py-12 bg-white/70 dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl space-y-2 shadow-sm p-6">
      <IconClipboardCheck class="w-12 h-12 mx-auto text-slate-400 stroke-[1.5]" />
      <div class="text-sm font-bold text-slate-700 dark:text-slate-300">
        {{ filtroActivo === 'solucionadas' ? 'No hay órdenes solucionadas en esta categoría' : 'No hay órdenes pendientes en esta categoría' }}
      </div>
      <div class="text-xs text-slate-500 dark:text-slate-500">
        {{ filtroActivo === 'solucionadas' 
          ? 'Las órdenes que marques como solucionadas aparecerán en este historial.' 
          : 'Excelente trabajo, no tienes actividades activas por realizar aquí.' }}
      </div>
      <div v-if="filtroActivo !== 'solucionadas' && countSolucionadasDeTipoActual > 0" class="pt-3">
        <button 
          @click="verHistorialTipoActual"
          class="text-xs font-extrabold text-emerald-600 dark:text-emerald-400 hover:underline flex items-center justify-center gap-1 mx-auto"
        >
          <span>Consultar {{ countSolucionadasDeTipoActual }} orden(es) ya solucionada(s)</span>
          <IconArrowRight class="w-3.5 h-3.5 stroke-[2.5]" />
        </button>
      </div>
    </div>

    <div v-else class="space-y-3">
      <div
        v-for="ot in filteredOts"
        :key="ot.id"
        @click="goToDetail(ot.id)"
        class="bg-white dark:bg-[#121215] border rounded-2xl p-4 space-y-3 cursor-pointer shadow-sm hover:shadow-md active:scale-[0.99] transition-all"
        :class="isOtSolucionada(ot) 
          ? 'border-emerald-200/80 dark:border-emerald-800/30 hover:border-emerald-400 dark:hover:border-emerald-600/50' 
          : 'border-slate-200 dark:border-white/10 hover:border-red-500/50 dark:hover:border-red-500/50'"
      >
        <div class="flex items-start justify-between gap-2">
          <div>
            <div class="flex items-center gap-2 flex-wrap">
              <span 
                class="font-mono text-sm font-extrabold"
                :class="isOtSolucionada(ot) ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'"
              >
                {{ ot.codigo }}
              </span>
              <span :class="tipoMantenimientoClass(ot.tipo_actividad || ot.tipo_mantenimiento)" class="px-2 py-0.5 rounded text-[10px] font-bold uppercase shadow-2xs">
                {{ formatTipoNombre(ot.tipo_actividad || ot.tipo_mantenimiento) }}
              </span>
              <span v-if="ot.subsistema" class="bg-slate-100 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300 px-2 py-0.5 rounded text-[10px] font-mono font-bold">
                {{ ot.subsistema }}
              </span>
              <span 
                v-if="isOtSolucionada(ot)" 
                class="bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/50 px-2 py-0.5 rounded text-[10px] font-bold flex items-center gap-1"
              >
                <IconCircleCheck class="w-3 h-3 stroke-[2.5]" />
                <span>Atendida</span>
              </span>
            </div>
            <h3 class="text-sm font-bold text-slate-900 dark:text-white mt-1.5 line-clamp-2">{{ ot.descripcion }}</h3>
            <div v-if="ot.sitio" class="text-xs font-bold text-amber-700 dark:text-amber-300 mt-1 flex items-center gap-1">
              <IconBuildingBroadcastTower class="w-4 h-4 stroke-[1.75]" />
              <span>Estación: {{ ot.sitio }}</span>
            </div>
          </div>
          <SlaBadge :fecha-limite="ot.fecha_limite_sla" :estado="ot.estado" />
        </div>

        <div class="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 pt-2.5 border-t border-slate-100 dark:border-white/10">
          <div class="flex items-center gap-1.5 truncate pr-2">
            <IconMapPin class="w-4 h-4 text-rose-500 shrink-0 stroke-[1.75]" />
            <span class="truncate">{{ ot.ubicacion }}</span>
            <span class="text-slate-300 dark:text-slate-600">•</span>
            <span class="uppercase text-[10px] font-bold text-slate-500 dark:text-slate-400 shrink-0">{{ ot.tipo_ubicacion || 'urbana' }}</span>
          </div>
          <div 
            class="flex items-center gap-1 font-extrabold whitespace-nowrap"
            :class="isOtSolucionada(ot) ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'"
          >
            <span>{{ isOtSolucionada(ot) ? 'Ver Registro' : 'Atender' }}</span>
            <IconArrowRight class="w-4 h-4 stroke-[2.5]" />
          </div>
        </div>
      </div>

      <!-- Banner discreto al pie si hay solucionadas de esta misma categoría en el historial -->
      <div 
        v-if="filtroActivo !== 'solucionadas' && filtroActivo !== 'todos' && countSolucionadasDeTipoActual > 0"
        class="bg-emerald-50/60 dark:bg-emerald-950/20 border border-emerald-200/60 dark:border-emerald-800/30 rounded-2xl p-3 flex items-center justify-between text-xs text-emerald-800 dark:text-emerald-300 shadow-xs"
      >
        <div class="flex items-center gap-2">
          <IconCircleCheck class="w-4 h-4 text-emerald-600 shrink-0" />
          <span>Tienes <strong>{{ countSolucionadasDeTipoActual }}</strong> {{ countSolucionadasDeTipoActual === 1 ? 'orden resuelta' : 'órdenes resueltas' }} en este tipo.</span>
        </div>
        <button 
          @click="verHistorialTipoActual"
          class="text-[11px] font-extrabold text-emerald-700 dark:text-emerald-400 hover:underline shrink-0"
        >
          Ver historial →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import client from '@/api/client';
import SlaBadge from '@/components/common/SlaBadge.vue';
import { 
  IconRefresh, 
  IconClock, 
  IconCircleCheck, 
  IconListCheck, 
  IconAlertTriangle, 
  IconShieldCheck, 
  IconTools, 
  IconClipboardCheck,
  IconBuildingBroadcastTower,
  IconMapPin,
  IconArrowRight
} from '@tabler/icons-vue';

const router = useRouter();
const ots = ref([]);
const loading = ref(true);
const filtroActivo = ref('todos');
const subfiltroSolucionadas = ref('todas');
const technicianName = ref('Técnico de Campo');

const isOtSolucionada = (ot) => {
  return ['solucionada', 'finalizada'].includes(ot?.estado);
};

const pendientesCount = computed(() => {
  return ots.value.filter(o => !isOtSolucionada(o)).length;
});

const emergenciasPendientesCount = computed(() => {
  return ots.value.filter(o => o.tipo_mantenimiento === 'emergencia' && !isOtSolucionada(o)).length;
});

const preventivosPendientesCount = computed(() => {
  return ots.value.filter(o => o.tipo_mantenimiento === 'preventivo' && !isOtSolucionada(o)).length;
});

const correctivosPendientesCount = computed(() => {
  return ots.value.filter(o => o.tipo_mantenimiento === 'correctivo' && !isOtSolucionada(o)).length;
});

const solucionadasCount = computed(() => {
  return ots.value.filter(o => isOtSolucionada(o)).length;
});

const countSolucionadasDeTipoActual = computed(() => {
  if (filtroActivo.value === 'todos' || filtroActivo.value === 'solucionadas') return 0;
  return ots.value.filter(o => o.tipo_mantenimiento === filtroActivo.value && isOtSolucionada(o)).length;
});

const filtros = computed(() => [
  { id: 'todos', label: 'Todas', shortLabel: 'Todas', icon: IconListCheck, count: pendientesCount.value },
  { id: 'emergencia', label: 'MEE / Emergencias', shortLabel: 'MEE', icon: IconAlertTriangle, count: emergenciasPendientesCount.value },
  { id: 'preventivo', label: 'MP / Preventivos', shortLabel: 'MP', icon: IconShieldCheck, count: preventivosPendientesCount.value },
  { id: 'correctivo', label: 'MC / Correctivos', shortLabel: 'MC', icon: IconTools, count: correctivosPendientesCount.value },
  { id: 'solucionadas', label: 'Solucionadas', shortLabel: 'Solución', icon: IconCircleCheck, count: solucionadasCount.value },
]);

const activarFiltroActivas = () => {
  filtroActivo.value = 'todos';
};

const activarFiltroSolucionadas = () => {
  filtroActivo.value = 'solucionadas';
  subfiltroSolucionadas.value = 'todas';
};

const verHistorialTipoActual = () => {
  const currentTipo = filtroActivo.value;
  filtroActivo.value = 'solucionadas';
  subfiltroSolucionadas.value = currentTipo;
};

const fetchOts = async () => {
  loading.value = true;
  try {
    const res = await client.get('/ots');
    if (res.data.status === 'success') {
      ots.value = res.data.data;
    }
  } catch (err) {
    console.error("Error al cargar OTs:", err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  technicianName.value = localStorage.getItem('smu_name') || localStorage.getItem('smu_username') || 'Técnico de Campo';
  fetchOts();
});

const filteredOts = computed(() => {
  // Pestañas operativas: EXCLUYEN solucionadas para dar espacio y foco total
  if (filtroActivo.value === 'emergencia') {
    return ots.value.filter(o => o.tipo_mantenimiento === 'emergencia' && !isOtSolucionada(o));
  }
  if (filtroActivo.value === 'preventivo') {
    return ots.value.filter(o => o.tipo_mantenimiento === 'preventivo' && !isOtSolucionada(o));
  }
  if (filtroActivo.value === 'correctivo') {
    return ots.value.filter(o => o.tipo_mantenimiento === 'correctivo' && !isOtSolucionada(o));
  }
  if (filtroActivo.value === 'solucionadas') {
    let list = ots.value.filter(o => isOtSolucionada(o));
    if (subfiltroSolucionadas.value !== 'todas') {
      list = list.filter(o => o.tipo_mantenimiento === subfiltroSolucionadas.value);
    }
    return list;
  }
  // En 'todos', solo devolvemos las órdenes activas/pendientes
  return ots.value.filter(o => !isOtSolucionada(o));
});

const goToDetail = (id) => {
  router.push(`/mobile/ot/${id}`);
};

const formatTipoNombre = (tipo) => {
  const str = (tipo || '').toLowerCase();
  if (str === 'obra_civil') return 'Obra Civil';
  if (str === 'informe_360') return 'Informe 360';
  if (str === 'rutina_7x24' || str.includes('7x24')) return 'Rutina MP 7x24';
  if (str === 'preventivo_planta') return 'Planta GE';
  if (str === 'preventivo_aire') return 'Aire AA';
  if (str === 'emergencia') return 'Emergencia';
  if (str === 'correctivo') return 'Correctivo';
  return tipo || 'Preventivo';
};

const tipoMantenimientoClass = (tipo) => {
  const str = (tipo || '').toLowerCase();
  if (str === 'emergencia') return 'bg-rose-100 text-rose-800 border border-rose-200 dark:bg-rose-950 dark:text-rose-400 dark:border-rose-500/30';
  if (str === 'correctivo') return 'bg-amber-100 text-amber-800 border border-amber-200 dark:bg-amber-950 dark:text-amber-400 dark:border-amber-500/30';
  if (str === 'obra_civil') return 'bg-orange-100 text-orange-800 border border-orange-200 dark:bg-orange-950/60 dark:text-orange-400 dark:border-orange-500/30';
  if (str === 'informe_360') return 'bg-purple-100 text-purple-800 border border-purple-200 dark:bg-purple-950/60 dark:text-purple-400 dark:border-purple-500/30';
  if (str === 'rutina_7x24' || str.includes('7x24')) return 'bg-indigo-100 text-indigo-800 border border-indigo-200 dark:bg-indigo-950/60 dark:text-indigo-400 dark:border-indigo-500/30';
  return 'bg-blue-100 text-blue-800 border border-blue-200 dark:bg-blue-950/60 dark:text-blue-400 dark:border-blue-500/30';
};
</script>

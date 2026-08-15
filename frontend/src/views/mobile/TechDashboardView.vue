<template>
  <div class="min-h-screen bg-slate-100 dark:bg-[#0a0b10] text-slate-900 dark:text-slate-100 p-4 space-y-5 pb-20 transition-colors duration-300">
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

    <!-- Indicadores Rápidos -->
    <div class="grid grid-cols-2 gap-3">
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl p-3 shadow-sm flex items-center justify-between">
        <div>
          <div class="text-[11px] text-slate-500 dark:text-slate-400 font-medium">Asignadas / En Sitio</div>
          <div class="text-2xl font-black text-amber-600 dark:text-amber-400 mt-0.5">{{ pendientesCount }}</div>
        </div>
        <div class="w-9 h-9 rounded-lg bg-amber-50 dark:bg-amber-950/50 border border-amber-200 dark:border-amber-800/40 text-amber-600 dark:text-amber-400 flex items-center justify-center">
          <IconClock class="w-5 h-5 stroke-[2]" />
        </div>
      </div>
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl p-3 shadow-sm flex items-center justify-between">
        <div>
          <div class="text-[11px] text-slate-500 dark:text-slate-400 font-medium">Solucionadas / Atendidas</div>
          <div class="text-2xl font-black text-emerald-600 dark:text-emerald-400 mt-0.5">{{ solucionadasCount }}</div>
        </div>
        <div class="w-9 h-9 rounded-lg bg-emerald-50 dark:bg-emerald-950/50 border border-emerald-200 dark:border-emerald-800/40 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
          <IconCircleCheck class="w-5 h-5 stroke-[2]" />
        </div>
      </div>
    </div>

    <!-- Barra de Filtros Segmentada Responsiva para Móviles (Shadcn Red Theme) -->
    <div class="space-y-2">
      <div class="bg-slate-200/60 dark:bg-[#121215] p-1 rounded-2xl border border-slate-200/80 dark:border-white/10">
        <div class="grid grid-cols-5 gap-1 text-center">
          <button
            v-for="f in filtros"
            :key="f.id"
            @click="filtroActivo = f.id"
            class="flex flex-col sm:flex-row items-center justify-center gap-1 px-1 py-2 rounded-xl text-xs font-bold transition-all duration-200"
            :class="filtroActivo === f.id 
              ? 'bg-red-600 text-white shadow-md shadow-red-600/20' 
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-white/40 dark:hover:bg-slate-800/50'"
          >
            <component :is="f.icon" class="w-4 h-4 stroke-[2.2] shrink-0" />
            <span class="truncate text-[10px] sm:text-xs font-extrabold">
              <span class="sm:hidden">{{ f.shortLabel }}</span>
              <span class="hidden sm:inline">{{ f.label }}</span>
            </span>
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
      <div class="text-sm font-bold text-slate-700 dark:text-slate-300">No hay órdenes asignadas</div>
      <div class="text-xs text-slate-500 dark:text-slate-500">Mantente atento a nuevas notificaciones de despacho de la central.</div>
    </div>

    <div v-else class="space-y-3">
      <div
        v-for="ot in filteredOts"
        :key="ot.id"
        @click="goToDetail(ot.id)"
        class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 hover:border-red-500/50 dark:hover:border-red-500/50 rounded-2xl p-4 space-y-3 cursor-pointer shadow-sm hover:shadow-md active:scale-[0.99] transition-all"
      >
        <div class="flex items-start justify-between">
          <div>
            <div class="flex items-center gap-2 flex-wrap">
              <span class="font-mono text-sm font-extrabold text-red-600 dark:text-red-400">{{ ot.codigo }}</span>
              <span :class="tipoMantenimientoClass(ot.tipo_mantenimiento)" class="px-2 py-0.5 rounded text-[10px] font-bold uppercase">
                {{ ot.tipo_mantenimiento || 'Preventivo' }}
              </span>
              <span v-if="ot.subsistema" class="bg-slate-100 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300 px-2 py-0.5 rounded text-[10px] font-mono font-bold">
                {{ ot.subsistema }}
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
          <div class="flex items-center gap-1 font-extrabold text-red-600 dark:text-red-400 whitespace-nowrap">
            <span>Atender</span>
            <IconArrowRight class="w-4 h-4 stroke-[2.5]" />
          </div>
        </div>
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
const technicianName = ref('Técnico de Campo');

const filtros = [
  { id: 'todos', label: 'Todas', shortLabel: 'Todas', icon: IconListCheck },
  { id: 'emergencia', label: 'MEE / Emergencias', shortLabel: 'MEE', icon: IconAlertTriangle },
  { id: 'preventivo', label: 'MP / Preventivos', shortLabel: 'MP', icon: IconShieldCheck },
  { id: 'correctivo', label: 'MC / Correctivos', shortLabel: 'MC', icon: IconTools },
  { id: 'solucionadas', label: 'Solucionadas', shortLabel: 'Solución', icon: IconCircleCheck },
];

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

const pendientesCount = computed(() => {
  return ots.value.filter(o => !['solucionada', 'finalizada'].includes(o.estado)).length;
});

const solucionadasCount = computed(() => {
  return ots.value.filter(o => ['solucionada', 'finalizada'].includes(o.estado)).length;
});

const filteredOts = computed(() => {
  if (filtroActivo.value === 'emergencia') {
    return ots.value.filter(o => o.tipo_mantenimiento === 'emergencia');
  }
  if (filtroActivo.value === 'preventivo') {
    return ots.value.filter(o => o.tipo_mantenimiento === 'preventivo');
  }
  if (filtroActivo.value === 'correctivo') {
    return ots.value.filter(o => o.tipo_mantenimiento === 'correctivo');
  }
  if (filtroActivo.value === 'solucionadas') {
    return ots.value.filter(o => ['solucionada', 'finalizada'].includes(o.estado));
  }
  return ots.value;
});

const goToDetail = (id) => {
  router.push(`/mobile/ot/${id}`);
};

const tipoMantenimientoClass = (tipo) => {
  if (tipo === 'emergencia') return 'bg-rose-100 text-rose-800 border border-rose-200 dark:bg-rose-950 dark:text-rose-400 dark:border-rose-500/30';
  if (tipo === 'correctivo') return 'bg-amber-100 text-amber-800 border border-amber-200 dark:bg-amber-950 dark:text-amber-400 dark:border-amber-500/30';
  return 'bg-red-50 text-red-700 border border-red-200 dark:bg-red-950/60 dark:text-red-400 dark:border-red-500/30';
};
</script>

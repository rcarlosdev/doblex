<template>
  <div class="min-h-screen bg-slate-950 text-slate-100 p-4 space-y-5 pb-20">
    <!-- Header Mobile -->
    <div class="flex items-center justify-between border-b border-slate-800 pb-3">
      <div>
        <h1 class="text-lg font-extrabold text-white flex items-center gap-2">
          <span class="bg-blue-600 text-white text-xs px-2 py-0.5 rounded font-mono">TÉCNICO</span>
          Órdenes de Trabajo
        </h1>
        <p class="text-xs text-slate-400">Seguimiento e Intervención en Campo</p>
      </div>
      <button @click="fetchOts" class="p-2 bg-slate-900 border border-slate-800 rounded-lg text-slate-300 hover:text-white">
        🔄
      </button>
    </div>

    <!-- Indicadores Rápidos -->
    <div class="grid grid-cols-2 gap-3">
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-3">
        <div class="text-xs text-slate-400 font-medium">Asignadas / En Ruta</div>
        <div class="text-xl font-black text-amber-400 mt-1">{{ pendientesCount }}</div>
      </div>
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-3">
        <div class="text-xs text-slate-400 font-medium">Solucionadas Hoy</div>
        <div class="text-xl font-black text-emerald-400 mt-1">{{ solucionadasCount }}</div>
      </div>
    </div>

    <!-- Filtros por Estado -->
    <div class="flex gap-2 overflow-x-auto pb-1 no-scrollbar">
      <button
        v-for="f in filtros"
        :key="f.id"
        @click="filtroActivo = f.id"
        class="px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all border"
        :class="filtroActivo === f.id ? 'bg-blue-600 border-blue-500 text-white shadow-md' : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-white'"
      >
        {{ f.label }}
      </button>
    </div>

    <!-- Lista de OTs -->
    <div v-if="loading" class="text-center py-10 text-slate-400 text-sm">
      Cargando Órdenes de Trabajo...
    </div>

    <div v-else-if="filteredOts.length === 0" class="text-center py-12 bg-slate-900/50 border border-slate-800/80 rounded-2xl space-y-2">
      <div class="text-2xl">📋</div>
      <div class="text-sm font-semibold text-slate-300">No hay órdenes asignadas</div>
      <div class="text-xs text-slate-500">Mantente atento a nuevas notificaciones de despacho.</div>
    </div>

    <div v-else class="space-y-3">
      <div
        v-for="ot in filteredOts"
        :key="ot.id"
        @click="goToDetail(ot.id)"
        class="bg-slate-900 border border-slate-800 hover:border-blue-500/50 rounded-xl p-4 space-y-3 cursor-pointer shadow-lg active:scale-[0.99] transition-all"
      >
        <div class="flex items-start justify-between">
          <div>
            <div class="flex items-center gap-2">
              <span class="font-mono text-sm font-extrabold text-blue-400">{{ ot.codigo }}</span>
              <span :class="tipoMantenimientoClass(ot.tipo_mantenimiento)" class="px-2 py-0.5 rounded text-[10px] font-bold uppercase">
                {{ ot.tipo_mantenimiento || 'Preventivo' }}
              </span>
            </div>
            <h3 class="text-sm font-bold text-white mt-1 line-clamp-1">{{ ot.descripcion }}</h3>
          </div>
          <SlaBadge :fecha-limite="ot.fecha_limite_sla" :estado="ot.estado" />
        </div>

        <div class="flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-slate-800/80">
          <div class="flex items-center gap-1.5">
            <span>📍 {{ ot.ubicacion }}</span>
            <span class="text-slate-600">•</span>
            <span class="uppercase text-[10px] font-bold text-slate-400">{{ ot.tipo_ubicacion || 'urbana' }}</span>
          </div>
          <div class="flex items-center gap-1 font-semibold text-blue-400">
            <span>Ver Detalle</span>
            <span>→</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import SlaBadge from '@/components/common/SlaBadge.vue';

const router = useRouter();
const ots = ref([]);
const loading = ref(true);
const filtroActivo = ref('todos');

const filtros = [
  { id: 'todos', label: 'Todas' },
  { id: 'pendientes', label: 'Pendientes / En Ruta' },
  { id: 'solucionadas', label: 'Solucionadas' },
];

const fetchOts = async () => {
  loading.value = true;
  try {
    const token = localStorage.getItem('smu_token');
    const res = await fetch('/api/ots', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json',
      },
    });
    const data = await res.json();
    if (data.status === 'success') {
      ots.value = data.data;
    }
  } catch (err) {
    console.error("Error al cargar OTs:", err);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchOts);

const pendientesCount = computed(() => {
  return ots.value.filter(o => !['solucionada', 'finalizada'].includes(o.estado)).length;
});

const solucionadasCount = computed(() => {
  return ots.value.filter(o => ['solucionada', 'finalizada'].includes(o.estado)).length;
});

const filteredOts = computed(() => {
  if (filtroActivo.value === 'pendientes') {
    return ots.value.filter(o => !['solucionada', 'finalizada'].includes(o.estado));
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
  return 'bg-blue-100 text-blue-800 border border-blue-200 dark:bg-blue-950 dark:text-blue-400 dark:border-blue-500/30';
};
</script>

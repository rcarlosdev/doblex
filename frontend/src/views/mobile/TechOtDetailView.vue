<template>
  <div class="min-h-screen bg-slate-950 text-slate-100 p-4 space-y-5 pb-24">
    <!-- Header Navegacion -->
    <div class="flex items-center justify-between border-b border-slate-800 pb-3">
      <button @click="$router.push('/mobile/dashboard')" class="flex items-center gap-1 text-xs text-blue-400 font-semibold">
        ← Volver
      </button>
      <div v-if="ot" class="font-mono text-xs font-extrabold text-white bg-slate-900 border border-slate-800 px-3 py-1 rounded-full">
        {{ ot.codigo }}
      </div>
    </div>

    <!-- Indicador de Carga -->
    <div v-if="loading" class="text-center py-12 text-slate-400 text-sm">
      Cargando detalle de la OT...
    </div>

    <div v-else-if="ot" class="space-y-4">
      <!-- Tarjeta Principal de Información -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-3 shadow-xl">
        <div class="flex items-start justify-between">
          <div>
            <span class="text-[10px] font-bold uppercase tracking-wider text-blue-400">Orden de Trabajo</span>
            <h2 class="text-base font-extrabold text-white mt-0.5">{{ ot.descripcion }}</h2>
          </div>
          <SlaBadge :fecha-limite="ot.fecha_limite_sla" :estado="ot.estado" />
        </div>

        <div class="grid grid-cols-2 gap-2 text-xs border-t border-slate-800/80 pt-3">
          <div>
            <span class="text-slate-500 block text-[10px]">Ubicación / Sitio:</span>
            <span class="font-semibold text-slate-200">📍 {{ ot.ubicacion }}</span>
          </div>
          <div>
            <span class="text-slate-500 block text-[10px]">Prioridad & Zona:</span>
            <span class="font-semibold text-amber-400">{{ ot.prioridad || 'P2' }} - {{ (ot.tipo_ubicacion || 'urbana').toUpperCase() }}</span>
          </div>
        </div>

        <!-- Estado Actual -->
        <div class="bg-slate-950 border border-slate-800 rounded-xl p-3 flex items-center justify-between">
          <span class="text-xs text-slate-400">Estado Actual:</span>
          <span :class="estadoBadgeClass(ot.estado)" class="px-3 py-1 rounded-full text-xs font-bold uppercase shadow-sm">
            {{ formatEstado(ot.estado) }}
          </span>
        </div>
      </div>

      <!-- Barra de Transición de Estados Táctil -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-3">
        <h3 class="text-xs font-bold text-slate-300 uppercase tracking-wider">Acciones de Flujo en Campo</h3>

        <div class="grid grid-cols-1 gap-2.5">
          <button
            v-if="ot.estado === 'asignada'"
            @click="cambiarEstado('en_camino')"
            :disabled="updating"
            class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-xl text-xs shadow-lg active:scale-98 transition-all flex items-center justify-center gap-2"
          >
            <span>🚗 Iniciar Desplazamiento (En Camino)</span>
          </button>

          <button
            v-if="ot.estado === 'en_camino'"
            @click="cambiarEstado('en_sitio')"
            :disabled="updating"
            class="w-full bg-amber-600 hover:bg-amber-500 text-white font-bold py-3 rounded-xl text-xs shadow-lg active:scale-98 transition-all flex items-center justify-center gap-2"
          >
            <span>📍 Registrar Llegada (En Sitio)</span>
          </button>

          <button
            v-if="['en_sitio', 'en_progreso'].includes(ot.estado)"
            @click="isCloseModalOpen = true"
            class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold py-3.5 rounded-xl text-sm shadow-xl active:scale-98 transition-all flex items-center justify-center gap-2"
          >
            <span>✅ Finalizar y Cerrar OT</span>
          </button>
        </div>
      </div>

      <!-- Carga de Evidencias Fotográficas -->
      <div class="space-y-3">
        <h3 class="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center justify-between">
          <span>Evidencias Fotográficas Obligatorias</span>
          <span class="text-blue-400 font-mono text-[11px]">{{ ot.evidencias?.length || 0 }} fotos</span>
        </h3>

        <PhotoUploader
          tipo="antes"
          :codigo-ot="ot.codigo"
          :evidencias-count="countEvidencias('antes')"
          @photo-uploaded="uploadPhoto"
        />

        <PhotoUploader
          tipo="durante"
          :codigo-ot="ot.codigo"
          :evidencias-count="countEvidencias('durante')"
          @photo-uploaded="uploadPhoto"
        />

        <PhotoUploader
          tipo="despues"
          :codigo-ot="ot.codigo"
          :evidencias-count="countEvidencias('despues')"
          @photo-uploaded="uploadPhoto"
        />
      </div>

      <!-- Checklist Dinámico de Intervención -->
      <DynamicChecklist subsistema="Sistema Eléctrico y Mantenimiento" />

      <!-- Modal de Cierre -->
      <CloseOtModal
        :is-open="isCloseModalOpen"
        :loading="updating"
        @close="isCloseModalOpen = false"
        @submit="handleCierreSubmit"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import SlaBadge from '@/components/common/SlaBadge.vue';
import PhotoUploader from '@/components/mobile/PhotoUploader.vue';
import DynamicChecklist from '@/components/mobile/DynamicChecklist.vue';
import CloseOtModal from '@/components/mobile/CloseOtModal.vue';

const route = useRoute();
const ot = ref(null);
const loading = ref(true);
const updating = ref(false);
const isCloseModalOpen = ref(false);

const fetchOtDetail = async () => {
  loading.value = true;
  try {
    const token = localStorage.getItem('smu_token');
    const res = await fetch(`/api/ots/${route.params.id}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json',
      },
    });
    const data = await res.json();
    if (data.status === 'success') {
      ot.value = data.data;
    }
  } catch (err) {
    console.error("Error al cargar detalle de OT:", err);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchOtDetail);

const countEvidencias = (tipo) => {
  if (!ot.value?.evidencias) return 0;
  return ot.value.evidencias.filter(e => e.tipo === tipo).length;
};

const cambiarEstado = async (nuevoEstado) => {
  updating.value = true;
  try {
    const token = localStorage.getItem('smu_token');
    const res = await fetch(`/api/ots/${ot.value.id}/estado`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json',
      },
      body: JSON.stringify({ estado: nuevoEstado }),
    });
    const data = await res.json();
    if (data.status === 'success') {
      ot.value.estado = nuevoEstado;
      fetchOtDetail();
    }
  } catch (err) {
    console.error("Error al cambiar estado:", err);
  } finally {
    updating.value = false;
  }
};

const uploadPhoto = async (payload) => {
  updating.value = true;
  try {
    const token = localStorage.getItem('smu_token');
    const res = await fetch(`/api/ots/${ot.value.id}/evidencia`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json',
      },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (data.status === 'success') {
      fetchOtDetail();
    }
  } catch (err) {
    console.error("Error al subir evidencia:", err);
  } finally {
    updating.value = false;
  }
};

const handleCierreSubmit = async (payload) => {
  updating.value = true;
  try {
    const token = localStorage.getItem('smu_token');
    const res = await fetch(`/api/ots/${ot.value.id}/cerrar`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json',
      },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (data.status === 'success') {
      isCloseModalOpen.value = false;
      fetchOtDetail();
    }
  } catch (err) {
    console.error("Error al cerrar OT:", err);
  } finally {
    updating.value = false;
  }
};

const formatEstado = (st) => {
  const map = {
    asignada: 'Asignada',
    en_camino: 'En Camino',
    en_sitio: 'En Sitio',
    en_progreso: 'En Progreso',
    detenida_materiales: 'Detenida por Materiales',
    solucionada: 'Solucionada',
    finalizada: 'Finalizada',
  };
  return map[st] || st;
};

const estadoBadgeClass = (st) => {
  if (st === 'solucionada' || st === 'finalizada') return 'bg-emerald-100 text-emerald-800 border border-emerald-200 dark:bg-emerald-950/80 dark:text-emerald-400 dark:border-emerald-500/40';
  if (st === 'en_camino' || st === 'en_sitio') return 'bg-amber-100 text-amber-800 border border-amber-200 dark:bg-amber-950/80 dark:text-amber-300 dark:border-amber-500/40';
  return 'bg-blue-100 text-blue-800 border border-blue-200 dark:bg-blue-950/80 dark:text-blue-300 dark:border-blue-500/40';
};
</script>

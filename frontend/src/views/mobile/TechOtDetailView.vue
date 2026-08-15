<template>
  <div class="min-h-screen bg-slate-100 dark:bg-[#0a0b10] text-slate-900 dark:text-slate-100 p-4 space-y-4 pb-24 transition-colors duration-300">
    <!-- Header de Detalle -->
    <div class="flex items-center justify-between border-b border-slate-200 dark:border-white/10 pb-3">
      <div class="flex items-center gap-3">
        <button 
          @click="$router.push('/mobile/dashboard')" 
          class="p-2 bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-white/5 active:scale-95 transition-all shadow-sm"
        >
          <IconArrowLeft class="w-5 h-5 stroke-[2]" />
        </button>
        <div v-if="ot">
          <div class="flex items-center gap-2">
            <span class="font-mono text-sm font-extrabold text-red-600 dark:text-red-400">{{ ot.codigo }}</span>
            <span :class="estadoBadgeClass(ot.estado)" class="px-2 py-0.5 rounded text-[10px] font-extrabold uppercase">
              {{ formatEstado(ot.estado) }}
            </span>
          </div>
          <p class="text-xs text-slate-500 dark:text-slate-400 font-medium truncate max-w-[200px] sm:max-w-xs">{{ ot.descripcion }}</p>
        </div>
      </div>
      <button 
        @click="fetchOtDetail" 
        class="p-2 bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl text-slate-700 dark:text-slate-300 hover:text-red-600 dark:hover:text-red-400 active:scale-95 transition-all shadow-sm"
      >
        <IconRefresh class="w-5 h-5 stroke-[2]" :class="{ 'animate-spin': loading }" />
      </button>
    </div>

    <!-- Indicador de Carga -->
    <div v-if="loading" class="text-center py-12 text-slate-500 dark:text-slate-400 text-sm flex flex-col items-center gap-2">
      <IconRefresh class="w-6 h-6 animate-spin text-red-600" />
      <span>Cargando detalle de la OT...</span>
    </div>

    <div v-else-if="ot" class="space-y-4">
      
      <!-- Navegación por Pestañas Segmentadas Móviles (5 Pestañas) -->
      <div class="bg-slate-200/80 dark:bg-[#121215] p-1 rounded-2xl border border-slate-200/80 dark:border-white/10 select-none">
        <div class="grid grid-cols-5 gap-1 text-center">
          <button
            v-for="t in tabs"
            :key="t.id"
            @click="activeTab = t.id"
            class="flex flex-col items-center justify-center py-2 px-1 rounded-xl text-xs font-bold transition-all duration-200"
            :class="activeTab === t.id 
              ? 'bg-red-600 text-white shadow-md shadow-red-600/20' 
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-white/40 dark:hover:bg-white/5'"
          >
            <component :is="t.icon" class="w-4 h-4 stroke-[2.2] mb-0.5" />
            <span class="truncate text-[10px] sm:text-xs font-extrabold">{{ t.shortLabel }}</span>
          </button>
        </div>
      </div>

      <!-- CONTENIDO PESTAÑA 1: FLUJO Y ACCIÓN -->
      <div v-if="activeTab === 'flujo'" class="space-y-4">
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-4 space-y-3 shadow-sm">
          <h3 class="text-xs font-extrabold text-slate-700 dark:text-slate-300 uppercase tracking-wider">Acciones de Desplazamiento & Campo</h3>

          <div class="grid grid-cols-1 gap-2.5">
            <button
              v-if="ot.estado === 'asignada'"
              @click="pedirConfirmacionDesplazamiento"
              :disabled="updating"
              class="w-full bg-red-600 hover:bg-red-500 text-white font-extrabold py-3.5 rounded-xl text-xs shadow-lg shadow-red-600/20 active:scale-98 transition-all flex items-center justify-center gap-2"
            >
              <IconCar class="w-5 h-5 stroke-[2]" />
              <span>Iniciar Desplazamiento (En Camino)</span>
            </button>

            <button
              v-if="ot.estado === 'en_camino'"
              @click="pedirConfirmacionLlegada"
              :disabled="updating"
              class="w-full bg-amber-600 hover:bg-amber-500 text-white font-extrabold py-3.5 rounded-xl text-xs shadow-lg active:scale-98 transition-all flex items-center justify-center gap-2"
            >
              <IconMapPinCheck class="w-5 h-5 stroke-[2]" />
              <span>Marcar Llegada a Sitio (GPS & Timestamp)</span>
            </button>

            <!-- Advertencia si la OT no está totalmente diligenciada -->
            <div v-if="!canCloseOt && ['en_sitio', 'en_progreso'].includes(ot.estado)" class="bg-amber-50 dark:bg-amber-950/60 border border-amber-200 dark:border-amber-800/80 rounded-xl p-3.5 space-y-2 text-xs">
              <div class="font-extrabold text-amber-800 dark:text-amber-300 flex items-center gap-1.5">
                <IconAlertTriangle class="w-4 h-4 stroke-[2] text-amber-600 dark:text-amber-400 shrink-0" />
                <span>Diligenciamiento Obligatorio Pendiente para Cierre:</span>
              </div>
              <ul class="space-y-1 pl-1">
                <li v-for="(req, i) in requisitosFaltantes" :key="i" class="font-bold text-rose-600 dark:text-rose-400 flex items-center gap-1.5 text-[11px]">
                  <span class="w-1.5 h-1.5 rounded-full bg-rose-500 shrink-0"></span>
                  <span>{{ req }}</span>
                </li>
              </ul>
              <div class="flex gap-2 pt-1 flex-wrap">
                <button v-if="countEvidencias('antes') < 1 || countEvidencias('durante') < 1 || countEvidencias('despues') < 1" @click="activeTab = 'evidencias'" class="bg-amber-200/80 dark:bg-amber-900/80 text-amber-900 dark:text-amber-100 font-extrabold px-2.5 py-1 rounded-lg text-[10px] hover:underline flex items-center gap-1">
                  <IconCamera class="w-3.5 h-3.5 stroke-[2]" />
                  <span>Ir a Cargar Fotos</span>
                </button>
                <button v-if="!ot.avances || ot.avances.length === 0" @click="activeTab = 'avances'" class="bg-amber-200/80 dark:bg-amber-900/80 text-amber-900 dark:text-amber-100 font-extrabold px-2.5 py-1 rounded-lg text-[10px] hover:underline flex items-center gap-1">
                  <IconActivity class="w-3.5 h-3.5 stroke-[2]" />
                  <span>Ir a Bitácora PDT</span>
                </button>
              </div>
            </div>

            <button
              v-if="['en_sitio', 'en_progreso'].includes(ot.estado)"
              @click="isCloseModalOpen = true"
              :disabled="!canCloseOt || updating"
              class="w-full font-black py-4 rounded-xl text-sm shadow-xl transition-all flex items-center justify-center gap-2"
              :class="canCloseOt 
                ? 'bg-emerald-600 hover:bg-emerald-500 text-white active:scale-98 cursor-pointer' 
                : 'bg-slate-200 dark:bg-slate-800/80 text-slate-400 dark:text-slate-500 border border-slate-300 dark:border-slate-700 cursor-not-allowed opacity-80'"
            >
              <IconCircleCheck class="w-5 h-5 stroke-[2]" />
              <span>{{ canCloseOt ? 'Finalizar y Cerrar OT' : 'Diligenciar Totalmente para Cerrar' }}</span>
            </button>

            <div v-if="['solucionada', 'finalizada'].includes(ot.estado)" class="bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800/80 rounded-xl p-3 text-center space-y-1 shadow-sm">
              <div class="text-xs font-bold text-emerald-700 dark:text-emerald-400 flex items-center justify-center gap-1.5">
                <IconCircleCheck class="w-4 h-4 stroke-[2]" />
                <span>Orden Solucionada Técnicamente</span>
              </div>
              <p class="text-[11px] text-slate-700 dark:text-slate-300" v-if="ot.observaciones_cierre">{{ ot.observaciones_cierre }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- CONTENIDO PESTAÑA 2: MINUTOGRAMA / AVANCES (PDT) -->
      <div v-if="activeTab === 'avances'" class="space-y-4">
        <!-- Formulario para publicar reporte -->
        <div v-if="!['solucionada', 'finalizada'].includes(ot.estado)" class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3 shadow-sm">
          <h3 class="text-xs font-extrabold text-slate-700 dark:text-slate-300 uppercase tracking-wider">Reportar Avance PDT Minutograma</h3>
          <div class="space-y-2">
            <div>
              <label class="text-[11px] text-slate-600 dark:text-slate-400 font-semibold block mb-1">Descripción del Avance / Bitácora</label>
              <textarea
                v-model="nuevoAvance.descripcion"
                rows="2"
                placeholder="Ej. Se realiza revisión de tablero eléctrico y cambio de breaker..."
                class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-2.5 text-xs text-slate-900 dark:text-white focus:ring-2 focus:ring-red-500 focus:outline-none"
              ></textarea>
            </div>
            <div class="flex gap-3 items-center">
              <div class="flex-1">
                <label class="text-[11px] text-slate-600 dark:text-slate-400 font-semibold block mb-1">% Incremental hoy</label>
                <input
                  v-model.number="nuevoAvance.porcentaje"
                  type="number"
                  min="1"
                  max="100"
                  class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-2 text-xs text-slate-900 dark:text-white font-mono"
                />
              </div>
              <div class="flex-1 pt-4">
                <button
                  @click="pedirConfirmacionAvance"
                  :disabled="updating || !nuevoAvance.descripcion"
                  class="w-full bg-red-600 hover:bg-red-500 text-white font-bold py-2.5 rounded-xl text-xs shadow-md shadow-red-600/20 active:scale-98 transition-all flex items-center justify-center gap-1.5"
                >
                  <IconSend class="w-4 h-4 stroke-[2]" />
                  <span>Registrar</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Histórico de Avances -->
        <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3 shadow-sm">
          <h3 class="text-xs font-extrabold text-slate-700 dark:text-slate-300 uppercase tracking-wider flex items-center justify-between">
            <span>Histórico de Bitácora (PDT)</span>
            <span class="text-red-600 dark:text-red-400 font-mono text-[11px]">{{ ot.avances?.length || 0 }} registros</span>
          </h3>

          <div v-if="!ot.avances || ot.avances.length === 0" class="text-center py-6 text-slate-400 dark:text-slate-500 text-xs">
            No se han registrado avances diarios todavía.
          </div>
          <div v-else class="space-y-2.5">
            <div v-for="av in ot.avances" :key="av.id" class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-1">
              <div class="flex justify-between items-center text-xs">
                <span class="font-extrabold text-red-600 dark:text-red-400">+{{ av.porcentaje }}% de avance</span>
                <span class="text-[10px] text-slate-400 dark:text-slate-500 font-mono">{{ formatDate(av.created_at || av.fecha_reporte) }}</span>
              </div>
              <p class="text-xs text-slate-800 dark:text-slate-200">{{ av.descripcion }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- CONTENIDO PESTAÑA 3: EVIDENCIAS FOTOGRÁFICAS -->
      <div v-if="activeTab === 'evidencias'" class="space-y-4">
        <h3 class="text-xs font-extrabold text-slate-700 dark:text-slate-300 uppercase tracking-wider flex items-center justify-between">
          <span>Evidencias Fotográficas Obligatorias</span>
          <span class="text-red-600 dark:text-red-400 font-mono text-[11px]">{{ ot.evidencias?.length || 0 }} fotos cargadas</span>
        </h3>

        <PhotoUploader
          tipo="antes"
          :codigo-ot="ot.codigo"
          :evidencias-count="countEvidencias('antes')"
          @photo-uploaded="pedirConfirmacionFoto"
        />

        <PhotoUploader
          tipo="durante"
          :codigo-ot="ot.codigo"
          :evidencias-count="countEvidencias('durante')"
          @photo-uploaded="pedirConfirmacionFoto"
        />

        <PhotoUploader
          tipo="despues"
          :codigo-ot="ot.codigo"
          :evidencias-count="countEvidencias('despues')"
          @photo-uploaded="pedirConfirmacionFoto"
        />
      </div>

      <!-- CONTENIDO PESTAÑA 4: REPUESTOS LPU -->
      <div v-if="activeTab === 'repuestos'" class="space-y-4">
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-4 space-y-3 shadow-sm">
          <div class="flex justify-between items-center">
            <h3 class="text-xs font-extrabold text-slate-700 dark:text-slate-300 uppercase tracking-wider">Insumos & Repuestos LPU Vinculados</h3>
            <button @click="isCloseModalOpen = true" class="text-xs text-red-600 dark:text-red-400 font-bold hover:underline flex items-center gap-1">
              <IconPlus class="w-3.5 h-3.5 stroke-[2.5]" />
              <span>Agregar / Modificar</span>
            </button>
          </div>

          <div v-if="!ot.repuestos || ot.repuestos.length === 0" class="text-center py-6 text-slate-400 dark:text-slate-500 text-xs">
            No se han registrado repuestos utilizados en esta intervención.
          </div>
          <div v-else class="space-y-2">
            <div v-for="rep in ot.repuestos" :key="rep.id" class="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800/80 rounded-xl p-3 flex justify-between items-center">
              <div>
                <div class="text-xs font-bold text-slate-900 dark:text-white">{{ rep.nombre_item }}</div>
                <div class="text-[10px] text-slate-500 dark:text-slate-400">Unidad: {{ rep.unidad_medida || 'unidad' }}</div>
              </div>
              <div class="bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 font-mono text-xs px-2.5 py-1 rounded-lg font-bold">
                Cant: {{ rep.cantidad }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CONTENIDO PESTAÑA 5: CHECKLIST DE INTERVENCIÓN -->
      <div v-if="activeTab === 'checklist'" class="space-y-4">
        <DynamicChecklist
          :subsistema="ot.subsistema || 'Sistema Eléctrico y Mantenimiento'"
          :ot-id="ot.id"
          @checklist-updated="handleChecklistUpdated"
        />
      </div>

      <!-- Modal de Cierre -->
      <CloseOtModal
        :is-open="isCloseModalOpen"
        :loading="updating"
        :error-msg="cierreErrorMsg"
        @close="isCloseModalOpen = false"
        @submit="pedirConfirmacionCierre"
      />

      <!-- Banner de Notificación Toast / Alerta de Mensajes al Usuario -->
      <div v-if="alertNotification.show" class="fixed top-4 right-4 left-4 sm:left-auto sm:w-96 z-[130] transition-all duration-300 transform">
        <div 
          class="p-4 rounded-2xl border shadow-2xl flex items-start gap-3 select-none backdrop-blur-md"
          :class="{
            'bg-emerald-50/95 border-emerald-300 text-emerald-950 dark:bg-emerald-950/90 dark:border-emerald-700 dark:text-emerald-100': alertNotification.type === 'success',
            'bg-rose-50/95 border-rose-300 text-rose-950 dark:bg-rose-950/90 dark:border-rose-700 dark:text-rose-100': alertNotification.type === 'error',
            'bg-amber-50/95 border-amber-300 text-amber-950 dark:bg-amber-950/90 dark:border-amber-700 dark:text-amber-100': alertNotification.type === 'warning'
          }"
        >
          <IconCircleCheck v-if="alertNotification.type === 'success'" class="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5 stroke-[2]" />
          <IconAlertTriangle v-else class="w-5 h-5 text-rose-600 dark:text-rose-400 shrink-0 mt-0.5 stroke-[2]" />
          <div class="flex-1 text-xs space-y-0.5">
            <div class="font-extrabold uppercase tracking-wide text-[11px]">{{ alertNotification.title }}</div>
            <div class="text-xs leading-relaxed font-medium">{{ alertNotification.message }}</div>
          </div>
          <button @click="alertNotification.show = false" class="p-1 hover:opacity-75 font-bold">
            <IconX class="w-4 h-4 stroke-[2]" />
          </button>
        </div>
      </div>

      <!-- Modal de Confirmación Previa para Acciones de Guardado/Finalización -->
      <ConfirmDialogModal
        :is-open="confirmModal.isOpen"
        :title="confirmModal.title"
        :subtitle="confirmModal.subtitle"
        :message="confirmModal.message"
        :confirm-text="confirmModal.confirmText"
        :type="confirmModal.type"
        :loading="updating"
        @confirm="handleConfirmAction"
        @cancel="confirmModal.isOpen = false"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import client from '@/api/client';
import SlaBadge from '@/components/common/SlaBadge.vue';
import PhotoUploader from '@/components/mobile/PhotoUploader.vue';
import DynamicChecklist from '@/components/mobile/DynamicChecklist.vue';
import CloseOtModal from '@/components/mobile/CloseOtModal.vue';
import ConfirmDialogModal from '@/components/common/ConfirmDialogModal.vue';
import { 
  IconArrowLeft, 
  IconRefresh, 
  IconBuildingBroadcastTower, 
  IconMapPin, 
  IconMapPinCheck,
  IconSteeringWheel, 
  IconActivity, 
  IconCamera, 
  IconBox, 
  IconListCheck,
  IconCar,
  IconCircleCheck,
  IconSend,
  IconPlus,
  IconAlertTriangle,
  IconX
} from '@tabler/icons-vue';

const route = useRoute();
const ot = ref(null);
const loading = ref(true);
const updating = ref(false);
const isCloseModalOpen = ref(false);
const cierreErrorMsg = ref('');
const activeTab = ref('flujo');

const alertNotification = ref({
  show: false,
  type: 'success',
  title: '',
  message: '',
});

const showNotification = (type, title, message) => {
  alertNotification.value = { show: true, type, title, message };
  setTimeout(() => {
    if (alertNotification.value.message === message) {
      alertNotification.value.show = false;
    }
  }, 7000);
};

const confirmModal = ref({
  isOpen: false,
  title: '',
  subtitle: '',
  message: '',
  confirmText: 'Sí, Confirmar',
  type: 'info',
  action: null,
});

const openConfirm = (opts) => {
  confirmModal.value = {
    isOpen: true,
    title: opts.title || 'Confirmar Acción',
    subtitle: opts.subtitle || 'Verifique antes de continuar',
    message: opts.message || '¿Desea proceder?',
    confirmText: opts.confirmText || 'Sí, Confirmar',
    type: opts.type || 'info',
    action: opts.action,
  };
};

const handleConfirmAction = async () => {
  if (confirmModal.value.action) {
    const act = confirmModal.value.action;
    confirmModal.value.isOpen = false;
    await act();
  }
};

const tabs = [
  { id: 'flujo', label: 'Flujo & Acción', shortLabel: 'Flujo', icon: IconSteeringWheel },
  { id: 'avances', label: 'Minutograma PDT', shortLabel: 'Bitácora', icon: IconActivity },
  { id: 'evidencias', label: 'Evidencias', shortLabel: 'Fotos', icon: IconCamera },
  { id: 'repuestos', label: 'Repuestos LPU', shortLabel: 'Insumos', icon: IconBox },
  { id: 'checklist', label: 'Checklist', shortLabel: 'Checklist', icon: IconListCheck },
];

const nuevoAvance = ref({
  descripcion: '',
  porcentaje: 10,
});

const fetchOtDetail = async () => {
  loading.value = true;
  try {
    const res = await client.get(`/ots/${route.params.id}`);
    if (res.data.status === 'success') {
      ot.value = res.data.data;
    }
  } catch (err) {
    const msg = err.response?.data?.message || 'Error al cargar detalle de OT.';
    showNotification('error', 'Error de Carga', msg);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchOtDetail);

const countEvidencias = (tipo) => {
  if (!ot.value?.evidencias) return 0;
  return ot.value.evidencias.filter(e => e.tipo === tipo).length;
};

const handleChecklistUpdated = (data) => {
  if (ot.value && !['solucionada', 'finalizada'].includes(ot.value.estado)) {
    // Actualizar el porcentaje de ejecución PDT dinámicamente según avance del checklist
    ot.value.progreso = Math.max(ot.value.progreso || 0, data.percentage);
  }
};

const requisitosFaltantes = computed(() => {
  if (!ot.value) return [];
  const faltantes = [];

  if (countEvidencias('antes') < 1) {
    faltantes.push('Falta Evidencia Fotográfica de ANTES (Mínimo 1 foto)');
  }
  if (countEvidencias('durante') < 1) {
    faltantes.push('Falta Evidencia Fotográfica de DURANTE (Mínimo 1 foto)');
  }
  if (countEvidencias('despues') < 1) {
    faltantes.push('Falta Evidencia Fotográfica de DESPUÉS (Mínimo 1 foto)');
  }
  if (!ot.value.avances || ot.value.avances.length === 0) {
    faltantes.push('Falta Registro de Bitácora / Avance PDT de la intervención');
  }

  return faltantes;
});

const canCloseOt = computed(() => {
  return requisitosFaltantes.value.length === 0;
});

const pedirConfirmacionDesplazamiento = () => {
  openConfirm({
    title: 'Iniciar Desplazamiento',
    subtitle: 'Acción de Campo',
    message: '¿Está seguro de iniciar el desplazamiento hacia el sitio? La OT cambiará a estado "En Camino".',
    confirmText: 'Sí, Iniciar Desplazamiento',
    type: 'warning',
    action: () => cambiarEstado('en_camino')
  });
};

const pedirConfirmacionLlegada = () => {
  openConfirm({
    title: 'Marcar Llegada a Sitio',
    subtitle: 'Registro GPS & Hora',
    message: '¿Confirmar llegada al sitio telecom? Se registrará la marca de tiempo actual y coordenadas GPS.',
    confirmText: 'Sí, Registrar Llegada',
    type: 'success',
    action: () => cambiarEstado('en_sitio')
  });
};

const cambiarEstado = async (nuevoEstado) => {
  updating.value = true;
  try {
    const res = await client.put(`/ots/${ot.value.id}/estado`, { estado: nuevoEstado });
    if (res.data.status === 'success') {
      ot.value.estado = nuevoEstado;
      showNotification('success', 'Estado Actualizado', `La OT cambió a estado "${formatEstado(nuevoEstado)}".`);
      fetchOtDetail();
    }
  } catch (err) {
    const msg = err.response?.data?.message || 'No se pudo actualizar el estado de la OT.';
    showNotification('error', 'Error al Cambiar Estado', msg);
  } finally {
    updating.value = false;
  }
};

const registrarLlegadaSitio = () => {
  pedirConfirmacionLlegada();
};

const pedirConfirmacionAvance = () => {
  if (!nuevoAvance.value.descripcion) return;
  openConfirm({
    title: 'Publicar Avance de Bitácora',
    subtitle: 'Minutograma PDT',
    message: `¿Desea registrar el avance de +${nuevoAvance.value.porcentaje}%: "${nuevoAvance.value.descripcion}"?`,
    confirmText: 'Sí, Publicar Avance',
    type: 'info',
    action: () => executeSubmitAvance()
  });
};

const executeSubmitAvance = async () => {
  updating.value = true;
  try {
    const res = await client.post('/avances', {
      ot_id: ot.value.id,
      descripcion: nuevoAvance.value.descripcion,
      porcentaje: nuevoAvance.value.porcentaje,
      fecha_reporte: new Date().toISOString().split('T')[0],
    });
    if (res.data.status === 'success') {
      nuevoAvance.value.descripcion = '';
      nuevoAvance.value.porcentaje = 10;
      showNotification('success', 'Avance Registrado', 'Se publicó el avance en la bitácora PDT.');
      fetchOtDetail();
    }
  } catch (err) {
    const msg = err.response?.data?.message || 'No se pudo registrar el avance.';
    showNotification('error', 'Error al Publicar Avance', msg);
  } finally {
    updating.value = false;
  }
};

const pedirConfirmacionFoto = (payload) => {
  openConfirm({
    title: 'Guardar Evidencia Fotográfica',
    subtitle: `Evidencia ${payload.tipo.toUpperCase()}`,
    message: `¿Desea subir y guardar esta fotografía como evidencia de ${payload.tipo.toUpperCase()} con marca de agua GPS incrustada?`,
    confirmText: 'Sí, Guardar Foto',
    type: 'success',
    action: () => executeUploadPhoto(payload)
  });
};

const executeUploadPhoto = async (payload) => {
  updating.value = true;
  try {
    const res = await client.post(`/ots/${ot.value.id}/evidencia`, payload);
    if (res.data.status === 'success') {
      showNotification('success', 'Evidencia Cargada', `Se guardó la foto de ${payload.tipo.toUpperCase()} con éxito.`);
      fetchOtDetail();
    }
  } catch (err) {
    const msg = err.response?.data?.message || 'No se pudo subir la fotografía de evidencia.';
    showNotification('error', 'Error al Guardar Foto', msg);
  } finally {
    updating.value = false;
  }
};

const pedirConfirmacionCierre = (payload) => {
  openConfirm({
    title: 'Finalizar y Solucionar OT',
    subtitle: `Cierre Técnico de la Orden ${ot.value?.codigo || ''}`,
    message: `¿Está seguro de confirmar y finalizar técnicamente esta Orden de Trabajo? La orden cambiará a estado Solucionada y no podrá ser editada por el técnico.`,
    confirmText: 'Sí, Cerrar OT',
    type: 'danger',
    action: () => executeHandleCierreSubmit(payload)
  });
};

const executeHandleCierreSubmit = async (payload) => {
  cierreErrorMsg.value = '';
  updating.value = true;
  try {
    const res = await client.post(`/ots/${ot.value.id}/cerrar`, payload);
    if (res.data.status === 'success') {
      isCloseModalOpen.value = false;
      showNotification('success', 'Orden Solucionada', res.data.message || 'La Orden de Trabajo fue finalizada con éxito.');
      fetchOtDetail();
    }
  } catch (err) {
    const msg = err.response?.data?.message || err.response?.data?.error || 'No se pudo cerrar la OT.';
    cierreErrorMsg.value = msg;
    showNotification('error', 'Error de Validación / Cierre', msg);
  } finally {
    updating.value = false;
  }
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return d.toLocaleDateString('es-CO', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' });
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
  return 'bg-red-100 text-red-800 border border-red-200 dark:bg-red-950/80 dark:text-red-300 dark:border-red-500/40';
};
</script>



<template>
  <Teleport to="body">
    <div v-if="isOpen" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-xs flex items-center justify-center p-3 sm:p-4 overflow-y-auto">
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl w-full max-w-lg overflow-hidden shadow-2xl p-4 sm:p-6 my-auto flex flex-col space-y-4">
        
        <!-- Header -->
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-3">
          <div class="flex items-center gap-2.5">
            <div class="w-9 h-9 rounded-xl bg-amber-50 dark:bg-amber-950/80 border border-amber-200 dark:border-amber-800 flex items-center justify-center text-amber-600 dark:text-amber-400 shrink-0">
              <IconMapPinCheck class="w-5 h-5 stroke-[2]" />
            </div>
            <div>
              <h3 class="text-sm sm:text-base font-extrabold text-slate-900 dark:text-white leading-tight">
                Registro de Llegada a Sitio
              </h3>
              <p class="text-[11px] text-slate-500 dark:text-slate-400 font-medium">
                Técnico con carnet visible y la estación al fondo
              </p>
            </div>
          </div>
          <button
            @click="$emit('close')"
            class="text-slate-400 hover:text-slate-700 dark:hover:text-white p-1 rounded-lg"
          >
            <IconX class="w-5 h-5 stroke-[2]" />
          </button>
        </div>

        <!-- Captura de Localización y Fecha/Hora -->
        <div class="p-3 bg-amber-50/70 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/50 rounded-xl space-y-1.5 text-xs text-amber-900 dark:text-amber-200">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-1.5">
              <IconClock class="w-4 h-4 text-amber-600 dark:text-amber-400 shrink-0" />
              <span class="font-bold">Fecha y Hora:</span>
              <span class="font-medium font-mono text-[11px]">{{ fechaHoraCaptura }}</span>
            </div>
            <button 
              @click="actualizarGps"
              class="text-[10px] text-amber-700 dark:text-amber-300 font-bold hover:underline"
            >
              Actualizar GPS
            </button>
          </div>
          <div class="flex items-center gap-1.5 pt-0.5 border-t border-amber-200/60 dark:border-amber-900/40">
            <IconMapPin class="w-4 h-4 text-amber-600 dark:text-amber-400 shrink-0" />
            <span class="font-bold">Localización (GPS):</span>
            <span class="font-mono text-[11px] font-semibold text-amber-950 dark:text-amber-100">
              {{ gpsCoords }}
            </span>
          </div>
        </div>

        <!-- Instrucción de la foto -->
        <div class="p-2.5 rounded-xl bg-slate-50 dark:bg-white/5 border border-slate-200/80 dark:border-white/10 text-[11px] text-slate-600 dark:text-slate-400 flex items-start gap-2">
          <IconIdBadge2 class="w-4 h-4 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
          <span>
            Tome una <strong>única fotografía</strong> donde aparezca el <strong>técnico portando el carnet legible</strong> y de fondo se aprecie la <strong>estación / torre</strong>. La foto quedará sellada con las coordenadas GPS y fecha/hora.
          </span>
        </div>

        <!-- Componente de captura fotográfica única -->
        <div class="space-y-2">
          <SinglePhotoCapture
            v-model="fotoLlegada"
            label="Foto del Técnico con Carnet y Sitio al Fondo *"
            tag="LLEGADA - TECNICO + CARNET + SITIO"
            :codigo-ot="codigoOt"
            placeholder="Tomar foto del técnico con carnet y sitio atrás"
            :required="true"
          />
        </div>

        <!-- Error local si falta la foto -->
        <div v-if="localError" class="p-2.5 rounded-xl bg-rose-50 dark:bg-rose-950/60 border border-rose-200 dark:border-rose-800 text-xs text-rose-700 dark:text-rose-300 font-medium">
          {{ localError }}
        </div>

        <!-- Botones de Acción -->
        <div class="flex items-center justify-end gap-2.5 pt-2 border-t border-slate-100 dark:border-white/10">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 rounded-xl text-xs font-bold text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-white/5"
          >
            Cancelar
          </button>
          <button
            type="button"
            @click="confirmarLlegada"
            :disabled="saving || !fotoLlegada"
            class="bg-amber-600 hover:bg-amber-500 disabled:opacity-50 text-white font-extrabold px-5 py-2.5 rounded-xl text-xs shadow-lg shadow-amber-600/20 flex items-center gap-2 active:scale-98 transition-all cursor-pointer"
          >
            <IconCheck class="w-4 h-4 stroke-[2.5]" />
            <span>{{ saving ? 'Registrando...' : 'Confirmar Arribo a Sitio' }}</span>
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { 
  IconMapPinCheck, 
  IconMapPin,
  IconX, 
  IconClock, 
  IconIdBadge2, 
  IconCheck 
} from '@tabler/icons-vue';
import SinglePhotoCapture from './SinglePhotoCapture.vue';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  codigoOt: {
    type: String,
    default: ''
  },
  initialFoto: {
    type: String,
    default: ''
  },
  initialCarnet: {
    type: String,
    default: ''
  },
  saving: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close', 'confirm']);

const fotoLlegada = ref(props.initialFoto || props.initialCarnet || '');
const localError = ref('');
const fechaHoraCaptura = ref('');
const gpsCoords = ref('Obteniendo GPS...');

const actualizarGps = () => {
  gpsCoords.value = 'Obteniendo GPS...';
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        gpsCoords.value = `${pos.coords.latitude.toFixed(6)}, ${pos.coords.longitude.toFixed(6)}`;
      },
      () => {
        gpsCoords.value = 'GPS no detectado (activar ubicación)';
      },
      { timeout: 8000, enableHighAccuracy: true }
    );
  } else {
    gpsCoords.value = 'Geolocalización no soportada';
  }
};

const actualizarFechaHora = () => {
  const ahora = new Date();
  fechaHoraCaptura.value = ahora.toLocaleString('es-CO', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
};

onMounted(() => {
  actualizarFechaHora();
  actualizarGps();
});

const confirmarLlegada = () => {
  localError.value = '';
  if (!fotoLlegada.value) {
    localError.value = 'Debe tomar la foto del técnico con el carnet y la estación al fondo para confirmar.';
    return;
  }

  const nowIso = new Date().toISOString();
  emit('confirm', {
    foto_llegada: fotoLlegada.value,
    foto_carnet: fotoLlegada.value,
    foto_estacion: fotoLlegada.value,
    gps: gpsCoords.value,
    fecha_hora_texto: fechaHoraCaptura.value,
    timestamp: nowIso
  });
};
</script>

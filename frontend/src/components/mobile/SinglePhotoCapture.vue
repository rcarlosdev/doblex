<template>
  <div class="space-y-1.5">
    <label v-if="label" class="block text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
      {{ label }} <span v-if="required" class="text-red-500">*</span>
    </label>

    <!-- ESTADO A: VISTA PREVIA CON MARCA DE AGUA PENDIENTE DE CONFIRMAR (FLUJO DE CONFIRMACIÓN) -->
    <div v-if="previewUrl" class="relative rounded-xl overflow-hidden border-2 border-emerald-500/90 shadow-xl group space-y-0 bg-slate-900 animate-in fade-in duration-200">
      <div class="relative">
        <img :src="previewUrl" alt="Vista Previa Evidencia" class="w-full h-56 object-cover" />
        <div class="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black/95 via-black/75 to-transparent p-3 text-[11px] text-slate-200 space-y-0.5 font-mono">
          <div>GPS: {{ coordsText }}</div>
          <div>Fecha: {{ dateText }}</div>
        </div>
      </div>

      <div class="p-2.5 bg-slate-50 dark:bg-[#0a0b10] flex items-center justify-end gap-2 border-t border-slate-200 dark:border-white/10">
        <button
          type="button"
          @click="cancelarPreview"
          class="px-3.5 py-1.5 rounded-lg text-xs font-bold text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-white/10 transition-colors cursor-pointer"
        >
          Cancelar
        </button>
        <button
          type="button"
          @click="confirmarGuardarFoto"
          class="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-1.5 rounded-lg text-xs font-black shadow-md flex items-center gap-1.5 active:scale-95 transition-all cursor-pointer"
        >
          <IconCheck class="w-4 h-4 stroke-[2.5]" />
          <span>Guardar esta Foto</span>
        </button>
      </div>
    </div>

    <!-- ESTADO B: NO HAY FOTO CARGADA (Y NO ESTÁ EN PREVIEW) -->
    <div v-else-if="!modelValue" class="relative">
      <button
        type="button"
        @click="triggerCamera"
        :disabled="disabled || processing"
        class="w-full flex items-center justify-center gap-2 py-2.5 px-3 rounded-xl border border-dashed text-xs font-bold transition-all cursor-pointer"
        :class="required && touched && !modelValue 
          ? 'border-rose-400 bg-rose-50/60 dark:bg-rose-950/30 text-rose-600 dark:text-rose-400' 
          : 'border-slate-300 dark:border-white/20 bg-slate-50 dark:bg-[#0a0b10] text-slate-700 dark:text-slate-300 hover:border-red-500 hover:text-red-600 dark:hover:text-red-400'"
      >
        <IconCamera class="w-4 h-4 text-red-600 dark:text-red-400 shrink-0 stroke-[2]" />
        <span>{{ processing ? 'Procesando marca de agua...' : (placeholder || 'Tomar / Subir Foto') }}</span>
      </button>
    </div>

    <!-- ESTADO C: FOTO YA GUARDADA/CONFIRMADA (CON ACCIONES DE ZOOM, CAMBIAR Y BORRAR) -->
    <div v-else class="relative rounded-xl overflow-hidden border border-slate-200 dark:border-white/10 bg-slate-900 group">
      <img
        :src="modelValue"
        alt="Foto evidencia"
        class="w-full h-40 object-cover cursor-pointer hover:opacity-95 transition-opacity"
        @click="showZoom = true"
      />
      <div class="absolute top-2 right-2 flex items-center gap-1.5">
        <button
          type="button"
          @click="showZoom = true"
          class="bg-black/60 hover:bg-black/80 text-white p-1 rounded-lg backdrop-blur-xs transition-colors cursor-pointer"
          title="Ver ampliada"
        >
          <IconEye class="w-3.5 h-3.5" />
        </button>
        <button
          v-if="!disabled"
          type="button"
          @click="triggerCamera"
          class="bg-black/60 hover:bg-black/80 text-white p-1 rounded-lg backdrop-blur-xs transition-colors cursor-pointer"
          title="Tomar nueva foto / Reemplazar"
        >
          <IconCamera class="w-3.5 h-3.5" />
        </button>
        <button
          v-if="!disabled"
          type="button"
          @click="removePhoto"
          class="bg-rose-600/80 hover:bg-rose-600 text-white p-1 rounded-lg backdrop-blur-xs transition-colors cursor-pointer"
          title="Eliminar foto"
        >
          <IconTrash class="w-3.5 h-3.5" />
        </button>
      </div>
      <div class="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black/80 to-transparent p-2 text-[10px] text-white flex items-center justify-between font-mono">
        <span class="truncate font-semibold">{{ tag || 'Evidencia técnica' }}</span>
        <span class="text-emerald-400 font-bold flex items-center gap-0.5 shrink-0">
          <IconCheck class="w-3.5 h-3.5 stroke-[3]" /> Cargada
        </span>
      </div>
    </div>

    <!-- Inputs ocultos para archivo y procesamiento de canvas -->
    <input
      ref="fileInputRef"
      type="file"
      accept="image/*"
      capture="environment"
      class="hidden"
      @change="onFileChange"
    />
    <canvas ref="canvasRef" class="hidden"></canvas>

    <!-- Modal Zoom para ver foto ampliada -->
    <Teleport to="body">
      <div
        v-if="showZoom"
        class="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-3"
        @click="showZoom = false"
      >
        <div class="relative max-w-3xl w-full max-h-[90vh] flex flex-col items-center">
          <img :src="modelValue" alt="Evidencia Ampliada" class="max-w-full max-h-[82vh] rounded-xl object-contain shadow-2xl" />
          <button
            type="button"
            @click="showZoom = false"
            class="mt-3 px-4 py-1.5 bg-white/10 hover:bg-white/20 text-white text-xs font-bold rounded-xl cursor-pointer"
          >
            Cerrar Vista
          </button>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { IconCamera, IconTrash, IconEye, IconCheck } from '@tabler/icons-vue';

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  tag: {
    type: String,
    default: ''
  },
  codigoOt: {
    type: String,
    default: ''
  },
  required: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  placeholder: {
    type: String,
    default: 'Tomar / Subir Foto'
  },
  touched: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue', 'change']);

const fileInputRef = ref(null);
const canvasRef = ref(null);
const processing = ref(false);
const showZoom = ref(false);

const previewUrl = ref(null);
const coordsText = ref('Buscando GPS...');
const dateText = ref('');
const currentGps = ref('Buscando GPS...');

const obtenerGps = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        currentGps.value = `${pos.coords.latitude.toFixed(6)}, ${pos.coords.longitude.toFixed(6)}`;
        coordsText.value = currentGps.value;
      },
      () => {
        currentGps.value = 'GPS no disponible';
        coordsText.value = 'GPS no disponible';
      },
      { enableHighAccuracy: true, timeout: 7000 }
    );
  } else {
    currentGps.value = 'GPS no soportado';
    coordsText.value = 'GPS no soportado';
  }
};

onMounted(() => {
  obtenerGps();
});

const triggerCamera = () => {
  obtenerGps();
  if (fileInputRef.value) {
    fileInputRef.value.click();
  }
};

const onFileChange = (e) => {
  const file = e.target.files?.[0];
  if (!file) return;

  processing.value = true;
  const reader = new FileReader();

  reader.onload = (event) => {
    const img = new Image();
    img.onload = () => {
      drawWatermark(img);
      processing.value = false;
      if (fileInputRef.value) fileInputRef.value.value = '';
    };
    img.onerror = () => {
      processing.value = false;
    };
    img.src = event.target.result;
  };

  reader.readAsDataURL(file);
};

const drawWatermark = (img) => {
  const cvs = canvasRef.value;
  if (!cvs) return;
  const ctx = cvs.getContext('2d');

  // Ajustar resolución máxima para rendimiento y tamaño
  const maxDim = 1280;
  let w = img.width;
  let h = img.height;
  if (w > maxDim || h > maxDim) {
    if (w > h) {
      h = Math.round((h * maxDim) / w);
      w = maxDim;
    } else {
      w = Math.round((w * maxDim) / h);
      h = maxDim;
    }
  }

  cvs.width = w;
  cvs.height = h;
  ctx.drawImage(img, 0, 0, w, h);

  const now = new Date();
  const dateStr = now.toLocaleString('es-CO', { timeZoneName: 'short' });
  dateText.value = dateStr;
  coordsText.value = currentGps.value;

  const barHeight = Math.max(46, Math.floor(h * 0.085));
  ctx.fillStyle = 'rgba(0, 0, 0, 0.75)';
  ctx.fillRect(0, h - barHeight, w, barHeight);

  const fontSize = Math.max(13, Math.floor(barHeight * 0.35));
  ctx.fillStyle = '#ffffff';
  ctx.font = `600 ${fontSize}px monospace, sans-serif`;

  const line1 = `GPS: ${coordsText.value}`;
  const line2 = `FECHA: ${dateStr}`;

  ctx.fillText(line1, 16, h - barHeight + fontSize + 4);
  ctx.fillText(line2, 16, h - barHeight + (fontSize * 2) + 8);

  previewUrl.value = cvs.toDataURL('image/jpeg', 0.82);
};

const confirmarGuardarFoto = () => {
  if (!previewUrl.value) return;
  const finalVal = previewUrl.value;
  emit('update:modelValue', finalVal);
  emit('change', {
    imagen_base64: finalVal,
    gps: coordsText.value,
    fecha: dateText.value
  });
  previewUrl.value = null;
};

const cancelarPreview = () => {
  previewUrl.value = null;
  if (fileInputRef.value) fileInputRef.value.value = '';
};

const removePhoto = () => {
  emit('update:modelValue', '');
  emit('change', '');
};
</script>

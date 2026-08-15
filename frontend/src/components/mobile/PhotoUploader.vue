<template>
  <div class="bg-white dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 rounded-xl p-4 space-y-4 shadow-sm transition-colors duration-300">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <span :class="tipoBadgeClass" class="px-2.5 py-0.5 rounded text-xs font-bold uppercase">
          Evidencia: {{ tipo }}
        </span>
        <span v-if="evidenciasCount > 0" class="text-xs text-slate-500 dark:text-slate-400 font-medium">
          ({{ evidenciasCount }} registradas)
        </span>
      </div>
      <button
        @click="triggerCamera"
        :disabled="uploading"
        class="bg-red-600 hover:bg-red-500 text-white px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 shadow-lg shadow-red-600/20 active:scale-95 transition-all"
      >
        <IconCamera class="w-4 h-4 stroke-[2]" />
        <span>{{ uploading ? 'Procesando...' : 'Tomar Foto' }}</span>
      </button>
    </div>

    <!-- Elemento input tipo file para camara nativa -->
    <input
      ref="fileInput"
      type="file"
      accept="image/*"
      capture="environment"
      class="hidden"
      @change="handlePhotoCapture"
    />

    <!-- Canvas para procesar la marca de agua (Oculto) -->
    <canvas ref="canvas" class="hidden"></canvas>

    <!-- Vista previa de foto procesada con watermark -->
    <div v-if="previewUrl" class="relative rounded-lg overflow-hidden border border-red-500/40 group">
      <img :src="previewUrl" alt="Vista Previa Evidencia" class="w-full h-48 object-cover" />
      <div class="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black/90 via-black/60 to-transparent p-2 text-[10px] text-slate-200 space-y-0.5">
        <div class="font-mono text-emerald-400 font-bold">✓ Marca de agua incrustada</div>
        <div>GPS: {{ coordsText }}</div>
        <div>Fecha: {{ dateText }}</div>
      </div>
      <button
        @click="confirmUpload"
        :disabled="uploading"
        class="absolute top-2 right-2 bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1 rounded text-xs font-bold shadow-md flex items-center gap-1"
      >
        <IconCheck class="w-3.5 h-3.5 stroke-[2.5]" />
        <span>Guardar Evidencia</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { IconCamera, IconCheck } from '@tabler/icons-vue';

const props = defineProps({
  tipo: {
    type: String,
    required: true, // 'antes', 'durante', 'despues'
  },
  codigoOt: {
    type: String,
    default: 'OT-000',
  },
  evidenciasCount: {
    type: Number,
    default: 0,
  },
});

const emit = defineEmits(['photo-uploaded']);

const fileInput = ref(null);
const canvas = ref(null);
const previewUrl = ref(null);
const uploading = ref(false);
const coordsText = ref('Buscando GPS...');
const dateText = ref('');
const currentLat = ref(null);
const currentLng = ref(null);

const tipoBadgeClass = computed(() => {
  if (props.tipo === 'antes') return 'bg-amber-50 text-amber-800 border border-amber-200 dark:bg-amber-950/60 dark:text-amber-300 dark:border-amber-500/30';
  if (props.tipo === 'durante') return 'bg-red-50 text-red-700 border border-red-200 dark:bg-red-950/60 dark:text-red-300 dark:border-red-500/30';
  return 'bg-emerald-50 text-emerald-700 border border-emerald-200 dark:bg-emerald-950/60 dark:text-emerald-300 dark:border-emerald-500/30';
});

const triggerCamera = () => {
  // Obtener geolocalización
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        currentLat.value = pos.coords.latitude;
        currentLng.value = pos.coords.longitude;
        coordsText.value = `${currentLat.value.toFixed(6)}, ${currentLng.value.toFixed(6)}`;
      },
      () => {
        coordsText.value = 'GPS no disponible';
      },
      { enableHighAccuracy: true, timeout: 5000 }
    );
  }
  fileInput.value.click();
};

const handlePhotoCapture = (e) => {
  const file = e.target.files[0];
  if (!file) return;

  uploading.value = true;
  const reader = new FileReader();

  reader.onload = (event) => {
    const img = new Image();
    img.onload = () => {
      drawWatermark(img);
      uploading.value = false;
    };
    img.src = event.target.result;
  };

  reader.readAsDataURL(file);
};

const drawWatermark = (img) => {
  const cvs = canvas.value;
  const ctx = cvs.getContext('2d');

  // Ajustar resolucion
  cvs.width = img.width;
  cvs.height = img.height;

  // Dibujar imagen original
  ctx.drawImage(img, 0, 0);

  // Formatear Fecha y Hora
  const now = new Date();
  const dateStr = now.toLocaleString('es-CO', { timeZoneName: 'short' });
  dateText.value = dateStr;

  // Dibujar franja inferior oscura para legibilidad
  const barHeight = Math.max(60, img.height * 0.1);
  ctx.fillStyle = 'rgba(0, 0, 0, 0.75)';
  ctx.fillRect(0, img.height - barHeight, img.width, barHeight);

  // Estilo de texto de la marca de agua
  const fontSize = Math.max(16, Math.floor(barHeight * 0.28));
  ctx.fillStyle = '#22c55e'; // Verde de verificación
  ctx.font = `bold ${fontSize}px sans-serif`;

  const line1 = `SMU EVIDENCIA: ${props.tipo.toUpperCase()} | OT: ${props.codigoOt}`;
  const line2 = `GPS: ${coordsText.value} | FECHA: ${dateStr}`;

  ctx.fillText(line1, 20, img.height - barHeight + fontSize + 8);
  ctx.fillStyle = '#ffffff';
  ctx.font = `${fontSize * 0.9}px monospace`;
  ctx.fillText(line2, 20, img.height - barHeight + (fontSize * 2) + 12);

  // Convertir canvas a data URL
  previewUrl.value = cvs.toDataURL('image/jpeg', 0.85);
};

const confirmUpload = () => {
  if (!previewUrl.value) return;
  emit('photo-uploaded', {
    tipo: props.tipo,
    imagen_base64: previewUrl.value,
    latitud: currentLat.value,
    longitud: currentLng.value,
  });
  previewUrl.value = null;
};
</script>

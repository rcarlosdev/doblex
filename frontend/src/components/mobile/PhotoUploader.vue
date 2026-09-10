<template>
  <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-4 shadow-sm transition-colors duration-300">
    <!-- Encabezado de Tipo de Evidencia -->
    <div class="flex items-center justify-between flex-wrap gap-2">
      <div class="flex items-center gap-2">
        <span :class="tipoBadgeClass" class="px-2.5 py-0.5 rounded-md text-xs font-black uppercase tracking-wider">
          Evidencia: {{ tipo }}
        </span>
        <span class="text-xs text-slate-500 dark:text-slate-400 font-bold">
          ({{ evidenciasList.length }} montadas)
        </span>
      </div>
      
      <button
        v-if="!readOnly"
        @click="triggerCamera"
        :disabled="uploading"
        class="bg-red-600 hover:bg-red-500 text-white px-3 py-1.5 rounded-xl text-xs font-extrabold flex items-center gap-1.5 shadow-lg shadow-red-600/20 active:scale-95 transition-all"
      >
        <IconCamera class="w-4 h-4 stroke-[2]" />
        <span>{{ uploading ? 'Procesando...' : 'Tomar / Montar Foto' }}</span>
      </button>
    </div>

    <!-- Elemento input tipo file oculto para camara/galería nativa -->
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

    <!-- VISTA PREVIA DE FOTO NUEVA PROCESADA CON MARCA DE AGUA (PENDIENTE DE CONFIRMAR) -->
    <div v-if="previewUrl" class="relative rounded-xl overflow-hidden border-2 border-red-500 shadow-xl group space-y-2">
      <div class="relative">
        <img :src="previewUrl" alt="Vista Previa Evidencia" class="w-full h-56 object-cover" />
        <div class="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black/90 via-black/70 to-transparent p-3 text-[10px] text-slate-200 space-y-0.5">
          <div class="font-mono text-emerald-400 font-bold flex items-center gap-1">
            <IconCheck class="w-3.5 h-3.5 stroke-[3]" />
            <span>Marca de agua incrustada con éxito</span>
          </div>
          <div>GPS: {{ coordsText }}</div>
          <div>Fecha: {{ dateText }}</div>
        </div>
      </div>

      <div class="p-2.5 bg-slate-50 dark:bg-[#0a0b10] flex justify-end gap-2 border-t border-slate-200 dark:border-white/10">
        <button
          @click="previewUrl = null"
          class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-white/10"
        >
          Cancelar
        </button>
        <button
          @click="confirmUpload"
          :disabled="uploading"
          class="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-1.5 rounded-lg text-xs font-black shadow-md flex items-center gap-1.5"
        >
          <IconCheck class="w-4 h-4 stroke-[2.5]" />
          <span>Guardar esta Foto</span>
        </button>
      </div>
    </div>

    <!-- GALERÍA DE IMÁGENES PREVIAMENTE MONTADAS / SUBIDAS EN LA OT -->
    <div v-if="evidenciasList.length > 0" class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
      <div
        v-for="ev in evidenciasList"
        :key="ev.id"
        class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl overflow-hidden shadow-xs flex flex-col justify-between group"
      >
        <div class="relative cursor-pointer" @click="selectedZoomPhoto = ev.url_imagen">
          <img :src="ev.url_imagen" @error="onFotoError($event, ev.tipo)" alt="Evidencia Carga" class="w-full h-40 object-cover hover:opacity-95 transition-opacity" />
          <div class="absolute inset-0 bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
            <span class="bg-black/70 text-white text-[10px] font-bold px-2 py-1 rounded-md flex items-center gap-1">
              <IconEye class="w-3.5 h-3.5" /> Ampliar Foto
            </span>
          </div>
          <div class="absolute top-2 left-2 bg-black/70 text-white text-[9px] font-mono px-2 py-0.5 rounded font-bold uppercase tracking-wider">
            {{ ev.tipo }}
          </div>
        </div>

        <div class="p-2.5 flex items-center justify-between gap-2 border-t border-slate-200/80 dark:border-white/10 text-[10px]">
          <div class="space-y-0.5 truncate text-slate-600 dark:text-slate-400">
            <div class="font-bold text-slate-800 dark:text-slate-200 font-mono">{{ formatDate(ev.fecha_hora_captura || ev.created_at) }}</div>
            <div v-if="ev.latitud" class="truncate font-mono text-[9px]">
              GPS: {{ Number(ev.latitud).toFixed(4) }}, {{ Number(ev.longitud).toFixed(4) }}
            </div>
          </div>

          <button
            v-if="!readOnly"
            @click.stop="$emit('delete-photo', ev.id)"
            class="bg-rose-50 dark:bg-rose-950/60 hover:bg-rose-600 hover:text-white border border-rose-200 dark:border-rose-800 text-rose-600 dark:text-rose-400 p-1.5 rounded-lg text-xs font-bold transition-all shrink-0 flex items-center gap-1"
            title="Eliminar esta foto"
          >
            <IconTrash class="w-3.5 h-3.5 stroke-[2]" />
            <span class="text-[10px] font-extrabold hidden xs:inline">Eliminar</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Mensaje si no hay fotos montadas -->
    <div v-else-if="!previewUrl" class="text-center py-6 bg-slate-50 dark:bg-[#0a0b10] border border-dashed border-slate-200 dark:border-white/10 rounded-xl space-y-1">
      <IconPhotoOff class="w-8 h-8 mx-auto text-slate-400 stroke-[1.5]" />
      <div class="text-xs font-bold text-slate-600 dark:text-slate-400">No hay fotos de {{ tipo.toUpperCase() }} cargadas</div>
      <div class="text-[10px] text-slate-400">Toca el botón "Tomar / Montar Foto" para registrar evidencia fotográfica.</div>
    </div>

    <!-- MODAL LIGHTBOX PARA VER IMAGEN EN TAMAÑO COMPLETO -->
    <Teleport to="body">
      <div v-if="selectedZoomPhoto" class="fixed inset-0 z-[150] bg-black/90 backdrop-blur-md flex items-center justify-center p-4" @click="selectedZoomPhoto = null">
        <div class="relative max-w-4xl max-h-[90vh] overflow-hidden rounded-2xl border border-white/20 shadow-2xl">
          <button @click="selectedZoomPhoto = null" class="absolute top-3 right-3 bg-black/70 hover:bg-black text-white p-2 rounded-full z-10 font-bold">
            <IconX class="w-5 h-5 stroke-[2.5]" />
          </button>
          <img :src="selectedZoomPhoto" alt="Ampliación Foto Evidencia" class="max-w-full max-h-[85vh] object-contain mx-auto rounded-lg" />
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { IconCamera, IconCheck, IconTrash, IconEye, IconPhotoOff, IconX } from '@tabler/icons-vue';

const props = defineProps({
  tipo: {
    type: String,
    required: true, // 'antes', 'durante', 'despues'
  },
  codigoOt: {
    type: String,
    default: 'OT-000',
  },
  evidenciasList: {
    type: Array,
    default: () => [],
  },
  readOnly: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['photo-uploaded', 'delete-photo']);

const fileInput = ref(null);
const canvas = ref(null);
const previewUrl = ref(null);
const uploading = ref(false);
const selectedZoomPhoto = ref(null);
const coordsText = ref('Buscando GPS...');
const dateText = ref('');
const currentLat = ref(null);
const currentLng = ref(null);

const tipoBadgeClass = computed(() => {
  if (props.tipo === 'antes') return 'bg-amber-100 text-amber-900 border border-amber-300 dark:bg-amber-950 dark:text-amber-300 dark:border-amber-700';
  if (props.tipo === 'durante') return 'bg-rose-100 text-rose-900 border border-rose-300 dark:bg-rose-950 dark:text-rose-300 dark:border-rose-700';
  return 'bg-emerald-100 text-emerald-900 border border-emerald-300 dark:bg-emerald-950 dark:text-emerald-300 dark:border-emerald-700';
});

const triggerCamera = () => {
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

  cvs.width = img.width;
  cvs.height = img.height;

  ctx.drawImage(img, 0, 0);

  const now = new Date();
  const dateStr = now.toLocaleString('es-CO', { timeZoneName: 'short' });
  dateText.value = dateStr;

  const barHeight = Math.max(60, img.height * 0.1);
  ctx.fillStyle = 'rgba(0, 0, 0, 0.75)';
  ctx.fillRect(0, img.height - barHeight, img.width, barHeight);

  const fontSize = Math.max(16, Math.floor(barHeight * 0.28));
  ctx.fillStyle = '#22c55e';
  ctx.font = `bold ${fontSize}px sans-serif`;

  const line1 = `SMU EVIDENCIA: ${props.tipo.toUpperCase()} | OT: ${props.codigoOt}`;
  const line2 = `GPS: ${coordsText.value} | FECHA: ${dateStr}`;

  ctx.fillText(line1, 20, img.height - barHeight + fontSize + 8);
  ctx.fillStyle = '#ffffff';
  ctx.font = `${fontSize * 0.9}px monospace`;
  ctx.fillText(line2, 20, img.height - barHeight + (fontSize * 2) + 12);

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

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return d.toLocaleDateString('es-CO', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' });
};

const fallbackEvidencias = {
  antes: 'https://images.unsplash.com/photo-1541888946425-d0fbb186f5f8?w=800',
  durante: 'https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800',
  despues: 'https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800'
};

const onFotoError = (event, tipo) => {
  if (event?.target) {
    event.target.src = fallbackEvidencias[tipo] || fallbackEvidencias.antes;
  }
};
</script>

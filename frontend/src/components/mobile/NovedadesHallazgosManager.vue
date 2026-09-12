<template>
  <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-sm transition-colors duration-300">
    <!-- Header -->
    <div class="flex items-center justify-between flex-wrap gap-2.5 border-b border-slate-100 dark:border-white/10 pb-3">
      <div class="flex items-center gap-2.5">
        <div class="w-8 h-8 rounded-xl bg-amber-50 dark:bg-amber-950/80 border border-amber-200 dark:border-amber-800 flex items-center justify-center text-amber-600 dark:text-amber-400 shrink-0">
          <IconAlertTriangle class="w-4 h-4 stroke-[2]" />
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h3 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
              Novedades & Hallazgos en Estación
            </h3>
            <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-slate-100 dark:bg-white/5 text-slate-600 dark:text-slate-400">
              {{ items.length }} {{ items.length === 1 ? 'reportado' : 'reportados' }}
            </span>
          </div>
          <p class="text-[11px] text-slate-500 dark:text-slate-400 font-medium mt-0.5">
            Registre anomalías o daños detectados en la estación durante la intervención (con fotografía de soporte).
          </p>
        </div>
      </div>

      <button
        v-if="!readOnly"
        type="button"
        @click="agregarHallazgo"
        class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-extrabold bg-amber-50 dark:bg-amber-950/60 text-amber-700 dark:text-amber-300 hover:bg-amber-100 border border-amber-200 dark:border-amber-800 transition-all active:scale-95 shadow-xs"
      >
        <IconPlus class="w-3.5 h-3.5 stroke-[2.5]" />
        <span>Agregar Hallazgo</span>
      </button>
    </div>

    <!-- Estado vacío -->
    <div v-if="items.length === 0" class="text-center py-6 px-4 bg-slate-50 dark:bg-[#0a0b10] border border-dashed border-slate-200 dark:border-white/10 rounded-xl space-y-2">
      <IconShieldCheck class="w-8 h-8 mx-auto text-emerald-500 stroke-[1.5]" />
      <div class="text-xs font-bold text-slate-800 dark:text-slate-200">
        Sin novedades críticas ni anomalías pendientes
      </div>
      <p class="text-[11px] text-slate-500 dark:text-slate-400 max-w-sm mx-auto">
        Si detecta deterioro en la caseta, planta, cerramiento, aires o energía, agréguelo como hallazgo fotográfico.
      </p>
      <button
        v-if="!readOnly"
        type="button"
        @click="agregarHallazgo"
        class="mt-2 inline-flex items-center gap-1.5 px-3 py-1.5 bg-amber-500 hover:bg-amber-600 text-white rounded-xl text-xs font-bold shadow-sm"
      >
        <IconPlus class="w-3.5 h-3.5 stroke-[2.5]" />
        <span>Reportar Hallazgo / Novedad</span>
      </button>
    </div>

    <!-- Lista de hallazgos -->
    <div v-else class="space-y-4">
      <div
        v-for="(h, index) in items"
        :key="index"
        class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200/90 dark:border-white/10 rounded-xl p-3.5 space-y-3 relative group"
      >
        <div class="flex items-center justify-between border-b border-slate-200/60 dark:border-white/5 pb-2">
          <div class="flex items-center gap-2">
            <span class="w-5 h-5 rounded-full bg-amber-200 dark:bg-amber-900/60 text-amber-800 dark:text-amber-200 text-[10px] flex items-center justify-center font-bold">
              {{ index + 1 }}
            </span>
            <span class="text-xs font-extrabold text-slate-800 dark:text-slate-200">
              Hallazgo #{{ index + 1 }}
            </span>
          </div>

          <button
            v-if="!readOnly"
            type="button"
            @click="eliminarHallazgo(index)"
            class="text-rose-500 hover:text-rose-700 dark:hover:text-rose-400 p-1 rounded-lg hover:bg-rose-50 dark:hover:bg-rose-950/50 transition-colors"
            title="Eliminar hallazgo"
          >
            <IconTrash class="w-4 h-4" />
          </button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <!-- Subsistema -->
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
              Sistema Afectado *
            </label>
            <select
              v-model="h.sistema"
              :disabled="readOnly"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 py-1 text-xs font-medium text-slate-800 dark:text-slate-200 focus:border-amber-500 focus:outline-none"
            >
              <option value="Grupo Electrógeno / Planta">Grupo Electrógeno / Planta</option>
              <option value="Climatización / Aires">Climatización / Aires</option>
              <option value="Transferencia / ATS">Transferencia / ATS</option>
              <option value="Sistema de Energía DC / Rectificador">Sistema de Energía DC / Rectificador</option>
              <option value="Infraestructura / Torre / Anclajes">Infraestructura / Torre / Anclajes</option>
              <option value="Cerramiento / Caseta / Seguridad">Cerramiento / Caseta / Seguridad</option>
              <option value="Puesta a Tierra (SPT)">Puesta a Tierra (SPT)</option>
              <option value="Otro">Otro</option>
            </select>
          </div>

          <!-- Prioridad -->
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
              Prioridad *
            </label>
            <select
              v-model="h.prioridad"
              :disabled="readOnly"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 py-1 text-xs font-medium text-slate-800 dark:text-slate-200 focus:border-amber-500 focus:outline-none"
            >
              <option value="Alta">Alta (Riesgo Inmediato)</option>
              <option value="Media">Media (Atención Próxima)</option>
              <option value="Baja">Baja (Mantenimiento Rutinario)</option>
            </select>
          </div>

          <!-- Resuelto en Visita -->
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
              ¿Resuelto en la Visita? *
            </label>
            <select
              v-model="h.resuelto_en_visita"
              :disabled="readOnly"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 py-1 text-xs font-medium text-slate-800 dark:text-slate-200 focus:border-amber-500 focus:outline-none"
            >
              <option value="Si">Sí, corregido en sitio</option>
              <option value="No">No, requiere acción posterior</option>
            </select>
          </div>
        </div>

        <!-- Descripción -->
        <div class="space-y-1">
          <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
            Descripción Detallada del Hallazgo *
          </label>
          <textarea
            v-model="h.descripcion"
            :disabled="readOnly"
            rows="2"
            placeholder="Describa claramente la novedad evidenciada, causa posible o impacto..."
            class="w-full rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 p-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-amber-500 focus:outline-none leading-relaxed"
          ></textarea>
        </div>

        <!-- Foto del hallazgo -->
        <div class="pt-1">
          <SinglePhotoCapture
            v-model="h.foto"
            :label="`Foto Soporte del Hallazgo *`"
            :tag="`HALLAZGO - ${(h.sistema || 'GENERAL').toUpperCase()}`"
            :codigo-ot="codigoOt"
            :disabled="readOnly"
            placeholder="Tomar foto de la anomalía o daño evidenciado"
            :required="true"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { IconAlertTriangle, IconPlus, IconTrash, IconShieldCheck } from '@tabler/icons-vue';
import SinglePhotoCapture from './SinglePhotoCapture.vue';

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  codigoOt: {
    type: String,
    default: ''
  },
  readOnly: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue']);

const items = computed({
  get: () => props.modelValue || [],
  set: (val) => emit('update:modelValue', val)
});

const agregarHallazgo = () => {
  const current = [...items.value];
  current.push({
    sistema: 'Infraestructura / Torre / Anclajes',
    prioridad: 'Media',
    resuelto_en_visita: 'No',
    descripcion: '',
    foto: ''
  });
  emit('update:modelValue', current);
};

const eliminarHallazgo = (idx) => {
  const current = [...items.value];
  current.splice(idx, 1);
  emit('update:modelValue', current);
};
</script>

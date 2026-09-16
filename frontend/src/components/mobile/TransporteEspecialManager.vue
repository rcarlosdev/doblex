<template>
  <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-sm transition-colors duration-300">
    <!-- Header -->
    <div class="flex items-center justify-between flex-wrap gap-2.5 border-b border-slate-100 dark:border-white/10 pb-3">
      <div class="flex items-center gap-2.5">
        <div class="w-8 h-8 rounded-xl bg-purple-50 dark:bg-purple-950/80 border border-purple-200 dark:border-purple-800 flex items-center justify-center text-purple-600 dark:text-purple-400 shrink-0">
          <IconTruck class="w-4 h-4 stroke-[2]" />
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h3 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
              Transporte Especial (LPU)
            </h3>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded-md bg-rose-100 text-rose-700 dark:bg-rose-950/60 dark:text-rose-300 border border-rose-200 dark:border-rose-800">
              OBLIGATORIO
            </span>
          </div>
          <p class="text-[11px] text-slate-500 dark:text-slate-400 font-medium mt-0.5">
            Registre la movilización fluvial, bestia, 4x4 o aéreo utilizada para acceder al sitio (con foto soporte).
          </p>
        </div>
      </div>

      <button
        v-if="!readOnly"
        type="button"
        @click="agregarTransporte"
        class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-extrabold bg-purple-50 dark:bg-purple-950/60 text-purple-700 dark:text-purple-300 hover:bg-purple-100 border border-purple-200 dark:border-purple-800 transition-all active:scale-95 shadow-xs"
      >
        <IconPlus class="w-3.5 h-3.5 stroke-[2.5]" />
        <span>Agregar Tramo</span>
      </button>
    </div>

    <!-- Lista de Transportes Registrados -->
    <div v-if="items.length === 0" class="text-center py-6 px-4 bg-purple-50/40 dark:bg-purple-950/20 border border-dashed border-purple-200 dark:border-purple-900/40 rounded-xl space-y-2">
      <IconTruck class="w-8 h-8 mx-auto text-purple-400 stroke-[1.5]" />
      <div class="text-xs font-bold text-slate-800 dark:text-slate-200">
        No se ha registrado transporte especial
      </div>
      <p class="text-[11px] text-slate-500 dark:text-slate-400 max-w-sm mx-auto">
        El registro de transporte especial y su fotografía son obligatorios para el cierre técnico de la orden.
      </p>
      <button
        v-if="!readOnly"
        type="button"
        @click="agregarTransporte"
        class="mt-2 inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-purple-600 hover:bg-purple-500 text-white rounded-xl text-xs font-bold shadow-sm"
      >
        <IconPlus class="w-3.5 h-3.5 stroke-[2.5]" />
        <span>Registrar Transporte Especial</span>
      </button>
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="(t, index) in items"
        :key="index"
        class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200/90 dark:border-white/10 rounded-xl p-3.5 space-y-3 relative group"
      >
        <!-- Título del tramo y botón eliminar -->
        <div class="flex items-center justify-between border-b border-slate-200/60 dark:border-white/5 pb-2">
          <span class="text-xs font-extrabold text-purple-700 dark:text-purple-300 flex items-center gap-1.5">
            <span class="w-5 h-5 rounded-full bg-purple-200 dark:bg-purple-900/60 text-purple-800 dark:text-purple-200 text-[10px] flex items-center justify-center font-bold">
              {{ index + 1 }}
            </span>
            <span>Tramo de Transporte</span>
          </span>

          <button
            v-if="!readOnly"
            type="button"
            @click="eliminarTransporte(index)"
            class="text-rose-500 hover:text-rose-700 dark:hover:text-rose-400 p-1 rounded-lg hover:bg-rose-50 dark:hover:bg-rose-950/50 transition-colors"
            title="Eliminar tramo"
          >
            <IconTrash class="w-4 h-4" />
          </button>
        </div>

        <!-- Grid de campos -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <!-- Tipo de Transporte -->
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
              Tipo de Transporte *
            </label>
            <select
              v-model="t.tipo"
              :disabled="readOnly"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 py-1 text-xs font-medium text-slate-800 dark:text-slate-200 focus:border-purple-500 focus:outline-none"
            >
              <option value="Lancha / Fluvial">Lancha / Fluvial</option>
              <option value="Mula / Bestia">Mula / Bestia de Carga</option>
              <option value="Vehículo 4x4 / Trocha">Vehículo 4x4 / Trocha</option>
              <option value="Aéreo / Avioneta">Aéreo / Avioneta</option>
              <option value="Cotero / Porteador">Cotero / Porteador a Hombro</option>
              <option value="Terrestre Convencional">Terrestre Convencional / Mixto</option>
            </select>
          </div>

          <!-- Distancia en KM -->
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
              Distancia (KM) *
            </label>
            <input
              type="number"
              v-model.number="t.distancia_km"
              :disabled="readOnly"
              placeholder="Ej. 45"
              min="0"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 py-1 text-xs font-medium text-slate-800 dark:text-slate-200 focus:border-purple-500 focus:outline-none"
            />
          </div>

          <!-- Tiempo de Desplazamiento -->
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
              Tiempo Desplazamiento *
            </label>
            <input
              type="text"
              v-model="t.tiempo_desplazamiento"
              :disabled="readOnly"
              placeholder="Ej. 1 hora 30 min"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 py-1 text-xs font-medium text-slate-800 dark:text-slate-200 focus:border-purple-500 focus:outline-none"
            />
          </div>
        </div>

        <!-- Observación -->
        <div class="space-y-1">
          <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
            Observación / Ruta / Placa / Embarcación
          </label>
          <input
            type="text"
            v-model="t.observacion"
            :disabled="readOnly"
            placeholder="Ej. Traslado fluvial desde muelle municipal hasta sitio de acceso..."
            class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 py-1 text-xs text-slate-800 dark:text-slate-200 focus:border-purple-500 focus:outline-none"
          />
        </div>

        <!-- Foto soporte OBLIGATORIA -->
        <div class="pt-1">
          <SinglePhotoCapture
            v-model="t.foto"
            :label="`Foto Soporte del Transporte (Obligatoria) *`"
            :tag="`TRANSPORTE - ${t.tipo || 'ESPECIAL'}`"
            :codigo-ot="codigoOt"
            :disabled="readOnly"
            placeholder="Tomar foto del transporte (lancha, vehículo, mula, ticket)"
            :required="true"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { IconTruck, IconPlus, IconTrash } from '@tabler/icons-vue';
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

const agregarTransporte = () => {
  const current = [...items.value];
  current.push({
    tipo: 'Vehículo 4x4 / Trocha',
    distancia_km: null,
    tiempo_desplazamiento: '',
    observacion: '',
    foto: ''
  });
  emit('update:modelValue', current);
};

const eliminarTransporte = (idx) => {
  const current = [...items.value];
  current.splice(idx, 1);
  emit('update:modelValue', current);
};
</script>

<template>
  <Teleport to="body">
    <div v-if="isOpen" class="fixed inset-0 z-50 bg-black/60 dark:bg-black/80 backdrop-blur-sm flex items-end sm:items-center justify-center p-4">
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl w-full max-w-lg overflow-hidden shadow-2xl space-y-4 p-5 max-h-[90vh] overflow-y-auto transition-colors duration-300">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
          <h3 class="text-lg font-extrabold text-slate-900 dark:text-white flex items-center gap-2">
            <IconCircleCheck class="w-5 h-5 text-emerald-600 dark:text-emerald-400 stroke-[2]" />
            Cierre y Solución Técnica de OT
          </h3>
          <button @click="$emit('close')" class="text-slate-400 hover:text-slate-700 dark:hover:text-white p-1 font-bold">
            <IconX class="w-4 h-4 stroke-[2]" />
          </button>
        </div>

        <!-- Clasificación de causa de falla -->
        <div class="space-y-1.5">
          <label class="text-xs font-semibold text-slate-700 dark:text-slate-300">Causa Raíz de la Falla <span class="text-rose-500">*</span></label>
          <select
            v-model="causaFalla"
            class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-900 dark:text-white focus:ring-2 focus:ring-red-500 focus:outline-none"
          >
            <option value="desgaste">Desgaste Natural / Vida Útil</option>
            <option value="vandalismo">Vandalismo / Hurto</option>
            <option value="factor_climatico">Factor Climático / Sobretensión</option>
            <option value="desconocido">Otro / Desconocido</option>
          </select>
        </div>

        <!-- Repuestos o insumos utilizados LPU -->
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <label class="text-xs font-semibold text-slate-700 dark:text-slate-300">Insumos & Repuestos Consumidos (LPU 2026)</label>
            <button
              @click="addRepuesto"
              class="text-xs text-red-600 dark:text-red-400 hover:underline font-semibold flex items-center gap-1"
            >
              <IconPlus class="w-3.5 h-3.5 stroke-[2.5]" />
              <span>Agregar Item</span>
            </button>
          </div>

          <div v-for="(item, idx) in repuestos" :key="idx" class="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800/80 p-2.5 rounded-xl">
            <div class="flex items-center gap-2">
              <input
                v-model="item.nombre_item"
                list="lpu-catalog"
                placeholder="Buscar catálogo LPU o escribir repuesto..."
                class="flex-1 min-w-0 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 focus:ring-2 focus:ring-red-500 focus:outline-none"
              />
              <input
                v-model.number="item.cantidad"
                type="number"
                min="1"
                placeholder="Cant."
                class="w-16 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg px-2 py-2 text-xs text-slate-900 dark:text-white text-center font-mono focus:ring-2 focus:ring-red-500 focus:outline-none shrink-0"
              />
              <button @click="removeRepuesto(idx)" class="text-rose-500 hover:text-rose-700 p-1 font-bold text-xs shrink-0" title="Eliminar item">
                <IconX class="w-4 h-4 stroke-[2]" />
              </button>
            </div>
          </div>

          <datalist id="lpu-catalog">
            <option v-for="cat in catalogoLpu" :key="cat" :value="cat"></option>
          </datalist>
        </div>

        <!-- Mensaje de error de validación / backend -->
        <div v-if="errorMsg || localError" class="bg-rose-50 dark:bg-rose-950/80 border border-rose-200 dark:border-rose-800 text-rose-700 dark:text-rose-300 p-3 rounded-xl text-xs flex items-start gap-2">
          <IconAlertCircle class="w-4 h-4 shrink-0 mt-0.5 stroke-[2]" />
          <div class="leading-relaxed font-medium">{{ errorMsg || localError }}</div>
        </div>

        <!-- Observaciones de Cierre -->
        <div class="space-y-1.5">
          <label class="text-xs font-semibold text-slate-700 dark:text-slate-300">Observaciones Finales de Intervención <span class="text-rose-500">*</span></label>
          <textarea
            v-model="observaciones"
            rows="3"
            placeholder="Describa el trabajo final realizado, medidas tomadas y recomendaciones para entrega..."
            class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg p-3 text-xs text-slate-900 dark:text-white focus:ring-2 focus:ring-red-500 focus:outline-none"
          ></textarea>
        </div>

        <!-- Botones de Acción -->
        <div class="flex items-center justify-end gap-3 pt-2">
          <button
            @click="$emit('close')"
            class="px-4 py-2 rounded-lg text-xs font-medium text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white"
          >
            Cancelar
          </button>
          <button
            @click="submitClose"
            :disabled="loading"
            class="bg-emerald-600 hover:bg-emerald-500 text-white px-5 py-2.5 rounded-xl text-xs font-extrabold shadow-lg flex items-center gap-2 active:scale-98 transition-all"
          >
            <IconCircleCheck class="w-4 h-4 stroke-[2]" />
            <span>{{ loading ? 'Finalizando...' : 'Confirmar y Solucionar OT' }}</span>
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue';
import { IconCircleCheck, IconPlus, IconX, IconAlertCircle } from '@tabler/icons-vue';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  errorMsg: {
    type: String,
    default: '',
  },
});

const emit = defineEmits(['close', 'submit']);

const causaFalla = ref('desgaste');
const observaciones = ref('');
const localError = ref('');
const repuestos = ref([
  { nombre_item: '', cantidad: 1, unidad_medida: 'unidad' }
]);

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    localError.value = '';
  }
});

const catalogoLpu = [
  'Batería 12V / 100Ah VRLA AGM (ME PW)',
  'Módulo Rectificador 48V / 50A (ME PW)',
  'Filtro de Aire Acondicionado / Climatización (ME/MC AA)',
  'Gas Refrigerante R410A / R22 (kg) (ME/MC AA)',
  'Compresor Aire Acondicionado 24K BTU (ME/MC AA)',
  'Filtro de Aceite / Combustible Planta GE (ME GE/ATS)',
  'Aceite Sintético para Motor GE Galón (ME GE/ATS)',
  'Interruptor Termomagnético Breaker 2x30A (ME MT-SE)',
  'Cable de Cobre Desnudo 2/0 AWG metro (Puesta a Tierra)',
  'Kit Anclajes y Pernería Alta Resistencia (ME ALTURA)',
  'Abrazadera Acero Inoxidable 2" - 4" (ME ALTURA)'
];

const addRepuesto = () => {
  repuestos.value.push({ nombre_item: '', cantidad: 1, unidad_medida: 'unidad' });
};

const removeRepuesto = (index) => {
  repuestos.value.splice(index, 1);
};

const submitClose = () => {
  localError.value = '';
  if (!observaciones.value || observaciones.value.trim().length < 5) {
    localError.value = 'Por favor ingrese las observaciones finales de la intervención (mínimo 5 caracteres).';
    return;
  }

  const filteredRepuestos = repuestos.value.filter(r => r.nombre_item.trim() !== '');
  emit('submit', {
    causa_falla: causaFalla.value,
    observaciones_cierre: observaciones.value,
    repuestos: filteredRepuestos,
  });
};
</script>


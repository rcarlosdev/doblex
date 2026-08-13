<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-end sm:items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg overflow-hidden shadow-2xl space-y-4 p-5 max-h-[90vh] overflow-y-auto">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <h3 class="text-lg font-bold text-white flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Cierre y Solución de OT
        </h3>
        <button @click="$emit('close')" class="text-slate-400 hover:text-white p-1">✕</button>
      </div>

      <!-- Clasificación de causa de falla -->
      <div class="space-y-1.5">
        <label class="text-xs font-semibold text-slate-300">Causa Raíz de la Falla <span class="text-rose-400">*</span></label>
        <select
          v-model="causaFalla"
          class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:ring-2 focus:ring-blue-500 focus:outline-none"
        >
          <option value="desgaste">Desgaste Natural / Vida Útil</option>
          <option value="vandalismo">Vandalismo / Hurto</option>
          <option value="factor_climatico">Factor Climático / Sobretensión</option>
          <option value="desconocido">Otro / Desconocido</option>
        </select>
      </div>

      <!-- Repuestos o insumos utilizados -->
      <div class="space-y-2">
        <div class="flex items-center justify-between">
          <label class="text-xs font-semibold text-slate-300">Repuestos e Insumos Consumidos</label>
          <button
            @click="addRepuesto"
            class="text-xs text-blue-400 hover:text-blue-300 font-semibold flex items-center gap-1"
          >
            + Agregar Item
          </button>
        </div>

        <div v-for="(item, idx) in repuestos" :key="idx" class="flex gap-2 items-center">
          <input
            v-model="item.nombre_item"
            placeholder="Ej. Filtro de aire"
            class="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-white"
          />
          <input
            v-model.number="item.cantidad"
            type="number"
            placeholder="Cant."
            class="w-20 bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-white"
          />
          <button @click="removeRepuesto(idx)" class="text-rose-400 hover:text-rose-300 text-xs px-2">✕</button>
        </div>
      </div>

      <!-- Observaciones de Cierre -->
      <div class="space-y-1.5">
        <label class="text-xs font-semibold text-slate-300">Observaciones Finales de Intervención</label>
        <textarea
          v-model="observaciones"
          rows="3"
          placeholder="Describa el trabajo final realizado y recomendaciones..."
          class="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-white focus:ring-2 focus:ring-blue-500 focus:outline-none"
        ></textarea>
      </div>

      <!-- Botones de Acción -->
      <div class="flex items-center justify-end gap-3 pt-2">
        <button
          @click="$emit('close')"
          class="px-4 py-2 rounded-lg text-xs font-medium text-slate-400 hover:text-white"
        >
          Cancelar
        </button>
        <button
          @click="submitClose"
          :disabled="loading"
          class="bg-emerald-600 hover:bg-emerald-500 text-white px-5 py-2 rounded-lg text-xs font-bold shadow-lg flex items-center gap-2"
        >
          <span>{{ loading ? 'Finalizando...' : 'Confirmar y Cerrar OT' }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['close', 'submit']);

const causaFalla = ref('desgaste');
const observaciones = ref('');
const repuestos = ref([
  { nombre_item: '', cantidad: 1, unidad_medida: 'unidad' }
]);

const addRepuesto = () => {
  repuestos.value.push({ nombre_item: '', cantidad: 1, unidad_medida: 'unidad' });
};

const removeRepuesto = (index) => {
  repuestos.value.splice(index, 1);
};

const submitClose = () => {
  const filteredRepuestos = repuestos.value.filter(r => r.nombre_item.trim() !== '');
  emit('submit', {
    causa_falla: causaFalla.value,
    observaciones_cierre: observaciones.value,
    repuestos: filteredRepuestos,
  });
};
</script>

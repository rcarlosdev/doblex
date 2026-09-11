<template>
  <Teleport to="body">
    <div v-if="isOpen" class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-2.5 sm:p-4 overflow-y-auto">
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl w-full max-w-lg overflow-hidden shadow-2xl p-3.5 sm:p-6 max-h-[94vh] flex flex-col my-auto transition-colors duration-300">
        
        <!-- Header del Modal (Fijo) -->
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-3 shrink-0">
          <div class="flex items-center gap-2.5 min-w-0 pr-2">
            <div class="w-8 h-8 rounded-xl bg-emerald-50 dark:bg-emerald-950/80 border border-emerald-200 dark:border-emerald-800 flex items-center justify-center text-emerald-600 dark:text-emerald-400 shrink-0">
              <IconCircleCheck class="w-5 h-5 stroke-[2.2]" />
            </div>
            <div class="min-w-0">
              <h3 class="text-sm sm:text-base font-extrabold text-slate-900 dark:text-white leading-tight truncate">
                Cierre y Solución Técnica de OT
              </h3>
              <p class="text-[10px] sm:text-[11px] text-slate-500 dark:text-slate-400 font-medium truncate">
                Finalización técnica del servicio en campo
              </p>
            </div>
          </div>
          <button 
            @click="$emit('close')" 
            class="text-slate-400 hover:text-slate-700 dark:hover:text-white p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-white/5 transition-colors cursor-pointer shrink-0"
            title="Cerrar ventana"
          >
            <IconX class="w-5 h-5 stroke-[2]" />
          </button>
        </div>

        <!-- Cuerpo del Modal con scroll estilizado -->
        <div class="space-y-4 overflow-y-auto pr-1 sm:pr-1.5 py-3 flex-1 custom-scrollbar">
          <!-- 1. Clasificación de causa de falla -->
          <div class="space-y-1.5">
            <label class="text-xs font-bold text-slate-800 dark:text-slate-200 flex items-center gap-1.5">
              <span>Causa Raíz de la Falla</span>
              <span class="text-rose-500 font-black">*</span>
            </label>
            <select
              v-model="causaFalla"
              class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl px-3 py-2.5 text-xs text-slate-900 dark:text-white font-medium focus:ring-2 focus:ring-red-500 focus:outline-none transition-all cursor-pointer"
            >
              <option value="desgaste">Desgaste Natural / Cumplimiento de Vida Útil</option>
              <option value="vandalismo">Vandalismo / Hurto / Daño por Terceros</option>
              <option value="factor_climatico">Factor Climático / Descarga Atmosférica / Sobretensión</option>
              <option value="desconocido">Otro Motivo / No Identificado</option>
            </select>
          </div>

          <!-- 2. Repuestos o insumos utilizados LPU con componente reutilizable InsumosMultiSelect -->
          <div class="space-y-2 pt-1 border-t border-slate-100 dark:border-white/10">
            <InsumosMultiSelect
              v-model="repuestos"
              label="Insumos & Repuestos LPU Consumidos"
              placeholder="Buscar repuesto consumido o escribir nuevo..."
              :show-sugerencias="true"
            />
          </div>

          <!-- Mensaje de error de validación / backend -->
          <div v-if="errorMsg || localError" class="bg-rose-50 dark:bg-rose-950/80 border border-rose-200 dark:border-rose-800 text-rose-700 dark:text-rose-300 p-3 rounded-xl text-xs flex items-start gap-2">
            <IconAlertCircle class="w-4 h-4 shrink-0 mt-0.5 stroke-[2]" />
            <div class="leading-relaxed font-medium">{{ errorMsg || localError }}</div>
          </div>

          <!-- 3. Observaciones de Cierre -->
          <div class="space-y-1.5 pt-1 border-t border-slate-100 dark:border-white/10">
            <div class="flex items-center justify-between">
              <label class="text-xs font-bold text-slate-800 dark:text-slate-200 flex items-center gap-1.5">
                <span>Observaciones Finales de Intervención</span>
                <span class="text-rose-500 font-black">*</span>
              </label>
              <span 
                class="text-[10px] font-mono font-bold"
                :class="observaciones.trim().length >= 5 ? 'text-emerald-600 dark:text-emerald-400' : 'text-slate-400 dark:text-slate-500'"
              >
                {{ observaciones.trim().length }}/5 caracteres mín.
              </span>
            </div>

            <textarea
              v-model="observaciones"
              rows="3"
              placeholder="Describa el trabajo final realizado, medidas tomadas y recomendaciones para entrega..."
              class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 text-xs text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 focus:ring-2 focus:ring-red-500 focus:outline-none transition-all font-medium"
            ></textarea>
          </div>
        </div>

        <!-- Botones de Acción (Fijos al pie) -->
        <div class="flex items-center justify-end gap-2.5 pt-3 border-t border-slate-100 dark:border-white/10 shrink-0">
          <button
            type="button"
            @click="$emit('close')"
            class="px-3.5 py-2 sm:px-4 sm:py-2.5 rounded-xl text-xs font-bold text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-white/5 transition-colors cursor-pointer"
          >
            Cancelar
          </button>
          <button
            type="button"
            @click="submitClose"
            :disabled="loading"
            class="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 sm:px-5 sm:py-2.5 rounded-xl text-xs font-extrabold shadow-lg shadow-emerald-600/20 flex items-center gap-2 active:scale-98 transition-all disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            <IconCircleCheck class="w-4 h-4 stroke-[2.2]" />
            <span>{{ loading ? 'Finalizando...' : 'Confirmar y Solucionar OT' }}</span>
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue';
import { 
  IconCircleCheck, 
  IconX, 
  IconAlertCircle 
} from '@tabler/icons-vue';
import InsumosMultiSelect from '@/components/common/InsumosMultiSelect.vue';

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
  initialRepuestos: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(['close', 'submit']);

const causaFalla = ref('desgaste');
const observaciones = ref('');
const localError = ref('');
const repuestos = ref([]);

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    localError.value = '';
    if (props.initialRepuestos && props.initialRepuestos.length > 0) {
      repuestos.value = props.initialRepuestos.map(r => ({
        nombre_item: r.nombre_item,
        cantidad: Number(r.cantidad) || 1,
        unidad_medida: r.unidad_medida || 'unidad',
      }));
    } else {
      repuestos.value = [];
    }
  }
});

const submitClose = () => {
  localError.value = '';
  if (!observaciones.value || observaciones.value.trim().length < 5) {
    localError.value = 'Por favor ingrese las observaciones finales de la intervención (mínimo 5 caracteres).';
    return;
  }

  const filteredRepuestos = repuestos.value.filter(r => r.nombre_item && r.nombre_item.trim() !== '');
  emit('submit', {
    causa_falla: causaFalla.value,
    observaciones_cierre: observaciones.value,
    repuestos: filteredRepuestos,
  });
};
</script>

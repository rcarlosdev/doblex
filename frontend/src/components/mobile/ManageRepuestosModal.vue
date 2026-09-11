<template>
  <Teleport to="body">
    <div v-if="isOpen" class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-2.5 sm:p-4 overflow-y-auto">
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl w-full max-w-lg overflow-hidden shadow-2xl p-3.5 sm:p-6 max-h-[94vh] flex flex-col my-auto transition-colors duration-300">
        
        <!-- Header del Modal (Fijo) -->
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-3 shrink-0">
          <div class="flex items-center gap-2.5 min-w-0 pr-2">
            <div class="w-8 h-8 rounded-xl bg-red-50 dark:bg-red-950/80 border border-red-200 dark:border-red-800 flex items-center justify-center text-red-600 dark:text-red-400 shrink-0">
              <IconBox class="w-4 h-4 stroke-[2]" />
            </div>
            <div class="min-w-0">
              <h3 class="text-sm sm:text-base font-extrabold text-slate-900 dark:text-white leading-tight truncate">
                Gestionar Insumos & Repuestos LPU
              </h3>
              <p class="text-[10px] sm:text-[11px] text-slate-500 dark:text-slate-400 font-medium truncate">
                Vincule o modifique los materiales utilizados en esta orden
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

        <!-- Cuerpo con scroll interno estilizado -->
        <div class="space-y-4 overflow-y-auto pr-1 sm:pr-1.5 py-3 flex-1 custom-scrollbar">
          <!-- Componente Reutilizable InsumosMultiSelect -->
          <InsumosMultiSelect
            v-model="items"
            label="Insumos y Repuestos Registrados"
            placeholder="Buscar en catálogo LPU o escribir nuevo..."
            :show-sugerencias="true"
          />

          <!-- Mensaje de error local -->
          <div v-if="localError" class="bg-rose-50 dark:bg-rose-950/80 border border-rose-200 dark:border-rose-800 text-rose-700 dark:text-rose-300 p-3 rounded-xl text-xs flex items-start gap-2">
            <IconAlertCircle class="w-4 h-4 shrink-0 mt-0.5 stroke-[2]" />
            <div class="leading-relaxed font-medium">{{ localError }}</div>
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
            @click="handleSave"
            :disabled="saving"
            class="bg-red-600 hover:bg-red-500 text-white px-4 py-2 sm:px-5 sm:py-2.5 rounded-xl text-xs font-extrabold shadow-lg shadow-red-600/20 flex items-center gap-2 active:scale-98 transition-all disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            <IconCheck class="w-4 h-4 stroke-[2.2]" />
            <span>{{ saving ? 'Guardando...' : 'Guardar Insumos' }}</span>
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue';
import { 
  IconBox, 
  IconX, 
  IconCheck, 
  IconAlertCircle 
} from '@tabler/icons-vue';
import InsumosMultiSelect from '@/components/common/InsumosMultiSelect.vue';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
  saving: {
    type: Boolean,
    default: false,
  },
  initialRepuestos: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(['close', 'save']);

const items = ref([]);
const localError = ref('');

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    localError.value = '';
    // Clonar lista existente para edición sin mutar reactivamente hasta guardar
    items.value = (props.initialRepuestos || []).map(r => ({
      nombre_item: r.nombre_item,
      cantidad: Number(r.cantidad) || 1,
      unidad_medida: r.unidad_medida || 'unidad',
    }));
  }
});

const handleSave = () => {
  localError.value = '';

  // Validar si algún repuesto tiene nombre vacío
  const invalid = items.value.find(r => !r.nombre_item || !r.nombre_item.trim());
  if (invalid) {
    localError.value = 'Todos los repuestos agregados deben tener un nombre o descripción válida.';
    return;
  }

  // Filtrar y sanitizar lista final
  const cleanList = items.value.map(r => ({
    nombre_item: r.nombre_item.trim(),
    cantidad: Number(r.cantidad) > 0 ? Number(r.cantidad) : 1,
    unidad_medida: r.unidad_medida || 'unidad',
  }));

  emit('save', cleanList);
};
</script>

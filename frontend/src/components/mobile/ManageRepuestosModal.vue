<template>
  <Teleport to="body">
    <div v-if="isOpen" class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-3 sm:p-4 overflow-y-auto">
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl w-full max-w-lg overflow-hidden shadow-2xl space-y-4 p-4 sm:p-6 max-h-[92vh] overflow-y-auto my-auto transition-colors duration-300">
        
        <!-- Header del Modal -->
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-3">
          <div class="flex items-center gap-2.5">
            <div class="w-8 h-8 rounded-xl bg-red-50 dark:bg-red-950/80 border border-red-200 dark:border-red-800 flex items-center justify-center text-red-600 dark:text-red-400">
              <IconBox class="w-5 h-5 stroke-[2]" />
            </div>
            <div>
              <h3 class="text-base font-extrabold text-slate-900 dark:text-white leading-tight">
                Gestionar Insumos & Repuestos LPU
              </h3>
              <p class="text-[11px] text-slate-500 dark:text-slate-400 font-medium">
                Vincule o modifique los materiales utilizados en esta orden
              </p>
            </div>
          </div>
          <button 
            @click="$emit('close')" 
            class="text-slate-400 hover:text-slate-700 dark:hover:text-white p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-white/5 transition-colors"
            title="Cerrar ventana"
          >
            <IconX class="w-5 h-5 stroke-[2]" />
          </button>
        </div>

        <!-- Sugerencias rápidas (Chips) para agregar en 1 clic -->
        <div class="space-y-1.5">
          <div class="text-[10px] font-semibold text-slate-500 dark:text-slate-400">
            Sugerencias frecuentes del catálogo LPU:
          </div>
          <div class="flex flex-wrap gap-1.5">
            <button
              v-for="sug in sugerenciasRapidas"
              :key="sug.nombre"
              type="button"
              @click="addSugItem(sug)"
              class="text-[10px] font-medium bg-slate-100 dark:bg-white/5 hover:bg-red-50 dark:hover:bg-red-950/40 text-slate-700 dark:text-slate-300 hover:text-red-600 dark:hover:text-red-400 border border-slate-200 dark:border-white/10 rounded-lg px-2.5 py-1 transition-all flex items-center gap-1 active:scale-95"
              :title="`Agregar ${sug.nombre}`"
            >
              <IconPlus class="w-3 h-3 text-red-500 stroke-[2.5]" />
              <span>{{ sug.short }}</span>
            </button>
          </div>
        </div>

        <!-- Estado Vacío (si no hay repuestos agregados) -->
        <div 
          v-if="items.length === 0" 
          class="bg-slate-50 dark:bg-[#0a0b10] border border-dashed border-slate-200 dark:border-white/10 rounded-2xl p-6 text-center space-y-2 select-none"
        >
          <div class="w-10 h-10 rounded-full bg-slate-100 dark:bg-white/5 flex items-center justify-center mx-auto text-slate-400 dark:text-slate-500">
            <IconPackageOff class="w-5 h-5 stroke-[1.5]" />
          </div>
          <p class="text-xs font-semibold text-slate-700 dark:text-slate-300">
            No hay repuestos registrados en la lista
          </p>
          <p class="text-[11px] text-slate-400 dark:text-slate-500 max-w-xs mx-auto">
            Puedes agregar ítems usando las sugerencias superiores o haciendo clic abajo.
          </p>
          <button
            type="button"
            @click="addItem"
            class="mt-2 inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-extrabold bg-red-600 hover:bg-red-500 text-white shadow-md shadow-red-600/20 active:scale-95 transition-all"
          >
            <IconPlus class="w-4 h-4 stroke-[2.5]" />
            <span>Agregar Primer Repuesto</span>
          </button>
        </div>

        <!-- Lista de Repuestos Agregados -->
        <div v-else class="space-y-2.5">
          <div
            v-for="(item, idx) in items"
            :key="idx"
            class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 p-3 rounded-2xl space-y-2.5 shadow-xs"
          >
            <!-- Fila superior: Indicador de item y botón eliminar -->
            <div class="flex items-center justify-between text-xs">
              <span class="font-extrabold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                <span class="w-1.5 h-1.5 rounded-full bg-red-600"></span>
                <span>Repuesto / Insumo #{{ idx + 1 }}</span>
              </span>
              <button
                type="button"
                @click="removeItem(idx)"
                class="text-rose-500 hover:text-rose-700 dark:hover:text-rose-400 p-1 rounded-md hover:bg-rose-50 dark:hover:bg-rose-950/40 text-xs font-bold flex items-center gap-1 transition-all"
                title="Eliminar este repuesto"
              >
                <IconTrash class="w-3.5 h-3.5 stroke-[2]" />
                <span>Quitar</span>
              </button>
            </div>

            <!-- Fila de Selección / Búsqueda en Catálogo -->
            <div>
              <input
                v-model="item.nombre_item"
                @input="autoDetectUnit(item)"
                list="lpu-catalog-manage"
                placeholder="Seleccione o escriba el nombre del repuesto..."
                class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-white/10 rounded-xl px-3 py-2 text-xs text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 focus:ring-2 focus:ring-red-500 focus:outline-none transition-all font-medium"
              />
            </div>

            <!-- Fila de Cantidad con botones +/- -->
            <div class="flex items-center justify-between pt-0.5">
              <span class="text-[11px] font-bold text-slate-600 dark:text-slate-400">
                Cantidad a reportar:
              </span>

              <div class="flex items-center gap-2">
                <!-- Stepper Disminuir -->
                <button
                  type="button"
                  @click="decrementQty(item)"
                  :disabled="item.cantidad <= 1"
                  class="w-7 h-7 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/10 disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center font-bold active:scale-95 transition-all shadow-xs"
                  title="Disminuir cantidad"
                >
                  <IconMinus class="w-3.5 h-3.5 stroke-[2.5]" />
                </button>

                <!-- Input numérico centrado -->
                <input
                  v-model.number="item.cantidad"
                  type="number"
                  min="1"
                  class="w-14 bg-white dark:bg-slate-900 border border-slate-200 dark:border-white/10 rounded-lg py-1 px-1 text-center font-mono text-xs font-black text-slate-900 dark:text-white focus:ring-2 focus:ring-red-500 focus:outline-none"
                />

                <!-- Stepper Aumentar -->
                <button
                  type="button"
                  @click="incrementQty(item)"
                  class="w-7 h-7 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/10 flex items-center justify-center font-bold active:scale-95 transition-all shadow-xs text-red-600 dark:text-red-400"
                  title="Aumentar cantidad"
                >
                  <IconPlus class="w-3.5 h-3.5 stroke-[2.5]" />
                </button>

                <!-- Etiqueta de unidad -->
                <span class="text-[10px] font-mono text-slate-500 dark:text-slate-400 pl-1">
                  {{ item.unidad_medida || 'unid.' }}
                </span>
              </div>
            </div>
          </div>

          <!-- Botón para añadir otro item al final de la lista -->
          <button
            type="button"
            @click="addItem"
            class="w-full py-2.5 rounded-xl border border-dashed border-slate-300 dark:border-white/15 text-xs font-extrabold text-slate-700 dark:text-slate-300 hover:text-red-600 dark:hover:text-red-400 hover:border-red-400 dark:hover:border-red-500/50 hover:bg-red-50/50 dark:hover:bg-red-950/20 transition-all flex items-center justify-center gap-1.5"
          >
            <IconPlus class="w-4 h-4 stroke-[2.5]" />
            <span>Agregar otro repuesto</span>
          </button>
        </div>

        <!-- Datalist para autocompletado LPU -->
        <datalist id="lpu-catalog-manage">
          <option v-for="cat in catalogoLpu" :key="cat" :value="cat"></option>
        </datalist>

        <!-- Mensaje de error local -->
        <div v-if="localError" class="bg-rose-50 dark:bg-rose-950/80 border border-rose-200 dark:border-rose-800 text-rose-700 dark:text-rose-300 p-3 rounded-xl text-xs flex items-start gap-2">
          <IconAlertCircle class="w-4 h-4 shrink-0 mt-0.5 stroke-[2]" />
          <div class="leading-relaxed font-medium">{{ localError }}</div>
        </div>

        <!-- Botones de Acción -->
        <div class="flex items-center justify-end gap-2.5 pt-2 border-t border-slate-100 dark:border-white/10">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2.5 rounded-xl text-xs font-bold text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-white/5 transition-colors"
          >
            Cancelar
          </button>
          <button
            type="button"
            @click="handleSave"
            :disabled="saving"
            class="bg-red-600 hover:bg-red-500 text-white px-5 py-2.5 rounded-xl text-xs font-extrabold shadow-lg shadow-red-600/20 flex items-center gap-2 active:scale-98 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
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
  IconPlus, 
  IconMinus, 
  IconX, 
  IconTrash, 
  IconPackageOff, 
  IconCheck, 
  IconAlertCircle 
} from '@tabler/icons-vue';

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

const sugerenciasRapidas = [
  { short: 'Batería 12V', nombre: 'Batería 12V / 100Ah VRLA AGM (ME PW)', unidad: 'unidad' },
  { short: 'Rectificador 48V', nombre: 'Módulo Rectificador 48V / 50A (ME PW)', unidad: 'unidad' },
  { short: 'Breaker 2x30A', nombre: 'Interruptor Termomagnético Breaker 2x30A (ME MT-SE)', unidad: 'unidad' },
  { short: 'Cable 2/0 P. Tierra', nombre: 'Cable de Cobre Desnudo 2/0 AWG metro (Puesta a Tierra)', unidad: 'metro' },
  { short: 'Filtro AA', nombre: 'Filtro de Aire Acondicionado / Climatización (ME/MC AA)', unidad: 'unidad' }
];

const addItem = () => {
  items.value.push({ nombre_item: '', cantidad: 1, unidad_medida: 'unidad' });
};

const addSugItem = (sug) => {
  const emptyIndex = items.value.findIndex(r => !r.nombre_item || r.nombre_item.trim() === '');
  if (emptyIndex !== -1) {
    items.value[emptyIndex].nombre_item = sug.nombre;
    items.value[emptyIndex].unidad_medida = sug.unidad;
    return;
  }
  items.value.push({
    nombre_item: sug.nombre,
    cantidad: 1,
    unidad_medida: sug.unidad
  });
};

const autoDetectUnit = (item) => {
  const lower = (item.nombre_item || '').toLowerCase();
  if (lower.includes('metro') || lower.includes('cable')) {
    item.unidad_medida = 'metro';
  } else if (lower.includes('kg') || lower.includes('gas')) {
    item.unidad_medida = 'kg';
  } else if (lower.includes('galón') || lower.includes('galon') || lower.includes('aceite')) {
    item.unidad_medida = 'galón';
  } else if (lower.includes('kit')) {
    item.unidad_medida = 'kit';
  } else {
    item.unidad_medida = 'unidad';
  }
};

const incrementQty = (item) => {
  item.cantidad = (Number(item.cantidad) || 0) + 1;
};

const decrementQty = (item) => {
  if (item.cantidad > 1) {
    item.cantidad = Number(item.cantidad) - 1;
  }
};

const removeItem = (index) => {
  items.value.splice(index, 1);
};

const handleSave = () => {
  localError.value = '';
  // Filtrar vacíos
  const validos = items.value.filter(i => i.nombre_item && i.nombre_item.trim() !== '');
  emit('save', validos);
};
</script>

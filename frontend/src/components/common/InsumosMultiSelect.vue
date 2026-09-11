<template>
  <div class="space-y-3 relative" ref="containerRef">
    <!-- Encabezado con Label y Contador -->
    <div v-if="label" class="flex items-center justify-between">
      <label class="text-[10px] font-bold text-neutral-500 dark:text-neutral-400 uppercase tracking-wider flex items-center gap-1.5">
        <IconBox class="w-3.5 h-3.5 text-red-600 dark:text-red-400 stroke-[2.2]" />
        <span>{{ label }}</span>
        <span v-if="required" class="text-rose-500 font-black">*</span>
      </label>
      <span class="text-[10px] font-mono font-bold" :class="items.length > 0 ? 'text-red-600 dark:text-red-400' : 'text-neutral-400'">
        {{ items.length }} {{ items.length === 1 ? 'insumo registrado' : 'insumos registrados' }}
      </span>
    </div>

    <!-- Sugerencias rápidas en Chips (Opcional) -->
    <div v-if="showSugerencias && !disabled" class="space-y-1.5">
      <div class="text-[10px] font-semibold text-neutral-500 dark:text-neutral-400 flex items-center gap-1">
        <span>Sugerencias frecuentes LPU:</span>
      </div>
      <div class="flex flex-wrap gap-1.5">
        <button
          v-for="sug in sugerencias"
          :key="sug.nombre"
          type="button"
          @click="addSugerencia(sug)"
          class="text-[10px] font-semibold bg-neutral-100 dark:bg-white/5 hover:bg-red-50 dark:hover:bg-red-950/40 text-neutral-700 dark:text-neutral-300 hover:text-red-600 dark:hover:text-red-400 border border-neutral-200 dark:border-white/10 rounded-lg px-2.5 py-1 transition-all flex items-center gap-1 active:scale-95 cursor-pointer"
          :title="`Agregar ${sug.nombre}`"
        >
          <IconPlus class="w-3 h-3 text-red-500 stroke-[2.5]" />
          <span>{{ sug.short }}</span>
        </button>
      </div>
    </div>

    <!-- Buscador con Desplegable Custom Elegante -->
    <div class="relative" v-if="!disabled">
      <div class="relative flex items-center">
        <IconSearch class="w-4 h-4 text-neutral-400 absolute left-3 pointer-events-none stroke-[2]" />
        <input
          ref="searchInputRef"
          type="text"
          v-model="searchQuery"
          @focus="isOpen = true"
          @input="isOpen = true"
          @keydown.esc="isOpen = false"
          @keydown.enter.prevent="handleEnterKey"
          :placeholder="placeholder"
          class="flex h-10 w-full rounded-xl border bg-white dark:bg-neutral-950 pl-9 pr-16 py-1.5 text-xs text-neutral-800 dark:text-neutral-200 placeholder:text-neutral-400 focus:outline-none focus:border-red-500 focus:ring-1 focus:ring-red-500 transition-all shadow-xs"
          :class="{
            'border-rose-300 dark:border-rose-700': required && items.length === 0 && touched,
            'border-neutral-200 dark:border-white/10': !(required && items.length === 0 && touched)
          }"
        />
        <div class="absolute right-2 flex items-center gap-1">
          <button
            v-if="searchQuery"
            type="button"
            @click="searchQuery = ''"
            class="text-neutral-400 hover:text-neutral-600 dark:hover:text-white p-1 cursor-pointer rounded-md hover:bg-neutral-100 dark:hover:bg-neutral-800"
            title="Limpiar búsqueda"
          >
            <IconX class="w-3.5 h-3.5 stroke-[2]" />
          </button>
          <button
            v-if="isOpen"
            type="button"
            @click="isOpen = false"
            class="text-[10px] font-bold text-neutral-400 hover:text-neutral-700 dark:hover:text-white px-2 py-0.5 rounded-md hover:bg-neutral-100 dark:hover:bg-neutral-800 cursor-pointer"
            title="Cerrar lista"
          >
            Cerrar
          </button>
        </div>
      </div>

      <!-- Menú Desplegable con Catálogo Oficial LPU y Búsqueda -->
      <div
        v-if="isOpen && (filteredCatalogo.length > 0 || searchQuery.trim().length > 0)"
        class="absolute left-0 right-0 top-full mt-1.5 bg-white dark:bg-[#18181b] border border-neutral-200 dark:border-neutral-700 rounded-2xl shadow-2xl z-50 max-h-56 sm:max-h-64 overflow-y-auto divide-y divide-neutral-100 dark:divide-neutral-800 custom-scrollbar"
      >
        <!-- Barra de encabezado del dropdown -->
        <div class="flex items-center justify-between px-3 py-1.5 bg-neutral-50 dark:bg-neutral-900 text-[10px] text-neutral-500 font-bold border-b border-neutral-100 dark:border-neutral-800">
          <span>Catálogo Oficial de Insumos & Repuestos</span>
          <span class="font-mono">{{ filteredCatalogo.length }} disponibles</span>
        </div>

        <!-- Opción personalizada si el texto ingresado no coincide exactamente -->
        <button
          v-if="searchQuery.trim().length > 0 && !hasExactMatch"
          type="button"
          @click="addCustomItem(searchQuery.trim())"
          class="w-full text-left px-3.5 py-2.5 hover:bg-red-50/80 dark:hover:bg-red-950/40 text-red-600 dark:text-red-400 flex items-center justify-between gap-2 transition-colors cursor-pointer"
        >
          <div class="flex items-center gap-2 min-w-0">
            <div class="w-6 h-6 rounded-lg bg-red-100 dark:bg-red-900/60 text-red-600 dark:text-red-300 flex items-center justify-center shrink-0">
              <IconPlus class="w-3.5 h-3.5 stroke-[2.5]" />
            </div>
            <div class="truncate">
              <span class="font-bold text-xs">Agregar personalizado:</span>
              <span class="font-medium ml-1.5 italic text-neutral-800 dark:text-neutral-200">"{{ searchQuery.trim() }}"</span>
            </div>
          </div>
          <span class="text-[10px] font-mono uppercase bg-red-100 dark:bg-red-900/50 px-2 py-0.5 rounded-full font-bold shrink-0">
            Nuevo Ítem
          </span>
        </button>

        <!-- Lista de Resultados Filtrados del Catálogo -->
        <button
          v-for="cat in filteredCatalogo"
          :key="cat.nombre"
          type="button"
          @click="selectCatalogItem(cat)"
          class="w-full text-left px-3.5 py-2.5 hover:bg-neutral-50 dark:hover:bg-neutral-800/80 flex items-center justify-between gap-2.5 transition-colors cursor-pointer group"
        >
          <div class="flex items-center gap-2.5 min-w-0">
            <div 
              class="w-7 h-7 rounded-xl flex items-center justify-center shrink-0 text-xs font-black"
              :class="getCategoryColor(cat.categoria)"
            >
              <component :is="getCategoryIcon(cat.categoria)" class="w-4 h-4 stroke-[2]" />
            </div>

            <div class="flex flex-col min-w-0">
              <span class="font-bold text-xs text-neutral-900 dark:text-neutral-100 truncate group-hover:text-red-600 dark:group-hover:text-red-400 transition-colors">
                {{ cat.nombre }}
              </span>
              <div class="flex items-center gap-1.5 text-[10px] text-neutral-500 dark:text-neutral-400 mt-0.5">
                <span class="font-medium text-neutral-600 dark:text-neutral-300 font-mono">{{ cat.categoria }}</span>
                <span>•</span>
                <span>Unidad: {{ cat.unidad }}</span>
              </div>
            </div>
          </div>

          <div class="flex items-center gap-1.5 shrink-0">
            <span class="text-[10px] font-mono px-2 py-0.5 rounded-md bg-neutral-100 dark:bg-neutral-800 text-neutral-600 dark:text-neutral-300 font-bold">
              {{ cat.unidad }}
            </span>
            <div class="w-5 h-5 rounded-lg bg-neutral-100 dark:bg-neutral-800 group-hover:bg-red-600 group-hover:text-white flex items-center justify-center transition-all">
              <IconPlus class="w-3 h-3 stroke-[2.5]" />
            </div>
          </div>
        </button>

        <div v-if="filteredCatalogo.length === 0 && searchQuery.trim().length === 0" class="p-4 text-center text-xs text-neutral-400">
          No hay elementos disponibles en el catálogo.
        </div>
      </div>
    </div>

    <!-- Lista de Insumos Seleccionados (Tarjetas enriquecidas con stepper de cantidad) -->
    <div v-if="items.length > 0" class="space-y-2">
      <div
        v-for="(item, idx) in items"
        :key="item.id || idx"
        class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 p-3 rounded-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-xs transition-all"
      >
        <!-- Info del Insumo -->
        <div class="flex items-center gap-2.5 min-w-0 flex-1">
          <div class="w-8 h-8 rounded-xl bg-red-50 dark:bg-red-950/80 border border-red-200 dark:border-red-800/60 text-red-600 dark:text-red-400 flex items-center justify-center shrink-0">
            <IconBox class="w-4 h-4 stroke-[2]" />
          </div>

          <div class="flex flex-col min-w-0 flex-1">
            <div class="flex items-center gap-2">
              <span class="font-extrabold text-xs text-neutral-900 dark:text-white truncate">
                {{ item.nombre_item }}
              </span>
            </div>
            <div class="flex items-center gap-2 text-[10px] text-neutral-500 dark:text-neutral-400 mt-0.5">
              <span>Unidad:</span>
              <select
                v-if="!disabled"
                v-model="item.unidad_medida"
                @change="triggerUpdate"
                class="bg-neutral-100 dark:bg-neutral-800 border-none rounded px-1.5 py-0.5 text-[10px] font-bold text-neutral-700 dark:text-neutral-300 outline-none"
              >
                <option value="unidad">Unidad</option>
                <option value="Galón">Galón</option>
                <option value="Kg">Kg</option>
                <option value="Metro">Metro</option>
                <option value="Litro">Litro</option>
                <option value="Rollo">Rollo</option>
                <option value="Kit">Kit</option>
              </select>
              <span v-else class="font-bold text-neutral-700 dark:text-neutral-300">{{ item.unidad_medida || 'unidad' }}</span>
            </div>
          </div>
        </div>

        <!-- Controles de Cantidad (+ / -) y Eliminar -->
        <div class="flex items-center justify-between sm:justify-end gap-3 shrink-0 pt-1 sm:pt-0 border-t sm:border-t-0 border-neutral-100 dark:border-white/5">
          <!-- Stepper de cantidad -->
          <div class="flex items-center gap-1.5 bg-neutral-50 dark:bg-[#0a0b10] border border-neutral-200/80 dark:border-white/10 rounded-xl p-1">
            <button
              v-if="!disabled"
              type="button"
              @click="decrementQty(item)"
              :disabled="item.cantidad <= 0.5"
              class="w-7 h-7 rounded-lg bg-white dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-white/10 disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center font-bold active:scale-95 transition-all shadow-xs cursor-pointer"
              title="Disminuir cantidad"
            >
              <IconMinus class="w-3.5 h-3.5 stroke-[2.5]" />
            </button>

            <input
              v-model.number="item.cantidad"
              @change="validateQty(item)"
              :disabled="disabled"
              type="number"
              step="0.5"
              min="0.5"
              class="w-12 bg-transparent text-center font-mono text-xs font-black text-neutral-900 dark:text-white focus:outline-none"
            />

            <button
              v-if="!disabled"
              type="button"
              @click="incrementQty(item)"
              class="w-7 h-7 rounded-lg bg-white dark:bg-neutral-800 text-red-600 dark:text-red-400 hover:bg-neutral-100 dark:hover:bg-white/10 flex items-center justify-center font-bold active:scale-95 transition-all shadow-xs cursor-pointer"
              title="Aumentar cantidad"
            >
              <IconPlus class="w-3.5 h-3.5 stroke-[2.5]" />
            </button>
          </div>

          <!-- Botón de Quitar Ítem -->
          <button
            v-if="!disabled"
            type="button"
            @click="removeItem(idx)"
            class="p-2 rounded-xl text-neutral-400 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/50 transition-colors cursor-pointer"
            title="Quitar este insumo"
          >
            <IconTrash class="w-4 h-4 stroke-[2]" />
          </button>
        </div>
      </div>
    </div>

    <!-- Estado Vacío cuando no hay ítems -->
    <div 
      v-else
      class="bg-neutral-50 dark:bg-[#0a0b10] border border-dashed border-neutral-200 dark:border-white/10 rounded-2xl p-5 text-center space-y-2 select-none"
    >
      <div class="w-9 h-9 rounded-xl bg-neutral-100 dark:bg-white/5 flex items-center justify-center mx-auto text-neutral-400 dark:text-neutral-500">
        <IconBox class="w-4 h-4 stroke-[1.8]" />
      </div>
      <div>
        <div class="text-xs font-extrabold text-neutral-700 dark:text-neutral-300">
          Sin insumos ni repuestos vinculados
        </div>
        <p class="text-[11px] text-neutral-400 dark:text-neutral-500 max-w-xs mx-auto mt-0.5">
          Busque en el catálogo superior o use las sugerencias para registrar materiales consumidos en sitio.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import { 
  IconBox, 
  IconPlus, 
  IconMinus, 
  IconX, 
  IconTrash, 
  IconSearch, 
  IconCheck,
  IconBolt,
  IconEngine,
  IconWind,
  IconTool
} from '@tabler/icons-vue';

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  label: {
    type: String,
    default: 'Insumos & Repuestos LPU Consumidos'
  },
  placeholder: {
    type: String,
    default: 'Buscar en catálogo LPU (ej. Batería 12V, Filtro, Refrigerante) o escribir nuevo...'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  showSugerencias: {
    type: Boolean,
    default: true
  },
  customCatalog: {
    type: Array,
    default: null
  }
});

const emit = defineEmits(['update:modelValue']);

const containerRef = ref(null);
const searchInputRef = ref(null);
const searchQuery = ref('');
const isOpen = ref(false);
const touched = ref(false);

const items = ref([]);

// Catálogo base enriquecido con categorías, unidad y palabras clave
const CATALOGO_OFICIAL = [
  { nombre: 'Batería 12V / 100Ah VRLA AGM (ME PW)', categoria: 'Energía / Baterías', unidad: 'unidad' },
  { nombre: 'Batería 2V / 500Ah OPzV Estacionaria (ME PW)', categoria: 'Energía / Baterías', unidad: 'unidad' },
  { nombre: 'Módulo Rectificador 48V / 50A (ME PW)', categoria: 'Fuerza DC', unidad: 'unidad' },
  { nombre: 'Filtro de Aire Acondicionado / Climatización (ME/MC AA)', categoria: 'Climatización AA', unidad: 'unidad' },
  { nombre: 'Gas Refrigerante R410A Ecológico (ME/MC AA)', categoria: 'Climatización AA', unidad: 'Kg' },
  { nombre: 'Gas Refrigerante R22 (ME/MC AA)', categoria: 'Climatización AA', unidad: 'Kg' },
  { nombre: 'Compresor Scroll 24K BTU 220V (ME/MC AA)', categoria: 'Climatización AA', unidad: 'unidad' },
  { nombre: 'Filtro Deshidratador 3/8 Soldable (ME/MC AA)', categoria: 'Climatización AA', unidad: 'unidad' },
  { nombre: 'Filtro de Aceite LF16015 Fleetguard (ME GE/ATS)', categoria: 'Plantas GE', unidad: 'unidad' },
  { nombre: 'Filtro Separador de Combustible FS1242 (ME GE/ATS)', categoria: 'Plantas GE', unidad: 'unidad' },
  { nombre: 'Aceite Lubricante 15W40 CI-4 (ME GE/ATS)', categoria: 'Plantas GE', unidad: 'Galón' },
  { nombre: 'Refrigerante Anticongelante 50/50 LPU (ME GE/ATS)', categoria: 'Plantas GE', unidad: 'Galón' },
  { nombre: 'Tarjeta Reguladora de Voltaje AVR SX460 (ME GE/ATS)', categoria: 'Plantas GE', unidad: 'unidad' },
  { nombre: 'Bomba de Agua Perkins / Selmec 40SC (ME GE/ATS)', categoria: 'Plantas GE', unidad: 'unidad' },
  { nombre: 'Interruptor Termomagnético Breaker 2x30A (ME MT-SE)', categoria: 'Subestación / MT', unidad: 'unidad' },
  { nombre: 'Cable de Cobre Desnudo 2/0 AWG (Puesta a Tierra)', categoria: 'SPT / Puesta a Tierra', unidad: 'Metro' },
  { nombre: 'Cartucho Soldadura Exotérmica Cadweld 90g', categoria: 'SPT / Puesta a Tierra', unidad: 'unidad' },
  { nombre: 'Kit Anclajes y Pernería A325 Alta Resistencia (ME ALTURA)', categoria: 'Torre / Alturas', unidad: 'unidad' },
  { nombre: 'Pintura Epóxica Balizamiento Naranja Aeronáutico', categoria: 'Torre / Alturas', unidad: 'Galón' },
  { nombre: 'Abrazadera Acero Inoxidable 2" - 4" (ME ALTURA)', categoria: 'Torre / Alturas', unidad: 'unidad' },
  { nombre: 'Cinta Autofundente y Vulcanizada 3M 23', categoria: 'Materiales Menores', unidad: 'Rollo' },
  { nombre: 'Terminal de Compresión 2 AWG 1/4"', categoria: 'Materiales Menores', unidad: 'unidad' },
];

const sugerencias = [
  { short: 'Batería 12V AGM', nombre: 'Batería 12V / 100Ah VRLA AGM (ME PW)', unidad: 'unidad' },
  { short: 'Filtro Aceite GE', nombre: 'Filtro de Aceite LF16015 Fleetguard (ME GE/ATS)', unidad: 'unidad' },
  { short: 'Aceite 15W40', nombre: 'Aceite Lubricante 15W40 CI-4 (ME GE/ATS)', unidad: 'Galón' },
  { short: 'Gas R410A', nombre: 'Gas Refrigerante R410A Ecológico (ME/MC AA)', unidad: 'Kg' },
  { short: 'Filtro AA Clima', nombre: 'Filtro de Aire Acondicionado / Climatización (ME/MC AA)', unidad: 'unidad' },
  { short: 'Cable 2/0 Tierra', nombre: 'Cable de Cobre Desnudo 2/0 AWG (Puesta a Tierra)', unidad: 'Metro' },
];

const catalogo = computed(() => {
  return props.customCatalog || CATALOGO_OFICIAL;
});

const filteredCatalogo = computed(() => {
  const q = searchQuery.value.toLowerCase().trim();
  if (!q) return catalogo.value;
  return catalogo.value.filter(cat => 
    cat.nombre.toLowerCase().includes(q) || 
    cat.categoria.toLowerCase().includes(q)
  );
});

const hasExactMatch = computed(() => {
  const q = searchQuery.value.toLowerCase().trim();
  if (!q) return false;
  return catalogo.value.some(cat => cat.nombre.toLowerCase() === q);
});

// Sincronización con v-model bidireccional
watch(() => props.modelValue, (newVal) => {
  if (Array.isArray(newVal)) {
    // Clonar para mutación local controlada
    items.value = newVal.map(it => ({
      nombre_item: it.nombre_item || it.nombre || '',
      cantidad: Number(it.cantidad) > 0 ? Number(it.cantidad) : 1,
      unidad_medida: it.unidad_medida || it.unidad || detectUnit(it.nombre_item || it.nombre || ''),
      categoria: it.categoria || ''
    }));
  } else {
    items.value = [];
  }
}, { immediate: true, deep: true });

const triggerUpdate = () => {
  touched.value = true;
  emit('update:modelValue', items.value.map(it => ({
    nombre_item: it.nombre_item,
    cantidad: Number(it.cantidad) || 1,
    unidad_medida: it.unidad_medida || 'unidad'
  })));
};

const detectUnit = (nombre) => {
  const n = (nombre || '').toLowerCase();
  if (n.includes('galón') || n.includes('galon') || n.includes('aceite') || n.includes('pintura') || n.includes('refrigerante 50/50')) return 'Galón';
  if (n.includes('metro') || n.includes('cable') || n.includes('manguera')) return 'Metro';
  if (n.includes('kg') || n.includes('r410a') || n.includes('r22') || n.includes('gas')) return 'Kg';
  if (n.includes('rollo') || n.includes('cinta')) return 'Rollo';
  if (n.includes('kit')) return 'Kit';
  return 'unidad';
};

const selectCatalogItem = (cat) => {
  // Verificar si ya existe en la lista para solo incrementar cantidad
  const existing = items.value.find(i => i.nombre_item.toLowerCase() === cat.nombre.toLowerCase());
  if (existing) {
    existing.cantidad = Number(existing.cantidad || 0) + 1;
  } else {
    items.value.push({
      nombre_item: cat.nombre,
      cantidad: 1,
      unidad_medida: cat.unidad || 'unidad',
      categoria: cat.categoria
    });
  }
  searchQuery.value = '';
  isOpen.value = false;
  triggerUpdate();
};

const addCustomItem = (nombre) => {
  if (!nombre) return;
  const existing = items.value.find(i => i.nombre_item.toLowerCase() === nombre.toLowerCase());
  if (existing) {
    existing.cantidad = Number(existing.cantidad || 0) + 1;
  } else {
    items.value.push({
      nombre_item: nombre,
      cantidad: 1,
      unidad_medida: detectUnit(nombre),
      categoria: 'Personalizado'
    });
  }
  searchQuery.value = '';
  isOpen.value = false;
  triggerUpdate();
};

const addSugerencia = (sug) => {
  const existing = items.value.find(i => i.nombre_item.toLowerCase() === sug.nombre.toLowerCase());
  if (existing) {
    existing.cantidad = Number(existing.cantidad || 0) + 1;
  } else {
    items.value.push({
      nombre_item: sug.nombre,
      cantidad: 1,
      unidad_medida: sug.unidad || 'unidad',
      categoria: 'LPU Frecuente'
    });
  }
  triggerUpdate();
};

const handleEnterKey = () => {
  const q = searchQuery.value.trim();
  if (!q) return;
  if (filteredCatalogo.value.length > 0) {
    selectCatalogItem(filteredCatalogo.value[0]);
  } else {
    addCustomItem(q);
  }
};

const removeItem = (idx) => {
  items.value.splice(idx, 1);
  triggerUpdate();
};

const incrementQty = (item) => {
  item.cantidad = (Number(item.cantidad) || 0) + 1;
  triggerUpdate();
};

const decrementQty = (item) => {
  if (item.cantidad > 1) {
    item.cantidad = (Number(item.cantidad) || 0) - 1;
  } else if (item.cantidad > 0.5) {
    item.cantidad = 0.5;
  }
  triggerUpdate();
};

const validateQty = (item) => {
  if (!item.cantidad || item.cantidad <= 0) {
    item.cantidad = 1;
  }
  triggerUpdate();
};

const getCategoryIcon = (cat) => {
  const c = (cat || '').toLowerCase();
  if (c.includes('batería') || c.includes('fuerza') || c.includes('energía')) return IconBolt;
  if (c.includes('planta') || c.includes('motor')) return IconEngine;
  if (c.includes('clima') || c.includes('aire')) return IconWind;
  return IconTool;
};

const getCategoryColor = (cat) => {
  const c = (cat || '').toLowerCase();
  if (c.includes('batería') || c.includes('fuerza')) return 'bg-amber-100 text-amber-700 dark:bg-amber-950/60 dark:text-amber-400';
  if (c.includes('planta')) return 'bg-blue-100 text-blue-700 dark:bg-blue-950/60 dark:text-blue-400';
  if (c.includes('clima')) return 'bg-cyan-100 text-cyan-700 dark:bg-cyan-950/60 dark:text-cyan-400';
  return 'bg-neutral-100 text-neutral-700 dark:bg-neutral-800 dark:text-neutral-300';
};

const handleClickOutside = (e) => {
  if (containerRef.value && !containerRef.value.contains(e.target)) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

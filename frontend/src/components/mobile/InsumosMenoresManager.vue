<template>
  <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-sm transition-colors duration-300 relative" ref="containerRef">
    <!-- Header del Componente -->
    <div class="flex items-center justify-between flex-wrap gap-2.5 border-b border-slate-100 dark:border-white/10 pb-3">
      <div class="flex items-center gap-2.5">
        <div class="w-8 h-8 rounded-xl bg-emerald-50 dark:bg-emerald-950/80 border border-emerald-200 dark:border-emerald-800 flex items-center justify-center text-emerald-600 dark:text-emerald-400 shrink-0">
          <IconTools class="w-4 h-4 stroke-[2]" />
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h3 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
              Materiales & Insumos Menores
            </h3>
            <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-slate-100 dark:bg-white/5 text-slate-600 dark:text-slate-400">
              {{ items.length }} {{ items.length === 1 ? 'insumo registrado' : 'insumos registrados' }}
            </span>
          </div>
          <p class="text-[11px] text-slate-500 dark:text-slate-400 font-medium mt-0.5">
            Buscador oficial de consumibles con captura obligatoria de foto ANTES y DESPUÉS de su aplicación.
          </p>
        </div>
      </div>
    </div>

    <!-- Sugerencias Rápidas LPU en Chips Interactivos -->
    <div v-if="!readOnly" class="space-y-1.5">
      <div class="text-[10px] font-semibold text-slate-500 dark:text-slate-400 flex items-center gap-1">
        <span>Sugerencias frecuentes LPU:</span>
      </div>
      <div class="flex flex-wrap gap-1.5">
        <button
          v-for="sug in sugerenciasInsumos"
          :key="sug.nombre"
          type="button"
          @click="agregarInsumoDirecto(sug.nombre, sug.unidad)"
          class="text-[10px] font-semibold bg-slate-100 dark:bg-white/5 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 text-slate-700 dark:text-slate-300 hover:text-emerald-600 dark:hover:text-emerald-400 border border-slate-200/80 dark:border-white/10 rounded-lg px-2.5 py-1 transition-all flex items-center gap-1 active:scale-95 cursor-pointer"
          :title="`Agregar ${sug.nombre}`"
        >
          <IconPlus class="w-3 h-3 text-emerald-600 dark:text-emerald-400 stroke-[2.5]" />
          <span>{{ sug.short }}</span>
        </button>
      </div>
    </div>

    <!-- Buscador Reactivo con Desplegable Custom Elegante (Similar a Buscador de Empleados) -->
    <div class="relative" v-if="!readOnly">
      <div class="relative flex items-center">
        <IconSearch class="w-4 h-4 text-slate-400 absolute left-3 pointer-events-none stroke-[2]" />
        <input
          ref="searchInputRef"
          type="text"
          v-model="busqueda"
          @focus="isOpen = true"
          @input="isOpen = true"
          @keydown.esc="isOpen = false"
          @keydown.enter.prevent="agregarDesdeBusqueda"
          placeholder="Buscar en catálogo oficial LPU (ej. Cinta 3M, Refrigerante, Cable, Silicona, Terminal) o escribir nuevo..."
          class="flex h-10 w-full rounded-xl border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 pl-9 pr-16 py-1.5 text-xs text-slate-800 dark:text-slate-200 placeholder:text-slate-400 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all shadow-xs"
        />
        <div class="absolute right-2 flex items-center gap-1">
          <button
            v-if="busqueda"
            type="button"
            @click="busqueda = ''"
            class="text-slate-400 hover:text-slate-600 dark:hover:text-white p-1 cursor-pointer rounded-md hover:bg-slate-100 dark:hover:bg-neutral-800"
            title="Limpiar búsqueda"
          >
            <IconX class="w-3.5 h-3.5 stroke-[2]" />
          </button>
          <button
            v-if="isOpen"
            type="button"
            @click="isOpen = false"
            class="text-[10px] font-bold text-slate-400 hover:text-slate-700 dark:hover:text-white px-2 py-0.5 rounded-md hover:bg-slate-100 dark:hover:bg-neutral-800 cursor-pointer"
            title="Cerrar lista"
          >
            Cerrar
          </button>
        </div>
      </div>

      <!-- Menú Desplegable Flotante con Catálogo Oficial LPU y Búsqueda en Tiempo Real -->
      <div
        v-if="isOpen && (filteredCatalogo.length > 0 || busqueda.trim().length > 0)"
        class="absolute left-0 right-0 top-full mt-1.5 bg-white dark:bg-[#18181b] border border-slate-200 dark:border-neutral-700 rounded-2xl shadow-2xl z-50 max-h-56 sm:max-h-64 overflow-y-auto divide-y divide-slate-100 dark:divide-neutral-800 custom-scrollbar"
      >
        <!-- Barra de encabezado del dropdown -->
        <div class="flex items-center justify-between px-3 py-1.5 bg-slate-50 dark:bg-neutral-900 text-[10px] text-slate-500 font-bold border-b border-slate-100 dark:border-neutral-800">
          <span>Catálogo Oficial de Materiales & Insumos Menores</span>
          <span class="font-mono">{{ filteredCatalogo.length }} disponibles</span>
        </div>

        <!-- Opción personalizada si el texto ingresado no coincide exactamente con el catálogo -->
        <button
          v-if="busqueda.trim().length > 0 && !hasExactMatch"
          type="button"
          @click="agregarDesdeBusqueda"
          class="w-full text-left px-3.5 py-2.5 hover:bg-emerald-50/80 dark:hover:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 flex items-center justify-between gap-2 transition-colors cursor-pointer"
        >
          <div class="flex items-center gap-2 min-w-0">
            <div class="w-6 h-6 rounded-lg bg-emerald-100 dark:bg-emerald-900/60 text-emerald-600 dark:text-emerald-300 flex items-center justify-center shrink-0">
              <IconPlus class="w-3.5 h-3.5 stroke-[2.5]" />
            </div>
            <div class="truncate">
              <span class="font-bold text-xs">Agregar nuevo material:</span>
              <span class="font-medium ml-1.5 italic text-slate-800 dark:text-slate-200">"{{ busqueda.trim() }}"</span>
            </div>
          </div>
          <span class="text-[10px] font-mono uppercase bg-emerald-100 dark:bg-emerald-900/50 px-2 py-0.5 rounded-full font-bold shrink-0">
            Nuevo Ítem
          </span>
        </button>

        <!-- Lista de Resultados Filtrados del Catálogo -->
        <button
          v-for="cat in filteredCatalogo"
          :key="cat.nombre"
          type="button"
          @click="seleccionarDelCatalogo(cat)"
          class="w-full text-left px-3.5 py-2.5 hover:bg-slate-50 dark:hover:bg-neutral-800/80 flex items-center justify-between gap-2.5 transition-colors cursor-pointer group"
        >
          <div class="flex items-center gap-2.5 min-w-0">
            <div 
              class="w-7 h-7 rounded-xl flex items-center justify-center shrink-0 text-xs font-black"
              :class="getCategoryColor(cat.categoria)"
            >
              <component :is="getCategoryIcon(cat.categoria)" class="w-4 h-4 stroke-[2]" />
            </div>

            <div class="flex flex-col min-w-0">
              <span class="font-bold text-xs text-slate-900 dark:text-slate-100 truncate group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors">
                {{ cat.nombre }}
              </span>
              <div class="flex items-center gap-1.5 text-[10px] text-slate-500 dark:text-slate-400 mt-0.5">
                <span class="font-medium text-slate-600 dark:text-slate-300 font-mono">{{ cat.categoria }}</span>
                <span>•</span>
                <span>Unidad: {{ cat.unidad }}</span>
              </div>
            </div>
          </div>

          <div class="flex items-center gap-1.5 shrink-0">
            <span class="text-[10px] font-mono px-2 py-0.5 rounded-md bg-slate-100 dark:bg-neutral-800 text-slate-600 dark:text-slate-300 font-bold">
              {{ cat.unidad }}
            </span>
            <div class="w-5 h-5 rounded-lg bg-slate-100 dark:bg-neutral-800 group-hover:bg-emerald-600 group-hover:text-white flex items-center justify-center transition-all">
              <IconPlus class="w-3 h-3 stroke-[2.5]" />
            </div>
          </div>
        </button>

        <div v-if="filteredCatalogo.length === 0 && busqueda.trim().length === 0" class="p-4 text-center text-xs text-slate-400">
          No hay elementos disponibles en el catálogo.
        </div>
      </div>
    </div>

    <!-- Estado vacío cuando no hay insumos -->
    <div v-if="items.length === 0 && !isOpen" class="text-center py-6 px-4 bg-slate-50 dark:bg-[#0a0b10] border border-dashed border-slate-200 dark:border-white/10 rounded-xl space-y-2">
      <IconTools class="w-8 h-8 mx-auto text-emerald-500 stroke-[1.5]" />
      <div class="text-xs font-bold text-slate-800 dark:text-slate-200">
        No se han registrado insumos ni consumibles menores
      </div>
      <p class="text-[11px] text-slate-500 dark:text-slate-400 max-w-sm mx-auto">
        Todo material menor (cintas, silicona, conectores, amarras, químicos) requiere foto antes y después.
      </p>
      <button
        v-if="!readOnly"
        type="button"
        @click="focarBuscador"
        class="mt-2 inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold shadow-sm cursor-pointer active:scale-95 transition-all"
      >
        <IconPlus class="w-3.5 h-3.5 stroke-[2.5]" />
        <span>Buscar & Registrar Insumo</span>
      </button>
    </div>

    <!-- Lista de Insumos Registrados con Fotos Antes y Después -->
    <div v-else class="space-y-4">
      <div
        v-for="(ins, index) in items"
        :key="index"
        class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200/90 dark:border-white/10 rounded-xl p-3.5 space-y-3 relative group"
      >
        <div class="flex items-center justify-between border-b border-slate-200/60 dark:border-white/5 pb-2">
          <div class="flex items-center gap-2">
            <span class="w-5 h-5 rounded-full bg-emerald-200 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-200 text-[10px] flex items-center justify-center font-bold">
              {{ index + 1 }}
            </span>
            <span class="text-xs font-black text-slate-900 dark:text-white">
              {{ ins.nombre_item || 'Insumo sin nombre' }}
            </span>
          </div>

          <button
            v-if="!readOnly"
            type="button"
            @click="eliminarInsumo(index)"
            class="text-rose-500 hover:text-rose-700 dark:hover:text-rose-400 p-1 rounded-lg hover:bg-rose-50 dark:hover:bg-rose-950/50 transition-colors cursor-pointer"
            title="Eliminar insumo"
          >
            <IconTrash class="w-4 h-4" />
          </button>
        </div>

        <!-- Descripción, Cantidad y Unidad -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div class="space-y-1 sm:col-span-1">
            <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
              Nombre Insumo *
            </label>
            <input
              type="text"
              v-model="ins.nombre_item"
              :disabled="readOnly"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 py-1 text-xs font-medium text-slate-800 dark:text-slate-200 focus:border-emerald-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
              Cantidad Utilizada *
            </label>
            <input
              type="number"
              v-model.number="ins.cantidad"
              :disabled="readOnly"
              min="0.1"
              step="0.5"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 py-1 text-xs font-medium text-slate-800 dark:text-slate-200 focus:border-emerald-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
              Unidad
            </label>
            <select
              v-model="ins.unidad_medida"
              :disabled="readOnly"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 py-1 text-xs font-medium text-slate-800 dark:text-slate-200 focus:border-emerald-500 focus:outline-none"
            >
              <option value="unidad">Unidad</option>
              <option value="rollo">Rollo</option>
              <option value="galon">Galón</option>
              <option value="litro">Litro</option>
              <option value="metro">Metro</option>
              <option value="paquete">Paquete</option>
              <option value="tarro">Tarro / Frasco</option>
              <option value="kit">Kit</option>
              <option value="kg">Kg</option>
            </select>
          </div>
        </div>

        <!-- Dos fotos obligatorias: ANTES y DESPUÉS -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
          <SinglePhotoCapture
            v-model="ins.foto_antes"
            label="Foto Insumo ANTES (Empaque / Previo) *"
            tag="INSUMO ANTES"
            :codigo-ot="codigoOt"
            :disabled="readOnly"
            placeholder="Tomar foto del insumo antes de aplicar"
            :required="true"
          />

          <SinglePhotoCapture
            v-model="ins.foto_despues"
            label="Foto Insumo DESPUÉS (Instalado / Aplicado) *"
            tag="INSUMO DESPUES"
            :codigo-ot="codigoOt"
            :disabled="readOnly"
            placeholder="Tomar foto del insumo aplicado en sitio"
            :required="true"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { 
  IconTools, 
  IconPlus, 
  IconTrash, 
  IconSearch, 
  IconX,
  IconBox,
  IconBolt,
  IconEngine,
  IconWind,
  IconTool
} from '@tabler/icons-vue';
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

const containerRef = ref(null);
const searchInputRef = ref(null);
const isOpen = ref(false);
const busqueda = ref('');

const items = computed({
  get: () => props.modelValue || [],
  set: (val) => emit('update:modelValue', val)
});

// Catálogo Oficial LPU enriquecido
const CATALOGO_OFICIAL_INSUMOS = [
  { nombre: 'Cinta Autofundente y Vulcanizada 3M 23', categoria: 'Materiales Menores', unidad: 'rollo' },
  { nombre: 'Cinta Aislante Negra 3M Super 33+', categoria: 'Materiales Menores', unidad: 'rollo' },
  { nombre: 'Cinta de Teflón Industrial 3/4"', categoria: 'Materiales Menores', unidad: 'rollo' },
  { nombre: 'Amarras Plásticas Negras UV 30cm (pack x100)', categoria: 'Materiales Menores', unidad: 'paquete' },
  { nombre: 'Limpiador Desengrasante Dieléctrico CRC', categoria: 'Materiales Menores', unidad: 'tarro' },
  { nombre: 'Silicona Sellante Estructural Transparente', categoria: 'Materiales Menores', unidad: 'unidad' },
  { nombre: 'Terminal de Compresión 2 AWG 1/4"', categoria: 'Materiales Menores', unidad: 'unidad' },
  { nombre: 'Terminal de Ojo 1/0 a 3/8"', categoria: 'Materiales Menores', unidad: 'unidad' },
  { nombre: 'Aceite Lubricante 15W40 CI-4 (Mobil Delvac / Shell)', categoria: 'Plantas GE', unidad: 'galon' },
  { nombre: 'Refrigerante Anticongelante 50/50 LPU Claro', categoria: 'Plantas GE', unidad: 'galon' },
  { nombre: 'Filtro de Aceite LF16015 Fleetguard', categoria: 'Plantas GE', unidad: 'unidad' },
  { nombre: 'Filtro Separador de Combustible FS1242', categoria: 'Plantas GE', unidad: 'unidad' },
  { nombre: 'Gas Refrigerante R410A Ecológico', categoria: 'Climatización AA', unidad: 'kg' },
  { nombre: 'Filtro de Aire Acondicionado / Climatización Tipo Panel', categoria: 'Climatización AA', unidad: 'unidad' },
  { nombre: 'Cable de Cobre Desnudo 2/0 AWG (Puesta a Tierra)', categoria: 'SPT / Puesta a Tierra', unidad: 'metro' },
  { nombre: 'Cartucho Soldadura Exotérmica Cadweld 90g', categoria: 'SPT / Puesta a Tierra', unidad: 'unidad' },
  { nombre: 'Abrazadera Acero Inoxidable 2" - 4"', categoria: 'Torre / Alturas', unidad: 'unidad' },
  { nombre: 'Kit Anclajes y Pernería A325 Alta Resistencia', categoria: 'Torre / Alturas', unidad: 'unidad' }
];

const sugerenciasInsumos = [
  { short: 'Cinta Autofundente', nombre: 'Cinta Autofundente y Vulcanizada 3M 23', unidad: 'rollo' },
  { short: 'Cinta Aislante 3M', nombre: 'Cinta Aislante Negra 3M Super 33+', unidad: 'rollo' },
  { short: 'Teflón Industrial', nombre: 'Cinta de Teflón Industrial 3/4"', unidad: 'rollo' },
  { short: 'Amarras Plásticas', nombre: 'Amarras Plásticas Negras UV 30cm (pack x100)', unidad: 'paquete' },
  { short: 'Limpiador Dieléctrico', nombre: 'Limpiador Desengrasante Dieléctrico CRC', unidad: 'tarro' },
  { short: 'Refrigerante 50/50', nombre: 'Refrigerante Anticongelante 50/50 LPU Claro', unidad: 'galon' },
  { short: 'Gas R410A', nombre: 'Gas Refrigerante R410A Ecológico', unidad: 'kg' },
  { short: 'Aceite 15W40', nombre: 'Aceite Lubricante 15W40 CI-4 (Mobil Delvac / Shell)', unidad: 'galon' }
];

const filteredCatalogo = computed(() => {
  const q = busqueda.value.toLowerCase().trim();
  if (!q) return CATALOGO_OFICIAL_INSUMOS;
  return CATALOGO_OFICIAL_INSUMOS.filter(cat => 
    cat.nombre.toLowerCase().includes(q) || 
    cat.categoria.toLowerCase().includes(q)
  );
});

const hasExactMatch = computed(() => {
  const q = busqueda.value.toLowerCase().trim();
  if (!q) return false;
  return CATALOGO_OFICIAL_INSUMOS.some(cat => cat.nombre.toLowerCase() === q);
});

const getCategoryIcon = (categoria) => {
  const cat = (categoria || '').toLowerCase();
  if (cat.includes('energía') || cat.includes('fuerza') || cat.includes('batería')) return IconBolt;
  if (cat.includes('planta') || cat.includes('ge')) return IconEngine;
  if (cat.includes('climatiz') || cat.includes('aa')) return IconWind;
  if (cat.includes('spt') || cat.includes('tierra')) return IconTool;
  return IconBox;
};

const getCategoryColor = (categoria) => {
  const cat = (categoria || '').toLowerCase();
  if (cat.includes('energía') || cat.includes('fuerza') || cat.includes('batería')) {
    return 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300';
  }
  if (cat.includes('planta') || cat.includes('ge')) {
    return 'bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300';
  }
  if (cat.includes('climatiz') || cat.includes('aa')) {
    return 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300';
  }
  if (cat.includes('spt') || cat.includes('tierra')) {
    return 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300';
  }
  return 'bg-slate-100 text-slate-700 dark:bg-neutral-800 dark:text-slate-300';
};

const detectUnit = (nombre) => {
  const n = (nombre || '').toLowerCase();
  if (n.includes('galón') || n.includes('galon') || n.includes('aceite') || n.includes('refrigerante 50/50')) return 'galon';
  if (n.includes('metro') || n.includes('cable') || n.includes('manguera')) return 'metro';
  if (n.includes('kg') || n.includes('r410a') || n.includes('r22') || n.includes('gas')) return 'kg';
  if (n.includes('rollo') || n.includes('cinta')) return 'rollo';
  if (n.includes('paquete') || n.includes('amarras')) return 'paquete';
  if (n.includes('tarro') || n.includes('limpiador')) return 'tarro';
  if (n.includes('kit')) return 'kit';
  return 'unidad';
};

const focarBuscador = () => {
  isOpen.value = true;
  if (searchInputRef.value) {
    searchInputRef.value.focus();
  }
};

const seleccionarDelCatalogo = (cat) => {
  agregarInsumoDirecto(cat.nombre, cat.unidad);
};

const agregarInsumoDirecto = (nombre, unidad = null) => {
  const finalUnit = unidad || detectUnit(nombre);
  const current = [...items.value];
  current.push({
    nombre_item: nombre,
    cantidad: 1,
    unidad_medida: finalUnit,
    foto_antes: '',
    foto_despues: ''
  });
  emit('update:modelValue', current);
  busqueda.value = '';
  isOpen.value = false;
};

const agregarDesdeBusqueda = () => {
  const query = busqueda.value.trim();
  if (!query) return;
  agregarInsumoDirecto(query);
};

const eliminarInsumo = (idx) => {
  const current = [...items.value];
  current.splice(idx, 1);
  emit('update:modelValue', current);
};

// Cerrar al hacer click afuera
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

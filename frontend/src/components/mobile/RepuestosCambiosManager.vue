<template>
  <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-sm transition-colors duration-300 relative" ref="containerRef">
    <!-- Header del Componente -->
    <div class="flex items-center justify-between flex-wrap gap-2.5 border-b border-slate-100 dark:border-white/10 pb-3">
      <div class="flex items-center gap-2.5">
        <div class="w-8 h-8 rounded-xl bg-blue-50 dark:bg-blue-950/80 border border-blue-200 dark:border-blue-800 flex items-center justify-center text-blue-600 dark:text-blue-400 shrink-0">
          <IconExchange class="w-4 h-4 stroke-[2]" />
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h3 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
              Repuestos Retirados & Instalados
            </h3>
            <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-slate-100 dark:bg-white/5 text-slate-600 dark:text-slate-400">
              {{ items.length }} {{ items.length === 1 ? 'cambio registrado' : 'cambios registrados' }}
            </span>
          </div>
          <p class="text-[11px] text-slate-500 dark:text-slate-400 font-medium mt-0.5">
            A medida que reemplace componentes, registre el repuesto retirado vs nuevo instalado y suba su fotografía.
          </p>
        </div>
      </div>
    </div>

    <!-- Sugerencias Rápidas LPU en Chips Interactivos -->
    <div v-if="!readOnly" class="space-y-1.5">
      <div class="text-[10px] font-semibold text-slate-500 dark:text-slate-400 flex items-center gap-1">
        <span>Sugerencias frecuentes de componentes:</span>
      </div>
      <div class="flex flex-wrap gap-1.5">
        <button
          v-for="sug in sugerenciasRepuestos"
          :key="sug.nombre"
          type="button"
          @click="agregarRepuestoDirecto(sug.nombre, sug.unidad)"
          class="text-[10px] font-semibold bg-slate-100 dark:bg-white/5 hover:bg-blue-50 dark:hover:bg-blue-950/40 text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 border border-slate-200/80 dark:border-white/10 rounded-lg px-2.5 py-1 transition-all flex items-center gap-1 active:scale-95 cursor-pointer"
          :title="`Registrar reemplazo de ${sug.nombre}`"
        >
          <IconPlus class="w-3 h-3 text-blue-600 dark:text-blue-400 stroke-[2.5]" />
          <span>{{ sug.short }}</span>
        </button>
      </div>
    </div>

    <!-- Buscador Reactivo con Desplegable Custom Elegante (Idéntico en Todos los Módulos) -->
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
          placeholder="Buscar repuesto a reemplazar en catálogo oficial (ej. Batería 12V, Tarjeta AVR, Bomba Perkins, Rectificador) o escribir nuevo..."
          class="flex h-10 w-full rounded-xl border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 pl-9 pr-16 py-1.5 text-xs text-slate-800 dark:text-slate-200 placeholder:text-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all shadow-xs"
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
          <span>Catálogo Oficial de Repuestos & Componentes LPU</span>
          <span class="font-mono">{{ filteredCatalogo.length }} disponibles</span>
        </div>

        <!-- Opción personalizada si el texto ingresado no coincide exactamente con el catálogo -->
        <button
          v-if="busqueda.trim().length > 0 && !hasExactMatch"
          type="button"
          @click="agregarDesdeBusqueda"
          class="w-full text-left px-3.5 py-2.5 hover:bg-blue-50/80 dark:hover:bg-blue-950/40 text-blue-600 dark:text-blue-400 flex items-center justify-between gap-2 transition-colors cursor-pointer"
        >
          <div class="flex items-center gap-2 min-w-0">
            <div class="w-6 h-6 rounded-lg bg-blue-100 dark:bg-blue-900/60 text-blue-600 dark:text-blue-300 flex items-center justify-center shrink-0">
              <IconPlus class="w-3.5 h-3.5 stroke-[2.5]" />
            </div>
            <div class="truncate">
              <span class="font-bold text-xs">Registrar nuevo componente:</span>
              <span class="font-medium ml-1.5 italic text-slate-800 dark:text-slate-200">"{{ busqueda.trim() }}"</span>
            </div>
          </div>
          <span class="text-[10px] font-mono uppercase bg-blue-100 dark:bg-blue-900/50 px-2 py-0.5 rounded-full font-bold shrink-0">
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
              <span class="font-bold text-xs text-slate-900 dark:text-slate-100 truncate group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
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
            <div class="w-5 h-5 rounded-lg bg-slate-100 dark:bg-neutral-800 group-hover:bg-blue-600 group-hover:text-white flex items-center justify-center transition-all">
              <IconPlus class="w-3 h-3 stroke-[2.5]" />
            </div>
          </div>
        </button>

        <div v-if="filteredCatalogo.length === 0 && busqueda.trim().length === 0" class="p-4 text-center text-xs text-slate-400">
          No hay elementos disponibles en el catálogo.
        </div>
      </div>
    </div>

    <!-- Estado vacío cuando no hay repuestos cambiados -->
    <div v-if="items.length === 0 && !isOpen" class="text-center py-6 px-4 bg-slate-50 dark:bg-[#0a0b10] border border-dashed border-slate-200 dark:border-white/10 rounded-xl space-y-2">
      <IconBox class="w-8 h-8 mx-auto text-blue-400 stroke-[1.5]" />
      <div class="text-xs font-bold text-slate-800 dark:text-slate-200">
        No se han registrado repuestos cambiados
      </div>
      <p class="text-[11px] text-slate-500 dark:text-slate-400 max-w-sm mx-auto">
        Si desmontó tarjetas, compresores, correas, filtros o piezas averiadas e instaló un reemplazo, regístrelo aquí con sus fotos.
      </p>
      <button
        v-if="!readOnly"
        type="button"
        @click="focarBuscador"
        class="mt-2 inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-bold shadow-sm cursor-pointer active:scale-95 transition-all"
      >
        <IconPlus class="w-3.5 h-3.5 stroke-[2.5]" />
        <span>Buscar & Registrar Repuesto</span>
      </button>
    </div>

    <!-- Lista de repuestos registrados con sus fotos de sustitución -->
    <div v-else class="space-y-4">
      <div
        v-for="(r, index) in items"
        :key="index"
        class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200/90 dark:border-white/10 rounded-xl p-3.5 space-y-3 relative group"
      >
        <div class="flex items-center justify-between border-b border-slate-200/60 dark:border-white/5 pb-2">
          <div class="flex items-center gap-2">
            <span class="w-5 h-5 rounded-full bg-blue-200 dark:bg-blue-900/60 text-blue-800 dark:text-blue-200 text-[10px] flex items-center justify-center font-bold">
              {{ index + 1 }}
            </span>
            <span class="text-xs font-extrabold text-slate-800 dark:text-slate-200 truncate max-w-xs sm:max-w-md">
              {{ r.item_instalado || r.item_retirado || `Reemplazo de Repuesto #${index + 1}` }}
            </span>
          </div>

          <button
            v-if="!readOnly"
            type="button"
            @click="eliminarRepuesto(index)"
            class="text-rose-500 hover:text-rose-700 dark:hover:text-rose-400 p-1 rounded-lg hover:bg-rose-50 dark:hover:bg-rose-950/50 transition-colors cursor-pointer"
            title="Eliminar este reemplazo"
          >
            <IconTrash class="w-4 h-4" />
          </button>
        </div>

        <!-- Cantidad y Unidad -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
              Cantidad *
            </label>
            <input
              type="number"
              v-model.number="r.cantidad"
              :disabled="readOnly"
              min="0.5"
              step="0.5"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 py-1 text-xs font-medium text-slate-800 dark:text-slate-200 focus:border-blue-500 focus:outline-none"
            />
          </div>
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
              Unidad de Medida
            </label>
            <select
              v-model="r.unidad_medida"
              :disabled="readOnly"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 py-1 text-xs font-medium text-slate-800 dark:text-slate-200 focus:border-blue-500 focus:outline-none"
            >
              <option value="unidad">Unidad</option>
              <option value="kit">Kit</option>
              <option value="juego">Juego</option>
              <option value="metro">Metro</option>
              <option value="galon">Galón</option>
              <option value="kg">Kg</option>
              <option value="rollo">Rollo</option>
            </select>
          </div>
        </div>

        <!-- Dos Columnas: Retirado vs Instalado -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
          <!-- Bloque Repuesto Retirado -->
          <div class="p-3 rounded-xl border border-rose-200/70 dark:border-rose-900/30 bg-rose-50/30 dark:bg-rose-950/10 space-y-2.5">
            <span class="text-[11px] font-black text-rose-700 dark:text-rose-400 uppercase tracking-wider flex items-center gap-1.5">
              <IconArrowBackUp class="w-3.5 h-3.5" />
              <span>1. Repuesto Retirado (Averiado / Antiguo)</span>
            </span>

            <div class="space-y-1">
              <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase">
                Descripción / Pieza *
              </label>
              <input
                type="text"
                v-model="r.item_retirado"
                :disabled="readOnly"
                placeholder="Ej. Tarjeta AVR averiada / Bomba agua con fuga..."
                class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 py-1 text-xs text-slate-800 dark:text-slate-200 focus:border-rose-500 focus:outline-none"
              />
            </div>

            <div class="space-y-1">
              <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase">
                Serial / Marca Retirada
              </label>
              <input
                type="text"
                v-model="r.serial_retirado"
                :disabled="readOnly"
                placeholder="Ej. Stamford SX460 S/N 93821"
                class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 py-1 text-xs text-slate-800 dark:text-slate-200 focus:border-rose-500 focus:outline-none font-mono"
              />
            </div>

            <SinglePhotoCapture
              v-model="r.foto_retirado"
              label="Foto Repuesto Retirado *"
              tag="REPUESTO RETIRADO"
              :codigo-ot="codigoOt"
              :disabled="readOnly"
              placeholder="Tomar foto del repuesto retirado"
              :required="true"
            />
          </div>

          <!-- Bloque Repuesto Instalado -->
          <div class="p-3 rounded-xl border border-emerald-200/70 dark:border-emerald-900/30 bg-emerald-50/30 dark:bg-emerald-950/10 space-y-2.5">
            <span class="text-[11px] font-black text-emerald-700 dark:text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
              <IconArrowForwardUp class="w-3.5 h-3.5" />
              <span>2. Repuesto Instalado (Nuevo)</span>
            </span>

            <div class="space-y-1">
              <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase">
                Descripción / Pieza Nueva *
              </label>
              <input
                type="text"
                v-model="r.item_instalado"
                :disabled="readOnly"
                placeholder="Ej. Tarjeta Reguladora de Voltaje AVR SX460 original..."
                class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 py-1 text-xs text-slate-800 dark:text-slate-200 focus:border-emerald-500 focus:outline-none"
              />
            </div>

            <div class="space-y-1">
              <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase">
                Serial / Marca Nueva
              </label>
              <input
                type="text"
                v-model="r.serial_instalado"
                :disabled="readOnly"
                placeholder="Ej. Stamford SX460 S/N NEW-7741"
                class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 py-1 text-xs text-slate-800 dark:text-slate-200 focus:border-emerald-500 focus:outline-none font-mono"
              />
            </div>

            <SinglePhotoCapture
              v-model="r.foto_instalado"
              label="Foto Repuesto Instalado *"
              tag="REPUESTO INSTALADO"
              :codigo-ot="codigoOt"
              :disabled="readOnly"
              placeholder="Tomar foto del repuesto instalado"
              :required="true"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { 
  IconExchange, 
  IconPlus, 
  IconTrash, 
  IconArrowBackUp, 
  IconArrowForwardUp, 
  IconBox,
  IconSearch,
  IconX,
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

// Catálogo Oficial LPU enriquecido para componentes y repuestos mayores
const CATALOGO_OFICIAL_REPUESTOS = [
  { nombre: 'Batería 12V / 100Ah VRLA AGM (ME PW)', categoria: 'Energía / Baterías', unidad: 'unidad' },
  { nombre: 'Batería 2V / 500Ah OPzV Estacionaria (ME PW)', categoria: 'Energía / Baterías', unidad: 'unidad' },
  { nombre: 'Módulo Rectificador 48V / 50A (ME PW)', categoria: 'Fuerza DC', unidad: 'unidad' },
  { nombre: 'Tarjeta Reguladora de Voltaje AVR SX460 (ME GE/ATS)', categoria: 'Plantas GE', unidad: 'unidad' },
  { nombre: 'Bomba de Agua Perkins / Selmec 40SC (ME GE/ATS)', categoria: 'Plantas GE', unidad: 'unidad' },
  { nombre: 'Compresor Scroll 24K BTU 220V (ME/MC AA)', categoria: 'Climatización AA', unidad: 'unidad' },
  { nombre: 'Filtro Deshidratador 3/8 Soldable (ME/MC AA)', categoria: 'Climatización AA', unidad: 'unidad' },
  { nombre: 'Filtro de Aceite LF16015 Fleetguard (ME GE/ATS)', categoria: 'Plantas GE', unidad: 'unidad' },
  { nombre: 'Filtro Separador de Combustible FS1242 (ME GE/ATS)', categoria: 'Plantas GE', unidad: 'unidad' },
  { nombre: 'Interruptor Termomagnético Breaker 2x30A (ME MT-SE)', categoria: 'Subestación / MT', unidad: 'unidad' },
  { nombre: 'Kit Anclajes y Pernería A325 Alta Resistencia (ME ALTURA)', categoria: 'Torre / Alturas', unidad: 'unidad' },
  { nombre: 'Abrazadera Acero Inoxidable 2" - 4" (ME ALTURA)', categoria: 'Torre / Alturas', unidad: 'unidad' },
  { nombre: 'Gas Refrigerante R410A Ecológico (ME/MC AA)', categoria: 'Climatización AA', unidad: 'kg' },
  { nombre: 'Aceite Lubricante 15W40 CI-4 (ME GE/ATS)', categoria: 'Plantas GE', unidad: 'galon' },
  { nombre: 'Cable de Cobre Desnudo 2/0 AWG (Puesta a Tierra)', categoria: 'SPT / Puesta a Tierra', unidad: 'metro' },
  { nombre: 'Cartucho Soldadura Exotérmica Cadweld 90g', categoria: 'SPT / Puesta a Tierra', unidad: 'unidad' }
];

const sugerenciasRepuestos = [
  { short: 'Batería 12V AGM', nombre: 'Batería 12V / 100Ah VRLA AGM (ME PW)', unidad: 'unidad' },
  { short: 'Rectificador 48V', nombre: 'Módulo Rectificador 48V / 50A (ME PW)', unidad: 'unidad' },
  { short: 'Tarjeta AVR SX460', nombre: 'Tarjeta Reguladora de Voltaje AVR SX460 (ME GE/ATS)', unidad: 'unidad' },
  { short: 'Bomba Agua Selmec', nombre: 'Bomba de Agua Perkins / Selmec 40SC (ME GE/ATS)', unidad: 'unidad' },
  { short: 'Compresor 24K BTU', nombre: 'Compresor Scroll 24K BTU 220V (ME/MC AA)', unidad: 'unidad' },
  { short: 'Filtro Aceite GE', nombre: 'Filtro de Aceite LF16015 Fleetguard (ME GE/ATS)', unidad: 'unidad' }
];

const filteredCatalogo = computed(() => {
  const q = busqueda.value.toLowerCase().trim();
  if (!q) return CATALOGO_OFICIAL_REPUESTOS;
  return CATALOGO_OFICIAL_REPUESTOS.filter(cat => 
    cat.nombre.toLowerCase().includes(q) || 
    cat.categoria.toLowerCase().includes(q)
  );
});

const hasExactMatch = computed(() => {
  const q = busqueda.value.toLowerCase().trim();
  if (!q) return false;
  return CATALOGO_OFICIAL_REPUESTOS.some(cat => cat.nombre.toLowerCase() === q);
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
  if (n.includes('galón') || n.includes('galon') || n.includes('aceite')) return 'galon';
  if (n.includes('metro') || n.includes('cable')) return 'metro';
  if (n.includes('kg') || n.includes('gas') || n.includes('r410a')) return 'kg';
  if (n.includes('kit')) return 'kit';
  if (n.includes('juego')) return 'juego';
  return 'unidad';
};

const focarBuscador = () => {
  isOpen.value = true;
  if (searchInputRef.value) {
    searchInputRef.value.focus();
  }
};

const seleccionarDelCatalogo = (cat) => {
  agregarRepuestoDirecto(cat.nombre, cat.unidad);
};

const agregarRepuestoDirecto = (nombre, unidad = null) => {
  const finalUnit = unidad || detectUnit(nombre);
  const current = [...items.value];
  current.push({
    item_retirado: `${nombre} (Averiado/Retirado)`,
    serial_retirado: '',
    foto_retirado: '',
    item_instalado: nombre,
    serial_instalado: '',
    foto_instalado: '',
    cantidad: 1,
    unidad_medida: finalUnit
  });
  emit('update:modelValue', current);
  busqueda.value = '';
  isOpen.value = false;
};

const agregarDesdeBusqueda = () => {
  const query = busqueda.value.trim();
  if (!query) return;
  agregarRepuestoDirecto(query);
};

const eliminarRepuesto = (idx) => {
  const current = [...items.value];
  current.splice(idx, 1);
  emit('update:modelValue', current);
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

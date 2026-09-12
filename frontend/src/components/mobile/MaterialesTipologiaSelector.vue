<template>
  <div class="space-y-4" ref="containerRef">
    <!-- CABECERA Y SELECCIÓN DE TIPOLOGÍA -->
    <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 shadow-xs">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-neutral-100 dark:border-white/5 pb-3">
        <div class="flex items-center gap-2.5">
          <div class="w-9 h-9 rounded-xl bg-amber-50 dark:bg-amber-950/60 border border-amber-200 dark:border-amber-800/60 text-amber-600 dark:text-amber-400 flex items-center justify-center shrink-0">
            <component :is="getTipologiaIcon(tipologiaActiva.numero)" class="w-5 h-5 stroke-[2]" />
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="font-black text-xs uppercase tracking-wider text-neutral-900 dark:text-white">
                Tipología {{ tipologiaActiva.numero }}: {{ tipologiaActiva.nombre_corto }}
              </span>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-amber-100 dark:bg-amber-900/40 text-amber-800 dark:text-amber-300 font-bold">
                Estándar LPU
              </span>
            </div>
            <p class="text-[11px] text-neutral-500 dark:text-neutral-400 font-medium mt-0.5">
              {{ tipologiaActiva.nombre_completo }}
            </p>
          </div>
        </div>

        <!-- Indicador de ítems reportados -->
        <div class="flex items-center gap-2 self-start sm:self-center">
          <span 
            class="text-[11px] font-mono font-bold px-3 py-1 rounded-xl transition-all flex items-center gap-1.5"
            :class="itemsReportadosCount > 0 
              ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20' 
              : 'bg-neutral-100 dark:bg-neutral-800 text-neutral-500'"
          >
            <IconCheck v-if="itemsReportadosCount > 0" class="w-3.5 h-3.5 stroke-[3]" />
            <span>{{ itemsReportadosCount }} {{ itemsReportadosCount === 1 ? 'ítem a reportar' : 'ítems a reportar' }}</span>
          </span>
        </div>
      </div>

      <!-- Nota explicativa amigable para campo -->
      <div class="mt-3 flex items-start gap-2 text-[11px] text-neutral-500 dark:text-neutral-400 bg-neutral-50 dark:bg-[#0a0b10] p-2.5 rounded-xl border border-neutral-200/60 dark:border-white/5">
        <IconAlertCircle class="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
        <div>
          <span class="font-bold text-neutral-700 dark:text-neutral-300">Instrucción de campo: </span>
          <span>Ingrese la cantidad de los materiales o actividades ejecutadas en sitio. Los ítems en 0 o vacíos no se guardarán en el reporte final.</span>
        </div>
      </div>

      <!-- BARRA DE BÚSQUEDA Y FILTROS TÁCTILES -->
      <div class="mt-3 space-y-2.5">
        <!-- Buscador -->
        <div class="relative flex items-center">
          <IconSearch class="w-4 h-4 text-neutral-400 absolute left-3 pointer-events-none stroke-[2]" />
          <input
            type="text"
            v-model="filtroTexto"
            placeholder="Buscar por nombre, código SAP (ej. 3046179) o palabra clave..."
            class="w-full h-10 rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] pl-9 pr-10 py-1.5 text-xs text-neutral-800 dark:text-neutral-200 placeholder:text-neutral-400 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 transition-all shadow-xs"
          />
          <button
            v-if="filtroTexto"
            type="button"
            @click="filtroTexto = ''"
            class="absolute right-2.5 text-neutral-400 hover:text-neutral-600 dark:hover:text-white p-1"
          >
            <IconX class="w-4 h-4 stroke-[2]" />
          </button>
        </div>

        <!-- Filtros en pastillas táctiles (scroll horizontal en móvil) -->
        <div class="flex items-center gap-1.5 overflow-x-auto pb-1 custom-scrollbar">
          <button
            type="button"
            @click="categoriaFiltro = 'todos'"
            class="px-2.5 py-1 rounded-lg text-[10px] font-bold shrink-0 transition-all cursor-pointer flex items-center gap-1"
            :class="categoriaFiltro === 'todos' 
              ? 'bg-neutral-900 dark:bg-white text-white dark:text-neutral-900 shadow-xs' 
              : 'bg-neutral-100 dark:bg-white/5 text-neutral-600 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-white/10'"
          >
            <span>Todos</span>
            <span class="opacity-70 font-mono">({{ itemsFiltradosBase.length }})</span>
          </button>

          <button
            type="button"
            @click="categoriaFiltro = 'con_cantidad'"
            class="px-2.5 py-1 rounded-lg text-[10px] font-bold shrink-0 transition-all cursor-pointer flex items-center gap-1"
            :class="categoriaFiltro === 'con_cantidad' 
              ? 'bg-emerald-600 text-white shadow-xs' 
              : 'bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800/60'"
          >
            <IconCheck class="w-3 h-3 stroke-[3]" />
            <span>Con Cantidad</span>
            <span class="font-mono">({{ itemsReportadosCount }})</span>
          </button>

          <button
            type="button"
            @click="categoriaFiltro = 'material'"
            class="px-2.5 py-1 rounded-lg text-[10px] font-bold shrink-0 transition-all cursor-pointer flex items-center gap-1"
            :class="categoriaFiltro === 'material' 
              ? 'bg-amber-600 text-white shadow-xs' 
              : 'bg-neutral-100 dark:bg-white/5 text-neutral-600 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-white/10'"
          >
            <span>Materiales (MT/MF)</span>
            <span class="opacity-70 font-mono">({{ countPorTipo('Material') }})</span>
          </button>

          <button
            type="button"
            @click="categoriaFiltro = 'mano_obra'"
            class="px-2.5 py-1 rounded-lg text-[10px] font-bold shrink-0 transition-all cursor-pointer flex items-center gap-1"
            :class="categoriaFiltro === 'mano_obra' 
              ? 'bg-indigo-600 text-white shadow-xs' 
              : 'bg-neutral-100 dark:bg-white/5 text-neutral-600 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-white/10'"
          >
            <span>Mano de Obra (MO/SRV)</span>
            <span class="opacity-70 font-mono">({{ countPorTipo('Mano de Obra') }})</span>
          </button>
        </div>
      </div>
    </div>

    <!-- LISTADO DE MATERIALES E ÍTEMS DE LA TIPOLOGÍA -->
    <div class="space-y-2.5">
      <div v-if="itemsMostrados.length === 0" class="bg-white dark:bg-[#121215] border border-dashed border-neutral-200 dark:border-white/10 rounded-2xl p-6 text-center space-y-2">
        <IconBox class="w-8 h-8 text-neutral-400 mx-auto stroke-[1.5]" />
        <div class="text-xs font-bold text-neutral-700 dark:text-neutral-300">
          No se encontraron ítems con el filtro actual
        </div>
        <p class="text-[11px] text-neutral-400 max-w-xs mx-auto">
          Intente con otra palabra de búsqueda o seleccione el filtro "Todos".
        </p>
        <button
          v-if="filtroTexto || categoriaFiltro !== 'todos'"
          type="button"
          @click="resetFiltros"
          class="inline-flex items-center gap-1 text-[11px] font-bold text-amber-600 dark:text-amber-400 hover:underline pt-1"
        >
          <span>Restablecer filtros</span>
        </button>
      </div>

      <!-- Tarjeta por cada ítem (Diseñada para celular) -->
      <div
        v-for="item in itemsMostrados"
        :key="getItemKey(item)"
        class="bg-white dark:bg-[#121215] border rounded-2xl p-3.5 transition-all shadow-xs"
        :class="getCantidad(item) > 0 
          ? 'border-emerald-500/60 dark:border-emerald-500/50 bg-emerald-50/20 dark:bg-emerald-950/20 ring-1 ring-emerald-500/30' 
          : 'border-neutral-200 dark:border-white/10 hover:border-neutral-300 dark:hover:border-white/20'"
      >
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <!-- Información del ítem -->
          <div class="min-w-0 flex-1 space-y-1">
            <div class="flex items-center gap-2 flex-wrap">
              <!-- Código SAP -->
              <span 
                v-if="item.codigo_sap"
                class="text-[10px] font-mono font-black px-2 py-0.5 rounded-md bg-neutral-100 dark:bg-white/10 text-neutral-800 dark:text-neutral-200 border border-neutral-200 dark:border-white/10"
              >
                SAP: {{ item.codigo_sap }}
              </span>

              <!-- Badge de Tipo (Material vs Mano de Obra) -->
              <span 
                class="text-[9px] uppercase font-black px-2 py-0.5 rounded-md"
                :class="item.tipo === 'Material' 
                  ? 'bg-amber-100 dark:bg-amber-900/40 text-amber-700 dark:text-amber-300' 
                  : 'bg-indigo-100 dark:bg-indigo-900/40 text-indigo-700 dark:text-indigo-300'"
              >
                {{ item.tipo }}
              </span>

              <!-- Unidad de medida -->
              <span class="text-[10px] font-mono text-neutral-500 dark:text-neutral-400">
                Unidad: <strong class="text-neutral-700 dark:text-neutral-300">{{ item.unidad }}</strong>
              </span>

              <!-- Indicador de seleccionado si cantidad > 0 -->
              <span 
                v-if="getCantidad(item) > 0"
                class="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-0.5 ml-auto"
              >
                <IconCheck class="w-3.5 h-3.5 stroke-[3]" />
                <span>Incluido</span>
              </span>
            </div>

            <!-- Nombre / Texto SAP -->
            <div class="font-bold text-xs text-neutral-900 dark:text-white leading-snug">
              {{ item.texto_sap }}
            </div>

            <!-- Alcance colapsable si difiere del texto -->
            <div v-if="item.alcance && item.alcance !== item.texto_sap" class="pt-0.5">
              <button
                type="button"
                @click="toggleAlcance(getItemKey(item))"
                class="text-[10px] text-neutral-500 dark:text-neutral-400 hover:text-amber-600 dark:hover:text-amber-400 flex items-center gap-1 font-medium transition-colors"
              >
                <span>{{ alcancesAbiertos[getItemKey(item)] ? 'Ocultar alcance técnico' : 'Ver alcance técnico...' }}</span>
                <IconChevronDown class="w-3 h-3 transition-transform" :class="{ 'rotate-180': alcancesAbiertos[getItemKey(item)] }" />
              </button>
              <div 
                v-if="alcancesAbiertos[getItemKey(item)]"
                class="mt-1 text-[11px] text-neutral-600 dark:text-neutral-300 bg-neutral-50 dark:bg-black/30 p-2 rounded-lg border border-neutral-200/50 dark:border-white/5 leading-relaxed"
              >
                {{ item.alcance }}
              </div>
            </div>
          </div>

          <!-- CONTROLES TÁCTILES DE CANTIDAD (Optimizados para pulgares) -->
          <div class="flex items-center justify-end gap-2 shrink-0 pt-2 sm:pt-0 border-t sm:border-t-0 border-neutral-100 dark:border-white/5">
            <div class="flex items-center bg-neutral-50 dark:bg-[#0a0b10] border border-neutral-200 dark:border-white/10 rounded-xl p-1 shadow-2xs">
              <!-- Botón Menos (-) -->
              <button
                type="button"
                @click="decrementarCantidad(item)"
                :disabled="readOnly || getCantidad(item) <= 0"
                class="w-9 h-9 rounded-lg flex items-center justify-center font-black text-sm transition-all active:scale-90"
                :class="getCantidad(item) > 0 
                  ? 'bg-neutral-200 dark:bg-white/10 text-neutral-800 dark:text-white hover:bg-rose-100 hover:text-rose-600 cursor-pointer' 
                  : 'text-neutral-300 dark:text-neutral-700 opacity-40 cursor-not-allowed'"
                title="Disminuir"
              >
                <IconMinus class="w-4 h-4 stroke-[2.5]" />
              </button>

              <!-- Input directo de cantidad -->
              <input
                type="number"
                min="0"
                step="any"
                inputmode="decimal"
                :disabled="readOnly"
                :value="getCantidadInput(item)"
                @input="handleInputCantidad(item, $event)"
                @focus="$event.target.select()"
                placeholder="0"
                class="w-14 h-9 text-center font-mono font-black text-xs bg-transparent text-neutral-900 dark:text-white outline-none"
              />

              <!-- Botón Más (+) -->
              <button
                type="button"
                @click="incrementarCantidad(item)"
                :disabled="readOnly"
                class="w-9 h-9 rounded-lg bg-neutral-200 dark:bg-white/10 text-neutral-800 dark:text-white hover:bg-emerald-100 dark:hover:bg-emerald-950 hover:text-emerald-600 flex items-center justify-center font-black text-sm transition-all active:scale-90 cursor-pointer"
                title="Aumentar"
              >
                <IconPlus class="w-4 h-4 stroke-[2.5]" />
              </button>
            </div>

            <!-- Botón de limpieza rápida si tiene cantidad -->
            <button
              v-if="!readOnly && getCantidad(item) > 0"
              type="button"
              @click="limpiarCantidad(item)"
              class="text-neutral-400 hover:text-rose-600 dark:hover:text-rose-400 p-1.5 rounded-lg hover:bg-rose-50 dark:hover:bg-rose-950/40 transition-colors"
              title="Poner en 0"
            >
              <IconTrash class="w-4 h-4 stroke-[2]" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- AGREGAR ÍTEM MANUAL NO LISTADO (Excepciones de campo) -->
    <div v-if="!readOnly" class="bg-white dark:bg-[#121215] border border-dashed border-neutral-200 dark:border-white/10 rounded-2xl p-3.5">
      <div v-if="!mostrandoFormManual">
        <button
          type="button"
          @click="mostrandoFormManual = true"
          class="w-full py-2.5 px-3 rounded-xl bg-neutral-50 dark:bg-white/5 hover:bg-neutral-100 dark:hover:bg-white/10 text-neutral-700 dark:text-neutral-300 font-bold text-xs flex items-center justify-center gap-2 transition-all cursor-pointer"
        >
          <IconPlus class="w-4 h-4 text-amber-500 stroke-[2.5]" />
          <span>¿Usó algún material o insumo no listado en la tipología? Agregar manual</span>
        </button>
      </div>

      <div v-else class="space-y-3">
        <div class="flex items-center justify-between border-b border-neutral-100 dark:border-white/5 pb-2">
          <span class="font-bold text-xs text-neutral-800 dark:text-neutral-200">
            Agregar Ítem Fuera de Catálogo
          </span>
          <button
            type="button"
            @click="mostrandoFormManual = false"
            class="text-neutral-400 hover:text-neutral-600 text-xs p-1"
          >
            <IconX class="w-4 h-4 stroke-[2]" />
          </button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-4 gap-2.5">
          <div class="sm:col-span-2">
            <label class="block text-[10px] font-bold text-neutral-500 uppercase mb-1">Descripción del Ítem *</label>
            <input
              type="text"
              v-model="manualItem.texto_sap"
              placeholder="Ej. Cinta Aislante 3M, Terminal, Breaker 2x30A..."
              class="w-full h-9 rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 text-xs outline-none focus:border-amber-500"
            />
          </div>

          <div>
            <label class="block text-[10px] font-bold text-neutral-500 uppercase mb-1">Código SAP (opcional)</label>
            <input
              type="text"
              v-model="manualItem.codigo_sap"
              placeholder="Ej. 3045000"
              class="w-full h-9 rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 text-xs outline-none focus:border-amber-500 font-mono"
            />
          </div>

          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block text-[10px] font-bold text-neutral-500 uppercase mb-1">Unidad</label>
              <select
                v-model="manualItem.unidad"
                class="w-full h-9 rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-2 text-xs outline-none font-bold"
              >
                <option value="UNIDAD">UNIDAD</option>
                <option value="ML">ML</option>
                <option value="GL">GL</option>
                <option value="KG">KG</option>
                <option value="LB">LB</option>
                <option value="VIAJE">VIAJE</option>
              </select>
            </div>
            <div>
              <label class="block text-[10px] font-bold text-neutral-500 uppercase mb-1">Cantidad *</label>
              <input
                type="number"
                min="0.1"
                step="any"
                v-model.number="manualItem.cantidad"
                placeholder="1"
                class="w-full h-9 rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-2 text-center text-xs font-mono font-bold outline-none focus:border-amber-500"
              />
            </div>
          </div>
        </div>

        <div class="flex justify-end gap-2 pt-1">
          <button
            type="button"
            @click="mostrandoFormManual = false"
            class="px-3 py-1.5 rounded-xl text-xs font-bold text-neutral-500 hover:bg-neutral-100 dark:hover:bg-white/5"
          >
            Cancelar
          </button>
          <button
            type="button"
            @click="guardarItemManual"
            :disabled="!manualItem.texto_sap.trim() || manualItem.cantidad <= 0"
            class="px-4 py-1.5 rounded-xl text-xs font-bold bg-amber-600 hover:bg-amber-500 text-white disabled:opacity-50 transition-all cursor-pointer flex items-center gap-1"
          >
            <IconPlus class="w-3.5 h-3.5 stroke-[3]" />
            <span>Agregar al reporte</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, reactive, onMounted } from 'vue';
import { 
  getTipologiaKeyFromSubsistema, 
  getTipologiaData 
} from '@/utils/catalogoTipologias';
import { 
  IconBox, 
  IconPlus, 
  IconMinus, 
  IconX, 
  IconTrash, 
  IconSearch, 
  IconCheck,
  IconAlertCircle,
  IconChevronDown,
  IconBolt,
  IconEngine,
  IconWind,
  IconTools
} from '@tabler/icons-vue';

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  subsistema: {
    type: String,
    default: 'PE - GRUPO ELECTROGENO'
  },
  readOnly: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue']);

// Mapa reactivo de cantidades: { [itemKey]: Number }
const cantidades = reactive({});

// Lista de ítems adicionales manuales
const itemsManuales = ref([]);

// Estado de UI
const filtroTexto = ref('');
const categoriaFiltro = ref('todos'); // 'todos', 'con_cantidad', 'material', 'mano_obra'
const alcancesAbiertos = reactive({});
const mostrandoFormManual = ref(false);

const manualItem = reactive({
  texto_sap: '',
  codigo_sap: '',
  unidad: 'UNIDAD',
  cantidad: 1,
  tipo: 'Material'
});

// Clave única para cada ítem
const getItemKey = (item) => {
  return item.codigo_sap ? String(item.codigo_sap).trim() : String(item.texto_sap).trim();
};

// Tipología activa deducida de props.subsistema
const tipologiaKey = computed(() => {
  return getTipologiaKeyFromSubsistema(props.subsistema);
});

const tipologiaActiva = computed(() => {
  return getTipologiaData(tipologiaKey.value);
});

// Icono según tipología
const getTipologiaIcon = (num) => {
  switch (Number(num)) {
    case 1: return IconBolt;
    case 2: return IconEngine;
    case 3: return IconWind;
    case 4: return IconBolt;
    case 5: return IconTools;
    default: return IconBox;
  }
};

// Todos los ítems base disponibles (tipología + manuales)
const itemsFiltradosBase = computed(() => {
  const base = tipologiaActiva.value?.items || [];
  return [...base, ...itemsManuales.value];
});

// Contador por tipo
const countPorTipo = (tipo) => {
  return itemsFiltradosBase.value.filter(i => i.tipo === tipo).length;
};

// Ítems mostrados con filtros de búsqueda y categoría
const itemsMostrados = computed(() => {
  let list = itemsFiltradosBase.value;

  // Filtro por categoría
  if (categoriaFiltro.value === 'con_cantidad') {
    list = list.filter(i => getCantidad(i) > 0);
  } else if (categoriaFiltro.value === 'material') {
    list = list.filter(i => i.tipo === 'Material');
  } else if (categoriaFiltro.value === 'mano_obra') {
    list = list.filter(i => i.tipo === 'Mano de Obra');
  }

  // Filtro por texto / SAP
  const q = filtroTexto.value.toLowerCase().trim();
  if (q) {
    list = list.filter(i => {
      const nom = (i.texto_sap || '').toLowerCase();
      const sap = String(i.codigo_sap || '').toLowerCase();
      const alc = (i.alcance || '').toLowerCase();
      return nom.includes(q) || sap.includes(q) || alc.includes(q);
    });
  }

  return list;
});

// Cantidad actual de un ítem
const getCantidad = (item) => {
  const k = getItemKey(item);
  const val = cantidades[k];
  return Number(val) > 0 ? Number(val) : 0;
};

const getCantidadInput = (item) => {
  const k = getItemKey(item);
  const val = cantidades[k];
  return val !== undefined && val !== null && val !== 0 ? val : '';
};

// Total de ítems con cantidad > 0
const itemsReportadosCount = computed(() => {
  return itemsFiltradosBase.value.filter(i => getCantidad(i) > 0).length;
});

// Manejo de incremento y decremento
const incrementarCantidad = (item) => {
  const k = getItemKey(item);
  const actual = getCantidad(item);
  cantidades[k] = actual + 1;
  emitirCambios();
};

const decrementarCantidad = (item) => {
  const k = getItemKey(item);
  const actual = getCantidad(item);
  if (actual > 1) {
    cantidades[k] = actual - 1;
  } else {
    delete cantidades[k];
  }
  emitirCambios();
};

const handleInputCantidad = (item, event) => {
  const k = getItemKey(item);
  const raw = event.target.value;
  if (raw === '' || raw === null || Number(raw) <= 0) {
    delete cantidades[k];
  } else {
    cantidades[k] = Number(raw);
  }
  emitirCambios();
};

const limpiarCantidad = (item) => {
  const k = getItemKey(item);
  delete cantidades[k];
  emitirCambios();
};

const toggleAlcance = (key) => {
  alcancesAbiertos[key] = !alcancesAbiertos[key];
};

const resetFiltros = () => {
  filtroTexto.value = '';
  categoriaFiltro.value = 'todos';
};

// Agregar ítem manual
const guardarItemManual = () => {
  if (!manualItem.texto_sap.trim() || manualItem.cantidad <= 0) return;
  const nuevo = {
    codigo_sap: manualItem.codigo_sap.trim(),
    texto_sap: manualItem.texto_sap.trim(),
    alcance: manualItem.texto_sap.trim(),
    unidad: manualItem.unidad,
    tipo: manualItem.tipo,
    es_manual: true
  };
  itemsManuales.value.push(nuevo);
  const k = getItemKey(nuevo);
  cantidades[k] = Number(manualItem.cantidad);

  // Reset form manual
  manualItem.texto_sap = '';
  manualItem.codigo_sap = '';
  manualItem.cantidad = 1;
  mostrandoFormManual.value = false;

  emitirCambios();
};

// REGLA FUNDAMENTAL: Solo emitir ítems cuya cantidad sea estrictamente mayor a 0
const emitirCambios = () => {
  const reportados = [];
  const allItems = itemsFiltradosBase.value;

  for (const it of allItems) {
    const k = getItemKey(it);
    const cant = cantidades[k];
    if (Number(cant) > 0) {
      reportados.push({
        codigo_sap: it.codigo_sap || '',
        nombre_item: it.texto_sap,
        descripcion: it.texto_sap,
        alcance: it.alcance || '',
        cantidad: Number(cant),
        unidad_medida: it.unidad || 'UNIDAD',
        unidad: it.unidad || 'UNIDAD',
        tipo: it.tipo || 'Material'
      });
    }
  }

  emit('update:modelValue', reportados);
};

// Sincronizar con modelValue inicial (por si ya venían materiales cargados en la OT)
const sincronizarDesdeModelValue = (arr) => {
  if (!Array.isArray(arr)) return;
  arr.forEach(it => {
    const rawName = it.nombre_item || it.nombre || it.descripcion || '';
    const rawSap = it.codigo_sap ? String(it.codigo_sap).trim() : '';
    const cant = Number(it.cantidad) > 0 ? Number(it.cantidad) : 1;

    // Buscar si ya existe en la tipología por código SAP o nombre
    const encontrado = tipologiaActiva.value?.items?.find(i => 
      (rawSap && String(i.codigo_sap).trim() === rawSap) ||
      (rawName && i.texto_sap.toLowerCase() === rawName.toLowerCase())
    );

    if (encontrado) {
      const k = getItemKey(encontrado);
      cantidades[k] = cant;
    } else if (rawName) {
      // Registrar como ítem manual si no estaba en la tipología
      const manualK = rawSap || rawName;
      if (!itemsManuales.value.some(m => getItemKey(m) === manualK)) {
        itemsManuales.value.push({
          codigo_sap: rawSap,
          texto_sap: rawName,
          alcance: it.alcance || rawName,
          unidad: it.unidad_medida || it.unidad || 'UNIDAD',
          tipo: it.tipo || 'Material',
          es_manual: true
        });
      }
      cantidades[manualK] = cant;
    }
  });
};

watch(() => props.modelValue, (newVal) => {
  if (Array.isArray(newVal) && newVal.length > 0) {
    sincronizarDesdeModelValue(newVal);
  }
}, { immediate: true });

// Al cambiar el subsistema, limpiar filtros de búsqueda
watch(() => props.subsistema, () => {
  filtroTexto.value = '';
  categoriaFiltro.value = 'todos';
  if (Array.isArray(props.modelValue) && props.modelValue.length > 0) {
    sincronizarDesdeModelValue(props.modelValue);
  }
});
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  height: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.4);
  border-radius: 9999px;
}
</style>

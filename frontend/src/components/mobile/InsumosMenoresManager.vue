<template>
  <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-sm transition-colors duration-300">
    <!-- Header -->
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
              {{ items.length }} {{ items.length === 1 ? 'insumo' : 'insumos' }}
            </span>
          </div>
          <p class="text-[11px] text-slate-500 dark:text-slate-400 font-medium mt-0.5">
            Buscador oficial de consumibles con captura obligatoria de foto ANTES y DESPUÉS de su aplicación.
          </p>
        </div>
      </div>

      <button
        v-if="!readOnly"
        type="button"
        @click="abrirSelector"
        class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-extrabold bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 hover:bg-emerald-100 border border-emerald-200 dark:border-emerald-800 transition-all active:scale-95 shadow-xs"
      >
        <IconPlus class="w-3.5 h-3.5 stroke-[2.5]" />
        <span>Agregar Insumo</span>
      </button>
    </div>

    <!-- Buscador / Selector rápido -->
    <div v-if="mostrandoBuscador && !readOnly" class="p-3 bg-slate-50 dark:bg-[#0a0b10] border border-slate-200/90 dark:border-white/10 rounded-xl space-y-2">
      <div class="flex items-center justify-between text-[11px] font-bold text-slate-700 dark:text-slate-300">
        <span>Buscar en Catálogo de Insumos Menores</span>
        <button
          type="button"
          @click="mostrandoBuscador = false"
          class="text-slate-400 hover:text-slate-600 dark:hover:text-white"
        >
          Cerrar
        </button>
      </div>

      <div class="relative">
        <IconSearch class="w-4 h-4 text-slate-400 absolute left-3 top-2.5 pointer-events-none stroke-[2]" />
        <input
          type="text"
          v-model="busqueda"
          placeholder="Buscar insumo (ej. Cinta autofundente, teflón, amarras, silicona, limpiador)..."
          class="w-full h-9 pl-9 pr-3 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 text-xs text-slate-800 dark:text-slate-200 focus:outline-none focus:border-emerald-500"
          @keydown.enter.prevent="agregarDesdeBusqueda"
        />
      </div>

      <!-- Sugerencias rápidas -->
      <div class="flex flex-wrap gap-1.5 pt-1">
        <button
          v-for="s in sugerenciasInsumos"
          :key="s.nombre"
          type="button"
          @click="agregarInsumoDirecto(s.nombre, s.unidad)"
          class="text-[10px] font-semibold bg-white dark:bg-neutral-900 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 text-slate-700 dark:text-slate-300 hover:text-emerald-600 border border-slate-200/80 dark:border-white/10 rounded-md px-2 py-1 transition-all flex items-center gap-1"
        >
          <IconPlus class="w-3 h-3 text-emerald-600" />
          <span>{{ s.nombre }}</span>
        </button>
      </div>

      <button
        v-if="busqueda.trim()"
        type="button"
        @click="agregarDesdeBusqueda"
        class="w-full py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-bold transition-all shadow-xs"
      >
        Agregar "{{ busqueda.trim() }}"
      </button>
    </div>

    <!-- Estado vacío -->
    <div v-if="items.length === 0 && !mostrandoBuscador" class="text-center py-6 px-4 bg-slate-50 dark:bg-[#0a0b10] border border-dashed border-slate-200 dark:border-white/10 rounded-xl space-y-2">
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
        @click="abrirSelector"
        class="mt-2 inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold shadow-sm"
      >
        <IconPlus class="w-3.5 h-3.5 stroke-[2.5]" />
        <span>Registrar Insumo Menor</span>
      </button>
    </div>

    <!-- Lista de insumos registrados con fotos Antes y Después -->
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
            class="text-rose-500 hover:text-rose-700 dark:hover:text-rose-400 p-1 rounded-lg hover:bg-rose-50 dark:hover:bg-rose-950/50 transition-colors"
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
import { ref, computed } from 'vue';
import { IconTools, IconPlus, IconTrash, IconSearch } from '@tabler/icons-vue';
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

const mostrandoBuscador = ref(false);
const busqueda = ref('');

const sugerenciasInsumos = [
  { nombre: 'Cinta autofundente 3M', unidad: 'rollo' },
  { nombre: 'Cinta aislante negra 3M', unidad: 'rollo' },
  { nombre: 'Cinta de teflón 3/4"', unidad: 'rollo' },
  { nombre: 'Amarras plásticas negras 30cm (pack)', unidad: 'paquete' },
  { nombre: 'Limpiador desengrasante dieléctrico', unidad: 'tarro' },
  { nombre: 'Aceite motor 15W40 Mobil Delvac', unidad: 'galon' },
  { nombre: 'Refrigerante 50/50 motor diésel', unidad: 'galon' },
  { nombre: 'Refrigerante ecológico R410A', unidad: 'unidad' },
  { nombre: 'Silicona sellante transparente', unidad: 'unidad' },
  { nombre: 'Terminal de ojo 1/0 a 3/8', unidad: 'unidad' }
];

const abrirSelector = () => {
  mostrandoBuscador.value = true;
  busqueda.value = '';
};

const agregarInsumoDirecto = (nombre, unidad = 'unidad') => {
  const current = [...items.value];
  current.push({
    nombre_item: nombre,
    cantidad: 1,
    unidad_medida: unidad,
    foto_antes: '',
    foto_despues: ''
  });
  emit('update:modelValue', current);
  mostrandoBuscador.value = false;
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
</script>

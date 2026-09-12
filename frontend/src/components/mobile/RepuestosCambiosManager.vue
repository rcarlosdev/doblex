<template>
  <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-sm transition-colors duration-300">
    <!-- Header -->
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
              {{ items.length }} {{ items.length === 1 ? 'cambio' : 'cambios' }}
            </span>
          </div>
          <p class="text-[11px] text-slate-500 dark:text-slate-400 font-medium mt-0.5">
            A medida que reemplace componentes, registre el repuesto retirado vs nuevo instalado y suba su fotografía.
          </p>
        </div>
      </div>

      <button
        v-if="!readOnly"
        type="button"
        @click="agregarRepuesto"
        class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-extrabold bg-blue-50 dark:bg-blue-950/60 text-blue-700 dark:text-blue-300 hover:bg-blue-100 border border-blue-200 dark:border-blue-800 transition-all active:scale-95 shadow-xs"
      >
        <IconPlus class="w-3.5 h-3.5 stroke-[2.5]" />
        <span>Registrar Repuesto</span>
      </button>
    </div>

    <!-- Estado vacío -->
    <div v-if="items.length === 0" class="text-center py-6 px-4 bg-slate-50 dark:bg-[#0a0b10] border border-dashed border-slate-200 dark:border-white/10 rounded-xl space-y-2">
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
        @click="agregarRepuesto"
        class="mt-2 inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-bold shadow-sm"
      >
        <IconPlus class="w-3.5 h-3.5 stroke-[2.5]" />
        <span>Agregar Reemplazo de Repuesto</span>
      </button>
    </div>

    <!-- Lista de repuestos -->
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
            <span class="text-xs font-extrabold text-slate-800 dark:text-slate-200">
              Reemplazo de Repuesto #{{ index + 1 }}
            </span>
          </div>

          <button
            v-if="!readOnly"
            type="button"
            @click="eliminarRepuesto(index)"
            class="text-rose-500 hover:text-rose-700 dark:hover:text-rose-400 p-1 rounded-lg hover:bg-rose-50 dark:hover:bg-rose-950/50 transition-colors"
            title="Eliminar repuesto"
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
              min="1"
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
                placeholder="Ej. Batería 12V 100Ah desgastada..."
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
                placeholder="Ej. Mac Gold S/N 93821"
                class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 py-1 text-xs text-slate-800 dark:text-slate-200 focus:border-rose-500 focus:outline-none"
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
                placeholder="Ej. Batería Willard Titán 1150 CCA nueva..."
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
                placeholder="Ej. Willard S/N W202688"
                class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 py-1 text-xs text-slate-800 dark:text-slate-200 focus:border-emerald-500 focus:outline-none"
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
import { computed } from 'vue';
import { 
  IconExchange, 
  IconPlus, 
  IconTrash, 
  IconBox, 
  IconArrowBackUp, 
  IconArrowForwardUp 
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

const items = computed({
  get: () => props.modelValue || [],
  set: (val) => emit('update:modelValue', val)
});

const agregarRepuesto = () => {
  const current = [...items.value];
  current.push({
    item_retirado: '',
    serial_retirado: '',
    foto_retirado: '',
    item_instalado: '',
    serial_instalado: '',
    foto_instalado: '',
    cantidad: 1,
    unidad_medida: 'unidad'
  });
  emit('update:modelValue', current);
};

const eliminarRepuesto = (idx) => {
  const current = [...items.value];
  current.splice(idx, 1);
  emit('update:modelValue', current);
};
</script>

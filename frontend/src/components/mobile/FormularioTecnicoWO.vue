<script setup>
import { reactive, watch } from 'vue';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { 
  IconAlertTriangle, 
  IconTool, 
  IconTruck, 
  IconCheck, 
  IconPackage,
  IconPlus,
  IconTrash,
  IconBox,
  IconBuildingBroadcastTower
} from '@tabler/icons-vue';

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  },
  readOnly: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue']);

const form = reactive({
  // 1. Información General y Estación
  tipo_sitio: 'Urbano',
  subsistema: 'Planta eléctrica',
  presenta_afectacion: 'No',

  // 2. Equipo en Falla y Diagnóstico
  tipo_equipo_falla: 'Planta eléctrica',
  marca_equipo: '',
  modelo_equipo: '',
  reparacion: true,
  reinstalacion: false,
  cambio_equipo: false,
  descripcion_falla: '',
  descripcion_solucion: '',

  // 3. Repuestos retirados e instalados
  repuesto_retirado: {
    descripcion: '',
    marca: '',
    modelo: '',
    serial: ''
  },
  repuesto_instalado: {
    descripcion: '',
    marca: '',
    modelo: '',
    serial: ''
  },

  // 4. Materiales LPU utilizados
  materiales: [],

  // 5. Transporte Especial
  desea_transporte_especial: 'No',
  tipo_transporte: 'Vehículo 4x4',
  distancia_km: null,
  tiempo_desplazamiento: '',
  observacion_transporte: '',

  // 6. Novedades en estación
  se_encontraron_novedades: 'No',
  sistema_novedad: 'Planta eléctrica',
  prioridad_novedad: 'Media',
  descripcion_novedad: '',
  resuelto_en_visita: 'Si',

  // 7. Cierre y Supervisión
  falla_resuelta: 'Si',
  observaciones_actividad: '',
  nombre_supervisor: '',
  ...props.modelValue
});

// Inicializar al menos los sub-objetos si vienen vacíos
if (!form.repuesto_retirado) {
  form.repuesto_retirado = { descripcion: '', marca: '', modelo: '', serial: '' };
}
if (!form.repuesto_instalado) {
  form.repuesto_instalado = { descripcion: '', marca: '', modelo: '', serial: '' };
}
if (!Array.isArray(form.materiales)) {
  form.materiales = [];
}

watch(form, (val) => {
  emit('update:modelValue', { ...val });
}, { deep: true });

// Sincronizar si modelValue cambia externamente (ej. carga desde API)
watch(() => props.modelValue, (newVal) => {
  if (newVal && Object.keys(newVal).length > 0) {
    Object.assign(form, newVal);
    if (!form.repuesto_retirado) form.repuesto_retirado = { descripcion: '', marca: '', modelo: '', serial: '' };
    if (!form.repuesto_instalado) form.repuesto_instalado = { descripcion: '', marca: '', modelo: '', serial: '' };
    if (!Array.isArray(form.materiales)) form.materiales = [];
  }
}, { deep: true });

const addMaterial = () => {
  form.materiales.push({
    descripcion: '',
    unidad: 'Unidad',
    cantidad: 1
  });
};

const removeMaterial = (index) => {
  form.materiales.splice(index, 1);
};
</script>

<template>
  <div class="space-y-5 text-xs select-text">
    <!-- Header de Identificación del Formato Oficial WO -->
    <div class="p-3.5 bg-amber-500/10 border border-amber-500/20 rounded-2xl flex items-center justify-between flex-wrap gap-2">
      <div class="flex items-center gap-2.5">
        <div class="p-2 bg-amber-500/20 text-amber-600 dark:text-amber-400 rounded-xl">
          <IconTool class="w-5 h-5 stroke-[2]" />
        </div>
        <div>
          <h4 class="font-extrabold text-neutral-900 dark:text-white text-xs">
            Formato Técnico: Mantenimiento Correctivo y Emergencias (WO)
          </h4>
          <p class="text-[10px] text-neutral-500 dark:text-neutral-400">
            Formato oficial Claro (Ref. WO0000005558781 - Móvil / Urbano-Rural)
          </p>
        </div>
      </div>
      <Badge variant="outline" class="border-amber-500/30 text-amber-600 dark:text-amber-400 font-bold text-[10px]">
        Correctivo & Emergencia
      </Badge>
    </div>

    <!-- 1. INFORMACIÓN GENERAL Y AFECTACIÓN DE SERVICIOS -->
    <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-3.5 shadow-xs">
      <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
        <IconBuildingBroadcastTower class="w-4 h-4 text-amber-500 stroke-[2]" />
        <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
          1. Información General & Afectación de Servicio
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">
            Tipo de Sitio
          </label>
          <select 
            v-model="form.tipo_sitio" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs focus:ring-1 focus:ring-amber-500 outline-none"
          >
            <option value="Urbano">Urbano</option>
            <option value="Rural">Rural</option>
          </select>
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">
            Subsistema Afectado
          </label>
          <select 
            v-model="form.subsistema" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs focus:ring-1 focus:ring-amber-500 outline-none"
          >
            <option value="Planta eléctrica">Planta eléctrica (GE)</option>
            <option value="Aire acondicionado">Aire acondicionado (HVAC)</option>
            <option value="Fuerza DC / Rectificadores">Fuerza DC / Rectificadores</option>
            <option value="Sistemas Híbridos SFV">Sistemas Híbridos SFV</option>
            <option value="Subestación / Acometida">Subestación / Acometida</option>
            <option value="Torre y Balizamiento">Torre y Balizamiento</option>
            <option value="Infraestructura / Cerramiento">Infraestructura / Cerramiento</option>
          </select>
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">
            ¿Presenta Afectación de Servicios? *
          </label>
          <select 
            v-model="form.presenta_afectacion" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-bold text-xs outline-none"
            :class="form.presenta_afectacion === 'Si' ? 'text-red-600' : 'text-neutral-700 dark:text-neutral-300'"
          >
            <option value="No">No (Sin afectación de tráfico)</option>
            <option value="Si">Sí (Tráfico caído o degradado)</option>
          </select>
        </div>
      </div>
    </div>

    <!-- 2. DIAGNÓSTICO DE FALLA Y SOLUCIÓN TÉCNICA -->
    <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
      <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
        <IconAlertTriangle class="w-4 h-4 text-amber-500 stroke-[2]" />
        <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
          2. Diagnóstico de Falla, Equipo & Solución
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">
            Tipo Equipo en Falla *
          </label>
          <Input v-model="form.tipo_equipo_falla" placeholder="Ej. Planta eléctrica, Motor Diesel" :disabled="readOnly" class="h-9 text-xs" />
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Marca del Equipo</label>
          <Input v-model="form.marca_equipo" placeholder="Ej. Selmec, Cummins, FG Wilson" :disabled="readOnly" class="h-9 text-xs" />
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Modelo / Referencia</label>
          <Input v-model="form.modelo_equipo" placeholder="Ej. 40SC, 30 KVA" :disabled="readOnly" class="h-9 text-xs font-mono" />
        </div>
      </div>

      <!-- Tipo de intervención realizada -->
      <div>
        <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1.5">
          Tipo de Intervención Realizada (Seleccione los que apliquen)
        </label>
        <div class="grid grid-cols-3 gap-2">
          <label class="flex items-center gap-2 p-2.5 rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] cursor-pointer hover:bg-neutral-100 dark:hover:bg-white/5 transition-all">
            <input type="checkbox" v-model="form.reparacion" :disabled="readOnly" class="rounded text-amber-600" />
            <span class="font-bold text-[11px] text-neutral-800 dark:text-neutral-200">Reparación</span>
          </label>
          <label class="flex items-center gap-2 p-2.5 rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] cursor-pointer hover:bg-neutral-100 dark:hover:bg-white/5 transition-all">
            <input type="checkbox" v-model="form.reinstalacion" :disabled="readOnly" class="rounded text-amber-600" />
            <span class="font-bold text-[11px] text-neutral-800 dark:text-neutral-200">Reinstalación</span>
          </label>
          <label class="flex items-center gap-2 p-2.5 rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] cursor-pointer hover:bg-neutral-100 dark:hover:bg-white/5 transition-all">
            <input type="checkbox" v-model="form.cambio_equipo" :disabled="readOnly" class="rounded text-amber-600" />
            <span class="font-bold text-[11px] text-neutral-800 dark:text-neutral-200">Cambio Equipo</span>
          </label>
        </div>
      </div>

      <!-- Descripciones de Falla y Solución -->
      <div class="space-y-3">
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">
            Descripción Detallada de la Falla Encontrada *
          </label>
          <textarea 
            v-model="form.descripcion_falla" 
            :disabled="readOnly"
            rows="2" 
            placeholder="Detalle síntomas, causas de origen y estado al arribar a sitio..."
            class="w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] p-3 text-xs focus:ring-1 focus:ring-amber-500 outline-none leading-relaxed"
          ></textarea>
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">
            Descripción de la Solución Técnica Ejecutada *
          </label>
          <textarea 
            v-model="form.descripcion_solucion" 
            :disabled="readOnly"
            rows="2" 
            placeholder="Detalle los trabajos realizados: reemplazo de piezas, calibración, pruebas en automático con carga y aval con supervisor..."
            class="w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] p-3 text-xs focus:ring-1 focus:ring-amber-500 outline-none leading-relaxed"
          ></textarea>
        </div>
      </div>
    </div>

    <!-- 3. TRAZABILIDAD DE REPUESTOS (RETIRADO VS INSTALADO) -->
    <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
      <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
        <IconPackage class="w-4 h-4 text-blue-500 stroke-[2]" />
        <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
          3. Trazabilidad de Repuestos (Retirado vs Instalado)
        </span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Repuesto Retirado -->
        <div class="p-3.5 bg-red-50/50 dark:bg-red-950/20 border border-red-200/60 dark:border-red-900/30 rounded-xl space-y-2">
          <div class="flex items-center justify-between">
            <span class="font-extrabold text-red-700 dark:text-red-400 text-[11px] uppercase">Repuesto Retirado (Dañado)</span>
            <Badge variant="outline" class="border-red-300 text-red-600 text-[9px] font-bold">Baja</Badge>
          </div>
          <Input v-model="form.repuesto_retirado.descripcion" placeholder="Descripción de la pieza retirada" :disabled="readOnly" class="h-8 text-xs bg-white dark:bg-black/20" />
          <div class="grid grid-cols-3 gap-1.5">
            <Input v-model="form.repuesto_retirado.marca" placeholder="Marca" :disabled="readOnly" class="h-8 text-[11px] bg-white dark:bg-black/20" />
            <Input v-model="form.repuesto_retirado.modelo" placeholder="Modelo" :disabled="readOnly" class="h-8 text-[11px] bg-white dark:bg-black/20" />
            <Input v-model="form.repuesto_retirado.serial" placeholder="Serial" :disabled="readOnly" class="h-8 text-[11px] bg-white dark:bg-black/20 font-mono" />
          </div>
        </div>

        <!-- Repuesto Instalado -->
        <div class="p-3.5 bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-200/60 dark:border-emerald-900/30 rounded-xl space-y-2">
          <div class="flex items-center justify-between">
            <span class="font-extrabold text-emerald-700 dark:text-emerald-400 text-[11px] uppercase">Repuesto Instalado (Nuevo)</span>
            <Badge variant="outline" class="border-emerald-300 text-emerald-600 text-[9px] font-bold">Operativo</Badge>
          </div>
          <Input v-model="form.repuesto_instalado.descripcion" placeholder="Descripción de la pieza nueva" :disabled="readOnly" class="h-8 text-xs bg-white dark:bg-black/20" />
          <div class="grid grid-cols-3 gap-1.5">
            <Input v-model="form.repuesto_instalado.marca" placeholder="Marca" :disabled="readOnly" class="h-8 text-[11px] bg-white dark:bg-black/20" />
            <Input v-model="form.repuesto_instalado.modelo" placeholder="Modelo" :disabled="readOnly" class="h-8 text-[11px] bg-white dark:bg-black/20" />
            <Input v-model="form.repuesto_instalado.serial" placeholder="Serial" :disabled="readOnly" class="h-8 text-[11px] bg-white dark:bg-black/20 font-mono" />
          </div>
        </div>
      </div>
    </div>

    <!-- 4. LISTADO DE MATERIALES UTILIZADOS EN LA ACTIVIDAD -->
    <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-3.5 shadow-xs">
      <div class="flex items-center justify-between border-b border-neutral-100 dark:border-white/5 pb-2.5">
        <div class="flex items-center gap-2">
          <IconBox class="w-4 h-4 text-amber-500 stroke-[2]" />
          <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
            4. Materiales e Insumos Menores Utilizados
          </span>
        </div>
        <button
          v-if="!readOnly"
          type="button"
          @click="addMaterial"
          class="inline-flex items-center gap-1 text-[11px] font-bold text-amber-700 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800/60 px-2.5 py-1 rounded-xl hover:bg-amber-100 transition-all active:scale-95 cursor-pointer"
        >
          <IconPlus class="w-3.5 h-3.5 stroke-[2.5]" />
          <span>Agregar Material</span>
        </button>
      </div>

      <div v-if="form.materiales.length === 0" class="text-center py-4 text-slate-400 dark:text-slate-500 text-[11px] border border-dashed border-neutral-200 dark:border-white/10 rounded-xl">
        Sin materiales menores registrados para esta actividad.
      </div>

      <div v-else class="space-y-2">
        <div 
          v-for="(mat, idx) in form.materiales" 
          :key="idx" 
          class="grid grid-cols-1 sm:grid-cols-12 gap-2 items-center p-2.5 rounded-xl bg-neutral-50 dark:bg-[#0a0b10] border border-neutral-200/80 dark:border-white/5"
        >
          <div class="sm:col-span-6">
            <Input v-model="mat.descripcion" placeholder="Descripción del material (ej. Refrigerante, Cinta vulcanizada)" :disabled="readOnly" class="h-8 text-xs" />
          </div>
          <div class="sm:col-span-3">
            <select 
              v-model="mat.unidad" 
              :disabled="readOnly"
              class="h-8 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-white dark:bg-black/20 px-2 font-medium text-xs outline-none"
            >
              <option value="Unidad">Unidad (UND)</option>
              <option value="Galón">Galón</option>
              <option value="Metro">Metro</option>
              <option value="Kg">Kg</option>
              <option value="Rollo">Rollo</option>
              <option value="Litro">Litro</option>
            </select>
          </div>
          <div class="sm:col-span-2">
            <Input type="number" step="0.5" min="0.1" v-model="mat.cantidad" placeholder="Cant." :disabled="readOnly" class="h-8 text-xs font-bold" />
          </div>
          <div v-if="!readOnly" class="sm:col-span-1 flex justify-end">
            <button 
              type="button" 
              @click="removeMaterial(idx)"
              class="p-1.5 text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-950/50 rounded-lg transition-all cursor-pointer"
            >
              <IconTrash class="w-4 h-4 stroke-[2]" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 5. REGISTRO DE TRANSPORTE ESPECIAL (SI APLICA) -->
    <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
      <div class="flex items-center justify-between border-b border-neutral-100 dark:border-white/5 pb-2.5">
        <div class="flex items-center gap-2">
          <IconTruck class="w-4 h-4 text-purple-500 stroke-[2]" />
          <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
            5. Registro de Transporte Especial (LPU)
          </span>
        </div>
        <select 
          v-model="form.desea_transporte_especial" 
          :disabled="readOnly"
          class="h-8 rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-2.5 text-xs font-bold text-purple-600 outline-none"
        >
          <option value="No">No requirió transporte especial</option>
          <option value="Si">Sí requirió transporte especial</option>
        </select>
      </div>

      <div v-if="form.desea_transporte_especial === 'Si'" class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Tipo de Transporte</label>
          <select 
            v-model="form.tipo_transporte" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs outline-none"
          >
            <option value="Vehículo 4x4">Vehículo 4x4 Campero</option>
            <option value="Lancha Fluvial">Lancha Fluvial / Canoa</option>
            <option value="Mular / Bestia">Mular / Bestia de Carga</option>
            <option value="Caminata / Ayudantía">Caminata / Ayudantía en Hombro</option>
            <option value="Aéreo">Aéreo / Helicóptero</option>
            <option value="Otro">Otro medio especial</option>
          </select>
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Distancia Recorrida (Km)</label>
          <Input type="number" step="0.1" v-model="form.distancia_km" placeholder="Ej. 25.5" :disabled="readOnly" class="h-9 text-xs" />
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Tiempo de Desplazamiento</label>
          <Input v-model="form.tiempo_desplazamiento" placeholder="Ej. 2h 15min" :disabled="readOnly" class="h-9 text-xs" />
        </div>
        <div class="sm:col-span-3">
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Observaciones de Transporte</label>
          <Input v-model="form.observacion_transporte" placeholder="Detalle estado de la trocha, caudal del río o transbordos realizados..." :disabled="readOnly" class="h-9 text-xs" />
        </div>
      </div>
    </div>

    <!-- 6. NOVEDADES Y HALLAZGOS EN LA ESTACIÓN -->
    <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
      <div class="flex items-center justify-between border-b border-neutral-100 dark:border-white/5 pb-2.5">
        <div class="flex items-center gap-2">
          <IconAlertTriangle class="w-4 h-4 text-rose-500 stroke-[2]" />
          <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
            6. Novedades y Hallazgos en Estación
          </span>
        </div>
        <select 
          v-model="form.se_encontraron_novedades" 
          :disabled="readOnly"
          class="h-8 rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-2.5 text-xs font-bold outline-none"
          :class="form.se_encontraron_novedades === 'Si' ? 'text-rose-600' : 'text-slate-600 dark:text-slate-400'"
        >
          <option value="No">No se encontraron novedades</option>
          <option value="Si">Sí se encontraron novedades</option>
        </select>
      </div>

      <div v-if="form.se_encontraron_novedades === 'Si'" class="grid grid-cols-1 sm:grid-cols-3 gap-3 p-3.5 bg-rose-50/50 dark:bg-rose-950/20 border border-rose-200/60 dark:border-rose-900/30 rounded-xl">
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Sistema Afectado</label>
          <select 
            v-model="form.sistema_novedad" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-white dark:bg-[#0a0b10] px-3 font-medium text-xs outline-none"
          >
            <option value="Planta eléctrica">Planta eléctrica</option>
            <option value="Aire acondicionado">Aire acondicionado</option>
            <option value="Cerramiento y Balizamiento">Cerramiento y Balizamiento</option>
            <option value="Torre / Obra Civil">Torre / Obra Civil</option>
            <option value="Subestación / Red Comercial">Subestación / Red Comercial</option>
            <option value="Baterías y Rectificador">Baterías y Rectificador</option>
          </select>
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Prioridad del Hallazgo</label>
          <select 
            v-model="form.prioridad_novedad" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-white dark:bg-[#0a0b10] px-3 font-bold text-xs outline-none"
            :class="form.prioridad_novedad === 'Alta' ? 'text-red-600' : form.prioridad_novedad === 'Media' ? 'text-amber-600' : 'text-blue-600'"
          >
            <option value="Alta">Alta (Riesgo inminente de corte)</option>
            <option value="Media">Media (Desgaste preventivo)</option>
            <option value="Baja">Baja (Mejora estética/menor)</option>
          </select>
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">¿Resuelto en la Visita?</label>
          <select 
            v-model="form.resuelto_en_visita" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-white dark:bg-[#0a0b10] px-3 font-medium text-xs outline-none"
          >
            <option value="Si">Sí (Solucionado en sitio)</option>
            <option value="No">No (Requiere nuevo reporte)</option>
          </select>
        </div>

        <div class="sm:col-span-3">
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Descripción de la Novedad / Hallazgo</label>
          <textarea 
            v-model="form.descripcion_novedad" 
            :disabled="readOnly"
            rows="2" 
            placeholder="Detalle los hallazgos que ponen en riesgo el servicio del sitio para trámite escalonado..."
            class="w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-white dark:bg-[#0a0b10] p-3 text-xs focus:ring-1 focus:ring-rose-500 outline-none leading-relaxed"
          ></textarea>
        </div>
      </div>
    </div>

    <!-- 7. CIERRE TÉCNICO Y SUPERVISIÓN -->
    <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
      <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
        <IconCheck class="w-4 h-4 text-emerald-500 stroke-[2.5]" />
        <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
          7. Cierre Técnico & Supervisión Claro
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">
            ¿Falla Resuelta a Satisfacción? *
          </label>
          <select 
            v-model="form.falla_resuelta" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-bold text-xs outline-none"
            :class="form.falla_resuelta === 'Si' ? 'text-emerald-600' : 'text-rose-600'"
          >
            <option value="Si">Sí (Equipo en modo automático y sin alarmas)</option>
            <option value="No">No (Requiere segunda intervención o repuesto mayor)</option>
          </select>
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">
            Nombre de Supervisor Claro Notificado
          </label>
          <Input v-model="form.nombre_supervisor" placeholder="Ej. Cleyver Espitia / Ing. de Guardia" :disabled="readOnly" class="h-9 text-xs" />
        </div>

        <div class="sm:col-span-2">
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">
            Observaciones Finales de la Actividad
          </label>
          <textarea 
            v-model="form.observaciones_actividad" 
            :disabled="readOnly"
            rows="2" 
            placeholder="Ej. PE queda en modo automático y sin alarmas. Estación cerrada bajo candado y sitio limpio..."
            class="w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] p-3 text-xs focus:ring-1 focus:ring-primary outline-none leading-relaxed"
          ></textarea>
        </div>
      </div>
    </div>
  </div>
</template>

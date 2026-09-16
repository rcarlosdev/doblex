<script setup>
import { reactive, watch, computed, nextTick } from 'vue';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import PhotoUploader from '@/components/mobile/PhotoUploader.vue';
import MaterialesTipologiaSelector from '@/components/mobile/MaterialesTipologiaSelector.vue';
import { 
  IconAlertTriangle, 
  IconTool, 
  IconTruck, 
  IconCheck, 
  IconPackage,
  IconPlus,
  IconTrash,
  IconBox,
  IconBuildingBroadcastTower,
  IconCamera
} from '@tabler/icons-vue';

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  },
  readOnly: {
    type: Boolean,
    default: false
  },
  tipoActividad: {
    type: String,
    default: ''
  },
  codigoOt: {
    type: String,
    default: ''
  },
  evidencias: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['update:modelValue', 'photo-uploaded', 'delete-photo']);

const form = reactive({
  // 1. Información General y Estación
  tipo_sitio: 'Urbano',
  subsistema: 'PE - GRUPO ELECTROGENO',
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

  // 3. Materiales & Actividades LPU utilizados (Estándar de Tipologías)
  materiales: [],

  // 4. Cierre y Supervisión Claro
  falla_resuelta: 'Si',
  observaciones_actividad: '',
  nombre_supervisor: '',
  ...props.modelValue
});

if (!Array.isArray(form.materiales)) {
  form.materiales = [];
}

const OPCIONES_SUBSISTEMA = [
  'SPT - SISTEMA PUESTA A TIERRA',
  'PE - GRUPO ELECTROGENO',
  'AA - AIRES ACONDICIONADOS',
  'PW - POWER',
  'MT-BT - MEDIA Y BAJA TENSION'
];

const normalizarSubsistema = (val) => {
  if (!val) return 'PE - GRUPO ELECTROGENO';
  const str = String(val).trim();
  const lower = str.toLowerCase();
  if (lower.startsWith('spt') || lower.includes('puesta a tierra') || lower.includes('tierra')) {
    return 'SPT - SISTEMA PUESTA A TIERRA';
  }
  if (lower.startsWith('pe') || lower.includes('planta') || lower.includes('electrogeno') || lower.includes('ge')) {
    return 'PE - GRUPO ELECTROGENO';
  }
  if (lower.startsWith('aa') || lower.includes('aire') || lower.includes('climatiz') || lower.includes('hvac')) {
    return 'AA - AIRES ACONDICIONADOS';
  }
  if (lower.startsWith('pw') || lower.includes('power') || lower.includes('fuerza') || lower.includes('dc') || lower.includes('rectificador')) {
    return 'PW - POWER';
  }
  if (lower.includes('mt') || lower.includes('bt') || lower.includes('media') || lower.includes('baja') || lower.includes('subestacion') || lower.includes('acometida')) {
    return 'MT-BT - MEDIA Y BAJA TENSION';
  }
  return str.toUpperCase();
};

form.subsistema = normalizarSubsistema(form.subsistema);

let isInternalSync = false;

watch(form, (val) => {
  if (isInternalSync) return;
  emit('update:modelValue', { ...val });
}, { deep: true });

// Sincronizar si modelValue cambia externamente (ej. carga desde API)
watch(() => props.modelValue, (newVal) => {
  if (newVal && Object.keys(newVal).length > 0) {
    if (JSON.stringify(newVal) !== JSON.stringify(form)) {
      isInternalSync = true;
      Object.assign(form, newVal);
      form.subsistema = normalizarSubsistema(form.subsistema);
      if (!form.repuesto_retirado) form.repuesto_retirado = { descripcion: '', marca: '', modelo: '', serial: '' };
      if (!form.repuesto_instalado) form.repuesto_instalado = { descripcion: '', marca: '', modelo: '', serial: '' };
      if (!Array.isArray(form.materiales)) form.materiales = [];
      nextTick(() => { isInternalSync = false; });
    }
  }
}, { deep: true });



const tituloActividad = computed(() => {
  const raw = (props.tipoActividad || form.tipo_actividad || '').toLowerCase().trim();
  if (!raw) return 'Correctivo';
  if (raw === 'correctivo') return 'Correctivo';
  if (raw === 'emergencia') return 'Emergencia';
  if (raw.startsWith('preventivo') || raw.includes('rutina') || raw.includes('7x24')) return 'Preventivo';
  if (raw === 'obra_civil') return 'Obra Civil';
  if (raw === 'informe_360' || raw.includes('360')) return 'Informe 360';
  return raw.charAt(0).toUpperCase() + raw.slice(1);
});

const bannerTheme = computed(() => {
  const t = tituloActividad.value.toLowerCase();
  if (t === 'emergencia') {
    return {
      wrapper: 'bg-rose-500/10 border-rose-500/20',
      iconBox: 'bg-rose-500/20 text-rose-600 dark:text-rose-400',
      badge: 'border-rose-500/30 text-rose-600 dark:text-rose-400'
    };
  }
  if (t === 'preventivo') {
    return {
      wrapper: 'bg-blue-500/10 border-blue-500/20',
      iconBox: 'bg-blue-500/20 text-blue-600 dark:text-blue-400',
      badge: 'border-blue-500/30 text-blue-600 dark:text-blue-400'
    };
  }
  return {
    wrapper: 'bg-amber-500/10 border-amber-500/20',
    iconBox: 'bg-amber-500/20 text-amber-600 dark:text-amber-400',
    badge: 'border-amber-500/30 text-amber-600 dark:text-amber-400'
  };
});

const getEvidenciasPorTipo = (tipo) => {
  return (props.evidencias || []).filter(e => e.tipo === tipo);
};
</script>

<template>
  <div class="space-y-5 text-xs select-text">
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
            <option v-for="opc in OPCIONES_SUBSISTEMA" :key="opc" :value="opc">
              {{ opc }}
            </option>
            <option v-if="form.subsistema && !OPCIONES_SUBSISTEMA.includes(form.subsistema)" :value="form.subsistema">
              {{ form.subsistema }}
            </option>
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

      <!-- Evidencias Fotográficas Obligatorias del Formato WO (Antes, Durante y Después) -->
      <div class="pt-3 border-t border-neutral-100 dark:border-white/5 space-y-3">
        <div class="flex items-center gap-1.5 text-neutral-800 dark:text-neutral-200">
          <IconCamera class="w-4 h-4 text-amber-500 stroke-[2]" />
          <span class="font-extrabold text-[11px] uppercase tracking-wider">
            Soportes Fotográficos de la Intervención (Claro WO)
          </span>
        </div>

        <PhotoUploader
          tipo="antes"
          titulo="1. Diagnóstico Inicial & Falla Encontrada"
          descripcion="Fotografía legible del estado del equipo averiado, daño físico o alarma activa en tablero antes de iniciar labores."
          badge-label="Antes (Falla)"
          :codigo-ot="codigoOt"
          :evidencias-list="getEvidenciasPorTipo('antes')"
          :read-only="readOnly"
          @photo-uploaded="emit('photo-uploaded', $event)"
          @delete-photo="emit('delete-photo', $event)"
        />

        <PhotoUploader
          tipo="durante"
          titulo="2. Intervención Técnica & Reparación"
          descripcion="Registro del proceso técnico: desmonte, piezas sustituidas vs repuestos nuevos instalados."
          badge-label="Durante (Reparación)"
          :codigo-ot="codigoOt"
          :evidencias-list="getEvidenciasPorTipo('durante')"
          :read-only="readOnly"
          @photo-uploaded="emit('photo-uploaded', $event)"
          @delete-photo="emit('delete-photo', $event)"
        />

        <PhotoUploader
          tipo="despues"
          titulo="3. Equipo Operativo en Servicio & Cierre"
          descripcion="Equipo solucionado operando en condiciones normales, tablero sin alarmas y pruebas con carga avaladas."
          badge-label="Después (Solucionado)"
          :codigo-ot="codigoOt"
          :evidencias-list="getEvidenciasPorTipo('despues')"
          :read-only="readOnly"
          @photo-uploaded="emit('photo-uploaded', $event)"
          @delete-photo="emit('delete-photo', $event)"
        />
      </div>
    </div>

    <!-- 3. MATERIALES E INSUMOS LPU UTILIZADOS (ESTÁNDAR TIPOLOGÍAS) -->
    <div class="space-y-3">
      <div class="flex items-center gap-2 px-1">
        <IconBox class="w-4 h-4 text-amber-500 stroke-[2.2]" />
        <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
          3. Materiales & Actividades LPU Reportados en Campo
        </span>
      </div>

      <MaterialesTipologiaSelector
        v-model="form.materiales"
        :subsistema="form.subsistema"
        :read-only="readOnly"
      />
    </div>

    <!-- 4. CIERRE TÉCNICO Y SUPERVISIÓN -->
    <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
      <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
        <IconCheck class="w-4 h-4 text-emerald-500 stroke-[2.5]" />
        <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
          4. Cierre Técnico & Supervisión Claro
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

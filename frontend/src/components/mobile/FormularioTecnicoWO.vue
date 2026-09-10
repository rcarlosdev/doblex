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
  IconTrash
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
  // Información y Falla
  presenta_afectacion: 'No',
  tipo_equipo_falla: 'Planta eléctrica',
  marca_equipo: '',
  modelo_equipo: '',
  reparacion: true,
  reinstalacion: false,
  cambio_equipo: false,
  descripcion_falla: '',
  descripcion_solucion: '',
  // Repuestos retirados e instalados
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
  // Materiales
  materiales: [],
  // Transporte Especial
  desea_transporte_especial: 'No',
  tipo_transporte: 'MULA 2X150',
  distancia_km: null,
  tiempo_desplazamiento: '',
  observacion_transporte: '',
  // Novedades en estación
  se_encontraron_novedades: 'No',
  prioridad_novedad: 'Media',
  descripcion_novedad: '',
  resuelto_en_visita: 'Si',
  // Cierre y Supervisión
  falla_resuelta: 'Si',
  observaciones_actividad: '',
  nombre_supervisor: '',
  ...props.modelValue
});

watch(form, (val) => {
  emit('update:modelValue', { ...val });
}, { deep: true });

const addMaterial = () => {
  form.materiales.push({
    descripcion: '',
    unidad: 'UND',
    cantidad: 1
  });
};

const removeMaterial = (index) => {
  form.materiales.splice(index, 1);
};
</script>

<template>
  <div class="space-y-6 text-xs select-text">
    <!-- Header de identificación del formato -->
    <div class="p-3.5 bg-amber-500/10 border border-amber-500/20 rounded-2xl flex items-center justify-between">
      <div class="flex items-center gap-2">
        <div class="p-2 bg-amber-500/20 text-amber-600 dark:text-amber-400 rounded-xl">
          <IconTool class="w-5 h-5 stroke-[2]" />
        </div>
        <div>
          <h4 class="font-extrabold text-neutral-900 dark:text-white text-xs">
            Formato Técnico: Mantenimiento Correctivo y Emergencias (WO)
          </h4>
          <p class="text-[10px] text-neutral-500 dark:text-neutral-400">
            Alineado con estándar oficial Claro / INMEL (Móvil & Urbano/Rural)
          </p>
        </div>
      </div>
      <Badge variant="outline" class="border-amber-500/30 text-amber-600 dark:text-amber-400 font-bold text-[10px]">
        Correctivo
      </Badge>
    </div>

    <!-- 1. DIAGNÓSTICO Y EQUIPO EN FALLA -->
    <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
      <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
        <IconAlertTriangle class="w-4 h-4 text-amber-500 stroke-[2]" />
        <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
          1. Diagnóstico de Falla y Equipo Intervenido
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">
            ¿Presenta Afectación de Servicios? *
          </label>
          <select 
            v-model="form.presenta_afectacion" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 py-1 font-medium text-xs"
          >
            <option value="No">No (Sin degradación crítica)</option>
            <option value="Si">Sí (Tráfico caído o en riesgo)</option>
          </select>
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">
            Tipo de Equipo en Falla *
          </label>
          <select 
            v-model="form.tipo_equipo_falla" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 py-1 font-medium text-xs"
          >
            <option value="Planta eléctrica">Planta eléctrica (GE)</option>
            <option value="Rectificador">Rectificador / Fuerza DC</option>
            <option value="Banco de Baterías">Banco de Baterías</option>
            <option value="Aire Acondicionado">Aire Acondicionado (HVAC)</option>
            <option value="Transferencia Automática">Transferencia Automática (ATS)</option>
            <option value="Transformador / Acometida">Transformador / Acometida</option>
            <option value="Otro">Otro subsistema</option>
          </select>
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Marca del Equipo</label>
          <Input v-model="form.marca_equipo" placeholder="Ej. Selmec, Cummins, FG Wilson" :disabled="readOnly" class="h-9 text-xs" />
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Modelo / Capacidad</label>
          <Input v-model="form.modelo_equipo" placeholder="Ej. 40SC, 30 KVA" :disabled="readOnly" class="h-9 text-xs" />
        </div>
      </div>

      <!-- Tipo de intervención realizada -->
      <div>
        <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1.5">
          Tipo de Intervención Ejecutada
        </label>
        <div class="grid grid-cols-3 gap-2">
          <label class="flex items-center gap-2 p-2 rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] cursor-pointer">
            <input type="checkbox" v-model="form.reparacion" :disabled="readOnly" class="rounded text-primary" />
            <span class="font-bold text-[11px]">Reparación</span>
          </label>
          <label class="flex items-center gap-2 p-2 rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] cursor-pointer">
            <input type="checkbox" v-model="form.reinstalacion" :disabled="readOnly" class="rounded text-primary" />
            <span class="font-bold text-[11px]">Reinstalación</span>
          </label>
          <label class="flex items-center gap-2 p-2 rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] cursor-pointer">
            <input type="checkbox" v-model="form.cambio_equipo" :disabled="readOnly" class="rounded text-primary" />
            <span class="font-bold text-[11px]">Cambio Equipo</span>
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
            placeholder="Detalle síntomas, alarmas activas y causa raíz encontrada en campo..."
            class="w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] p-3 text-xs focus:ring-1 focus:ring-primary outline-none"
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
            placeholder="Detalle trabajos ejecutados: calibraciones, desmontes, pruebas y estado final..."
            class="w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] p-3 text-xs focus:ring-1 focus:ring-primary outline-none"
          ></textarea>
        </div>
      </div>
    </div>

    <!-- 2. TRAZABILIDAD DE REPUESTOS (RETIRADO VS INSTALADO) -->
    <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
      <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
        <IconPackage class="w-4 h-4 text-blue-500 stroke-[2]" />
        <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
          2. Repuestos y Partes (Retirado vs Instalado)
        </span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Repuesto Retirado -->
        <div class="p-3 bg-red-50/50 dark:bg-red-950/20 border border-red-200/60 dark:border-red-900/30 rounded-xl space-y-2">
          <div class="flex items-center justify-between">
            <span class="font-extrabold text-red-700 dark:text-red-400 text-[11px] uppercase">Parte Retirada (Dañada)</span>
            <Badge variant="outline" class="border-red-300 text-red-600 text-[9px]">Baja</Badge>
          </div>
          <Input v-model="form.repuesto_retirado.descripcion" placeholder="Descripción de la pieza retirada" :disabled="readOnly" class="h-8 text-xs bg-white dark:bg-black/20" />
          <div class="grid grid-cols-3 gap-1.5">
            <Input v-model="form.repuesto_retirado.marca" placeholder="Marca" :disabled="readOnly" class="h-8 text-[11px] bg-white dark:bg-black/20" />
            <Input v-model="form.repuesto_retirado.modelo" placeholder="Modelo" :disabled="readOnly" class="h-8 text-[11px] bg-white dark:bg-black/20" />
            <Input v-model="form.repuesto_retirado.serial" placeholder="Serial" :disabled="readOnly" class="h-8 text-[11px] bg-white dark:bg-black/20 font-mono" />
          </div>
        </div>

        <!-- Repuesto Instalado -->
        <div class="p-3 bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-200/60 dark:border-emerald-900/30 rounded-xl space-y-2">
          <div class="flex items-center justify-between">
            <span class="font-extrabold text-emerald-700 dark:text-emerald-400 text-[11px] uppercase">Parte Nueva Instalada</span>
            <Badge variant="outline" class="border-emerald-300 text-emerald-600 text-[9px]">Operativo</Badge>
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

    <!-- 3. TRANSPORTE ESPECIAL (SI APLICA) -->
    <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
      <div class="flex items-center justify-between border-b border-neutral-100 dark:border-white/5 pb-2.5">
        <div class="flex items-center gap-2">
          <IconTruck class="w-4 h-4 text-purple-500 stroke-[2]" />
          <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
            3. Registro de Transporte Especial (LPU)
          </span>
        </div>
        <select 
          v-model="form.desea_transporte_especial" 
          :disabled="readOnly"
          class="h-7 rounded-lg border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-2 text-xs font-bold text-purple-600"
        >
          <option value="No">No requirió</option>
          <option value="Si">Sí requirió transporte especial</option>
        </select>
      </div>

      <div v-if="form.desea_transporte_especial === 'Si'" class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Tipo de Transporte</label>
          <Input v-model="form.tipo_transporte" placeholder="Ej. Mular, Fluvial, Nocturno" :disabled="readOnly" class="h-9 text-xs" />
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Distancia Recorrida (Km)</label>
          <Input type="number" step="0.1" v-model="form.distancia_km" placeholder="Ej. 18.5" :disabled="readOnly" class="h-9 text-xs" />
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Tiempo de Desplazamiento</label>
          <Input v-model="form.tiempo_desplazamiento" placeholder="Ej. 3h 30min" :disabled="readOnly" class="h-9 text-xs" />
        </div>
        <div class="sm:col-span-3">
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Observaciones de Transporte</label>
          <Input v-model="form.observacion_transporte" placeholder="Detalle condiciones de ruta, transbordo o ayudantía..." :disabled="readOnly" class="h-9 text-xs" />
        </div>
      </div>
    </div>

    <!-- 4. NOVEDADES DE LA ESTACIÓN Y CIERRE -->
    <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
      <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
        <IconCheck class="w-4 h-4 text-emerald-500 stroke-[2.5]" />
        <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
          4. Novedades de Estación & Cierre Operativo
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
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-bold text-xs"
            :class="form.falla_resuelta === 'Si' ? 'text-emerald-600' : 'text-rose-600'"
          >
            <option value="Si">Sí (Equipo en modo automático y sin alarmas)</option>
            <option value="No">No (Requiere segunda visita o repuesto adicional)</option>
          </select>
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">
            Nombre de Supervisor Claro Notificado
          </label>
          <Input v-model="form.nombre_supervisor" placeholder="Ej. Cleyver Espitia / Ing. de Soporte" :disabled="readOnly" class="h-9 text-xs" />
        </div>

        <div class="sm:col-span-2">
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">
            Observaciones Finales de la Actividad
          </label>
          <textarea 
            v-model="form.observaciones_actividad" 
            :disabled="readOnly"
            rows="2" 
            placeholder="Ej. PE queda en modo automático, tablero energizado, sitio cerrado bajo llave..."
            class="w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] p-3 text-xs focus:ring-1 focus:ring-primary outline-none"
          ></textarea>
        </div>
      </div>
    </div>
  </div>
</template>

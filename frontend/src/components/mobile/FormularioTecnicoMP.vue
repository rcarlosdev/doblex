<script setup>
import { reactive, watch, computed } from 'vue';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { 
  IconEngine, 
  IconGauge, 
  IconBatteryCharging, 
  IconUsers, 
  IconCircleCheck,
  IconWind, 
  IconSnowflake,
  IconDroplet,
  IconBolt,
  IconActivity,
  IconClock
} from '@tabler/icons-vue';

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  },
  tipoPreventivo: {
    type: String,
    default: 'planta' // 'planta' o 'aire'
  },
  readOnly: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue']);

const form = reactive({
  // 1. Datos Generales de Planta Eléctrica / Equipo
  marca_equipo: '',
  modelo_equipo: '',
  serial_equipo: '',
  horometro_inicial: null,
  frecuencia_hz: 60,
  capacidad_kva: null,
  
  // Motor y Generador
  marca_motor: '',
  modelo_motor: '',
  serial_motor: '',
  marca_generador: '',
  modelo_generador: '',
  serial_generador: '',

  // 2. Sistema de Baterías
  voltaje_bateria: null,
  voltaje_arranque_bateria: null,
  capacidad_bateria: null,
  tipo_bateria: 'Celda Húmeda',
  estado_bornes: 'Limpios y Ajustados',

  // 3. Sistema de Lubricación y Servicio de Filtración (Lista de Chequeo Oficial)
  filtro_aceite_cambiado: 'Realizado',
  filtro_combustible_cambiado: 'Realizado',
  filtro_aire_estado: 'Cambiado Nuevo',
  cambio_aceite_motor: 'Realizado (15W40)',
  galones_aceite_suministrados: null,
  nivel_refrigerante: 'Normal',
  fugas_lubricacion: 'Sin Fugas',
  presion_aceite_psi: null,
  temperatura_motor_c: null,

  // 4. Combustible y Tanques
  tamano_tanque_galones: null,
  nivel_combustible_porcentaje: null,
  estado_alarma_nivel: 'Normal',
  trampa_agua_drenada: 'Si',
  lineas_combustible_estado: 'Conforme Sin Fugas',

  // 5. Prueba de Encendido ATS con Carga (15 Minutos Mínimo)
  prueba_ats_15min: 'Exitosa con Carga',
  horometro_final_prueba: null,
  tiempo_transferencia_seg: 10,
  voltaje_l1_l2: null,
  voltaje_l2_l3: null,
  voltaje_l1_l3: null,
  frecuencia_operacion_hz: 60,
  planta_en_automatico: 'Si',
  presenta_alarmas: 'No',

  // Climatización / Aire Acondicionado (MP AIRE)
  capacidad_btu: 24000,
  tipo_refrigerante: 'R410A',
  presion_baja_psi: 120,
  presion_alta_psi: 350,
  corriente_compresor_amp: null,
  voltaje_alimentacion_aa: null,
  temperatura_inyeccion_c: null,
  temperatura_retorno_c: null,
  limpieza_evaporador: 'Si',
  limpieza_condensador: 'Si',
  cambio_lavado_filtros: 'Si',
  desague_drenaje_ok: 'Si',

  // Responsables de Campo
  responsable_tec_1: '',
  responsable_tec_2: '',
  observaciones_preventivo: '',
  ...props.modelValue
});

const saltoTermico = computed(() => {
  if (form.temperatura_retorno_c != null && form.temperatura_inyeccion_c != null) {
    const diff = Number(form.temperatura_retorno_c) - Number(form.temperatura_inyeccion_c);
    return isNaN(diff) ? null : diff.toFixed(1);
  }
  return null;
});

watch(form, (val) => {
  emit('update:modelValue', { ...val });
}, { deep: true });
</script>

<template>
  <div class="space-y-6 text-xs select-text">
    <!-- Header identificador -->
    <div class="p-3.5 bg-blue-500/10 border border-blue-500/20 rounded-2xl flex items-center justify-between">
      <div class="flex items-center gap-2">
        <div class="p-2 bg-blue-500/20 text-blue-600 dark:text-blue-400 rounded-xl">
          <IconWind v-if="tipoPreventivo === 'aire'" class="w-5 h-5 stroke-[2]" />
          <IconEngine v-else class="w-5 h-5 stroke-[2]" />
        </div>
        <div>
          <h4 class="font-extrabold text-neutral-900 dark:text-white text-xs">
            Formato Técnico: Mantenimiento Preventivo (MP - {{ tipoPreventivo === 'aire' ? 'CLIMATIZACIÓN / AIRE' : 'PLANTA ELÉCTRICA / GE' }})
          </h4>
          <p class="text-[10px] text-neutral-500 dark:text-neutral-400">
            Alineado con estándar oficial Claro / INMEL (Plan de Mantenimiento Preventivo Integral)
          </p>
        </div>
      </div>
      <Badge variant="outline" class="border-blue-500/30 text-blue-600 dark:text-blue-400 font-bold text-[10px]">
        {{ tipoPreventivo === 'aire' ? 'MP Aire' : 'MP Planta' }}
      </Badge>
    </div>

    <!-- SECCIÓN PLANTA: 1. DATOS PRINCIPALES DE PLANTA / GRUPO ELECTRÓGENO -->
    <div v-if="tipoPreventivo !== 'aire'" class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
      <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
        <IconEngine class="w-4 h-4 text-blue-500 stroke-[2]" />
        <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
          1. Ficha Técnica del Grupo Electrógeno (Planta)
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Marca Equipo</label>
          <Input v-model="form.marca_equipo" placeholder="Ej. AGG Power, Cummins, Selmec" :disabled="readOnly" class="h-9 text-xs" />
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Modelo</label>
          <Input v-model="form.modelo_equipo" placeholder="Ej. C27D6" :disabled="readOnly" class="h-9 text-xs" />
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Serial N°</label>
          <Input v-model="form.serial_equipo" placeholder="Ej. A1904183" :disabled="readOnly" class="h-9 text-xs font-mono" />
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Horómetro Inicial (Horas) *</label>
          <Input type="number" step="0.1" v-model="form.horometro_inicial" placeholder="Ej. 3913.3" :disabled="readOnly" class="h-9 text-xs font-bold text-blue-600" />
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Capacidad (KVA)</label>
          <Input type="number" v-model="form.capacidad_kva" placeholder="Ej. 24" :disabled="readOnly" class="h-9 text-xs" />
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Frecuencia (Hz)</label>
          <Input type="number" v-model="form.frecuencia_hz" placeholder="60" :disabled="readOnly" class="h-9 text-xs" />
        </div>
      </div>

      <!-- Motor y Generador -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2 border-t border-neutral-100 dark:border-white/5">
        <div class="space-y-2 p-3 bg-neutral-50 dark:bg-white/[0.02] rounded-xl border border-neutral-200/60 dark:border-white/5">
          <span class="font-bold text-[10px] uppercase tracking-wider text-neutral-600 dark:text-neutral-400">Datos Motor</span>
          <Input v-model="form.marca_motor" placeholder="Marca Motor (Ej. Cummins)" :disabled="readOnly" class="h-8 text-xs" />
          <div class="grid grid-cols-2 gap-2">
            <Input v-model="form.modelo_motor" placeholder="Modelo (Ej. 4B3.9-G2)" :disabled="readOnly" class="h-8 text-[11px]" />
            <Input v-model="form.serial_motor" placeholder="Serial Motor" :disabled="readOnly" class="h-8 text-[11px] font-mono" />
          </div>
        </div>

        <div class="space-y-2 p-3 bg-neutral-50 dark:bg-white/[0.02] rounded-xl border border-neutral-200/60 dark:border-white/5">
          <span class="font-bold text-[10px] uppercase tracking-wider text-neutral-600 dark:text-neutral-400">Datos Generador</span>
          <Input v-model="form.marca_generador" placeholder="Marca Generador (Ej. Stamford)" :disabled="readOnly" class="h-8 text-xs" />
          <div class="grid grid-cols-2 gap-2">
            <Input v-model="form.modelo_generador" placeholder="Modelo (Ej. PI144D1)" :disabled="readOnly" class="h-8 text-[11px]" />
            <Input v-model="form.serial_generador" placeholder="Serial Generador" :disabled="readOnly" class="h-8 text-[11px] font-mono" />
          </div>
        </div>
      </div>
    </div>

    <!-- SECCIÓN PLANTA: 2. SISTEMA DE BATERÍAS -->
    <div v-if="tipoPreventivo !== 'aire'" class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
      <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
        <IconBatteryCharging class="w-4 h-4 text-emerald-500 stroke-[2]" />
        <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
          2. Sistema de Baterías de Arranque
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Voltaje Batería (V DC) *</label>
          <Input type="number" step="0.1" v-model="form.voltaje_bateria" placeholder="Ej. 25.4" :disabled="readOnly" class="h-9 text-xs font-bold text-emerald-600" />
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Capacidad Batería (Ah / CCA)</label>
          <Input type="number" v-model="form.capacidad_bateria" placeholder="Ej. 1150" :disabled="readOnly" class="h-9 text-xs" />
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Tipo de Batería</label>
          <select 
            v-model="form.tipo_bateria" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs"
          >
            <option value="Celda Húmeda">Celda Húmeda (Ácido-Plomo)</option>
            <option value="Libre de Mantenimiento">Libre de Mantenimiento (AGM/GEL)</option>
            <option value="Litio">Litio</option>
          </select>
        </div>
      </div>
    </div>

    <!-- SECCIÓN PLANTA: 3. SISTEMA DE LUBRICACIÓN Y SERVICIO DE FILTRACIÓN -->
    <div v-if="tipoPreventivo !== 'aire'" class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
      <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
        <IconDroplet class="w-4 h-4 text-amber-500 stroke-[2]" />
        <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
          3. Sistema de Lubricación & Servicio de Filtración
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Cambio Filtro de Aceite</label>
          <select 
            v-model="form.filtro_aceite_cambiado" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs"
          >
            <option value="Realizado">Realizado (Nuevo)</option>
            <option value="Bueno">En Buen Estado / No Aplica</option>
            <option value="Pendiente">Pendiente por Suministro</option>
          </select>
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Cambio Filtro de Combustible</label>
          <select 
            v-model="form.filtro_combustible_cambiado" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs"
          >
            <option value="Realizado">Realizado (Nuevo)</option>
            <option value="Bueno">En Buen Estado / No Aplica</option>
            <option value="Pendiente">Pendiente por Suministro</option>
          </select>
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Filtro de Aire</label>
          <select 
            v-model="form.filtro_aire_estado" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs"
          >
            <option value="Cambiado Nuevo">Cambiado Nuevo</option>
            <option value="Sopleteado Limpio">Sopleteado y Limpio</option>
            <option value="Bueno">En Buen Estado</option>
          </select>
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Cambio de Aceite de Motor</label>
          <select 
            v-model="form.cambio_aceite_motor" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs"
          >
            <option value="Realizado (15W40)">Realizado (15W40 Nuevo)</option>
            <option value="Nivel Completado">Nivel Completado</option>
            <option value="Conforme">Nivel Conforme / No Requiere</option>
          </select>
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Galones Aceite Suministrados</label>
          <Input type="number" step="0.5" v-model="form.galones_aceite_suministrados" placeholder="Ej. 3.5" :disabled="readOnly" class="h-9 text-xs" />
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Nivel Refrigerante Radiador</label>
          <select 
            v-model="form.nivel_refrigerante" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs"
          >
            <option value="Normal">Normal (Nivel OK)</option>
            <option value="Completado">Completado / Rellenado</option>
            <option value="Bajo">Bajo Nivel (Requiere atención)</option>
          </select>
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Inspección de Fugas</label>
          <select 
            v-model="form.fugas_lubricacion" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs"
          >
            <option value="Sin Fugas">Sin Fugas (Juntas y mangueras secas)</option>
            <option value="Fuga Leve">Presenta Fuga Leve</option>
            <option value="Fuga Critica">Presenta Fuga Crítica</option>
          </select>
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Presión de Aceite (PSI)</label>
          <Input type="number" v-model="form.presion_aceite_psi" placeholder="Ej. 45" :disabled="readOnly" class="h-9 text-xs" />
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Temperatura Motor (°C)</label>
          <Input type="number" v-model="form.temperatura_motor_c" placeholder="Ej. 82" :disabled="readOnly" class="h-9 text-xs" />
        </div>
      </div>
    </div>

    <!-- SECCIÓN PLANTA: 4. SISTEMA DE COMBUSTIBLE -->
    <div v-if="tipoPreventivo !== 'aire'" class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
      <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
        <IconGauge class="w-4 h-4 text-amber-500 stroke-[2]" />
        <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
          4. Sistema de Combustible y Almacenamiento
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Capacidad Tanque (Galones)</label>
          <Input type="number" v-model="form.tamano_tanque_galones" placeholder="Ej. 150" :disabled="readOnly" class="h-9 text-xs" />
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Nivel Combustible Actual (%) *</label>
          <Input type="number" min="0" max="100" v-model="form.nivel_combustible_porcentaje" placeholder="Ej. 85" :disabled="readOnly" class="h-9 text-xs font-bold text-amber-600" />
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Estado Alarma de Nivel</label>
          <select 
            v-model="form.estado_alarma_nivel" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs"
          >
            <option value="Normal">Normal (Sin alarma)</option>
            <option value="Alarma">Alarma de Bajo Nivel Activa</option>
          </select>
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Trampa de Agua Drenada</label>
          <select 
            v-model="form.trampa_agua_drenada" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs"
          >
            <option value="Si">Sí (Drenada y limpia)</option>
            <option value="No">No / No aplica</option>
          </select>
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Líneas de Combustible</label>
          <select 
            v-model="form.lineas_combustible_estado" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs"
          >
            <option value="Conforme Sin Fugas">Conforme Sin Fugas</option>
            <option value="Fuga Detectada">Fuga Detectada en Acoples</option>
            <option value="Mangueras Resecas">Mangueras Resecas (Requiere Cambio)</option>
          </select>
        </div>
      </div>
    </div>

    <!-- SECCIÓN PLANTA: 5. PROTOCOLO DE PRUEBA DE ENCENDIDO ATS CON CARGA (15 MIN) -->
    <div v-if="tipoPreventivo !== 'aire'" class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
      <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
        <IconBolt class="w-4 h-4 text-yellow-500 stroke-[2]" />
        <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
          5. Prueba de Encendido y Transferencia ATS con Carga (15 Minutos)
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Prueba ATS 15 Min con Carga *</label>
          <select 
            v-model="form.prueba_ats_15min" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-bold text-xs"
            :class="form.prueba_ats_15min === 'Exitosa con Carga' ? 'text-emerald-600' : 'text-amber-600'"
          >
            <option value="Exitosa con Carga">Exitosa con Carga (15 min)</option>
            <option value="Prueba en Vacio">Prueba en Vacío (Sin transferencia)</option>
            <option value="Falla en Transferencia">Falla en Transferencia</option>
            <option value="No Realizada">No Realizada por Novedad</option>
          </select>
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Horómetro Final de Prueba *</label>
          <Input type="number" step="0.1" v-model="form.horometro_final_prueba" placeholder="Ej. 3913.6" :disabled="readOnly" class="h-9 text-xs font-bold text-blue-600" />
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Tiempo de Transferencia (Seg)</label>
          <Input type="number" v-model="form.tiempo_transferencia_seg" placeholder="Ej. 10" :disabled="readOnly" class="h-9 text-xs" />
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Voltaje Generación L1-L2 (VAC)</label>
          <Input type="number" v-model="form.voltaje_l1_l2" placeholder="Ej. 220" :disabled="readOnly" class="h-9 text-xs font-mono" />
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Voltaje Generación L2-L3 (VAC)</label>
          <Input type="number" v-model="form.voltaje_l2_l3" placeholder="Ej. 220" :disabled="readOnly" class="h-9 text-xs font-mono" />
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Voltaje Generación L1-L3 (VAC)</label>
          <Input type="number" v-model="form.voltaje_l1_l3" placeholder="Ej. 220" :disabled="readOnly" class="h-9 text-xs font-mono" />
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Frecuencia en Carga (Hz)</label>
          <Input type="number" v-model="form.frecuencia_operacion_hz" placeholder="60" :disabled="readOnly" class="h-9 text-xs" />
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">¿Planta Queda en Automático? *</label>
          <select 
            v-model="form.planta_en_automatico" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-bold text-xs"
            :class="form.planta_en_automatico === 'Si' ? 'text-emerald-600' : 'text-rose-600'"
          >
            <option value="Si">Sí (Listo para Emergencias)</option>
            <option value="No">No (En Manual / Fuera de Servicio)</option>
          </select>
        </div>

        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">¿Tablero sin Alarmas Activas?</label>
          <select 
            v-model="form.presenta_alarmas" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs"
          >
            <option value="No">No (Tablero despejado sin fallas)</option>
            <option value="Si">Sí (Presenta alarmas)</option>
          </select>
        </div>
      </div>
    </div>

    <!-- SECCIÓN CLIMATIZACIÓN: 1. FICHA TÉCNICA AIRE ACONDICIONADO -->
    <div v-if="tipoPreventivo === 'aire'" class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
      <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
        <IconWind class="w-4 h-4 text-cyan-500 stroke-[2]" />
        <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
          1. Ficha Técnica de Climatización (Aire Acondicionado)
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Marca Equipo AA</label>
          <Input v-model="form.marca_equipo" placeholder="Ej. ComfortStar, York, Carrier" :disabled="readOnly" class="h-9 text-xs" />
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Modelo / Referencia</label>
          <Input v-model="form.modelo_equipo" placeholder="Ej. YHE24" :disabled="readOnly" class="h-9 text-xs" />
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Serial N°</label>
          <Input v-model="form.serial_equipo" placeholder="Serial evaporador/condensador" :disabled="readOnly" class="h-9 text-xs font-mono" />
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Capacidad (BTU) *</label>
          <Input type="number" v-model="form.capacidad_btu" placeholder="Ej. 24000" :disabled="readOnly" class="h-9 text-xs font-bold text-cyan-600" />
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Tipo de Gas Refrigerante</label>
          <select 
            v-model="form.tipo_refrigerante" 
            :disabled="readOnly"
            class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs"
          >
            <option value="R410A">R410A (Ecológico)</option>
            <option value="R22">R22</option>
            <option value="R32">R32</option>
            <option value="R134a">R134a</option>
          </select>
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Corriente Compresor (Amp)</label>
          <Input type="number" step="0.1" v-model="form.corriente_compresor_amp" placeholder="Ej. 9.8" :disabled="readOnly" class="h-9 text-xs" />
        </div>
      </div>
    </div>

    <!-- SECCIÓN CLIMATIZACIÓN: 2. PARÁMETROS DE OPERACIÓN AA -->
    <div v-if="tipoPreventivo === 'aire'" class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
      <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
        <IconSnowflake class="w-4 h-4 text-cyan-500 stroke-[2]" />
        <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
          2. Parámetros de Operación y Chequeo Climatización
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-4 gap-3">
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Presión Baja (PSI)</label>
          <Input type="number" v-model="form.presion_baja_psi" placeholder="Ej. 120" :disabled="readOnly" class="h-9 text-xs" />
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Presión Alta (PSI)</label>
          <Input type="number" v-model="form.presion_alta_psi" placeholder="Ej. 350" :disabled="readOnly" class="h-9 text-xs" />
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Temp. Inyección (°C)</label>
          <Input type="number" step="0.5" v-model="form.temperatura_inyeccion_c" placeholder="Ej. 14.5" :disabled="readOnly" class="h-9 text-xs" />
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Temp. Retorno (°C)</label>
          <Input type="number" step="0.5" v-model="form.temperatura_retorno_c" placeholder="Ej. 22.0" :disabled="readOnly" class="h-9 text-xs" />
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2 border-t border-neutral-100 dark:border-white/5">
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Voltaje Alimentación AA (VAC)</label>
          <Input type="number" v-model="form.voltaje_alimentacion_aa" placeholder="Ej. 220" :disabled="readOnly" class="h-9 text-xs" />
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Salto Térmico (Delta T = Retorno - Inyección)</label>
          <div class="h-9 rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 flex items-center justify-between text-xs font-bold">
            <span :class="saltoTermico && Number(saltoTermico) >= 8 ? 'text-emerald-600' : 'text-amber-600'">
              {{ saltoTermico != null ? `${saltoTermico} °C (${Number(saltoTermico) >= 8 ? 'Óptimo ≥ 8°C' : 'Bajo Rendimiento'})` : 'Ingrese Temp. Inyección y Retorno' }}
            </span>
            <IconSnowflake class="w-4 h-4 text-cyan-500 stroke-[2]" />
          </div>
        </div>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-2 border-t border-neutral-100 dark:border-white/5">
        <label class="flex items-center gap-2 p-2.5 rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] cursor-pointer">
          <input type="checkbox" v-model="form.limpieza_evaporador" true-value="Si" false-value="No" :disabled="readOnly" class="rounded text-primary" />
          <span class="font-bold text-[11px]">Lavado Evaporador</span>
        </label>
        <label class="flex items-center gap-2 p-2.5 rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] cursor-pointer">
          <input type="checkbox" v-model="form.limpieza_condensador" true-value="Si" false-value="No" :disabled="readOnly" class="rounded text-primary" />
          <span class="font-bold text-[11px]">Lavado Condensador</span>
        </label>
        <label class="flex items-center gap-2 p-2.5 rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] cursor-pointer">
          <input type="checkbox" v-model="form.cambio_lavado_filtros" true-value="Si" false-value="No" :disabled="readOnly" class="rounded text-primary" />
          <span class="font-bold text-[11px]">Filtros Limpios</span>
        </label>
        <label class="flex items-center gap-2 p-2.5 rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] cursor-pointer">
          <input type="checkbox" v-model="form.desague_drenaje_ok" true-value="Si" false-value="No" :disabled="readOnly" class="rounded text-primary" />
          <span class="font-bold text-[11px]">Drenaje Despejado</span>
        </label>
      </div>
    </div>

    <!-- 4. RESPONSABLES TÉCNICOS DE CAMPO -->
    <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
      <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
        <IconUsers class="w-4 h-4 text-purple-500 stroke-[2]" />
        <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
          4. Personal Técnico Ejecutor
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Responsable Técnico 1 *</label>
          <Input v-model="form.responsable_tec_1" placeholder="Nombre completo técnico líder" :disabled="readOnly" class="h-9 text-xs" />
        </div>
        <div>
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Responsable Técnico 2</label>
          <Input v-model="form.responsable_tec_2" placeholder="Nombre auxiliar / No aplica" :disabled="readOnly" class="h-9 text-xs" />
        </div>
        <div class="sm:col-span-2">
          <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Observaciones del Mantenimiento Preventivo</label>
          <textarea 
            v-model="form.observaciones_preventivo" 
            :disabled="readOnly"
            rows="2" 
            placeholder="Rutina ejecutada conforme a lista de chequeo, pruebas con carga satisfactorias..."
            class="w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] p-3 text-xs focus:ring-1 focus:ring-primary outline-none"
          ></textarea>
        </div>
      </div>
    </div>
  </div>
</template>

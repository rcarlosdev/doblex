<script setup>
import { reactive, watch, computed } from 'vue';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { 
  IconEngine, 
  IconGauge, 
  IconBatteryCharging, 
  IconUsers, 
  IconWind, 
  IconSnowflake,
  IconDroplet,
  IconBolt,
  IconClock,
  IconCheck,
  IconAlertTriangle,
  IconShieldCheck
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
  // 1. Datos Principales de Planta Eléctrica / ATS (Ref. Hoja PROPUESTA ELECTROGENO)
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

  // Transferencia Automática (ATS)
  marca_ats: '',
  modelo_ats: '',
  capacidad_ats_amp: null,

  // 2. Sistema de Baterías
  voltaje_bateria: null,
  capacidad_bateria: null,
  tipo_bateria: 'Celda Húmeda',
  estado_bornes: 'Limpios y Ajustados',

  // 3. Sistema de Lubricación y Servicio de Filtración (Ref. Hoja Lista de MP)
  filtro_aceite_cambiado: 'Realizado',
  filtro_combustible_cambiado: 'Realizado',
  filtro_aire_estado: 'Cambiado Nuevo',
  cambio_aceite_motor: 'Realizado (15W40)',
  galones_aceite_suministrados: null,
  nivel_refrigerante: 'Normal',
  fugas_lubricacion: 'Sin Fugas',
  presion_aceite_psi: null,
  temperatura_motor_c: null,

  // 4. Combustible y Tanques (Ref. Hoja Prueba de Planta)
  tamano_tanque_galones: null,
  nivel_combustible_porcentaje: null,
  estado_alarma_nivel: 'Normal',
  trampa_agua_drenada: 'Si',
  lineas_combustible_estado: 'Conforme Sin Fugas',

  // 5. Prueba de Encendido de Planta (Ref. Hoja Prueba de Planta & Parámetros en Carga)
  planta_operativa: 'Si',
  presenta_alarmas: 'No',
  alarmas_detalle: '',
  prueba_ats_15min: 'Exitosa con Carga',
  horometro_final_prueba: null,
  tiempo_transferencia_seg: 10,
  planta_temporizada: 'No',
  horario_temporizacion: '',
  alarma_externa_noc_ok: 'Si',
  requiere_cambio_cabina: 'No',
  planta_en_automatico: 'Si',

  // Parámetros Eléctricos en Carga (Ref. Hoja Lista de MP)
  voltaje_l1_l2: null,
  voltaje_l2_l3: null,
  voltaje_l1_l3: null,
  voltaje_l1_n: null,
  voltaje_l2_n: null,
  voltaje_l3_n: null,
  corriente_l1_amp: null,
  corriente_l2_amp: null,
  corriente_l3_amp: null,
  porcentaje_cargabilidad: null,
  frecuencia_operacion_hz: 60,

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

  // Responsables de Campo y Observaciones
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

watch(() => props.modelValue, (newVal) => {
  if (newVal && Object.keys(newVal).length > 0) {
    Object.assign(form, newVal);
  }
}, { deep: true });
</script>

<template>
  <div class="space-y-5 text-xs select-text">
    <!-- Header de Identificación del Formato Oficial MP -->
    <div class="p-3.5 bg-blue-500/10 border border-blue-500/20 rounded-2xl flex items-center justify-between flex-wrap gap-2">
      <div class="flex items-center gap-2.5">
        <div class="p-2 bg-blue-500/20 text-blue-600 dark:text-blue-400 rounded-xl">
          <IconWind v-if="tipoPreventivo === 'aire'" class="w-5 h-5 stroke-[2]" />
          <IconEngine v-else class="w-5 h-5 stroke-[2]" />
        </div>
        <div>
          <h4 class="font-extrabold text-neutral-900 dark:text-white text-xs">
            Formato Técnico: Mantenimiento Preventivo (MP - {{ tipoPreventivo === 'aire' ? 'CLIMATIZACIÓN / AIRE' : 'PLANTA ELÉCTRICA / GE' }})
          </h4>
          <p class="text-[10px] text-neutral-500 dark:text-neutral-400">
            Formato oficial Claro (Ref. OT5304019 - MP RPT Bahía Solano)
          </p>
        </div>
      </div>
      <Badge variant="outline" class="border-blue-500/30 text-blue-600 dark:text-blue-400 font-bold text-[10px]">
        {{ tipoPreventivo === 'aire' ? 'MP Climatización' : 'MP Grupo Electrógeno' }}
      </Badge>
    </div>

    <!-- ============================================================= -->
    <!-- CASO 1: SECCIÓN MANTENIMIENTO PREVENTIVO PLANTA ELÉCTRICA    -->
    <!-- ============================================================= -->
    <template v-if="tipoPreventivo !== 'aire'">
      <!-- 1. DATOS PRINCIPALES DE PLANTAS Y ATS (PLACA) -->
      <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
        <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
          <IconEngine class="w-4 h-4 text-blue-500 stroke-[2]" />
          <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
            1. Datos Principales de Planta, Motor, Generador y ATS (Placas Técnicas)
          </span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Marca Planta *</label>
            <Input v-model="form.marca_equipo" placeholder="Ej. AGG POWER SOLUTIONS, Cummins" :disabled="readOnly" class="h-9 text-xs" />
          </div>
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Modelo Planta</label>
            <Input v-model="form.modelo_equipo" placeholder="Ej. C27D6" :disabled="readOnly" class="h-9 text-xs" />
          </div>
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Serial N° Planta</label>
            <Input v-model="form.serial_equipo" placeholder="Ej. A1904183" :disabled="readOnly" class="h-9 text-xs font-mono" />
          </div>
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Horómetro Inicial (Horas) *</label>
            <Input type="number" step="0.1" v-model="form.horometro_inicial" placeholder="Ej. 3913.3" :disabled="readOnly" class="h-9 text-xs font-bold text-blue-600" />
          </div>
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Capacidad (KVA) *</label>
            <Input type="number" v-model="form.capacidad_kva" placeholder="Ej. 24" :disabled="readOnly" class="h-9 text-xs" />
          </div>
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Frecuencia (Hz)</label>
            <Input type="number" v-model="form.frecuencia_hz" placeholder="60" :disabled="readOnly" class="h-9 text-xs" />
          </div>
        </div>

        <!-- Sub-componentes: Motor, Generador y ATS -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 border-t border-neutral-100 dark:border-white/5">
          <!-- Motor -->
          <div class="space-y-2 p-3 bg-neutral-50 dark:bg-white/[0.02] rounded-xl border border-neutral-200/60 dark:border-white/5">
            <span class="font-bold text-[10px] uppercase tracking-wider text-blue-600 dark:text-blue-400">Motor Diesel</span>
            <Input v-model="form.marca_motor" placeholder="Marca (Ej. CUMMINS)" :disabled="readOnly" class="h-8 text-xs" />
            <Input v-model="form.modelo_motor" placeholder="Modelo (Ej. 4B3.9-G2)" :disabled="readOnly" class="h-8 text-[11px]" />
            <Input v-model="form.serial_motor" placeholder="Serial (Ej. 78934783)" :disabled="readOnly" class="h-8 text-[11px] font-mono" />
          </div>

          <!-- Generador -->
          <div class="space-y-2 p-3 bg-neutral-50 dark:bg-white/[0.02] rounded-xl border border-neutral-200/60 dark:border-white/5">
            <span class="font-bold text-[10px] uppercase tracking-wider text-blue-600 dark:text-blue-400">Generador / Alternador</span>
            <Input v-model="form.marca_generador" placeholder="Marca (Ej. STAMFORD)" :disabled="readOnly" class="h-8 text-xs" />
            <Input v-model="form.modelo_generador" placeholder="Modelo (Ej. PI144D1)" :disabled="readOnly" class="h-8 text-[11px]" />
            <Input v-model="form.serial_generador" placeholder="Serial (Ej. B18G294552)" :disabled="readOnly" class="h-8 text-[11px] font-mono" />
          </div>

          <!-- Transferencia Automática ATS -->
          <div class="space-y-2 p-3 bg-neutral-50 dark:bg-white/[0.02] rounded-xl border border-neutral-200/60 dark:border-white/5">
            <span class="font-bold text-[10px] uppercase tracking-wider text-blue-600 dark:text-blue-400">Transferencia ATS</span>
            <Input v-model="form.marca_ats" placeholder="Marca ATS (Ej. ABB, Socomec)" :disabled="readOnly" class="h-8 text-xs" />
            <Input v-model="form.modelo_ats" placeholder="Modelo ATS (Ej. OTM-70A)" :disabled="readOnly" class="h-8 text-[11px]" />
            <Input type="number" v-model="form.capacidad_ats_amp" placeholder="Capacidad Amp (Ej. 70)" :disabled="readOnly" class="h-8 text-[11px] font-mono" />
          </div>
        </div>
      </div>

      <!-- 2. SISTEMA DE BATERÍAS -->
      <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
        <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
          <IconBatteryCharging class="w-4 h-4 text-emerald-500 stroke-[2]" />
          <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
            2. Sistema de Baterías de Arranque
          </span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-4 gap-3">
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Voltaje Batería (V DC) *</label>
            <Input type="number" step="0.1" v-model="form.voltaje_bateria" placeholder="Ej. 25.2" :disabled="readOnly" class="h-9 text-xs font-bold text-emerald-600" />
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
              class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs outline-none"
            >
              <option value="Celda Húmeda">Celda Húmeda (Ácido-Plomo)</option>
              <option value="Libre de Mantenimiento">Libre de Mantenimiento (AGM/GEL)</option>
              <option value="Sellada VRLA">Sellada VRLA</option>
            </select>
          </div>
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Estado de Bornes</label>
            <select 
              v-model="form.estado_bornes" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs outline-none"
            >
              <option value="Limpios y Ajustados">Limpios y Ajustados</option>
              <option value="Sulfatados (Limpiados)">Sulfatados (Limpiados en sitio)</option>
              <option value="Flojos (Ajustados)">Flojos (Ajustados en sitio)</option>
            </select>
          </div>
        </div>
      </div>

      <!-- 3. RUTINA Y PRUEBA DE ENCENDIDO DE PLANTA (HOJA PRUEBA DE PLANTA) -->
      <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
        <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
          <IconBolt class="w-4 h-4 text-amber-500 stroke-[2]" />
          <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
            3. Rutina de Encendido y Prueba de Planta (15 Minutos con Carga)
          </span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">
              ¿Planta Eléctrica se Encuentra Operativa? *
            </label>
            <select 
              v-model="form.planta_operativa" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-bold text-xs outline-none"
              :class="form.planta_operativa === 'Si' ? 'text-emerald-600' : 'text-rose-600'"
            >
              <option value="Si">Sí (Operativa y funcional)</option>
              <option value="No">No (Fuera de servicio / Dañada)</option>
            </select>
          </div>

          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">
              Prueba 15 Min con Carga Simulando Falla *
            </label>
            <select 
              v-model="form.prueba_ats_15min" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-bold text-xs outline-none"
              :class="form.prueba_ats_15min === 'Exitosa con Carga' ? 'text-emerald-600' : 'text-amber-600'"
            >
              <option value="Exitosa con Carga">Sí - Soporta 15 min de carga</option>
              <option value="Prueba en Vacio">Prueba en Vacío (Sin transferencia)</option>
              <option value="Falla en Transferencia">Falla en Transferencia</option>
              <option value="No Realizada">No Realizada por Novedad</option>
            </select>
          </div>

          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">
              Horómetro Final de Prueba *
            </label>
            <Input type="number" step="0.1" v-model="form.horometro_final_prueba" placeholder="Ej. 3913.6" :disabled="readOnly" class="h-9 text-xs font-bold text-blue-600" />
          </div>

          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">
              ¿Presenta Alarmas en Tablero?
            </label>
            <select 
              v-model="form.presenta_alarmas" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs outline-none"
            >
              <option value="No">No (Despejado sin alarmas)</option>
              <option value="Si">Sí (Presenta alarmas activas)</option>
            </select>
          </div>

          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">
              Alarma Externa Planta Operativa (NOC)
            </label>
            <select 
              v-model="form.alarma_externa_noc_ok" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs outline-none"
            >
              <option value="Si">Sí (Validada con NOC)</option>
              <option value="No">No / Pendiente validación NOC</option>
            </select>
          </div>

          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">
              ¿Planta Queda en Automático? *
            </label>
            <select 
              v-model="form.planta_en_automatico" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-bold text-xs outline-none"
              :class="form.planta_en_automatico === 'Si' ? 'text-emerald-600' : 'text-rose-600'"
            >
              <option value="Si">Sí (En Automático lista para actuar)</option>
              <option value="No">No (En Manual / Fuera de servicio)</option>
            </select>
          </div>

          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">
              ¿Planta está Temporizada?
            </label>
            <select 
              v-model="form.planta_temporizada" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs outline-none"
            >
              <option value="No">No (Operación 24/7)</option>
              <option value="Si">Sí (Horario restringido)</option>
            </select>
          </div>

          <div v-if="form.planta_temporizada === 'Si'">
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Horario Temporización</label>
            <Input v-model="form.horario_temporizacion" placeholder="De: 06:00 Hasta: 22:00" :disabled="readOnly" class="h-9 text-xs" />
          </div>

          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">
              ¿PE Requiere Cambio de Cabina?
            </label>
            <select 
              v-model="form.requiere_cambio_cabina" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs outline-none"
            >
              <option value="No">No (Cabina en buen estado)</option>
              <option value="Si">Sí (Cabina corroída / deteriorada)</option>
            </select>
          </div>
        </div>
      </div>

      <!-- 4. PARÁMETROS ELÉCTRICOS DE OPERACIÓN EN CARGA (HOJA LISTA DE MP) -->
      <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
        <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
          <IconGauge class="w-4 h-4 text-cyan-500 stroke-[2]" />
          <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
            4. Parámetros Eléctricos de Generación en Carga
          </span>
        </div>

        <!-- Voltajes Fase-Fase y Fase-Neutro -->
        <div class="grid grid-cols-2 sm:grid-cols-6 gap-2.5">
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">V L1-L2 (VAC)</label>
            <Input type="number" v-model="form.voltaje_l1_l2" placeholder="220" :disabled="readOnly" class="h-8 text-xs font-mono font-bold text-cyan-600" />
          </div>
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">V L2-L3 (VAC)</label>
            <Input type="number" v-model="form.voltaje_l2_l3" placeholder="220" :disabled="readOnly" class="h-8 text-xs font-mono font-bold text-cyan-600" />
          </div>
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">V L1-L3 (VAC)</label>
            <Input type="number" v-model="form.voltaje_l1_l3" placeholder="220" :disabled="readOnly" class="h-8 text-xs font-mono font-bold text-cyan-600" />
          </div>
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">V L1-N (VAC)</label>
            <Input type="number" v-model="form.voltaje_l1_n" placeholder="127" :disabled="readOnly" class="h-8 text-xs font-mono" />
          </div>
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">V L2-N (VAC)</label>
            <Input type="number" v-model="form.voltaje_l2_n" placeholder="127" :disabled="readOnly" class="h-8 text-xs font-mono" />
          </div>
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">V L3-N (VAC)</label>
            <Input type="number" v-model="form.voltaje_l3_n" placeholder="127" :disabled="readOnly" class="h-8 text-xs font-mono" />
          </div>
        </div>

        <!-- Corrientes y Cargabilidad -->
        <div class="grid grid-cols-2 sm:grid-cols-5 gap-2.5 pt-2 border-t border-neutral-100 dark:border-white/5">
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Corriente L1 (A)</label>
            <Input type="number" step="0.1" v-model="form.corriente_l1_amp" placeholder="Ej. 5.6" :disabled="readOnly" class="h-8 text-xs font-mono" />
          </div>
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Corriente L2 (A)</label>
            <Input type="number" step="0.1" v-model="form.corriente_l2_amp" placeholder="Ej. 5.8" :disabled="readOnly" class="h-8 text-xs font-mono" />
          </div>
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Corriente L3 (A)</label>
            <Input type="number" step="0.1" v-model="form.corriente_l3_amp" placeholder="Ej. 5.5" :disabled="readOnly" class="h-8 text-xs font-mono" />
          </div>
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Cargabilidad (%)</label>
            <Input type="number" step="0.5" v-model="form.porcentaje_cargabilidad" placeholder="Ej. 8%" :disabled="readOnly" class="h-8 text-xs font-bold text-cyan-600" />
          </div>
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Frecuencia (Hz)</label>
            <Input type="number" v-model="form.frecuencia_operacion_hz" placeholder="60" :disabled="readOnly" class="h-8 text-xs font-bold" />
          </div>
        </div>
      </div>

      <!-- 5. CHECKLIST INTEGRAL DE LUBRICACIÓN, COMBUSTIBLE Y REFRIGERACIÓN -->
      <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
        <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
          <IconDroplet class="w-4 h-4 text-amber-500 stroke-[2]" />
          <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
            5. Rutina de Lubricación, Filtración & Combustible
          </span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Cambio Filtro Aceite</label>
            <select 
              v-model="form.filtro_aceite_cambiado" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs outline-none"
            >
              <option value="Realizado">Realizado (Nuevo instalado)</option>
              <option value="Bueno">En Buen Estado / No Aplica</option>
              <option value="Pendiente">Pendiente por Suministro</option>
            </select>
          </div>

          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Cambio Filtro Combustible</label>
            <select 
              v-model="form.filtro_combustible_cambiado" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs outline-none"
            >
              <option value="Realizado">Realizado (Nuevo instalado)</option>
              <option value="Bueno">En Buen Estado / No Aplica</option>
              <option value="Pendiente">Pendiente por Suministro</option>
            </select>
          </div>

          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Filtro de Aire</label>
            <select 
              v-model="form.filtro_aire_estado" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs outline-none"
            >
              <option value="Cambiado Nuevo">Cambiado Nuevo</option>
              <option value="Sopleteado Limpio">Sopleteado y Limpio</option>
              <option value="Bueno">En Buen Estado</option>
            </select>
          </div>

          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Cambio de Aceite Motor (15W40)</label>
            <select 
              v-model="form.cambio_aceite_motor" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs outline-none"
            >
              <option value="Realizado (15W40)">Realizado (15W40 Nuevo)</option>
              <option value="Nivel Completado">Nivel Completado / Relleno</option>
              <option value="Conforme">Conforme (No requiere cambio)</option>
            </select>
          </div>

          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Galones Aceite Suministrados</label>
            <Input type="number" step="0.5" v-model="form.galones_aceite_suministrados" placeholder="Ej. 3.5" :disabled="readOnly" class="h-9 text-xs" />
          </div>

          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Presión de Aceite (PSI)</label>
            <Input type="number" v-model="form.presion_aceite_psi" placeholder="Ej. 52" :disabled="readOnly" class="h-9 text-xs font-bold" />
          </div>

          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Nivel Refrigerante Radiador</label>
            <select 
              v-model="form.nivel_refrigerante" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs outline-none"
            >
              <option value="Normal">Normal (Nivel óptimo)</option>
              <option value="Completado">Completado con refrigerante</option>
              <option value="Bajo">Bajo Nivel (Requiere revisión)</option>
            </select>
          </div>

          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Temperatura Motor (°C)</label>
            <Input type="number" v-model="form.temperatura_motor_c" placeholder="Ej. 78" :disabled="readOnly" class="h-9 text-xs" />
          </div>

          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Inspección de Fugas</label>
            <select 
              v-model="form.fugas_lubricacion" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs outline-none"
            >
              <option value="Sin Fugas">Sin Fugas (Seco y conforme)</option>
              <option value="Fuga Leve">Fuga Leve (Por retenedor/manguera)</option>
              <option value="Fuga Critica">Fuga Crítica</option>
            </select>
          </div>

          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Tamaño Tanque (Galones)</label>
            <Input type="number" v-model="form.tamano_tanque_galones" placeholder="Ej. 48" :disabled="readOnly" class="h-9 text-xs" />
          </div>

          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Nivel Combustible (%) *</label>
            <Input type="number" min="0" max="100" v-model="form.nivel_combustible_porcentaje" placeholder="Ej. 90" :disabled="readOnly" class="h-9 text-xs font-bold text-amber-600" />
          </div>

          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Trampa de Agua Drenada</label>
            <select 
              v-model="form.trampa_agua_drenada" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs outline-none"
            >
              <option value="Si">Sí (Drenada y limpia)</option>
              <option value="No">No / No aplica</option>
            </select>
          </div>
        </div>
      </div>
    </template>

    <!-- ============================================================= -->
    <!-- CASO 2: SECCIÓN MANTENIMIENTO PREVENTIVO CLIMATIZACIÓN (AA)   -->
    <!-- ============================================================= -->
    <template v-else>
      <!-- 1. FICHA TÉCNICA AIRE ACONDICIONADO -->
      <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
        <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
          <IconWind class="w-4 h-4 text-cyan-500 stroke-[2]" />
          <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
            1. Ficha Técnica de Climatización (Aire Acondicionado)
          </span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Marca Equipo AA *</label>
            <Input v-model="form.marca_equipo" placeholder="Ej. ComfortStar, York, Carrier" :disabled="readOnly" class="h-9 text-xs" />
          </div>
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Modelo / Referencia</label>
            <Input v-model="form.modelo_equipo" placeholder="Ej. CP-24K-INV" :disabled="readOnly" class="h-9 text-xs" />
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
              class="h-9 w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 font-medium text-xs outline-none"
            >
              <option value="R410A">R410A (Ecológico)</option>
              <option value="R22">R22</option>
              <option value="R32">R32</option>
              <option value="R134a">R134a</option>
            </select>
          </div>
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Corriente Compresor (Amp)</label>
            <Input type="number" step="0.1" v-model="form.corriente_compresor_amp" placeholder="Ej. 9.8" :disabled="readOnly" class="h-9 text-xs font-mono" />
          </div>
        </div>
      </div>

      <!-- 2. PARÁMETROS DE OPERACIÓN Y SALTO TÉRMICO AA -->
      <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
        <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
          <IconSnowflake class="w-4 h-4 text-cyan-500 stroke-[2]" />
          <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
            2. Parámetros de Operación, Presiones & Salto Térmico
          </span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-4 gap-3">
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Presión Baja (PSI)</label>
            <Input type="number" v-model="form.presion_baja_psi" placeholder="Ej. 120" :disabled="readOnly" class="h-9 text-xs font-mono" />
          </div>
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Presión Alta (PSI)</label>
            <Input type="number" v-model="form.presion_alta_psi" placeholder="Ej. 350" :disabled="readOnly" class="h-9 text-xs font-mono" />
          </div>
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Temp. Inyección (°C)</label>
            <Input type="number" step="0.5" v-model="form.temperatura_inyeccion_c" placeholder="Ej. 13.5" :disabled="readOnly" class="h-9 text-xs font-mono" />
          </div>
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Temp. Retorno (°C)</label>
            <Input type="number" step="0.5" v-model="form.temperatura_retorno_c" placeholder="Ej. 23.0" :disabled="readOnly" class="h-9 text-xs font-mono" />
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2 border-t border-neutral-100 dark:border-white/5">
          <div>
            <label class="block font-bold text-neutral-600 dark:text-neutral-400 text-[10px] uppercase mb-1">Voltaje Alimentación AA (VAC)</label>
            <Input type="number" v-model="form.voltaje_alimentacion_aa" placeholder="Ej. 220" :disabled="readOnly" class="h-9 text-xs font-mono" />
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
            <input type="checkbox" v-model="form.limpieza_evaporador" true-value="Si" false-value="No" :disabled="readOnly" class="rounded text-cyan-600" />
            <span class="font-bold text-[11px] text-neutral-800 dark:text-neutral-200">Lavado Evaporador</span>
          </label>
          <label class="flex items-center gap-2 p-2.5 rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] cursor-pointer">
            <input type="checkbox" v-model="form.limpieza_condensador" true-value="Si" false-value="No" :disabled="readOnly" class="rounded text-cyan-600" />
            <span class="font-bold text-[11px] text-neutral-800 dark:text-neutral-200">Lavado Condensador</span>
          </label>
          <label class="flex items-center gap-2 p-2.5 rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] cursor-pointer">
            <input type="checkbox" v-model="form.cambio_lavado_filtros" true-value="Si" false-value="No" :disabled="readOnly" class="rounded text-cyan-600" />
            <span class="font-bold text-[11px] text-neutral-800 dark:text-neutral-200">Filtros Limpios</span>
          </label>
          <label class="flex items-center gap-2 p-2.5 rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] cursor-pointer">
            <input type="checkbox" v-model="form.desague_drenaje_ok" true-value="Si" false-value="No" :disabled="readOnly" class="rounded text-cyan-600" />
            <span class="font-bold text-[11px] text-neutral-800 dark:text-neutral-200">Drenaje Despejado</span>
          </label>
        </div>
      </div>
    </template>

    <!-- ============================================================= -->
    <!-- RESPONSABLES TÉCNICOS Y OBSERVACIONES DE CIERRE PREVENTIVO     -->
    <!-- ============================================================= -->
    <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
      <div class="flex items-center gap-2 border-b border-neutral-100 dark:border-white/5 pb-2.5">
        <IconUsers class="w-4 h-4 text-purple-500 stroke-[2]" />
        <span class="font-black text-neutral-800 dark:text-neutral-200 uppercase tracking-wider text-[11px]">
          Personal Técnico Ejecutor & Observaciones
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
            placeholder="Rutina ejecutada conforme a lista de chequeo MP, prueba 15 min con carga exitosa y caseta limpia..."
            class="w-full rounded-xl border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] p-3 text-xs focus:ring-1 focus:ring-primary outline-none leading-relaxed"
          ></textarea>
        </div>
      </div>
    </div>
  </div>
</template>

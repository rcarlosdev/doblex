<script setup>
import { reactive, watch, computed, nextTick } from 'vue';
import { 
  IconEngine, 
  IconGauge, 
  IconBatteryCharging, 
  IconWind, 
  IconSnowflake,
  IconDroplet,
  IconBolt,
  IconClock,
  IconCheck,
  IconAlertTriangle,
  IconShieldCheck,
  IconClipboardCheck,
  IconTools
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
  // ==========================================
  // 1. CAMPOS MP PLANTA ELÉCTRICA (Ref: OT5304019)
  // ==========================================
  // Datos Principales Grupo Electrógeno
  marca_equipo: 'AGG POWER SOLUTIONS',
  modelo_equipo: '',
  serial_equipo: '',
  horometro_inicial: null,
  frecuencia_hz: 60,
  capacidad_kva: 24,
  capacidad_kw: 19.2,
  velocidad_rpm: 1800,
  admision_aire: 'OK',

  // Motor Diésel
  marca_motor: 'CUMMINS',
  modelo_motor: '',
  serial_motor: '',
  presion_aceite_bar: 4.2,
  presion_aceite_psi: null,
  temperatura_aceite_c: null,
  temperatura_refrigerante_c: 80,

  // Generador Eléctrico
  marca_generador: 'STAMFORD',
  modelo_generador: '',
  serial_generador: '',
  temperatura_ambiente_c: 28,

  // Sistema de Baterías
  voltaje_bateria: 25.4,
  capacidad_bateria: 1150,
  tipo_bateria: 'Celda Húmeda',
  cantidad_baterias: 2,
  estado_bateria: 'Bueno',
  estado_cargador: 'Bueno',
  estado_bornes: 'Limpios y Ajustados',

  // Transferencia Automática (ATS)
  marca_ats: '',
  modelo_ats: '',
  serial_ats: '',
  tipo_ats: 'Automática',
  capacidad_ats_amp: 100,

  // Parámetros Eléctricos en Carga
  voltaje_l1_l2: 220,
  voltaje_l2_l3: 220,
  voltaje_l1_l3: 220,
  voltaje_l1_n: 127,
  voltaje_l2_n: 127,
  voltaje_l3_n: 127,
  corriente_l1_amp: null,
  corriente_l2_amp: null,
  corriente_l3_amp: null,
  porcentaje_cargabilidad: null,
  frecuencia_operacion_hz: 60,

  // Combustible y Tanques
  tamano_tanque_galones: 50,
  nivel_combustible_porcentaje: 80,
  estado_alarma_nivel: 'Normal',
  trampa_agua_drenada: 'Si',
  lineas_combustible_estado: 'Conforme Sin Fugas',

  // Servicio de Filtración (Lista de MP)
  cambio_aceite: 'SI',
  cambio_filtros_aire: 'SI',
  cambio_filtros_combustible: 'SI',
  cambio_filtros_aceite: 'SI',
  cambio_mangueras_precalentador: 'NO',
  cambio_refrigerante: 'SI',
  cambio_baterias: 'NO',
  galones_aceite_suministrados: null,

  // Resultados de Pruebas Operativas
  prueba_vacio: 'Bueno',
  prueba_carga: 'Bueno',
  prueba_ats_red_planta: 'Bueno',
  prueba_manual_forzada: 'Bueno',
  prueba_ats_15min: 'Exitosa con Carga',
  horometro_final_prueba: null,
  tiempo_transferencia_seg: 10,
  planta_operativa: 'Si',
  presenta_alarmas: 'No',
  alarmas_detalle: '',
  planta_temporizada: 'No',
  horario_temporizacion: '',
  alarma_externa_noc_ok: 'Si',
  requiere_cambio_cabina: 'No',
  planta_en_automatico: 'Si',

  // Checklist Subsistemas Planta
  chk_lubricacion: 'Bueno',
  chk_combustible: 'Bueno',
  chk_aspiracion: 'Bueno',
  chk_refrigeracion: 'Bueno',
  chk_escape: 'Bueno',
  chk_electrico_motor: 'Bueno',
  chk_generador: 'Bueno',
  chk_modulo_control: 'Bueno',
  chk_transferencia: 'Bueno',

  // ==========================================
  // 2. CAMPOS MP AIRE ACONDICIONADO (Ref: WO0000005520436)
  // ==========================================
  // Datos Generales AA
  marca_aa: 'MCQUAY',
  marca_aa_otro: '',
  modelo_aa: '',
  serial_aa: '',
  id_activo_fijo_aa: 'NO APLICA',
  estado_equipo_aa: 'OPERATIVO',
  tipo_aire: 'Mini Split',
  alimentacion_ac_aa: 'Bifásica',
  voltaje_entrada_aa: 220,
  corriente_aa_amp: 9.3,
  capacidad_btu_aa: 24,
  gestion_remota_ip_aa: '0',
  cantidad_compresores: 1,

  // Temperaturas y Termostato
  temperatura_cuarto_equipo: 30,
  temperatura_aa_entrada: 28,
  temperatura_aa_salida: 20,
  temp_display: 18,
  temp_termostato: 22,
  ajuste_termostato: 22,
  temp_termostato_pos_ajuste: 22,

  // Unidad Condensadora y Compresor
  compresor_marca: 'MCQUAY',
  compresor_modelo: '',
  compresor_serial: '',
  compresor_tipo: 'ROTATIVO',
  compresor_refrigerante: 'R410A',
  compresor_aislamiento_mohm: 0,
  presion_succion_psi: 100,
  presion_descarga_psi: 300,
  nivel_aceite_compresor: 'Ok',
  compresor_voltaje: 220,
  compresor_corriente: 9.3,

  condensadora_marca: 'MCQUAY',
  condensadora_modelo: '',
  condensadora_serial: '',
  temperatura_entrada_cond: 35,
  temperatura_salida_cond: 40,
  diametro_eje_cond: 0,
  diametro_aspas_cond: 0,

  // Unidad Manejadora
  manejadora_marca: 'MCQUAY',
  manejadora_modelo: '',
  manejadora_tipo: 'VERTICAL',
  tipo_filtro_aa: 'LAVABLE',
  tipo_correa_aa: 'NO APLICA',
  marca_motor_aa: 'NO VISIBLE',
  alimentacion_motor_aa: 'Bifásica',
  voltaje_motor_aa: 220,
  corriente_motor_aa: 1.5,
  aislamiento_motor_mohm: 0,
  serial_motor_aa: 'NO APLICA',
  dimensiones_blower: 0,

  // Lista de Chequeo General Aire (38 ítems de evaluación Si / No / N/A)
  chk_aa_fijacion_condensadora: 'Si',
  chk_aa_fijacion_manejadora: 'Si',
  chk_aa_anclaje_tuberias: 'Si',
  chk_aa_condiciones_fisicas: 'Si',
  chk_aa_manuales: 'No',
  chk_aa_control_remoto: 'Si',
  chk_aa_serpentin_limpio: 'Si',
  chk_aa_circulacion_aire_natural: 'Si',
  chk_aa_fugas_aire_cuarto: 'No',
  chk_aa_tuberias_buen_estado: 'Si',
  chk_aa_rejilla_direccion: 'N/A',
  chk_aa_chasis_sin_oxido: 'Si',
  chk_aa_drenaje_libre: 'Si',
  chk_aa_conexiones_electricas: 'Si',
  chk_aa_condensadora_sin_ruidos: 'Si',
  chk_aa_manejadora_sin_ruidos: 'Si',
  chk_aa_elementos_control_ok: 'Si',
  chk_aa_lubricacion_rodamientos: 'Si',
  chk_aa_ejes_chumaceras: 'N/A',
  chk_aa_tarjeta_control_ok: 'Si',
  chk_aa_sin_alarmas: 'Si',
  chk_aa_sin_fugas_refrigerante: 'Si',
  chk_aa_valvula_solenoide: 'N/A',
  chk_aa_filtros_secado: 'N/A',
  chk_aa_aislamiento_termico: 'Si',
  chk_aa_nivel_enfriamiento: 'Si',
  chk_aa_reinicio_automatico: 'Si',
  chk_aa_distribucion_aire: 'Si',
  chk_aa_display_sin_fallas: 'Si',
  chk_aa_tierra_chasis: 'Si',
  chk_aa_tierra_potencia: 'Si',
  chk_aa_ducteria: 'N/A',
  chk_aa_protecciones_electricas: 'Si',
  chk_aa_correas: 'N/A',
  chk_aa_rtu_remota: 'Si',
  chk_aa_aspa_ventilador: 'Si',
  chk_aa_seguridad_rejillas: 'N/A',
  chk_aa_drenaje_funcional: 'Si',
  chk_aa_requiere_cambio_obsolescencia: 'No',

  // Acciones Realizadas Aire (11 acciones Si / No)
  act_limpieza_serpentines: 'Si',
  act_ajuste_controles: 'No',
  act_adicion_refrigerante: 'No',
  act_correccion_drenajes: 'No',
  act_lubricacion_componentes: 'No',
  act_cambio_filtros_secado: 'No',
  act_alineacion_poleas: 'No',
  act_cambio_componentes_electronicos: 'No',
  act_cambio_compresor: 'No',
  act_cambio_correas_filtros: 'No',
  act_otras_reparaciones: 'No',

  // ==========================================
  // 3. COMÚN: OBSERVACIONES Y PLAN DE MEJORA
  // ==========================================
  plan_de_mejora: '',
  responsable_tec_1: '',
  responsable_tec_2: '',
  empresa_ejecuta: 'INMEL / DOBLEX',
  revisor_informe: '',
  ...props.modelValue
});

// Salto térmico automático en Aire Acondicionado
const saltoTermico = computed(() => {
  if (form.temperatura_aa_entrada != null && form.temperatura_aa_salida != null) {
    const diff = Number(form.temperatura_aa_entrada) - Number(form.temperatura_aa_salida);
    return isNaN(diff) ? null : diff.toFixed(1);
  }
  return null;
});

// Inicializar plan de mejora por defecto según tipo si está vacío
watch(() => props.tipoPreventivo, (tipo) => {
  if (!form.plan_de_mejora) {
    if (tipo === 'aire') {
      form.plan_de_mejora = 'Durante la ejecución del mantenimiento preventivo de climatización se realizó limpieza profunda de serpentines y filtros. Las presiones frigoríficas y salto térmico quedaron en parámetros operativos óptimos.';
    } else {
      form.plan_de_mejora = 'Durante la ejecución del mantenimiento preventivo se verificó el correcto funcionamiento del grupo electrógeno, sin evidenciar anomalías operativas. La planta queda 100% operativa y dentro de parámetros normales de funcionamiento en modo automático.';
    }
  }
}, { immediate: true });

let isInternalSync = false;

watch(form, (val) => {
  if (isInternalSync) return;
  emit('update:modelValue', { ...val });
}, { deep: true });

watch(() => props.modelValue, (newVal) => {
  if (newVal && Object.keys(newVal).length > 0) {
    if (JSON.stringify(newVal) !== JSON.stringify(form)) {
      isInternalSync = true;
      Object.assign(form, newVal);
      nextTick(() => { isInternalSync = false; });
    }
  }
}, { deep: true });
</script>

<template>
  <div class="space-y-5 text-xs select-text">

    <!-- ============================================================== -->
    <!-- CASO A: FORMATO MP AIRE ACONDICIONADO (Ref: WO0000005520436)   -->
    <!-- ============================================================== -->
    <template v-if="tipoPreventivo === 'aire'">
      <!-- Banner Identificador del Formato -->
      <div class="p-3.5 bg-sky-50 dark:bg-sky-950/40 border border-sky-200 dark:border-sky-800/60 rounded-2xl flex items-center justify-between gap-3">
        <div class="flex items-center gap-2.5">
          <div class="w-9 h-9 rounded-xl bg-sky-600 text-white flex items-center justify-center shrink-0 shadow-md">
            <IconSnowflake class="w-5 h-5 stroke-[2]" />
          </div>
          <div>
            <h4 class="font-black text-xs text-sky-950 dark:text-sky-200 uppercase tracking-wide">
              Mantenimiento Preventivo Climatización (MP-AIRE)
            </h4>
            <p class="text-[11px] text-sky-700 dark:text-sky-400 font-medium">
              Protocolo oficial de evaluación técnica, unidades y parámetros frigoríficos
            </p>
          </div>
        </div>
        <span class="text-[10px] font-mono font-bold bg-sky-200/80 dark:bg-sky-900/60 text-sky-900 dark:text-sky-300 px-2 py-0.5 rounded-md shrink-0">
          Ref. WO0000005520436
        </span>
      </div>

      <!-- SECCIÓN 1: DATOS GENERALES DEL EQUIPO DE AIRE -->
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
        <div class="flex items-center gap-2 border-b border-slate-100 dark:border-white/10 pb-2.5">
          <IconWind class="w-4 h-4 text-sky-600 dark:text-sky-400" />
          <h4 class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider">
            1. Datos Generales del Aire Acondicionado
          </h4>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Marca del Equipo *</label>
            <input
              type="text"
              v-model="form.marca_aa"
              :disabled="readOnly"
              placeholder="Ej. MCQUAY, YORK, LG, CARRIER..."
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Modelo del Equipo *</label>
            <input
              type="text"
              v-model="form.modelo_aa"
              :disabled="readOnly"
              placeholder="Ej. MQMI-17024-CWF216A"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Serial del Equipo *</label>
            <input
              type="text"
              v-model="form.serial_aa"
              :disabled="readOnly"
              placeholder="Ej. C200130208"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Tipo de Aire *</label>
            <select
              v-model="form.tipo_aire"
              :disabled="readOnly"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            >
              <option value="Mini Split">Mini Split</option>
              <option value="Paquete">Paquete</option>
              <option value="Ventana">Ventana</option>
              <option value="Multi Split">Multi Split</option>
              <option value="Precisión">Precisión</option>
              <option value="Mochila">Mochila</option>
            </select>
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Estado del Equipo *</label>
            <select
              v-model="form.estado_equipo_aa"
              :disabled="readOnly"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none font-bold"
            >
              <option value="OPERATIVO">OPERATIVO</option>
              <option value="FUERA DE SERVICIO">FUERA DE SERVICIO</option>
              <option value="STAND-BY">STAND-BY (Respaldo)</option>
            </select>
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Alimentación AC *</label>
            <select
              v-model="form.alimentacion_ac_aa"
              :disabled="readOnly"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            >
              <option value="Bifásica">Bifásica (220V)</option>
              <option value="Trifásica">Trifásica (208V / 220V)</option>
              <option value="Monofásica">Monofásica (110V)</option>
            </select>
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Voltaje Entrada (V) *</label>
            <input
              type="number"
              v-model.number="form.voltaje_entrada_aa"
              :disabled="readOnly"
              placeholder="Ej. 220"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Corriente (AMP) *</label>
            <input
              type="number"
              step="0.1"
              v-model.number="form.corriente_aa_amp"
              :disabled="readOnly"
              placeholder="Ej. 9.3"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Capacidad (BTU / KBTU) *</label>
            <input
              type="number"
              v-model.number="form.capacidad_btu_aa"
              :disabled="readOnly"
              placeholder="Ej. 24 (24000 BTU)"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            />
          </div>
        </div>
      </div>

      <!-- SECCIÓN 2: TEMPERATURAS Y TERMOSTATO -->
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-2.5">
          <div class="flex items-center gap-2">
            <IconGauge class="w-4 h-4 text-sky-600 dark:text-sky-400" />
            <h4 class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider">
              2. Temperaturas Operativas y Termostato
            </h4>
          </div>

          <!-- Badge de Salto Térmico Dinámico -->
          <div v-if="saltoTermico !== null" class="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-emerald-50 dark:bg-emerald-950/50 border border-emerald-200 dark:border-emerald-800 text-emerald-700 dark:text-emerald-300 font-mono text-xs font-black">
            <span>ΔT (Salto Térmico):</span>
            <span>{{ saltoTermico }} °C</span>
          </div>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Temp. Cuarto (°C) *</label>
            <input
              type="number"
              v-model.number="form.temperatura_cuarto_equipo"
              :disabled="readOnly"
              placeholder="Ej. 30"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Temp. AA Entrada (°C) *</label>
            <input
              type="number"
              v-model.number="form.temperatura_aa_entrada"
              :disabled="readOnly"
              placeholder="Ej. 28"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Temp. AA Salida (°C) *</label>
            <input
              type="number"
              v-model.number="form.temperatura_aa_salida"
              :disabled="readOnly"
              placeholder="Ej. 18"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Temp. Display (°C)</label>
            <input
              type="number"
              v-model.number="form.temp_display"
              :disabled="readOnly"
              placeholder="Ej. 18"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Temp. Termostato Previa</label>
            <input
              type="number"
              v-model.number="form.temp_termostato"
              :disabled="readOnly"
              placeholder="Ej. 22"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Ajuste Termostato</label>
            <input
              type="number"
              v-model.number="form.ajuste_termostato"
              :disabled="readOnly"
              placeholder="Ej. 22"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1 col-span-2">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Temp. Termostato Pos Ajuste (°C) *</label>
            <input
              type="number"
              v-model.number="form.temp_termostato_pos_ajuste"
              :disabled="readOnly"
              placeholder="Ej. 22"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs font-bold text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            />
          </div>
        </div>
      </div>

      <!-- SECCIÓN 3: UNIDAD CONDENSADORA & COMPRESOR -->
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
        <div class="flex items-center gap-2 border-b border-slate-100 dark:border-white/10 pb-2.5">
          <IconEngine class="w-4 h-4 text-sky-600 dark:text-sky-400" />
          <h4 class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider">
            3. Unidad Condensadora & Circuito Frigorífico (Compresor)
          </h4>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Tipo Compresor *</label>
            <select
              v-model="form.compresor_tipo"
              :disabled="readOnly"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            >
              <option value="ROTATIVO">ROTATIVO</option>
              <option value="SCROLL">SCROLL</option>
              <option value="RECIPROCANTE">RECIPROCANTE</option>
            </select>
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Refrigerante Ecológico *</label>
            <select
              v-model="form.compresor_refrigerante"
              :disabled="readOnly"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none font-bold"
            >
              <option value="R410A">R410A</option>
              <option value="R22">R22</option>
              <option value="R134a">R134a</option>
              <option value="R407c">R407c</option>
              <option value="R32">R32</option>
            </select>
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Presión de Succión (PSI) *</label>
            <input
              type="number"
              v-model.number="form.presion_succion_psi"
              :disabled="readOnly"
              placeholder="Ej. 100 - 120 PSI"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Presión de Descarga (PSI) *</label>
            <input
              type="number"
              v-model.number="form.presion_descarga_psi"
              :disabled="readOnly"
              placeholder="Ej. 280 - 350 PSI"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Nivel de Aceite</label>
            <select
              v-model="form.nivel_aceite_compresor"
              :disabled="readOnly"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            >
              <option value="Ok">Ok (Normal)</option>
              <option value="Bajo">Bajo</option>
              <option value="No Visible">No Visible / No Aplica</option>
            </select>
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Temp. Entrada Condensador (°C)</label>
            <input
              type="number"
              v-model.number="form.temperatura_entrada_cond"
              :disabled="readOnly"
              placeholder="Ej. 35"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            />
          </div>
        </div>
      </div>

      <!-- SECCIÓN 4: UNIDAD MANEJADORA (EVAPORADORA) -->
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
        <div class="flex items-center gap-2 border-b border-slate-100 dark:border-white/10 pb-2.5">
          <IconBolt class="w-4 h-4 text-sky-600 dark:text-sky-400" />
          <h4 class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider">
            4. Unidad Manejadora (Evaporadora / Interior)
          </h4>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Tipo Manejadora *</label>
            <select
              v-model="form.manejadora_tipo"
              :disabled="readOnly"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            >
              <option value="VERTICAL">VERTICAL (Mural / Split)</option>
              <option value="HORIZONTAL">HORIZONTAL (Ducto / Cassette)</option>
              <option value="PISO TECHO">PISO TECHO</option>
            </select>
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Tipo de Filtro *</label>
            <select
              v-model="form.tipo_filtro_aa"
              :disabled="readOnly"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            >
              <option value="LAVABLE">LAVABLE</option>
              <option value="DESECHABLE">DESECHABLE</option>
              <option value="METÁLICO">METÁLICO</option>
            </select>
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Voltaje Motor Blower (V)</label>
            <input
              type="number"
              v-model.number="form.voltaje_motor_aa"
              :disabled="readOnly"
              placeholder="Ej. 220"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-sky-500 focus:outline-none"
            />
          </div>
        </div>
      </div>

      <!-- SECCIÓN 5: LISTA DE CHEQUEO GENERAL (38 ÍTEMS DEL EXCEL) -->
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
        <div class="flex items-center gap-2 border-b border-slate-100 dark:border-white/10 pb-2.5">
          <IconClipboardCheck class="w-4 h-4 text-sky-600 dark:text-sky-400" />
          <h4 class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider">
            5. Lista de Chequeo General (Parámetros de Evaluación)
          </h4>
        </div>

        <div class="space-y-2">
          <!-- Item Helper Component Inline -->
          <div
            v-for="item in [
              { key: 'chk_aa_fijacion_condensadora', label: '1. La fijación de las unidades condensadoras es la adecuada' },
              { key: 'chk_aa_fijacion_manejadora', label: '2. La fijación de las unidades manejadoras es la adecuada' },
              { key: 'chk_aa_anclaje_tuberias', label: '3. El anclaje y fijación de tuberías es el adecuado' },
              { key: 'chk_aa_condiciones_fisicas', label: '4. Las unidades condensadoras y manejadoras se encuentran en buenas condiciones físicas' },
              { key: 'chk_aa_serpentin_limpio', label: '5. Serpentín de unidades condensadoras limpios y en buenas condiciones' },
              { key: 'chk_aa_circulacion_aire_natural', label: '6. Buena circulación de aire natural en las unidades condensadoras' },
              { key: 'chk_aa_fugas_aire_cuarto', label: '7. Existen fugas de aire acondicionado en el cuarto de telecom' },
              { key: 'chk_aa_tuberias_buen_estado', label: '8. Tuberías de conexión sin golpes, fugas de refrigerante ni corrosión' },
              { key: 'chk_aa_chasis_sin_oxido', label: '9. Chasis de las unidades libre de óxido o corrosión' },
              { key: 'chk_aa_drenaje_libre', label: '10. Tubo de drenaje del agua condensada libre de obstrucciones' },
              { key: 'chk_aa_conexiones_electricas', label: '11. Conexiones eléctricas en buenas condiciones y ajustadas' },
              { key: 'chk_aa_condensadora_sin_ruidos', label: '12. Unidad condensadora opera adecuadamente (sin ruidos ni vibraciones)' },
              { key: 'chk_aa_manejadora_sin_ruidos', label: '13. Unidad manejadora opera adecuadamente (sin ruidos extraños)' },
              { key: 'chk_aa_elementos_control_ok', label: '14. Elementos de control (pulsadores, contactores, relés) operan bien' },
              { key: 'chk_aa_tarjeta_control_ok', label: '15. Tarjeta de control de aire acondicionado opera adecuadamente' },
              { key: 'chk_aa_sin_alarmas', label: '16. Se presentan alarmas en las unidades (sonora, visual, códigos)' },
              { key: 'chk_aa_sin_fugas_refrigerante', label: '17. Se presentan fugas de refrigerante en serpentines o tuberías' },
              { key: 'chk_aa_aislamiento_termico', label: '18. Aislamiento térmico (armaflex) en buenas condiciones' },
              { key: 'chk_aa_nivel_enfriamiento', label: '19. Nivel de enfriamiento adecuado en rejillas de salida' },
              { key: 'chk_aa_reinicio_automatico', label: '20. Reinicio automático con corte de energía comercial' },
              { key: 'chk_aa_distribucion_aire', label: '21. Se garantiza la distribución uniforme de aire frío por todo el salón' },
              { key: 'chk_aa_tierra_chasis', label: '22. Chasis del aire debidamente puesto a tierra (condensadora y manejadora)' },
              { key: 'chk_aa_tierra_potencia', label: '23. Sistema de potencia y control puesto a tierra de forma adecuada' },
              { key: 'chk_aa_rtu_remota', label: '24. Gestión remota (RTU / Monitoreo) funciona adecuadamente' },
              { key: 'chk_aa_aspa_ventilador', label: '25. Aspa del ventilador en buen estado y sin deformaciones' },
              { key: 'chk_aa_drenaje_funcional', label: '26. Bandeja y drenaje funcionan adecuadamente' },
              { key: 'chk_aa_requiere_cambio_obsolescencia', label: '27. ¿El equipo de aire acondicionado requiere cambio por obsolescencia?' },
            ]"
            :key="item.key"
            class="flex items-center justify-between gap-3 p-2.5 rounded-xl border border-slate-100 dark:border-white/5 bg-slate-50/60 dark:bg-[#0a0b10] hover:bg-slate-50 transition-colors"
          >
            <span class="text-xs text-slate-700 dark:text-slate-300 font-medium leading-tight">
              {{ item.label }}
            </span>
            <div class="flex items-center gap-1 shrink-0">
              <button
                v-for="opt in ['Si', 'No', 'N/A']"
                :key="opt"
                type="button"
                :disabled="readOnly"
                @click="form[item.key] = opt"
                class="px-2.5 py-1 rounded-lg text-[10px] font-extrabold transition-all active:scale-95"
                :class="form[item.key] === opt
                  ? (opt === 'Si' ? 'bg-emerald-600 text-white' : opt === 'No' ? 'bg-rose-600 text-white' : 'bg-slate-600 text-white')
                  : 'bg-white dark:bg-neutral-900 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-white/10'"
              >
                {{ opt }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- SECCIÓN 6: ACCIONES REALIZADAS (11 ACCIONES) -->
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
        <div class="flex items-center gap-2 border-b border-slate-100 dark:border-white/10 pb-2.5">
          <IconTools class="w-4 h-4 text-sky-600 dark:text-sky-400" />
          <h4 class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider">
            6. Acciones Realizadas en la Rutina Preventiva
          </h4>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
          <div
            v-for="act in [
              { key: 'act_limpieza_serpentines', label: 'Limpieza profunda de serpentines (químico/agua)' },
              { key: 'act_ajuste_controles', label: 'Ajuste de elementos de control y contactores' },
              { key: 'act_adicion_refrigerante', label: 'Adición o carga de refrigerante ecológico' },
              { key: 'act_correccion_drenajes', label: 'Corrección y desobstrucción de drenajes' },
              { key: 'act_lubricacion_componentes', label: 'Lubricación de componentes y rodamientos' },
              { key: 'act_cambio_filtros_secado', label: 'Cambio de filtros de secado' },
              { key: 'act_alineacion_poleas', label: 'Alineación de poleas y tensión de correas' },
              { key: 'act_cambio_componentes_electronicos', label: 'Cambio de componentes electrónicos' },
              { key: 'act_cambio_compresor', label: 'Cambio de compresor' },
              { key: 'act_cambio_correas_filtros', label: 'Lavado o cambio de filtros / correas' },
              { key: 'act_otras_reparaciones', label: 'Otras reparaciones mecánicas o eléctricas' },
            ]"
            :key="act.key"
            class="flex items-center justify-between p-2.5 rounded-xl border border-slate-100 dark:border-white/5 bg-slate-50/60 dark:bg-[#0a0b10]"
          >
            <span class="text-xs text-slate-700 dark:text-slate-300 font-medium">{{ act.label }}</span>
            <div class="flex items-center gap-1 shrink-0">
              <button
                type="button"
                :disabled="readOnly"
                @click="form[act.key] = 'Si'"
                class="px-2.5 py-1 rounded-lg text-[10px] font-bold"
                :class="form[act.key] === 'Si' ? 'bg-emerald-600 text-white' : 'bg-white dark:bg-neutral-900 border border-slate-200 dark:border-white/10 text-slate-600'"
              >
                Sí
              </button>
              <button
                type="button"
                :disabled="readOnly"
                @click="form[act.key] = 'No'"
                class="px-2.5 py-1 rounded-lg text-[10px] font-bold"
                :class="form[act.key] === 'No' ? 'bg-slate-700 text-white' : 'bg-white dark:bg-neutral-900 border border-slate-200 dark:border-white/10 text-slate-600'"
              >
                No
              </button>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- ============================================================== -->
    <!-- CASO B: FORMATO MP PLANTA ELÉCTRICA (Ref: OT5304019)           -->
    <!-- ============================================================== -->
    <template v-else>
      <!-- Banner Identificador del Formato -->
      <div class="p-3.5 bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-800/60 rounded-2xl flex items-center justify-between gap-3">
        <div class="flex items-center gap-2.5">
          <div class="w-9 h-9 rounded-xl bg-red-600 text-white flex items-center justify-center shrink-0 shadow-md">
            <IconEngine class="w-5 h-5 stroke-[2]" />
          </div>
          <div>
            <h4 class="font-black text-xs text-red-950 dark:text-red-200 uppercase tracking-wide">
              Plan de Mantenimiento Sistema Grupo Electrógeno (MP-PLANTA)
            </h4>
            <p class="text-[11px] text-red-700 dark:text-red-400 font-medium">
              Protocolo oficial de evaluación técnica de planta diésel, motor, generador y ATS
            </p>
          </div>
        </div>
        <span class="text-[10px] font-mono font-bold bg-red-200/80 dark:bg-red-900/60 text-red-900 dark:text-red-300 px-2 py-0.5 rounded-md shrink-0">
          Ref. OT5304019
        </span>
      </div>

      <!-- SECCIÓN 1: DATOS PRINCIPALES DE PLANTAS -->
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
        <div class="flex items-center gap-2 border-b border-slate-100 dark:border-white/10 pb-2.5">
          <IconEngine class="w-4 h-4 text-red-600 dark:text-red-400" />
          <h4 class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider">
            1. Datos Principales de Planta Eléctrica & Motor
          </h4>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Marca Equipo *</label>
            <input
              type="text"
              v-model="form.marca_equipo"
              :disabled="readOnly"
              placeholder="Ej. AGG POWER SOLUTIONS, FG WILSON..."
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-red-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Modelo Equipo *</label>
            <input
              type="text"
              v-model="form.modelo_equipo"
              :disabled="readOnly"
              placeholder="Ej. C27D6"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-red-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Serial Equipo *</label>
            <input
              type="text"
              v-model="form.serial_equipo"
              :disabled="readOnly"
              placeholder="Ej. A1904183"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-red-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Horómetro Inicial *</label>
            <input
              type="number"
              step="0.1"
              v-model.number="form.horometro_inicial"
              :disabled="readOnly"
              placeholder="Ej. 3913.4"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs font-bold text-slate-800 dark:text-slate-200 focus:border-red-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Capacidad KVA *</label>
            <input
              type="number"
              v-model.number="form.capacidad_kva"
              :disabled="readOnly"
              placeholder="Ej. 24"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-red-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Marca Motor Diésel *</label>
            <input
              type="text"
              v-model="form.marca_motor"
              :disabled="readOnly"
              placeholder="Ej. CUMMINS, PERKINS, JOHN DEERE..."
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-red-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Modelo y Serial Motor *</label>
            <input
              type="text"
              v-model="form.modelo_motor"
              :disabled="readOnly"
              placeholder="Ej. 4B3.9-G2 | S/N 78934783"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-red-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Presión de Aceite (BAR) *</label>
            <input
              type="number"
              step="0.1"
              v-model.number="form.presion_aceite_bar"
              :disabled="readOnly"
              placeholder="Ej. 4.2 BAR"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-red-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Temp. Refrigerante (°C) *</label>
            <input
              type="number"
              v-model.number="form.temperatura_refrigerante_c"
              :disabled="readOnly"
              placeholder="Ej. 79"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-red-500 focus:outline-none"
            />
          </div>
        </div>
      </div>

      <!-- SECCIÓN 2: GENERADOR, BATERÍAS Y TRANSFERENCIA ATS -->
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
        <div class="flex items-center gap-2 border-b border-slate-100 dark:border-white/10 pb-2.5">
          <IconBatteryCharging class="w-4 h-4 text-red-600 dark:text-red-400" />
          <h4 class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider">
            2. Generador, Baterías y Transferencia Automática (ATS)
          </h4>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Marca y Serial Generador</label>
            <input
              type="text"
              v-model="form.marca_generador"
              :disabled="readOnly"
              placeholder="Ej. STAMFORD PI144D1"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-red-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Voltaje Batería de Arranque (V) *</label>
            <input
              type="number"
              step="0.1"
              v-model.number="form.voltaje_bateria"
              :disabled="readOnly"
              placeholder="Ej. 25.2 V (o 12.6V)"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs font-bold text-slate-800 dark:text-slate-200 focus:border-red-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Capacidad Batería (CCA / AH)</label>
            <input
              type="number"
              v-model.number="form.capacidad_bateria"
              :disabled="readOnly"
              placeholder="Ej. 1150"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-red-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Estado de Batería *</label>
            <select
              v-model="form.estado_bateria"
              :disabled="readOnly"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-red-500 focus:outline-none"
            >
              <option value="Bueno">Bueno (En servicio)</option>
              <option value="Regular">Regular</option>
              <option value="Malo">Malo (Requiere cambio)</option>
            </select>
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Estado del Cargador *</label>
            <select
              v-model="form.estado_cargador"
              :disabled="readOnly"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-red-500 focus:outline-none"
            >
              <option value="Bueno">Bueno (Operativo)</option>
              <option value="Averiado">Averiado / Desconectado</option>
            </select>
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Capacidad ATS (Amp) *</label>
            <input
              type="number"
              v-model.number="form.capacidad_ats_amp"
              :disabled="readOnly"
              placeholder="Ej. 100 Amp"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-red-500 focus:outline-none"
            />
          </div>
        </div>
      </div>

      <!-- SECCIÓN 3: SERVICIO DE FILTRACIÓN (LISTA DE MP) -->
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
        <div class="flex items-center gap-2 border-b border-slate-100 dark:border-white/10 pb-2.5">
          <IconDroplet class="w-4 h-4 text-red-600 dark:text-red-400" />
          <h4 class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider">
            3. Servicio de Filtración & Mantenimiento Preventivo
          </h4>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
          <div
            v-for="item in [
              { key: 'cambio_aceite', label: 'Cambio de Aceite' },
              { key: 'cambio_filtros_aire', label: 'Cambio Filtros de Aire' },
              { key: 'cambio_filtros_combustible', label: 'Cambio Filtros Combustible' },
              { key: 'cambio_filtros_aceite', label: 'Cambio Filtros de Aceite' },
              { key: 'cambio_mangueras_precalentador', label: 'Mangueras Precalentador' },
              { key: 'cambio_refrigerante', label: 'Ajuste / Cambio Refrigerante' },
              { key: 'cambio_baterias', label: 'Cambio de Baterías' },
            ]"
            :key="item.key"
            class="p-2.5 rounded-xl border border-slate-100 dark:border-white/5 bg-slate-50/60 dark:bg-[#0a0b10] flex flex-col justify-between space-y-1.5"
          >
            <span class="text-[11px] text-slate-700 dark:text-slate-300 font-bold leading-tight">{{ item.label }}</span>
            <div class="flex items-center gap-1">
              <button
                type="button"
                :disabled="readOnly"
                @click="form[item.key] = 'SI'"
                class="flex-1 py-1 rounded-md text-[10px] font-extrabold"
                :class="form[item.key] === 'SI' ? 'bg-emerald-600 text-white' : 'bg-white dark:bg-neutral-900 text-slate-500 border border-slate-200 dark:border-white/10'"
              >
                SÍ
              </button>
              <button
                type="button"
                :disabled="readOnly"
                @click="form[item.key] = 'NO'"
                class="flex-1 py-1 rounded-md text-[10px] font-extrabold"
                :class="form[item.key] === 'NO' ? 'bg-slate-700 text-white' : 'bg-white dark:bg-neutral-900 text-slate-500 border border-slate-200 dark:border-white/10'"
              >
                NO
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- SECCIÓN 4: PRUEBAS OPERATIVAS & ENCENDIDO 15 MIN -->
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
        <div class="flex items-center gap-2 border-b border-slate-100 dark:border-white/10 pb-2.5">
          <IconClock class="w-4 h-4 text-red-600 dark:text-red-400" />
          <h4 class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider">
            4. Resultado de Pruebas Operativas & Encendido ATS (15 Minutos)
          </h4>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Prueba con Carga (15 Min) *</label>
            <select
              v-model="form.prueba_ats_15min"
              :disabled="readOnly"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-red-500 focus:outline-none font-bold"
            >
              <option value="Exitosa con Carga">Exitosa con Carga</option>
              <option value="Con Novedad">Con Novedad</option>
              <option value="No Realizada">No Realizada</option>
            </select>
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">Horómetro Final Prueba</label>
            <input
              type="number"
              step="0.1"
              v-model.number="form.horometro_final_prueba"
              :disabled="readOnly"
              placeholder="Ej. 3913.6"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-red-500 focus:outline-none"
            />
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">¿Planta Queda en Automático? *</label>
            <select
              v-model="form.planta_en_automatico"
              :disabled="readOnly"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-red-500 focus:outline-none font-bold"
            >
              <option value="Si">Sí (100% Operativa)</option>
              <option value="No">No (Manual / Fuera de servicio)</option>
            </select>
          </div>

          <div class="space-y-1">
            <label class="font-bold text-[10px] text-slate-500 uppercase">¿Presenta Alarmas Activas? *</label>
            <select
              v-model="form.presenta_alarmas"
              :disabled="readOnly"
              class="w-full h-9 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:border-red-500 focus:outline-none font-bold"
            >
              <option value="No">No (Tablero Despejado)</option>
              <option value="Si">Sí (Ver detalle)</option>
            </select>
          </div>

          <div class="space-y-1 col-span-2" v-if="form.presenta_alarmas === 'Si'">
            <label class="font-bold text-[10px] text-rose-500 uppercase">Detalle de las Alarmas</label>
            <input
              type="text"
              v-model="form.alarmas_detalle"
              :disabled="readOnly"
              placeholder="Describa la alarma activa en el panel DSE / Deepsea / Cummins..."
              class="w-full h-9 rounded-lg border border-rose-300 dark:border-rose-800 bg-white dark:bg-neutral-950 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:outline-none"
            />
          </div>
        </div>
      </div>
    </template>

    <!-- ============================================================== -->
    <!-- SECCIÓN COMÚN: PLAN DE MEJORA Y OBSERVACIONES TÉCNICAS         -->
    <!-- ============================================================== -->
    <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-3 shadow-xs">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-2.5">
        <div class="flex items-center gap-2">
          <IconShieldCheck class="w-4 h-4 text-slate-700 dark:text-slate-300" />
          <h4 class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider">
            Concepto Técnico & Plan de Mejora
          </h4>
        </div>
        <span class="text-[10px] text-slate-400">Entrega de Mantenimiento</span>
      </div>

      <div class="space-y-1.5">
        <label class="font-bold text-[10px] text-slate-500 uppercase">
          Plan de Mejora / Observaciones de Cierre Preventivo *
        </label>
        <textarea
          v-model="form.plan_de_mejora"
          :disabled="readOnly"
          rows="3"
          placeholder="Escriba el concepto técnico general del mantenimiento ejecutado..."
          class="w-full rounded-xl border border-slate-200 dark:border-white/10 bg-white dark:bg-neutral-950 p-3 text-xs text-slate-800 dark:text-slate-200 focus:border-red-500 focus:outline-none leading-relaxed"
        ></textarea>
      </div>
    </div>

  </div>
</template>

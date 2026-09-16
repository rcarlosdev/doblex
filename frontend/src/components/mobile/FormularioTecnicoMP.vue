<script setup>
import { reactive, watch, computed, nextTick } from 'vue';
import PhotoUploader from '@/components/mobile/PhotoUploader.vue';
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
  IconTools,
  IconCamera
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

const getEvidenciasPorTipo = (tipo) => {
  return (props.evidencias || []).filter(e => e.tipo === tipo);
};

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
  numero_rutina_7x24: 'Rutina 1',
  ...props.modelValue
});

// Detectar si la OT corresponde a Rutina 7x24 (frecuencia decenal cada ~10 días)
const isRutina7x24 = computed(() => {
  const tp = (props.tipoPreventivo || '').toLowerCase();
  const otCode = (props.codigoOt || '').toLowerCase();
  return tp.includes('7x24') || 
         tp.includes('rutina') || 
         otCode.includes('7x24') || 
         Boolean(props.modelValue?.numero_rutina_7x24) ||
         Boolean(form.numero_rutina_7x24 && form.numero_rutina_7x24 !== '');
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

    <!-- SELECTOR DE CICLO DE RUTINA 7x24 (RUTINA 1, 2 Ó 3 - CADA ~10 DÍAS) -->
    <div 
      v-if="isRutina7x24" 
      class="p-4 sm:p-5 rounded-2xl border-2 border-indigo-200 dark:border-indigo-800/60 bg-gradient-to-br from-indigo-50/90 via-white to-indigo-50/40 dark:from-indigo-950/40 dark:via-[#121215] dark:to-indigo-950/20 shadow-sm space-y-3.5 animate-in fade-in slide-in-from-top-2 duration-300"
    >
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-indigo-100 dark:border-indigo-900/50 pb-3">
        <div class="flex items-center gap-2.5">
          <div class="w-9 h-9 rounded-xl bg-indigo-600 text-white flex items-center justify-center shadow-md shadow-indigo-600/20 shrink-0">
            <IconClock class="w-5 h-5 stroke-[2.5]" />
          </div>
          <div>
            <div class="flex items-center gap-2 flex-wrap">
              <h4 class="text-xs font-black text-indigo-950 dark:text-indigo-200 uppercase tracking-wider">
                Ciclo de Rutina 7x24
              </h4>
            </div>
            <p class="text-[11px] text-indigo-700/80 dark:text-indigo-300/80 mt-0.5">
              Seleccione la rutina correspondiente al momento de ejecución:
            </p>
          </div>
        </div>
        
        <div class="text-[11px] font-bold text-indigo-900 dark:text-indigo-300 bg-indigo-100/70 dark:bg-indigo-900/40 px-3 py-1 rounded-lg self-start sm:self-auto border border-indigo-200 dark:border-indigo-800/50">
          Ciclo Activo: <span class="font-extrabold underline decoration-indigo-500">{{ form.numero_rutina_7x24 || 'Rutina 1' }}</span>
        </div>
      </div>

      <!-- Selector Interactivo Pills / Cards: Rutina 1, Rutina 2, Rutina 3 -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
        <button
          type="button"
          :disabled="readOnly"
          @click="form.numero_rutina_7x24 = 'Rutina 1'"
          class="flex items-center gap-3 p-3 rounded-xl border transition-all text-left cursor-pointer"
          :class="form.numero_rutina_7x24 === 'Rutina 1' 
            ? 'border-indigo-600 bg-indigo-600 text-white shadow-md shadow-indigo-600/25 ring-2 ring-indigo-600/30' 
            : 'border-indigo-100 dark:border-indigo-900/40 bg-white dark:bg-[#151722] hover:border-indigo-300 text-slate-700 dark:text-slate-300'"
        >
          <div 
            class="w-8 h-8 rounded-lg flex items-center justify-center font-black text-sm shrink-0"
            :class="form.numero_rutina_7x24 === 'Rutina 1' ? 'bg-white/20 text-white' : 'bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400'"
          >
            1
          </div>
          <div class="font-black text-xs sm:text-sm">Rutina 1</div>
        </button>

        <button
          type="button"
          :disabled="readOnly"
          @click="form.numero_rutina_7x24 = 'Rutina 2'"
          class="flex items-center gap-3 p-3 rounded-xl border transition-all text-left cursor-pointer"
          :class="form.numero_rutina_7x24 === 'Rutina 2' 
            ? 'border-indigo-600 bg-indigo-600 text-white shadow-md shadow-indigo-600/25 ring-2 ring-indigo-600/30' 
            : 'border-indigo-100 dark:border-indigo-900/40 bg-white dark:bg-[#151722] hover:border-indigo-300 text-slate-700 dark:text-slate-300'"
        >
          <div 
            class="w-8 h-8 rounded-lg flex items-center justify-center font-black text-sm shrink-0"
            :class="form.numero_rutina_7x24 === 'Rutina 2' ? 'bg-white/20 text-white' : 'bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400'"
          >
            2
          </div>
          <div class="font-black text-xs sm:text-sm">Rutina 2</div>
        </button>

        <button
          type="button"
          :disabled="readOnly"
          @click="form.numero_rutina_7x24 = 'Rutina 3'"
          class="flex items-center gap-3 p-3 rounded-xl border transition-all text-left cursor-pointer"
          :class="form.numero_rutina_7x24 === 'Rutina 3' 
            ? 'border-indigo-600 bg-indigo-600 text-white shadow-md shadow-indigo-600/25 ring-2 ring-indigo-600/30' 
            : 'border-indigo-100 dark:border-indigo-900/40 bg-white dark:bg-[#151722] hover:border-indigo-300 text-slate-700 dark:text-slate-300'"
        >
          <div 
            class="w-8 h-8 rounded-lg flex items-center justify-center font-black text-sm shrink-0"
            :class="form.numero_rutina_7x24 === 'Rutina 3' ? 'bg-white/20 text-white' : 'bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400'"
          >
            3
          </div>
          <div class="font-black text-xs sm:text-sm">Rutina 3</div>
        </button>
      </div>
    </div>

    <!-- ============================================================== -->
    <!-- CASO A: FORMATO MP AIRE ACONDICIONADO (Ref: WO0000005520436)   -->
    <!-- ============================================================== -->
    <template v-if="tipoPreventivo === 'aire'">
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

        <!-- Soporte Fotográfico: Placas y Estado Previo AA -->
        <div class="pt-3 border-t border-slate-100 dark:border-white/5 space-y-2">
          <div class="flex items-center gap-1.5 text-slate-800 dark:text-slate-200">
            <IconCamera class="w-4 h-4 text-sky-600 dark:text-sky-400 stroke-[2]" />
            <span class="font-extrabold text-[11px] uppercase tracking-wider">
              Anexo Fotográfico: Placa Técnica & Estado Previo AA
            </span>
          </div>
          <PhotoUploader
            tipo="placas"
            titulo="Placa Técnica & Estado Previo AA"
            descripcion="Placa de características técnicas del equipo (evaporador/condensador) y estado físico antes del lavado."
            badge-label="Placa & Previo"
            :codigo-ot="codigoOt"
            :evidencias-list="[...getEvidenciasPorTipo('placas'), ...getEvidenciasPorTipo('antes')]"
            :read-only="readOnly"
            @photo-uploaded="emit('photo-uploaded', $event)"
            @delete-photo="emit('delete-photo', $event)"
          />
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

        <!-- Soporte Fotográfico: Mediciones Frigoríficas y Termostato -->
        <div class="pt-3 border-t border-slate-100 dark:border-white/5 space-y-2">
          <div class="flex items-center gap-1.5 text-slate-800 dark:text-slate-200">
            <IconCamera class="w-4 h-4 text-sky-600 dark:text-sky-400 stroke-[2]" />
            <span class="font-extrabold text-[11px] uppercase tracking-wider">
              Anexo Fotográfico: Mediciones Operativas y Frigoríficas
            </span>
          </div>
          <PhotoUploader
            tipo="pruebas"
            titulo="Mediciones Operativas y Frigoríficas"
            descripcion="Lectura manométrica (presión de baja/alta PSI), pinza amperimétrica (corriente compresor) y termómetro inyección/retorno."
            badge-label="Mediciones & Cierre"
            :codigo-ot="codigoOt"
            :evidencias-list="[...getEvidenciasPorTipo('pruebas'), ...getEvidenciasPorTipo('despues')]"
            :read-only="readOnly"
            @photo-uploaded="emit('photo-uploaded', $event)"
            @delete-photo="emit('delete-photo', $event)"
          />
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

        <!-- SECCIÓN 4 DEL EXCEL OFICIAL: SOPORTES MANTENIMIENTO (ANEXOS FOTOGRÁFICOS) -->
        <div class="pt-5 border-t border-slate-100 dark:border-white/5 space-y-4">
          <div class="flex items-center gap-2">
            <IconCamera class="w-5 h-5 text-sky-600 dark:text-sky-400 stroke-[2.5]" />
            <div>
              <h4 class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider">
                4. Soportes Mantenimiento (Anexos Fotográficos Oficiales Claro)
              </h4>
              <p class="text-[11px] text-slate-500 dark:text-slate-400">
                Registro fotográfico estructurado según cuadrícula oficial del formato de aire (WO0000005520436)
              </p>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
            <!-- Fila 1: Pos Mantenimiento -->
            <PhotoUploader
              tipo="condensadora_pos"
              titulo="Condensadora Pos Mantenimiento"
              descripcion="Unidad condensadora lavada a presión y desincrustada."
              badge-label="Condensadora Pos"
              badge-class="bg-sky-100 text-sky-900 border border-sky-300 dark:bg-sky-950 dark:text-sky-300 dark:border-sky-700"
              :codigo-ot="codigoOt"
              :evidencias-list="[...getEvidenciasPorTipo('condensadora_pos'), ...getEvidenciasPorTipo('mantenimiento')]"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="evaporadora_pos"
              titulo="Evaporadora Pos Mantenimiento"
              descripcion="Unidad manejadora/evaporadora limpia y bandeja despejada."
              badge-label="Evaporadora Pos"
              badge-class="bg-sky-100 text-sky-900 border border-sky-300 dark:bg-sky-950 dark:text-sky-300 dark:border-sky-700"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('evaporadora_pos')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="filtros_pos"
              titulo="Filtros Pos Mantenimiento"
              descripcion="Mallas y filtros limpios, lavados y secos."
              badge-label="Filtros Pos"
              badge-class="bg-sky-100 text-sky-900 border border-sky-300 dark:bg-sky-950 dark:text-sky-300 dark:border-sky-700"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('filtros_pos')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <!-- Fila 2: Panorámicas -->
            <PhotoUploader
              tipo="panoramica_condensadora"
              titulo="Panorámica Unidad Condensadora"
              descripcion="Vista general panorámica de la unidad condensadora exterior."
              badge-label="Panorámica Condensadora"
              badge-class="bg-slate-100 text-slate-900 border border-slate-300 dark:bg-neutral-800 dark:text-slate-200 dark:border-white/10"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('panoramica_condensadora')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="panoramica_manejadora"
              titulo="Panorámica Unidad Manejadora"
              descripcion="Vista panorámica de la manejadora/split montada en salón."
              badge-label="Panorámica Manejadora"
              badge-class="bg-slate-100 text-slate-900 border border-slate-300 dark:bg-neutral-800 dark:text-slate-200 dark:border-white/10"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('panoramica_manejadora')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="panoramica_compresor"
              titulo="Panorámica Compresor"
              descripcion="Vista del compresor dentro de la condensadora (o N/A)."
              badge-label="Panorámica Compresor"
              badge-class="bg-slate-100 text-slate-900 border border-slate-300 dark:bg-neutral-800 dark:text-slate-200 dark:border-white/10"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('panoramica_compresor')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <!-- Fila 3: Operativa y Motor -->
            <PhotoUploader
              tipo="panoramica_aa"
              titulo="Panorámica Aire Acondicionado"
              descripcion="Vista panorámica completa del sistema y entorno del sitio."
              badge-label="Panorámica General"
              badge-class="bg-slate-100 text-slate-900 border border-slate-300 dark:bg-neutral-800 dark:text-slate-200 dark:border-white/10"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('panoramica_aa')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="motor_aspa"
              titulo="Motor y Aspa Condensadora"
              descripcion="Inspección de las aspas del ventilador y motor condensador."
              badge-label="Motor & Aspa"
              badge-class="bg-amber-100 text-amber-900 border border-amber-300 dark:bg-amber-950 dark:text-amber-300 dark:border-amber-700"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('motor_aspa')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="temp_entrada"
              titulo="Temperatura Aire de Entrada"
              descripcion="Medición con pirómetro/termómetro en el retorno de aire (°C)."
              badge-label="Temp. Entrada"
              badge-class="bg-emerald-100 text-emerald-900 border border-emerald-300 dark:bg-emerald-950 dark:text-emerald-300 dark:border-emerald-700"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('temp_entrada')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <!-- Fila 4: Temperaturas y Termostato -->
            <PhotoUploader
              tipo="temp_salida"
              titulo="Temperatura Aire de Salida"
              descripcion="Medición con pirómetro en la inyección de aire frío (°C)."
              badge-label="Temp. Salida"
              badge-class="bg-emerald-100 text-emerald-900 border border-emerald-300 dark:bg-emerald-950 dark:text-emerald-300 dark:border-emerald-700"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('temp_salida')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="temp_salon"
              titulo="Temperatura Salón"
              descripcion="Medición de la temperatura ambiente general de la sala."
              badge-label="Temp. Salón"
              badge-class="bg-emerald-100 text-emerald-900 border border-emerald-300 dark:bg-emerald-950 dark:text-emerald-300 dark:border-emerald-700"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('temp_salon')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="termostato"
              titulo="Termostato / Display"
              descripcion="Display digital del termostato mostrando el setpoint (ej. 18°C/22°C)."
              badge-label="Termostato"
              badge-class="bg-emerald-100 text-emerald-900 border border-emerald-300 dark:bg-emerald-950 dark:text-emerald-300 dark:border-emerald-700"
              :codigo-ot="codigoOt"
              :evidencias-list="[...getEvidenciasPorTipo('termostato'), ...getEvidenciasPorTipo('pruebas')]"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <!-- Fila 5: Ajustes y Serial -->
            <PhotoUploader
              tipo="ajustes_mecanicos"
              titulo="Ajustes Mecánicos y Eléctricos (Unidad 1)"
              descripcion="Revisión de cableado, borneras, anclaje y componentes eléctricos."
              badge-label="Ajustes Eléctricos"
              badge-class="bg-indigo-100 text-indigo-900 border border-indigo-300 dark:bg-indigo-950 dark:text-indigo-300 dark:border-indigo-700"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('ajustes_mecanicos')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="ajustes_mecanicos_2"
              titulo="Ajustes Mecánicos y Eléctricos (Unidad 2)"
              descripcion="Fijaciones mecánicas, ductos y tuberías frigoríficas."
              badge-label="Ajustes Mecánicos"
              badge-class="bg-indigo-100 text-indigo-900 border border-indigo-300 dark:bg-indigo-950 dark:text-indigo-300 dark:border-indigo-700"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('ajustes_mecanicos_2')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="serial_elemento"
              titulo="Serial del Elemento / Placa"
              descripcion="Foto nítida del serial y modelo del aire o compresor."
              badge-label="Serial Elemento"
              badge-class="bg-purple-100 text-purple-900 border border-purple-300 dark:bg-purple-950 dark:text-purple-300 dark:border-purple-700"
              :codigo-ot="codigoOt"
              :evidencias-list="[...getEvidenciasPorTipo('serial_elemento'), ...getEvidenciasPorTipo('placas')]"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />
          </div>
        </div>
      </div>
    </template>

    <!-- ============================================================== -->
    <!-- CASO B: FORMATO MP PLANTA ELÉCTRICA (Ref: OT5304019)           -->
    <!-- ============================================================== -->
    <template v-else>
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

        <!-- Soporte Fotográfico: Placas Técnicas de Planta, Motor y Generador (Excel Claro) -->
        <div class="pt-4 border-t border-slate-100 dark:border-white/5 space-y-3">
          <div class="flex items-center gap-1.5 text-slate-800 dark:text-slate-200">
            <IconCamera class="w-4 h-4 text-red-600 dark:text-red-400 stroke-[2]" />
            <span class="font-extrabold text-[11px] uppercase tracking-wider">
              Anexo Fotográfico: Placas Técnicas de Equipos (Excel Claro)
            </span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <PhotoUploader
              tipo="placa_planta"
              titulo="Placa Planta Eléctrica"
              descripcion="Placa del grupo electrógeno (KVA, KW, modelo y serial)."
              badge-label="Placa Planta"
              badge-class="bg-purple-100 text-purple-900 border border-purple-300 dark:bg-purple-950 dark:text-purple-300 dark:border-purple-700"
              :codigo-ot="codigoOt"
              :evidencias-list="[...getEvidenciasPorTipo('placa_planta'), ...getEvidenciasPorTipo('placas')]"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="placa_motor"
              titulo="Placa Motor Diésel"
              descripcion="Placa del motor térmico (Cummins, Perkins, etc.)."
              badge-label="Placa Motor"
              badge-class="bg-purple-100 text-purple-900 border border-purple-300 dark:bg-purple-950 dark:text-purple-300 dark:border-purple-700"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('placa_motor')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="placa_generador"
              titulo="Placa Generador / Alternador"
              descripcion="Placa técnica del alternador eléctrico (Stamford, Leroy Somer)."
              badge-label="Placa Generador"
              badge-class="bg-purple-100 text-purple-900 border border-purple-300 dark:bg-purple-950 dark:text-purple-300 dark:border-purple-700"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('placa_generador')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
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

        <!-- Soporte Fotográfico: Horómetro Inicial, Cabina, Baterías y ATS (Excel Claro) -->
        <div class="pt-4 border-t border-slate-100 dark:border-white/5 space-y-3">
          <div class="flex items-center gap-1.5 text-slate-800 dark:text-slate-200">
            <IconCamera class="w-4 h-4 text-red-600 dark:text-red-400 stroke-[2]" />
            <span class="font-extrabold text-[11px] uppercase tracking-wider">
              Anexo Fotográfico: Estado Inicial, Cabina, Batería & Transferencia ATS
            </span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            <PhotoUploader
              tipo="horometro_inicial"
              titulo="Lectura Horómetro Inicial"
              descripcion="Foto nítida del contador de horas antes de arrancar la rutina."
              badge-label="Horómetro Inicial"
              badge-class="bg-amber-100 text-amber-900 border border-amber-300 dark:bg-amber-950 dark:text-amber-300 dark:border-amber-700"
              :codigo-ot="codigoOt"
              :evidencias-list="[...getEvidenciasPorTipo('horometro_inicial'), ...getEvidenciasPorTipo('inicial')]"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="panoramica_cabina"
              titulo="Panorámica Cabina / Caseta"
              descripcion="Estado físico de la insonorización, cerraduras e intemperie."
              badge-label="Cabina / Caseta"
              badge-class="bg-slate-100 text-slate-900 border border-slate-300 dark:bg-neutral-800 dark:text-slate-200 dark:border-white/10"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('panoramica_cabina')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="panoramica_bateria"
              titulo="Panorámica Batería de Arranque"
              descripcion="Bornes, sulfatación, nivel de electrolito y cableado."
              badge-label="Batería Arranque"
              badge-class="bg-purple-100 text-purple-900 border border-purple-300 dark:bg-purple-950 dark:text-purple-300 dark:border-purple-700"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('panoramica_bateria')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="panoramica_ats"
              titulo="Panorámica Transferencia (ATS)"
              descripcion="Gabinete ATS, contactores de red/planta y cableado de potencia."
              badge-label="Gabinete ATS"
              badge-class="bg-indigo-100 text-indigo-900 border border-indigo-300 dark:bg-indigo-950 dark:text-indigo-300 dark:border-indigo-700"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('panoramica_ats')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
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

        <!-- SECCIÓN DE SOPORTES FOTOGRÁFICOS DE PLANTA (SEGÚN EXCEL OFICIAL OT5304019) -->
        <div class="pt-5 border-t border-slate-100 dark:border-white/5 space-y-4">
          <div class="flex items-center gap-2">
            <IconCamera class="w-5 h-5 text-red-600 dark:text-red-400 stroke-[2.5]" />
            <div>
              <h4 class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider">
                Soportes Mantenimiento: Rutina de Filtración y Fluidos (Excel Claro OT5304019)
              </h4>
              <p class="text-[11px] text-slate-500 dark:text-slate-400">
                Evidencias fotográficas durante la ejecución de cambio de consumibles y fluidos
              </p>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
            <PhotoUploader
              tipo="filtro_aceite"
              titulo="Cambio de Filtro de Aceite"
              descripcion="Filtro nuevo instalado y retiro del filtro usado."
              badge-label="Filtro Aceite"
              badge-class="bg-blue-100 text-blue-900 border border-blue-300 dark:bg-blue-950 dark:text-blue-300 dark:border-blue-700"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('filtro_aceite')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="filtro_combustible"
              titulo="Cambio de Filtro de Combustible"
              descripcion="Sustitución de filtro principal/separador trampa de agua."
              badge-label="Filtro Combustible"
              badge-class="bg-blue-100 text-blue-900 border border-blue-300 dark:bg-blue-950 dark:text-blue-300 dark:border-blue-700"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('filtro_combustible')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="filtro_aire"
              titulo="Cambio de Filtro de Aire"
              descripcion="Limpieza de alojamiento y cartucho de aire nuevo colocado."
              badge-label="Filtro Aire"
              badge-class="bg-blue-100 text-blue-900 border border-blue-300 dark:bg-blue-950 dark:text-blue-300 dark:border-blue-700"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('filtro_aire')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="cambio_aceite"
              titulo="Cambio de Aceite (Durante Ejecución)"
              descripcion="Drenaje de lubricante usado y llenado con aceite nuevo 15W40."
              badge-label="Cambio Aceite"
              badge-class="bg-amber-100 text-amber-900 border border-amber-300 dark:bg-amber-950 dark:text-amber-300 dark:border-amber-700"
              :codigo-ot="codigoOt"
              :evidencias-list="[...getEvidenciasPorTipo('cambio_aceite'), ...getEvidenciasPorTipo('filtracion')]"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="cambio_refrigerante"
              titulo="Cambio de Refrigerante / Inspección"
              descripcion="Nivel y adición de refrigerante 50/50 en radiador/tanque."
              badge-label="Refrigerante"
              badge-class="bg-cyan-100 text-cyan-900 border border-cyan-300 dark:bg-cyan-950 dark:text-cyan-300 dark:border-cyan-700"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('cambio_refrigerante')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="nivel_aceite_final"
              titulo="Nivel de Aceite Final (Varilla)"
              descripcion="Foto de la varilla marcando nivel óptimo entre Min y Max."
              badge-label="Nivel Aceite Final"
              badge-class="bg-emerald-100 text-emerald-900 border border-emerald-300 dark:bg-emerald-950 dark:text-emerald-300 dark:border-emerald-700"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('nivel_aceite_final')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />
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

        <!-- Soporte Fotográfico: Pruebas Operativas ATS con Carga (Excel Claro) -->
        <div class="pt-4 border-t border-slate-100 dark:border-white/5 space-y-3">
          <div class="flex items-center gap-1.5 text-slate-800 dark:text-slate-200">
            <IconCamera class="w-4 h-4 text-red-600 dark:text-red-400 stroke-[2]" />
            <span class="font-extrabold text-[11px] uppercase tracking-wider">
              Anexo Fotográfico: Pruebas Operativas ATS con Carga (15 Minutos)
            </span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <PhotoUploader
              tipo="prueba_carga"
              titulo="Lectura Instrumentos con Carga"
              descripcion="Voltímetro, frecuencímetro y amperímetro durante los 15 min de prueba activa."
              badge-label="Lectura Instrumentos"
              badge-class="bg-emerald-100 text-emerald-900 border border-emerald-300 dark:bg-emerald-950 dark:text-emerald-300 dark:border-emerald-700"
              :codigo-ot="codigoOt"
              :evidencias-list="[...getEvidenciasPorTipo('prueba_carga'), ...getEvidenciasPorTipo('pruebas')]"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="horometro_final"
              titulo="Lectura Horómetro Final"
              descripcion="Registro del horómetro al culminar exitosamente la prueba con carga."
              badge-label="Horómetro Final"
              badge-class="bg-amber-100 text-amber-900 border border-amber-300 dark:bg-amber-950 dark:text-amber-300 dark:border-amber-700"
              :codigo-ot="codigoOt"
              :evidencias-list="getEvidenciasPorTipo('horometro_final')"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
            />

            <PhotoUploader
              tipo="planta_automatico"
              titulo="Tablero de Control en Automático"
              descripcion="Selector en posición AUTO, sin alarmas ni fallas activas."
              badge-label="Planta en AUTO"
              badge-class="bg-purple-100 text-purple-900 border border-purple-300 dark:bg-purple-950 dark:text-purple-300 dark:border-purple-700"
              :codigo-ot="codigoOt"
              :evidencias-list="[...getEvidenciasPorTipo('planta_automatico'), ...getEvidenciasPorTipo('despues')]"
              :read-only="readOnly"
              @photo-uploaded="emit('photo-uploaded', $event)"
              @delete-photo="emit('delete-photo', $event)"
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

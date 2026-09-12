<script setup>
import { reactive, watch, computed, ref, nextTick } from 'vue';
import { 
  IconEngine, 
  IconGauge, 
  IconBolt, 
  IconClock, 
  IconCheck, 
  IconAlertTriangle, 
  IconShieldCheck, 
  IconTools,
  IconChartBar,
  IconCircleCheck,
  IconCircleX,
  IconClipboardCheck,
  IconAward,
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

// Pestaña activa interna para navegar cómodamente en móvil
const activeSubtab = ref('ge_diagnostico'); // 'ge_diagnostico', 'megger_banco', 'spt_sistema', 'instrumentos'

const form = reactive({
  // =========================================================================
  // 1. DATOS GENERALES GE (Ref: Plantilla Inspección Técnica - Diagnósticos GE)
  // =========================================================================
  ge_estacion_base: '',
  ge_fecha_solicitud: '',
  ge_horometro: 184,
  ge_marca_planta: 'CUMMINS',
  ge_modelo_planta: '60DGCB',
  ge_estado_fisico: 'BUENO',
  ge_estado_operacional: 'OPERATIVO',
  ge_potencia_kw: 60,
  ge_consumo_kva: 75,
  ge_marca_generador: 'STAMFORD',
  ge_modelo_generador: 'NO VISIBLE',

  // Estados de los 6 Subsistemas GE
  // 1. Sistema de Generación
  ge_estado_devanado: 'REGULAR',
  ge_estado_tarjeta_avr: 'REGULAR',
  ge_estado_generador_general: 'REGULAR',
  // 2. Sistema de Combustible / Motor
  ge_estado_pistones: 'BUENO',
  ge_estado_bomba_inyeccion: 'BUENO',
  ge_estado_sistema_admision: 'BUENO',
  ge_estado_motor_general: 'BUENO',
  // 3. Sistema de Control (Análogo o Digital)
  ge_tipo_control: 'analogo', // 'analogo' o 'digital_comap'
  ge_estado_tablero_control: 'REGULAR',
  ge_estado_medidores_analogos: 'REGULAR',
  ge_estado_cableado_control: 'REGULAR',
  ge_estado_botones_paro: 'REGULAR',
  ge_estado_control_general: 'REGULAR',
  // 4. Sistema de Refrigeración
  ge_estado_radiador: 'REGULAR',
  ge_estado_ventilador: 'BUENO',
  ge_estado_bomba_agua: 'REGULAR',
  ge_estado_termostato: 'REGULAR',
  ge_estado_mangueras: 'REGULAR',
  ge_estado_sensor_temperatura: 'REGULAR',
  ge_estado_refrigerante: 'REGULAR',
  // 5. Sistema Eléctrico
  ge_estado_alternador: 'REGULAR',
  ge_estado_avr_electrico: 'REGULAR',
  ge_estado_bateria_arranque: 'REGULAR',
  ge_estado_cargador_bateria: 'REGULAR',
  ge_estado_arranque_electrico: 'REGULAR',
  ge_estado_breaker_principal: 'REGULAR',
  ge_estado_spt_planta: 'REGULAR',
  ge_estado_ats_planta: 'BUENO',
  // 6. Sistema de Escape
  ge_estado_multiple_escape: 'BUENO',
  ge_estado_tubo_escape: 'BUENO',
  ge_estado_silenciador: 'BUENO',
  ge_estado_aislantes_termicos: 'BUENO',

  // Hallazgos detallados por subsistema
  hallazgos_diagnostico_ge: [
    {
      sistema: 'Sistema de Generación',
      componente: 'Generador, Tarjeta AVR',
      descripcion: 'Deterioro en componentes electrónicos de tarjeta AVR, aislamiento bajo.',
      criticidad: 'Alta',
      accion_recomendada: 'Cambio de tarjeta AVR y mantenimiento del generador.',
      evento: 'Deterioro en generador y AVR',
      sintoma: 'Medidas bajas de megger',
      causa_raiz: 'Desgaste por tiempo de operación sin mantenimiento.',
      acciones_correctivas: 'Cambio de tarjeta AVR y barnizado/secado de bobinado.'
    }
  ],

  // =========================================================================
  // 2. PRUEBA MEGGER (AISLAMIENTO ALTERNADOR) (Ref: Plantilla 360 Simple)
  // =========================================================================
  megger_vdc_prueba: 1000,
  megger_temp_c: 84,
  megger_hr_porcentaje: 72,
  megger_r_min_criterio: 5.0, // MΩ
  megger_pi_min_criterio: 2.0,
  megger_puntos: [
    { punto: 'U – Tierra', r1min: 2.29, r10min: 3.44 },
    { punto: 'V – Tierra', r1min: 2.93, r10min: 4.40 },
    { punto: 'W – Tierra', r1min: 3.40, r10min: 5.10 },
    { punto: 'U – V', r1min: 4.93, r10min: 7.40 },
    { punto: 'V – W', r1min: 5.67, r10min: 8.50 },
    { punto: 'W – U', r1min: 6.60, r10min: 9.90 },
    { punto: 'Excitación – Tierra', r1min: null, r10min: null }
  ],
  megger_diagnostico: 'Probable humedad severa, contaminación o degradación del aislamiento (R < umbral).',
  megger_plan_accion: '1) Limpieza de bornes/terminales y secado controlado. 2) Repetir megger. 3) Si persiste: inspección interna o barnizado.',

  // =========================================================================
  // 3. PRUEBA CON BANCO RESISTIVO / CARGA (Ref: Plantilla 360 Simple)
  // =========================================================================
  banco_vnom_ll: 220,
  banco_fnom_hz: 60,
  banco_carga_objetivo_pct: 80,
  banco_lecturas: [
    { tiempo: '00:05', carga_pct: 80, v_ll: 220, hz: 60, i_prom: 145, kw: 48, temp_c: 84, presion_bar: 3.7, notas: 'Inicio de prueba. Parámetros estables.' },
    { tiempo: '00:15', carga_pct: 80, v_ll: 220, hz: 60, i_prom: 145, kw: 48, temp_c: 84, presion_bar: 3.7, notas: 'Operación normal sin alarmas.' },
    { tiempo: '00:30', carga_pct: 80, v_ll: 220, hz: 60, i_prom: 145, kw: 48, temp_c: 84, presion_bar: 3.7, notas: 'Frecuencia y voltaje estables.' },
    { tiempo: '00:45', carga_pct: 80, v_ll: 220, hz: 60, i_prom: 145, kw: 48, temp_c: 84, presion_bar: 3.7, notas: 'Sin variaciones ni vibraciones anormales.' },
    { tiempo: '01:00', carga_pct: 80, v_ll: 220, hz: 60, i_prom: 145, kw: 48, temp_c: 84, presion_bar: 3.7, notas: 'Prueba finalizada satisfactoriamente.' }
  ],
  banco_conclusion: 'APTO',
  banco_observaciones: 'Operación estable en V/Hz dentro de criterios con carga al 80%.',

  // =========================================================================
  // 4. INSPECCIÓN SISTEMA DE PUESTA A TIERRA (SPT) (Ref: Plantilla SPT)
  // =========================================================================
  // A. Resistividad Wenner
  spt_wenner_imposible: true,
  spt_wenner_motivo_imposible: 'No aplica por imposibilidad física de realizar el método (Suelo de concreto / sin área libre).',
  spt_condicion_suelo: 'Suelo de concreto',
  spt_wenner_lecturas: [
    { a: 1, r: null },
    { a: 2, r: null },
    { a: 4, r: null },
    { a: 8, r: null },
    { a: 10, r: null },
    { a: 12, r: null },
    { a: 14, r: null }
  ],

  // B. Resistencia Caída de Potencial (62%)
  spt_caida_imposible: false,
  spt_caida_criterio_max: 5.0, // Ω
  spt_r_62_medida: 4.8, // Ω medido al 62%
  spt_caida_observaciones: 'Resistencia cumple criterio RETIE/IEC (< 5 Ω).',

  // C. Equipotencialidad y Continuidad (11 Puntos)
  spt_umbral_continuidad_max: 1.0, // Ω
  spt_equipotencialidad_puntos: [
    { id: 1, elemento: 'Barra Equipotencial Principal (BEP) / Barraje de tierra', r_ohm: 0.04 },
    { id: 2, elemento: 'Rack / gabinete de ACCESO RAN (BTS/BBU/DU) – chasis', r_ohm: 0.06 },
    { id: 3, elemento: 'Rack / gabinete de TRANSMISIÓN (MW IDU / Router) – chasis', r_ohm: 0.08 },
    { id: 4, elemento: 'Gabinete RECTIFICADOR / POWER DC (-48V) – chasis', r_ohm: 0.05 },
    { id: 5, elemento: 'Banco de BATERÍAS (rack/caja y bandejas) – estructura', r_ohm: 0.05 },
    { id: 6, elemento: 'Tablero de DISTRIBUCIÓN DC (PDB / fusiblera) – carcasa', r_ohm: 0.07 },
    { id: 7, elemento: 'Tablero GENERAL AC / protecciones (TGP) – carcasa', r_ohm: 0.09 },
    { id: 8, elemento: 'TRANSFERENCIA AUTOMÁTICA (ATS) – carcasa metálica', r_ohm: 0.12 },
    { id: 9, elemento: 'GRUPO ELECTRÓGENO (chasis/bastidor + alternador)', r_ohm: 0.06 },
    { id: 10, elemento: 'AIRES ACONDICIONADOS (AA-1 y AA-2) – chasis metálico', r_ohm: 0.12 },
    { id: 11, elemento: 'Torre/estructura metálica + bajante LPS (pararrayos)', r_ohm: 0.15 }
  ],

  // =========================================================================
  // 5. INSTRUMENTOS Y CALIBRACIÓN (Ref: Plantilla 360 Simple)
  // =========================================================================
  instrumentos: [
    { tipo: 'MEGÓHMETRO', marca_modelo: 'KAIWEETS / KE2500', serial: 'KW-25091', fecha_calib: '2026-04-25', vigencia_dias: 365, certificado: 'CERT-001' },
    { tipo: 'BANCO RESISTIVO', marca_modelo: 'RESISTENCIAS Y EQUIPOS IND.', serial: 'BR-80KW-02', fecha_calib: '2026-05-05', vigencia_dias: 365, certificado: 'CERT-002' },
    { tipo: 'MULTÍMETRO DIGITAL', marca_modelo: 'ERASMUS / EMS-50', serial: '12109699', fecha_calib: '2026-04-25', vigencia_dias: 365, certificado: 'CERT-003' },
    { tipo: 'PINZA AMPERIMÉTRICA', marca_modelo: 'UNI-T / UT204+', serial: 'UT-88341', fecha_calib: '2026-04-25', vigencia_dias: 365, certificado: 'CERT-004' },
    { tipo: 'TELURÓMETRO', marca_modelo: 'KYORITSU / 4105A', serial: 'KY-4105-09', fecha_calib: '2026-04-25', vigencia_dias: 365, certificado: 'CERT-005' }
  ]
});

// Cálculos automáticos computados
const vidaUtilHoras = computed(() => {
  const h = Number(form.ge_horometro) || 0;
  return ((h / 25000) * 100).toFixed(2);
});

// Megger PI y Cumplimiento
const meggerResultados = computed(() => {
  let cumpleTotal = true;
  const evaluados = form.megger_puntos.map(p => {
    const r1 = Number(p.r1min);
    const r10 = Number(p.r10min);
    if (!r1 || !r10) return { ...p, pi: null, cumple: null };
    const pi = Number((r10 / r1).toFixed(2));
    const cumpleR = r1 >= form.megger_r_min_criterio;
    const cumplePI = pi >= form.megger_pi_min_criterio;
    const cumple = cumpleR && cumplePI;
    if (!cumple) cumpleTotal = false;
    return { ...p, pi, cumple };
  });
  return { puntos: evaluados, cumpleGlobal: cumpleTotal };
});

// Equipotencialidad Cumplimiento
const equipotencialidadResumen = computed(() => {
  let ok = 0;
  let fail = 0;
  form.spt_equipotencialidad_puntos.forEach(p => {
    if (p.r_ohm !== null && p.r_ohm !== undefined && p.r_ohm !== '') {
      if (Number(p.r_ohm) <= form.spt_umbral_continuidad_max) {
        ok++;
      } else {
        fail++;
      }
    }
  });
  return { total: form.spt_equipotencialidad_puntos.length, ok, fail, esConforme: fail === 0 && ok > 0 };
});

// Sincronización reactiva bidireccional segura (sin rebotes)
let isInternalSync = false;

watch(() => props.modelValue, (newVal) => {
  if (isInternalSync || !newVal) return;
  const currentSnap = JSON.stringify(form);
  const newSnap = JSON.stringify(newVal);
  if (currentSnap !== newSnap) {
    isInternalSync = true;
    Object.keys(newVal).forEach(key => {
      if (key in form) {
        form[key] = newVal[key];
      }
    });
    nextTick(() => { isInternalSync = false; });
  }
}, { deep: true, immediate: true });

watch(form, (newVal) => {
  if (isInternalSync) return;
  isInternalSync = true;
  emit('update:modelValue', {
    ...props.modelValue,
    ...newVal,
    rutina_tipo: '360_informe',
    megger_cumple_global: meggerResultados.value.cumpleGlobal,
    spt_equipotencialidad_conforme: equipotencialidadResumen.value.esConforme,
    vida_util_calculada_pct: vidaUtilHoras.value
  });
  nextTick(() => { isInternalSync = false; });
}, { deep: true });

const agregarHallazgoGe = () => {
  form.hallazgos_diagnostico_ge.push({
    sistema: 'Sistema Eléctrico',
    componente: '',
    descripcion: '',
    criticidad: 'Media',
    accion_recomendada: '',
    evento: '',
    sintoma: '',
    causa_raiz: '',
    acciones_correctivas: ''
  });
};

const eliminarHallazgoGe = (index) => {
  form.hallazgos_diagnostico_ge.splice(index, 1);
};
</script>

<template>
  <div class="space-y-4 text-xs select-text">
    <!-- Header Oficial Claro: Diagnóstico 360 -->
    <div class="p-3.5 bg-purple-500/10 border border-purple-500/20 rounded-2xl flex items-center justify-between flex-wrap gap-2">
      <div class="flex items-center gap-2.5">
        <div class="p-2 bg-purple-500/20 text-purple-600 dark:text-purple-400 rounded-xl">
          <IconShieldCheck class="w-5 h-5 stroke-[2]" />
        </div>
        <div>
          <h4 class="font-extrabold text-neutral-900 dark:text-white text-xs">
            Formato Técnico 360: Diagnóstico Integral GE & Sistema SPT
          </h4>
          <p class="text-[10px] text-neutral-500 dark:text-neutral-400">
            Plantillas Oficiales Claro (Diagnósticos GE SMU • SPT Wenner/Equipotencialidad • Megger & Banco 360)
          </p>
        </div>
      </div>
      <span class="px-2.5 py-0.5 rounded-full bg-purple-100 text-purple-800 dark:bg-purple-950 dark:text-purple-300 font-mono font-black text-[10px] border border-purple-300 dark:border-purple-800">
        INFORME 360
      </span>
    </div>

    <!-- Navegación por Subpestañas del Formato 360 -->
    <div class="bg-slate-100 dark:bg-[#121215] p-1 rounded-2xl border border-slate-200 dark:border-white/10 select-none">
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-1 text-center">
        <button
          type="button"
          @click="activeSubtab = 'ge_diagnostico'"
          class="flex items-center justify-center gap-1.5 py-2 px-2 rounded-xl text-xs font-bold transition-all"
          :class="activeSubtab === 'ge_diagnostico' 
            ? 'bg-purple-600 text-white shadow-sm' 
            : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-white/50 dark:hover:bg-white/5'"
        >
          <IconEngine class="w-4 h-4 stroke-[2]" />
          <span>1. Diagnóstico GE</span>
        </button>

        <button
          type="button"
          @click="activeSubtab = 'megger_banco'"
          class="flex items-center justify-center gap-1.5 py-2 px-2 rounded-xl text-xs font-bold transition-all"
          :class="activeSubtab === 'megger_banco' 
            ? 'bg-purple-600 text-white shadow-sm' 
            : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-white/50 dark:hover:bg-white/5'"
        >
          <IconBolt class="w-4 h-4 stroke-[2]" />
          <span>2. Megger & Banco</span>
        </button>

        <button
          type="button"
          @click="activeSubtab = 'spt_sistema'"
          class="flex items-center justify-center gap-1.5 py-2 px-2 rounded-xl text-xs font-bold transition-all"
          :class="activeSubtab === 'spt_sistema' 
            ? 'bg-purple-600 text-white shadow-sm' 
            : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-white/50 dark:hover:bg-white/5'"
        >
          <IconShieldCheck class="w-4 h-4 stroke-[2]" />
          <span>3. Sistema SPT</span>
        </button>

        <button
          type="button"
          @click="activeSubtab = 'instrumentos'"
          class="flex items-center justify-center gap-1.5 py-2 px-2 rounded-xl text-xs font-bold transition-all"
          :class="activeSubtab === 'instrumentos' 
            ? 'bg-purple-600 text-white shadow-sm' 
            : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-white/50 dark:hover:bg-white/5'"
        >
          <IconAward class="w-4 h-4 stroke-[2]" />
          <span>4. Instrumentos</span>
        </button>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- SUBTAB 1: DIAGNÓSTICO DETALLADO GE (6 SUBSISTEMAS) -->
    <!-- ========================================================================= -->
    <div v-show="activeSubtab === 'ge_diagnostico'" class="space-y-4">
      <!-- Ficha Técnica GE y Cálculo de Vida Útil -->
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3.5 shadow-xs">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/5 pb-2.5">
          <div class="flex items-center gap-2">
            <IconEngine class="w-4 h-4 text-purple-600 dark:text-purple-400 stroke-[2]" />
            <span class="font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider text-[11px]">
              Datos Principales del Grupo Electrógeno (Placa & Horómetro)
            </span>
          </div>
          <span class="text-[10px] font-mono font-bold text-slate-500">
            Base vida útil: 25.000 h
          </span>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div>
            <label class="block font-bold text-slate-500 text-[10px] uppercase mb-1">Fabricante Planta *</label>
            <input 
              type="text" 
              v-model="form.ge_marca_planta" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50 dark:bg-[#0a0b10] px-3 font-bold text-xs outline-none" 
            />
          </div>

          <div>
            <label class="block font-bold text-slate-500 text-[10px] uppercase mb-1">Modelo Planta</label>
            <input 
              type="text" 
              v-model="form.ge_modelo_planta" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50 dark:bg-[#0a0b10] px-3 font-mono text-xs outline-none" 
            />
          </div>

          <div>
            <label class="block font-bold text-slate-500 text-[10px] uppercase mb-1">Horómetro (h) *</label>
            <input 
              type="number" 
              v-model.number="form.ge_horometro" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50 dark:bg-[#0a0b10] px-3 font-mono font-black text-red-600 text-xs outline-none" 
            />
          </div>

          <div>
            <label class="block font-bold text-slate-500 text-[10px] uppercase mb-1">% Vida Útil (Auto)</label>
            <div class="h-9 w-full rounded-xl border border-purple-200 dark:border-purple-900/40 bg-purple-50 dark:bg-purple-950/20 px-3 flex items-center font-mono font-black text-purple-700 dark:text-purple-300 text-xs">
              {{ vidaUtilHoras }}%
            </div>
          </div>

          <div>
            <label class="block font-bold text-slate-500 text-[10px] uppercase mb-1">Estado Físico</label>
            <select 
              v-model="form.ge_estado_fisico" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50 dark:bg-[#0a0b10] px-3 font-bold text-xs outline-none"
            >
              <option value="BUENO">BUENO</option>
              <option value="REGULAR">REGULAR</option>
              <option value="MALO">MALO</option>
            </select>
          </div>

          <div>
            <label class="block font-bold text-slate-500 text-[10px] uppercase mb-1">Estado Operacional</label>
            <select 
              v-model="form.ge_estado_operacional" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50 dark:bg-[#0a0b10] px-3 font-bold text-xs outline-none"
            >
              <option value="OPERATIVO">OPERATIVO</option>
              <option value="FUERA_DE_SERVICIO">FUERA DE SERVICIO</option>
              <option value="DEGRADADO">DEGRADADO</option>
            </select>
          </div>

          <div>
            <label class="block font-bold text-slate-500 text-[10px] uppercase mb-1">Potencia (KW)</label>
            <input 
              type="number" 
              v-model.number="form.ge_potencia_kw" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50 dark:bg-[#0a0b10] px-3 font-mono text-xs outline-none" 
            />
          </div>

          <div>
            <label class="block font-bold text-slate-500 text-[10px] uppercase mb-1">Capacidad (KVA)</label>
            <input 
              type="number" 
              v-model.number="form.ge_consumo_kva" 
              :disabled="readOnly"
              class="h-9 w-full rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50 dark:bg-[#0a0b10] px-3 font-mono text-xs outline-none" 
            />
          </div>
        </div>
      </div>

      <!-- Evaluación de los 6 Subsistemas GE -->
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-4 shadow-xs">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/5 pb-2.5">
          <span class="font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider text-[11px]">
            Inspección por Subsistemas del Grupo Electrógeno (Claro MC)
          </span>
          <span class="text-[10px] font-bold text-purple-600 dark:text-purple-400">
            6 Sistemas Auditados
          </span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
          <!-- 1. Generación -->
          <div class="p-3 rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50/50 dark:bg-[#0a0b10] space-y-2">
            <span class="font-bold text-slate-900 dark:text-white block text-xs border-b border-slate-200/60 pb-1">1. Generación</span>
            <div class="space-y-1.5 text-[11px]">
              <div class="flex items-center justify-between">
                <span class="text-slate-500">Devanado:</span>
                <select v-model="form.ge_estado_devanado" :disabled="readOnly" class="h-7 rounded border bg-white dark:bg-[#121215] px-1 text-[10px] font-bold">
                  <option value="BUENO">Bueno</option><option value="REGULAR">Regular</option><option value="MALO">Malo</option>
                </select>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-slate-500">Tarjeta AVR:</span>
                <select v-model="form.ge_estado_tarjeta_avr" :disabled="readOnly" class="h-7 rounded border bg-white dark:bg-[#121215] px-1 text-[10px] font-bold">
                  <option value="BUENO">Bueno</option><option value="REGULAR">Regular</option><option value="MALO">Malo</option>
                </select>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-slate-500">Generador General:</span>
                <select v-model="form.ge_estado_generador_general" :disabled="readOnly" class="h-7 rounded border bg-white dark:bg-[#121215] px-1 text-[10px] font-bold">
                  <option value="BUENO">Bueno</option><option value="REGULAR">Regular</option><option value="MALO">Malo</option>
                </select>
              </div>
            </div>
          </div>

          <!-- 2. Combustible & Motor -->
          <div class="p-3 rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50/50 dark:bg-[#0a0b10] space-y-2">
            <span class="font-bold text-slate-900 dark:text-white block text-xs border-b border-slate-200/60 pb-1">2. Combustible & Motor</span>
            <div class="space-y-1.5 text-[11px]">
              <div class="flex items-center justify-between">
                <span class="text-slate-500">Pistones:</span>
                <select v-model="form.ge_estado_pistones" :disabled="readOnly" class="h-7 rounded border bg-white dark:bg-[#121215] px-1 text-[10px] font-bold">
                  <option value="BUENO">Bueno</option><option value="REGULAR">Regular</option><option value="MALO">Malo</option>
                </select>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-slate-500">Bomba Inyección:</span>
                <select v-model="form.ge_estado_bomba_inyeccion" :disabled="readOnly" class="h-7 rounded border bg-white dark:bg-[#121215] px-1 text-[10px] font-bold">
                  <option value="BUENO">Bueno</option><option value="REGULAR">Regular</option><option value="MALO">Malo</option>
                </select>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-slate-500">Motor General:</span>
                <select v-model="form.ge_estado_motor_general" :disabled="readOnly" class="h-7 rounded border bg-white dark:bg-[#121215] px-1 text-[10px] font-bold">
                  <option value="BUENO">Bueno</option><option value="REGULAR">Regular</option><option value="MALO">Malo</option>
                </select>
              </div>
            </div>
          </div>

          <!-- 3. Control -->
          <div class="p-3 rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50/50 dark:bg-[#0a0b10] space-y-2">
            <span class="font-bold text-slate-900 dark:text-white block text-xs border-b border-slate-200/60 pb-1">3. Sistema de Control</span>
            <div class="space-y-1.5 text-[11px]">
              <div class="flex items-center justify-between">
                <span class="text-slate-500">Tablero:</span>
                <select v-model="form.ge_estado_tablero_control" :disabled="readOnly" class="h-7 rounded border bg-white dark:bg-[#121215] px-1 text-[10px] font-bold">
                  <option value="BUENO">Bueno</option><option value="REGULAR">Regular</option><option value="MALO">Malo</option>
                </select>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-slate-500">Medidores:</span>
                <select v-model="form.ge_estado_medidores_analogos" :disabled="readOnly" class="h-7 rounded border bg-white dark:bg-[#121215] px-1 text-[10px] font-bold">
                  <option value="BUENO">Bueno</option><option value="REGULAR">Regular</option><option value="MALO">Malo</option>
                </select>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-slate-500">Cableado:</span>
                <select v-model="form.ge_estado_cableado_control" :disabled="readOnly" class="h-7 rounded border bg-white dark:bg-[#121215] px-1 text-[10px] font-bold">
                  <option value="BUENO">Bueno</option><option value="REGULAR">Regular</option><option value="MALO">Malo</option>
                </select>
              </div>
            </div>
          </div>

          <!-- 4. Refrigeración -->
          <div class="p-3 rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50/50 dark:bg-[#0a0b10] space-y-2">
            <span class="font-bold text-slate-900 dark:text-white block text-xs border-b border-slate-200/60 pb-1">4. Refrigeración</span>
            <div class="space-y-1.5 text-[11px]">
              <div class="flex items-center justify-between">
                <span class="text-slate-500">Radiador:</span>
                <select v-model="form.ge_estado_radiador" :disabled="readOnly" class="h-7 rounded border bg-white dark:bg-[#121215] px-1 text-[10px] font-bold">
                  <option value="BUENO">Bueno</option><option value="REGULAR">Regular</option><option value="MALO">Malo</option>
                </select>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-slate-500">Bomba Agua:</span>
                <select v-model="form.ge_estado_bomba_agua" :disabled="readOnly" class="h-7 rounded border bg-white dark:bg-[#121215] px-1 text-[10px] font-bold">
                  <option value="BUENO">Bueno</option><option value="REGULAR">Regular</option><option value="MALO">Malo</option>
                </select>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-slate-500">Mangueras:</span>
                <select v-model="form.ge_estado_mangueras" :disabled="readOnly" class="h-7 rounded border bg-white dark:bg-[#121215] px-1 text-[10px] font-bold">
                  <option value="BUENO">Bueno</option><option value="REGULAR">Regular</option><option value="MALO">Malo</option>
                </select>
              </div>
            </div>
          </div>

          <!-- 5. Eléctrico -->
          <div class="p-3 rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50/50 dark:bg-[#0a0b10] space-y-2">
            <span class="font-bold text-slate-900 dark:text-white block text-xs border-b border-slate-200/60 pb-1">5. Sistema Eléctrico</span>
            <div class="space-y-1.5 text-[11px]">
              <div class="flex items-center justify-between">
                <span class="text-slate-500">Alternador:</span>
                <select v-model="form.ge_estado_alternador" :disabled="readOnly" class="h-7 rounded border bg-white dark:bg-[#121215] px-1 text-[10px] font-bold">
                  <option value="BUENO">Bueno</option><option value="REGULAR">Regular</option><option value="MALO">Malo</option>
                </select>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-slate-500">Batería Arranque:</span>
                <select v-model="form.ge_estado_bateria_arranque" :disabled="readOnly" class="h-7 rounded border bg-white dark:bg-[#121215] px-1 text-[10px] font-bold">
                  <option value="BUENO">Bueno</option><option value="REGULAR">Regular</option><option value="MALO">Malo</option>
                </select>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-slate-500">ATS:</span>
                <select v-model="form.ge_estado_ats_planta" :disabled="readOnly" class="h-7 rounded border bg-white dark:bg-[#121215] px-1 text-[10px] font-bold">
                  <option value="BUENO">Bueno</option><option value="REGULAR">Regular</option><option value="MALO">Malo</option>
                </select>
              </div>
            </div>
          </div>

          <!-- 6. Escape -->
          <div class="p-3 rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50/50 dark:bg-[#0a0b10] space-y-2">
            <span class="font-bold text-slate-900 dark:text-white block text-xs border-b border-slate-200/60 pb-1">6. Sistema de Escape</span>
            <div class="space-y-1.5 text-[11px]">
              <div class="flex items-center justify-between">
                <span class="text-slate-500">Múltiple Escape:</span>
                <select v-model="form.ge_estado_multiple_escape" :disabled="readOnly" class="h-7 rounded border bg-white dark:bg-[#121215] px-1 text-[10px] font-bold">
                  <option value="BUENO">Bueno</option><option value="REGULAR">Regular</option><option value="MALO">Malo</option>
                </select>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-slate-500">Silenciador:</span>
                <select v-model="form.ge_estado_silenciador" :disabled="readOnly" class="h-7 rounded border bg-white dark:bg-[#121215] px-1 text-[10px] font-bold">
                  <option value="BUENO">Bueno</option><option value="REGULAR">Regular</option><option value="MALO">Malo</option>
                </select>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-slate-500">Aislantes / Lonas:</span>
                <select v-model="form.ge_estado_aislantes_termicos" :disabled="readOnly" class="h-7 rounded border bg-white dark:bg-[#121215] px-1 text-[10px] font-bold">
                  <option value="BUENO">Bueno</option><option value="REGULAR">Regular</option><option value="MALO">Malo</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Matriz de Hallazgos y Causa Raíz por Sistema -->
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3 shadow-xs">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/5 pb-2.5">
          <div class="flex items-center gap-2">
            <IconAlertTriangle class="w-4 h-4 text-amber-500 stroke-[2]" />
            <span class="font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider text-[11px]">
              Matriz de Hallazgos, Causa Raíz & Recomendaciones Técnicas
            </span>
          </div>
          <button
            v-if="!readOnly"
            type="button"
            @click="agregarHallazgoGe"
            class="px-2.5 py-1 bg-purple-600 hover:bg-purple-500 text-white rounded-lg text-[10px] font-bold flex items-center gap-1 cursor-pointer transition-all"
          >
            <IconPlus class="w-3.5 h-3.5 stroke-[2.5]" />
            <span>+ Agregar Hallazgo</span>
          </button>
        </div>

        <div v-if="form.hallazgos_diagnostico_ge.length === 0" class="text-center py-6 text-slate-400">
          Sin hallazgos críticos reportados en los subsistemas del grupo electrógeno.
        </div>

        <div v-else class="space-y-3">
          <div 
            v-for="(h, hIdx) in form.hallazgos_diagnostico_ge" 
            :key="hIdx"
            class="p-3 rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50 dark:bg-[#0a0b10] space-y-2 relative"
          >
            <button
              v-if="!readOnly"
              type="button"
              @click="eliminarHallazgoGe(hIdx)"
              class="absolute top-2.5 right-2.5 p-1 text-slate-400 hover:text-rose-600 transition-colors cursor-pointer"
              title="Eliminar hallazgo"
            >
              <IconTrash class="w-4 h-4" />
            </button>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 pr-8">
              <div>
                <label class="block text-[10px] font-bold text-slate-500 uppercase">Sistema Afectado</label>
                <select v-model="h.sistema" :disabled="readOnly" class="h-8 w-full rounded-lg border bg-white dark:bg-[#121215] px-2 text-xs font-bold">
                  <option value="Sistema de Generación">Sistema de Generación</option>
                  <option value="Sistema de Combustible">Sistema de Combustible</option>
                  <option value="Sistema de Control">Sistema de Control</option>
                  <option value="Sistema de Refrigeración">Sistema de Refrigeración</option>
                  <option value="Sistema Eléctrico">Sistema Eléctrico</option>
                  <option value="Sistema de Escape">Sistema de Escape</option>
                </select>
              </div>

              <div>
                <label class="block text-[10px] font-bold text-slate-500 uppercase">Componente</label>
                <input type="text" v-model="h.componente" :disabled="readOnly" placeholder="Ej. Tarjeta AVR, Bomba de agua" class="h-8 w-full rounded-lg border bg-white dark:bg-[#121215] px-2 text-xs" />
              </div>

              <div>
                <label class="block text-[10px] font-bold text-slate-500 uppercase">Criticidad</label>
                <select v-model="h.criticidad" :disabled="readOnly" class="h-8 w-full rounded-lg border bg-white dark:bg-[#121215] px-2 text-xs font-bold">
                  <option value="Alta">Alta</option>
                  <option value="Media">Media</option>
                  <option value="Baja">Baja</option>
                </select>
              </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
              <div>
                <label class="block text-[10px] font-bold text-slate-500 uppercase mb-0.5">Descripción del Hallazgo</label>
                <textarea v-model="h.descripcion" :disabled="readOnly" rows="2" class="w-full rounded-lg border bg-white dark:bg-[#121215] p-2 text-xs leading-relaxed resize-none"></textarea>
              </div>
              <div>
                <label class="block text-[10px] font-bold text-slate-500 uppercase mb-0.5">Causa Raíz & Acción Correctiva</label>
                <textarea v-model="h.acciones_correctivas" :disabled="readOnly" rows="2" placeholder="Detalle la causa raíz y la recomendación técnica para MC..." class="w-full rounded-lg border bg-white dark:bg-[#121215] p-2 text-xs leading-relaxed resize-none"></textarea>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- SUBTAB 2: MEGGER (AISLAMIENTO) & BANCO RESISTIVO (CARGA) -->
    <!-- ========================================================================= -->
    <div v-show="activeSubtab === 'megger_banco'" class="space-y-4">
      <!-- Prueba MEGGER Alternador -->
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3.5 shadow-xs">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/5 pb-2.5 flex-wrap gap-2">
          <div class="flex items-center gap-2">
            <IconBolt class="w-4 h-4 text-purple-600 dark:text-purple-400 stroke-[2]" />
            <span class="font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider text-[11px]">
              Prueba MEGGER: Aislamiento del Alternador (Ref: Plantilla 360 Simple)
            </span>
          </div>
          <span 
            class="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-black"
            :class="meggerResultados.cumpleGlobal ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300'"
          >
            {{ meggerResultados.cumpleGlobal ? 'CUMPLE AISLAMIENTO' : 'NO APTO (R / PI BAJA)' }}
          </span>
        </div>

        <!-- Parámetros de prueba -->
        <div class="grid grid-cols-3 sm:grid-cols-5 gap-2 text-xs">
          <div class="p-2 rounded-xl bg-slate-50 dark:bg-[#0a0b10] border">
            <span class="text-[9px] text-slate-400 font-bold block uppercase">Vdc Prueba</span>
            <span class="font-mono font-black text-slate-800 dark:text-slate-200">1000 V</span>
          </div>
          <div class="p-2 rounded-xl bg-slate-50 dark:bg-[#0a0b10] border">
            <span class="text-[9px] text-slate-400 font-bold block uppercase">Temp. Operación</span>
            <input type="number" v-model.number="form.megger_temp_c" :disabled="readOnly" class="font-mono font-bold text-slate-800 dark:text-slate-200 w-full bg-transparent outline-none" />
          </div>
          <div class="p-2 rounded-xl bg-slate-50 dark:bg-[#0a0b10] border">
            <span class="text-[9px] text-slate-400 font-bold block uppercase">Humedad HR (%)</span>
            <input type="number" v-model.number="form.megger_hr_porcentaje" :disabled="readOnly" class="font-mono font-bold text-slate-800 dark:text-slate-200 w-full bg-transparent outline-none" />
          </div>
          <div class="p-2 rounded-xl bg-slate-50 dark:bg-[#0a0b10] border">
            <span class="text-[9px] text-slate-400 font-bold block uppercase">Criterio R Mín.</span>
            <span class="font-mono font-bold text-slate-800 dark:text-slate-200">≥ 5.0 MΩ</span>
          </div>
          <div class="p-2 rounded-xl bg-slate-50 dark:bg-[#0a0b10] border">
            <span class="text-[9px] text-slate-400 font-bold block uppercase">Criterio PI Mín.</span>
            <span class="font-mono font-bold text-slate-800 dark:text-slate-200">≥ 2.0</span>
          </div>
        </div>

        <!-- Tabla de Puntos U-V-W vs Tierra -->
        <div class="overflow-x-auto border border-slate-200 dark:border-white/10 rounded-xl">
          <table class="w-full text-xs text-left">
            <thead class="bg-slate-100 dark:bg-white/5 text-[10px] font-black uppercase text-slate-500 border-b">
              <tr>
                <th class="py-2 px-3">Punto de Prueba</th>
                <th class="py-2 px-3 text-right">R @ 1 min (MΩ)</th>
                <th class="py-2 px-3 text-right">R @ 10 min (MΩ)</th>
                <th class="py-2 px-3 text-center">PI (Calculado)</th>
                <th class="py-2 px-3 text-center">Estado</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-white/5">
              <tr v-for="(p, pIdx) in meggerResultados.puntos" :key="pIdx" class="hover:bg-slate-50 dark:hover:bg-white/[0.02]">
                <td class="py-2 px-3 font-bold text-slate-800 dark:text-slate-200">{{ p.punto }}</td>
                <td class="py-2 px-3 text-right">
                  <input 
                    type="number" 
                    step="0.01"
                    v-model.number="form.megger_puntos[pIdx].r1min" 
                    :disabled="readOnly"
                    class="w-20 text-right font-mono font-bold h-7 rounded border px-1.5 bg-white dark:bg-[#121215] outline-none" 
                  />
                </td>
                <td class="py-2 px-3 text-right">
                  <input 
                    type="number" 
                    step="0.01"
                    v-model.number="form.megger_puntos[pIdx].r10min" 
                    :disabled="readOnly"
                    class="w-20 text-right font-mono font-bold h-7 rounded border px-1.5 bg-white dark:bg-[#121215] outline-none" 
                  />
                </td>
                <td class="py-2 px-3 text-center font-mono font-black text-slate-800 dark:text-slate-200">
                  {{ p.pi !== null ? p.pi : 'N/A' }}
                </td>
                <td class="py-2 px-3 text-center">
                  <span 
                    v-if="p.cumple !== null"
                    class="px-2 py-0.5 rounded text-[10px] font-black"
                    :class="p.cumple ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300'"
                  >
                    {{ p.cumple ? 'CUMPLE' : 'NO CUMPLE' }}
                  </span>
                  <span v-else class="text-[10px] text-slate-400 italic">-</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Prueba con Banco Resistivo / Carga (Bitácora Horaria) -->
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3.5 shadow-xs">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/5 pb-2.5">
          <div class="flex items-center gap-2">
            <IconGauge class="w-4 h-4 text-purple-600 dark:text-purple-400 stroke-[2]" />
            <span class="font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider text-[11px]">
              Prueba con Banco Resistivo (Bitácora de Carga 1 Hora)
            </span>
          </div>
          <span class="text-[10px] font-bold text-emerald-600 dark:text-emerald-400">
            Carga Objetivo: {{ form.banco_carga_objetivo_pct }}%
          </span>
        </div>

        <div class="overflow-x-auto border border-slate-200 dark:border-white/10 rounded-xl">
          <table class="w-full text-xs text-left">
            <thead class="bg-slate-100 dark:bg-white/5 text-[10px] font-black uppercase text-slate-500 border-b">
              <tr>
                <th class="py-2 px-2.5">Tiempo</th>
                <th class="py-2 px-2 text-right">% Carga</th>
                <th class="py-2 px-2 text-right">V L-L</th>
                <th class="py-2 px-2 text-right">Hz</th>
                <th class="py-2 px-2 text-right">I Prom (A)</th>
                <th class="py-2 px-2 text-right">KW</th>
                <th class="py-2 px-2 text-right">T° Ref</th>
                <th class="py-2 px-2 text-right">P. Aceite</th>
                <th class="py-2 px-2.5">Observación / Notas</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-white/5 font-mono">
              <tr v-for="(b, bIdx) in form.banco_lecturas" :key="bIdx">
                <td class="py-2 px-2.5 font-bold text-slate-800 dark:text-slate-200">{{ b.tiempo }}</td>
                <td class="py-2 px-2 text-right">{{ b.carga_pct }}%</td>
                <td class="py-2 px-2 text-right">
                  <input type="number" v-model.number="b.v_ll" :disabled="readOnly" class="w-14 text-right h-6 rounded border px-1 bg-white dark:bg-[#121215]" />
                </td>
                <td class="py-2 px-2 text-right">
                  <input type="number" v-model.number="b.hz" :disabled="readOnly" class="w-12 text-right h-6 rounded border px-1 bg-white dark:bg-[#121215]" />
                </td>
                <td class="py-2 px-2 text-right">
                  <input type="number" v-model.number="b.i_prom" :disabled="readOnly" class="w-14 text-right h-6 rounded border px-1 bg-white dark:bg-[#121215]" />
                </td>
                <td class="py-2 px-2 text-right">
                  <input type="number" v-model.number="b.kw" :disabled="readOnly" class="w-14 text-right h-6 rounded border px-1 bg-white dark:bg-[#121215]" />
                </td>
                <td class="py-2 px-2 text-right">
                  <input type="number" v-model.number="b.temp_c" :disabled="readOnly" class="w-12 text-right h-6 rounded border px-1 bg-white dark:bg-[#121215]" />
                </td>
                <td class="py-2 px-2 text-right">
                  <input type="number" step="0.1" v-model.number="b.presion_bar" :disabled="readOnly" class="w-14 text-right h-6 rounded border px-1 bg-white dark:bg-[#121215]" />
                </td>
                <td class="py-2 px-2.5 font-sans">
                  <input type="text" v-model="b.notas" :disabled="readOnly" class="w-full text-xs h-6 rounded border px-1.5 bg-white dark:bg-[#121215]" />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- SUBTAB 3: SISTEMA DE PUESTA A TIERRA (SPT) (WENNER & EQUIPOTENCIALIDAD) -->
    <!-- ========================================================================= -->
    <div v-show="activeSubtab === 'spt_sistema'" class="space-y-4">
      <!-- 1. Resistividad Wenner -->
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3.5 shadow-xs">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/5 pb-2.5">
          <div class="flex items-center gap-2">
            <IconShieldCheck class="w-4 h-4 text-purple-600 dark:text-purple-400 stroke-[2]" />
            <span class="font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider text-[11px]">
              1. Resistividad del Terreno (Método Wenner - 4 Electrodos)
            </span>
          </div>
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" v-model="form.spt_wenner_imposible" :disabled="readOnly" class="rounded text-purple-600" />
            <span class="text-[10px] font-bold text-amber-600">Imposibilidad física en sitio</span>
          </label>
        </div>

        <div v-if="form.spt_wenner_imposible" class="p-3 rounded-xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 text-amber-800 dark:text-amber-300 text-xs">
          <span class="font-bold block mb-1">Observación técnica registrada:</span>
          {{ form.spt_wenner_motivo_imposible }}
        </div>

        <div v-else class="space-y-2">
          <p class="text-[11px] text-slate-500">
            Medición de resistividad aparente del terreno mediante 4 electrodos alineados equidistantes (C1-P1-P2-C2).
          </p>
        </div>
      </div>

      <!-- 2. Resistencia Eléctrica SPT (Caída de Potencial 62%) -->
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3.5 shadow-xs">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/5 pb-2.5">
          <div class="flex items-center gap-2">
            <IconBolt class="w-4 h-4 text-purple-600 dark:text-purple-400 stroke-[2]" />
            <span class="font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider text-[11px]">
              2. Resistencia del SPT (Método Caída de Potencial 62%)
            </span>
          </div>
          <span 
            class="px-2 py-0.5 rounded text-[10px] font-black"
            :class="Number(form.spt_r_62_medida) < form.spt_caida_criterio_max ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300'"
          >
            {{ Number(form.spt_r_62_medida) < form.spt_caida_criterio_max ? 'APTO RETIE/IEC' : 'NO CONFORME' }}
          </span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 items-center text-xs">
          <div class="p-2.5 rounded-xl bg-slate-50 dark:bg-[#0a0b10] border">
            <span class="text-[10px] text-slate-400 font-bold block uppercase">Criterio Normativo</span>
            <span class="font-mono font-black text-slate-800 dark:text-slate-200">&lt; 5.0 Ω</span>
          </div>

          <div class="p-2.5 rounded-xl bg-slate-50 dark:bg-[#0a0b10] border">
            <span class="text-[10px] text-slate-400 font-bold block uppercase">Resistencia al 62% (Ω) *</span>
            <input 
              type="number" 
              step="0.01"
              v-model.number="form.spt_r_62_medida" 
              :disabled="readOnly"
              class="w-full text-left font-mono font-black text-purple-600 dark:text-purple-400 text-sm bg-transparent outline-none mt-0.5" 
            />
          </div>

          <div class="p-2.5 rounded-xl bg-slate-50 dark:bg-[#0a0b10] border">
            <span class="text-[10px] text-slate-400 font-bold block uppercase">Observación</span>
            <span class="text-[11px] font-medium text-slate-600 dark:text-slate-300 block truncate">{{ form.spt_caida_observaciones }}</span>
          </div>
        </div>
      </div>

      <!-- 3. Equipotencialidad y Continuidad (11 Puntos) -->
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3.5 shadow-xs">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/5 pb-2.5 flex-wrap gap-2">
          <div>
            <span class="font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider text-[11px]">
              3. Matriz de Equipotencialidad & Continuidad (11 Puntos Clave)
            </span>
            <p class="text-[10px] text-slate-400">
              Punto de Referencia: Barra Equipotencial Principal (BEP). Umbral: ≤ {{ form.spt_umbral_continuidad_max }} Ω
            </p>
          </div>
          <span 
            class="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-black"
            :class="equipotencialidadResumen.esConforme ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300'"
          >
            {{ equipotencialidadResumen.ok }} / {{ equipotencialidadResumen.total }} Conformes
          </span>
        </div>

        <div class="overflow-x-auto border border-slate-200 dark:border-white/10 rounded-xl">
          <table class="w-full text-xs text-left">
            <thead class="bg-slate-100 dark:bg-white/5 text-[10px] font-black uppercase text-slate-500 border-b">
              <tr>
                <th class="py-2 px-3">#</th>
                <th class="py-2 px-3">Elemento / Punto de Estación</th>
                <th class="py-2 px-3 text-right">Medida (Ω)</th>
                <th class="py-2 px-3 text-center">Estado</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-white/5">
              <tr v-for="(item, idx) in form.spt_equipotencialidad_puntos" :key="item.id" class="hover:bg-slate-50 dark:hover:bg-white/[0.02]">
                <td class="py-2 px-3 font-mono text-slate-400">{{ idx + 1 }}</td>
                <td class="py-2 px-3 font-medium text-slate-800 dark:text-slate-200">{{ item.elemento }}</td>
                <td class="py-2 px-3 text-right">
                  <input 
                    type="number" 
                    step="0.01"
                    v-model.number="item.r_ohm" 
                    :disabled="readOnly"
                    class="w-20 text-right font-mono font-bold h-7 rounded border px-1.5 bg-white dark:bg-[#121215] outline-none" 
                  />
                </td>
                <td class="py-2 px-3 text-center">
                  <span 
                    v-if="item.r_ohm !== null && item.r_ohm !== undefined && item.r_ohm !== ''"
                    class="px-2 py-0.5 rounded text-[10px] font-black"
                    :class="Number(item.r_ohm) <= form.spt_umbral_continuidad_max ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300'"
                  >
                    {{ Number(item.r_ohm) <= form.spt_umbral_continuidad_max ? 'CUMPLE' : 'NO CUMPLE' }}
                  </span>
                  <span v-else class="text-[10px] text-slate-400 italic">-</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- SUBTAB 4: INSTRUMENTOS Y CALIBRACIONES (CERTIFICADOS) -->
    <!-- ========================================================================= -->
    <div v-show="activeSubtab === 'instrumentos'" class="space-y-4">
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3.5 shadow-xs">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/5 pb-2.5">
          <div class="flex items-center gap-2">
            <IconAward class="w-4 h-4 text-purple-600 dark:text-purple-400 stroke-[2]" />
            <span class="font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider text-[11px]">
              Instrumentos de Medición & Certificados de Calibración
            </span>
          </div>
          <span class="text-[10px] font-mono font-bold text-emerald-600 dark:text-emerald-400">
            Trazabilidad Documental Obligatoria
          </span>
        </div>

        <div class="overflow-x-auto border border-slate-200 dark:border-white/10 rounded-xl">
          <table class="w-full text-xs text-left">
            <thead class="bg-slate-100 dark:bg-white/5 text-[10px] font-black uppercase text-slate-500 border-b">
              <tr>
                <th class="py-2.5 px-3">Instrumento</th>
                <th class="py-2.5 px-3">Marca / Modelo</th>
                <th class="py-2.5 px-3">Serial</th>
                <th class="py-2.5 px-3">Fecha Calib.</th>
                <th class="py-2.5 px-3 text-center">Código Certificado</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-white/5">
              <tr v-for="(inst, iIdx) in form.instrumentos" :key="iIdx" class="hover:bg-slate-50 dark:hover:bg-white/[0.02]">
                <td class="py-2.5 px-3 font-bold text-slate-800 dark:text-slate-200">{{ inst.tipo }}</td>
                <td class="py-2.5 px-3">
                  <input type="text" v-model="inst.marca_modelo" :disabled="readOnly" class="h-7 w-full rounded border px-1.5 bg-white dark:bg-[#121215] text-xs" />
                </td>
                <td class="py-2.5 px-3">
                  <input type="text" v-model="inst.serial" :disabled="readOnly" class="h-7 w-full font-mono rounded border px-1.5 bg-white dark:bg-[#121215] text-xs" />
                </td>
                <td class="py-2.5 px-3">
                  <input type="date" v-model="inst.fecha_calib" :disabled="readOnly" class="h-7 rounded border px-1.5 bg-white dark:bg-[#121215] text-xs font-mono" />
                </td>
                <td class="py-2.5 px-3 text-center font-mono font-bold text-purple-600">
                  <input type="text" v-model="inst.certificado" :disabled="readOnly" class="h-7 w-24 text-center rounded border px-1.5 bg-white dark:bg-[#121215] text-xs font-mono font-bold" />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

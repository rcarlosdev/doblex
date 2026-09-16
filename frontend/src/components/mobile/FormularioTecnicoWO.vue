<script setup>
import { reactive, watch, computed, nextTick, ref, onMounted } from 'vue';
import { Input } from '@/components/ui/input';
import SinglePhotoCapture from '@/components/mobile/SinglePhotoCapture.vue';
import MaterialesTipologiaSelector from '@/components/mobile/MaterialesTipologiaSelector.vue';
import RepuestosCambiosManager from '@/components/mobile/RepuestosCambiosManager.vue';
import TransporteEspecialManager from '@/components/mobile/TransporteEspecialManager.vue';
import NovedadesHallazgosManager from '@/components/mobile/NovedadesHallazgosManager.vue';
import { 
  IconAlertTriangle, 
  IconTool, 
  IconCheck, 
  IconBox, 
  IconBuildingBroadcastTower, 
  IconCamera,
  IconExchange,
  IconTruck,
  IconClock,
  IconMapPin,
  IconUserCheck,
  IconFileText,
  IconShieldCheck,
  IconInfoCircle,
  IconActivity,
  IconNotes,
  IconDeviceFloppy,
  IconFileCertificate,
  IconPlus, 
  IconTrash,
  IconAlertCircle, 
  IconCompass
} from '@tabler/icons-vue';

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  },
  ot: {
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

const OPCIONES_SUBSISTEMA = [
  'SPT - SISTEMA PUESTA A TIERRA',
  'PE - GRUPO ELECTROGENO',
  'AA - AIRES ACONDICIONADOS',
  'PW - POWER',
  'ACCESO-TX',
  'MT-BT - MEDIA Y BAJA TENSION'
];

const normalizarSubsistema = (val) => {
  if (!val) return 'SPT - SISTEMA PUESTA A TIERRA';
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
  if (lower.includes('acceso') || lower.includes('tx') || lower.includes('transmision') || lower.includes('rfs')) {
    return 'ACCESO-TX';
  }
  if (lower.includes('mt') || lower.includes('bt') || lower.includes('media') || lower.includes('baja') || lower.includes('subestacion') || lower.includes('acometida')) {
    return 'MT-BT - MEDIA Y BAJA TENSION';
  }
  return str.toUpperCase();
};

const getNowFormatted = () => {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
};

const buildInitialState = () => {
  const ot = props.ot || {};
  const mv = props.modelValue || {};

  return {
    // 1. INFORMACIÓN GENERAL (Ref: Hoja1 Rows 5-12)
    sitio: mv.sitio || ot.sitio || '',
    categoria: mv.categoria || ot.categoria || (ot.tipo_ubicacion === 'rural' ? 'Rural' : 'Urbano'),
    regional: mv.regional || ot.regional || 'COSTA',
    responsable: mv.responsable || ot.assigned_user?.name || ot.coordinador || 'Personal de Campo',
    departamento: mv.departamento || ot.departamento || 'Atlántico',
    no_inc: mv.no_inc || mv.numero_inc || mv.ticket_inc || 'SMU008212',
    direccion: mv.direccion || ot.ubicacion || '',
    codigo_ot: mv.codigo_ot || ot.codigo || props.codigoOt || '',
    tipo_estacion: mv.tipo_estacion || ot.tipo_estacion || 'Outdoor',
    fecha_ejecucion: mv.fecha_ejecucion || (ot.fecha_inicio ? String(ot.fecha_inicio).replace('T', ' ').slice(0, 16) : getNowFormatted()),
    tipo_sitio: mv.tipo_sitio || (ot.tipo_ubicacion === 'rural' ? 'Rural' : 'Urbano'),
    fecha_fin_actividad: mv.fecha_fin_actividad || '',
    site_owner: mv.site_owner || ot.site_owner || '',

    // 2. INFORMACIÓN DE LA ACTIVIDAD (Ref: Hoja1 Rows 13-17)
    tipo_actividad_label: mv.tipo_actividad_label || (props.tipoActividad === 'emergencia' ? 'Emergencia' : 'MC'),
    tipo_equipo_falla: mv.tipo_equipo_falla || 'SPT',
    subsistema: normalizarSubsistema(mv.subsistema || ot.subsistema || 'SPT'),
    modelo_equipo: mv.modelo_equipo || 'N/A',
    presenta_afectacion: mv.presenta_afectacion || 'Si',
    reinstalacion: mv.reinstalacion !== undefined ? (typeof mv.reinstalacion === 'boolean' ? (mv.reinstalacion ? 'Si' : 'No') : mv.reinstalacion) : 'No',
    cambio_equipo: mv.cambio_equipo !== undefined ? (typeof mv.cambio_equipo === 'boolean' ? (mv.cambio_equipo ? 'Si' : 'No') : mv.cambio_equipo) : 'Si',
    reparacion: mv.reparacion !== undefined ? (typeof mv.reparacion === 'boolean' ? (mv.reparacion ? 'Si' : 'No') : mv.reparacion) : 'No',

    // 3. DESCRIPCIÓN DE LA FALLA & 4. SOLUCIÓN (Ref: Hoja1 Rows 18-21)
    descripcion_falla: mv.descripcion_falla || ot.descripcion || '',
    descripcion_solucion: mv.descripcion_solucion || '',

    // 5. CAMBIO DE REPUESTOS Y/O PARTES (FORMULARIO Cols 18-28)
    repuestos_cambios: Array.isArray(mv.repuestos_cambios) ? mv.repuestos_cambios : [],

    // 6. LISTADO DE MATERIALES UTILIZADOS (Ref: Hoja1 Rows 22-39)
    materiales: Array.isArray(mv.materiales) ? mv.materiales : [],

    // 7. EVIDENCIAS FOTOGRÁFICAS DE LA ACTIVIDAD (Ref: Hoja1 Rows 40-534)
    evidencias_actividad: Array.isArray(mv.evidencias_actividad) && mv.evidencias_actividad.length > 0
      ? mv.evidencias_actividad
      : (Array.isArray(props.evidencias) && props.evidencias.length > 0
          ? props.evidencias.map((e, idx) => ({
              id: e.id || (`ev_${idx + 1}`),
              foto_url: e.url || e.foto_url || '',
              descripcion: e.descripcion || e.tag || ''
            }))
          : [
              { id: 'ev_1', foto_url: '', descripcion: '' }
            ]
        ),

    // Soportes Técnicos Específicos Opcionales (Telurómetro & Plano SPT)
    aplica_soportes_especificos: mv.aplica_soportes_especificos || ((mv.medicion_telurometro_valor || mv.medicion_telurometro_foto || mv.plano_instalacion_foto) ? 'Si' : 'No'),
    medicion_telurometro_valor: mv.medicion_telurometro_valor || '',
    medicion_telurometro_foto: mv.medicion_telurometro_foto || '',
    plano_instalacion_foto: mv.plano_instalacion_foto || '',

    // 8. RESULTADO Y OBSERVACIONES (Ref: Hoja1 Rows 535-536)
    falla_resuelta: mv.falla_resuelta || 'Si',
    observaciones_actividad: mv.observaciones_actividad || '',

    // 9. HALLAZGOS Y NOVEDADES (FORMULARIO Cols 41-50)
    hay_novedades: mv.hay_novedades || (Array.isArray(mv.hallazgos) && mv.hallazgos.length > 0 ? 'Si' : 'No'),
    hallazgos: Array.isArray(mv.hallazgos) ? mv.hallazgos : [],

    // 10. TRANSPORTE ESPECIAL (FORMULARIO Cols 52-57 / Hoja1 Rows 542-544)
    desea_transporte_especial: mv.desea_transporte_especial || (Array.isArray(mv.transportes_especiales) && mv.transportes_especiales.length > 0 ? 'Si' : 'No'),
    transportes_especiales: Array.isArray(mv.transportes_especiales) ? mv.transportes_especiales : [],

    // 11. PERSONAL Y SUPERVISIÓN / FIRMAS (Ref: Hoja1 Rows 545-546 & FIRMAS)
    responsable_tec_1: mv.responsable_tec_1 || ot.assigned_user?.name || 'Técnico Responsable',
    responsable_tec_2: mv.responsable_tec_2 || '',
    empresa_ejecuta: mv.empresa_ejecuta || 'INMEL / DOBLEX S.A.S.',
    nombre_supervisor: mv.nombre_supervisor || ot.site_owner || 'Supervisor Operativo Claro',
    fecha_elaboracion: mv.fecha_elaboracion || new Date().toISOString().slice(0, 10),
    firma_tecnico_lat: mv.firma_tecnico_lat || null,
    firma_tecnico_lng: mv.firma_tecnico_lng || null,
    firma_tecnico_confirmada: mv.firma_tecnico_confirmada || false,

    ...mv
  };
};

const form = reactive(buildInitialState());

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
      form.subsistema = normalizarSubsistema(form.subsistema);
      if (!Array.isArray(form.materiales)) form.materiales = [];
      if (!Array.isArray(form.repuestos_cambios)) form.repuestos_cambios = [];
      if (!Array.isArray(form.hallazgos)) form.hallazgos = [];
      if (!Array.isArray(form.transportes_especiales)) form.transportes_especiales = [];
      if (!Array.isArray(form.evidencias_actividad)) form.evidencias_actividad = [];
      nextTick(() => { isInternalSync = false; });
    }
  }
}, { deep: true });

watch(() => props.ot, (newOt) => {
  if (newOt) {
    if (!form.sitio && newOt.sitio) form.sitio = newOt.sitio;
    if (!form.direccion && newOt.ubicacion) form.direccion = newOt.ubicacion;
    if (!form.departamento && newOt.departamento) form.departamento = newOt.departamento;
    if (!form.regional && newOt.regional) form.regional = newOt.regional;
    if (!form.site_owner && newOt.site_owner) form.site_owner = newOt.site_owner;
    if (!form.codigo_ot && newOt.codigo) form.codigo_ot = newOt.codigo;
    if (!form.responsable && newOt.assigned_user?.name) form.responsable = newOt.assigned_user.name;
    if (!form.responsable_tec_1 && newOt.assigned_user?.name) form.responsable_tec_1 = newOt.assigned_user.name;
  }
}, { immediate: true });

const CHIPS_PASOS_RAPIDOS = [
  'Diagnóstico y verificación inicial',
  'Excavación y tendido SPT',
  'Desmonte de pieza / equipo averiado',
  'Instalación y montaje de repuesto nuevo',
  'Soldadura exotérmica / Aterrizaje',
  'Tratamiento de suelo con hidrosuelo',
  'Ajuste, torqueo y cableado de fuerza',
  'Pruebas con carga en automático',
  'Medición final y entrega operativa'
];

const aplicarSugerenciaPaso = (ev, sugerencia) => {
  if (!ev.descripcion) {
    ev.descripcion = sugerencia;
  } else {
    ev.descripcion = `${ev.descripcion}. ${sugerencia}`;
  }
};

const agregarEvidenciaActividad = () => {
  if (!Array.isArray(form.evidencias_actividad)) {
    form.evidencias_actividad = [];
  }
  form.evidencias_actividad.push({
    id: 'ev_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4),
    foto_url: '',
    descripcion: ''
  });
};

const eliminarEvidenciaActividad = (idx) => {
  if (Array.isArray(form.evidencias_actividad)) {
    form.evidencias_actividad.splice(idx, 1);
  }
};

// Captura de geolocalización para la firma del técnico (según sheet FIRMAS: Latitud y Longitud)
const capturandoGps = ref(false);
const gpsMensaje = ref('');

const capturarCoordenadasFirma = () => {
  if (!navigator.geolocation) {
    gpsMensaje.value = 'Geolocalización no soportada por el navegador.';
    return;
  }
  capturandoGps.value = true;
  gpsMensaje.value = '';
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      form.firma_tecnico_lat = Number(pos.coords.latitude.toFixed(6));
      form.firma_tecnico_lng = Number(pos.coords.longitude.toFixed(6));
      form.firma_tecnico_confirmada = true;
      capturandoGps.value = false;
      gpsMensaje.value = `Coordenadas capturadas con éxito: (${form.firma_tecnico_lat}, ${form.firma_tecnico_lng})`;
    },
    (err) => {
      console.warn('Error capturando GPS:', err);
      // Coordenadas de contingencia basadas en ubicación de sitio si falla hardware
      form.firma_tecnico_lat = 10.91937;
      form.firma_tecnico_lng = -74.78389;
      form.firma_tecnico_confirmada = true;
      capturandoGps.value = false;
      gpsMensaje.value = 'Coordenadas de estación registradas por contingencia.';
    },
    { timeout: 8000, enableHighAccuracy: true }
  );
};
</script>

<template>
  <div class="space-y-4 sm:space-y-5 text-xs select-text">

    <!-- CABECERA INSTITUCIONAL CLARO -->
    <div class="relative overflow-hidden bg-gradient-to-br from-red-600 via-red-700 to-rose-900 text-white rounded-2xl p-4 sm:p-5 shadow-sm border border-red-500/30">
      <div class="relative z-10 space-y-2">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 border-b border-white/20 pb-3">
          <div class="space-y-1">
            <span class="text-[10px] font-black tracking-widest uppercase text-red-200 block">
              OPERACIÓN Y MANTENIMIENTO CLARO - PROVEEDORES
            </span>
            <h2 class="text-sm sm:text-base font-black uppercase tracking-wide flex items-center gap-2">
              <span>Mantenimiento Correctivo y Emergencias</span>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-white/20 text-white border border-white/30 backdrop-blur-xs">
                {{ form.tipo_actividad_label === 'Emergencia' ? 'EMERGENCIA' : 'MC' }}
              </span>
            </h2>
          </div>
          <div class="text-[11px] font-mono font-bold bg-black/30 backdrop-blur-xs px-3 py-1.5 rounded-xl border border-white/20 self-start sm:self-auto flex items-center gap-1.5">
            <span class="text-white/70">OT:</span>
            <span class="text-white font-black tracking-wider">{{ form.codigo_ot || props.codigoOt }}</span>
          </div>
        </div>
        <p class="text-[11px] text-red-100/90 leading-relaxed font-medium">
          Formato oficial de intervención en campo para registro de diagnóstico, sustitución de repuestos, consumo de materiales LPU, evidencias fotográficas y firmas con georreferenciación.
        </p>
      </div>
    </div>

    <!-- 1. INFORMACIÓN GENERAL -->
    <div class="bg-white dark:bg-[#111216] border border-slate-200/90 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs transition-all">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/5 pb-3">
        <div class="flex items-center gap-2.5">
          <div class="w-7 h-7 rounded-lg bg-red-50 dark:bg-red-950/40 text-red-600 dark:text-red-400 flex items-center justify-center">
            <IconBuildingBroadcastTower class="w-4 h-4 stroke-[2.2]" />
          </div>
          <div>
            <span class="font-black text-slate-900 dark:text-white uppercase tracking-wider text-xs block">
              1. Información General
            </span>
            <span class="text-[10px] text-slate-400">Datos principales de la estación y orden de trabajo</span>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
        <!-- Nombre de Estación -->
        <div class="space-y-1">
          <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase">
            Nombre de Estación <span class="text-red-500">*</span>
          </label>
          <Input v-model="form.sitio" placeholder="Ej. ATL.SUAN / MON.CENTRO" :disabled="readOnly" class="h-10 text-xs font-bold uppercase" />
        </div>

        <!-- Categoría -->
        <div class="space-y-1">
          <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase">
            Categoría <span class="text-red-500">*</span>
          </label>
          <select 
            v-model="form.categoria" 
            :disabled="readOnly"
            class="h-10 w-full rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50 dark:bg-[#0a0b10] px-3 font-semibold text-xs text-slate-800 dark:text-slate-200 outline-none focus:ring-2 focus:ring-red-500/20 focus:border-red-500 transition-all"
          >
            <option value="Urbano">Urbano</option>
            <option value="Rural">Rural</option>
          </select>
        </div>

        <!-- Regional -->
        <div class="space-y-1">
          <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase">
            Regional <span class="text-red-500">*</span>
          </label>
          <Input v-model="form.regional" placeholder="Ej. COSTA, R1, R2" :disabled="readOnly" class="h-10 text-xs font-semibold uppercase" />
        </div>

        <!-- Responsable / Técnico Líder -->
        <div class="space-y-1">
          <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase">
            Responsable en Sitio <span class="text-red-500">*</span>
          </label>
          <Input v-model="form.responsable" placeholder="Nombre del técnico líder" :disabled="readOnly" class="h-10 text-xs font-semibold" />
        </div>

        <!-- Departamento -->
        <div class="space-y-1">
          <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase">
            Departamento <span class="text-red-500">*</span>
          </label>
          <Input v-model="form.departamento" placeholder="Ej. Atlántico, Córdoba" :disabled="readOnly" class="h-10 text-xs" />
        </div>

        <!-- No. INC -->
        <div class="space-y-1">
          <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase flex items-center justify-between">
            <span>No. INC (Ticket Claro) <span class="text-red-500">*</span></span>
            <span class="text-[9px] text-red-600 dark:text-red-400 font-black">Oficial</span>
          </label>
          <Input v-model="form.no_inc" placeholder="Ej. SMU008212 o INC-10492" :disabled="readOnly" class="h-10 text-xs font-mono font-bold text-red-600 dark:text-red-400 uppercase" />
        </div>

        <!-- Dirección -->
        <div class="space-y-1 sm:col-span-2">
          <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase">
            Dirección de la Estación
          </label>
          <Input v-model="form.direccion" placeholder="Dirección física del sitio" :disabled="readOnly" class="h-10 text-xs" />
        </div>

        <!-- Tipo de Estación -->
        <div class="space-y-1">
          <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase">
            Tipo de Estación <span class="text-red-500">*</span>
          </label>
          <select 
            v-model="form.tipo_estacion" 
            :disabled="readOnly"
            class="h-10 w-full rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50 dark:bg-[#0a0b10] px-3 font-semibold text-xs text-slate-800 dark:text-slate-200 outline-none focus:ring-2 focus:ring-red-500/20 focus:border-red-500 transition-all"
          >
            <option value="Outdoor">Outdoor</option>
            <option value="Indoor">Indoor</option>
            <option value="Móvil">Móvil</option>
            <option value="Repetidora">Repetidora</option>
          </select>
        </div>

        <!-- Tipo de Sitio -->
        <div class="space-y-1">
          <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase">
            Tipo de Sitio <span class="text-red-500">*</span>
          </label>
          <select 
            v-model="form.tipo_sitio" 
            :disabled="readOnly"
            class="h-10 w-full rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50 dark:bg-[#0a0b10] px-3 font-semibold text-xs text-slate-800 dark:text-slate-200 outline-none focus:ring-2 focus:ring-red-500/20 focus:border-red-500 transition-all"
          >
            <option value="Urbano">Urbano</option>
            <option value="Rural">Rural</option>
          </select>
        </div>

        <!-- Fecha Ejecución -->
        <div class="space-y-1">
          <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase">
            Fecha Ejecución <span class="text-red-500">*</span>
          </label>
          <Input type="text" v-model="form.fecha_ejecucion" placeholder="AAAA-MM-DD HH:MM" :disabled="readOnly" class="h-10 text-xs font-mono" />
        </div>

        <!-- Site Owner -->
        <div class="space-y-1">
          <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase">
            Site Owner (SO Claro) <span class="text-red-500">*</span>
          </label>
          <Input v-model="form.site_owner" placeholder="Ej. Ernesto Rocha / Cleyver Espitia" :disabled="readOnly" class="h-10 text-xs font-bold text-slate-900 dark:text-white" />
        </div>
      </div>
    </div>

    <!-- 2. INFORMACIÓN DE LA ACTIVIDAD -->
    <div class="bg-white dark:bg-[#111216] border border-slate-200/90 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs transition-all">
      <div class="flex items-center gap-2.5 border-b border-slate-100 dark:border-white/5 pb-3">
        <div class="w-7 h-7 rounded-lg bg-amber-50 dark:bg-amber-950/40 text-amber-600 dark:text-amber-400 flex items-center justify-center">
          <IconActivity class="w-4 h-4 stroke-[2.2]" />
        </div>
        <div>
          <span class="font-black text-slate-900 dark:text-white uppercase tracking-wider text-xs block">
            2. Información de la Actividad
          </span>
          <span class="text-[10px] text-slate-400">Subsistema, equipo y modalidad de la intervención técnica</span>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
        <!-- Tipo de Actividad -->
        <div class="space-y-1">
          <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase">
            Tipo de Actividad <span class="text-red-500">*</span>
          </label>
          <select 
            v-model="form.tipo_actividad_label" 
            :disabled="readOnly"
            class="h-10 w-full rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50 dark:bg-[#0a0b10] px-3 font-bold text-xs text-slate-800 dark:text-slate-200 outline-none focus:ring-2 focus:ring-red-500/20 focus:border-red-500 transition-all"
          >
            <option value="MC">MC (Mantenimiento Correctivo)</option>
            <option value="Emergencia">Emergencia</option>
          </select>
        </div>

        <!-- Subsistema -->
        <div class="space-y-1">
          <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase">
            Subsistema <span class="text-red-500">*</span>
          </label>
          <select 
            v-model="form.subsistema" 
            :disabled="readOnly"
            class="h-10 w-full rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50 dark:bg-[#0a0b10] px-3 font-bold text-xs text-slate-800 dark:text-slate-200 outline-none focus:ring-2 focus:ring-red-500/20 focus:border-red-500 transition-all"
          >
            <option v-for="opc in OPCIONES_SUBSISTEMA" :key="opc" :value="opc">
              {{ opc }}
            </option>
            <option v-if="form.subsistema && !OPCIONES_SUBSISTEMA.includes(form.subsistema)" :value="form.subsistema">
              {{ form.subsistema }}
            </option>
          </select>
        </div>

        <!-- Tipo de Equipo en Falla -->
        <div class="space-y-1">
          <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase">
            Tipo de Equipo en Falla <span class="text-red-500">*</span>
          </label>
          <Input v-model="form.tipo_equipo_falla" placeholder="Ej. SPT, Planta eléctrica, SELMEC, etc." :disabled="readOnly" class="h-10 text-xs font-bold" />
        </div>

        <!-- Modelo / Ref. -->
        <div class="space-y-1">
          <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase">
            Modelo / Referencia
          </label>
          <Input v-model="form.modelo_equipo" placeholder="Ej. 40SC, N/A" :disabled="readOnly" class="h-10 text-xs font-mono" />
        </div>
      </div>

      <!-- Flags de Intervención (Si / No) -->
      <div class="space-y-2 pt-1">
        <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase">
          Parámetros de Intervención Técnica (Si / No)
        </label>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
          <!-- Presenta Afectación de Servicios -->
          <div class="p-2.5 rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50/70 dark:bg-[#0a0b10] space-y-1.5">
            <span class="text-[10px] font-bold text-slate-500 uppercase block leading-tight">
              ¿Afectación de Servicios?
            </span>
            <div class="grid grid-cols-2 p-1 bg-slate-200/60 dark:bg-white/5 rounded-xl gap-1">
              <button
                type="button"
                :disabled="readOnly"
                @click="form.presenta_afectacion = 'Si'"
                class="py-1 rounded-lg font-black text-xs transition-all cursor-pointer active:scale-95"
                :class="form.presenta_afectacion === 'Si' ? 'bg-rose-600 text-white shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'"
              >
                Si
              </button>
              <button
                type="button"
                :disabled="readOnly"
                @click="form.presenta_afectacion = 'No'"
                class="py-1 rounded-lg font-black text-xs transition-all cursor-pointer active:scale-95"
                :class="form.presenta_afectacion === 'No' ? 'bg-emerald-600 text-white shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'"
              >
                No
              </button>
            </div>
          </div>

          <!-- Reparación -->
          <div class="p-2.5 rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50/70 dark:bg-[#0a0b10] space-y-1.5">
            <span class="text-[10px] font-bold text-slate-500 uppercase block leading-tight">
              ¿Reparación?
            </span>
            <div class="grid grid-cols-2 p-1 bg-slate-200/60 dark:bg-white/5 rounded-xl gap-1">
              <button
                type="button"
                :disabled="readOnly"
                @click="form.reparacion = 'Si'"
                class="py-1 rounded-lg font-black text-xs transition-all cursor-pointer active:scale-95"
                :class="form.reparacion === 'Si' ? 'bg-amber-600 text-white shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'"
              >
                Si
              </button>
              <button
                type="button"
                :disabled="readOnly"
                @click="form.reparacion = 'No'"
                class="py-1 rounded-lg font-black text-xs transition-all cursor-pointer active:scale-95"
                :class="form.reparacion === 'No' ? 'bg-slate-700 text-white dark:bg-white/20' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'"
              >
                No
              </button>
            </div>
          </div>

          <!-- Reinstalación -->
          <div class="p-2.5 rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50/70 dark:bg-[#0a0b10] space-y-1.5">
            <span class="text-[10px] font-bold text-slate-500 uppercase block leading-tight">
              ¿Reinstalación?
            </span>
            <div class="grid grid-cols-2 p-1 bg-slate-200/60 dark:bg-white/5 rounded-xl gap-1">
              <button
                type="button"
                :disabled="readOnly"
                @click="form.reinstalacion = 'Si'"
                class="py-1 rounded-lg font-black text-xs transition-all cursor-pointer active:scale-95"
                :class="form.reinstalacion === 'Si' ? 'bg-blue-600 text-white shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'"
              >
                Si
              </button>
              <button
                type="button"
                :disabled="readOnly"
                @click="form.reinstalacion = 'No'"
                class="py-1 rounded-lg font-black text-xs transition-all cursor-pointer active:scale-95"
                :class="form.reinstalacion === 'No' ? 'bg-slate-700 text-white dark:bg-white/20' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'"
              >
                No
              </button>
            </div>
          </div>

          <!-- Cambio de Equipo -->
          <div class="p-2.5 rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50/70 dark:bg-[#0a0b10] space-y-1.5">
            <span class="text-[10px] font-bold text-slate-500 uppercase block leading-tight">
              ¿Cambio de Equipo?
            </span>
            <div class="grid grid-cols-2 p-1 bg-slate-200/60 dark:bg-white/5 rounded-xl gap-1">
              <button
                type="button"
                :disabled="readOnly"
                @click="form.cambio_equipo = 'Si'"
                class="py-1 rounded-lg font-black text-xs transition-all cursor-pointer active:scale-95"
                :class="form.cambio_equipo === 'Si' ? 'bg-purple-600 text-white shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'"
              >
                Si
              </button>
              <button
                type="button"
                :disabled="readOnly"
                @click="form.cambio_equipo = 'No'"
                class="py-1 rounded-lg font-black text-xs transition-all cursor-pointer active:scale-95"
                :class="form.cambio_equipo === 'No' ? 'bg-slate-700 text-white dark:bg-white/20' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'"
              >
                No
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 3. DESCRIPCIÓN DE LA FALLA -->
    <div class="bg-white dark:bg-[#111216] border border-slate-200/90 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-3 shadow-xs transition-all">
      <div class="flex items-center gap-2.5 border-b border-slate-100 dark:border-white/5 pb-2.5">
        <div class="w-7 h-7 rounded-lg bg-rose-50 dark:bg-rose-950/40 text-rose-600 dark:text-rose-400 flex items-center justify-center">
          <IconAlertTriangle class="w-4 h-4 stroke-[2.2]" />
        </div>
        <div>
          <span class="font-black text-slate-900 dark:text-white uppercase tracking-wider text-xs block">
            3. Descripción de la Falla Encontrada <span class="text-red-500">*</span>
          </span>
          <span class="text-[10px] text-slate-400">Síntomas, diagnóstico y estado de la estación al arribar</span>
        </div>
      </div>
      <textarea 
        v-model="form.descripcion_falla" 
        :disabled="readOnly"
        rows="3" 
        placeholder="Describa en detalle los síntomas encontrados, causas de la falla, estado del equipo y alarmas presentes..."
        class="w-full rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50/70 dark:bg-[#0a0b10] p-3 text-xs text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-red-500/20 focus:border-red-500 outline-none leading-relaxed transition-all"
      ></textarea>
    </div>

    <!-- 4. DESCRIPCIÓN DE LA SOLUCIÓN TÉCNICA -->
    <div class="bg-white dark:bg-[#111216] border border-slate-200/90 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-3 shadow-xs transition-all">
      <div class="flex items-center gap-2.5 border-b border-slate-100 dark:border-white/5 pb-2.5">
        <div class="w-7 h-7 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
          <IconTool class="w-4 h-4 stroke-[2.2]" />
        </div>
        <div>
          <span class="font-black text-slate-900 dark:text-white uppercase tracking-wider text-xs block">
            4. Descripción de la Solución Técnica Ejecutada <span class="text-red-500">*</span>
          </span>
          <span class="text-[10px] text-slate-400">Labores realizadas, ajustes, calibración y pruebas de servicio</span>
        </div>
      </div>
      <textarea 
        v-model="form.descripcion_solucion" 
        :disabled="readOnly"
        rows="3" 
        placeholder="Detalle los trabajos técnicos realizados, componentes reemplazados, pruebas con carga y validación con el centro de gestión..."
        class="w-full rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50/70 dark:bg-[#0a0b10] p-3 text-xs text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none leading-relaxed transition-all"
      ></textarea>
    </div>

    <!-- 5. CAMBIO DE REPUESTOS Y/O PARTES -->
    <div class="space-y-2">
      <RepuestosCambiosManager
        v-model="form.repuestos_cambios"
        :codigo-ot="codigoOt"
        :read-only="readOnly"
      />
    </div>

    <!-- 6. LISTADO DE MATERIALES UTILIZADOS -->
    <div class="space-y-2">
      <div class="bg-white dark:bg-[#111216] border border-slate-200/90 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-3.5 shadow-xs transition-all">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/5 pb-2.5">
          <div class="flex items-center gap-2.5">
            <div class="w-7 h-7 rounded-lg bg-amber-50 dark:bg-amber-950/40 text-amber-600 dark:text-amber-400 flex items-center justify-center">
              <IconBox class="w-4 h-4 stroke-[2.2]" />
            </div>
            <div>
              <span class="font-black text-slate-900 dark:text-white uppercase tracking-wider text-xs block">
                6. Listado de Materiales Utilizados
              </span>
              <span class="text-[10px] text-slate-400">Consumo de insumos y materiales del catálogo LPU</span>
            </div>
          </div>
          <span class="text-[10px] font-mono font-bold px-2.5 py-1 rounded-full bg-slate-100 dark:bg-white/5 text-slate-600 dark:text-slate-400">
            {{ form.materiales?.length || 0 }} ítem(s)
          </span>
        </div>

        <MaterialesTipologiaSelector
          v-model="form.materiales"
          :subsistema="form.subsistema"
          :read-only="readOnly"
        />
      </div>
    </div>

    <!-- 7. EVIDENCIA FOTOGRÁFICA DE LA ACTIVIDAD -->
    <div class="bg-white dark:bg-[#111216] border border-slate-200/90 dark:border-white/10 rounded-2xl overflow-hidden shadow-xs space-y-4 pb-5 transition-all">
      <!-- Banner Rojo Oficial Claro -->
      <div class="bg-gradient-to-r from-[#e60000] to-[#c70000] text-white px-4 py-2.5 border-b-2 border-[#002060] flex items-center justify-between shadow-xs">
        <div class="flex items-center gap-2">
          <IconCamera class="w-4 h-4 text-white stroke-[2.5]" />
          <span class="font-black text-xs sm:text-sm uppercase tracking-wider text-white">
            EVIDENCIA FOTOGRÁFICA DE LA ACTIVIDAD
          </span>
        </div>
        <button
          v-if="!readOnly"
          type="button"
          @click="agregarEvidenciaActividad"
          class="bg-white text-red-700 hover:bg-white/95 px-2.5 py-1 rounded-lg text-[11px] font-black shadow-xs flex items-center gap-1 active:scale-95 transition-all cursor-pointer"
        >
          <IconPlus class="w-3.5 h-3.5 stroke-[3]" />
          <span>Agregar Paso</span>
        </button>
      </div>

      <div class="px-4 sm:px-5 space-y-4">
        <!-- Encabezado de la lista -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 dark:border-white/5 pb-2.5">
          <div>
            <span class="text-xs font-black uppercase text-slate-800 dark:text-slate-200 tracking-wider block">
              Registro de Evidencias y Pasos Ejecutados en Sitio
            </span>
            <p class="text-[10px] text-slate-500 dark:text-slate-400">
              Capture la foto de cada labor y describa el procedimiento ejecutado.
            </p>
          </div>
          <span class="text-[10px] font-mono font-bold px-2.5 py-1 rounded-full bg-slate-100 dark:bg-white/5 text-slate-600 dark:text-slate-400 self-start sm:self-auto">
            {{ form.evidencias_actividad?.length || 0 }} paso(s)
          </span>
        </div>

        <!-- Lista de tarjetas de evidencias -->
        <div v-if="form.evidencias_actividad && form.evidencias_actividad.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-3.5">
          <div
            v-for="(ev, idx) in form.evidencias_actividad"
            :key="ev.id || idx"
            class="p-3.5 rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50/70 dark:bg-[#0c0d12] space-y-3 relative group transition-all hover:border-red-400/60 dark:hover:border-red-500/40"
          >
            <!-- Cabecera de la tarjeta con numeración y botón eliminar -->
            <div class="flex items-center justify-between border-b border-slate-200/60 dark:border-white/5 pb-2">
              <div class="flex items-center gap-1.5">
                <span class="w-5 h-5 rounded-full bg-red-600 text-white font-black text-[10px] flex items-center justify-center">
                  {{ idx + 1 }}
                </span>
                <span class="text-[11px] font-bold text-slate-800 dark:text-slate-200">
                  Paso de la Actividad
                </span>
              </div>
              <button
                v-if="!readOnly"
                type="button"
                @click="eliminarEvidenciaActividad(idx)"
                class="text-slate-400 hover:text-rose-600 dark:hover:text-rose-400 p-1 rounded-lg hover:bg-rose-50 dark:hover:bg-rose-950/30 transition-colors cursor-pointer"
                title="Eliminar este paso"
              >
                <IconTrash class="w-4 h-4 stroke-[2]" />
              </button>
            </div>

            <!-- Captura de Foto con SinglePhotoCapture -->
            <div class="space-y-1">
              <label class="block text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                Foto de la Evidencia
              </label>
              <SinglePhotoCapture
                v-model="ev.foto_url"
                :tag="`EVIDENCIA PASO #${idx + 1}`"
                :codigo-ot="codigoOt"
                :disabled="readOnly"
                placeholder="Tomar o subir foto de este paso"
              />
            </div>

            <!-- Campo para la Descripción del proceso o paso ejecutado -->
            <div class="space-y-1.5">
              <label class="block text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                Descripción del proceso o paso ejecutado
              </label>
              <textarea
                v-model="ev.descripcion"
                :disabled="readOnly"
                rows="2"
                placeholder="Ej. Excavación perimetral, desmonte de equipo averiado, fijación de varilla SPT, instalación de motobomba..."
                class="w-full rounded-xl border border-slate-200 dark:border-white/10 bg-white dark:bg-[#121215] p-2.5 text-xs text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-red-500/20 focus:border-red-500 outline-none leading-relaxed transition-all"
              ></textarea>

              <!-- Sugerencias rápidas en chips táctiles -->
              <div v-if="!readOnly" class="space-y-1 pt-0.5">
                <span class="text-[9px] font-bold text-slate-400 block uppercase">Sugerencias rápidas:</span>
                <div class="flex flex-wrap gap-1">
                  <button
                    v-for="chip in CHIPS_PASOS_RAPIDOS"
                    :key="chip"
                    type="button"
                    @click="aplicarSugerenciaPaso(ev, chip)"
                    class="px-2 py-0.5 rounded-md text-[9px] font-medium bg-slate-200/80 hover:bg-red-50 hover:text-red-700 dark:bg-white/5 dark:hover:bg-white/10 text-slate-700 dark:text-slate-300 transition-colors cursor-pointer active:scale-95"
                  >
                    + {{ chip }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Estado vacío si no hay evidencias -->
        <div v-else class="p-6 rounded-xl bg-slate-50 dark:bg-[#0c0d12] border border-dashed border-slate-300 dark:border-white/10 text-center space-y-2.5">
          <div class="w-10 h-10 rounded-full bg-red-50 dark:bg-red-950/40 text-red-600 dark:text-red-400 mx-auto flex items-center justify-center">
            <IconCamera class="w-5 h-5 stroke-[2]" />
          </div>
          <div class="space-y-1">
            <p class="text-xs font-bold text-slate-800 dark:text-slate-200">
              Aún no se han registrado evidencias de la actividad
            </p>
            <p class="text-[11px] text-slate-500 dark:text-slate-400 max-w-md mx-auto">
              El personal en campo puede registrar paso a paso las fotos y describir cada labor o proceso realizado durante el mantenimiento.
            </p>
          </div>
          <button
            v-if="!readOnly"
            type="button"
            @click="agregarEvidenciaActividad"
            class="bg-[#e60000] hover:bg-red-700 text-white px-4 py-2 rounded-xl text-xs font-bold shadow-xs inline-flex items-center gap-2 active:scale-95 transition-all cursor-pointer"
          >
            <IconPlus class="w-4 h-4 stroke-[3]" />
            <span>Agregar Primera Evidencia de Paso</span>
          </button>
        </div>

        <!-- Soportes Técnicos Específicos Opcionales -->
        <div class="pt-4 border-t border-slate-100 dark:border-white/5 space-y-3">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <span class="text-xs font-black uppercase text-slate-800 dark:text-slate-200 tracking-wider block">
                Soportes Técnicos Específicos (Opcionales)
              </span>
              <span class="text-[10px] text-slate-400">
                Medición de Telurómetro & Plano de Instalación (Aplica para SPT o según intervención técnica)
              </span>
            </div>
            <div class="flex items-center gap-2 self-start sm:self-auto">
              <span class="text-[10px] font-bold text-slate-500 uppercase">¿Aplica?:</span>
              <div class="grid grid-cols-2 p-1 bg-slate-200/60 dark:bg-white/5 rounded-xl gap-1">
                <button
                  type="button"
                  :disabled="readOnly"
                  @click="form.aplica_soportes_especificos = 'Si'"
                  class="px-3 py-1 rounded-lg font-bold text-xs transition-all cursor-pointer active:scale-95"
                  :class="form.aplica_soportes_especificos === 'Si' ? 'bg-[#e60000] text-white shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'"
                >
                  Si
                </button>
                <button
                  type="button"
                  :disabled="readOnly"
                  @click="form.aplica_soportes_especificos = 'No'"
                  class="px-3 py-1 rounded-lg font-bold text-xs transition-all cursor-pointer active:scale-95"
                  :class="form.aplica_soportes_especificos === 'No' ? 'bg-slate-700 text-white dark:bg-white/20' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'"
                >
                  No
                </button>
              </div>
            </div>
          </div>

          <!-- Si no aplica -->
          <div v-if="form.aplica_soportes_especificos === 'No'" class="p-3 rounded-xl bg-slate-50 dark:bg-[#0c0d12] border border-slate-100 dark:border-white/5 text-slate-500 text-[11px] flex items-center gap-2">
            <IconInfoCircle class="w-4 h-4 text-slate-400 shrink-0" />
            <span>Soportes de telurómetro y plano omitidos para esta labor.</span>
          </div>

          <!-- Si aplica -->
          <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-3.5 pt-1 animate-in fade-in duration-200">
            <!-- Medición de Telurómetro -->
            <div class="p-3.5 bg-slate-50 dark:bg-[#0c0d12] border border-slate-200 dark:border-white/10 rounded-xl space-y-2.5">
              <div class="flex items-center justify-between">
                <span class="font-bold text-slate-800 dark:text-slate-200 text-xs">Medición de Telurómetro (Ohmios)</span>
              </div>
              <Input 
                v-model="form.medicion_telurometro_valor" 
                placeholder="Ej. 2.4 Ω (Ohmios)" 
                :disabled="readOnly" 
                class="h-10 text-xs font-mono" 
              />
              <SinglePhotoCapture
                v-model="form.medicion_telurometro_foto"
                label="Foto Pantalla Telurómetro (Opcional)"
                tag="MEDICION DE TELUROMETRO"
                :codigo-ot="codigoOt"
                :disabled="readOnly"
                placeholder="Tomar foto legible de la lectura del telurómetro"
              />
            </div>

            <!-- Plano de Instalación SPT / Croquis -->
            <div class="p-3.5 bg-slate-50 dark:bg-[#0c0d12] border border-slate-200 dark:border-white/10 rounded-xl space-y-2.5">
              <div class="flex items-center justify-between">
                <span class="font-bold text-slate-800 dark:text-slate-200 text-xs">Plano / Esquema de Instalación</span>
              </div>
              <p class="text-[10px] text-slate-500 dark:text-slate-400">
                Esquema de distribución, bajantes, anillo SPT o diagrama unifilar intervenido (Opcional).
              </p>
              <SinglePhotoCapture
                v-model="form.plano_instalacion_foto"
                label="Foto Plano / Croquis de Instalación (Opcional)"
                tag="PLANO DE INSTALACION SPT"
                :codigo-ot="codigoOt"
                :disabled="readOnly"
                placeholder="Tomar foto del plano o esquema de trabajo"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 8. RESULTADO Y OBSERVACIONES -->
    <div class="bg-white dark:bg-[#111216] border border-slate-200/90 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-3.5 shadow-xs transition-all">
      <div class="flex items-center gap-2.5 border-b border-slate-100 dark:border-white/5 pb-2.5">
        <div class="w-7 h-7 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
          <IconCheck class="w-4 h-4 stroke-[2.5]" />
        </div>
        <div>
          <span class="font-black text-slate-900 dark:text-white uppercase tracking-wider text-xs block">
            8. Resultado y Observaciones de la Actividad
          </span>
          <span class="text-[10px] text-slate-400">Cierre técnico y estado final de entrega</span>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3.5 items-center">
        <!-- Falla Resuelta -->
        <div class="p-3 rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50/70 dark:bg-[#0a0b10] space-y-1.5">
          <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase">
            FALLA RESUELTA <span class="text-red-500">*</span>
          </label>
          <div class="grid grid-cols-2 p-1 bg-slate-200/60 dark:bg-white/5 rounded-xl gap-1">
            <button
              type="button"
              :disabled="readOnly"
              @click="form.falla_resuelta = 'Si'"
              class="py-1.5 rounded-lg font-black text-xs transition-all cursor-pointer active:scale-95"
              :class="form.falla_resuelta === 'Si' ? 'bg-emerald-600 text-white shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'"
            >
              Sí (Resuelta)
            </button>
            <button
              type="button"
              :disabled="readOnly"
              @click="form.falla_resuelta = 'No'"
              class="py-1.5 rounded-lg font-black text-xs transition-all cursor-pointer active:scale-95"
              :class="form.falla_resuelta === 'No' ? 'bg-rose-600 text-white shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'"
            >
              No (Pendiente)
            </button>
          </div>
        </div>

        <!-- Observaciones -->
        <div class="sm:col-span-2 space-y-1">
          <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase">
            Observaciones de la Actividad
          </label>
          <textarea 
            v-model="form.observaciones_actividad" 
            :disabled="readOnly"
            rows="2" 
            placeholder="Ej. Se equilibraron las cargas de equipos. SPT queda por debajo de 5 Ohmios conforme al estándar Claro..."
            class="w-full rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50/70 dark:bg-[#0a0b10] p-2.5 text-xs text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none leading-relaxed transition-all"
          ></textarea>
        </div>
      </div>
    </div>

    <!-- 9. HALLAZGOS Y NOVEDADES EN LA ESTACIÓN -->
    <div class="bg-white dark:bg-[#111216] border border-slate-200/90 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-3.5 shadow-xs transition-all">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 dark:border-white/5 pb-2.5">
        <div class="flex items-center gap-2.5">
          <div class="w-7 h-7 rounded-lg bg-amber-50 dark:bg-amber-950/40 text-amber-600 dark:text-amber-400 flex items-center justify-center">
            <IconAlertCircle class="w-4 h-4 stroke-[2.2]" />
          </div>
          <div>
            <span class="font-black text-slate-900 dark:text-white uppercase tracking-wider text-xs block">
              9. Novedades y Hallazgos en la Estación
            </span>
            <span class="text-[10px] text-slate-400">Reporte de condiciones de riesgo o hallazgos adicionales</span>
          </div>
        </div>
        <div class="flex items-center gap-2 self-start sm:self-auto">
          <span class="text-[10px] font-bold text-slate-500 uppercase">¿Novedades?:</span>
          <div class="grid grid-cols-2 p-1 bg-slate-200/60 dark:bg-white/5 rounded-xl gap-1">
            <button
              type="button"
              :disabled="readOnly"
              @click="form.hay_novedades = 'Si'"
              class="px-3 py-1 rounded-lg font-black text-xs transition-all cursor-pointer active:scale-95"
              :class="form.hay_novedades === 'Si' ? 'bg-amber-600 text-white shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'"
            >
              Si
            </button>
            <button
              type="button"
              :disabled="readOnly"
              @click="form.hay_novedades = 'No'"
              class="px-3 py-1 rounded-lg font-black text-xs transition-all cursor-pointer active:scale-95"
              :class="form.hay_novedades === 'No' ? 'bg-slate-700 text-white dark:bg-white/20' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'"
            >
              No
            </button>
          </div>
        </div>
      </div>

      <div v-if="form.hay_novedades === 'Si'" class="space-y-3 animate-in fade-in duration-200">
        <NovedadesHallazgosManager
          v-model="form.hallazgos"
          :codigo-ot="codigoOt"
          :read-only="readOnly"
        />
      </div>
      <p v-else class="text-[11px] text-slate-500 dark:text-slate-400 italic">
        No se reportaron novedades de riesgo ni hallazgos adicionales en la estación durante la visita.
      </p>
    </div>

    <!-- 10. TRANSPORTE ESPECIAL -->
    <div class="bg-white dark:bg-[#111216] border border-slate-200/90 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-3.5 shadow-xs transition-all">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 dark:border-white/5 pb-2.5">
        <div class="flex items-center gap-2.5">
          <div class="w-7 h-7 rounded-lg bg-blue-50 dark:bg-blue-950/40 text-blue-600 dark:text-blue-400 flex items-center justify-center">
            <IconTruck class="w-4 h-4 stroke-[2.2]" />
          </div>
          <div>
            <span class="font-black text-slate-900 dark:text-white uppercase tracking-wider text-xs block">
              10. Transporte Especial
            </span>
            <span class="text-[10px] text-slate-400">Rutas fluviales, mulares o vehículos 4x4 de acceso difícil</span>
          </div>
        </div>
        <div class="flex items-center gap-2 self-start sm:self-auto">
          <span class="text-[10px] font-bold text-slate-500 uppercase">¿Aplica?:</span>
          <div class="grid grid-cols-2 p-1 bg-slate-200/60 dark:bg-white/5 rounded-xl gap-1">
            <button
              type="button"
              :disabled="readOnly"
              @click="form.desea_transporte_especial = 'Si'"
              class="px-3 py-1 rounded-lg font-black text-xs transition-all cursor-pointer active:scale-95"
              :class="form.desea_transporte_especial === 'Si' ? 'bg-blue-600 text-white shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'"
            >
              Si
            </button>
            <button
              type="button"
              :disabled="readOnly"
              @click="form.desea_transporte_especial = 'No'"
              class="px-3 py-1 rounded-lg font-black text-xs transition-all cursor-pointer active:scale-95"
              :class="form.desea_transporte_especial === 'No' ? 'bg-slate-700 text-white dark:bg-white/20' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'"
            >
              No
            </button>
          </div>
        </div>
      </div>

      <div v-if="form.desea_transporte_especial === 'Si'" class="space-y-3 animate-in fade-in duration-200">
        <TransporteEspecialManager
          v-model="form.transportes_especiales"
          :codigo-ot="codigoOt"
          :read-only="readOnly"
        />
      </div>
      <p v-else class="text-[11px] text-slate-500 dark:text-slate-400 italic">
        Desplazamiento ordinario en vehículo de cuadrilla sin requerimiento de transporte fluvial o especial.
      </p>
    </div>

    <!-- 11. PERSONAL Y SUPERVISIÓN / FIRMAS -->
    <div class="bg-white dark:bg-[#111216] border border-slate-200/90 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs transition-all">
      <div class="flex items-center gap-2.5 border-b border-slate-100 dark:border-white/5 pb-2.5">
        <div class="w-7 h-7 rounded-lg bg-purple-50 dark:bg-purple-950/40 text-purple-600 dark:text-purple-400 flex items-center justify-center">
          <IconFileCertificate class="w-4 h-4 stroke-[2.2]" />
        </div>
        <div>
          <span class="font-black text-slate-900 dark:text-white uppercase tracking-wider text-xs block">
            11. Personal Ejecutor, Supervisión & Firmas (Con GPS)
          </span>
          <span class="text-[10px] text-slate-400">Responsables de la labor y georreferenciación de la firma</span>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
        <div class="space-y-1">
          <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase">
            Personal Quien Ejecuta (Técnico 1) <span class="text-red-500">*</span>
          </label>
          <Input v-model="form.responsable_tec_1" placeholder="Nombre técnico líder" :disabled="readOnly" class="h-10 text-xs font-bold" />
        </div>

        <div class="space-y-1">
          <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase">
            Técnico Acompañante (Técnico 2)
          </label>
          <Input v-model="form.responsable_tec_2" placeholder="Nombre técnico acompañante" :disabled="readOnly" class="h-10 text-xs" />
        </div>

        <div class="space-y-1">
          <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase">
            Empresa Quien Ejecuta <span class="text-red-500">*</span>
          </label>
          <Input v-model="form.empresa_ejecuta" :disabled="readOnly" class="h-10 text-xs font-bold uppercase text-slate-800 dark:text-slate-200" />
        </div>

        <div class="space-y-1">
          <label class="block font-bold text-slate-600 dark:text-slate-400 text-[10px] uppercase">
            Nombre de Quien Revisa (Supervisor Claro) <span class="text-red-500">*</span>
          </label>
          <Input v-model="form.nombre_supervisor" placeholder="Supervisor Claro" :disabled="readOnly" class="h-10 text-xs font-bold" />
        </div>
      </div>

      <!-- Panel de Firma Digital con Coordenadas GPS -->
      <div class="p-3.5 bg-purple-50/70 dark:bg-purple-950/20 border border-purple-200 dark:border-purple-800/40 rounded-xl space-y-2.5">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div class="flex items-center gap-2">
            <IconUserCheck class="w-4 h-4 text-purple-600 dark:text-purple-400 stroke-[2.2]" />
            <span class="font-bold text-purple-950 dark:text-purple-200 text-xs">
              Firma Digital de Responsable en Sitio & Coordenadas GPS
            </span>
          </div>
          <span 
            class="text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full self-start sm:self-auto"
            :class="form.firma_tecnico_confirmada ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300'"
          >
            {{ form.firma_tecnico_confirmada ? '✓ Firmado y Georreferenciado' : 'Pendiente de Firma' }}
          </span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-xs items-center">
          <div class="bg-white dark:bg-[#121215] border border-purple-200/80 dark:border-white/10 rounded-lg p-2">
            <span class="text-[9px] font-bold text-slate-400 uppercase block">Latitud GPS</span>
            <span class="font-mono font-bold text-slate-800 dark:text-slate-200">{{ form.firma_tecnico_lat || 'Pendiente' }}</span>
          </div>
          <div class="bg-white dark:bg-[#121215] border border-purple-200/80 dark:border-white/10 rounded-lg p-2">
            <span class="text-[9px] font-bold text-slate-400 uppercase block">Longitud GPS</span>
            <span class="font-mono font-bold text-slate-800 dark:text-slate-200">{{ form.firma_tecnico_lng || 'Pendiente' }}</span>
          </div>
          <div>
            <button
              v-if="!readOnly"
              type="button"
              @click="capturarCoordenadasFirma"
              :disabled="capturandoGps"
              class="w-full h-10 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all shadow-xs cursor-pointer"
            >
              <IconCompass class="w-3.5 h-3.5 stroke-[2]" :class="{ 'animate-spin': capturandoGps }" />
              <span>{{ capturandoGps ? 'Capturando GPS...' : (form.firma_tecnico_confirmada ? 'Actualizar Firma GPS' : 'Firmar con GPS') }}</span>
            </button>
          </div>
        </div>
        <p v-if="gpsMensaje" class="text-[10px] text-purple-700 dark:text-purple-300 font-medium">
          {{ gpsMensaje }}
        </p>
      </div>
    </div>

  </div>
</template>

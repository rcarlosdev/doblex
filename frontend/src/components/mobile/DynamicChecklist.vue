<template>
  <div class="space-y-4">
    <!-- Selector de Protocolos de Inspección Múltiple -->
    <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3 shadow-sm transition-colors duration-300">
      <div class="flex items-center justify-between flex-wrap gap-2">
        <div>
          <h4 class="text-xs font-extrabold text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
            <IconListCheck class="w-4 h-4 text-red-600 dark:text-red-400 stroke-[2]" />
            <span>Protocolos de Inspección Técnica en Campo</span>
          </h4>
          <p class="text-[11px] text-slate-500 dark:text-slate-400 font-medium mt-0.5">
            Seleccione o cambie de protocolo si este trabajo requiere múltiples inspecciones.
          </p>
        </div>

        <div class="bg-red-50 dark:bg-red-950/80 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 font-mono text-xs px-3 py-1.5 rounded-xl font-extrabold flex items-center gap-1.5 shadow-xs">
          <span>Consolidado: {{ consolidatedPercent }}% Cumplido</span>
        </div>
      </div>

      <!-- Barra de Selector de Protocolos (Pestañas Secundarias de Inspección) -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-1.5 pt-1">
        <button
          v-for="p in availableProtocols"
          :key="p.key"
          @click="selectProtocol(p.key)"
          class="p-2.5 rounded-xl text-left border transition-all flex flex-col justify-between select-none"
          :class="activeProtocolKey === p.key
            ? 'bg-red-600 border-red-600 text-white shadow-md shadow-red-600/20'
            : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/5'"
        >
          <div class="flex items-center justify-between gap-1">
            <span class="text-[10px] font-mono font-black uppercase tracking-wide truncate">{{ p.shortLabel }}</span>
            <span
              class="text-[9px] font-bold font-mono px-1.5 py-0.2 rounded"
              :class="activeProtocolKey === p.key
                ? 'bg-white/20 text-white'
                : getProtocolProgress(p.key) === 100
                  ? 'bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300'
                  : 'bg-slate-200 dark:bg-white/10 text-slate-600 dark:text-slate-400'"
            >
              {{ getProtocolProgress(p.key) }}%
            </span>
          </div>
          <div class="text-[11px] font-bold truncate mt-1" :class="activeProtocolKey === p.key ? 'text-white' : 'text-slate-900 dark:text-white'">
            {{ p.name }}
          </div>
        </button>
      </div>
    </div>

    <!-- Contenido del Protocolo Activo Seleccionado -->
    <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3 shadow-sm">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-3 flex-wrap gap-2">
        <div>
          <h4 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-red-600"></span>
            <span>{{ activeTemplate.title }}</span>
          </h4>
          <p class="text-[11px] text-slate-500 dark:text-slate-400 font-medium mt-0.5">
            {{ activeTemplate.subtitle }}
          </p>
        </div>
        <div class="text-xs font-mono font-extrabold text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-950/60 px-3 py-1 rounded-xl border border-red-200 dark:border-red-800">
          {{ activeCompletadosCount }} / {{ activeTasks.length }} Tareas ({{ activePercentage }}%)
        </div>
      </div>

      <!-- Leyenda de colores de plantilla oficial -->
      <div class="flex items-center justify-between text-[10px] bg-slate-50 dark:bg-[#0a0b10] p-2.5 rounded-xl border border-slate-200/80 dark:border-white/10 flex-wrap gap-2">
        <div class="flex items-center gap-2 flex-wrap">
          <span class="font-bold text-slate-600 dark:text-slate-400">Guía de Campo:</span>
          <span class="bg-amber-100 dark:bg-amber-950/80 text-amber-900 dark:text-amber-300 px-2 py-0.5 rounded font-bold border border-amber-300 dark:border-amber-700">Amarillo = Celda de Entrada</span>
          <span class="bg-emerald-100 dark:bg-emerald-950/80 text-emerald-900 dark:text-emerald-300 px-2 py-0.5 rounded font-bold border border-emerald-300 dark:border-emerald-700">Verde = Criterio Norma</span>
        </div>
        <div class="text-emerald-600 dark:text-emerald-400 font-bold flex items-center gap-1 text-[10px]">
          ✓ Auto-guardado en dispositivo
        </div>
      </div>

      <!-- Tareas del Protocolo Seleccionado -->
      <div class="space-y-2.5 pt-1">
        <div
          v-for="(task, idx) in activeTasks"
          :key="idx"
          class="p-3 rounded-xl border transition-all shadow-xs space-y-2"
          :class="task.completado ? 'bg-emerald-50/60 dark:bg-emerald-950/20 border-emerald-300 dark:border-emerald-500/30' : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10'"
        >
          <div class="flex items-start justify-between gap-3 cursor-pointer select-none" @click="toggleTask(idx)">
            <div class="flex items-start gap-3">
              <div
                class="w-5 h-5 rounded-lg flex items-center justify-center border transition-all shrink-0 mt-0.5"
                :class="task.completado ? 'bg-emerald-500 border-emerald-400 text-white shadow-xs' : 'border-slate-300 dark:border-white/20 bg-white dark:bg-[#0a0b10]'"
              >
                <IconCheck v-if="task.completado" class="w-3.5 h-3.5 stroke-[3]" />
              </div>
              <div class="space-y-0.5">
                <div class="text-xs font-bold text-slate-900 dark:text-white">{{ task.tarea }}</div>
                <div class="text-[11px] text-slate-500 dark:text-slate-400 font-medium">
                  <span class="font-bold text-slate-700 dark:text-slate-300">Acción:</span> {{ task.accion }}
                </div>
              </div>
            </div>
            
            <div class="shrink-0 text-right">
              <span class="text-[10px] font-mono px-2 py-0.5 rounded-full font-bold border transition-colors"
                :class="task.completado ? 'bg-emerald-100 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-300 border-emerald-300 dark:border-emerald-700' : 'bg-amber-100 dark:bg-amber-950/80 text-amber-800 dark:text-amber-300 border-amber-300 dark:border-amber-700'"
              >
                {{ task.completado ? 'CUMPLE' : 'PENDIENTE' }}
              </span>
            </div>
          </div>

          <!-- Campos especiales de medición (si aplica) -->
          <div v-if="task.tipoInput" class="pt-2 border-t border-slate-200/60 dark:border-white/10 flex items-center gap-3">
            <div class="flex-1">
              <label class="text-[10px] font-bold text-amber-700 dark:text-amber-400 uppercase tracking-wide block mb-1">
                {{ task.inputLabel }} (Diligenciar celda amarilla)
              </label>
              <div class="flex gap-2 items-center">
                <input
                  v-model="task.valorIngresado"
                  @input="onValueInput(idx)"
                  @change="onValueInput(idx)"
                  :placeholder="task.inputPlaceholder"
                  class="flex-1 bg-amber-50 dark:bg-amber-950/40 border border-amber-300 dark:border-amber-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-900 dark:text-white font-mono focus:ring-2 focus:ring-red-500 focus:outline-none transition-colors"
                />
                <span class="text-xs text-slate-500 dark:text-slate-400 font-mono font-bold">{{ task.unidad }}</span>
              </div>
            </div>
            
            <div class="w-36 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-300 dark:border-emerald-800 rounded-lg p-2 text-center space-y-0.5">
              <div class="text-[9px] text-emerald-700 dark:text-emerald-400 font-bold">Criterio Referencia (Verde)</div>
              <div class="text-[10px] text-emerald-950 dark:text-emerald-200 font-mono font-bold">{{ task.criterioRef }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { IconListCheck, IconCheck } from '@tabler/icons-vue';

const props = defineProps({
  otId: {
    type: [Number, String],
    default: null,
  },
  subsistema: {
    type: String,
    default: 'Mantenimiento General',
  },
});

const emit = defineEmits(['checklist-updated']);

const availableProtocols = [
  { key: 'SPT', shortLabel: 'SPT', name: 'Puesta a Tierra (BEP & Wenner)' },
  { key: 'GE', shortLabel: 'GE 360', name: 'Planta Eléctrica (Megger & Banco)' },
  { key: 'AA', shortLabel: 'Aires AA', name: 'Climatización & Refrigeración' },
  { key: 'POWER', shortLabel: 'Fuerza DC', name: 'Energía Rectificadores & Baterías' },
];

const activeProtocolKey = ref('GE');

// Definición de Plantillas por Protocolo
const ALL_PROTOCOLS = {
  SPT: {
    title: 'Plantilla de Inspección Técnica SPT & Equipotencialidad',
    subtitle: 'Basado en norma SPT y resistencia equipotencial (Telurómetro & Método Wenner)',
    tasks: [
      {
        tarea: 'Medición de Resistencia de Puesta a Tierra (Sistema Principal BEP)',
        accion: 'Medir con Telurómetro y registrar valor en ohmios',
        completado: false,
        tipoInput: 'number',
        inputLabel: 'Resistencia SPT Medida',
        inputPlaceholder: 'Ej. 2.4',
        unidad: 'Ω',
        valorIngresado: '',
        criterioRef: '≤ 5.0 Ω (Cumple)'
      },
      {
        tarea: 'Resistividad de Terreno (Método de 4 picas Wenner)',
        accion: 'Registrar resistividad en celdas de prueba',
        completado: false,
        tipoInput: 'number',
        inputLabel: 'Resistividad Promedio',
        inputPlaceholder: 'Ej. 45.8',
        unidad: 'Ω·m',
        valorIngresado: '',
        criterioRef: 'Referencia Terreno'
      },
      {
        tarea: 'Equipotencialidad Gabinete RECTIFICADOR / POWER DC (-48V) a BEP',
        accion: 'Verificar unión de chasis metálico a barra de tierra BEP',
        completado: false,
        tipoInput: 'number',
        inputLabel: 'Impedancia de Unión',
        inputPlaceholder: 'Ej. 0.1',
        unidad: 'Ω',
        valorIngresado: '',
        criterioRef: '≤ 1.2 Ω (Cumple)'
      },
      {
        tarea: 'Equipotencialidad Rack / Gabinete de TRANSMISIÓN (MW IDU / Router / Switch)',
        accion: 'Inspección de cable de cobre desnudo a tierra',
        completado: false,
        tipoInput: 'number',
        inputLabel: 'Impedancia de Unión',
        inputPlaceholder: 'Ej. 0.2',
        unidad: 'Ω',
        valorIngresado: '',
        criterioRef: '≤ 1.2 Ω (Cumple)'
      },
      {
        tarea: 'Equipotencialidad Aires Acondicionados (Evaporador / Condensador AA-1 y AA-2)',
        accion: 'Verificar aterrizaje de chasis metálico',
        completado: false,
        tipoInput: 'number',
        inputLabel: 'Impedancia de Unión',
        inputPlaceholder: 'Ej. 0.15',
        unidad: 'Ω',
        valorIngresado: '',
        criterioRef: '≤ 1.2 Ω (Cumple)'
      },
      {
        tarea: 'Torre Metálica + Bajante LPS (Pararrayos) + Cerramiento Perimetral a BEP',
        accion: 'Inspeccionar integridad física de conectores y bajante LPS',
        completado: false,
        tipoInput: null
      }
    ]
  },
  GE: {
    title: 'Plantilla de Inspección Detallada & Pruebas 360 Grupo Electrógeno (GE/ATS)',
    subtitle: 'Pruebas Megger (Aislamiento), Banco Resistivo bajo Carga y Diagnóstico por Sistemas',
    tasks: [
      {
        tarea: 'Prueba Megger de Aislamiento Alternador Generador (U, V, W a Tierra @ 1000 Vdc)',
        accion: 'Medir resistencia de aislamiento a 1 minuto',
        completado: false,
        tipoInput: 'number',
        inputLabel: 'R@1min Promedio Medida',
        inputPlaceholder: 'Ej. 5.5',
        unidad: 'MΩ',
        valorIngresado: '',
        criterioRef: '≥ 5.0 MΩ (Apto)'
      },
      {
        tarea: 'Prueba con Banco Resistivo / Carga (Desempeño V L-L, Hz, Amperaje a 80-100% Carga)',
        accion: 'Someter a carga continua durante 60 minutos',
        completado: false,
        tipoInput: 'number',
        inputLabel: 'Voltaje L-L Estable Bajo Carga',
        inputPlaceholder: 'Ej. 220',
        unidad: 'V',
        valorIngresado: '',
        criterioRef: 'Tolerancia ± 5% (Apto)'
      },
      {
        tarea: 'Sistema de Generación: Tarjeta AVR y Bobinado de Alternador',
        accion: 'Verificar regulación de voltaje, estado físico de tarjeta AVR y devanados',
        completado: false,
        tipoInput: null
      },
      {
        tarea: 'Sistema de Combustible: Tanque de Día, Bomba, Inyectores y Filtros',
        accion: 'Inspeccionar ausencia de fugas, nivel de ACPM y purga de agua',
        completado: false,
        tipoInput: null
      },
      {
        tarea: 'Sistema de Motor y Lubricación: Nivel de Aceite Sintético y Filtros',
        accion: 'Revisión de presión de aceite de motor y estado de fluido',
        completado: false,
        tipoInput: null
      },
      {
        tarea: 'Sistema de Control y Conmutación: Tablero ATS / Controlador Módulo DeepSea',
        accion: 'Verificar transferencia automática Red-Planta y cargador de batería 12V',
        completado: false,
        tipoInput: null
      },
      {
        tarea: 'Registro de Certificados de Calibración de Instrumentos (Megóhmetro, Multímetro, Pinza)',
        accion: 'Comprobar vigencia de calibración de equipos de prueba',
        completado: false,
        tipoInput: null
      }
    ]
  },
  AA: {
    title: 'Plantilla de Inspección Técnica Climatización & Aires Acondicionados (AA)',
    subtitle: 'Mantenimiento Preventivo y Correctivo de Evaporadores, Condensadores y Gas Refrigerante',
    tasks: [
      {
        tarea: 'Inspección y Limpieza de Serpentín Evaporador y Condensador (AA-1 y AA-2)',
        accion: 'Lavar serpentines con desincrustante y soplado de disipadores',
        completado: false,
        tipoInput: null
      },
      {
        tarea: 'Medición de Presión de Gas Refrigerante (R410A / R22)',
        accion: 'Medir presión de succión y descarga con manómetro',
        completado: false,
        tipoInput: 'number',
        inputLabel: 'Presión de Succión Medida',
        inputPlaceholder: 'Ej. 120',
        unidad: 'PSI',
        valorIngresado: '',
        criterioRef: '110-130 PSI (Norma R410A)'
      },
      {
        tarea: 'Verificación de Consumo Eléctrico de Compresores (Amperaje Nominal)',
        accion: 'Medir corriente de trabajo con pinza amperimétrica',
        completado: false,
        tipoInput: 'number',
        inputLabel: 'Amperaje Medido',
        inputPlaceholder: 'Ej. 12.5',
        unidad: 'A',
        valorIngresado: '',
        criterioRef: '≤ I Nominal Placa'
      },
      {
        tarea: 'Revisión de Manguera de Drenaje, Bandeja de Condensados y Bomba',
        accion: 'Limpiar trayecto de drenaje y comprobar flujo continuo',
        completado: false,
        tipoInput: null
      },
      {
        tarea: 'Verificación de Secuenciador / Termostato de Alternancia de Equipos AA',
        accion: 'Probar cambio automático de equipo principal a respaldo cada 12 horas',
        completado: false,
        tipoInput: null
      }
    ]
  },
  POWER: {
    title: 'Plantilla de Inspección Técnica Sistemas de Energía & Fuerza (POWER DC / MT-SE)',
    subtitle: 'Protocolo de Mantenimiento Preventivo y Correctivo de Tableros y Módulos Rectificadores',
    tasks: [
      {
        tarea: 'Inspección Visual de Bornes, Cableado de Potencia y Apriete de Conexiones',
        accion: 'Torquear tornillería de barras principales y breakers',
        completado: false,
        tipoInput: null
      },
      {
        tarea: 'Verificación de Módulos Rectificadores 48V / 50A y Voltaje DC de Salida',
        accion: 'Medir tensión DC en barras de salida a baterías',
        completado: false,
        tipoInput: 'number',
        inputLabel: 'Voltaje Flotación DC Medido',
        inputPlaceholder: 'Ej. 54.2',
        unidad: 'Vdc',
        valorIngresado: '',
        criterioRef: '53.5 - 54.5 Vdc (Cumple)'
      },
      {
        tarea: 'Inspección de Banco de Baterías 12V / 100Ah VRLA AGM',
        accion: 'Medir voltaje individual de cada celda/monobloc en flotación',
        completado: false,
        tipoInput: 'number',
        inputLabel: 'Voltaje Promedio por Batería',
        inputPlaceholder: 'Ej. 13.5',
        unidad: 'Vdc',
        valorIngresado: '',
        criterioRef: '13.4 - 13.8 Vdc (Saludable)'
      },
      {
        tarea: 'Verificación de Interruptores Termomagnéticos (Breakers) y Fusibles DC',
        accion: 'Probar operatividad térmica y continuidad de fusibles',
        completado: false,
        tipoInput: null
      }
    ]
  }
};

// Estado reactivo para almacenar las tareas de cada protocolo
const protocolStates = ref({
  SPT: [],
  GE: [],
  AA: [],
  POWER: []
});

const getStorageKey = (key) => `smu_checklist_ot_${props.otId || 'general'}_${key}`;

// Determinar el protocolo por defecto según el subsistema de la OT
const detectDefaultProtocol = (subStr) => {
  const s = (subStr || '').toUpperCase();
  if (s.includes('SPT') || s.includes('TIERRA') || s.includes('PARARRAYOS')) return 'SPT';
  if (s.includes('GE') || s.includes('ATS') || s.includes('PLANTA') || s.includes('GENERADOR')) return 'GE';
  if (s.includes('AA') || s.includes('AIRE') || s.includes('CLIMA')) return 'AA';
  return 'POWER';
};

const activeTemplate = computed(() => ALL_PROTOCOLS[activeProtocolKey.value] || ALL_PROTOCOLS.GE);
const activeTasks = computed(() => protocolStates.value[activeProtocolKey.value] || []);

const activeCompletadosCount = computed(() => {
  return activeTasks.value.filter(t => t.completado).length;
});

const activePercentage = computed(() => {
  const total = activeTasks.value.length;
  return total > 0 ? Math.round((activeCompletadosCount.value / total) * 100) : 0;
});

const getProtocolProgress = (key) => {
  const tasksArr = protocolStates.value[key] || [];
  if (tasksArr.length === 0) return 0;
  const done = tasksArr.filter(t => t.completado).length;
  return Math.round((done / tasksArr.length) * 100);
};

const consolidatedPercent = computed(() => {
  const keys = Object.keys(ALL_PROTOCOLS);
  let totalTasks = 0;
  let totalDone = 0;
  keys.forEach(k => {
    const arr = protocolStates.value[k] || [];
    totalTasks += arr.length;
    totalDone += arr.filter(t => t.completado).length;
  });
  return totalTasks > 0 ? Math.round((totalDone / totalTasks) * 100) : 0;
});

const notifyUpdate = () => {
  emit('checklist-updated', { percentage: consolidatedPercent.value });
};

const loadAllSavedStates = () => {
  Object.keys(ALL_PROTOCOLS).forEach(key => {
    const baseTasks = ALL_PROTOCOLS[key].tasks.map(t => ({ ...t }));
    try {
      const savedRaw = localStorage.getItem(getStorageKey(key));
      if (savedRaw) {
        const savedArr = JSON.parse(savedRaw);
        baseTasks.forEach((t, i) => {
          if (savedArr[i]) {
            t.completado = !!savedArr[i].completado;
            if (savedArr[i].valorIngresado !== undefined && savedArr[i].valorIngresado !== null) {
              t.valorIngresado = savedArr[i].valorIngresado;
            }
          }
        });
      }
    } catch (e) {
      console.error(`Error al cargar avance de protocolo ${key}:`, e);
    }
    protocolStates.value[key] = baseTasks;
  });
  notifyUpdate();
};

const saveActiveState = () => {
  const key = activeProtocolKey.value;
  try {
    localStorage.setItem(getStorageKey(key), JSON.stringify(protocolStates.value[key].map(t => ({
      completado: t.completado,
      valorIngresado: t.valorIngresado
    }))));
  } catch (e) {
    console.error(`Error al guardar avance de protocolo ${key}:`, e);
  }
  notifyUpdate();
};

const selectProtocol = (key) => {
  activeProtocolKey.value = key;
};

watch([() => props.subsistema, () => props.otId], () => {
  activeProtocolKey.value = detectDefaultProtocol(props.subsistema);
  loadAllSavedStates();
}, { immediate: true });

onMounted(() => {
  activeProtocolKey.value = detectDefaultProtocol(props.subsistema);
  loadAllSavedStates();
});

const toggleTask = (index) => {
  protocolStates.value[activeProtocolKey.value][index].completado = !protocolStates.value[activeProtocolKey.value][index].completado;
  saveActiveState();
};

const onValueInput = (index) => {
  const val = protocolStates.value[activeProtocolKey.value][index].valorIngresado;
  if (val !== undefined && val !== null && String(val).trim() !== '') {
    protocolStates.value[activeProtocolKey.value][index].completado = true;
  }
  saveActiveState();
};
</script>

<template>
  <div class="space-y-4">
    <!-- Encabezado de Plantilla Técnica -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-4 space-y-3 shadow-sm transition-colors duration-300">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
        <div>
          <h4 class="text-xs font-extrabold text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
            <IconListCheck class="w-4 h-4 text-red-600 dark:text-red-400 stroke-[2]" />
            <span>{{ templateTitle }}</span>
          </h4>
          <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5 font-medium">
            {{ templateSubtitle }}
          </p>
        </div>
        <div class="bg-red-50 dark:bg-red-950/80 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 font-mono text-xs px-3 py-1.5 rounded-xl font-extrabold flex items-center gap-1.5 shadow-xs">
          <span>{{ completadosCount }} / {{ tasks.length }} Cumplidos</span>
          <span class="text-[10px] text-red-500 dark:text-red-400 font-normal">({{ percentageProgress }}%)</span>
        </div>
      </div>

      <!-- Leyenda de colores de plantilla oficial -->
      <div class="flex items-center justify-between text-[10px] bg-slate-50 dark:bg-slate-950 p-2.5 rounded-xl border border-slate-200/80 dark:border-slate-800/80 flex-wrap gap-2">
        <div class="flex items-center gap-2">
          <span class="font-bold text-slate-600 dark:text-slate-400">Guía de Diligenciamiento:</span>
          <span class="bg-amber-100 dark:bg-amber-950/80 text-amber-800 dark:text-amber-300 px-2 py-0.5 rounded font-bold border border-amber-300 dark:border-amber-700">Amarillo = Diligenciar en Campo</span>
          <span class="bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300 px-2 py-0.5 rounded font-bold border border-emerald-300 dark:border-emerald-700">Verde = Criterio de Referencia</span>
        </div>
        <div v-if="hasSavedState" class="text-emerald-600 dark:text-emerald-400 font-bold flex items-center gap-1 text-[10px]">
          ✓ Guardado automáticamente
        </div>
      </div>

      <!-- Lista de Verificación / Tareas Técnicas -->
      <div class="space-y-2.5 pt-1">
        <div
          v-for="(task, idx) in tasks"
          :key="idx"
          class="p-3 rounded-xl border transition-all shadow-xs space-y-2"
          :class="task.completado ? 'bg-emerald-50/60 dark:bg-emerald-950/20 border-emerald-300 dark:border-emerald-500/30' : 'bg-slate-50 dark:bg-slate-950/60 border-slate-200 dark:border-slate-800'"
        >
          <div class="flex items-start justify-between gap-3 cursor-pointer select-none" @click="toggleTask(idx)">
            <div class="flex items-start gap-3">
              <div
                class="w-5 h-5 rounded-lg flex items-center justify-center border transition-all shrink-0 mt-0.5"
                :class="task.completado ? 'bg-emerald-500 border-emerald-400 text-white shadow-xs' : 'border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900'"
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

          <!-- Campos especiales de medición (si aplica para la tarea) -->
          <div v-if="task.tipoInput" class="pt-2 border-t border-slate-200/60 dark:border-slate-800/60 flex items-center gap-3">
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

const hasSavedState = ref(false);

const storageKey = computed(() => `smu_checklist_ot_${props.otId || 'general'}`);

// Plantillas Oficiales basadas en los archivos Excel de referencia en /docs
const getTemplateData = (subsistemaStr) => {
  const sub = (subsistemaStr || '').toUpperCase();

  // 1. PUESTA A TIERRA / SPT (Basado en Plantilla para inspección técnica SPT ANT.Apartado.xlsx)
  if (sub.includes('SPT') || sub.includes('TIERRA') || sub.includes('PARARRAYOS')) {
    return {
      title: 'Plantilla de Inspección Técnica SPT & Equipotencialidad',
      subtitle: 'Basado en norma de referencia SPT y resistencia equipotencial (Telurómetro)',
      tasks: [
        {
          tarea: 'Medición de Resistencia de Puesta a Tierra (Sistema Principal BEP)',
          accion: 'Medir con Telurómetro y registrar valor',
          completado: false,
          tipoInput: 'number',
          inputLabel: 'Resistencia SPT Medida',
          inputPlaceholder: 'Ej. 2.4',
          unidad: 'Ω',
          valorIngresado: '',
          criterioRef: '≤ 5.0 Ω (Cumple)'
        },
        {
          tarea: 'Resistividad de Terreno (Método Wenner)',
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
    };
  }

  // 2. PLANTA ELÉCTRICA / GE / ATS / PRUEBAS 360 (Basado en Plantilla_Grupo_Electrogeno_360 y Diagnósticos GE SMU)
  if (sub.includes('GE') || sub.includes('ATS') || sub.includes('PLANTA') || sub.includes('GENERADOR')) {
    return {
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
    };
  }

  // 3. CLIMATIZACIÓN / AIRES ACONDICIONADOS (ME/MC AA)
  if (sub.includes('AA') || sub.includes('AIRE') || sub.includes('CLIMA')) {
    return {
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
    };
  }

  // 4. PLANTILLA GENERAL / SISTEMA ELÉCTRICO Y FUERZA (ME PW / ME MT-SE)
  return {
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
  };
};

const templateData = computed(() => getTemplateData(props.subsistema));
const templateTitle = computed(() => templateData.value.title);
const templateSubtitle = computed(() => templateData.value.subtitle);

const tasks = ref([]);

const completadosCount = computed(() => {
  return tasks.value.filter(t => t.completado).length;
});

const percentageProgress = computed(() => {
  const total = tasks.value.length;
  return total > 0 ? Math.round((completadosCount.value / total) * 100) : 0;
});

const notifyUpdate = () => {
  const total = tasks.value.length;
  const count = completadosCount.value;
  const percent = total > 0 ? Math.round((count / total) * 100) : 0;
  emit('checklist-updated', { completadosCount: count, totalCount: total, percentage: percent });
};

const loadSavedState = () => {
  const baseTasks = templateData.value.tasks.map(t => ({ ...t }));
  try {
    const savedRaw = localStorage.getItem(storageKey.value);
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
      hasSavedState.value = true;
    } else {
      hasSavedState.value = false;
    }
  } catch (e) {
    console.error('Error al cargar avance de checklist:', e);
  }
  tasks.value = baseTasks;
  notifyUpdate();
};

const saveCurrentState = () => {
  try {
    localStorage.setItem(storageKey.value, JSON.stringify(tasks.value.map(t => ({
      completado: t.completado,
      valorIngresado: t.valorIngresado
    }))));
    hasSavedState.value = true;
  } catch (e) {
    console.error('Error al guardar estado de checklist:', e);
  }
  notifyUpdate();
};

watch([() => props.subsistema, () => props.otId], () => {
  loadSavedState();
}, { immediate: true });

onMounted(loadSavedState);

const toggleTask = (index) => {
  tasks.value[index].completado = !tasks.value[index].completado;
  saveCurrentState();
};

const onValueInput = (index) => {
  const val = tasks.value[index].valorIngresado;
  if (val !== undefined && val !== null && String(val).trim() !== '') {
    tasks.value[index].completado = true;
  }
  saveCurrentState();
};
</script>

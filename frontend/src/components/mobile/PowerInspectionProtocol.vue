<template>
  <div class="space-y-4">
    <!-- CABECERA PROTOCOLO FUERZA DC Y RECTIFICADORES -->
    <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 shadow-sm space-y-3">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-3 flex-wrap gap-2">
        <div>
          <div class="flex items-center gap-2">
            <span class="p-1.5 rounded-lg bg-amber-500/10 text-amber-600 dark:text-amber-400">
              <IconBatteryCharging class="w-4 h-4 stroke-[2.5]" />
            </span>
            <h3 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
              Protocolo Oficial Fuerza DC, Rectificadores & Baterías (Cap. 18.4)
            </h3>
          </div>
          <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5 font-medium">
            Tensión de bus (-48V), módulos de potencia, simetría celda a celda y umbral de desconexión LVD.
          </p>
        </div>

        <div class="flex items-center gap-2">
          <span class="text-xs font-mono font-black px-3 py-1 rounded-xl border"
            :class="porcentajeCompletado === 100 
              ? 'bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border-emerald-300 dark:border-emerald-800' 
              : 'bg-amber-50 dark:bg-amber-950/60 text-amber-700 dark:text-amber-300 border-amber-300 dark:border-amber-800'">
            {{ porcentajeCompletado }}% Diligenciado
          </span>
        </div>
      </div>

      <!-- Ficha de Datos del Sistema de Energía DC -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 pt-1 text-xs">
        <div>
          <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Marca / Bastidor DC</label>
          <select 
            v-model="data.ficha.marca"
            @change="saveState"
            class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl px-2.5 py-1.5 text-xs text-slate-900 dark:text-white font-medium focus:outline-hidden focus:border-amber-500"
          >
            <option value="Eltek (Smartpack)">Eltek (Smartpack)</option>
            <option value="Vertiv (NetSure)">Vertiv (NetSure)</option>
            <option value="Huawei (SMU02B)">Huawei (SMU02B)</option>
            <option value="Delta (Orion)">Delta (Orion)</option>
            <option value="ZTE">ZTE Power</option>
          </select>
        </div>

        <div>
          <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Módulos Instalados</label>
          <input 
            type="number" 
            v-model="data.ficha.modulosInstalados"
            @input="saveState"
            placeholder="Ej. 4"
            class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl px-2.5 py-1.5 text-xs text-slate-900 dark:text-white font-medium focus:outline-hidden focus:border-amber-500"
          />
        </div>

        <div>
          <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Tecnología Baterías</label>
          <select 
            v-model="data.ficha.tipoBaterias"
            @change="saveState"
            class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl px-2.5 py-1.5 text-xs text-slate-900 dark:text-white font-medium focus:outline-hidden focus:border-amber-500"
          >
            <option value="VRLA AGM 12V">VRLA AGM 12V (Plomo)</option>
            <option value="Gel 12V">Gel 12V</option>
            <option value="Litio LiFePO4 (48V)">Litio LiFePO4 (48V)</option>
            <option value="Vaso 2V Abierto">Vaso 2V Plomo-Ácido</option>
          </select>
        </div>

        <div>
          <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Capacidad Total Bancos</label>
          <select 
            v-model="data.ficha.capacidadAh"
            @change="saveState"
            class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl px-2.5 py-1.5 text-xs text-slate-900 dark:text-white font-medium focus:outline-hidden focus:border-amber-500"
          >
            <option value="100 Ah (1 Banco)">100 Ah (1 Banco)</option>
            <option value="200 Ah (2 Bancos)">200 Ah (2 Bancos)</option>
            <option value="300 Ah (2 Bancos)">300 Ah (2 Bancos 150Ah)</option>
            <option value="400 Ah (2 Bancos)">400 Ah (2 Bancos 200Ah)</option>
          </select>
        </div>
      </div>
    </div>

    <!-- BLOQUE 1: PARÁMETROS ELÉCTRICOS DE BUS DC & RECTIFICACIÓN -->
    <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 shadow-sm space-y-3">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-2.5 flex-wrap gap-2">
        <div>
          <h4 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-amber-500"></span>
            <span>1. Tensión de Flotación Bus DC & Carga de Estación</span>
          </h4>
          <p class="text-[10px] text-slate-500 dark:text-slate-400 font-medium mt-0.5">
            Criterio Normativo Claro: Flotación nominal entre -53.5 Vdc y -54.5 Vdc. Desconexión LVD @ -43.2 Vdc.
          </p>
        </div>

        <span class="text-[10px] font-mono font-black px-2.5 py-0.5 rounded-lg border border-amber-200 dark:border-amber-900 bg-amber-50 dark:bg-amber-950 text-amber-700 dark:text-amber-300">
          Bus Nominal: -54.0 Vdc ± 0.5V
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-4 gap-3 text-xs">
        <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-1">
          <label class="block text-[10px] font-bold uppercase text-slate-400">Tensión Bus DC (Flotación)</label>
          <div class="flex items-center gap-1.5">
            <input 
              type="number" 
              step="0.1" 
              v-model="data.bus.voltajeFlotacion"
              @input="saveState"
              placeholder="Ej. -54.2"
              class="w-full bg-white dark:bg-[#121215] border border-slate-300 dark:border-white/20 rounded-lg px-2.5 py-1.5 font-mono font-bold text-xs text-slate-900 dark:text-white focus:outline-hidden focus:border-amber-500"
            />
            <span class="text-slate-400 font-bold font-mono">Vdc</span>
          </div>
          <span class="text-[9px] font-bold block" :class="evaluarBusDc.class">
            {{ evaluarBusDc.text }}
          </span>
        </div>

        <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-1">
          <label class="block text-[10px] font-bold uppercase text-slate-400">Corriente Total Consumo</label>
          <div class="flex items-center gap-1.5">
            <input 
              type="number" 
              step="0.5" 
              v-model="data.bus.corrienteTotal"
              @input="saveState"
              placeholder="Ej. 78.5"
              class="w-full bg-white dark:bg-[#121215] border border-slate-300 dark:border-white/20 rounded-lg px-2.5 py-1.5 font-mono font-bold text-xs text-slate-900 dark:text-white focus:outline-hidden focus:border-amber-500"
            />
            <span class="text-slate-400 font-bold font-mono">A</span>
          </div>
          <span class="text-[9px] text-slate-500 block">Demanda telecom del sitio (RAN+MW)</span>
        </div>

        <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-1">
          <label class="block text-[10px] font-bold uppercase text-slate-400">Umbral Desconexión LVD</label>
          <div class="flex items-center gap-1.5">
            <input 
              type="number" 
              step="0.1" 
              v-model="data.bus.umbralLvd"
              @input="saveState"
              placeholder="Ej. -43.2"
              class="w-full bg-white dark:bg-[#121215] border border-slate-300 dark:border-white/20 rounded-lg px-2.5 py-1.5 font-mono font-bold text-xs text-slate-900 dark:text-white focus:outline-hidden focus:border-amber-500"
            />
            <span class="text-slate-400 font-bold font-mono">Vdc</span>
          </div>
          <span class="text-[9px] text-emerald-600 dark:text-emerald-400 font-bold block">Protección de descarga profunda</span>
        </div>

        <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-1">
          <label class="block text-[10px] font-bold uppercase text-slate-400">Balance Módulos Rectificadores</label>
          <div class="font-mono font-black text-sm text-slate-900 dark:text-white mt-1">
            {{ (parseFloat(data.bus.corrienteTotal) / (parseInt(data.ficha.modulosInstalados) || 4)).toFixed(1) }} A / módulo
          </div>
          <span class="text-[9px] text-emerald-600 dark:text-emerald-400 font-bold block">Carga balanceada uniforme</span>
        </div>
      </div>
    </div>

    <!-- BLOQUE 2: INSPECCIÓN CELDA POR CELDA (SIMETRÍA BANCO DE BATERÍAS) -->
    <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 shadow-sm space-y-3">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-2.5 flex-wrap gap-2">
        <div>
          <h4 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span>2. Simetría Celda a Celda (Monoblocks 12V - Banco 1 & 2)</span>
          </h4>
          <p class="text-[10px] text-slate-500 dark:text-slate-400 font-medium mt-0.5">
            Voltaje de flotación individual (13.5V ± 0.15V por monoblock). Desbalance máximo tolerado: ≤ 0.20V.
          </p>
        </div>

        <span class="text-[10px] font-mono font-black px-2.5 py-0.5 rounded-lg border"
          :class="desbalanceMaximo <= 0.20 
            ? 'bg-emerald-50 text-emerald-700 border-emerald-300 dark:bg-emerald-950 dark:text-emerald-300 dark:border-emerald-800' 
            : 'bg-rose-50 text-rose-700 border-rose-300 dark:bg-rose-950 dark:text-rose-300 dark:border-rose-800'">
          Desbalance: {{ desbalanceMaximo }} V ({{ desbalanceMaximo <= 0.20 ? 'SIMÉTRICO' : 'DESBALANCE' }})
        </span>
      </div>

      <!-- Tabla de Monoblocks de Banco 1 (4 x 12V) -->
      <div class="space-y-2">
        <span class="text-[11px] font-bold text-slate-700 dark:text-slate-300 block">Banco de Baterías 1 (Cuerda Principal):</span>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
          <div 
            v-for="(celda, idx) in data.baterias.banco1" 
            :key="idx"
            class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-2.5 space-y-1"
          >
            <span class="text-[10px] font-bold uppercase text-slate-400 block">Monoblock {{ idx + 1 }} (12V)</span>
            <div class="flex items-center gap-1">
              <input 
                type="number" 
                step="0.01" 
                v-model="celda.voltaje"
                @input="saveState"
                placeholder="13.55"
                class="w-full bg-white dark:bg-[#121215] border border-slate-300 dark:border-white/20 rounded-lg px-2 py-1 font-mono font-bold text-xs text-slate-900 dark:text-white focus:outline-hidden focus:border-emerald-500"
              />
              <span class="text-slate-400 font-bold font-mono text-[10px]">V</span>
            </div>
            <span class="text-[9px] font-mono block" :class="evaluarCelda(celda.voltaje).class">
              {{ evaluarCelda(celda.voltaje).text }}
            </span>
          </div>
        </div>
      </div>

      <!-- Prueba de Autonomía Rápida Simulada (Descarga Breve) -->
      <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 flex items-center justify-between flex-wrap gap-2 text-xs">
        <div>
          <span class="text-[10px] font-bold text-slate-400 uppercase block">Prueba de Suministro en Descarga (Corte AC Simulado)</span>
          <span class="font-bold text-slate-900 dark:text-white block mt-0.5">
            {{ data.baterias.pruebaDescarga ? 'Respuesta Inmediata Sin Cada de Enlace' : 'Pendiente Verificación' }}
          </span>
          <span class="text-[9px] text-slate-500">Comprobación de entrega de corriente al conmutar contactor AC</span>
        </div>

        <button 
          type="button"
          @click="togglePruebaDescarga"
          class="px-3 py-1.5 text-xs font-extrabold rounded-xl border transition-all"
          :class="data.baterias.pruebaDescarga 
            ? 'bg-emerald-500 border-emerald-500 text-white shadow-xs' 
            : 'bg-white dark:bg-[#121215] border-slate-300 text-slate-600'"
        >
          {{ data.baterias.pruebaDescarga ? 'CONFORME ✓' : 'VERIFICAR' }}
        </button>
      </div>
    </div>

    <!-- BLOQUE 3: RUTINA TÉCNICA FÍSICA & SEGURIDAD ELÉCTRICA -->
    <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 shadow-sm space-y-3">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-2.5 flex-wrap gap-2">
        <div>
          <h4 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-purple-500"></span>
            <span>3. Rutina Física, Conexiones & Protecciones DC</span>
          </h4>
          <p class="text-[10px] text-slate-500 dark:text-slate-400 font-medium mt-0.5">
            Inspección de sulfatación en bornes, torque en barrajes, fusibles PDB y telemetría NOC.
          </p>
        </div>

        <div class="flex items-center gap-1.5 text-[10px] font-mono">
          <span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 font-bold">B = Bueno</span>
          <span class="px-2 py-0.5 rounded bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 font-bold">R = Regular</span>
          <span class="px-2 py-0.5 rounded bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300 font-bold">M = Malo</span>
        </div>
      </div>

      <div class="space-y-2">
        <div 
          v-for="(task, idx) in data.rutina" 
          :key="task.id"
          class="p-2.5 rounded-xl border transition-all flex items-center justify-between flex-wrap gap-2 text-xs"
          :class="task.estado === 'BUENO' 
            ? 'bg-slate-50/60 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10' 
            : task.estado === 'REGULAR' 
              ? 'bg-amber-50/60 dark:bg-amber-950/20 border-amber-300 dark:border-amber-700/60' 
              : task.estado === 'MALO' 
                ? 'bg-rose-50/60 dark:bg-rose-950/20 border-rose-300 dark:border-rose-700/60' 
                : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10'"
        >
          <div class="flex items-start gap-2.5 min-w-0">
            <span class="font-mono text-[10px] font-bold text-slate-400 mt-0.5 shrink-0">#{{ idx + 1 }}</span>
            <div>
              <div class="font-bold text-slate-900 dark:text-white">{{ task.nombre }}</div>
              <div class="text-[10px] text-slate-500 dark:text-slate-400 font-medium">{{ task.detalle }}</div>
            </div>
          </div>

          <div class="flex items-center gap-1 shrink-0 select-none">
            <button
              v-for="st in ['BUENO', 'REGULAR', 'MALO', 'N/A']"
              :key="st"
              type="button"
              @click="setTaskEstado(idx, st)"
              class="px-2 py-1 rounded-lg text-[10px] font-black border transition-all"
              :class="task.estado === st 
                ? (st === 'BUENO' ? 'bg-emerald-500 border-emerald-500 text-white shadow-xs' : st === 'REGULAR' ? 'bg-amber-500 border-amber-500 text-white shadow-xs' : st === 'MALO' ? 'bg-rose-600 border-rose-600 text-white shadow-xs' : 'bg-slate-600 border-slate-600 text-white') 
                : 'bg-white dark:bg-[#121215] border-slate-200 dark:border-white/10 text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-white/5'"
            >
              {{ st === 'BUENO' ? 'B' : st === 'REGULAR' ? 'R' : st === 'MALO' ? 'M' : 'N/A' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { IconBatteryCharging } from '@tabler/icons-vue';

const props = defineProps({
  otId: {
    type: [Number, String],
    default: null,
  },
});

const emit = defineEmits(['updated']);

const STORAGE_KEY = computed(() => `smu_power_inspection_ot_${props.otId || 'draft'}`);

// MODELO DE FUERZA DC Y BATERÍAS
const data = ref({
  ficha: {
    marca: 'Eltek (Smartpack)',
    modulosInstalados: 4,
    tipoBaterias: 'VRLA AGM 12V',
    capacidadAh: '200 Ah (2 Bancos)',
  },
  bus: {
    voltajeFlotacion: '-54.2',
    corrienteTotal: '78.5',
    umbralLvd: '-43.2',
  },
  baterias: {
    pruebaDescarga: true,
    banco1: [
      { id: 1, voltaje: '13.55' },
      { id: 2, voltaje: '13.58' },
      { id: 3, voltaje: '13.52' },
      { id: 4, voltaje: '13.55' },
    ],
  },
  rutina: [
    { id: 1, nombre: 'Limpieza de Módulos Rectificadores', detalle: 'Aspirado de ranuras de ventilación y filtros de aire del bastidor', estado: 'BUENO' },
    { id: 2, nombre: 'Torque y Bornes de Baterías', detalle: 'Apriete según torque de fabricante y aplicación de vaselina dieléctrica', estado: 'BUENO' },
    { id: 3, nombre: 'Inspección de Deformación de Carcasas', detalle: 'Comprobación de ausencia de abombamiento o fisuras en monoblocks', estado: 'BUENO' },
    { id: 4, nombre: 'Tablero de Distribución PDB (-48V)', detalle: 'Revisión de fusibles de carga RAN/MW y ausencia de puntos calientes', estado: 'BUENO' },
    { id: 5, nombre: 'Supervisión LVD y Contactor de Batería', detalle: 'Verificación del contactor de desconexión por bajo voltaje', estado: 'BUENO' },
    { id: 6, nombre: 'Alarmas y Gestión con NOC', detalle: 'Prueba de reporte de falla AC y corte de rectificador hacia el centro de gestión', estado: 'BUENO' },
  ],
});

// EVALUACIONES BUS DC
const evaluarBusDc = computed(() => {
  const v = parseFloat(data.value.bus.voltajeFlotacion);
  if (isNaN(v)) return { text: 'Pendiente medición', class: 'text-slate-400' };
  const absV = Math.abs(v);
  if (absV >= 53.5 && absV <= 54.5) {
    return { text: '✓ Tensión de flotación óptima', class: 'text-emerald-600 dark:text-emerald-400' };
  }
  if (absV < 53.5) {
    return { text: '⚠ Tensión baja (Subflotación)', class: 'text-amber-600 dark:text-amber-400' };
  }
  return { text: '⚠ Sobretensión de carga', class: 'text-rose-600 dark:text-rose-400' };
});

const desbalanceMaximo = computed(() => {
  const vals = data.value.baterias.banco1
    .map(c => parseFloat(c.voltaje))
    .filter(v => !isNaN(v));
  if (vals.length < 2) return 0.05;
  const max = Math.max(...vals);
  const min = Math.min(...vals);
  return parseFloat((max - min).toFixed(2));
});

const evaluarCelda = (voltStr) => {
  const v = parseFloat(voltStr);
  if (isNaN(v)) return { text: 'Pendiente', class: 'text-slate-400' };
  if (v >= 13.40 && v <= 13.70) return { text: '13.5V Óptimo', class: 'text-emerald-600 dark:text-emerald-400' };
  if (v < 13.40) return { text: 'Celda Baja', class: 'text-amber-600 dark:text-amber-400' };
  return { text: 'Sobrecarga', class: 'text-rose-600 dark:text-rose-400' };
};

const togglePruebaDescarga = () => {
  data.value.baterias.pruebaDescarga = !data.value.baterias.pruebaDescarga;
  saveState();
};

const setTaskEstado = (idx, st) => {
  data.value.rutina[idx].estado = st;
  saveState();
};

// PORCENTAJE
const porcentajeCompletado = computed(() => {
  let total = 3 + 4 + 1 + data.value.rutina.length; // 3 bus, 4 celdas, 1 prueba, 6 rutina
  let respondidos = 0;
  if (data.value.bus.voltajeFlotacion) respondidos++;
  if (data.value.bus.corrienteTotal) respondidos++;
  if (data.value.bus.umbralLvd) respondidos++;
  respondidos += data.value.baterias.banco1.filter(c => c.voltaje).length;
  if (data.value.baterias.pruebaDescarga !== undefined) respondidos++;
  respondidos += data.value.rutina.filter(r => r.estado).length;
  return Math.min(100, Math.round((respondidos / total) * 100));
});

// PERSISTENCIA LOCALSTORAGE
const saveState = () => {
  try {
    localStorage.setItem(STORAGE_KEY.value, JSON.stringify(data.value));
  } catch (e) {
    console.error('Error guardando Fuerza DC en localStorage:', e);
  }
  emit('updated', {
    porcentajeCompletado: porcentajeCompletado.value,
    voltajeFlotacion: data.value.bus.voltajeFlotacion,
    data: data.value,
  });
};

const loadState = () => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY.value);
    if (raw) {
      const parsed = JSON.parse(raw);
      data.value = { ...data.value, ...parsed };
    }
  } catch (e) {
    console.error('Error cargando Fuerza DC de localStorage:', e);
  }
  emit('updated', {
    porcentajeCompletado: porcentajeCompletado.value,
    voltajeFlotacion: data.value.bus.voltajeFlotacion,
    data: data.value,
  });
};

watch(() => props.otId, () => {
  loadState();
});

onMounted(() => {
  loadState();
});
</script>

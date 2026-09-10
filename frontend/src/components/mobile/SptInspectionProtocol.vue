<template>
  <div class="space-y-4">
    <!-- CABECERA DEL PROTOCOLO SPT -->
    <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 shadow-sm space-y-3">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-3 flex-wrap gap-2">
        <div>
          <div class="flex items-center gap-2">
            <span class="p-1.5 rounded-lg bg-amber-500/10 text-amber-600 dark:text-amber-400">
              <IconBolt class="w-4 h-4 stroke-[2.5]" />
            </span>
            <h3 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
              Protocolo Oficial SPT & Equipotencialidad (Plantilla SMU)
            </h3>
          </div>
          <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5 font-medium">
            Resistividad Wenner, Caída de Potencial (62%) y Matriz de Continuidad según RETIE / IEC.
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

      <!-- Ficha de Instrumento y Terreno -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 pt-1 text-xs">
        <div>
          <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Condición de Suelo</label>
          <select 
            v-model="data.ficha.condicionSuelo"
            @change="saveState"
            class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl px-2.5 py-1.5 text-xs text-slate-900 dark:text-white focus:outline-hidden focus:border-red-600 font-medium"
          >
            <option value="Suelo de concreto / losa">Suelo de concreto / losa</option>
            <option value="Terreno natural (tierra húmeda)">Terreno natural (tierra húmeda)</option>
            <option value="Terreno arcilloso / mixto">Terreno arcilloso / mixto</option>
            <option value="Terreno rocoso / cascajo">Terreno rocoso / cascajo</option>
          </select>
        </div>

        <div>
          <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Instrumento Utilizado</label>
          <input 
            type="text" 
            v-model="data.ficha.instrumento"
            @input="saveState"
            placeholder="Ej. Telurómetro AEMC 4630"
            class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl px-2.5 py-1.5 text-xs text-slate-900 dark:text-white font-medium focus:outline-hidden focus:border-red-600"
          />
        </div>

        <div>
          <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Electrodo / Malla Evaluada</label>
          <input 
            type="text" 
            v-model="data.ficha.electrodoBajoPrueba"
            @input="saveState"
            placeholder="Ej. Malla torre + anillo perimetral"
            class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl px-2.5 py-1.5 text-xs text-slate-900 dark:text-white font-medium focus:outline-hidden focus:border-red-600"
          />
        </div>
      </div>
    </div>

    <!-- BLOQUE 1: RESISTIVIDAD WENNER DE 4 PICAS -->
    <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 shadow-sm space-y-3">
      <div class="flex items-center justify-between flex-wrap gap-2 border-b border-slate-100 dark:border-white/10 pb-2.5">
        <div>
          <h4 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-amber-500"></span>
            <span>1. Resistividad de Terreno (Método Wenner de 4 Picas)</span>
          </h4>
          <p class="text-[10px] text-slate-500 dark:text-slate-400 font-medium mt-0.5">
            Cálculo automático de ρ = 2·π·a·R (Ω·m). Umbrales: ≤100 Conductor | 100-300 Intermedio | >300 Alta Resistividad.
          </p>
        </div>

        <!-- Conmutador de Imposibilidad Física (Plantilla Oficial) -->
        <div class="flex items-center gap-1.5">
          <button 
            type="button"
            @click="toggleWennerAplica(true)"
            class="px-2.5 py-1 rounded-lg text-[10px] font-extrabold border transition-all"
            :class="data.wenner.aplica 
              ? 'bg-amber-500 border-amber-500 text-white shadow-xs' 
              : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10 text-slate-600 dark:text-slate-400'"
          >
            Medir en Terreno
          </button>
          <button 
            type="button"
            @click="toggleWennerAplica(false)"
            class="px-2.5 py-1 rounded-lg text-[10px] font-extrabold border transition-all"
            :class="!data.wenner.aplica 
              ? 'bg-rose-600 border-rose-600 text-white shadow-xs' 
              : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10 text-slate-600 dark:text-slate-400'"
          >
            No Aplica (Imposibilidad Física)
          </button>
        </div>
      </div>

      <!-- Caso: No Aplica por Imposibilidad Física -->
      <div v-if="!data.wenner.aplica" class="bg-amber-50/60 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900/60 rounded-xl p-3 space-y-2">
        <div class="flex items-center gap-2 text-xs font-bold text-amber-800 dark:text-amber-300">
          <IconAlertTriangle class="w-4 h-4 shrink-0" />
          <span>Excepción Técnica Documentada en Plantilla SMU</span>
        </div>
        <p class="text-[11px] text-slate-600 dark:text-slate-400">
          Justificación por imposibilidad física de realizar el método (sitio en azotea, sobre losa perimetral de concreto, o sin retiro perimetral suficiente para el tendido de picas).
        </p>
        <textarea 
          v-model="data.wenner.justificacionNoAplica"
          @input="saveState"
          rows="2"
          class="w-full bg-white dark:bg-[#0a0b10] border border-amber-300 dark:border-amber-800/80 rounded-lg p-2 text-xs text-slate-900 dark:text-white focus:outline-hidden"
          placeholder="Escriba la justificación técnica..."
        ></textarea>
      </div>

      <!-- Caso: Tabla de Lecturas Wenner -->
      <div v-else class="space-y-3">
        <div class="overflow-x-auto border border-slate-200 dark:border-white/10 rounded-xl">
          <table class="w-full text-xs text-left">
            <thead class="bg-slate-50 dark:bg-white/5 text-[10px] font-black uppercase text-slate-500 border-b border-slate-200 dark:border-white/10">
              <tr>
                <th class="py-2 px-3 text-center">Separación a (m)</th>
                <th class="py-2 px-3">Resistencia Medida R (Ω)</th>
                <th class="py-2 px-3 text-right">Resistividad ρ (Ω·m)</th>
                <th class="py-2 px-3 text-center">Clasificación Terreno</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-white/5">
              <tr v-for="(row, idx) in data.wenner.lecturas" :key="idx" class="hover:bg-slate-50/60 dark:hover:bg-white/[0.02]">
                <td class="py-2 px-3 font-mono font-bold text-center text-slate-700 dark:text-slate-300">
                  {{ row.separacion }} m
                </td>
                <td class="py-1.5 px-3">
                  <div class="flex items-center gap-1.5">
                    <input 
                      type="number" 
                      step="0.01" 
                      v-model="row.r"
                      @input="calcularRho(idx)"
                      placeholder="Ej. 12.5"
                      class="w-24 bg-amber-50/70 dark:bg-amber-950/30 border border-amber-300 dark:border-amber-700/60 rounded-lg px-2 py-1 font-mono font-bold text-xs text-slate-900 dark:text-white focus:outline-hidden focus:border-amber-500"
                    />
                    <span class="text-slate-400 font-mono text-[11px]">Ω</span>
                  </div>
                </td>
                <td class="py-2 px-3 text-right font-mono font-black" :class="row.rho ? 'text-slate-900 dark:text-white' : 'text-slate-400'">
                  {{ row.rho !== null ? row.rho + ' Ω·m' : '—' }}
                </td>
                <td class="py-2 px-3 text-center">
                  <span v-if="row.rho !== null" class="text-[9px] font-extrabold px-2 py-0.5 rounded-full"
                    :class="row.rho <= 100 
                      ? 'bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300' 
                      : row.rho <= 300 
                        ? 'bg-amber-100 dark:bg-amber-950 text-amber-800 dark:text-amber-300' 
                        : 'bg-rose-100 dark:bg-rose-950 text-rose-800 dark:text-rose-300'">
                    {{ row.rho <= 100 ? 'Conductor' : row.rho <= 300 ? 'Intermedio' : 'Alta Resistividad' }}
                  </span>
                  <span v-else class="text-[10px] text-slate-400">—</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Consolidado Wenner -->
        <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 flex items-center justify-between flex-wrap gap-2 text-xs">
          <div>
            <span class="text-[10px] font-bold text-slate-400 uppercase block">Resistividad Promedio Ponderada (ρ̄)</span>
            <span class="font-mono font-black text-sm text-slate-900 dark:text-white">
              {{ rhoPromedio !== null ? rhoPromedio + ' Ω·m' : 'Sin lecturas completas' }}
            </span>
          </div>
          <div v-if="rhoPromedio !== null">
            <span class="text-[10px] font-black px-2.5 py-1 rounded-lg"
              :class="rhoPromedio <= 300 
                ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' 
                : 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300'">
              {{ rhoPromedio <= 300 ? 'Cumple Criterio de Diseño (≤ 300 Ω·m)' : 'Requiere Malla Expandida (> 300 Ω·m)' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- BLOQUE 2: RESISTENCIA DE PUESTA A TIERRA (CAÍDA DE POTENCIAL 62%) -->
    <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 shadow-sm space-y-3">
      <div class="flex items-center justify-between flex-wrap gap-2 border-b border-slate-100 dark:border-white/10 pb-2.5">
        <div>
          <h4 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-red-600"></span>
            <span>2. Resistencia de Puesta a Tierra (Método Caída de Potencial - 62%)</span>
          </h4>
          <p class="text-[10px] text-slate-500 dark:text-slate-400 font-medium mt-0.5">
            Criterio Normativo RETIE / IEC: R(SPT) ≤ 5.0 Ω para Estaciones de Telecomunicaciones.
          </p>
        </div>

        <span class="text-[10px] font-mono font-black px-2.5 py-0.5 rounded-lg border border-red-200 dark:border-red-900 bg-red-50 dark:bg-red-950 text-red-700 dark:text-red-300">
          Criterio Máximo: ≤ 5.0 Ω
        </span>
      </div>

      <div class="overflow-x-auto border border-slate-200 dark:border-white/10 rounded-xl">
        <table class="w-full text-xs text-left">
          <thead class="bg-slate-50 dark:bg-white/5 text-[10px] font-black uppercase text-slate-500 border-b border-slate-200 dark:border-white/10">
            <tr>
              <th class="py-2 px-3 text-center">Distancia P (%)</th>
              <th class="py-2 px-3 text-center">Distancia (m)</th>
              <th class="py-2 px-3">Resistencia Medida (Ω)</th>
              <th class="py-2 px-3 text-center">Evaluación RETIE</th>
              <th class="py-2 px-3">Diagnóstico Técnico</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 dark:divide-white/5">
            <tr 
              v-for="(row, idx) in data.caidaPotencial.lecturas" 
              :key="idx"
              :class="row.porcentaje === 62 ? 'bg-amber-50/40 dark:bg-amber-950/15 font-medium' : 'hover:bg-slate-50/60 dark:hover:bg-white/[0.02]'"
            >
              <td class="py-2 px-3 text-center font-mono font-bold">
                <span :class="row.porcentaje === 62 ? 'px-1.5 py-0.5 rounded bg-amber-200 dark:bg-amber-900 text-amber-950 dark:text-amber-200 font-black' : ''">
                  {{ row.porcentaje }}%
                </span>
              </td>
              <td class="py-2 px-3 text-center font-mono text-slate-500">
                {{ row.distanciaM }} m
              </td>
              <td class="py-1.5 px-3">
                <div class="flex items-center gap-1.5">
                  <input 
                    type="number" 
                    step="0.01" 
                    v-model="row.r"
                    @input="evaluarCaidaPotencial(idx)"
                    placeholder="Ej. 3.4"
                    class="w-24 bg-amber-50/70 dark:bg-amber-950/30 border border-amber-300 dark:border-amber-700/60 rounded-lg px-2 py-1 font-mono font-bold text-xs text-slate-900 dark:text-white focus:outline-hidden focus:border-amber-500"
                  />
                  <span class="text-slate-400 font-mono text-[11px]">Ω</span>
                </div>
              </td>
              <td class="py-2 px-3 text-center">
                <span 
                  v-if="row.cumple !== null" 
                  class="text-[9px] font-black px-2 py-0.5 rounded-full"
                  :class="row.cumple 
                    ? 'bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300' 
                    : 'bg-rose-100 dark:bg-rose-950 text-rose-800 dark:text-rose-300'"
                >
                  {{ row.cumple ? 'CUMPLE (≤ 5.0 Ω)' : 'NO CUMPLE (> 5.0 Ω)' }}
                </span>
                <span v-else class="text-[10px] text-slate-400">—</span>
              </td>
              <td class="py-2 px-3 text-[11px] text-slate-600 dark:text-slate-400">
                {{ row.obs || '—' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Concepto Automático del Sistema de Puesta a Tierra -->
      <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 flex items-center justify-between flex-wrap gap-2 text-xs">
        <div>
          <span class="text-[10px] font-bold text-slate-400 uppercase block">Concepto Técnico Oficial (Punto 62% Referencia)</span>
          <span class="font-bold text-slate-900 dark:text-white flex items-center gap-1.5 mt-0.5">
            <span class="font-mono text-sm font-black">{{ resistencia62Valor !== null ? resistencia62Valor + ' Ω' : 'Pendiente' }}</span>
            <span v-if="resistencia62Valor !== null" class="text-[10px] text-slate-500">
              ({{ resistencia62Valor <= 5.0 ? 'Dentro del margen normativo RETIE' : 'Excede límite máximo permitido' }})
            </span>
          </span>
        </div>

        <div v-if="resistencia62Valor !== null">
          <span class="text-xs font-black px-3 py-1 rounded-xl uppercase tracking-wider"
            :class="resistencia62Valor <= 5.0 
              ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800' 
              : 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300 border border-rose-300 dark:border-rose-800'">
            {{ resistencia62Valor <= 5.0 ? 'ESTADO: APTO' : 'ESTADO: NO APTO (CORRECTIVO)' }}
          </span>
        </div>
      </div>
    </div>

    <!-- BLOQUE 3: MATRIZ DE EQUIPOTENCIALIDAD Y CONTINUIDAD (11 PUNTOS CRÍTICOS) -->
    <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 shadow-sm space-y-3">
      <div class="flex items-center justify-between flex-wrap gap-2 border-b border-slate-100 dark:border-white/10 pb-2.5">
        <div>
          <h4 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span>3. Matriz de Equipotencialidad y Continuidad (11 Puntos Críticos)</span>
          </h4>
          <p class="text-[10px] text-slate-500 dark:text-slate-400 font-medium mt-0.5">
            Continuidad eléctrica medida hacia la Barra Equipotencial Principal (BEP). Criterio: ≤ 1.2 Ω.
          </p>
        </div>

        <div class="text-xs font-mono font-black text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60 px-2.5 py-1 rounded-xl border border-emerald-200 dark:border-emerald-800">
          {{ equipotencialidadCumplidos }} / {{ data.equipotencialidad.puntos.length }} Conformes
        </div>
      </div>

      <div class="overflow-x-auto border border-slate-200 dark:border-white/10 rounded-xl">
        <table class="w-full text-xs text-left">
          <thead class="bg-slate-50 dark:bg-white/5 text-[10px] font-black uppercase text-slate-500 border-b border-slate-200 dark:border-white/10">
            <tr>
              <th class="py-2 px-3 text-center">#</th>
              <th class="py-2 px-3">Elemento / Subsistema en Terreno</th>
              <th class="py-2 px-3">Lectura (Ω)</th>
              <th class="py-2 px-3 text-center">Evaluación</th>
              <th class="py-2 px-3">Acción Sugerida</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 dark:divide-white/5">
            <tr v-for="(p, idx) in data.equipotencialidad.puntos" :key="p.id" class="hover:bg-slate-50/60 dark:hover:bg-white/[0.02]">
              <td class="py-2.5 px-3 font-mono text-center text-slate-400">{{ idx + 1 }}</td>
              <td class="py-2.5 px-3">
                <div class="font-bold text-slate-900 dark:text-white text-xs">{{ p.nombre }}</div>
                <div class="text-[10px] text-slate-500 dark:text-slate-400">{{ p.descripcion }}</div>
              </td>
              <td class="py-1.5 px-3">
                <div class="flex items-center gap-1.5">
                  <input 
                    type="number" 
                    step="0.01" 
                    v-model="p.valorR"
                    @input="evaluarEquipotencialidad(idx)"
                    placeholder="Ej. 0.4"
                    class="w-20 bg-amber-50/70 dark:bg-amber-950/30 border border-amber-300 dark:border-amber-700/60 rounded-lg px-2 py-1 font-mono font-bold text-xs text-slate-900 dark:text-white focus:outline-hidden focus:border-amber-500"
                  />
                  <span class="text-slate-400 font-mono text-[11px]">Ω</span>
                </div>
              </td>
              <td class="py-2.5 px-3 text-center">
                <span 
                  v-if="p.cumple !== null" 
                  class="text-[9px] font-black px-2 py-0.5 rounded-full"
                  :class="p.cumple 
                    ? 'bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300' 
                    : 'bg-rose-100 dark:bg-rose-950 text-rose-800 dark:text-rose-300'"
                >
                  {{ p.cumple ? 'CUMPLE (≤ 1.2 Ω)' : 'NO CUMPLE' }}
                </span>
                <span v-else class="text-[10px] text-slate-400">—</span>
              </td>
              <td class="py-2.5 px-3 text-[11px] text-slate-600 dark:text-slate-400">
                <span :class="p.cumple === false ? 'font-bold text-rose-600 dark:text-rose-400' : ''">
                  {{ p.accionSugerida || '—' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { IconBolt, IconAlertTriangle } from '@tabler/icons-vue';

const props = defineProps({
  otId: {
    type: [Number, String],
    default: null,
  },
});

const emit = defineEmits(['updated']);

const STORAGE_KEY = computed(() => `smu_spt_inspection_ot_${props.otId || 'draft'}`);

// MODELO DE DATOS BASADO EN PLANTILLA OFICIAL DE CLARO / SMU
const data = ref({
  ficha: {
    condicionSuelo: 'Suelo de concreto / losa',
    instrumento: 'Telurómetro AEMC 4630 (Modo Caída 62% y Wenner)',
    electrodoBajoPrueba: 'Malla puesta a tierra telecom (Torre + Contenedor)',
  },
  wenner: {
    aplica: false, // Por defecto en sitios tipo Apartado es frecuente que aplique excepción de losa
    justificacionNoAplica: 'No aplica por imposibilidad física de realizar el método (sitio sobre losa perimetral de concreto sin acceso a suelo natural).',
    lecturas: [
      { separacion: 1, r: '', rho: null },
      { separacion: 2, r: '', rho: null },
      { separacion: 4, r: '', rho: null },
      { separacion: 8, r: '', rho: null },
      { separacion: 10, r: '', rho: null },
      { separacion: 12, r: '', rho: null },
      { separacion: 14, r: '', rho: null },
    ],
  },
  caidaPotencial: {
    criterioMax: 5.0,
    lecturas: [
      { porcentaje: 20, distanciaM: 10, r: '4.8', cumple: true, obs: 'R dentro de umbral normal' },
      { porcentaje: 40, distanciaM: 20, r: '4.6', cumple: true, obs: 'R dentro de umbral normal' },
      { porcentaje: 62, distanciaM: 31, r: '4.3', cumple: true, obs: 'R óptima conforme RETIE (≤ 5.0 Ω)' },
      { porcentaje: 80, distanciaM: 40, r: '4.5', cumple: true, obs: 'Meseta de potencial estable' },
    ],
  },
  equipotencialidad: {
    puntos: [
      { id: 1, nombre: 'Barra Equipotencial Principal (BEP)', descripcion: 'Barraje maestro de tierra del sitio (Punto de referencia cero)', valorR: '0.05', cumple: true, accionSugerida: 'Punto de referencia verificado' },
      { id: 2, nombre: 'Gabinete RAN / BTS (Acceso Celular)', descripcion: 'Chasis metálico y bornes de tierra de gabinetes BBU / DU', valorR: '0.40', cumple: true, accionSugerida: 'Sin acción (Continuidad óptima)' },
      { id: 3, nombre: 'Gabinete Transmisión (MW / Router)', descripcion: 'Chasis metálico de switches, routers y modem microondas', valorR: '0.35', cumple: true, accionSugerida: 'Sin acción (Continuidad óptima)' },
      { id: 4, nombre: 'Gabinete Rectificador / Power DC (-48V)', descripcion: 'Chasis, puerta y barra de retorno del rectificador', valorR: '0.20', cumple: true, accionSugerida: 'Sin acción (Continuidad óptima)' },
      { id: 5, nombre: 'Bancos de Baterías (-48V)', descripcion: 'Bandejas y rack metálico portabaterías', valorR: '0.30', cumple: true, accionSugerida: 'Sin acción (Continuidad óptima)' },
      { id: 6, nombre: 'Tablero de Distribución DC (PDB)', descripcion: 'Carcasa metálica y barrajes de distribución de cargas DC', valorR: '0.25', cumple: true, accionSugerida: 'Sin acción (Continuidad óptima)' },
      { id: 7, nombre: 'Tablero General AC / TGP', descripcion: 'Carcasa metálica, borne PE y DPS de acometida', valorR: '0.15', cumple: true, accionSugerida: 'Sin acción (Continuidad óptima)' },
      { id: 8, nombre: 'Transferencia Automática (ATS)', descripcion: 'Chasis de contactores y gabinete de control ATS', valorR: '0.45', cumple: true, accionSugerida: 'Sin acción (Continuidad óptima)' },
      { id: 9, nombre: 'Grupo Electrógeno (Planta)', descripcion: 'Bastidor antivibratorio y carcasa de alternador', valorR: '0.60', cumple: true, accionSugerida: 'Sin acción (Continuidad óptima)' },
      { id: 10, nombre: 'Aires Acondicionados (AA-1 y AA-2)', descripcion: 'Chasis de evaporadores y condensadores exteriores', valorR: '0.50', cumple: true, accionSugerida: 'Sin acción (Continuidad óptima)' },
      { id: 11, nombre: 'Torre / Bajante LPS (Pararrayos)', descripcion: 'Pata de torre de telecomunicaciones y cerramiento perimetral a BEP', valorR: '0.70', cumple: true, accionSugerida: 'Sin acción (Continuidad óptima)' },
    ],
  },
});

// CALCULOS WENNER
const toggleWennerAplica = (val) => {
  data.value.wenner.aplica = val;
  saveState();
};

const calcularRho = (idx) => {
  const item = data.value.wenner.lecturas[idx];
  const rNum = parseFloat(item.r);
  if (!isNaN(rNum) && rNum > 0) {
    // Formula oficial: rho = 2 * PI * a * R
    item.rho = parseFloat((2 * Math.PI * item.separacion * rNum).toFixed(1));
  } else {
    item.rho = null;
  }
  saveState();
};

const rhoPromedio = computed(() => {
  if (!data.value.wenner.aplica) return null;
  const validos = data.value.wenner.lecturas.filter(l => l.rho !== null);
  if (validos.length === 0) return null;
  const suma = validos.reduce((acc, curr) => acc + curr.rho, 0);
  return parseFloat((suma / validos.length).toFixed(1));
});

// CALCULOS CAIDA DE POTENCIAL 62%
const evaluarCaidaPotencial = (idx) => {
  const item = data.value.caidaPotencial.lecturas[idx];
  const rNum = parseFloat(item.r);
  if (!isNaN(rNum)) {
    item.cumple = rNum <= 5.0;
    item.obs = item.cumple ? 'R conforme norma RETIE (≤ 5.0 Ω)' : 'R alta (> 5.0 Ω) → acondicionar suelo o expandir malla';
  } else {
    item.cumple = null;
    item.obs = '';
  }
  saveState();
};

const resistencia62Valor = computed(() => {
  const punto62 = data.value.caidaPotencial.lecturas.find(l => l.porcentaje === 62);
  if (punto62 && punto62.r !== '' && !isNaN(parseFloat(punto62.r))) {
    return parseFloat(punto62.r);
  }
  return null;
});

// CALCULOS EQUIPOTENCIALIDAD
const evaluarEquipotencialidad = (idx) => {
  const punto = data.value.equipotencialidad.puntos[idx];
  const val = parseFloat(punto.valorR);
  if (!isNaN(val)) {
    punto.cumple = val <= 1.2;
    punto.accionSugerida = punto.cumple ? 'Sin acción (Continuidad óptima)' : 'Ajustar / limpiar unión de terminal a BEP y reapretar';
  } else {
    punto.cumple = null;
    punto.accionSugerida = '';
  }
  saveState();
};

const equipotencialidadCumplidos = computed(() => {
  return data.value.equipotencialidad.puntos.filter(p => p.cumple === true).length;
});

// PORCENTAJE DE DILIGENCIAMIENTO
const porcentajeCompletado = computed(() => {
  let totalPuntos = 1 + 4 + data.value.equipotencialidad.puntos.length; // Wenner (aplica o no), 4 caida, 11 equipotencialidad
  let logrados = 0;

  if (!data.value.wenner.aplica || rhoPromedio.value !== null) logrados += 1;

  const caidaValidos = data.value.caidaPotencial.lecturas.filter(l => l.cumple !== null).length;
  logrados += caidaValidos;

  const eqValidos = data.value.equipotencialidad.puntos.filter(p => p.cumple !== null).length;
  logrados += eqValidos;

  return Math.min(100, Math.round((logrados / totalPuntos) * 100));
});

// PERSISTENCIA LOCALSTORAGE
const saveState = () => {
  try {
    localStorage.setItem(STORAGE_KEY.value, JSON.stringify(data.value));
  } catch (e) {
    console.error('Error guardando SPT en localStorage:', e);
  }
  emit('updated', {
    porcentajeCompletado: porcentajeCompletado.value,
    resistencia62: resistencia62Valor.value,
    equipotencialidadOk: equipotencialidadCumplidos.value === data.value.equipotencialidad.puntos.length,
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
    console.error('Error cargando SPT de localStorage:', e);
  }
  emit('updated', {
    porcentajeCompletado: porcentajeCompletado.value,
    resistencia62: resistencia62Valor.value,
    equipotencialidadOk: equipotencialidadCumplidos.value === data.value.equipotencialidad.puntos.length,
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

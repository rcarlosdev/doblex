<template>
  <div class="space-y-4">
    <!-- 1. TARJETA DE FICHA TÉCNICA DE LA PLANTA & HORÓMETRO -->
    <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-4 shadow-sm transition-colors duration-300">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-3 flex-wrap gap-2">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-600 dark:text-amber-400 flex items-center justify-center">
            <IconEngine class="w-4 h-4 stroke-[2]" />
          </div>
          <div>
            <h4 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
              Ficha Técnica del Grupo Electrógeno (GE)
            </h4>
            <p class="text-[11px] text-slate-500 dark:text-slate-400 font-medium">
              Datos de placa y horómetro según Anexo Técnico SMU
            </p>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-slate-100 dark:bg-white/5 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-white/10">
            Vida Útil: {{ vidaUtilCalculada }}% (25.000h)
          </span>
        </div>
      </div>

      <!-- Fila de Horómetro y Vida Útil -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 bg-amber-50/50 dark:bg-amber-950/20 border border-amber-200/80 dark:border-amber-900/40 rounded-xl p-3">
        <div class="space-y-1">
          <label class="text-[10px] font-extrabold text-amber-900 dark:text-amber-300 uppercase tracking-wide flex items-center gap-1">
            <span>Horómetro Actual *</span>
            <span class="text-rose-500">*</span>
          </label>
          <div class="flex items-center gap-1.5">
            <input
              type="number"
              v-model.number="ficha.horometro"
              @input="saveChanges"
              placeholder="Ej. 184"
              class="w-full bg-white dark:bg-[#0a0b10] border border-amber-300 dark:border-amber-700/80 rounded-lg px-2.5 py-1.5 text-xs font-mono font-bold text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:outline-none"
            />
            <span class="text-xs font-bold text-amber-800 dark:text-amber-400 font-mono">Horas</span>
          </div>
        </div>

        <div class="space-y-1">
          <label class="text-[10px] font-extrabold text-amber-900 dark:text-amber-300 uppercase tracking-wide">
            % Vida Útil Consumida
          </label>
          <div class="h-8 flex items-center px-2.5 rounded-lg bg-white/70 dark:bg-[#0a0b10] border border-amber-300/60 dark:border-amber-700/50">
            <span class="text-xs font-mono font-extrabold text-slate-800 dark:text-slate-200">
              {{ vidaUtilCalculada }}%
            </span>
          </div>
        </div>

        <div class="space-y-1">
          <label class="text-[10px] font-extrabold text-amber-900 dark:text-amber-300 uppercase tracking-wide">
            Estado Operacional Planta *
          </label>
          <select
            v-model="ficha.estado_operacional"
            @change="saveChanges"
            class="w-full h-8 bg-white dark:bg-[#0a0b10] border border-amber-300 dark:border-amber-700/80 rounded-lg px-2 text-xs font-bold text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-amber-500 focus:outline-none cursor-pointer"
          >
            <option value="OPERATIVO">OPERATIVO</option>
            <option value="FUERA_DE_SERVICIO">FUERA DE SERVICIO</option>
            <option value="EN_FALLA">EN ALERTA / FALLA PARCIAL</option>
          </select>
        </div>
      </div>

      <!-- Datos de Placa Planta & Generador -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 pt-1">
        <div class="space-y-1">
          <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase">Fabricante Planta</label>
          <input
            v-model="ficha.fabricante_planta"
            @input="saveChanges"
            placeholder="CUMMINS"
            class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-lg px-2.5 py-1 text-xs text-slate-800 dark:text-white font-medium"
          />
        </div>

        <div class="space-y-1">
          <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase">Modelo Planta</label>
          <input
            v-model="ficha.modelo_planta"
            @input="saveChanges"
            placeholder="60DGCB"
            class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-lg px-2.5 py-1 text-xs text-slate-800 dark:text-white font-medium"
          />
        </div>

        <div class="space-y-1">
          <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase">Capacidad Efectiva (KW)</label>
          <input
            type="number"
            v-model.number="ficha.potencia_kw"
            @input="saveChanges"
            placeholder="60"
            class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-lg px-2.5 py-1 text-xs text-slate-800 dark:text-white font-mono font-bold"
          />
        </div>

        <div class="space-y-1">
          <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase">Capacidad Total (KVA)</label>
          <input
            type="number"
            v-model.number="ficha.potencia_kva"
            @input="saveChanges"
            placeholder="75"
            class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-lg px-2.5 py-1 text-xs text-slate-800 dark:text-white font-mono font-bold"
          />
        </div>

        <div class="space-y-1">
          <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase">Fabricante Generador</label>
          <input
            v-model="ficha.fabricante_generador"
            @input="saveChanges"
            placeholder="STAMFORD"
            class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-lg px-2.5 py-1 text-xs text-slate-800 dark:text-white font-medium"
          />
        </div>

        <div class="space-y-1">
          <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase">Modelo Generador</label>
          <input
            v-model="ficha.modelo_generador"
            @input="saveChanges"
            placeholder="UCI224E / NO VISIBLE"
            class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-lg px-2.5 py-1 text-xs text-slate-800 dark:text-white font-medium"
          />
        </div>

        <div class="space-y-1">
          <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase">Estado Físico General</label>
          <select
            v-model="ficha.estado_fisico"
            @change="saveChanges"
            class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-lg px-2 py-1 text-xs font-medium text-slate-800 dark:text-white cursor-pointer"
          >
            <option value="BUENO">BUENO</option>
            <option value="REGULAR">REGULAR</option>
            <option value="MALO">MALO</option>
          </select>
        </div>

        <div class="space-y-1">
          <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase">Tipo de Control</label>
          <select
            v-model="ficha.tipo_control"
            @change="saveChanges"
            class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-lg px-2 py-1 text-xs font-bold text-slate-800 dark:text-white cursor-pointer"
          >
            <option value="digital">Digital (Comap / DeepSea)</option>
            <option value="analogo">Análogo (Relojes / Llave)</option>
          </select>
        </div>
      </div>
    </div>

    <!-- 2. PRUEBAS CUANTITATIVAS OBLIGATORIAS (MEGGER & BANCO DE CARGA) -->
    <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3 shadow-sm">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-2.5">
        <div class="flex items-center gap-2">
          <IconBolt class="w-4 h-4 text-red-600 dark:text-red-400 stroke-[2]" />
          <h4 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
            Pruebas Cuantitativas & Parámetros Normativos
          </h4>
        </div>
        <span class="text-[10px] font-bold text-slate-500 dark:text-slate-400">Criterios de Aceptación</span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <!-- Megger -->
        <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-slate-900 dark:text-white">Aislamiento Megger Alternador</span>
            <span
              class="text-[9px] font-mono font-bold px-1.5 py-0.5 rounded"
              :class="mediciones.megger >= 5 ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300'"
            >
              {{ mediciones.megger >= 5 ? 'CUMPLE (≥ 5.0 MΩ)' : 'DEGRADADO (< 5.0 MΩ)' }}
            </span>
          </div>
          <div class="text-[10px] text-slate-500 dark:text-slate-400">U, V, W a Tierra @ 1000 Vdc a 1 min</div>
          <div class="flex items-center gap-2">
            <input
              type="number"
              step="0.1"
              v-model.number="mediciones.megger"
              @input="saveChanges"
              placeholder="Ej. 5.5"
              class="flex-1 bg-amber-50 dark:bg-amber-950/40 border border-amber-300 dark:border-amber-700/80 rounded-lg px-2.5 py-1.5 text-xs font-mono font-bold text-slate-900 dark:text-white"
            />
            <span class="text-xs font-bold font-mono text-slate-600 dark:text-slate-400">MΩ</span>
          </div>
        </div>

        <!-- Banco de Carga -->
        <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-slate-900 dark:text-white">Voltaje L-L Bajo Carga (60 min)</span>
            <span class="text-[9px] font-mono font-bold px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
              Ref: 208-230 V (± 5%)
            </span>
          </div>
          <div class="text-[10px] text-slate-500 dark:text-slate-400">Desempeño con banco resistivo 80-100% carga</div>
          <div class="flex items-center gap-2">
            <input
              type="number"
              v-model.number="mediciones.voltaje_carga"
              @input="saveChanges"
              placeholder="Ej. 220"
              class="flex-1 bg-amber-50 dark:bg-amber-950/40 border border-amber-300 dark:border-amber-700/80 rounded-lg px-2.5 py-1.5 text-xs font-mono font-bold text-slate-900 dark:text-white"
            />
            <span class="text-xs font-bold font-mono text-slate-600 dark:text-slate-400">VAC</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 3. INSPECCIÓN DE LOS 8 SUBSISTEMAS DEL EXCEL -->
    <div class="space-y-3">
      <div class="flex items-center justify-between px-1">
        <h4 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
          <IconChecklist class="w-4 h-4 text-red-600 dark:text-red-400 stroke-[2]" />
          <span>Evaluación Detallada por Subsistemas (8 Sistemas)</span>
        </h4>
        <span class="text-[10px] font-mono font-bold text-slate-500">
          {{ subsistemasEvaluadosCount }} / {{ totalComponentesCount }} Componentes
        </span>
      </div>

      <!-- Tarjeta de cada uno de los 8 Subsistemas -->
      <div
        v-for="sist in subsistemasList"
        :key="sist.id"
        class="bg-white dark:bg-[#121215] border rounded-2xl p-4 space-y-3 shadow-sm transition-all"
        :class="sist.tieneFalla ? 'border-rose-300 dark:border-rose-900/60 bg-rose-50/10' : 'border-slate-200 dark:border-white/10'"
      >
        <!-- Cabecera del Subsistema -->
        <div class="flex items-center justify-between flex-wrap gap-2">
          <div class="flex items-center gap-2">
            <component :is="sist.icon" class="w-4 h-4 text-slate-700 dark:text-slate-300 stroke-[2]" />
            <h5 class="text-xs font-extrabold text-slate-900 dark:text-white">
              {{ sist.numero }}. {{ sist.nombre }}
            </h5>
          </div>

          <div class="flex items-center gap-1.5">
            <span
              v-if="sist.tieneFalla"
              class="px-2 py-0.5 rounded text-[9px] font-black uppercase tracking-wider bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300 border border-rose-300 dark:border-rose-800"
            >
              Con Hallazgo (RCA)
            </span>
            <span
              v-else-if="sist.todoBueno"
              class="px-2 py-0.5 rounded text-[9px] font-black uppercase tracking-wider bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300"
            >
              100% Conforme
            </span>
          </div>
        </div>

        <!-- Componentes a evaluar con selector rápido tipo semáforo -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 pt-1">
          <div
            v-for="comp in sist.componentes"
            :key="comp.key"
            class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200/80 dark:border-white/5 rounded-xl p-2.5 flex items-center justify-between gap-2"
          >
            <span class="text-xs font-bold text-slate-800 dark:text-slate-200 truncate" :title="comp.label">
              {{ comp.label }}
            </span>

            <!-- Botones semáforo: B, R, M, N/A -->
            <div class="inline-flex rounded-lg border border-slate-200 dark:border-white/10 p-0.5 bg-white dark:bg-[#121215] shrink-0">
              <button
                type="button"
                @click="setComponentStatus(comp.key, 'BUENO')"
                class="px-2 py-1 rounded text-[10px] font-black transition-all"
                :class="estadosComponentes[comp.key] === 'BUENO' ? 'bg-emerald-600 text-white shadow-xs' : 'text-slate-500 hover:text-slate-800 dark:hover:text-white'"
                title="Bueno (Operativo)"
              >
                B
              </button>
              <button
                type="button"
                @click="setComponentStatus(comp.key, 'REGULAR')"
                class="px-2 py-1 rounded text-[10px] font-black transition-all"
                :class="estadosComponentes[comp.key] === 'REGULAR' ? 'bg-amber-500 text-white shadow-xs' : 'text-slate-500 hover:text-slate-800 dark:hover:text-white'"
                title="Regular (Desgaste / Requiere atención)"
              >
                R
              </button>
              <button
                type="button"
                @click="setComponentStatus(comp.key, 'MALO')"
                class="px-2 py-1 rounded text-[10px] font-black transition-all"
                :class="estadosComponentes[comp.key] === 'MALO' ? 'bg-rose-600 text-white shadow-xs' : 'text-slate-500 hover:text-slate-800 dark:hover:text-white'"
                title="Malo (Falla / Avería)"
              >
                M
              </button>
              <button
                type="button"
                @click="setComponentStatus(comp.key, 'NO_APLICA')"
                class="px-1.5 py-1 rounded text-[9px] font-black transition-all"
                :class="estadosComponentes[comp.key] === 'NO_APLICA' ? 'bg-slate-500 text-white shadow-xs' : 'text-slate-400 hover:text-slate-600'"
                title="No Aplica"
              >
                N/A
              </button>
            </div>
          </div>
        </div>

        <!-- 4. BLOQUE DINÁMICO DE HALLAZGO & ANÁLISIS RCA (Si algún componente está Regular o Malo) -->
        <div v-if="sist.tieneFalla" class="mt-3 pt-3 border-t border-rose-200 dark:border-rose-900/50 space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-xs font-black text-rose-700 dark:text-rose-400 flex items-center gap-1.5">
              <IconAlertTriangle class="w-4 h-4 stroke-[2.2]" />
              <span>Diagnóstico de Falla & Causa Raíz (RCA - {{ sist.nombre }})</span>
            </span>
            <span class="text-[9px] font-bold text-rose-600 dark:text-rose-400 uppercase bg-rose-100 dark:bg-rose-950/80 px-2 py-0.5 rounded">
              Requerido por Plantilla Claro/Inmel
            </span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            <div class="space-y-1">
              <label class="text-[10px] font-extrabold text-slate-700 dark:text-slate-300 uppercase">Descripción del Hallazgo *</label>
              <textarea
                v-model="hallazgos[sist.id].descripcion"
                @input="saveChanges"
                rows="2"
                placeholder="Ej. Deterioro en tarjeta AVR y desprendimiento de barniz en devanado..."
                class="w-full bg-rose-50/40 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900/50 rounded-xl p-2 text-xs text-slate-900 dark:text-white"
              ></textarea>
            </div>

            <div class="space-y-1">
              <label class="text-[10px] font-extrabold text-slate-700 dark:text-slate-300 uppercase">Acción Recomendada / Insumos *</label>
              <textarea
                v-model="hallazgos[sist.id].accion_recomendada"
                @input="saveChanges"
                rows="2"
                placeholder="Ej. Cambio de tarjeta AVR reguladora y mantenimiento de alternador..."
                class="w-full bg-rose-50/40 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900/50 rounded-xl p-2 text-xs text-slate-900 dark:text-white"
              ></textarea>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
            <div class="space-y-1">
              <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase">Nivel de Criticidad</label>
              <select
                v-model="hallazgos[sist.id].criticidad"
                @change="saveChanges"
                class="w-full h-8 bg-white dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-lg px-2 text-xs font-bold text-slate-800 dark:text-white cursor-pointer"
              >
                <option value="Alta">Alta (Afecta Disponibilidad)</option>
                <option value="Media">Media (Desgaste Programable)</option>
                <option value="Baja">Baja (Observación Menor)</option>
              </select>
            </div>

            <div class="space-y-1">
              <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase">Causa Inmediata</label>
              <input
                v-model="hallazgos[sist.id].causa_inmediata"
                @input="saveChanges"
                placeholder="Ej. Sobretemperatura / Corto"
                class="w-full bg-white dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-lg px-2 py-1 text-xs text-slate-800 dark:text-white"
              />
            </div>

            <div class="space-y-1">
              <label class="text-[10px] font-bold text-slate-600 dark:text-slate-400 uppercase">Causa Raíz</label>
              <input
                v-model="hallazgos[sist.id].causa_raiz"
                @input="saveChanges"
                placeholder="Ej. Desgaste por tiempo de operación"
                class="w-full bg-white dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-lg px-2 py-1 text-xs text-slate-800 dark:text-white"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import {
  IconEngine,
  IconBolt,
  IconChecklist,
  IconAlertTriangle,
  IconCpu,
  IconGauge,
  IconWind,
  IconFlame,
  IconGasStation,
  IconBuildingWarehouse
} from '@tabler/icons-vue';

const props = defineProps({
  otId: {
    type: [Number, String],
    default: null,
  },
});

const emit = defineEmits(['updated']);

// 1. Ficha Técnica y Placa
const ficha = ref({
  horometro: 184,
  estado_operacional: 'OPERATIVO',
  fabricante_planta: 'CUMMINS',
  modelo_planta: '60DGCB',
  potencia_kw: 60,
  potencia_kva: 75,
  fabricante_generador: 'STAMFORD',
  modelo_generador: 'UCI224E',
  estado_fisico: 'BUENO',
  tipo_control: 'digital'
});

// 2. Mediciones Cuantitativas
const mediciones = ref({
  megger: 5.5,
  voltaje_carga: 220
});

// % Vida útil calculada automáticamente sobre 25.000 horas
const vidaUtilCalculada = computed(() => {
  const h = Number(ficha.value.horometro) || 0;
  return ((h / 25000) * 100).toFixed(2);
});

// 3. Definición de los 8 Subsistemas del Excel
const definicionSubsistemas = [
  {
    id: 'generacion',
    numero: '1',
    nombre: 'Sistema de Generación',
    icon: IconBolt,
    componentes: [
      { key: 'gen_devanado', label: 'Estado Devanados' },
      { key: 'gen_avr', label: 'Tarjeta Reguladora AVR' },
      { key: 'gen_general', label: 'Generador en General' }
    ]
  },
  {
    id: 'motor',
    numero: '2',
    nombre: 'Sistema de Motor y Combustible',
    icon: IconEngine,
    componentes: [
      { key: 'mot_pistones', label: 'Pistones y Compresión' },
      { key: 'mot_bomba_inyeccion', label: 'Bomba de Inyección' },
      { key: 'mot_admision', label: 'Sistema de Admisión / Filtros' },
      { key: 'mot_general', label: 'Motor en General' }
    ]
  },
  {
    id: 'control',
    numero: '3',
    nombre: 'Sistema de Control y Conmutación',
    icon: IconCpu,
    componentes: [
      { key: 'ctrl_tablero', label: 'Tablero de Control' },
      { key: 'ctrl_parametros', label: 'Parámetros Eléctricos / Medidores' },
      { key: 'ctrl_cableado', label: 'Arnés de Cableado' },
      { key: 'ctrl_botones', label: 'Botones Paro / Arranque' },
      { key: 'ctrl_general', label: 'Control en General' }
    ]
  },
  {
    id: 'refrigeracion',
    numero: '4',
    nombre: 'Sistema de Refrigeración',
    icon: IconWind,
    componentes: [
      { key: 'ref_radiador', label: 'Radiador y Panal' },
      { key: 'ref_ventilador', label: 'Ventilador y Aspas' },
      { key: 'ref_bomba_agua', label: 'Bomba de Agua y Sellos' },
      { key: 'ref_termostato', label: 'Termostato' },
      { key: 'ref_mangueras', label: 'Mangueras y Tuberías' },
      { key: 'ref_sensor', label: 'Sensor de Temperatura' },
      { key: 'ref_refrigerante', label: 'Nivel y Estado Refrigerante' }
    ]
  },
  {
    id: 'electrico',
    numero: '5',
    nombre: 'Sistema Eléctrico de Fuerza y Arranque',
    icon: IconGauge,
    componentes: [
      { key: 'elec_alternador', label: 'Alternador Auxiliar 12/24V' },
      { key: 'elec_bateria', label: 'Batería de Arranque' },
      { key: 'elec_cargador', label: 'Cargador Estático de Batería' },
      { key: 'elec_motor_arranque', label: 'Motor de Arranque Eléctrico' },
      { key: 'elec_disyuntor', label: 'Disyuntor Termomagnético Principal' },
      { key: 'elec_spt', label: 'Puesta a Tierra Chasis (SPT)' },
      { key: 'elec_ats', label: 'Transferencia Automática (ATS)' }
    ]
  },
  {
    id: 'escape',
    numero: '6',
    nombre: 'Sistema de Escape y Gases',
    icon: IconFlame,
    componentes: [
      { key: 'esc_multiple', label: 'Múltiple de Escape' },
      { key: 'esc_tubo', label: 'Tubo y Fuelles de Escape' },
      { key: 'esc_silenciador', label: 'Silenciador / Mofle' },
      { key: 'esc_aislante', label: 'Aislantes Térmicos / Lonas' }
    ]
  },
  {
    id: 'alimentacion',
    numero: '7',
    nombre: 'Alimentación de Combustible',
    icon: IconGasStation,
    componentes: [
      { key: 'comb_tanque', label: 'Tanque Diario de Almacenamiento' },
      { key: 'comb_filtracion', label: 'Filtración y Vaso Trampa' },
      { key: 'comb_mangueras', label: 'Mangueras de Retorno y Suministro' }
    ]
  },
  {
    id: 'cabina',
    numero: '8',
    nombre: 'Cabina Insonorizada (Canopy)',
    icon: IconBuildingWarehouse,
    componentes: [
      { key: 'cab_estructura', label: 'Estructura Física y Pintura' },
      { key: 'cab_aislamiento', label: 'Aislamiento Acústico' },
      { key: 'cab_ventilacion', label: 'Ventilación y Persianas' },
      { key: 'cab_puertas', label: 'Cerraduras, Bisagras y Puertas' }
    ]
  }
];

// Estados individuales de cada componente
const estadosComponentes = ref({});

// Diagnóstico / RCA por subsistema
const hallazgos = ref({
  generacion: { descripcion: '', accion_recomendada: '', criticidad: 'Alta', causa_inmediata: '', causa_raiz: '' },
  motor: { descripcion: '', accion_recomendada: '', criticidad: 'Media', causa_inmediata: '', causa_raiz: '' },
  control: { descripcion: '', accion_recomendada: '', criticidad: 'Media', causa_inmediata: '', causa_raiz: '' },
  refrigeracion: { descripcion: '', accion_recomendada: '', criticidad: 'Media', causa_inmediata: '', causa_raiz: '' },
  electrico: { descripcion: '', accion_recomendada: '', criticidad: 'Alta', causa_inmediata: '', causa_raiz: '' },
  escape: { descripcion: '', accion_recomendada: '', criticidad: 'Baja', causa_inmediata: '', causa_raiz: '' },
  alimentacion: { descripcion: '', accion_recomendada: '', criticidad: 'Media', causa_inmediata: '', causa_raiz: '' },
  cabina: { descripcion: '', accion_recomendada: '', criticidad: 'Baja', causa_inmediata: '', causa_raiz: '' },
});

// Inicializar componentes por defecto en BUENO
definicionSubsistemas.forEach(s => {
  s.componentes.forEach(c => {
    estadosComponentes.value[c.key] = 'BUENO';
  });
});

const setComponentStatus = (key, status) => {
  estadosComponentes.value[key] = status;
  saveChanges();
};

const subsistemasList = computed(() => {
  return definicionSubsistemas.map(s => {
    const comps = s.componentes;
    const tieneFalla = comps.some(c => estadosComponentes.value[c.key] === 'REGULAR' || estadosComponentes.value[c.key] === 'MALO');
    const todoBueno = comps.every(c => estadosComponentes.value[c.key] === 'BUENO');
    return {
      ...s,
      tieneFalla,
      todoBueno
    };
  });
});

const totalComponentesCount = computed(() => {
  return definicionSubsistemas.reduce((acc, s) => acc + s.componentes.length, 0);
});

const subsistemasEvaluadosCount = computed(() => {
  let count = 0;
  definicionSubsistemas.forEach(s => {
    s.componentes.forEach(c => {
      if (estadosComponentes.value[c.key]) count++;
    });
  });
  return count;
});

// Clave de persistencia en localStorage
const storageKey = computed(() => `smu_ge_inspection_ot_${props.otId || 'general'}`);

const loadSavedData = () => {
  try {
    const raw = localStorage.getItem(storageKey.value);
    if (raw) {
      const data = JSON.parse(raw);
      if (data.ficha) ficha.value = { ...ficha.value, ...data.ficha };
      if (data.mediciones) mediciones.value = { ...mediciones.value, ...data.mediciones };
      if (data.estadosComponentes) estadosComponentes.value = { ...estadosComponentes.value, ...data.estadosComponentes };
      if (data.hallazgos) hallazgos.value = { ...hallazgos.value, ...data.hallazgos };
    }
  } catch (e) {
    console.error('Error al cargar datos de inspección GE:', e);
  }
};

const saveChanges = () => {
  try {
    const dataToSave = {
      ficha: ficha.value,
      mediciones: mediciones.value,
      estadosComponentes: estadosComponentes.value,
      hallazgos: hallazgos.value,
      porcentajeCompletado: Math.round((subsistemasEvaluadosCount.value / totalComponentesCount.value) * 100)
    };
    localStorage.setItem(storageKey.value, JSON.stringify(dataToSave));
    emit('updated', dataToSave);
  } catch (e) {
    console.error('Error al guardar datos de inspección GE:', e);
  }
};

watch(() => props.otId, () => {
  loadSavedData();
}, { immediate: true });

onMounted(() => {
  loadSavedData();
});
</script>

<template>
  <div class="space-y-4">
    <!-- CABECERA DEL PROTOCOLO DE CLIMATIZACIÓN (AA) -->
    <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 shadow-sm space-y-3">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-3 flex-wrap gap-2">
        <div>
          <div class="flex items-center gap-2">
            <span class="p-1.5 rounded-lg bg-sky-500/10 text-sky-600 dark:text-sky-400">
              <IconSnowflake class="w-4 h-4 stroke-[2.5]" />
            </span>
            <h3 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
              Protocolo Oficial de Climatización & Aires AA (Cap. 18.1 Anexo Técnico)
            </h3>
          </div>
          <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5 font-medium">
            Termodinámica (ΔT), presiones de gas refrigerante, control secuencial dual y rutina física.
          </p>
        </div>

        <div class="flex items-center gap-2">
          <span class="text-xs font-mono font-black px-3 py-1 rounded-xl border"
            :class="porcentajeCompletado === 100 
              ? 'bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border-emerald-300 dark:border-emerald-800' 
              : 'bg-sky-50 dark:bg-sky-950/60 text-sky-700 dark:text-sky-300 border-sky-300 dark:border-sky-800'">
            {{ porcentajeCompletado }}% Diligenciado
          </span>
        </div>
      </div>

      <!-- Selector de Unidad en Sitio (Esquema Redundante Dual Telecom: AA-1 / AA-2) -->
      <div class="flex items-center justify-between flex-wrap gap-2 pt-1">
        <div class="flex items-center gap-2">
          <span class="text-xs font-bold text-slate-700 dark:text-slate-300">Unidad en Inspección:</span>
          <div class="inline-flex p-1 bg-slate-100 dark:bg-[#0a0b10] rounded-xl border border-slate-200 dark:border-white/10">
            <button 
              type="button" 
              @click="unidadActiva = 'aa1'"
              class="px-3 py-1 text-xs font-extrabold rounded-lg transition-all"
              :class="unidadActiva === 'aa1' ? 'bg-sky-600 text-white shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'"
            >
              Unidad AA-1 (Líder)
            </button>
            <button 
              type="button" 
              @click="unidadActiva = 'aa2'"
              class="px-3 py-1 text-xs font-extrabold rounded-lg transition-all"
              :class="unidadActiva === 'aa2' ? 'bg-sky-600 text-white shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'"
            >
              Unidad AA-2 (Respaldo)
            </button>
          </div>
        </div>

        <span class="text-[11px] font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
          ✓ Configuración Dual Redundante Activa
        </span>
      </div>

      <!-- Ficha de Datos de Placa de la Unidad Seleccionada -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 pt-1 text-xs">
        <div>
          <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Marca del Equipo</label>
          <select 
            v-model="activeUnidadData.ficha.marca"
            @change="saveState"
            class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl px-2.5 py-1.5 text-xs text-slate-900 dark:text-white font-medium focus:outline-hidden focus:border-sky-500"
          >
            <option value="York">York</option>
            <option value="Carrier">Carrier</option>
            <option value="Trane">Trane</option>
            <option value="Marvair">Marvair (Mochila)</option>
            <option value="LG">LG Inverter</option>
            <option value="Lennox">Lennox</option>
          </select>
        </div>

        <div>
          <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Tipo de Unidad</label>
          <select 
            v-model="activeUnidadData.ficha.tipo"
            @change="saveState"
            class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl px-2.5 py-1.5 text-xs text-slate-900 dark:text-white font-medium focus:outline-hidden focus:border-sky-500"
          >
            <option value="Mini-Split Confort">Mini-Split Confort</option>
            <option value="Mochila Wall-Mount">Mochila Wall-Mount</option>
            <option value="Piso Techo">Piso Techo</option>
            <option value="Paquete Compacto">Paquete Compacto</option>
          </select>
        </div>

        <div>
          <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Capacidad Nominal</label>
          <select 
            v-model="activeUnidadData.ficha.capacidad"
            @change="saveState"
            class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl px-2.5 py-1.5 text-xs text-slate-900 dark:text-white font-medium focus:outline-hidden focus:border-sky-500"
          >
            <option value="18000 BTU (1.5 TR)">18.000 BTU (1.5 TR)</option>
            <option value="24000 BTU (2.0 TR)">24.000 BTU (2.0 TR)</option>
            <option value="36000 BTU (3.0 TR)">36.000 BTU (3.0 TR)</option>
            <option value="60000 BTU (5.0 TR)">60.000 BTU (5.0 TR)</option>
          </select>
        </div>

        <div>
          <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Refrigerante</label>
          <select 
            v-model="activeUnidadData.ficha.refrigerante"
            @change="saveState"
            class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl px-2.5 py-1.5 text-xs text-slate-900 dark:text-white font-medium focus:outline-hidden focus:border-sky-500"
          >
            <option value="R410A">R410A (Ecológico)</option>
            <option value="R22">R22 (Transición)</option>
            <option value="R134a">R134a</option>
          </select>
        </div>
      </div>
    </div>

    <!-- BLOQUE 1: MEDICIONES TERMODINÁMICAS Y DELTA T (ΔT) -->
    <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 shadow-sm space-y-3">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-2.5 flex-wrap gap-2">
        <div>
          <h4 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-sky-500"></span>
            <span>1. Balance Térmico & Salto Térmico (ΔT = T.Retorno - T.Inyección)</span>
          </h4>
          <p class="text-[10px] text-slate-500 dark:text-slate-400 font-medium mt-0.5">
            Criterio Normativo Claro: Salto térmico óptimo entre 10.0°C y 16.0°C bajo carga operativa.
          </p>
        </div>

        <span class="text-[10px] font-mono font-black px-2.5 py-0.5 rounded-lg border border-sky-200 dark:border-sky-900 bg-sky-50 dark:bg-sky-950 text-sky-700 dark:text-sky-300">
          Rango Exigido: 10°C ≤ ΔT ≤ 16°C
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-4 gap-3 text-xs">
        <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-1">
          <label class="block text-[10px] font-bold uppercase text-slate-400">T. Retorno (Sala Telecom)</label>
          <div class="flex items-center gap-1.5">
            <input 
              type="number" 
              step="0.1" 
              v-model="activeUnidadData.termo.tempRetorno"
              @input="saveState"
              placeholder="Ej. 24.5"
              class="w-full bg-white dark:bg-[#121215] border border-slate-300 dark:border-white/20 rounded-lg px-2.5 py-1.5 font-mono font-bold text-xs text-slate-900 dark:text-white focus:outline-hidden focus:border-sky-500"
            />
            <span class="text-slate-400 font-bold font-mono">°C</span>
          </div>
          <span class="text-[9px] text-slate-500 block">Temperatura a la entrada del evaporador</span>
        </div>

        <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-1">
          <label class="block text-[10px] font-bold uppercase text-slate-400">T. Inyección (Salida Difusor)</label>
          <div class="flex items-center gap-1.5">
            <input 
              type="number" 
              step="0.1" 
              v-model="activeUnidadData.termo.tempInyeccion"
              @input="saveState"
              placeholder="Ej. 12.0"
              class="w-full bg-white dark:bg-[#121215] border border-slate-300 dark:border-white/20 rounded-lg px-2.5 py-1.5 font-mono font-bold text-xs text-slate-900 dark:text-white focus:outline-hidden focus:border-sky-500"
            />
            <span class="text-slate-400 font-bold font-mono">°C</span>
          </div>
          <span class="text-[9px] text-slate-500 block">Temperatura a la salida del flujo frío</span>
        </div>

        <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-1">
          <label class="block text-[10px] font-bold uppercase text-slate-400">T. Ambiente Exterior</label>
          <div class="flex items-center gap-1.5">
            <input 
              type="number" 
              step="0.1" 
              v-model="activeUnidadData.termo.tempAmbiente"
              @input="saveState"
              placeholder="Ej. 31.5"
              class="w-full bg-white dark:bg-[#121215] border border-slate-300 dark:border-white/20 rounded-lg px-2.5 py-1.5 font-mono font-bold text-xs text-slate-900 dark:text-white focus:outline-hidden focus:border-sky-500"
            />
            <span class="text-slate-400 font-bold font-mono">°C</span>
          </div>
          <span class="text-[9px] text-slate-500 block">Condición climática externa al sitio</span>
        </div>

        <!-- Cálculo automático de Salto Térmico Delta T -->
        <div class="bg-sky-50/60 dark:bg-sky-950/20 border border-sky-200 dark:border-sky-900/60 rounded-xl p-3 flex flex-col justify-between">
          <span class="text-[10px] font-bold text-sky-800 dark:text-sky-300 uppercase block">Salto Térmico Efectivo (ΔT)</span>
          <div class="font-mono font-black text-xl my-1" :class="deltaTClass">
            {{ deltaTValor !== null ? deltaTValor + ' °C' : '—' }}
          </div>
          <div>
            <span v-if="deltaTValor !== null" class="text-[9px] font-extrabold px-2 py-0.5 rounded-full" :class="deltaTBadgeClass">
              {{ deltaTLabel }}
            </span>
            <span v-else class="text-[10px] text-slate-400">Ingrese retorno e inyección</span>
          </div>
        </div>
      </div>
    </div>

    <!-- BLOQUE 2: PRESIÓN DE REFRIGERANTE & PARÁMETROS ELÉCTRICOS -->
    <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 shadow-sm space-y-3">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-2.5 flex-wrap gap-2">
        <div>
          <h4 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-indigo-500"></span>
            <span>2. Presiones de Circuito & Parámetros Eléctricos</span>
          </h4>
          <p class="text-[10px] text-slate-500 dark:text-slate-400 font-medium mt-0.5">
            Presión de succión/descarga con manómetros y amperaje de compresor vs placa (RLA).
          </p>
        </div>

        <span class="text-[10px] font-mono font-bold text-slate-500">
          Ref: {{ activeUnidadData.ficha.refrigerante }}
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
        <!-- Presión de Succión / Baja -->
        <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-1">
          <div class="flex items-center justify-between">
            <label class="text-[10px] font-bold uppercase text-slate-400">Presión Baja (Succión)</label>
            <span class="text-[9px] font-mono text-slate-500">Normal: 110-135 PSI</span>
          </div>
          <div class="flex items-center gap-1.5">
            <input 
              type="number" 
              v-model="activeUnidadData.presion.succion"
              @input="saveState"
              placeholder="Ej. 120"
              class="w-full bg-white dark:bg-[#121215] border border-slate-300 dark:border-white/20 rounded-lg px-2.5 py-1.5 font-mono font-bold text-xs text-slate-900 dark:text-white focus:outline-hidden focus:border-indigo-500"
            />
            <span class="text-slate-400 font-bold font-mono">PSI</span>
          </div>
          <span class="text-[9px] font-bold block" :class="evaluarPresionSuccion.class">
            {{ evaluarPresionSuccion.text }}
          </span>
        </div>

        <!-- Presión de Descarga / Alta -->
        <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-1">
          <div class="flex items-center justify-between">
            <label class="text-[10px] font-bold uppercase text-slate-400">Presión Alta (Descarga)</label>
            <span class="text-[9px] font-mono text-slate-500">Normal: 320-390 PSI</span>
          </div>
          <div class="flex items-center gap-1.5">
            <input 
              type="number" 
              v-model="activeUnidadData.presion.descarga"
              @input="saveState"
              placeholder="Ej. 345"
              class="w-full bg-white dark:bg-[#121215] border border-slate-300 dark:border-white/20 rounded-lg px-2.5 py-1.5 font-mono font-bold text-xs text-slate-900 dark:text-white focus:outline-hidden focus:border-indigo-500"
            />
            <span class="text-slate-400 font-bold font-mono">PSI</span>
          </div>
          <span class="text-[9px] font-bold block" :class="evaluarPresionDescarga.class">
            {{ evaluarPresionDescarga.text }}
          </span>
        </div>

        <!-- Corriente Compresor (Amperios) -->
        <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-1">
          <div class="flex items-center justify-between">
            <label class="text-[10px] font-bold uppercase text-slate-400">Corriente Compresor</label>
            <span class="text-[9px] font-mono text-slate-500">RLA: {{ activeUnidadData.electrico.rla || 11.5 }}A</span>
          </div>
          <div class="flex items-center gap-1.5">
            <input 
              type="number" 
              step="0.1" 
              v-model="activeUnidadData.electrico.corrienteCompresor"
              @input="saveState"
              placeholder="Ej. 8.4"
              class="w-full bg-white dark:bg-[#121215] border border-slate-300 dark:border-white/20 rounded-lg px-2.5 py-1.5 font-mono font-bold text-xs text-slate-900 dark:text-white focus:outline-hidden focus:border-indigo-500"
            />
            <span class="text-slate-400 font-bold font-mono">A</span>
          </div>
          <span class="text-[9px] text-emerald-600 dark:text-emerald-400 font-bold block">
            Carga {{ ((activeUnidadData.electrico.corrienteCompresor || 8.4) / (activeUnidadData.electrico.rla || 11.5) * 100).toFixed(0) }}% de nominal
          </span>
        </div>

        <!-- Voltaje de Alimentación AC -->
        <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-1">
          <div class="flex items-center justify-between">
            <label class="text-[10px] font-bold uppercase text-slate-400">Tensión de Línea AC</label>
            <span class="text-[9px] font-mono text-slate-500">208-230 VAC</span>
          </div>
          <div class="flex items-center gap-1.5">
            <input 
              type="number" 
              v-model="activeUnidadData.electrico.voltajeAc"
              @input="saveState"
              placeholder="Ej. 222"
              class="w-full bg-white dark:bg-[#121215] border border-slate-300 dark:border-white/20 rounded-lg px-2.5 py-1.5 font-mono font-bold text-xs text-slate-900 dark:text-white focus:outline-hidden focus:border-indigo-500"
            />
            <span class="text-slate-400 font-bold font-mono">VAC</span>
          </div>
          <span class="text-[9px] text-slate-500 block">Estabilidad ± 5% conforme</span>
        </div>
      </div>
    </div>

    <!-- BLOQUE 3: CONTROL SECUENCIAL DUAL & ALTERNANCIA TELECOM -->
    <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 shadow-sm space-y-3">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-2.5 flex-wrap gap-2">
        <div>
          <h4 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span>3. Control Secuencial, Termostato & Rotación Dual</span>
          </h4>
          <p class="text-[10px] text-slate-500 dark:text-slate-400 font-medium mt-0.5">
            Verificación obligatoria de alternancia horaria (12h/12h o 24h/24h) y respuesta tras falla AC.
          </p>
        </div>

        <span class="text-[10px] font-black px-2.5 py-0.5 rounded-lg bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
          Redundancia 1+1 Activa
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
        <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 flex items-center justify-between">
          <div>
            <span class="text-[10px] font-bold text-slate-400 uppercase block">Temperatura de Consigna</span>
            <span class="font-mono font-black text-sm text-slate-900 dark:text-white">
              {{ activeUnidadData.control.setpoint || 23.0 }} °C
            </span>
            <span class="text-[9px] text-slate-500 block">Rango estándar Claro: 22°C - 24°C</span>
          </div>
          <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
            CONFORME
          </span>
        </div>

        <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 flex items-center justify-between">
          <div>
            <span class="text-[10px] font-bold text-slate-400 uppercase block">Prueba de Rotación Forzada</span>
            <span class="font-bold text-xs text-slate-900 dark:text-white block mt-0.5">
              {{ activeUnidadData.control.rotacionForzada ? 'Conmutación Exitosa' : 'Pendiente' }}
            </span>
            <span class="text-[9px] text-slate-500 block">Transferencia de carga a unidad hermana</span>
          </div>
          <button 
            type="button"
            @click="toggleRotacion"
            class="px-2.5 py-1 text-[10px] font-extrabold rounded-lg border transition-all"
            :class="activeUnidadData.control.rotacionForzada 
              ? 'bg-emerald-500 border-emerald-500 text-white' 
              : 'bg-white dark:bg-[#121215] border-slate-300 text-slate-600'"
          >
            {{ activeUnidadData.control.rotacionForzada ? 'PROBADO ✓' : 'PROBAR' }}
          </button>
        </div>

        <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 flex items-center justify-between">
          <div>
            <span class="text-[10px] font-bold text-slate-400 uppercase block">Auto-Reinicio Post Corte AC</span>
            <span class="font-bold text-xs text-slate-900 dark:text-white block mt-0.5">
              {{ activeUnidadData.control.reinicioAuto ? 'Función Activa' : 'No Responde' }}
            </span>
            <span class="text-[9px] text-slate-500 block">Arranque sin intervención manual</span>
          </div>
          <button 
            type="button"
            @click="toggleReinicio"
            class="px-2.5 py-1 text-[10px] font-extrabold rounded-lg border transition-all"
            :class="activeUnidadData.control.reinicioAuto 
              ? 'bg-emerald-500 border-emerald-500 text-white' 
              : 'bg-white dark:bg-[#121215] border-slate-300 text-slate-600'"
          >
            {{ activeUnidadData.control.reinicioAuto ? 'ACTIVO ✓' : 'INACTIVO' }}
          </button>
        </div>
      </div>
    </div>

    <!-- BLOQUE 4: RUTINA TÉCNICA FÍSICA Y LIMPIEZA QUÍMICA (ANEXO TÉCNICO) -->
    <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 shadow-sm space-y-3">
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-2.5 flex-wrap gap-2">
        <div>
          <h4 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-purple-500"></span>
            <span>4. Rutina Física, Limpieza Química & Componentes</span>
          </h4>
          <p class="text-[10px] text-slate-500 dark:text-slate-400 font-medium mt-0.5">
            Inspección de serpentines con desengrasante Foaming, turbinas, drenajes y conexiones.
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
          v-for="(task, idx) in activeUnidadData.rutina" 
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
import { IconSnowflake } from '@tabler/icons-vue';

const props = defineProps({
  otId: {
    type: [Number, String],
    default: null,
  },
});

const emit = defineEmits(['updated']);

const STORAGE_KEY = computed(() => `smu_aa_inspection_ot_${props.otId || 'draft'}`);

const unidadActiva = ref('aa1');

// MODELO DUAL OFICIAL DE CLIMATIZACIÓN (AA-1 Y AA-2)
const data = ref({
  aa1: {
    ficha: {
      marca: 'York',
      tipo: 'Mini-Split Confort',
      capacidad: '24000 BTU (2.0 TR)',
      refrigerante: 'R410A',
    },
    termo: {
      tempRetorno: '24.2',
      tempInyeccion: '12.4',
      tempAmbiente: '31.5',
    },
    presion: {
      succion: '122',
      descarga: '348',
    },
    electrico: {
      rla: 11.5,
      corrienteCompresor: '8.6',
      voltajeAc: '222',
    },
    control: {
      setpoint: '23.0',
      rotacionForzada: true,
      reinicioAuto: true,
    },
    rutina: [
      { id: 1, nombre: 'Serpentín Evaporador', detalle: 'Limpieza química con agua y limpiador desengrasante Foaming', estado: 'BUENO' },
      { id: 2, nombre: 'Serpentín Condensador', detalle: 'Desincrustación y lavado a presión de aletas exteriores', estado: 'BUENO' },
      { id: 3, nombre: 'Bandeja y Drenaje de Condensados', detalle: 'Evacuación libre hacia el exterior de sala sin estancamiento', estado: 'BUENO' },
      { id: 4, nombre: 'Filtros de Aire Evaporadora', detalle: 'Lavado o reemplazo de mallas de filtrado de polvo', estado: 'BUENO' },
      { id: 5, nombre: 'Motores y Blowers de Turbina', detalle: 'Revisión de bujes, rodamientos, balanceo y ruidos anómalos', estado: 'BUENO' },
      { id: 6, nombre: 'Válvulas y Gusanillos de Carga', detalle: 'Inspección de fugas de refrigerante y aceite en puertos', estado: 'BUENO' },
      { id: 7, nombre: 'Aislamiento Térmico Tuberías', detalle: 'Aislamiento Armaflex en línea de succión sin roturas', estado: 'BUENO' },
      { id: 8, nombre: 'Contactor y Protecciones Eléctricas', detalle: 'Revisión de platinos de contactor y torque en bornes', estado: 'BUENO' },
    ],
  },
  aa2: {
    ficha: {
      marca: 'York',
      tipo: 'Mini-Split Confort',
      capacidad: '24000 BTU (2.0 TR)',
      refrigerante: 'R410A',
    },
    termo: {
      tempRetorno: '24.0',
      tempInyeccion: '12.8',
      tempAmbiente: '31.5',
    },
    presion: {
      succion: '120',
      descarga: '340',
    },
    electrico: {
      rla: 11.5,
      corrienteCompresor: '8.4',
      voltajeAc: '222',
    },
    control: {
      setpoint: '23.0',
      rotacionForzada: true,
      reinicioAuto: true,
    },
    rutina: [
      { id: 1, nombre: 'Serpentín Evaporador', detalle: 'Limpieza química con agua y limpiador desengrasante Foaming', estado: 'BUENO' },
      { id: 2, nombre: 'Serpentín Condensador', detalle: 'Desincrustación y lavado a presión de aletas exteriores', estado: 'BUENO' },
      { id: 3, nombre: 'Bandeja y Drenaje de Condensados', detalle: 'Evacuación libre hacia el exterior de sala sin estancamiento', estado: 'BUENO' },
      { id: 4, nombre: 'Filtros de Aire Evaporadora', detalle: 'Lavado o reemplazo de mallas de filtrado de polvo', estado: 'BUENO' },
      { id: 5, nombre: 'Motores y Blowers de Turbina', detalle: 'Revisión de bujes, rodamientos, balanceo y ruidos anómalos', estado: 'BUENO' },
      { id: 6, nombre: 'Válvulas y Gusanillos de Carga', detalle: 'Inspección de fugas de refrigerante y aceite en puertos', estado: 'BUENO' },
      { id: 7, nombre: 'Aislamiento Térmico Tuberías', detalle: 'Aislamiento Armaflex en línea de succión sin roturas', estado: 'BUENO' },
      { id: 8, nombre: 'Contactor y Protecciones Eléctricas', detalle: 'Revisión de platinos de contactor y torque en bornes', estado: 'BUENO' },
    ],
  },
});

const activeUnidadData = computed(() => {
  return data.value[unidadActiva.value] || data.value.aa1;
});

// CALCULOS TERMICOS
const deltaTValor = computed(() => {
  const ret = parseFloat(activeUnidadData.value.termo.tempRetorno);
  const iny = parseFloat(activeUnidadData.value.termo.tempInyeccion);
  if (!isNaN(ret) && !isNaN(iny)) {
    return parseFloat((ret - iny).toFixed(1));
  }
  return null;
});

const deltaTClass = computed(() => {
  if (deltaTValor.value === null) return 'text-slate-400';
  if (deltaTValor.value >= 10.0 && deltaTValor.value <= 16.0) return 'text-emerald-600 dark:text-emerald-400';
  if (deltaTValor.value < 10.0) return 'text-amber-600 dark:text-amber-400';
  return 'text-rose-600 dark:text-rose-400';
});

const deltaTBadgeClass = computed(() => {
  if (deltaTValor.value === null) return 'bg-slate-100 text-slate-500';
  if (deltaTValor.value >= 10.0 && deltaTValor.value <= 16.0) {
    return 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300';
  }
  if (deltaTValor.value < 10.0) {
    return 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300';
  }
  return 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300';
});

const deltaTLabel = computed(() => {
  if (deltaTValor.value === null) return '';
  if (deltaTValor.value >= 10.0 && deltaTValor.value <= 16.0) return 'ÓPTIMO (10°C - 16°C)';
  if (deltaTValor.value < 10.0) return 'BAJO SALTO (Revisar Gas/Filtros)';
  return 'SALTO ELEVADO (Flujo Restringido)';
});

// EVALUACION DE PRESIONES
const evaluarPresionSuccion = computed(() => {
  const p = parseFloat(activeUnidadData.value.presion.succion);
  if (isNaN(p)) return { text: 'Pendiente medición', class: 'text-slate-400' };
  if (p >= 110 && p <= 135) return { text: '✓ Presión de baja óptima', class: 'text-emerald-600 dark:text-emerald-400' };
  if (p < 110) return { text: '⚠ Fuga o falta de refrigerante', class: 'text-amber-600 dark:text-amber-400' };
  return { text: '⚠ Sobrepresión en succión', class: 'text-rose-600 dark:text-rose-400' };
});

const evaluarPresionDescarga = computed(() => {
  const p = parseFloat(activeUnidadData.value.presion.descarga);
  if (isNaN(p)) return { text: 'Pendiente medición', class: 'text-slate-400' };
  if (p >= 320 && p <= 390) return { text: '✓ Presión de alta óptima', class: 'text-emerald-600 dark:text-emerald-400' };
  if (p > 390) return { text: '⚠ Condensador sucio o sobrecarga', class: 'text-rose-600 dark:text-rose-400' };
  return { text: 'Presión baja', class: 'text-slate-500' };
});

// CONTROL
const toggleRotacion = () => {
  activeUnidadData.value.control.rotacionForzada = !activeUnidadData.value.control.rotacionForzada;
  saveState();
};

const toggleReinicio = () => {
  activeUnidadData.value.control.reinicioAuto = !activeUnidadData.value.control.reinicioAuto;
  saveState();
};

const setTaskEstado = (idx, st) => {
  activeUnidadData.value.rutina[idx].estado = st;
  saveState();
};

// PORCENTAJE DE DILIGENCIAMIENTO
const porcentajeCompletado = computed(() => {
  // Evaluamos ambas unidades (AA-1 y AA-2)
  let totalItems = 2 * (3 + 2 + 2 + 8); // 3 termo, 2 presion, 2 control, 8 rutina por unidad
  let respondidos = 0;

  ['aa1', 'aa2'].forEach(uKey => {
    const u = data.value[uKey];
    if (u.termo.tempRetorno) respondidos++;
    if (u.termo.tempInyeccion) respondidos++;
    if (u.termo.tempAmbiente) respondidos++;
    if (u.presion.succion) respondidos++;
    if (u.presion.descarga) respondidos++;
    if (u.control.rotacionForzada !== undefined) respondidos++;
    if (u.control.reinicioAuto !== undefined) respondidos++;
    respondidos += u.rutina.filter(r => r.estado).length;
  });

  return Math.min(100, Math.round((respondidos / totalItems) * 100));
});

// PERSISTENCIA LOCALSTORAGE
const saveState = () => {
  try {
    localStorage.setItem(STORAGE_KEY.value, JSON.stringify(data.value));
  } catch (e) {
    console.error('Error guardando AA en localStorage:', e);
  }
  emit('updated', {
    porcentajeCompletado: porcentajeCompletado.value,
    deltaT: deltaTValor.value,
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
    console.error('Error cargando AA de localStorage:', e);
  }
  emit('updated', {
    porcentajeCompletado: porcentajeCompletado.value,
    deltaT: deltaTValor.value,
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

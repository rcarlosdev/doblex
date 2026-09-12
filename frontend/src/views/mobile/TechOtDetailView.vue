<template>
  <div class="space-y-4 max-w-4xl mx-auto pb-24 select-none transition-colors duration-300">
    <!-- Header de Detalle -->
    <div class="flex items-center justify-between border-b border-slate-200 dark:border-white/10 pb-3">
      <div class="flex items-center gap-3">
        <button 
          @click="$router.push('/mobile/dashboard')" 
          class="p-2 bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-white/5 active:scale-95 transition-all shadow-sm"
        >
          <IconArrowLeft class="w-5 h-5 stroke-[2]" />
        </button>
        <div v-if="ot">
          <div class="flex items-center gap-2 flex-wrap">
            <span class="font-mono text-sm font-extrabold text-red-600 dark:text-red-400">{{ ot.codigo }}</span>
            <span v-if="ot.id_actividad" class="font-mono text-[10px] bg-slate-100 dark:bg-white/10 border border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300 font-bold px-1.5 py-0.5 rounded">
              {{ ot.id_actividad }}
            </span>
            <span :class="estadoBadgeClass(ot.estado)" class="px-2 py-0.5 rounded text-[10px] font-extrabold uppercase">
              {{ formatEstado(ot.estado) }}
            </span>
          </div>
          <p class="text-xs text-slate-500 dark:text-slate-400 font-medium truncate max-w-[200px] sm:max-w-xs">{{ ot.descripcion }}</p>
        </div>
      </div>
      <button 
        @click="fetchOtDetail" 
        class="p-2 bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl text-slate-700 dark:text-slate-300 hover:text-red-600 dark:hover:text-red-400 active:scale-95 transition-all shadow-sm"
      >
        <IconRefresh class="w-5 h-5 stroke-[2]" :class="{ 'animate-spin': loading }" />
      </button>
    </div>

    <!-- Indicador de Carga -->
    <div v-if="loading" class="text-center py-12 text-slate-500 dark:text-slate-400 text-sm flex flex-col items-center gap-2">
      <IconRefresh class="w-6 h-6 animate-spin text-red-600" />
      <span>Cargando detalle de la OT...</span>
    </div>

    <div v-else-if="ot" class="space-y-4">
      
      <!-- Navegación por Pestañas Segmentadas Móviles (5 Pestañas) -->
      <div class="bg-slate-200/80 dark:bg-[#121215] p-1 rounded-2xl border border-slate-200/80 dark:border-white/10 select-none">
        <div class="grid grid-cols-5 gap-1 text-center">
          <button
            v-for="t in tabs"
            :key="t.id"
            @click="activeTab = t.id"
            class="flex flex-col items-center justify-center py-2 px-1 rounded-xl text-xs font-bold transition-all duration-200"
            :class="activeTab === t.id 
              ? 'bg-red-600 text-white shadow-md shadow-red-600/20' 
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-white/40 dark:hover:bg-white/5'"
          >
            <component :is="t.icon" class="w-4 h-4 stroke-[2.2] mb-0.5" />
            <span class="truncate text-[10px] sm:text-xs font-extrabold">{{ t.shortLabel }}</span>
          </button>
        </div>
      </div>

      <!-- CONTENIDO PESTAÑA 1: FLUJO Y ACCIÓN -->
      <div v-if="activeTab === 'flujo'" class="space-y-4">

        <!-- 1. STEPPER VISUAL DE FASES OPERATIVAS -->
        <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 shadow-xs space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider flex items-center gap-1.5">
              <IconSteeringWheel class="w-4 h-4 text-red-600 dark:text-red-400 stroke-[2.2]" />
              <span>Etapas del Ciclo Operativo</span>
            </h3>
            <span :class="estadoBadgeClass(ot.estado)" class="px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-wider">
              {{ formatEstado(ot.estado) }}
            </span>
          </div>

          <!-- Stepper horizontal con conectores -->
          <div class="grid grid-cols-5 gap-1 pt-1 select-none">
            <div 
              v-for="(step, idx) in etapasFlujo" 
              :key="step.key"
              class="flex flex-col items-center text-center space-y-1 relative"
            >
              <!-- Línea conectora entre nodos -->
              <div 
                v-if="idx > 0" 
                class="absolute -left-1/2 top-3 w-full h-0.5 -z-0"
                :class="getEtapaIndex(ot.estado) >= idx 
                  ? 'bg-emerald-500 dark:bg-emerald-600' 
                  : 'bg-slate-200 dark:bg-white/10'"
              ></div>

              <!-- Nodo de estado -->
              <div 
                class="w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-mono font-black z-10 transition-all"
                :class="getEtapaIndex(ot.estado) > idx
                  ? 'bg-emerald-600 text-white shadow-xs'
                  : getEtapaIndex(ot.estado) === idx
                    ? ot.estado === 'detenida_materiales'
                      ? 'bg-amber-500 text-white ring-4 ring-amber-500/20 animate-pulse'
                      : ['solucionada', 'finalizada'].includes(ot.estado)
                        ? 'bg-emerald-600 text-white ring-4 ring-emerald-500/20'
                        : 'bg-red-600 text-white ring-4 ring-red-500/20 animate-pulse'
                    : 'bg-slate-100 dark:bg-[#0a0b10] border border-slate-300 dark:border-white/15 text-slate-400 dark:text-slate-600'"
              >
                <IconCheck v-if="getEtapaIndex(ot.estado) > idx || (idx === 4 && ['solucionada', 'finalizada'].includes(ot.estado))" class="w-3.5 h-3.5 stroke-[3]" />
                <span v-else>{{ idx + 1 }}</span>
              </div>

              <!-- Texto de la fase -->
              <div class="space-y-0.5">
                <span 
                  class="text-[10px] font-bold block truncate max-w-full"
                  :class="getEtapaIndex(ot.estado) === idx ? 'text-red-600 dark:text-red-400 font-black' : 'text-slate-600 dark:text-slate-400'"
                >
                  {{ step.label }}
                </span>
                <span class="text-[8px] text-slate-400 dark:text-slate-500 hidden sm:block">
                  {{ step.desc }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 2. FICHA TÉCNICA DEL SITIO & DETALLES DEL REQUERIMIENTO -->
        <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-4 shadow-xs">
          <!-- Cabecera de Sitio y SLA -->
          <div class="flex flex-wrap items-start justify-between gap-2 border-b border-slate-100 dark:border-white/10 pb-3">
            <div class="space-y-1 min-w-0 flex-1">
              <div class="flex items-center gap-2 flex-wrap">
                <div class="p-1 rounded-lg bg-red-500/10 text-red-600 dark:text-red-400">
                  <IconBuildingBroadcastTower class="w-4 h-4 stroke-[2.2]" />
                </div>
                <h2 class="text-sm sm:text-base font-black text-slate-900 dark:text-white truncate">
                  {{ ot.sitio || 'Estación / Sitio Telecom' }}
                </h2>
                <span :class="tipoMantenimientoBadgeClass(ot.tipo_mantenimiento)" class="px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-wider">
                  {{ tipoMantenimientoLabel(ot.tipo_mantenimiento) }}
                </span>
              </div>

              <!-- Ubicación con botón directo para abrir Google Maps / Waze -->
              <div class="flex items-center gap-2 text-xs text-slate-600 dark:text-slate-300 pt-0.5">
                <IconMapPin class="w-4 h-4 text-slate-400 shrink-0 stroke-[2]" />
                <span class="truncate font-medium">{{ ot.ubicacion }}</span>
                <button
                  type="button"
                  @click="abrirUbicacionMaps"
                  class="inline-flex items-center gap-1 text-[11px] font-bold text-red-600 dark:text-red-400 hover:text-red-500 dark:hover:text-red-300 hover:underline shrink-0 ml-1"
                  title="Abrir coordenadas en Google Maps"
                >
                  <IconNavigation class="w-3.5 h-3.5 stroke-[2.2]" />
                  <span>Navegar GPS</span>
                  <IconExternalLink class="w-3 h-3 stroke-[2]" />
                </button>
              </div>
            </div>

            <!-- SLA Dinámico -->
            <div v-if="ot.fecha_limite_sla" class="shrink-0">
              <SlaBadge :fecha-limite="ot.fecha_limite_sla" :estado="ot.estado" />
            </div>
          </div>

          <!-- Grid de Especificaciones Clave -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-xs">
            <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200/80 dark:border-white/10 rounded-xl p-2.5 space-y-0.5">
              <span class="text-[10px] text-slate-400 dark:text-slate-500 font-bold uppercase tracking-wider">Actividad & Tipo</span>
              <div class="font-bold text-slate-800 dark:text-slate-200 truncate">
                {{ ot.tipo_actividad ? ot.tipo_actividad.toUpperCase() : (ot.tipo_mantenimiento || 'Preventivo').toUpperCase() }}
              </div>
            </div>

            <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200/80 dark:border-white/10 rounded-xl p-2.5 space-y-0.5">
              <span class="text-[10px] text-slate-400 dark:text-slate-500 font-bold uppercase tracking-wider">Prioridad & Zona</span>
              <div class="font-mono font-black text-slate-900 dark:text-white flex items-center gap-1">
                <span class="w-2 h-2 rounded-full" :class="ot.prioridad === 'P1' ? 'bg-red-600' : ot.prioridad === 'P2' ? 'bg-amber-500' : 'bg-blue-500'"></span>
                <span>{{ ot.prioridad || 'P2' }} ({{ (ot.categoria || ot.tipo_ubicacion || 'normal').toUpperCase() }})</span>
              </div>
            </div>

            <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200/80 dark:border-white/10 rounded-xl p-2.5 space-y-0.5">
              <span class="text-[10px] text-slate-400 dark:text-slate-500 font-bold uppercase tracking-wider">Estación & Owner</span>
              <div class="font-bold text-slate-800 dark:text-slate-200 truncate">
                {{ ot.tipo_estacion || 'MOVIL' }} • {{ ot.site_owner || 'CLARO' }}
              </div>
            </div>

            <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200/80 dark:border-white/10 rounded-xl p-2.5 space-y-0.5">
              <span class="text-[10px] text-slate-400 dark:text-slate-500 font-bold uppercase tracking-wider">Coordinador / Regional</span>
              <div class="font-bold text-slate-800 dark:text-slate-200 truncate">
                {{ ot.coordinador || 'Sin coord.' }} ({{ ot.regional || 'R1' }})
              </div>
            </div>
          </div>

          <!-- Descripción del requerimiento técnico -->
          <div class="space-y-1">
            <span class="text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
              Diagnóstico Inicial / Síntoma Reportado:
            </span>
            <p class="text-xs text-slate-800 dark:text-slate-200 bg-slate-50 dark:bg-[#0a0b10] border border-slate-200/80 dark:border-white/10 rounded-xl p-3 leading-relaxed">
              {{ ot.descripcion }}
            </p>
          </div>
        </div>

        <!-- 3. ACCIONES OPERATIVAS Y TRANSICIÓN DE ESTADO -->
        <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 sm:p-5 space-y-3.5 shadow-xs">
          <h3 class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider flex items-center justify-between">
            <span>Acción Operativa Requerida</span>
            <span class="text-[10px] text-slate-400 dark:text-slate-500 font-medium">Control de Flujo</span>
          </h3>

          <!-- Si está Asignada: Iniciar Desplazamiento -->
          <div v-if="ot.estado === 'asignada'" class="space-y-2">
            <div class="p-3 bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-900/40 rounded-xl text-xs text-red-800 dark:text-red-300">
              La orden está asignada a su cuadrilla. Inicie su desplazamiento hacia el sitio cuando emprenda la ruta.
            </div>
            <button
              @click="pedirConfirmacionDesplazamiento"
              :disabled="updating"
              class="w-full bg-red-600 hover:bg-red-500 text-white font-black py-3.5 rounded-xl text-xs shadow-lg shadow-red-600/20 active:scale-98 transition-all flex items-center justify-center gap-2 cursor-pointer"
            >
              <IconCar class="w-5 h-5 stroke-[2]" />
              <span>Iniciar Desplazamiento (En Camino)</span>
            </button>
          </div>

          <!-- Si está En Camino: Marcar Llegada a Sitio -->
          <div v-else-if="ot.estado === 'en_camino'" class="space-y-2">
            <div class="p-3 bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/40 rounded-xl text-xs text-amber-800 dark:text-amber-300">
              Usted se encuentra en ruta hacia la estación. Al arribar a la torre o central, registre su llegada.
            </div>
            <button
              @click="pedirConfirmacionLlegada"
              :disabled="updating"
              class="w-full bg-amber-600 hover:bg-amber-500 text-white font-black py-3.5 rounded-xl text-xs shadow-lg shadow-amber-600/20 active:scale-98 transition-all flex items-center justify-center gap-2 cursor-pointer"
            >
              <IconMapPinCheck class="w-5 h-5 stroke-[2]" />
              <span>Marcar Llegada a Sitio (GPS & Timestamp)</span>
            </button>
          </div>

          <!-- Si está En Sitio: Iniciar Intervención Técnica -->
          <div v-else-if="ot.estado === 'en_sitio'" class="space-y-2">
            <div class="p-3 bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-900/40 rounded-xl text-xs text-blue-800 dark:text-blue-300">
              Llegada a sitio registrada con éxito. Dé inicio a la intervención técnica para habilitar los reportes de campo.
            </div>
            <button
              @click="pedirConfirmacionIniciarTrabajos"
              :disabled="updating"
              class="w-full bg-red-600 hover:bg-red-500 text-white font-black py-3.5 rounded-xl text-xs shadow-lg shadow-red-600/20 active:scale-98 transition-all flex items-center justify-center gap-2 cursor-pointer"
            >
              <IconPlayerPlay class="w-5 h-5 stroke-[2]" />
              <span>Iniciar Ejecución Técnica (En Progreso)</span>
            </button>
          </div>

          <!-- Si está Detenida por Materiales: Reanudar -->
          <div v-else-if="ot.estado === 'detenida_materiales'" class="space-y-2">
            <div class="p-3 bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/40 rounded-xl text-xs text-amber-800 dark:text-amber-300 flex items-center gap-2">
              <IconAlertTriangle class="w-4 h-4 shrink-0 text-amber-600" />
              <span>Intervención pausada temporalmente por espera de insumos o materiales.</span>
            </div>
            <button
              @click="pedirConfirmacionReanudar"
              :disabled="updating"
              class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-black py-3.5 rounded-xl text-xs shadow-lg active:scale-98 transition-all flex items-center justify-center gap-2 cursor-pointer"
            >
              <IconPlayerPlay class="w-5 h-5 stroke-[2]" />
              <span>Reanudar Intervención Técnica (En Progreso)</span>
            </button>
          </div>

          <!-- Opciones secundarias si está En Progreso (Ej: Pausar por Materiales) -->
          <div v-if="ot.estado === 'en_progreso'" class="flex justify-end pt-1">
            <button
              type="button"
              @click="pedirConfirmacionPausarMateriales"
              :disabled="updating"
              class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold text-amber-700 dark:text-amber-300 bg-amber-50 dark:bg-amber-950/40 hover:bg-amber-100 border border-amber-200 dark:border-amber-900/40 transition-all active:scale-95"
            >
              <IconPlayerPause class="w-3.5 h-3.5 stroke-[2]" />
              <span>Pausar por Falta de Materiales</span>
            </button>
          </div>

          <!-- 4. MATRIZ DE REQUISITOS OBLIGATORIOS PARA EL CIERRE TÉCNICO -->
          <div v-if="['en_sitio', 'en_progreso', 'detenida_materiales'].includes(ot.estado)" class="pt-2 space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-[11px] font-black text-slate-700 dark:text-slate-300 uppercase tracking-wider">
                Matriz de Requisitos para Cierre Técnico
              </span>
              <span 
                class="text-[10px] font-mono font-black px-2 py-0.5 rounded-md"
                :class="canCloseOt 
                  ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400' 
                  : 'bg-amber-500/10 text-amber-600 dark:text-amber-400'"
              >
                {{ canCloseOt ? '100% Completo' : `${requisitosFaltantes.length} pendientes` }}
              </span>
            </div>

            <!-- Grid de tarjetas de requisitos según Tipo de Trabajo -->
            <!-- 0. REGLAS TRANSVERSALES OBLIGATORIAS (TODOS LOS TIPOS DE TRABAJO) -->
            <div class="space-y-1.5 pb-2">
              <span class="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider block">
                Reglas Transversales Obligatorias
              </span>
              <div class="grid grid-cols-2 sm:grid-cols-5 gap-2">
                <!-- 1. Llegada Sitio (Carnet y Estación) -->
                <div 
                  class="border rounded-xl p-3 space-y-1 transition-all"
                  :class="tieneLlegadaOk
                    ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-800 dark:text-emerald-300' 
                    : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300'"
                >
                  <div class="flex items-center justify-between text-xs">
                    <span class="font-bold text-[11px]">Llegada Sitio</span>
                    <IconCircleCheck v-if="tieneLlegadaOk" class="w-4 h-4 text-emerald-600 dark:text-emerald-400 stroke-[2.5]" />
                    <IconCircleX v-else class="w-4 h-4 text-rose-500 stroke-[2]" />
                  </div>
                  <div class="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                    {{ tieneLlegadaOk ? 'Técnico + Carnet + Sitio OK' : 'Pendiente foto' }}
                  </div>
                  <button 
                    v-if="!tieneLlegadaOk" 
                    @click="isLlegadaModalOpen = true"
                    class="text-[10px] text-amber-600 dark:text-amber-400 font-extrabold hover:underline block pt-0.5"
                  >
                    + Registrar Llegada
                  </button>
                </div>

                <!-- 2. Transporte Especial LPU -->
                <div 
                  class="border rounded-xl p-3 space-y-1 transition-all"
                  :class="tieneTransporteOk
                    ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-800 dark:text-emerald-300' 
                    : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300'"
                >
                  <div class="flex items-center justify-between text-xs">
                    <span class="font-bold text-[11px]">Transporte LPU</span>
                    <IconCircleCheck v-if="tieneTransporteOk" class="w-4 h-4 text-emerald-600 dark:text-emerald-400 stroke-[2.5]" />
                    <IconCircleX v-else class="w-4 h-4 text-rose-500 stroke-[2]" />
                  </div>
                  <div class="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                    {{ tieneTransporteOk ? 'Con foto soporte' : 'Obligatorio' }}
                  </div>
                  <button 
                    v-if="!tieneTransporteOk" 
                    @click="activeTab = 'checklist'"
                    class="text-[10px] text-amber-600 dark:text-amber-400 font-extrabold hover:underline block pt-0.5"
                  >
                    + Registrar LPU
                  </button>
                </div>

                <!-- 3. Insumos Menores (Antes & Después) -->
                <div 
                  class="border rounded-xl p-3 space-y-1 transition-all"
                  :class="tieneInsumosOk
                    ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-800 dark:text-emerald-300' 
                    : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300'"
                >
                  <div class="flex items-center justify-between text-xs">
                    <span class="font-bold text-[11px]">Insumos Menores</span>
                    <IconCircleCheck v-if="tieneInsumosOk" class="w-4 h-4 text-emerald-600 dark:text-emerald-400 stroke-[2.5]" />
                    <IconCircleX v-else class="w-4 h-4 text-rose-500 stroke-[2]" />
                  </div>
                  <div class="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                    {{ tieneInsumosOk ? 'Antes & Después OK' : 'Faltan fotos' }}
                  </div>
                  <button 
                    v-if="!tieneInsumosOk" 
                    @click="activeTab = 'repuestos'"
                    class="text-[10px] text-amber-600 dark:text-amber-400 font-extrabold hover:underline block pt-0.5"
                  >
                    + Ver Insumos
                  </button>
                </div>

                <!-- 4. Repuestos Cambiados -->
                <div 
                  class="border rounded-xl p-3 space-y-1 transition-all"
                  :class="tieneRepuestosOk
                    ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-800 dark:text-emerald-300' 
                    : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300'"
                >
                  <div class="flex items-center justify-between text-xs">
                    <span class="font-bold text-[11px]">Repuestos Ret./Inst.</span>
                    <IconCircleCheck v-if="tieneRepuestosOk" class="w-4 h-4 text-emerald-600 dark:text-emerald-400 stroke-[2.5]" />
                    <IconCircleX v-else class="w-4 h-4 text-rose-500 stroke-[2]" />
                  </div>
                  <div class="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                    {{ tieneRepuestosOk ? 'Fotos completas' : 'Faltan fotos' }}
                  </div>
                  <button 
                    v-if="!tieneRepuestosOk" 
                    @click="activeTab = 'repuestos'"
                    class="text-[10px] text-amber-600 dark:text-amber-400 font-extrabold hover:underline block pt-0.5"
                  >
                    + Ver Repuestos
                  </button>
                </div>

                <!-- 5. Novedades y Hallazgos -->
                <div 
                  class="border rounded-xl p-3 space-y-1 transition-all"
                  :class="tieneHallazgosOk
                    ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-800 dark:text-emerald-300' 
                    : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300'"
                >
                  <div class="flex items-center justify-between text-xs">
                    <span class="font-bold text-[11px]">Hallazgos Estación</span>
                    <IconCircleCheck v-if="tieneHallazgosOk" class="w-4 h-4 text-emerald-600 dark:text-emerald-400 stroke-[2.5]" />
                    <IconCircleX v-else class="w-4 h-4 text-rose-500 stroke-[2]" />
                  </div>
                  <div class="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                    {{ tieneHallazgosOk ? 'Fotos completas' : 'Falta foto soporte' }}
                  </div>
                  <button 
                    v-if="!tieneHallazgosOk" 
                    @click="activeTab = 'checklist'"
                    class="text-[10px] text-amber-600 dark:text-amber-400 font-extrabold hover:underline block pt-0.5"
                  >
                    + Ver Hallazgos
                  </button>
                </div>
              </div>
            </div>

            <!-- Separador / Título de Requisitos Específicos -->
            <span class="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider block">
              Requisitos Específicos del Tipo de Mantenimiento
            </span>

            <!-- 1. CASO WO: CORRECTIVO Y EMERGENCIA -->
            <div v-if="isCorrectivo" class="grid grid-cols-2 sm:grid-cols-4 gap-2">
              <!-- Requisito Foto Antes -->
              <div 
                class="border rounded-xl p-3 space-y-1 transition-all"
                :class="countEvidencias('antes') >= 1 
                  ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-800 dark:text-emerald-300' 
                  : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300'"
              >
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-[11px]">Foto ANTES</span>
                  <IconCircleCheck v-if="countEvidencias('antes') >= 1" class="w-4 h-4 text-emerald-600 dark:text-emerald-400 stroke-[2.5]" />
                  <IconCircleX v-else class="w-4 h-4 text-rose-500 stroke-[2]" />
                </div>
                <div class="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                  {{ countEvidencias('antes') }} cargada(s)
                </div>
                <button 
                  v-if="countEvidencias('antes') < 1" 
                  @click="activeTab = 'evidencias'"
                  class="text-[10px] text-red-600 dark:text-red-400 font-extrabold hover:underline block pt-0.5"
                >
                  + Cargar foto
                </button>
              </div>

              <!-- Requisito Foto Durante -->
              <div 
                class="border rounded-xl p-3 space-y-1 transition-all"
                :class="countEvidencias('durante') >= 1 
                  ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-800 dark:text-emerald-300' 
                  : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300'"
              >
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-[11px]">Foto DURANTE</span>
                  <IconCircleCheck v-if="countEvidencias('durante') >= 1" class="w-4 h-4 text-emerald-600 dark:text-emerald-400 stroke-[2.5]" />
                  <IconCircleX v-else class="w-4 h-4 text-rose-500 stroke-[2]" />
                </div>
                <div class="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                  {{ countEvidencias('durante') }} cargada(s)
                </div>
                <button 
                  v-if="countEvidencias('durante') < 1" 
                  @click="activeTab = 'evidencias'"
                  class="text-[10px] text-red-600 dark:text-red-400 font-extrabold hover:underline block pt-0.5"
                >
                  + Cargar foto
                </button>
              </div>

              <!-- Requisito Foto Después -->
              <div 
                class="border rounded-xl p-3 space-y-1 transition-all"
                :class="countEvidencias('despues') >= 1 
                  ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-800 dark:text-emerald-300' 
                  : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300'"
              >
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-[11px]">Foto DESPUÉS</span>
                  <IconCircleCheck v-if="countEvidencias('despues') >= 1" class="w-4 h-4 text-emerald-600 dark:text-emerald-400 stroke-[2.5]" />
                  <IconCircleX v-else class="w-4 h-4 text-rose-500 stroke-[2]" />
                </div>
                <div class="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                  {{ countEvidencias('despues') }} cargada(s)
                </div>
                <button 
                  v-if="countEvidencias('despues') < 1" 
                  @click="activeTab = 'evidencias'"
                  class="text-[10px] text-red-600 dark:text-red-400 font-extrabold hover:underline block pt-0.5"
                >
                  + Cargar foto
                </button>
              </div>

              <!-- Requisito Bitácora PDT -->
              <div 
                class="border rounded-xl p-3 space-y-1 transition-all"
                :class="(ot.avances && ot.avances.length > 0) 
                  ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-800 dark:text-emerald-300' 
                  : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300'"
              >
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-[11px]">Bitácora PDT</span>
                  <IconCircleCheck v-if="ot.avances && ot.avances.length > 0" class="w-4 h-4 text-emerald-600 dark:text-emerald-400 stroke-[2.5]" />
                  <IconCircleX v-else class="w-4 h-4 text-rose-500 stroke-[2]" />
                </div>
                <div class="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                  {{ ot.avances?.length || 0 }} hito(s)
                </div>
                <button 
                  v-if="!ot.avances || ot.avances.length === 0" 
                  @click="activeTab = 'avances'"
                  class="text-[10px] text-red-600 dark:text-red-400 font-extrabold hover:underline block pt-0.5"
                >
                  + Publicar hito
                </button>
              </div>
            </div>

            <!-- 2. CASO MP PLANTA ELÉCTRICA -->
            <div v-else-if="!isPreventivoAire" class="grid grid-cols-2 sm:grid-cols-5 gap-2">
              <!-- Requisito Placas Técnicas -->
              <div 
                class="border rounded-xl p-3 space-y-1 transition-all"
                :class="(countEvidencias('placas') >= 1 || countEvidencias('antes') >= 1)
                  ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-800 dark:text-emerald-300' 
                  : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300'"
              >
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-[11px]">Placas Técnicas</span>
                  <IconCircleCheck v-if="countEvidencias('placas') >= 1 || countEvidencias('antes') >= 1" class="w-4 h-4 text-emerald-600 dark:text-emerald-400 stroke-[2.5]" />
                  <IconCircleX v-else class="w-4 h-4 text-rose-500 stroke-[2]" />
                </div>
                <div class="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                  {{ countEvidencias('placas') + countEvidencias('antes') }} cargada(s)
                </div>
                <button 
                  v-if="countEvidencias('placas') < 1 && countEvidencias('antes') < 1" 
                  @click="activeTab = 'evidencias'"
                  class="text-[10px] text-red-600 dark:text-red-400 font-extrabold hover:underline block pt-0.5"
                >
                  + Cargar foto
                </button>
              </div>

              <!-- Requisito Horómetro Inicial -->
              <div 
                class="border rounded-xl p-3 space-y-1 transition-all"
                :class="(countEvidencias('inicial') >= 1 || countEvidencias('antes') >= 1)
                  ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-800 dark:text-emerald-300' 
                  : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300'"
              >
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-[11px]">Horómetro Inicial</span>
                  <IconCircleCheck v-if="countEvidencias('inicial') >= 1 || countEvidencias('antes') >= 1" class="w-4 h-4 text-emerald-600 dark:text-emerald-400 stroke-[2.5]" />
                  <IconCircleX v-else class="w-4 h-4 text-rose-500 stroke-[2]" />
                </div>
                <div class="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                  {{ countEvidencias('inicial') }} cargada(s)
                </div>
                <button 
                  v-if="countEvidencias('inicial') < 1 && countEvidencias('antes') < 1" 
                  @click="activeTab = 'evidencias'"
                  class="text-[10px] text-red-600 dark:text-red-400 font-extrabold hover:underline block pt-0.5"
                >
                  + Cargar foto
                </button>
              </div>

              <!-- Requisito Filtración & Mantenimiento -->
              <div 
                class="border rounded-xl p-3 space-y-1 transition-all"
                :class="(countEvidencias('mantenimiento') >= 1 || countEvidencias('durante') >= 1 || countEvidencias('filtracion') >= 1)
                  ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-800 dark:text-emerald-300' 
                  : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300'"
              >
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-[11px]">Filtración & Aceite</span>
                  <IconCircleCheck v-if="countEvidencias('mantenimiento') >= 1 || countEvidencias('durante') >= 1 || countEvidencias('filtracion') >= 1" class="w-4 h-4 text-emerald-600 dark:text-emerald-400 stroke-[2.5]" />
                  <IconCircleX v-else class="w-4 h-4 text-rose-500 stroke-[2]" />
                </div>
                <div class="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                  {{ countEvidencias('mantenimiento') + countEvidencias('durante') + countEvidencias('filtracion') }} cargada(s)
                </div>
                <button 
                  v-if="countEvidencias('mantenimiento') < 1 && countEvidencias('durante') < 1 && countEvidencias('filtracion') < 1" 
                  @click="activeTab = 'evidencias'"
                  class="text-[10px] text-red-600 dark:text-red-400 font-extrabold hover:underline block pt-0.5"
                >
                  + Cargar foto
                </button>
              </div>

              <!-- Requisito Pruebas ATS con Carga -->
              <div 
                class="border rounded-xl p-3 space-y-1 transition-all"
                :class="(countEvidencias('pruebas') >= 1 || countEvidencias('despues') >= 1)
                  ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-800 dark:text-emerald-300' 
                  : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300'"
              >
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-[11px]">Pruebas ATS Carga</span>
                  <IconCircleCheck v-if="countEvidencias('pruebas') >= 1 || countEvidencias('despues') >= 1" class="w-4 h-4 text-emerald-600 dark:text-emerald-400 stroke-[2.5]" />
                  <IconCircleX v-else class="w-4 h-4 text-rose-500 stroke-[2]" />
                </div>
                <div class="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                  {{ countEvidencias('pruebas') + countEvidencias('despues') }} cargada(s)
                </div>
                <button 
                  v-if="countEvidencias('pruebas') < 1 && countEvidencias('despues') < 1" 
                  @click="activeTab = 'evidencias'"
                  class="text-[10px] text-red-600 dark:text-red-400 font-extrabold hover:underline block pt-0.5"
                >
                  + Cargar foto
                </button>
              </div>

              <!-- Requisito Bitácora PDT -->
              <div 
                class="border rounded-xl p-3 space-y-1 transition-all"
                :class="(ot.avances && ot.avances.length > 0) 
                  ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-800 dark:text-emerald-300' 
                  : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300'"
              >
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-[11px]">Bitácora PDT</span>
                  <IconCircleCheck v-if="ot.avances && ot.avances.length > 0" class="w-4 h-4 text-emerald-600 dark:text-emerald-400 stroke-[2.5]" />
                  <IconCircleX v-else class="w-4 h-4 text-rose-500 stroke-[2]" />
                </div>
                <div class="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                  {{ ot.avances?.length || 0 }} hito(s)
                </div>
                <button 
                  v-if="!ot.avances || ot.avances.length === 0" 
                  @click="activeTab = 'avances'"
                  class="text-[10px] text-red-600 dark:text-red-400 font-extrabold hover:underline block pt-0.5"
                >
                  + Publicar hito
                </button>
              </div>
            </div>

            <!-- 3. CASO MP AIRE ACONDICIONADO -->
            <div v-else class="grid grid-cols-2 sm:grid-cols-4 gap-2">
              <!-- Requisito Placa Técnica AA -->
              <div 
                class="border rounded-xl p-3 space-y-1 transition-all"
                :class="(countEvidencias('placas') >= 1 || countEvidencias('antes') >= 1)
                  ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-800 dark:text-emerald-300' 
                  : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300'"
              >
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-[11px]">Placa Técnica AA</span>
                  <IconCircleCheck v-if="countEvidencias('placas') >= 1 || countEvidencias('antes') >= 1" class="w-4 h-4 text-emerald-600 dark:text-emerald-400 stroke-[2.5]" />
                  <IconCircleX v-else class="w-4 h-4 text-rose-500 stroke-[2]" />
                </div>
                <div class="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                  {{ countEvidencias('placas') + countEvidencias('antes') }} cargada(s)
                </div>
                <button 
                  v-if="countEvidencias('placas') < 1 && countEvidencias('antes') < 1" 
                  @click="activeTab = 'evidencias'"
                  class="text-[10px] text-red-600 dark:text-red-400 font-extrabold hover:underline block pt-0.5"
                >
                  + Cargar foto
                </button>
              </div>

              <!-- Requisito Lavado Serpentines -->
              <div 
                class="border rounded-xl p-3 space-y-1 transition-all"
                :class="(countEvidencias('mantenimiento') >= 1 || countEvidencias('durante') >= 1)
                  ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-800 dark:text-emerald-300' 
                  : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300'"
              >
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-[11px]">Lavado Serpentines</span>
                  <IconCircleCheck v-if="countEvidencias('mantenimiento') >= 1 || countEvidencias('durante') >= 1" class="w-4 h-4 text-emerald-600 dark:text-emerald-400 stroke-[2.5]" />
                  <IconCircleX v-else class="w-4 h-4 text-rose-500 stroke-[2]" />
                </div>
                <div class="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                  {{ countEvidencias('mantenimiento') + countEvidencias('durante') }} cargada(s)
                </div>
                <button 
                  v-if="countEvidencias('mantenimiento') < 1 && countEvidencias('durante') < 1" 
                  @click="activeTab = 'evidencias'"
                  class="text-[10px] text-red-600 dark:text-red-400 font-extrabold hover:underline block pt-0.5"
                >
                  + Cargar foto
                </button>
              </div>

              <!-- Requisito Mediciones Operativas -->
              <div 
                class="border rounded-xl p-3 space-y-1 transition-all"
                :class="(countEvidencias('pruebas') >= 1 || countEvidencias('despues') >= 1)
                  ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-800 dark:text-emerald-300' 
                  : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300'"
              >
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-[11px]">Mediciones Operativas</span>
                  <IconCircleCheck v-if="countEvidencias('pruebas') >= 1 || countEvidencias('despues') >= 1" class="w-4 h-4 text-emerald-600 dark:text-emerald-400 stroke-[2.5]" />
                  <IconCircleX v-else class="w-4 h-4 text-rose-500 stroke-[2]" />
                </div>
                <div class="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                  {{ countEvidencias('pruebas') + countEvidencias('despues') }} cargada(s)
                </div>
                <button 
                  v-if="countEvidencias('pruebas') < 1 && countEvidencias('despues') < 1" 
                  @click="activeTab = 'evidencias'"
                  class="text-[10px] text-red-600 dark:text-red-400 font-extrabold hover:underline block pt-0.5"
                >
                  + Cargar foto
                </button>
              </div>

              <!-- Requisito Bitácora PDT -->
              <div 
                class="border rounded-xl p-3 space-y-1 transition-all"
                :class="(ot.avances && ot.avances.length > 0) 
                  ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-800 dark:text-emerald-300' 
                  : 'bg-slate-50 dark:bg-[#0a0b10] border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300'"
              >
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-[11px]">Bitácora PDT</span>
                  <IconCircleCheck v-if="ot.avances && ot.avances.length > 0" class="w-4 h-4 text-emerald-600 dark:text-emerald-400 stroke-[2.5]" />
                  <IconCircleX v-else class="w-4 h-4 text-rose-500 stroke-[2]" />
                </div>
                <div class="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                  {{ ot.avances?.length || 0 }} hito(s)
                </div>
                <button 
                  v-if="!ot.avances || ot.avances.length === 0" 
                  @click="activeTab = 'avances'"
                  class="text-[10px] text-red-600 dark:text-red-400 font-extrabold hover:underline block pt-0.5"
                >
                  + Publicar hito
                </button>
              </div>
            </div>

            <!-- Lista de Pendientes si falta algo para cerrar -->
            <div v-if="requisitosFaltantes.length > 0" class="p-3 bg-amber-500/10 border border-amber-500/30 rounded-xl space-y-1.5 text-xs">
              <div class="flex items-center gap-1.5 font-bold text-amber-700 dark:text-amber-400">
                <IconAlertTriangle class="w-4 h-4 shrink-0" />
                <span>Pendientes para Habilitar Cierre Técnico ({{ requisitosFaltantes.length }}):</span>
              </div>
              <ul class="list-disc list-inside space-y-0.5 text-[11px] text-amber-800 dark:text-amber-300/90 font-medium pl-1">
                <li v-for="(req, rIdx) in requisitosFaltantes" :key="rIdx">
                  {{ req }}
                </li>
              </ul>
            </div>

            <!-- Botón Principal de Cierre Definitivo -->
            <button
              @click="isCloseModalOpen = true"
              :disabled="!canCloseOt || updating"
              class="w-full font-black py-4 rounded-xl text-xs sm:text-sm shadow-xl transition-all flex items-center justify-center gap-2"
              :class="canCloseOt 
                ? 'bg-emerald-600 hover:bg-emerald-500 text-white active:scale-98 cursor-pointer shadow-emerald-600/25' 
                : 'bg-slate-100 dark:bg-white/5 text-slate-400 dark:text-slate-500 border border-slate-200 dark:border-white/10 cursor-not-allowed opacity-80'"
            >
              <IconCircleCheck class="w-5 h-5 stroke-[2.2]" />
              <span>{{ canCloseOt ? 'Finalizar y Solucionar OT en Campo' : 'Complete los Requisitos Previos para Cerrar' }}</span>
            </button>
          </div>

          <!-- Si la OT ya está solucionada o finalizada -->
          <div v-if="['solucionada', 'finalizada'].includes(ot.estado)" class="bg-emerald-50/70 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/60 rounded-2xl p-4 sm:p-5 text-center space-y-3 shadow-xs">
            <div class="w-12 h-12 rounded-full bg-emerald-100 dark:bg-emerald-900/60 text-emerald-600 dark:text-emerald-400 flex items-center justify-center mx-auto shadow-xs">
              <IconCircleCheck class="w-7 h-7 stroke-[2.5]" />
            </div>
            <div>
              <h4 class="text-sm font-black text-emerald-800 dark:text-emerald-300">Orden de Trabajo Solucionada Técnicamente</h4>
              <p class="text-xs text-slate-600 dark:text-slate-400 mt-0.5">
                Cerrada el {{ formatDate(ot.fecha_solucion || ot.updated_at) }}
              </p>
            </div>

            <div class="bg-white dark:bg-[#0a0b10] border border-emerald-200/60 dark:border-white/10 rounded-xl p-3 text-left space-y-1.5 text-xs">
              <div v-if="ot.causa_falla" class="flex justify-between items-center text-[11px]">
                <span class="text-slate-500 dark:text-slate-400 font-semibold">Causa Raíz de Falla:</span>
                <span class="font-bold text-slate-800 dark:text-slate-200 uppercase font-mono">{{ ot.causa_falla }}</span>
              </div>
              <div v-if="ot.observaciones_cierre" class="pt-1 border-t border-slate-100 dark:border-white/10">
                <span class="text-slate-500 dark:text-slate-400 font-semibold block text-[11px]">Observaciones de Cierre:</span>
                <p class="text-slate-800 dark:text-slate-200 mt-0.5 leading-relaxed">{{ ot.observaciones_cierre }}</p>
              </div>
              <div class="flex justify-between items-center text-[11px] pt-1 border-t border-slate-100 dark:border-white/10">
                <span class="text-slate-500 dark:text-slate-400 font-semibold">Insumos Registrados:</span>
                <span class="font-bold text-slate-800 dark:text-slate-200">{{ ot.repuestos?.length || 0 }} ítems LPU</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CONTENIDO PESTAÑA 2: MINUTOGRAMA / AVANCES (PDT) -->
      <div v-if="activeTab === 'avances'" class="space-y-4">
        
        <!-- 1. RESUMEN DE PROGRESO PDT ACUMULADO -->
        <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3 shadow-xs">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <div class="p-1.5 rounded-lg bg-red-500/10 text-red-600 dark:text-red-400">
                <IconTrendingUp class="w-4 h-4 stroke-[2.2]" />
              </div>
              <h3 class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider">Progreso Acumulado PDT</h3>
            </div>
            <div class="flex items-center gap-1.5">
              <span class="font-mono font-black text-sm text-red-600 dark:text-red-400">{{ ot.progreso || 0 }}%</span>
              <span class="text-xs text-slate-400 dark:text-slate-500 font-bold">/ 100%</span>
            </div>
          </div>

          <!-- Barra de progreso dual (Actual + Proyección si está editando) -->
          <div class="w-full bg-slate-100 dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-full h-3 overflow-hidden flex p-0.5">
            <!-- Barra actual -->
            <div
              class="bg-gradient-to-r from-red-600 to-red-500 h-full rounded-full transition-all duration-500 shadow-sm"
              :style="{ width: `${Math.min(100, ot.progreso || 0)}%` }"
            ></div>
            <!-- Barra proyectada nueva (si aplica) -->
            <div
              v-if="!['solucionada', 'finalizada'].includes(ot.estado) && nuevoAvance.porcentaje > 0 && maxAvancePermitido > 0"
              class="bg-red-400/80 dark:bg-red-500/70 h-full rounded-full transition-all duration-300 animate-pulse ml-0.5"
              :style="{ width: `${Math.min(nuevoAvance.porcentaje, maxAvancePermitido)}%` }"
            ></div>
          </div>

          <!-- Sub-indicadores de meta -->
          <div class="flex items-center justify-between text-[11px] pt-1">
            <div class="text-slate-500 dark:text-slate-400 font-medium">
              Restante para meta: 
              <span class="font-mono font-black text-slate-700 dark:text-slate-200">{{ maxAvancePermitido }}%</span>
            </div>
            <div v-if="!['solucionada', 'finalizada'].includes(ot.estado) && nuevoAvance.porcentaje > 0 && maxAvancePermitido > 0" class="text-red-600 dark:text-red-400 font-semibold font-mono">
              Proyectado: {{ avanceProyectado }}%
            </div>
            <div v-else-if="maxAvancePermitido === 0" class="flex items-center gap-1 text-emerald-600 dark:text-emerald-400 font-bold">
              <IconCheck class="w-3.5 h-3.5 stroke-[2.5]" />
              <span>Meta 100% alcanzada</span>
            </div>
          </div>
        </div>

        <!-- 2. FORMULARIO PARA REGISTRAR NUEVO AVANCE -->
        <div v-if="!['solucionada', 'finalizada'].includes(ot.estado)" class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3.5 shadow-xs">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <div class="p-1.5 rounded-lg bg-red-500/10 text-red-600 dark:text-red-400">
                <IconNotes class="w-4 h-4 stroke-[2.2]" />
              </div>
              <h3 class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider">Nuevo Reporte en Bitácora</h3>
            </div>
            <span class="text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider">Hito de Campo</span>
          </div>

          <!-- Si ya alcanzó el 100%, advertir -->
          <div v-if="maxAvancePermitido === 0" class="p-3 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/40 rounded-xl flex items-center gap-2.5 text-xs text-emerald-800 dark:text-emerald-300">
            <IconCheck class="w-4 h-4 shrink-0 text-emerald-600 dark:text-emerald-400 stroke-[2.5]" />
            <p>La orden ya se encuentra al <strong>100% de ejecución técnica</strong>. No es posible adicionar más porcentaje de avance.</p>
          </div>

          <!-- Formulario activo si aún resta porcentaje -->
          <div v-else class="space-y-3">
            <!-- Textarea con contador de caracteres -->
            <div>
              <div class="flex justify-between items-center mb-1">
                <label class="text-[11px] text-slate-600 dark:text-slate-400 font-semibold">
                  Descripción Técnica de la Actividad Realizada
                </label>
                <span 
                  class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-md"
                  :class="(nuevoAvance.descripcion || '').trim().length >= 5 ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400' : 'bg-amber-500/10 text-amber-600 dark:text-amber-400'"
                >
                  {{ (nuevoAvance.descripcion || '').trim().length }}/5 mín.
                </span>
              </div>
              <textarea
                v-model="nuevoAvance.descripcion"
                rows="3"
                placeholder="Describa el trabajo realizado (ej. Se completó el conexionado del tablero de fuerza, pruebas de aislamiento y rotulación de breakers)..."
                class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 text-xs text-slate-900 dark:text-white placeholder:text-slate-400 focus:ring-2 focus:ring-red-500 focus:outline-none transition-all leading-relaxed resize-none"
              ></textarea>
            </div>

            <!-- Chips de preajuste rápido -->
            <div>
              <label class="text-[11px] text-slate-600 dark:text-slate-400 font-semibold block mb-1.5">
                Selección Rápida de Incremento (%)
              </label>
              <div class="flex flex-wrap gap-1.5">
                <button
                  v-for="preset in [5, 10, 15, 20, 25]"
                  :key="preset"
                  type="button"
                  @click="setAvancePreset(preset)"
                  :disabled="preset > maxAvancePermitido"
                  class="px-2.5 py-1 rounded-lg text-xs font-mono font-bold transition-all"
                  :class="nuevoAvance.porcentaje === preset 
                    ? 'bg-red-600 text-white shadow-xs' 
                    : preset > maxAvancePermitido 
                      ? 'bg-slate-100 dark:bg-white/5 text-slate-400 dark:text-slate-600 cursor-not-allowed opacity-50' 
                      : 'bg-slate-100 hover:bg-slate-200 dark:bg-[#0a0b10] dark:hover:bg-white/10 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-white/10 active:scale-95'"
                >
                  +{{ preset }}%
                </button>
                <button
                  type="button"
                  @click="setAvancePreset('restante')"
                  class="px-2.5 py-1 rounded-lg text-xs font-mono font-bold transition-all"
                  :class="nuevoAvance.porcentaje === maxAvancePermitido 
                    ? 'bg-red-600 text-white shadow-xs' 
                    : 'bg-red-50 hover:bg-red-100 dark:bg-red-950/40 dark:hover:bg-red-900/50 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-900/60 active:scale-95'"
                >
                  Restante (+{{ maxAvancePermitido }}%)
                </button>
              </div>
            </div>

            <!-- Entrada numérica precisa y botón de envío -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1 items-end">
              <div>
                <label class="text-[11px] text-slate-600 dark:text-slate-400 font-semibold block mb-1">
                  % Incremental a Registrar
                </label>
                <div class="relative">
                  <input
                    v-model.number="nuevoAvance.porcentaje"
                    type="number"
                    min="1"
                    :max="maxAvancePermitido"
                    class="w-full bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl px-3 py-2.5 text-xs text-slate-900 dark:text-white font-mono font-bold focus:ring-2 focus:ring-red-500 focus:outline-none"
                  />
                  <span class="absolute right-3 top-2.5 text-xs font-mono font-bold text-slate-400">%</span>
                </div>
              </div>

              <div>
                <button
                  @click="pedirConfirmacionAvance"
                  :disabled="updating || !isAvanceValido"
                  class="w-full py-2.5 px-4 rounded-xl text-xs font-extrabold flex items-center justify-center gap-2 transition-all shadow-md"
                  :class="isAvanceValido && !updating
                    ? 'bg-red-600 hover:bg-red-500 text-white shadow-red-600/25 active:scale-98 cursor-pointer' 
                    : 'bg-slate-200 dark:bg-white/5 text-slate-400 dark:text-slate-600 cursor-not-allowed shadow-none'"
                >
                  <IconSend class="w-4 h-4 stroke-[2]" />
                  <span>Publicar en Bitácora (+{{ nuevoAvance.porcentaje || 0 }}%)</span>
                </button>
              </div>
            </div>

            <div v-if="(nuevoAvance.descripcion || '').trim().length > 0 && (nuevoAvance.descripcion || '').trim().length < 5" class="flex items-center gap-1.5 text-[11px] text-amber-600 dark:text-amber-400">
              <IconAlertCircle class="w-3.5 h-3.5 shrink-0" />
              <span>La descripción debe contener al menos 5 caracteres técnicos.</span>
            </div>
          </div>
        </div>

        <!-- 3. HISTÓRICO CRONOLÓGICO DE BITÁCORA (TIMELINE) -->
        <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3.5 shadow-xs">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <div class="p-1.5 rounded-lg bg-red-500/10 text-red-600 dark:text-red-400">
                <IconHistory class="w-4 h-4 stroke-[2.2]" />
              </div>
              <h3 class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider">Línea de Tiempo Bitácora (PDT)</h3>
            </div>
            <span class="text-red-600 dark:text-red-400 font-mono text-[11px] font-black bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-900/40 px-2 py-0.5 rounded-md">
              {{ ot.avances?.length || 0 }} registros
            </span>
          </div>

          <!-- Empty state si no hay avances -->
          <div v-if="!ot.avances || ot.avances.length === 0" class="text-center py-8 px-4 bg-slate-50 dark:bg-[#0a0b10] border border-dashed border-slate-200 dark:border-white/10 rounded-xl space-y-2">
            <IconHistory class="w-8 h-8 mx-auto text-slate-300 dark:text-slate-600 stroke-[1.5]" />
            <p class="text-xs font-bold text-slate-600 dark:text-slate-400">Sin registros de bitácora todavía</p>
            <p class="text-[11px] text-slate-400 dark:text-slate-500 max-w-xs mx-auto">
              Publique los hitos y actividades técnicas ejecutadas en sitio para documentar el minutograma de la orden.
            </p>
          </div>

          <!-- Lista en Timeline vertical -->
          <div v-else class="space-y-3 pt-1">
            <div 
              v-for="(av, idx) in ot.avances" 
              :key="av.id || idx"
              class="relative pl-6 pb-4 last:pb-1 border-l-2 border-slate-200 dark:border-white/10 ml-2"
            >
              <!-- Nodo / Icono en la línea de tiempo -->
              <div class="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-red-600 border-2 border-white dark:border-[#121215] flex items-center justify-center">
                <div class="w-1.5 h-1.5 rounded-full bg-white"></div>
              </div>

              <!-- Tarjeta de contenido del avance -->
              <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200/80 dark:border-white/10 rounded-xl p-3 space-y-2 shadow-xs -mt-1.5">
                <!-- Cabecera del hito -->
                <div class="flex flex-wrap items-center justify-between gap-1.5 text-xs">
                  <div class="flex items-center gap-2">
                    <span class="font-mono font-black text-xs px-2 py-0.5 rounded-md bg-red-100 text-red-700 dark:bg-red-950/80 dark:text-red-300 border border-red-200 dark:border-red-900/60">
                      +{{ av.porcentaje }}%
                    </span>
                    <div class="flex items-center gap-1 text-slate-600 dark:text-slate-300 font-semibold text-[11px]">
                      <IconUser class="w-3.5 h-3.5 text-slate-400 dark:text-slate-500 stroke-[2]" />
                      <span>{{ av.user?.name || 'Técnico de Campo' }}</span>
                    </div>
                  </div>
                  <div class="flex items-center gap-1 text-[10px] text-slate-400 dark:text-slate-500 font-mono">
                    <IconClock class="w-3 h-3 stroke-[2]" />
                    <span>{{ formatDate(av.created_at || av.fecha_reporte) }}</span>
                  </div>
                </div>

                <!-- Descripción del hito -->
                <p class="text-xs text-slate-800 dark:text-slate-200 leading-relaxed font-normal whitespace-pre-line">
                  {{ av.descripcion }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CONTENIDO PESTAÑA 3: EVIDENCIAS FOTOGRÁFICAS SEGÚN TIPO DE TRABAJO -->
      <div v-if="activeTab === 'evidencias'" class="space-y-5">
        <div class="p-3 bg-slate-100 dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-2xl flex items-center justify-between flex-wrap gap-2">
          <div>
            <h3 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
              Protocolo de Evidencias: {{ isCorrectivo ? 'Correctivos & Obras (WO)' : (isPreventivoAire ? 'Preventivo Climatización (MP AA)' : (isPreventivo7x24 ? 'Preventivo Rutina 7x24 (MP)' : 'Preventivo Planta Eléctrica (MP GE)')) }}
            </h3>
            <p class="text-[11px] text-slate-500 dark:text-slate-400">
              Formato de captura fotográfica con geolocalización GPS y fecha incrustada
            </p>
          </div>
          <span class="text-red-600 dark:text-red-400 font-mono text-xs font-black bg-red-50 dark:bg-red-950/60 border border-red-200 dark:border-red-900/60 px-2.5 py-1 rounded-xl">
            {{ ot.evidencias?.length || 0 }} fotos registradas
          </span>
        </div>

        <!-- 1. CASO FORMATO WO: CORRECTIVO Y EMERGENCIA -->
        <template v-if="isCorrectivo">
          <PhotoUploader
            tipo="antes"
            titulo="1. Diagnóstico Inicial & Falla Encontrada"
            descripcion="Fotografía legible del estado del equipo averiado, daño físico o alarma activa en tablero antes de iniciar labores."
            badge-label="Antes (Falla)"
            :codigo-ot="ot.codigo"
            :evidencias-list="getEvidenciasPorTipo('antes')"
            :read-only="['solucionada', 'finalizada'].includes(ot.estado)"
            @photo-uploaded="pedirConfirmacionFoto"
            @delete-photo="pedirConfirmacionBorrarFoto"
          />

          <PhotoUploader
            tipo="durante"
            titulo="2. Intervención Técnica & Repuestos"
            descripcion="Registro del proceso de reparación, piezas retiradas vs repuestos nuevos instalados con serial y marca legibles."
            badge-label="Durante (Reparación)"
            :codigo-ot="ot.codigo"
            :evidencias-list="getEvidenciasPorTipo('durante')"
            :read-only="['solucionada', 'finalizada'].includes(ot.estado)"
            @photo-uploaded="pedirConfirmacionFoto"
            @delete-photo="pedirConfirmacionBorrarFoto"
          />

          <PhotoUploader
            tipo="despues"
            titulo="3. Equipo Operativo en Servicio & Cierre"
            descripcion="Equipo solucionado operando en condiciones normales, tablero sin alarmas y caseta cerrada y limpia."
            badge-label="Después (Solucionado)"
            :codigo-ot="ot.codigo"
            :evidencias-list="getEvidenciasPorTipo('despues')"
            :read-only="['solucionada', 'finalizada'].includes(ot.estado)"
            @photo-uploaded="pedirConfirmacionFoto"
            @delete-photo="pedirConfirmacionBorrarFoto"
          />

          <PhotoUploader
            tipo="transporte"
            titulo="4. Soporte Transporte Especial (Si Aplica)"
            descripcion="Registro fotográfico si se utilizó transporte en lancha fluvial, mula o vehículo de trocha difícil para acceder al sitio."
            badge-label="Transporte Especial (Opcional)"
            :codigo-ot="ot.codigo"
            :evidencias-list="getEvidenciasPorTipo('transporte')"
            :read-only="['solucionada', 'finalizada'].includes(ot.estado)"
            @photo-uploaded="pedirConfirmacionFoto"
            @delete-photo="pedirConfirmacionBorrarFoto"
          />
        </template>

        <!-- 2. CASO FORMATO MP: PREVENTIVO PLANTA ELÉCTRICA (GE) -->
        <template v-else-if="!isPreventivoAire">
          <PhotoUploader
            tipo="placas"
            titulo="1. Placas Técnicas de Equipos"
            descripcion="Fotos nítidas de la placa de datos de la Planta Eléctrica, placa del Motor Diesel y placa del Generador."
            badge-label="Placas Técnicas"
            :codigo-ot="ot.codigo"
            :evidencias-list="[...getEvidenciasPorTipo('placas'), ...getEvidenciasPorTipo('antes')]"
            :read-only="['solucionada', 'finalizada'].includes(ot.estado)"
            @photo-uploaded="pedirConfirmacionFoto"
            @delete-photo="pedirConfirmacionBorrarFoto"
          />

          <PhotoUploader
            tipo="inicial"
            titulo="2. Horómetro Inicial & Estado de Caseta"
            descripcion="Foto legible del horómetro del tablero antes de la rutina y panorámica del grupo electrógeno en su caseta/cabina."
            badge-label="Horómetro Inicial"
            :codigo-ot="ot.codigo"
            :evidencias-list="getEvidenciasPorTipo('inicial')"
            :read-only="['solucionada', 'finalizada'].includes(ot.estado)"
            @photo-uploaded="pedirConfirmacionFoto"
            @delete-photo="pedirConfirmacionBorrarFoto"
          />

          <PhotoUploader
            tipo="mantenimiento"
            titulo="3. Servicio de Filtración & Mantenimiento"
            descripcion="Evidencias fotográficas del cambio de filtro de aceite, combustible, aire, lubricante nuevo y refrigerante."
            badge-label="Filtración & Rutina"
            :codigo-ot="ot.codigo"
            :evidencias-list="[...getEvidenciasPorTipo('mantenimiento'), ...getEvidenciasPorTipo('durante'), ...getEvidenciasPorTipo('filtracion')]"
            :read-only="['solucionada', 'finalizada'].includes(ot.estado)"
            @photo-uploaded="pedirConfirmacionFoto"
            @delete-photo="pedirConfirmacionBorrarFoto"
          />

          <PhotoUploader
            tipo="pruebas"
            titulo="4. Pruebas Operativas ATS con Carga (15 Min)"
            descripcion="Prueba con carga simulando falla de energía (15 min), horómetro final de prueba y tablero en modo automático sin alarmas."
            badge-label="Pruebas con Carga"
            :codigo-ot="ot.codigo"
            :evidencias-list="[...getEvidenciasPorTipo('pruebas'), ...getEvidenciasPorTipo('despues')]"
            :read-only="['solucionada', 'finalizada'].includes(ot.estado)"
            @photo-uploaded="pedirConfirmacionFoto"
            @delete-photo="pedirConfirmacionBorrarFoto"
          />

          <PhotoUploader
            tipo="transporte"
            titulo="5. Soporte Transporte Especial (Si Aplica)"
            descripcion="Fotografía de movilización especial fluvial (lancha) o bestia/mula requerida para el mantenimiento del sitio."
            badge-label="Transporte Especial (Opcional)"
            :codigo-ot="ot.codigo"
            :evidencias-list="getEvidenciasPorTipo('transporte')"
            :read-only="['solucionada', 'finalizada'].includes(ot.estado)"
            @photo-uploaded="pedirConfirmacionFoto"
            @delete-photo="pedirConfirmacionBorrarFoto"
          />
        </template>

        <!-- 3. CASO FORMATO MP: PREVENTIVO CLIMATIZACIÓN (AIRE ACONDICIONADO) -->
        <template v-else>
          <PhotoUploader
            tipo="placas"
            titulo="1. Placa Técnica & Estado Previo AA"
            descripcion="Placa de características técnicas del equipo (evaporador/condensador) y estado de suciedad antes del lavado."
            badge-label="Placa & Previo"
            :codigo-ot="ot.codigo"
            :evidencias-list="[...getEvidenciasPorTipo('placas'), ...getEvidenciasPorTipo('antes')]"
            :read-only="['solucionada', 'finalizada'].includes(ot.estado)"
            @photo-uploaded="pedirConfirmacionFoto"
            @delete-photo="pedirConfirmacionBorrarFoto"
          />

          <PhotoUploader
            tipo="mantenimiento"
            titulo="2. Lavado & Mantenimiento de Serpentines"
            descripcion="Lavado a presión de serpentín condensador/evaporador, limpieza profunda de filtros y bandeja de desagüe."
            badge-label="Lavado & Mantenimiento"
            :codigo-ot="ot.codigo"
            :evidencias-list="[...getEvidenciasPorTipo('mantenimiento'), ...getEvidenciasPorTipo('durante')]"
            :read-only="['solucionada', 'finalizada'].includes(ot.estado)"
            @photo-uploaded="pedirConfirmacionFoto"
            @delete-photo="pedirConfirmacionBorrarFoto"
          />

          <PhotoUploader
            tipo="pruebas"
            titulo="3. Mediciones Operativas y Frigoríficas"
            descripcion="Lectura manométrica (presión de baja/alta PSI), pinza amperimétrica (corriente compresor) y termómetro de inyección/retorno."
            badge-label="Mediciones & Cierre"
            :codigo-ot="ot.codigo"
            :evidencias-list="[...getEvidenciasPorTipo('pruebas'), ...getEvidenciasPorTipo('despues')]"
            :read-only="['solucionada', 'finalizada'].includes(ot.estado)"
            @photo-uploaded="pedirConfirmacionFoto"
            @delete-photo="pedirConfirmacionBorrarFoto"
          />

          <PhotoUploader
            tipo="transporte"
            titulo="4. Soporte Transporte Especial (Si Aplica)"
            descripcion="Fotografía de movilización especial si aplicó para acceder a la estación de climatización."
            badge-label="Transporte Especial (Opcional)"
            :codigo-ot="ot.codigo"
            :evidencias-list="getEvidenciasPorTipo('transporte')"
            :read-only="['solucionada', 'finalizada'].includes(ot.estado)"
            @photo-uploaded="pedirConfirmacionFoto"
            @delete-photo="pedirConfirmacionBorrarFoto"
          />
        </template>
      </div>

      <!-- CONTENIDO PESTAÑA 4: REPUESTOS LPU -->
      <!-- CONTENIDO PESTAÑA 4: REPUESTOS E INSUMOS -->
      <div v-if="activeTab === 'repuestos'" class="space-y-4">
        <!-- 1. Materiales e Insumos Menores Utilizados (Buscador + Foto Antes y Después) -->
        <InsumosMenoresManager
          v-model="otFormularioData.insumos_menores"
          :codigo-ot="ot.codigo"
          :read-only="['solucionada', 'finalizada'].includes(ot.estado)"
        />

        <!-- 2. Repuestos Retirados e Instalados con Foto -->
        <RepuestosCambiosManager
          v-model="otFormularioData.repuestos_cambios"
          :codigo-ot="ot.codigo"
          :read-only="['solucionada', 'finalizada'].includes(ot.estado)"
        />

        <!-- Botón para Guardar Insumos y Repuestos de Campo -->
        <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 flex flex-col sm:flex-row items-center justify-between gap-3 shadow-xs">
          <div>
            <div class="text-xs font-black text-slate-900 dark:text-white flex items-center gap-1.5">
              <IconBox class="w-4 h-4 text-red-600 stroke-[2.2]" />
              <span>Guardar Insumos Menores & Repuestos Cambiados</span>
            </div>
            <p class="text-[11px] text-slate-500 dark:text-slate-400">
              Guarda tus consumibles menores y piezas reemplazadas con sus fotografías de respaldo.
            </p>
          </div>
          <button
            type="button"
            @click="guardarFormularioTecnico"
            :disabled="guardandoFormulario"
            class="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl text-xs font-black bg-red-600 hover:bg-red-500 text-white shadow-md active:scale-95 transition-all cursor-pointer disabled:opacity-50"
          >
            <IconDeviceFloppy class="w-4 h-4 stroke-[2.2]" />
            <span>{{ guardandoFormulario ? 'Guardando...' : 'Guardar Insumos & Repuestos' }}</span>
          </button>
        </div>
      </div>

      <!-- CONTENIDO PESTAÑA 5: FORMULARIO TÉCNICO DE CAMPO & CHECKLIST -->
      <div v-if="activeTab === 'checklist'" class="space-y-4">
        <!-- Barra de Estado de Sincronización del Formulario -->
        <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl px-4 py-2.5 flex items-center justify-between shadow-xs">
          <div class="flex items-center gap-2">
            <IconFileCheck class="w-4 h-4 text-red-600 dark:text-red-400 stroke-[2]" />
            <span class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider">
              Formato Técnico de Campo
            </span>
          </div>
          <div class="flex items-center gap-2">
            <span 
              v-if="autoSaveStatus === 'saving' || guardandoFormulario" 
              class="text-[11px] font-bold text-amber-600 dark:text-amber-400 flex items-center gap-1.5"
            >
              <svg class="animate-spin h-3.5 w-3.5 text-amber-600 dark:text-amber-400" viewBox="0 0 24 24" fill="none">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
              </svg>
              Guardando cambios...
            </span>
            <span 
              v-else-if="autoSaveStatus === 'saved'" 
              class="text-[11px] font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1"
            >
              <IconCheck class="w-3.5 h-3.5 stroke-[3]" />
              Guardado en servidor
            </span>
            <span 
              v-else-if="autoSaveStatus === 'unsaved'" 
              class="text-[11px] font-bold text-slate-400 flex items-center gap-1"
            >
              Cambios pendientes
            </span>
            <button
              type="button"
              @click="guardarFormularioTecnico"
              :disabled="guardandoFormulario || isAutoSaving"
              class="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-white/5 hover:bg-slate-200 dark:hover:bg-white/10 text-slate-700 dark:text-slate-300 text-[10px] font-bold transition-all cursor-pointer"
            >
              Guardar ahora
            </button>
          </div>
        </div>

        <!-- 1. Control de Llegada a Sitio (Técnico con Carnet y Sitio al Fondo) -->
        <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3 shadow-xs">
          <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-2.5">
            <div class="flex items-center gap-2">
              <IconMapPinCheck class="w-4 h-4 text-amber-600 dark:text-amber-400 stroke-[2]" />
              <h4 class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider">
                Control de Llegada a Sitio (Técnico con Carnet & Estación)
              </h4>
            </div>
          </div>

          <div>
            <SinglePhotoCapture
              v-model="otFormularioData.llegada_foto"
              label="Foto del Técnico con Carnet y Estación al Fondo *"
              tag="LLEGADA - TECNICO + CARNET + SITIO"
              :codigo-ot="ot.codigo"
              :disabled="['solucionada', 'finalizada'].includes(ot.estado)"
              placeholder="Tomar foto del técnico con carnet visible y sitio al fondo"
              :required="true"
              @change="handleFotoLlegadaChange"
            />
          </div>
        </div>

        <!-- 2. Formulario Técnico Específico según tipo de trabajo -->
        <FormularioTecnicoWO
          v-if="isCorrectivo"
          v-model="otFormularioData"
        />
        <FormularioTecnicoMP
          v-else
          v-model="otFormularioData"
          :tipo-preventivo="isPreventivoAire ? 'aire' : (isPreventivo7x24 ? 'rutina_7x24' : 'planta')"
        />

        <!-- 3. Repuestos Retirados e Instalados (con Fotos de Sustitución) -->
        <RepuestosCambiosManager
          v-model="otFormularioData.repuestos_cambios"
          :codigo-ot="ot.codigo"
          :read-only="['solucionada', 'finalizada'].includes(ot.estado)"
        />

        <!-- 4. Materiales e Insumos Menores Utilizados (con Fotos Antes y Después) -->
        <InsumosMenoresManager
          v-model="otFormularioData.insumos_menores"
          :codigo-ot="ot.codigo"
          :read-only="['solucionada', 'finalizada'].includes(ot.estado)"
        />

        <!-- 5. Registro de Transporte Especial (LPU) - OBLIGATORIO -->
        <TransporteEspecialManager
          v-model="otFormularioData.transportes_especiales"
          :codigo-ot="ot.codigo"
          :read-only="['solucionada', 'finalizada'].includes(ot.estado)"
        />

        <!-- 6. Novedades y Hallazgos en Estación (con Fotos de Respaldo) -->
        <NovedadesHallazgosManager
          v-model="otFormularioData.hallazgos"
          :codigo-ot="ot.codigo"
          :read-only="['solucionada', 'finalizada'].includes(ot.estado)"
        />

        <!-- Botón para Guardar Formulario Técnico en Cualquier Momento -->
        <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 flex flex-col sm:flex-row items-center justify-between gap-3 shadow-xs">
          <div>
            <div class="text-xs font-black text-slate-900 dark:text-white flex items-center gap-1.5">
              <IconFileCheck class="w-4 h-4 text-emerald-500 stroke-[2.2]" />
              <span>Diligenciamiento de Campo (Formato Oficial {{ isCorrectivo ? 'WO' : 'MP' }})</span>
            </div>
            <p class="text-[11px] text-slate-500 dark:text-slate-400">
              Guarda tus avances técnicos en cualquier momento durante la intervención en sitio.
            </p>
          </div>
          <button
            type="button"
            @click="guardarFormularioTecnico"
            :disabled="guardandoFormulario"
            class="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl text-xs font-black bg-emerald-600 hover:bg-emerald-500 text-white shadow-md active:scale-95 transition-all cursor-pointer disabled:opacity-50"
          >
            <IconDeviceFloppy class="w-4 h-4 stroke-[2.2]" />
            <span>{{ guardandoFormulario ? 'Guardando...' : 'Guardar Formato de Campo' }}</span>
          </button>
        </div>
      </div>

      <!-- Modal para Registrar Llegada a Sitio (Técnico con carnet y sitio atrás) -->
      <LlegadaSitioModal
        :is-open="isLlegadaModalOpen"
        :codigo-ot="ot?.codigo_ot || ''"
        :saving="updating"
        :initial-foto="otFormularioData?.llegada_foto || otFormularioData?.llegada_sitio || otFormularioData?.llegada_carnet || ''"
        @close="isLlegadaModalOpen = false"
        @confirm="handleConfirmarLlegada"
      />

      <!-- Modal para Gestionar Insumos LPU (sin obligar a cerrar la OT) -->
      <ManageRepuestosModal
        :is-open="isManageRepuestosModalOpen"
        :saving="savingRepuestos"
        :initial-repuestos="ot?.repuestos || []"
        @close="isManageRepuestosModalOpen = false"
        @save="handleSaveRepuestos"
      />

      <!-- Modal de Cierre Definitivo de OT -->
      <CloseOtModal
        :is-open="isCloseModalOpen"
        :loading="updating"
        :error-msg="cierreErrorMsg"
        :initial-repuestos="ot?.repuestos || []"
        @close="isCloseModalOpen = false"
        @submit="pedirConfirmacionCierre"
      />

      <!-- Banner de Notificación Toast / Alerta de Mensajes al Usuario -->
      <div v-if="alertNotification.show" class="fixed top-4 right-4 left-4 sm:left-auto sm:w-96 z-[130] transition-all duration-300 transform">
        <div 
          class="p-4 rounded-2xl border shadow-2xl flex items-start gap-3 select-none backdrop-blur-md"
          :class="{
            'bg-emerald-50/95 border-emerald-300 text-emerald-950 dark:bg-emerald-950/90 dark:border-emerald-700 dark:text-emerald-100': alertNotification.type === 'success',
            'bg-rose-50/95 border-rose-300 text-rose-950 dark:bg-rose-950/90 dark:border-rose-700 dark:text-rose-100': alertNotification.type === 'error',
            'bg-amber-50/95 border-amber-300 text-amber-950 dark:bg-amber-950/90 dark:border-amber-700 dark:text-amber-100': alertNotification.type === 'warning'
          }"
        >
          <IconCircleCheck v-if="alertNotification.type === 'success'" class="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5 stroke-[2]" />
          <IconAlertTriangle v-else class="w-5 h-5 text-rose-600 dark:text-rose-400 shrink-0 mt-0.5 stroke-[2]" />
          <div class="flex-1 text-xs space-y-0.5">
            <div class="font-extrabold uppercase tracking-wide text-[11px]">{{ alertNotification.title }}</div>
            <div class="text-xs leading-relaxed font-medium">{{ alertNotification.message }}</div>
          </div>
          <button @click="alertNotification.show = false" class="p-1 hover:opacity-75 font-bold">
            <IconX class="w-4 h-4 stroke-[2]" />
          </button>
        </div>
      </div>

      <!-- Modal de Confirmación Previa para Acciones de Guardado/Finalización -->
      <ConfirmDialogModal
        :is-open="confirmModal.isOpen"
        :title="confirmModal.title"
        :subtitle="confirmModal.subtitle"
        :message="confirmModal.message"
        :confirm-text="confirmModal.confirmText"
        :type="confirmModal.type"
        :loading="updating"
        @confirm="handleConfirmAction"
        @cancel="confirmModal.isOpen = false"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import client from '@/api/client';
import SlaBadge from '@/components/common/SlaBadge.vue';
import PhotoUploader from '@/components/mobile/PhotoUploader.vue';
import FormularioTecnicoWO from '@/components/mobile/FormularioTecnicoWO.vue';
import FormularioTecnicoMP from '@/components/mobile/FormularioTecnicoMP.vue';
import CloseOtModal from '@/components/mobile/CloseOtModal.vue';
import ManageRepuestosModal from '@/components/mobile/ManageRepuestosModal.vue';
import ConfirmDialogModal from '@/components/common/ConfirmDialogModal.vue';
import LlegadaSitioModal from '@/components/mobile/LlegadaSitioModal.vue';
import TransporteEspecialManager from '@/components/mobile/TransporteEspecialManager.vue';
import NovedadesHallazgosManager from '@/components/mobile/NovedadesHallazgosManager.vue';
import RepuestosCambiosManager from '@/components/mobile/RepuestosCambiosManager.vue';
import InsumosMenoresManager from '@/components/mobile/InsumosMenoresManager.vue';
import SinglePhotoCapture from '@/components/mobile/SinglePhotoCapture.vue';
import { 
  IconArrowLeft, 
  IconRefresh, 
  IconBuildingBroadcastTower, 
  IconMapPin, 
  IconMapPinCheck,
  IconSteeringWheel, 
  IconActivity, 
  IconCamera, 
  IconBox, 
  IconPackageOff,
  IconListCheck,
  IconCar,
  IconCircleCheck,
  IconSend,
  IconPlus,
  IconAlertTriangle,
  IconX,
  IconTrendingUp,
  IconNotes,
  IconHistory,
  IconUser,
  IconClock,
  IconCheck,
  IconAlertCircle,
  IconPlayerPlay,
  IconPlayerPause,
  IconExternalLink,
  IconNavigation,
  IconTool,
  IconCircleX,
  IconDeviceFloppy,
  IconFileCheck,
  IconTruck,
  IconTools,
  IconExchange,
  IconIdBadge2
} from '@tabler/icons-vue';

const route = useRoute();
const ot = ref(null);
const loading = ref(true);
const updating = ref(false);
const isCloseModalOpen = ref(false);
const isManageRepuestosModalOpen = ref(false);
const isLlegadaModalOpen = ref(false);
const savingRepuestos = ref(false);
const cierreErrorMsg = ref('');
const activeTab = ref('flujo');

const alertNotification = ref({
  show: false,
  type: 'success',
  title: '',
  message: '',
});

const showNotification = (type, title, message) => {
  alertNotification.value = { show: true, type, title, message };
  setTimeout(() => {
    if (alertNotification.value.message === message) {
      alertNotification.value.show = false;
    }
  }, 7000);
};

const handleSaveRepuestos = async (repuestosList) => {
  if (!ot.value?.id) return;
  savingRepuestos.value = true;
  try {
    const res = await client.post(`/ots/${ot.value.id}/repuestos`, {
      repuestos: repuestosList
    });
    if (res.data.status === 'success') {
      showNotification('success', 'Insumos Actualizados', 'Se registraron los materiales e insumos en la OT con éxito.');
      isManageRepuestosModalOpen.value = false;
      fetchOtDetail();
    }
  } catch (err) {
    const msg = err.response?.data?.message || 'No se pudieron guardar los insumos.';
    showNotification('error', 'Error al Guardar Insumos', msg);
  } finally {
    savingRepuestos.value = false;
  }
};

const confirmModal = ref({
  isOpen: false,
  title: '',
  subtitle: '',
  message: '',
  confirmText: 'Sí, Confirmar',
  type: 'info',
  action: null,
});

const openConfirm = (opts) => {
  confirmModal.value = {
    isOpen: true,
    title: opts.title || 'Confirmar Acción',
    subtitle: opts.subtitle || 'Verifique antes de continuar',
    message: opts.message || '¿Desea proceder?',
    confirmText: opts.confirmText || 'Sí, Confirmar',
    type: opts.type || 'info',
    action: opts.action,
  };
};

const handleConfirmAction = async () => {
  if (confirmModal.value.action) {
    const act = confirmModal.value.action;
    confirmModal.value.isOpen = false;
    await act();
  }
};

const tabs = [
  { id: 'flujo', label: 'Flujo & Acción', shortLabel: 'Flujo', icon: IconSteeringWheel },
  { id: 'avances', label: 'Minutograma PDT', shortLabel: 'Bitácora', icon: IconActivity },
  { id: 'evidencias', label: 'Evidencias', shortLabel: 'Fotos', icon: IconCamera },
  { id: 'checklist', label: 'Formulario de Campo', shortLabel: 'Formato', icon: IconFileCheck },
  { id: 'repuestos', label: 'Repuestos LPU', shortLabel: 'Insumos', icon: IconBox },
];

const otFormularioData = ref({});
const guardandoFormulario = ref(false);

const isPreventivo = computed(() => {
  const tAct = (ot.value?.tipo_actividad || '').toLowerCase();
  const tMant = (ot.value?.tipo_mantenimiento || '').toLowerCase();
  return tMant === 'preventivo' || tAct.includes('preventivo') || tAct.includes('rutina') || tAct.includes('7x24');
});

const isCorrectivo = computed(() => !isPreventivo.value);

const isPreventivoAire = computed(() => {
  const tAct = (ot.value?.tipo_actividad || '').toLowerCase();
  const sub = (ot.value?.subsistema || '').toLowerCase();
  return tAct === 'preventivo_aire' || sub.includes('aire');
});

const isPreventivo7x24 = computed(() => {
  const tAct = (ot.value?.tipo_actividad || '').toLowerCase();
  return tAct.includes('7x24') || tAct.includes('rutina');
});

const autoSaveStatus = ref('saved'); // 'saved', 'saving', 'unsaved'
let lastSavedSnapshot = '';
let isAutoSaving = false;
let autosaveTimeout = null;
let initialDataLoaded = false;

watch(() => ot.value, (newOt) => {
  if (newOt && !initialDataLoaded) {
    if (newOt.datos_formulario && typeof newOt.datos_formulario === 'object') {
      otFormularioData.value = { ...newOt.datos_formulario };
    } else if (typeof newOt.datos_formulario === 'string') {
      try {
        otFormularioData.value = JSON.parse(newOt.datos_formulario);
      } catch (e) {
        otFormularioData.value = {};
      }
    } else {
      otFormularioData.value = {};
    }
    if (!otFormularioData.value.llegada_foto) {
      otFormularioData.value.llegada_foto = 
        otFormularioData.value.llegada_sitio || 
        otFormularioData.value.llegada_carnet_sitio || 
        otFormularioData.value.llegada_carnet || '';
    }
    lastSavedSnapshot = JSON.stringify(otFormularioData.value);
    initialDataLoaded = true;
  }
}, { immediate: true });

// Guardado del formulario técnico con control estricto de concurrencia y sin loops reactivos
const ejecutarGuardadoFormulario = async (silencioso = true) => {
  if (!ot.value?.id || ['solucionada', 'finalizada'].includes(ot.value?.estado)) return;
  
  const currentSnapshot = JSON.stringify(otFormularioData.value);
  // Si no hay cambios reales respecto al último guardado, abortar para no saturar la red
  if (currentSnapshot === lastSavedSnapshot || isAutoSaving) return;

  isAutoSaving = true;
  autoSaveStatus.value = 'saving';
  if (!silencioso) guardandoFormulario.value = true;

  try {
    const res = await client.put(`/ots/${ot.value.id}/formulario`, {
      datos_formulario: otFormularioData.value
    });

    if (res.data?.status === 'success') {
      lastSavedSnapshot = currentSnapshot;
      autoSaveStatus.value = 'saved';

      // Si el backend reemplazó fotos en base64 por rutas /uploads/, sincronizar solo esos campos
      if (res.data.data?.datos_formulario) {
        const parsed = typeof res.data.data.datos_formulario === 'string'
          ? JSON.parse(res.data.data.datos_formulario)
          : res.data.data.datos_formulario;

        if (parsed?.llegada_foto && parsed.llegada_foto.startsWith('/uploads/')) {
          otFormularioData.value.llegada_foto = parsed.llegada_foto;
          otFormularioData.value.llegada_sitio = parsed.llegada_foto;
        }
        lastSavedSnapshot = JSON.stringify(otFormularioData.value);
      }

      if (res.data.data?.evidencias) {
        ot.value.evidencias = res.data.data.evidencias;
      }

      if (!silencioso) {
        showNotification('success', 'Formato Guardado', 'El formulario técnico de campo se ha guardado exitosamente.');
      }
    }
  } catch (err) {
    autoSaveStatus.value = 'unsaved';
    if (!silencioso) {
      const msg = err.response?.data?.message || 'Error al guardar el formulario técnico.';
      showNotification('error', 'Error al Guardar', msg);
    }
  } finally {
    isAutoSaving = false;
    if (!silencioso) guardandoFormulario.value = false;
  }
};

const guardarFormularioTecnico = () => ejecutarGuardadoFormulario(false);

// 1. Guardar automáticamente al cambiar de pestaña
watch(activeTab, (newTab, oldTab) => {
  if (oldTab === 'checklist') {
    ejecutarGuardadoFormulario(true);
  }
});

// 2. Guardar automáticamente por inactividad tras cambios reales (debounce seguro de 3.5 segundos)
watch(otFormularioData, () => {
  if (!initialDataLoaded || !ot.value?.id || ['solucionada', 'finalizada'].includes(ot.value?.estado)) return;
  const currentSnapshot = JSON.stringify(otFormularioData.value);
  if (currentSnapshot === lastSavedSnapshot) return;

  autoSaveStatus.value = 'unsaved';
  if (autosaveTimeout) clearTimeout(autosaveTimeout);
  autosaveTimeout = setTimeout(() => {
    ejecutarGuardadoFormulario(true);
  }, 3500);
}, { deep: true });

const nuevoAvance = ref({
  descripcion: '',
  porcentaje: 10,
});

const maxAvancePermitido = computed(() => {
  const actual = Number(ot.value?.progreso) || 0;
  return Math.max(0, 100 - actual);
});

const avanceProyectado = computed(() => {
  const actual = Number(ot.value?.progreso) || 0;
  const inc = Number(nuevoAvance.value.porcentaje) || 0;
  return Math.min(100, actual + inc);
});

const isAvanceValido = computed(() => {
  const desc = (nuevoAvance.value.descripcion || '').trim();
  const pct = Number(nuevoAvance.value.porcentaje) || 0;
  return desc.length >= 5 && pct > 0 && pct <= maxAvancePermitido.value;
});

const setAvancePreset = (val) => {
  const max = maxAvancePermitido.value;
  if (val === 'restante') {
    nuevoAvance.value.porcentaje = max;
  } else {
    nuevoAvance.value.porcentaje = Math.min(val, max);
  }
};

watch(maxAvancePermitido, (newMax) => {
  if (nuevoAvance.value.porcentaje > newMax) {
    nuevoAvance.value.porcentaje = Math.max(1, newMax);
  }
});

const fetchOtDetail = async () => {
  loading.value = true;
  try {
    const res = await client.get(`/ots/${route.params.id}`);
    if (res.data.status === 'success') {
      ot.value = res.data.data;
    }
  } catch (err) {
    const msg = err.response?.data?.message || 'Error al cargar detalle de OT.';
    showNotification('error', 'Error de Carga', msg);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchOtDetail);

const countEvidencias = (tipo) => {
  if (!ot.value?.evidencias) return 0;
  return ot.value.evidencias.filter(e => e.tipo === tipo).length;
};

const getEvidenciasPorTipo = (tipo) => {
  if (!ot.value?.evidencias) return [];
  return ot.value.evidencias.filter(e => e.tipo === tipo);
};

const pedirConfirmacionBorrarFoto = (evidenciaId) => {
  openConfirm({
    title: 'Eliminar Evidencia Fotográfica',
    subtitle: 'Acción de Borrado',
    message: '¿Está seguro de eliminar esta fotografía de evidencia? Deberá subir una nueva foto si es requerida para el cierre de la OT.',
    confirmText: 'Sí, Eliminar Foto',
    type: 'danger',
    action: () => executeDeletePhoto(evidenciaId)
  });
};

const executeDeletePhoto = async (evidenciaId) => {
  updating.value = true;
  try {
    const res = await client.delete(`/evidencias/${evidenciaId}`);
    if (res.data.status === 'success') {
      showNotification('success', 'Foto Eliminada', 'Se eliminó la evidencia fotográfica con éxito.');
      fetchOtDetail();
    }
  } catch (err) {
    const msg = err.response?.data?.message || 'No se pudo eliminar la evidencia fotográfica.';
    showNotification('error', 'Error al Eliminar Foto', msg);
  } finally {
    updating.value = false;
  }
};


const isPreventivoPlanta = computed(() => {
  return !isCorrectivo.value && !isPreventivoAire.value;
});

// Reglas Transversales Computadas
const tieneLlegadaOk = computed(() => {
  const f = Boolean(
    otFormularioData.value?.llegada_foto || 
    otFormularioData.value?.llegada_sitio || 
    otFormularioData.value?.llegada_tecnico_sitio ||
    otFormularioData.value?.llegada_carnet_sitio ||
    countEvidencias('llegada_sitio') > 0 ||
    countEvidencias('llegada') > 0
  );
  const c = Boolean(otFormularioData.value?.llegada_carnet || countEvidencias('llegada_carnet') > 0 || countEvidencias('carnet') > 0);
  const e = Boolean(otFormularioData.value?.llegada_estacion || countEvidencias('llegada_estacion') > 0 || countEvidencias('estacion') > 0);
  return f || (c && e);
});

const tieneTransporteOk = computed(() => {
  const tr = otFormularioData.value?.transportes_especiales || [];
  return (Array.isArray(tr) && tr.length > 0 && tr.some(t => Boolean(t.foto))) || countEvidencias('transporte') > 0;
});

const tieneRepuestosOk = computed(() => {
  const rc = otFormularioData.value?.repuestos_cambios || [];
  if (!Array.isArray(rc) || rc.length === 0) return true;
  return rc.every(r => (!r.item_retirado && !r.item_instalado) || (Boolean(r.foto_retirado) && Boolean(r.foto_instalado)));
});

const tieneInsumosOk = computed(() => {
  const ins = otFormularioData.value?.insumos_menores || [];
  if (!Array.isArray(ins) || ins.length === 0) return true;
  return ins.every(i => !i.nombre_item || (Boolean(i.foto_antes) && Boolean(i.foto_despues)));
});

const tieneHallazgosOk = computed(() => {
  const h = otFormularioData.value?.hallazgos || [];
  if (!Array.isArray(h) || h.length === 0) return true;
  return h.every(item => (!item.descripcion && !item.sistema) || Boolean(item.foto));
});

const requisitosFaltantes = computed(() => {
  if (!ot.value) return [];
  const faltantes = [];

  // 1. REGLA OBLIGATORIA: Foto llegada a sitio (Técnico con carnet y sitio atrás)
  if (!tieneLlegadaOk.value) {
    faltantes.push('Falta Foto de Llegada a Sitio (Técnico con carnet y estación al fondo)');
  }

  // 2. REGLA OBLIGATORIA: Registro de Transporte Especial (LPU) con foto
  if (!tieneTransporteOk.value) {
    faltantes.push('Falta Registro Obligatorio de Transporte Especial con Foto Soporte');
  }

  // 3. REGLA: Fotos en repuestos cambiados si existen
  if (!tieneRepuestosOk.value) {
    faltantes.push('Hay repuestos cambiados pendientes de foto retirada o instalada');
  }

  // 4. REGLA: Fotos antes y después en insumos menores si existen
  if (!tieneInsumosOk.value) {
    faltantes.push('Hay insumos menores pendientes de foto ANTES o DESPUÉS');
  }

  // 5. REGLA: Foto en novedades y hallazgos si existen
  if (!tieneHallazgosOk.value) {
    faltantes.push('Hay novedades o hallazgos pendientes de fotografía soporte');
  }

  // Requisitos específicos según tipo de trabajo
  if (isCorrectivo.value) {
    if (countEvidencias('antes') < 1) {
      faltantes.push('Falta Evidencia Fotográfica de ANTES (Falla encontrada)');
    }
    if (countEvidencias('durante') < 1) {
      faltantes.push('Falta Evidencia Fotográfica de DURANTE (Intervención técnica)');
    }
    if (countEvidencias('despues') < 1) {
      faltantes.push('Falta Evidencia Fotográfica de DESPUÉS (Equipo solucionado)');
    }
  } else if (!isPreventivoAire.value) {
    // Preventivo Planta Eléctrica
    if (countEvidencias('placas') < 1 && countEvidencias('antes') < 1) {
      faltantes.push('Falta Evidencia de Placas Técnicas (Planta, Motor, Generador)');
    }
    if (countEvidencias('inicial') < 1 && countEvidencias('antes') < 1) {
      faltantes.push('Falta Evidencia de Horómetro Inicial & Estado de Caseta');
    }
    if (countEvidencias('mantenimiento') < 1 && countEvidencias('durante') < 1 && countEvidencias('filtracion') < 1) {
      faltantes.push('Falta Evidencia de Servicio de Filtración & Mantenimiento');
    }
    if (countEvidencias('pruebas') < 1 && countEvidencias('despues') < 1) {
      faltantes.push('Falta Evidencia de Pruebas Operativas ATS con Carga (15 min)');
    }
  } else {
    // Preventivo Aire Acondicionado
    if (countEvidencias('placas') < 1 && countEvidencias('antes') < 1) {
      faltantes.push('Falta Evidencia de Placa Técnica & Estado Previo AA');
    }
    if (countEvidencias('mantenimiento') < 1 && countEvidencias('durante') < 1) {
      faltantes.push('Falta Evidencia de Lavado & Mantenimiento de Serpentines');
    }
    if (countEvidencias('pruebas') < 1 && countEvidencias('despues') < 1) {
      faltantes.push('Falta Evidencia de Mediciones Operativas y Presiones');
    }
  }

  if (!ot.value.avances || ot.value.avances.length === 0) {
    faltantes.push('Falta Registro de Bitácora / Avance PDT de la intervención');
  }

  return faltantes;
});

const canCloseOt = computed(() => {
  return requisitosFaltantes.value.length === 0;
});

const pedirConfirmacionDesplazamiento = () => {
  openConfirm({
    title: 'Iniciar Desplazamiento',
    subtitle: 'Acción de Campo',
    message: '¿Está seguro de iniciar el desplazamiento hacia el sitio? La OT cambiará a estado "En Camino".',
    confirmText: 'Sí, Iniciar Desplazamiento',
    type: 'warning',
    action: () => cambiarEstado('en_camino')
  });
};

const pedirConfirmacionLlegada = () => {
  isLlegadaModalOpen.value = true;
};

const handleFotoLlegadaChange = async (data) => {
  if (data && typeof data === 'object') {
    if (data.gps) {
      otFormularioData.value.gps_llegada = data.gps;
      if (typeof data.gps === 'string' && data.gps.includes(',')) {
        const parts = data.gps.split(',');
        const lat = parseFloat(parts[0].trim());
        const lng = parseFloat(parts[1].trim());
        if (!isNaN(lat) && !isNaN(lng)) {
          otFormularioData.value.llegada_lat = lat;
          otFormularioData.value.llegada_lng = lng;
        }
      }
    }
    if (data.fecha) {
      otFormularioData.value.fecha_hora_texto_llegada = data.fecha;
      otFormularioData.value.llegada_fecha = data.fecha;
    }
    otFormularioData.value.fecha_llegada = new Date().toISOString();
    if (data.imagen_base64 && ot.value?.id) {
      try {
        await client.post(`/ots/${ot.value.id}/evidencia`, {
          tipo: 'llegada_sitio',
          imagen_base64: data.imagen_base64,
          latitud: otFormularioData.value.llegada_lat,
          longitud: otFormularioData.value.llegada_lng,
        });
      } catch (e) {
        console.warn('Evidencia de llegada subida:', e);
      }
    }
  }
};

const handleConfirmarLlegada = async (data) => {
  updating.value = true;
  try {
    const foto = data.foto_llegada || data.foto_carnet;
    otFormularioData.value.llegada_foto = foto;
    otFormularioData.value.llegada_sitio = foto;
    otFormularioData.value.llegada_carnet = foto;
    otFormularioData.value.llegada_estacion = foto;
    otFormularioData.value.fecha_llegada = data.timestamp;
    otFormularioData.value.fecha_hora_texto_llegada = data.fecha_hora_texto;
    otFormularioData.value.gps_llegada = data.gps;

    // Subir foto como evidencia formal
    try {
      await client.post(`/ots/${ot.value.id}/evidencia`, {
        tipo: 'llegada_sitio',
        imagen_base64: foto,
      });
    } catch (e) {
      console.warn('Evidencia subida en formulario:', e);
    }

    // Guardar formulario actualizado
    await client.put(`/ots/${ot.value.id}/formulario`, {
      datos_formulario: otFormularioData.value
    });

    // Cambiar estado a 'en_sitio'
    await cambiarEstado('en_sitio');

    isLlegadaModalOpen.value = false;
    showNotification('success', 'Llegada Registrada', 'Foto del técnico con carnet y sitio al fondo guardada con éxito.');
    fetchOtDetail();
  } catch (err) {
    const msg = err.response?.data?.message || 'Error al registrar llegada a sitio.';
    showNotification('error', 'Error', msg);
  } finally {
    updating.value = false;
  }
};

const cambiarEstado = async (nuevoEstado) => {
  updating.value = true;
  try {
    const res = await client.put(`/ots/${ot.value.id}/estado`, { estado: nuevoEstado });
    if (res.data.status === 'success') {
      ot.value.estado = nuevoEstado;
      showNotification('success', 'Estado Actualizado', `La OT cambió a estado "${formatEstado(nuevoEstado)}".`);
      fetchOtDetail();
    }
  } catch (err) {
    const msg = err.response?.data?.message || 'No se pudo actualizar el estado de la OT.';
    showNotification('error', 'Error al Cambiar Estado', msg);
  } finally {
    updating.value = false;
  }
};

const etapasFlujo = [
  { key: 'asignada', label: 'Asignada', desc: 'En central' },
  { key: 'en_camino', label: 'En Camino', desc: 'Traslado' },
  { key: 'en_sitio', label: 'En Sitio', desc: 'Arribo a torre' },
  { key: 'en_progreso', label: 'En Ejecución', desc: 'Intervención' },
  { key: 'solucionada', label: 'Solucionada', desc: 'Cierre técnico' },
];

const getEtapaIndex = (st) => {
  if (st === 'detenida_materiales') return 3;
  if (st === 'finalizada') return 4;
  const idx = etapasFlujo.findIndex(e => e.key === st);
  return idx >= 0 ? idx : 0;
};

const pedirConfirmacionIniciarTrabajos = () => {
  openConfirm({
    title: 'Iniciar Ejecución Técnica',
    subtitle: 'Comienzo de Labores en Sitio',
    message: '¿Confirmar inicio de la intervención técnica en sitio? La orden cambiará a estado "En Progreso" y se habilitará el reporte de bitácora y checklist.',
    confirmText: 'Sí, Iniciar Trabajos',
    type: 'success',
    action: () => cambiarEstado('en_progreso')
  });
};

const pedirConfirmacionPausarMateriales = () => {
  openConfirm({
    title: 'Pausar por Materiales',
    subtitle: 'Espera de Suministros LPU',
    message: '¿Desea marcar la orden como "Detenida por Materiales"? Utilice esta opción si la intervención no puede continuar temporalmente por falta de repuestos o insumos.',
    confirmText: 'Sí, Pausar OT',
    type: 'warning',
    action: () => cambiarEstado('detenida_materiales')
  });
};

const pedirConfirmacionReanudar = () => {
  openConfirm({
    title: 'Reanudar Intervención',
    subtitle: 'Reinicio de Labores',
    message: '¿Reanudar la ejecución técnica en sitio? La orden volverá a estado "En Progreso".',
    confirmText: 'Sí, Reanudar',
    type: 'success',
    action: () => cambiarEstado('en_progreso')
  });
};

const abrirUbicacionMaps = () => {
  if (!ot.value?.ubicacion) return;
  const query = encodeURIComponent(ot.value.ubicacion);
  window.open(`https://www.google.com/maps/search/?api=1&query=${query}`, '_blank');
};

const tipoMantenimientoLabel = (t) => {
  const map = {
    preventivo: 'Preventivo',
    correctivo: 'Correctivo',
    emergencia: 'Emergencia Crítica',
  };
  return map[t] || t || 'Mantenimiento';
};

const tipoMantenimientoBadgeClass = (t) => {
  if (t === 'emergencia') return 'bg-red-100 text-red-700 dark:bg-red-950/80 dark:text-red-300 border border-red-200 dark:border-red-900/60';
  if (t === 'correctivo') return 'bg-amber-100 text-amber-700 dark:bg-amber-950/80 dark:text-amber-300 border border-amber-200 dark:border-amber-900/60';
  return 'bg-blue-100 text-blue-700 dark:bg-blue-950/80 dark:text-blue-300 border border-blue-200 dark:border-blue-900/60';
};

const pedirConfirmacionAvance = () => {
  if (!isAvanceValido.value) return;
  const actual = Number(ot.value?.progreso) || 0;
  const inc = Number(nuevoAvance.value.porcentaje) || 0;
  const nuevoTotal = Math.min(100, actual + inc);
  
  openConfirm({
    title: 'Publicar Avance en Bitácora',
    subtitle: 'Minutograma PDT Telecom',
    message: `¿Desea registrar el avance de +${inc}%?\nEl progreso acumulado de la OT pasará de ${actual}% al ${nuevoTotal}%.\n\nDescripción: "${nuevoAvance.value.descripcion.trim()}"`,
    confirmText: 'Sí, Registrar Avance',
    type: 'info',
    action: () => executeSubmitAvance()
  });
};

const executeSubmitAvance = async () => {
  updating.value = true;
  try {
    const res = await client.post('/avances', {
      ot_id: ot.value.id,
      descripcion: nuevoAvance.value.descripcion.trim(),
      porcentaje: Number(nuevoAvance.value.porcentaje),
      fecha_reporte: new Date().toLocaleDateString('en-CA'),
    });
    if (res.data.status === 'success') {
      nuevoAvance.value.descripcion = '';
      showNotification('success', 'Avance Registrado', 'Se publicó el avance en la bitácora PDT correctamente.');
      await fetchOtDetail();
      nuevoAvance.value.porcentaje = Math.min(10, maxAvancePermitido.value);
    }
  } catch (err) {
    const msg = err.response?.data?.message || err.response?.data?.error || 'No se pudo registrar el avance.';
    showNotification('error', 'Error al Publicar Avance', msg);
  } finally {
    updating.value = false;
  }
};

const pedirConfirmacionFoto = (payload) => {
  openConfirm({
    title: 'Guardar Evidencia Fotográfica',
    subtitle: `Evidencia ${payload.tipo.toUpperCase()}`,
    message: `¿Desea subir y guardar esta fotografía como evidencia de ${payload.tipo.toUpperCase()} con marca de agua GPS incrustada?`,
    confirmText: 'Sí, Guardar Foto',
    type: 'success',
    action: () => executeUploadPhoto(payload)
  });
};

const executeUploadPhoto = async (payload) => {
  updating.value = true;
  try {
    const res = await client.post(`/ots/${ot.value.id}/evidencia`, payload);
    if (res.data.status === 'success') {
      showNotification('success', 'Evidencia Cargada', `Se guardó la foto de ${payload.tipo.toUpperCase()} con éxito.`);
      fetchOtDetail();
    }
  } catch (err) {
    const msg = err.response?.data?.message || 'No se pudo subir la fotografía de evidencia.';
    showNotification('error', 'Error al Guardar Foto', msg);
  } finally {
    updating.value = false;
  }
};

const pedirConfirmacionCierre = (payload) => {
  openConfirm({
    title: 'Finalizar y Solucionar OT',
    subtitle: `Cierre Técnico de la Orden ${ot.value?.codigo || ''}`,
    message: `¿Está seguro de confirmar y finalizar técnicamente esta Orden de Trabajo? La orden cambiará a estado Solucionada y no podrá ser editada por el técnico.`,
    confirmText: 'Sí, Cerrar OT',
    type: 'danger',
    action: () => executeHandleCierreSubmit(payload)
  });
};

const executeHandleCierreSubmit = async (payload) => {
  cierreErrorMsg.value = '';
  updating.value = true;
  try {
    const finalPayload = {
      ...payload,
      datos_formulario: otFormularioData.value
    };
    const res = await client.post(`/ots/${ot.value.id}/cerrar`, finalPayload);
    if (res.data.status === 'success') {
      isCloseModalOpen.value = false;
      showNotification('success', 'Orden Solucionada', res.data.message || 'La Orden de Trabajo fue finalizada con éxito.');
      fetchOtDetail();
    }
  } catch (err) {
    const msg = err.response?.data?.message || err.response?.data?.error || 'No se pudo cerrar la OT.';
    cierreErrorMsg.value = msg;
    showNotification('error', 'Error de Validación / Cierre', msg);
  } finally {
    updating.value = false;
  }
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return d.toLocaleDateString('es-CO', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' });
};

const formatEstado = (st) => {
  const map = {
    asignada: 'Asignada',
    en_camino: 'En Camino',
    en_sitio: 'En Sitio',
    en_progreso: 'En Progreso',
    detenida_materiales: 'Detenida por Materiales',
    solucionada: 'Solucionada',
    finalizada: 'Finalizada',
  };
  return map[st] || st;
};

const estadoBadgeClass = (st) => {
  if (st === 'solucionada' || st === 'finalizada') return 'bg-emerald-100 text-emerald-800 border border-emerald-200 dark:bg-emerald-950/80 dark:text-emerald-400 dark:border-emerald-500/40';
  if (st === 'en_camino' || st === 'en_sitio') return 'bg-amber-100 text-amber-800 border border-amber-200 dark:bg-amber-950/80 dark:text-amber-300 dark:border-amber-500/40';
  return 'bg-red-100 text-red-800 border border-red-200 dark:bg-red-950/80 dark:text-red-300 dark:border-red-500/40';
};
</script>



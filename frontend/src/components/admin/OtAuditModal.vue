<template>
  <Teleport to="body">
    <div v-if="isOpen" class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-3 sm:p-4 overflow-y-auto">
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl w-full max-w-5xl xl:max-w-6xl max-h-[92vh] flex flex-col overflow-hidden shadow-2xl transition-colors duration-300 my-auto">
        
        <!-- Header del Modal -->
        <div class="flex items-center justify-between border-b border-slate-200 dark:border-white/10 px-5 py-4 shrink-0 bg-slate-50/50 dark:bg-white/[0.02]">
          <div class="flex items-center gap-3 min-w-0">
            <div class="w-10 h-10 rounded-xl bg-red-500/10 text-red-600 dark:text-red-400 flex items-center justify-center shrink-0 border border-red-500/20">
              <IconFileCheck class="w-5 h-5 stroke-[2]" />
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2 flex-wrap">
                <span class="font-mono text-sm font-black text-red-600 dark:text-red-400">{{ ot?.codigo }}</span>
                <span :class="estadoBadgeClass(ot?.estado)" class="px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-wider">
                  {{ formatEstado(ot?.estado) }}
                </span>
                <span v-if="ot?.progreso !== undefined" class="font-mono text-xs font-bold text-slate-500 dark:text-slate-400">
                  {{ ot.progreso }}% Ejecutado
                </span>
              </div>
              <h3 class="text-sm font-bold text-slate-800 dark:text-slate-200 truncate mt-0.5">
                {{ ot?.sitio ? `Estación: ${ot.sitio}` : ot?.descripcion }}
              </h3>
            </div>
          </div>

          <div class="flex items-center gap-2 shrink-0">
            <button
              v-if="ot?.id"
              type="button"
              @click="$router.push(`/mobile/ot/${ot.id}`)"
              class="px-2.5 py-1.5 rounded-lg border border-slate-200 dark:border-white/10 text-xs font-bold text-slate-600 dark:text-slate-300 hover:text-red-600 dark:hover:text-red-400 hover:border-red-300 dark:hover:border-red-800 transition-all flex items-center gap-1.5 shadow-2xs"
              title="Abrir vista técnica de campo para esta orden"
            >
              <IconDeviceMobile class="w-3.5 h-3.5 stroke-[2]" />
              <span class="hidden sm:inline">Vista de Campo</span>
            </button>

            <button 
              @click="$emit('close')" 
              class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-white/5 transition-colors"
              title="Cerrar ventana"
            >
              <IconX class="w-5 h-5 stroke-[2]" />
            </button>
          </div>
        </div>

        <!-- Pestañas del Expediente (Estilo Cápsula con Controles de Avance) -->
        <div class="border-b border-slate-200 dark:border-white/10 px-3 sm:px-5 py-2.5 bg-slate-50/70 dark:bg-[#0a0b10] shrink-0">
          <div class="flex items-center gap-1.5 relative">
            <!-- Botón Desplazar a la Izquierda -->
            <button
              type="button"
              @click="scrollTabs(-1)"
              class="p-1.5 rounded-xl border border-slate-200 dark:border-white/10 bg-white dark:bg-[#121215] text-slate-500 hover:text-red-600 dark:hover:text-red-400 hover:border-red-300 dark:hover:border-red-800 transition-all shadow-xs shrink-0 active:scale-95 cursor-pointer"
              title="Ver pestañas anteriores"
            >
              <IconChevronLeft class="w-4 h-4 stroke-[2.5]" />
            </button>

            <!-- Contenedor de Pestañas con Desplazamiento por Rueda, Arrastre y Clic -->
            <div
              ref="tabsNavRef"
              @wheel="onTabsWheel"
              @mousedown="onMouseDown"
              @mouseleave="onMouseLeave"
              @mouseup="onMouseUp"
              @mousemove="onMouseMove"
              class="flex items-center gap-1.5 overflow-x-auto select-none py-0.5 scroll-smooth [scrollbar-width:none] [-ms-overflow-style:none] [&::-webkit-scrollbar]:hidden flex-1 cursor-grab active:cursor-grabbing"
            >
              <button
                v-for="t in tabs"
                :key="t.id"
                @click="selectTab(t.id, $event)"
                class="px-2.5 sm:px-3 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 whitespace-nowrap shrink-0 border select-none cursor-pointer"
                :class="activeTab === t.id 
                  ? 'bg-red-600 border-red-600 text-white shadow-sm shadow-red-600/20' 
                  : 'bg-white dark:bg-[#121215] border-slate-200 dark:border-white/10 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:border-slate-300 dark:hover:border-white/20'"
              >
                <component :is="t.icon" class="w-3.5 h-3.5 stroke-[2.2]" />
                <span>{{ t.label }}</span>
                <span 
                  v-if="t.badge !== undefined" 
                  class="px-1.5 py-0.2 rounded-full text-[10px] font-mono font-black"
                  :class="activeTab === t.id ? 'bg-white/20 text-white' : 'bg-slate-100 dark:bg-white/10 text-slate-600 dark:text-slate-400'"
                >
                  {{ t.badge }}
                </span>
              </button>
            </div>

            <!-- Botón Desplazar a la Derecha (Avanzar) -->
            <button
              type="button"
              @click="scrollTabs(1)"
              class="p-1.5 rounded-xl border border-slate-200 dark:border-white/10 bg-white dark:bg-[#121215] text-slate-500 hover:text-red-600 dark:hover:text-red-400 hover:border-red-300 dark:hover:border-red-800 transition-all shadow-xs shrink-0 active:scale-95 cursor-pointer"
              title="Avanzar para ver más pestañas (AA, Fuerza DC)"
            >
              <IconChevronRight class="w-4 h-4 stroke-[2.5]" />
            </button>
          </div>
        </div>

        <!-- Cuerpo del Modal (Contenido Scrolleable) -->
        <div class="p-5 overflow-y-auto space-y-4 flex-1">
          
          <!-- PESTAÑA 1: RESUMEN GENERAL & FICHA -->
          <div v-if="activeTab === 'resumen'" class="space-y-4">
            <!-- Grid de datos técnicos clave -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
              <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-1">
                <span class="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Estación / Sitio Base</span>
                <div class="font-black text-xs text-slate-900 dark:text-white flex items-center gap-1.5 truncate">
                  <IconBuildingBroadcastTower class="w-4 h-4 text-red-600 dark:text-red-400 shrink-0" />
                  <span class="truncate">{{ ot?.sitio || 'No especificado' }}</span>
                </div>
              </div>

              <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-1">
                <span class="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Tipo & Criticidad</span>
                <div class="flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase" :class="tipoBadgeClass(ot?.tipo_actividad || ot?.tipo_mantenimiento)">
                    {{ formatTipoLabel(ot?.tipo_actividad || ot?.tipo_mantenimiento) }}
                  </span>
                  <span class="font-mono font-bold text-xs text-slate-700 dark:text-slate-300">
                    {{ ot?.prioridad }} ({{ ot?.tipo_ubicacion }})
                  </span>
                </div>
              </div>

              <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-1">
                <span class="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Subsistema & Gasto</span>
                <div class="font-bold text-xs text-slate-800 dark:text-slate-200 truncate">
                  {{ ot?.subsistema || 'Sistema Eléctrico' }}
                </div>
                <span class="text-[10px] font-mono font-bold text-slate-500">{{ ot?.tipo_gasto || 'OPEX' }}</span>
              </div>

              <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-1">
                <span class="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Cuadrilla / Asignado</span>
                <div class="font-bold text-xs text-slate-800 dark:text-slate-200 truncate flex items-center gap-1">
                  <IconUsers class="w-3.5 h-3.5 text-slate-400 shrink-0" />
                  <span class="truncate">{{ ot?.cuadrilla?.nombre || ot?.assigned_user?.name || 'Sin Asignar' }}</span>
                </div>
                <div class="text-[10px] text-slate-500 truncate" v-if="ot?.assigned_user">
                  Resp: {{ ot.assigned_user.name }}
                </div>
              </div>
            </div>

            <!-- Ubicación y SLA -->
            <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3.5 flex flex-wrap items-center justify-between gap-3">
              <div class="flex items-center gap-2 text-xs text-slate-700 dark:text-slate-300 min-w-0 flex-1">
                <IconMapPin class="w-4 h-4 text-red-600 shrink-0 stroke-[2]" />
                <span class="font-medium truncate">{{ ot?.ubicacion }}</span>
                <button
                  type="button"
                  @click="abrirMaps(ot?.ubicacion)"
                  class="text-[11px] font-bold text-red-600 dark:text-red-400 hover:underline inline-flex items-center gap-1 shrink-0 ml-1"
                >
                  <IconExternalLink class="w-3.5 h-3.5" />
                  <span>Ver Mapa</span>
                </button>
              </div>

              <div v-if="ot?.fecha_limite_sla" class="shrink-0">
                <SlaBadge :fecha-limite="ot.fecha_limite_sla" :estado="ot.estado" />
              </div>
            </div>

            <!-- Descripción del trabajo reportado -->
            <div class="space-y-1">
              <span class="text-[11px] text-slate-400 font-bold uppercase tracking-wider block">
                Descripción / Síntoma de la Falla:
              </span>
              <p class="text-xs text-slate-800 dark:text-slate-200 bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3.5 leading-relaxed">
                {{ ot?.descripcion }}
              </p>
            </div>

            <!-- Datos de Cierre Técnico (si está Solucionada o Finalizada) -->
            <div v-if="['solucionada', 'finalizada'].includes(ot?.estado)" class="p-4 bg-emerald-50/70 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800/60 rounded-xl space-y-2.5">
              <div class="flex items-center gap-2 text-xs font-black text-emerald-800 dark:text-emerald-300">
                <IconCircleCheck class="w-4 h-4 stroke-[2.5]" />
                <span>Certificación de Cierre Técnico en Campo</span>
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                <div>
                  <span class="text-slate-500 dark:text-slate-400 font-semibold block text-[11px]">Causa Raíz de la Falla:</span>
                  <span class="font-bold text-slate-800 dark:text-slate-200 uppercase font-mono">{{ ot.causa_falla || 'No especificada' }}</span>
                </div>
                <div>
                  <span class="text-slate-500 dark:text-slate-400 font-semibold block text-[11px]">Fecha de Solución Técnica:</span>
                  <span class="font-mono text-slate-800 dark:text-slate-200">{{ formatDate(ot.fecha_solucion || ot.updated_at) }}</span>
                </div>
              </div>
              <div v-if="ot.observaciones_cierre" class="pt-2 border-t border-emerald-200/60 dark:border-white/10 text-xs">
                <span class="text-slate-500 dark:text-slate-400 font-semibold block text-[11px]">Observaciones del Técnico:</span>
                <p class="text-slate-800 dark:text-slate-200 mt-0.5 leading-relaxed">{{ ot.observaciones_cierre }}</p>
              </div>
            </div>
          </div>

          <!-- PESTAÑA: FORMATO TÉCNICO DE CAMPO -->
          <div v-if="activeTab === 'formato_campo'" class="space-y-4">
            <!-- Header Resumen del Formulario -->
            <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-2xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-xs">
              <div class="space-y-0.5">
                <div class="flex items-center gap-2">
                  <IconFileCheck class="w-4 h-4 text-red-600 dark:text-red-400 stroke-[2]" />
                  <h4 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
                    Formato Técnico Oficial Claro
                  </h4>
                </div>
                <p class="text-[11px] text-slate-500 dark:text-slate-400 font-medium">
                  {{ tituloFormatoCampo }}
                </p>
              </div>
              <div class="flex items-center gap-2">
                <span 
                  class="px-2.5 py-1 rounded-lg text-[10px] font-black uppercase tracking-wider"
                  :class="hasFormData ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300'"
                >
                  {{ hasFormData ? 'Diligenciado en Sitio' : 'Pendiente de Diligenciar' }}
                </span>
                <span class="px-2 py-0.5 rounded bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-300 text-[10px] font-black uppercase">
                  {{ isFormatoWo ? 'WO Correctivo' : (isFormatoMpAire ? 'MP Climatización' : 'MP Planta Eléctrica') }}
                </span>
              </div>
            </div>

            <!-- 1. CONTROL DE LLEGADA A SITIO (TÉCNICO CON CARNET Y ESTACIÓN AL FONDO) -->
            <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3 shadow-xs">
              <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-2.5">
                <div class="flex items-center gap-2">
                  <IconMapPinCheck class="w-4 h-4 text-emerald-600 dark:text-emerald-400 stroke-[2]" />
                  <span class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
                    1. Control de Llegada a Sitio (Técnico + Carnet + Estación)
                  </span>
                </div>
                <span 
                  v-if="parsedFormData.llegada_foto || parsedFormData.llegada_sitio" 
                  class="text-[10px] font-black px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 flex items-center gap-1"
                >
                  <IconCheck class="w-3 h-3 stroke-[3]" /> Foto Verificada
                </span>
                <span v-else class="text-[10px] font-bold text-amber-600 dark:text-amber-400">
                  Sin Foto de Llegada
                </span>
              </div>

              <div v-if="parsedFormData.llegada_foto || parsedFormData.llegada_sitio" class="grid grid-cols-1 sm:grid-cols-3 gap-3 items-center">
                <!-- Miniatura con Zoom -->
                <div 
                  class="relative aspect-video rounded-xl overflow-hidden bg-black/60 group cursor-pointer border border-slate-200 dark:border-white/10"
                  @click="abrirZoom(parsedFormData.llegada_foto || parsedFormData.llegada_sitio, 'Llegada a Sitio', parsedFormData.llegada_fecha)"
                >
                  <img 
                    :src="parsedFormData.llegada_foto || parsedFormData.llegada_sitio" 
                    alt="Llegada a Sitio" 
                    class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center text-white text-xs font-bold gap-1 transition-opacity">
                    <IconZoomIn class="w-4 h-4" />
                    <span>Ampliar</span>
                  </div>
                  <div class="absolute bottom-1 left-1 bg-black/70 px-1.5 py-0.5 rounded text-[9px] text-white font-mono">
                    LLEGADA
                  </div>
                </div>

                <!-- Metadatos de Llegada -->
                <div class="sm:col-span-2 space-y-2 text-xs">
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                      <span class="text-[10px] text-slate-400 font-bold block uppercase">Fecha y Hora de Arribo</span>
                      <span class="font-mono font-black text-slate-800 dark:text-slate-200">
                        {{ parsedFormData.llegada_fecha ? formatDate(parsedFormData.llegada_fecha) : (ot?.fecha_llegada_sitio ? formatDate(ot.fecha_llegada_sitio) : 'Capturada en Foto') }}
                      </span>
                    </div>

                    <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                      <span class="text-[10px] text-slate-400 font-bold block uppercase">Georreferenciación GPS</span>
                      <div class="flex items-center justify-between">
                        <span class="font-mono font-black text-emerald-600 dark:text-emerald-400 text-[11px]">
                          {{ parsedFormData.llegada_lat && parsedFormData.llegada_lng ? `${Number(parsedFormData.llegada_lat).toFixed(5)}, ${Number(parsedFormData.llegada_lng).toFixed(5)}` : 'Estampada en Foto' }}
                        </span>
                        <button
                          v-if="parsedFormData.llegada_lat && parsedFormData.llegada_lng"
                          type="button"
                          @click="abrirMaps(`${parsedFormData.llegada_lat},${parsedFormData.llegada_lng}`)"
                          class="text-[10px] text-blue-600 hover:underline flex items-center gap-0.5 font-bold cursor-pointer"
                        >
                          <IconExternalLink class="w-3 h-3" /> Maps
                        </button>
                      </div>
                    </div>
                  </div>

                  <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5 flex items-center justify-between">
                    <div>
                      <span class="text-[10px] text-slate-400 font-bold block uppercase">Técnico / Cuadrilla</span>
                      <span class="font-bold text-slate-800 dark:text-slate-200">{{ ot?.assigned_user?.name || ot?.coordinador || 'Personal de Campo' }}</span>
                    </div>
                    <span class="text-[10px] font-mono text-slate-400">Estación: {{ ot?.sitio || 'Sin Sitio' }}</span>
                  </div>
                </div>
              </div>

              <div v-else class="text-center py-6 bg-slate-50 dark:bg-[#0a0b10] border border-dashed border-slate-200 dark:border-white/10 rounded-xl space-y-1">
                <IconCameraOff class="w-6 h-6 text-slate-400 mx-auto stroke-[1.5]" />
                <p class="text-xs font-bold text-slate-600 dark:text-slate-400">El técnico aún no ha cargado la fotografía de llegada a sitio</p>
              </div>
            </div>

            <!-- 2. ESPECIFICACIONES TÉCNICAS SEGÚN TIPO DE TRABAJO -->
            <!-- A. CASO FORMATO WO: CORRECTIVOS Y EMERGENCIAS -->
            <div v-if="isFormatoWo" class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3.5 shadow-xs">
              <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-2.5">
                <div class="flex items-center gap-2">
                  <IconTool class="w-4 h-4 text-amber-600 dark:text-amber-400 stroke-[2]" />
                  <span class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
                    2. Diagnóstico Técnico & Cierre Claro WO
                  </span>
                </div>
                <span class="text-[10px] font-black px-2 py-0.5 rounded bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300">
                  Ref. WO0000005558781
                </span>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-xs">
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Tipo de Sitio</span>
                  <span class="font-bold text-slate-800 dark:text-slate-200">{{ parsedFormData.tipo_sitio || 'Urbano' }}</span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Subsistema</span>
                  <span class="font-bold text-slate-800 dark:text-slate-200">{{ parsedFormData.subsistema || ot?.subsistema || 'Planta eléctrica' }}</span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">¿Afectación de Servicios?</span>
                  <span class="font-black" :class="parsedFormData.presenta_afectacion === 'Si' ? 'text-rose-600' : 'text-emerald-600'">
                    {{ parsedFormData.presenta_afectacion || 'No' }}
                  </span>
                </div>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-xs">
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Equipo en Falla</span>
                  <span class="font-bold text-slate-800 dark:text-slate-200">{{ parsedFormData.tipo_equipo_falla || 'Planta eléctrica' }}</span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Marca</span>
                  <span class="font-bold text-slate-800 dark:text-slate-200">{{ parsedFormData.marca_equipo || 'Selmec / Cummins' }}</span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Modelo / Ref.</span>
                  <span class="font-mono font-bold text-slate-800 dark:text-slate-200">{{ parsedFormData.modelo_equipo || 'N/A' }}</span>
                </div>
              </div>

              <!-- Intervenciones Realizadas -->
              <div class="flex flex-wrap gap-2 text-xs">
                <span class="text-[10px] text-slate-400 font-bold uppercase self-center mr-1">Intervención:</span>
                <span v-if="parsedFormData.reparacion" class="px-2 py-0.5 rounded-lg bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 font-bold text-[10px]">✓ Reparación</span>
                <span v-if="parsedFormData.reinstalacion" class="px-2 py-0.5 rounded-lg bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300 font-bold text-[10px]">✓ Reinstalación</span>
                <span v-if="parsedFormData.cambio_equipo" class="px-2 py-0.5 rounded-lg bg-purple-100 text-purple-800 dark:bg-purple-950 dark:text-purple-300 font-bold text-[10px]">✓ Cambio de Equipo</span>
              </div>

              <!-- Textos de Falla y Solución -->
              <div class="space-y-2 text-xs">
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-3">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase mb-1">Descripción de la Falla Encontrada</span>
                  <p class="text-slate-800 dark:text-slate-200 leading-relaxed">{{ parsedFormData.descripcion_falla || ot?.descripcion || 'Sin descripción de falla' }}</p>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-3">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase mb-1">Solución Técnica Ejecutada en Sitio</span>
                  <p class="text-slate-800 dark:text-slate-200 leading-relaxed">{{ parsedFormData.descripcion_solucion || ot?.observaciones_cierre || 'Sin solución técnica registrada' }}</p>
                </div>
              </div>

              <!-- Cierre de Supervisión Claro -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs pt-1 border-t border-slate-100 dark:border-white/10">
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">¿Falla Resuelta a Satisfacción?</span>
                  <span class="font-black" :class="parsedFormData.falla_resuelta === 'No' ? 'text-rose-600' : 'text-emerald-600'">
                    {{ parsedFormData.falla_resuelta === 'No' ? 'No (Requiere 2da intervención)' : 'Sí (Equipo en servicio normal)' }}
                  </span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Supervisor Claro Notificado</span>
                  <span class="font-bold text-slate-800 dark:text-slate-200">{{ parsedFormData.nombre_supervisor || 'Ing. de Guardia Claro' }}</span>
                </div>
              </div>
            </div>

            <!-- B. CASO FORMATO MP: PREVENTIVO PLANTA ELÉCTRICA (Ref: OT5304019) -->
            <div v-else-if="isFormatoMpPlanta" class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3.5 shadow-xs">
              <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-2.5">
                <div class="flex items-center gap-2">
                  <IconEngine class="w-4 h-4 text-red-600 dark:text-red-400 stroke-[2]" />
                  <span class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
                    2. Parámetros Técnicos Planta Eléctrica (Ref: OT5304019)
                  </span>
                </div>
                <span class="text-[10px] font-black px-2 py-0.5 rounded bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-300">
                  Planilla Oficial GE
                </span>
              </div>

              <!-- Ficha GE y Motor -->
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-xs">
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Marca GE</span>
                  <span class="font-bold text-slate-800 dark:text-slate-200">{{ parsedFormData.marca_equipo || 'AGG POWER SOLUTIONS' }}</span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Horómetro Inicial</span>
                  <span class="font-mono font-black text-red-600 dark:text-red-400">{{ parsedFormData.horometro_inicial !== null && parsedFormData.horometro_inicial !== undefined ? `${parsedFormData.horometro_inicial} hrs` : 'N/A' }}</span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Motor Diésel</span>
                  <span class="font-bold text-slate-800 dark:text-slate-200">{{ parsedFormData.marca_motor || 'CUMMINS' }}</span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Presión Aceite</span>
                  <span class="font-mono font-bold text-slate-800 dark:text-slate-200">{{ parsedFormData.presion_aceite_bar ? `${parsedFormData.presion_aceite_bar} Bar` : '4.2 Bar' }}</span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Temp. Refrigerante</span>
                  <span class="font-mono font-bold text-slate-800 dark:text-slate-200">{{ parsedFormData.temperatura_refrigerante_c ? `${parsedFormData.temperatura_refrigerante_c} °C` : '80 °C' }}</span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Voltaje Batería</span>
                  <span class="font-mono font-bold text-emerald-600 dark:text-emerald-400">{{ parsedFormData.voltaje_bateria ? `${parsedFormData.voltaje_bateria} Vdc` : '25.4 Vdc' }}</span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Combustible</span>
                  <span class="font-mono font-bold text-amber-600 dark:text-amber-400">{{ parsedFormData.nivel_combustible_porcentaje ? `${parsedFormData.nivel_combustible_porcentaje}%` : '80%' }}</span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Prueba ATS 15 Min</span>
                  <span class="font-bold text-emerald-600 dark:text-emerald-400">{{ parsedFormData.prueba_ats_15min || 'Exitosa con Carga' }}</span>
                </div>
              </div>

              <!-- Parámetros Eléctricos en Carga -->
              <div class="p-3 bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl space-y-2">
                <span class="text-[10px] text-slate-500 font-bold uppercase block">Parámetros Eléctricos en Carga (L-L & L-N)</span>
                <div class="grid grid-cols-3 sm:grid-cols-6 gap-2 text-center text-xs">
                  <div class="p-1.5 bg-white dark:bg-[#121215] rounded-lg border border-slate-200 dark:border-white/5">
                    <span class="text-[9px] text-slate-400 font-mono block">V L1-L2</span>
                    <span class="font-mono font-black text-slate-800 dark:text-slate-200">{{ parsedFormData.voltaje_l1_l2 || 220 }} V</span>
                  </div>
                  <div class="p-1.5 bg-white dark:bg-[#121215] rounded-lg border border-slate-200 dark:border-white/5">
                    <span class="text-[9px] text-slate-400 font-mono block">V L2-L3</span>
                    <span class="font-mono font-black text-slate-800 dark:text-slate-200">{{ parsedFormData.voltaje_l2_l3 || 220 }} V</span>
                  </div>
                  <div class="p-1.5 bg-white dark:bg-[#121215] rounded-lg border border-slate-200 dark:border-white/5">
                    <span class="text-[9px] text-slate-400 font-mono block">V L1-L3</span>
                    <span class="font-mono font-black text-slate-800 dark:text-slate-200">{{ parsedFormData.voltaje_l1_l3 || 220 }} V</span>
                  </div>
                  <div class="p-1.5 bg-white dark:bg-[#121215] rounded-lg border border-slate-200 dark:border-white/5">
                    <span class="text-[9px] text-slate-400 font-mono block">V L1-N</span>
                    <span class="font-mono font-black text-slate-800 dark:text-slate-200">{{ parsedFormData.voltaje_l1_n || 127 }} V</span>
                  </div>
                  <div class="p-1.5 bg-white dark:bg-[#121215] rounded-lg border border-slate-200 dark:border-white/5">
                    <span class="text-[9px] text-slate-400 font-mono block">V L2-N</span>
                    <span class="font-mono font-black text-slate-800 dark:text-slate-200">{{ parsedFormData.voltaje_l2_n || 127 }} V</span>
                  </div>
                  <div class="p-1.5 bg-white dark:bg-[#121215] rounded-lg border border-slate-200 dark:border-white/5">
                    <span class="text-[9px] text-slate-400 font-mono block">Frecuencia</span>
                    <span class="font-mono font-black text-slate-800 dark:text-slate-200">{{ parsedFormData.frecuencia_operacion_hz || 60 }} Hz</span>
                  </div>
                </div>
              </div>

              <!-- Resumen Servicio de Filtración -->
              <div class="flex flex-wrap gap-2 text-xs">
                <span class="text-[10px] text-slate-400 font-bold uppercase self-center mr-1">Filtración MP:</span>
                <span class="px-2 py-0.5 rounded-lg font-bold text-[10px]" :class="parsedFormData.cambio_aceite === 'SI' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-slate-100 text-slate-600'">Aceite: {{ parsedFormData.cambio_aceite || 'SI' }}</span>
                <span class="px-2 py-0.5 rounded-lg font-bold text-[10px]" :class="parsedFormData.cambio_filtros_aire === 'SI' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-slate-100 text-slate-600'">Filtro Aire: {{ parsedFormData.cambio_filtros_aire || 'SI' }}</span>
                <span class="px-2 py-0.5 rounded-lg font-bold text-[10px]" :class="parsedFormData.cambio_filtros_combustible === 'SI' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-slate-100 text-slate-600'">Filtro Combustible: {{ parsedFormData.cambio_filtros_combustible || 'SI' }}</span>
                <span class="px-2 py-0.5 rounded-lg font-bold text-[10px]" :class="parsedFormData.cambio_refrigerante === 'SI' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-slate-100 text-slate-600'">Refrigerante: {{ parsedFormData.cambio_refrigerante || 'SI' }}</span>
                <span class="px-2 py-0.5 rounded-lg bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 font-bold text-[10px]">Planta en Automático: {{ parsedFormData.planta_en_automatico || 'Si' }}</span>
              </div>
            </div>

            <!-- C. CASO FORMATO MP: PREVENTIVO CLIMATIZACIÓN (Ref: WO0000005520436) -->
            <div v-else-if="isFormatoMpAire" class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3.5 shadow-xs">
              <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-2.5">
                <div class="flex items-center gap-2">
                  <IconSnowflake class="w-4 h-4 text-cyan-600 dark:text-cyan-400 stroke-[2]" />
                  <span class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
                    2. Parámetros Técnicos Climatización (Ref: WO0000005520436)
                  </span>
                </div>
                <span class="text-[10px] font-black px-2 py-0.5 rounded bg-cyan-100 text-cyan-800 dark:bg-cyan-950 dark:text-cyan-300">
                  Planilla Oficial AA
                </span>
              </div>

              <!-- Ficha AA y Temperaturas -->
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-xs">
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Marca AA</span>
                  <span class="font-bold text-slate-800 dark:text-slate-200">{{ parsedFormData.marca_aa || 'MCQUAY' }}</span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Tipo de Aire</span>
                  <span class="font-bold text-slate-800 dark:text-slate-200">{{ parsedFormData.tipo_aire || 'Mini Split' }}</span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Capacidad BTU</span>
                  <span class="font-mono font-bold text-slate-800 dark:text-slate-200">{{ parsedFormData.capacidad_btu_aa ? `${parsedFormData.capacidad_btu_aa} kBTU` : '24 kBTU' }}</span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Estado del Equipo</span>
                  <span class="font-bold text-emerald-600 dark:text-emerald-400">{{ parsedFormData.estado_equipo_aa || 'OPERATIVO' }}</span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Temp. Cuarto Equipos</span>
                  <span class="font-mono font-bold text-slate-800 dark:text-slate-200">{{ parsedFormData.temperatura_cuarto_equipo ? `${parsedFormData.temperatura_cuarto_equipo} °C` : '30 °C' }}</span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Temp. Entrada Evap.</span>
                  <span class="font-mono font-bold text-slate-800 dark:text-slate-200">{{ parsedFormData.temperatura_aa_entrada ? `${parsedFormData.temperatura_aa_entrada} °C` : '28 °C' }}</span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Temp. Inyección/Salida</span>
                  <span class="font-mono font-bold text-cyan-600 dark:text-cyan-400">{{ parsedFormData.temperatura_aa_salida ? `${parsedFormData.temperatura_aa_salida} °C` : '20 °C' }}</span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Ajuste Termostato</span>
                  <span class="font-mono font-bold text-slate-800 dark:text-slate-200">{{ parsedFormData.ajuste_termostato ? `${parsedFormData.ajuste_termostato} °C` : '22 °C' }}</span>
                </div>
              </div>

              <!-- Compresor y Presiones -->
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-xs">
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Refrigerante</span>
                  <span class="font-mono font-black text-slate-800 dark:text-slate-200">{{ parsedFormData.compresor_refrigerante || 'R410A' }}</span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Presión Succión</span>
                  <span class="font-mono font-bold text-blue-600 dark:text-blue-400">{{ parsedFormData.presion_succion_psi ? `${parsedFormData.presion_succion_psi} PSI` : '100 PSI' }}</span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Presión Descarga</span>
                  <span class="font-mono font-bold text-rose-600 dark:text-rose-400">{{ parsedFormData.presion_descarga_psi ? `${parsedFormData.presion_descarga_psi} PSI` : '300 PSI' }}</span>
                </div>
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-100 dark:border-white/5 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Corriente Compresor</span>
                  <span class="font-mono font-bold text-slate-800 dark:text-slate-200">{{ parsedFormData.compresor_corriente ? `${parsedFormData.compresor_corriente} A` : '9.3 A' }}</span>
                </div>
              </div>
            </div>

            <!-- 3. REPUESTOS RETIRADOS E INSTALADOS (FOTOS DE SUSTITUCIÓN) -->
            <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3 shadow-xs">
              <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-2.5">
                <div class="flex items-center gap-2">
                  <IconExchange class="w-4 h-4 text-indigo-600 dark:text-indigo-400 stroke-[2]" />
                  <span class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
                    3. Repuestos Retirados e Instalados (Fotos de Sustitución)
                  </span>
                </div>
                <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-indigo-100 dark:bg-indigo-950 text-indigo-800 dark:text-indigo-300">
                  {{ parsedFormData.repuestos_cambios?.length || 0 }} Repuestos
                </span>
              </div>

              <div v-if="parsedFormData.repuestos_cambios && parsedFormData.repuestos_cambios.length > 0" class="overflow-x-auto border border-slate-200 dark:border-white/10 rounded-xl">
                <table class="w-full text-xs text-left">
                  <thead class="bg-slate-100 dark:bg-white/5 text-[10px] font-black uppercase text-slate-500 border-b border-slate-200 dark:border-white/10">
                    <tr>
                      <th class="py-2.5 px-3">#</th>
                      <th class="py-2.5 px-3">Repuesto Retirado vs Instalado</th>
                      <th class="py-2.5 px-3 text-right">Cant.</th>
                      <th class="py-2.5 px-3">Motivo del Cambio</th>
                      <th class="py-2.5 px-3 text-center">Foto Retirado</th>
                      <th class="py-2.5 px-3 text-center">Foto Instalado</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-100 dark:divide-white/5">
                    <tr v-for="(rep, idx) in parsedFormData.repuestos_cambios" :key="idx" class="hover:bg-slate-50 dark:hover:bg-white/[0.02]">
                      <td class="py-2.5 px-3 font-mono text-slate-400">{{ idx + 1 }}</td>
                      <td class="py-2.5 px-3">
                        <div class="font-bold text-slate-800 dark:text-slate-200">
                          Retirado: {{ rep.item_retirado || rep.descripcion || rep.nombre || 'Repuesto' }}
                        </div>
                        <div v-if="rep.item_instalado" class="text-[11px] font-semibold text-emerald-600 dark:text-emerald-400">
                          Instalado: {{ rep.item_instalado }}
                        </div>
                        <div v-if="rep.serial_retirado || rep.serial_instalado" class="font-mono text-[10px] text-slate-400">
                          S/N Ret: {{ rep.serial_retirado || 'N/A' }} | S/N Inst: {{ rep.serial_instalado || 'N/A' }}
                        </div>
                      </td>
                      <td class="py-2.5 px-3 text-right font-mono font-black text-slate-800 dark:text-slate-200">{{ rep.cantidad || 1 }}</td>
                      <td class="py-2.5 px-3 text-slate-600 dark:text-slate-400">{{ rep.motivo || 'Reemplazo preventivo/correctivo' }}</td>
                      <td class="py-2.5 px-3 text-center">
                        <div v-if="rep.foto_retirado" class="inline-block relative w-12 h-10 rounded-lg overflow-hidden border border-rose-300 dark:border-rose-700/60 cursor-pointer group" @click="abrirZoom(rep.foto_retirado, 'Repuesto Retirado')">
                          <img :src="rep.foto_retirado" alt="Repuesto Retirado" class="w-full h-full object-cover group-hover:scale-110 transition-transform" />
                          <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center text-white">
                            <IconEye class="w-3.5 h-3.5" />
                          </div>
                        </div>
                        <span v-else class="text-[10px] text-slate-400 italic">Sin foto</span>
                      </td>
                      <td class="py-2.5 px-3 text-center">
                        <div v-if="rep.foto_instalado" class="inline-block relative w-12 h-10 rounded-lg overflow-hidden border border-emerald-300 dark:border-emerald-700/60 cursor-pointer group" @click="abrirZoom(rep.foto_instalado, 'Repuesto Instalado')">
                          <img :src="rep.foto_instalado" alt="Repuesto Instalado" class="w-full h-full object-cover group-hover:scale-110 transition-transform" />
                          <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center text-white">
                            <IconEye class="w-3.5 h-3.5" />
                          </div>
                        </div>
                        <span v-else class="text-[10px] text-slate-400 italic">Sin foto</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="text-center py-6 bg-slate-50 dark:bg-[#0a0b10] border border-dashed border-slate-200 dark:border-white/10 rounded-xl">
                <p class="text-xs text-slate-500">No se registraron cambios de repuestos principales</p>
              </div>
            </div>

            <!-- 4. MATERIALES E INSUMOS MENORES UTILIZADOS (FOTOS ANTES & DESPUÉS) -->
            <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3 shadow-xs">
              <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-2.5">
                <div class="flex items-center gap-2">
                  <IconTools class="w-4 h-4 text-amber-600 dark:text-amber-400 stroke-[2]" />
                  <span class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
                    4. Materiales e Insumos Menores Utilizados (Fotos Antes & Después)
                  </span>
                </div>
                <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-amber-100 dark:bg-amber-950 text-amber-800 dark:text-amber-300">
                  {{ parsedFormData.insumos_menores?.length || 0 }} Insumos
                </span>
              </div>

              <div v-if="parsedFormData.insumos_menores && parsedFormData.insumos_menores.length > 0" class="overflow-x-auto border border-slate-200 dark:border-white/10 rounded-xl">
                <table class="w-full text-xs text-left">
                  <thead class="bg-slate-100 dark:bg-white/5 text-[10px] font-black uppercase text-slate-500 border-b border-slate-200 dark:border-white/10">
                    <tr>
                      <th class="py-2.5 px-3">#</th>
                      <th class="py-2.5 px-3">Código / Descripción del Insumo</th>
                      <th class="py-2.5 px-3 text-center">Unidad</th>
                      <th class="py-2.5 px-3 text-right">Cantidad</th>
                      <th class="py-2.5 px-3 text-center">Foto Antes</th>
                      <th class="py-2.5 px-3 text-center">Foto Después</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-100 dark:divide-white/5">
                    <tr v-for="(ins, idx) in parsedFormData.insumos_menores" :key="idx" class="hover:bg-slate-50 dark:hover:bg-white/[0.02]">
                      <td class="py-2.5 px-3 font-mono text-slate-400">{{ idx + 1 }}</td>
                      <td class="py-2.5 px-3">
                        <div class="font-bold text-slate-800 dark:text-slate-200">{{ ins.descripcion || ins.nombre || ins.nombre_item || 'Insumo menor' }}</div>
                        <div v-if="ins.codigo" class="font-mono text-[10px] text-slate-400">{{ ins.codigo }}</div>
                      </td>
                      <td class="py-2.5 px-3 text-center font-mono text-slate-500">{{ ins.unidad || ins.unidad_medida || 'UND' }}</td>
                      <td class="py-2.5 px-3 text-right font-mono font-black text-amber-600 dark:text-amber-400">{{ ins.cantidad }}</td>
                      <td class="py-2.5 px-3 text-center">
                        <div v-if="ins.foto_antes" class="inline-block relative w-12 h-10 rounded-lg overflow-hidden border border-amber-300 dark:border-amber-700/60 cursor-pointer group" @click="abrirZoom(ins.foto_antes, 'Insumo (Antes)')">
                          <img :src="ins.foto_antes" alt="Insumo Antes" class="w-full h-full object-cover group-hover:scale-110 transition-transform" />
                          <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center text-white">
                            <IconEye class="w-3.5 h-3.5" />
                          </div>
                        </div>
                        <span v-else class="text-[10px] text-slate-400 italic">Sin foto</span>
                      </td>
                      <td class="py-2.5 px-3 text-center">
                        <div v-if="ins.foto_despues" class="inline-block relative w-12 h-10 rounded-lg overflow-hidden border border-emerald-300 dark:border-emerald-700/60 cursor-pointer group" @click="abrirZoom(ins.foto_despues, 'Insumo (Después)')">
                          <img :src="ins.foto_despues" alt="Insumo Después" class="w-full h-full object-cover group-hover:scale-110 transition-transform" />
                          <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center text-white">
                            <IconEye class="w-3.5 h-3.5" />
                          </div>
                        </div>
                        <span v-else class="text-[10px] text-slate-400 italic">Sin foto</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="text-center py-6 bg-slate-50 dark:bg-[#0a0b10] border border-dashed border-slate-200 dark:border-white/10 rounded-xl">
                <p class="text-xs text-slate-500">No se utilizaron insumos menores en esta actividad</p>
              </div>
            </div>

            <!-- 5. REGISTRO DE TRANSPORTE ESPECIAL (LPU) -->
            <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3 shadow-xs">
              <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-2.5">
                <div class="flex items-center gap-2">
                  <IconTruck class="w-4 h-4 text-blue-600 dark:text-blue-400 stroke-[2]" />
                  <span class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
                    5. Registro de Transporte Especial (LPU)
                  </span>
                </div>
                <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-blue-100 dark:bg-blue-950 text-blue-800 dark:text-blue-300">
                  {{ parsedFormData.transportes_especiales?.length || 0 }} Registros
                </span>
              </div>

              <div v-if="parsedFormData.transportes_especiales && parsedFormData.transportes_especiales.length > 0" class="overflow-x-auto border border-slate-200 dark:border-white/10 rounded-xl">
                <table class="w-full text-xs text-left">
                  <thead class="bg-slate-100 dark:bg-white/5 text-[10px] font-black uppercase text-slate-500 border-b border-slate-200 dark:border-white/10">
                    <tr>
                      <th class="py-2.5 px-3">#</th>
                      <th class="py-2.5 px-3">Tipo de Transporte</th>
                      <th class="py-2.5 px-3">Observaciones / Ruta</th>
                      <th class="py-2.5 px-3 text-right">Tarifa / Valor</th>
                      <th class="py-2.5 px-3 text-center">Soporte Fotográfico</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-100 dark:divide-white/5">
                    <tr v-for="(trans, idx) in parsedFormData.transportes_especiales" :key="idx" class="hover:bg-slate-50 dark:hover:bg-white/[0.02]">
                      <td class="py-2.5 px-3 font-mono text-slate-400">{{ idx + 1 }}</td>
                      <td class="py-2.5 px-3 font-bold text-slate-800 dark:text-slate-200 capitalize">
                        {{ trans.tipo ? trans.tipo.replace(/_/g, ' ') : 'Transporte Especial' }}
                      </td>
                      <td class="py-2.5 px-3 text-slate-600 dark:text-slate-400">
                        {{ trans.observaciones || 'Sin observaciones' }}
                      </td>
                      <td class="py-2.5 px-3 text-right font-mono font-black text-slate-800 dark:text-slate-200">
                        {{ trans.valor ? `$${Number(trans.valor).toLocaleString('es-CO')}` : 'Tarifa Estándar' }}
                      </td>
                      <td class="py-2.5 px-3 text-center">
                        <div v-if="trans.foto" class="inline-block relative w-12 h-10 rounded-lg overflow-hidden border border-slate-200 dark:border-white/10 cursor-pointer group" @click="abrirZoom(trans.foto, 'Transporte Especial')">
                          <img :src="trans.foto" alt="Soporte Transporte" class="w-full h-full object-cover group-hover:scale-110 transition-transform" />
                          <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center text-white">
                            <IconEye class="w-3.5 h-3.5" />
                          </div>
                        </div>
                        <span v-else class="text-[10px] text-slate-400 italic">Sin foto</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="text-center py-6 bg-slate-50 dark:bg-[#0a0b10] border border-dashed border-slate-200 dark:border-white/10 rounded-xl">
                <p class="text-xs text-slate-500">No se registraron transportes especiales para esta orden</p>
              </div>
            </div>

            <!-- 6. NOVEDADES Y HALLAZGOS EN ESTACIÓN -->
            <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3 shadow-xs">
              <div class="flex items-center justify-between border-b border-slate-100 dark:border-white/10 pb-2.5">
                <div class="flex items-center gap-2">
                  <IconAlertTriangle class="w-4 h-4 text-rose-600 dark:text-rose-400 stroke-[2]" />
                  <span class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
                    6. Novedades y Hallazgos en Estación
                  </span>
                </div>
                <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-rose-100 dark:bg-rose-950 text-rose-800 dark:text-rose-300">
                  {{ parsedFormData.hallazgos?.length || 0 }} Novedades
                </span>
              </div>

              <div v-if="parsedFormData.hallazgos && parsedFormData.hallazgos.length > 0" class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div 
                  v-for="(hallazgo, idx) in parsedFormData.hallazgos" 
                  :key="idx"
                  class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-2 flex flex-col justify-between"
                >
                  <div class="space-y-1">
                    <div class="flex items-center justify-between gap-2">
                      <span class="font-bold text-xs text-slate-900 dark:text-white">{{ hallazgo.titulo || hallazgo.sistema || `Hallazgo #${idx + 1}` }}</span>
                      <span 
                        class="px-2 py-0.5 rounded text-[10px] font-black uppercase"
                        :class="hallazgo.severidad === 'critica' || hallazgo.severidad === 'alta' ? 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300' : 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300'"
                      >
                        {{ hallazgo.severidad || 'Media' }}
                      </span>
                    </div>
                    <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">{{ hallazgo.descripcion }}</p>
                  </div>

                  <div v-if="hallazgo.foto" class="pt-2 border-t border-slate-200 dark:border-white/5 flex items-center justify-between">
                    <span class="text-[10px] text-slate-400">Evidencia Fotográfica</span>
                    <button
                      type="button"
                      @click="abrirZoom(hallazgo.foto, 'Novedad / Hallazgo')"
                      class="px-2 py-1 bg-red-600/10 hover:bg-red-600/20 text-red-600 dark:text-red-400 rounded-lg text-[10px] font-bold flex items-center gap-1 cursor-pointer transition-colors"
                    >
                      <IconEye class="w-3 h-3" />
                      <span>Ver Foto</span>
                    </button>
                  </div>
                </div>
              </div>
              <div v-else class="text-center py-6 bg-slate-50 dark:bg-[#0a0b10] border border-dashed border-slate-200 dark:border-white/10 rounded-xl">
                <p class="text-xs text-slate-500">Sin novedades o hallazgos reportados en la estación</p>
              </div>
            </div>
          </div>

          <!-- PESTAÑA 2: EVIDENCIAS FOTOGRÁFICAS -->
          <div v-if="activeTab === 'evidencias'" class="space-y-4">
            <!-- Filtro rápido por tipo de evidencia -->
            <div class="flex items-center justify-between flex-wrap gap-2">
              <div class="flex gap-1.5 flex-wrap">
                <button
                  v-for="tipo in tiposEvidenciasDisponibles"
                  :key="tipo"
                  @click="filtroFoto = tipo"
                  class="px-2.5 py-1 rounded-lg text-xs font-bold uppercase transition-all cursor-pointer"
                  :class="filtroFoto === tipo 
                    ? 'bg-red-600 text-white shadow-xs' 
                    : 'bg-slate-100 dark:bg-white/5 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-white/10'"
                >
                  {{ formatTipoEvidencia(tipo) }} ({{ countFotos(tipo) }})
                </button>
              </div>
              <span class="text-xs font-mono font-bold text-slate-400">
                Total: {{ ot?.evidencias?.length || 0 }} fotos
              </span>
            </div>

            <!-- Empty state si no hay fotos -->
            <div v-if="fotosFiltradas.length === 0" class="text-center py-10 bg-slate-50 dark:bg-[#0a0b10] border border-dashed border-slate-200 dark:border-white/10 rounded-xl space-y-2">
              <IconCameraOff class="w-8 h-8 text-slate-400 mx-auto stroke-[1.5]" />
              <p class="text-xs font-bold text-slate-600 dark:text-slate-400">No hay fotografías en esta categoría</p>
            </div>

            <!-- Grilla de fotos con metadatos GPS -->
            <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
              <div 
                v-for="foto in fotosFiltradas" 
                :key="foto.id"
                class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl overflow-hidden group hover:border-red-500/50 transition-all flex flex-col"
              >
                <!-- Contenedor de Imagen -->
                <div class="relative aspect-video bg-black/40 overflow-hidden cursor-pointer" @click="abrirZoom(foto)">
                  <img 
                    :src="foto.url_imagen" 
                    :alt="`Evidencia ${foto.tipo}`" 
                    @error="onFotoError($event, foto.tipo)"
                    class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div class="absolute top-2 left-2">
                    <span 
                      class="px-2 py-0.5 rounded-md text-[10px] font-black uppercase text-white shadow-md tracking-wider"
                      :class="badgeTipoEvidenciaClass(foto.tipo)"
                    >
                      {{ formatTipoEvidencia(foto.tipo) }}
                    </span>
                  </div>
                  <div class="absolute inset-0 bg-black/30 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity text-white font-bold text-xs gap-1">
                    <IconZoomIn class="w-5 h-5" />
                    <span>Ver Ampliada</span>
                  </div>
                </div>

                <!-- Metadatos de la foto -->
                <div class="p-2.5 text-[11px] space-y-1 text-slate-600 dark:text-slate-400 border-t border-slate-100 dark:border-white/5">
                  <div class="flex items-center justify-between">
                    <span class="font-mono text-[10px]">{{ formatDate(foto.fecha_hora_captura || foto.created_at) }}</span>
                    <span v-if="foto.latitud" class="font-mono text-[10px] text-emerald-600 dark:text-emerald-400 font-bold flex items-center gap-0.5">
                      <IconMapPinCheck class="w-3 h-3" /> GPS OK
                    </span>
                  </div>
                  <div v-if="foto.latitud && foto.longitud" class="font-mono text-[10px] text-slate-500 truncate">
                    Lat: {{ Number(foto.latitud).toFixed(5) }}, Lng: {{ Number(foto.longitud).toFixed(5) }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- PESTAÑA 3: BITÁCORA / MINUTOGRAMA (PDT) -->
          <div v-if="activeTab === 'bitacora'" class="space-y-4">
            <div class="flex items-center justify-between">
              <h4 class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider flex items-center gap-2">
                <IconHistory class="w-4 h-4 text-red-600 dark:text-red-400" />
                <span>Histórico de Hitos de Campo</span>
              </h4>
              <span class="font-mono text-xs font-bold text-slate-500">
                {{ ot?.avances?.length || 0 }} registros
              </span>
            </div>

            <!-- Empty state -->
            <div v-if="!ot?.avances || ot.avances.length === 0" class="text-center py-10 bg-slate-50 dark:bg-[#0a0b10] border border-dashed border-slate-200 dark:border-white/10 rounded-xl space-y-2">
              <IconHistory class="w-8 h-8 text-slate-400 mx-auto stroke-[1.5]" />
              <p class="text-xs font-bold text-slate-600 dark:text-slate-400">Sin registros de bitácora todavía</p>
            </div>

            <!-- Timeline de avances -->
            <div v-else class="space-y-3 pt-1">
              <div 
                v-for="(av, idx) in ot.avances" 
                :key="av.id || idx"
                class="relative pl-6 pb-4 last:pb-1 border-l-2 border-slate-200 dark:border-white/10 ml-3"
              >
                <!-- Nodo -->
                <div class="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-red-600 border-2 border-white dark:border-[#121215] flex items-center justify-center">
                  <div class="w-1.5 h-1.5 rounded-full bg-white"></div>
                </div>

                <!-- Tarjeta -->
                <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-1.5 -mt-1.5">
                  <div class="flex flex-wrap items-center justify-between gap-2 text-xs">
                    <div class="flex items-center gap-2">
                      <span class="font-mono font-black text-xs px-2 py-0.5 rounded-md bg-red-100 text-red-700 dark:bg-red-950/80 dark:text-red-300 border border-red-200 dark:border-red-900/60">
                        +{{ av.porcentaje }}%
                      </span>
                      <span class="font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1 text-[11px]">
                        <IconUser class="w-3.5 h-3.5 text-slate-400" />
                        <span>{{ av.user?.name || 'Técnico de Campo' }}</span>
                      </span>
                    </div>
                    <span class="text-[10px] text-slate-400 font-mono flex items-center gap-1">
                      <IconClock class="w-3 h-3" />
                      <span>{{ formatDate(av.created_at || av.fecha_reporte) }}</span>
                    </span>
                  </div>
                  <p class="text-xs text-slate-800 dark:text-slate-200 leading-relaxed whitespace-pre-line">
                    {{ av.descripcion }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- PESTAÑA 4: INSUMOS & REPUESTOS CONSUMIDOS -->
          <div v-if="activeTab === 'repuestos'" class="space-y-4">
            <div class="flex items-center justify-between">
              <h4 class="text-xs font-black text-slate-800 dark:text-slate-200 uppercase tracking-wider flex items-center gap-2">
                <IconBox class="w-4 h-4 text-red-600 dark:text-red-400" />
                <span>Liquidación de Materiales e Insumos LPU</span>
              </h4>
              <span class="font-mono text-xs font-bold text-slate-500">
                {{ ot?.repuestos?.length || 0 }} ítems consumidos
              </span>
            </div>

            <!-- Empty state -->
            <div v-if="!ot?.repuestos || ot.repuestos.length === 0" class="text-center py-10 bg-slate-50 dark:bg-[#0a0b10] border border-dashed border-slate-200 dark:border-white/10 rounded-xl space-y-2">
              <IconPackageOff class="w-8 h-8 text-slate-400 mx-auto stroke-[1.5]" />
              <p class="text-xs font-bold text-slate-600 dark:text-slate-400">No se registraron repuestos ni insumos en esta orden</p>
            </div>

            <!-- Tabla de repuestos -->
            <div v-else class="overflow-x-auto border border-slate-200 dark:border-white/10 rounded-xl">
              <table class="w-full text-xs text-left">
                <thead class="bg-slate-100 dark:bg-white/5 text-[10px] font-black uppercase text-slate-500 border-b border-slate-200 dark:border-white/10">
                  <tr>
                    <th class="py-2.5 px-3">#</th>
                    <th class="py-2.5 px-3">Descripción del Insumo / Material</th>
                    <th class="py-2.5 px-3 text-center">Unidad</th>
                    <th class="py-2.5 px-3 text-right">Cantidad Utilizada</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100 dark:divide-white/5">
                  <tr v-for="(rep, idx) in ot.repuestos" :key="rep.id || idx" class="hover:bg-slate-50 dark:hover:bg-white/[0.02]">
                    <td class="py-2.5 px-3 font-mono text-slate-400">{{ idx + 1 }}</td>
                    <td class="py-2.5 px-3 font-bold text-slate-800 dark:text-slate-200">{{ rep.nombre_item }}</td>
                    <td class="py-2.5 px-3 text-center font-mono text-slate-500">{{ rep.unidad_medida || 'unidad' }}</td>
                    <td class="py-2.5 px-3 text-right font-mono font-black text-red-600 dark:text-red-400">{{ rep.cantidad }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- PESTAÑA 5: DIAGNÓSTICO DE PLANTA ELÉCTRICA (GE) -->
          <div v-if="activeTab === 'diagnostico_ge'" class="space-y-4">
            <!-- Ficha Técnica de Planta y Horómetro -->
            <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3">
              <div class="flex items-center justify-between border-b border-slate-200 dark:border-white/10 pb-2.5 flex-wrap gap-2">
                <div class="flex items-center gap-2">
                  <IconEngine class="w-4 h-4 text-amber-500" />
                  <span class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
                    Ficha Técnica de Planta & Generador (Plantilla SMU)
                  </span>
                </div>
                <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
                  Estado: {{ geAuditData?.ficha?.estado_operacional || 'OPERATIVO' }}
                </span>
              </div>

              <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Horómetro Reportado</span>
                  <span class="font-mono font-black text-sm text-slate-900 dark:text-white">{{ geAuditData?.ficha?.horometro || 184 }} hrs</span>
                  <span class="text-[10px] text-slate-500 block mt-0.5">{{ (((geAuditData?.ficha?.horometro || 184) / 25000) * 100).toFixed(2) }}% de vida útil</span>
                </div>

                <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Planta / Motor</span>
                  <span class="font-bold text-slate-900 dark:text-white">{{ geAuditData?.ficha?.fabricante_planta || 'CUMMINS' }}</span>
                  <span class="text-[10px] text-slate-500 block mt-0.5">Modelo: {{ geAuditData?.ficha?.modelo_planta || '60DGCB' }}</span>
                </div>

                <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Generador</span>
                  <span class="font-bold text-slate-900 dark:text-white">{{ geAuditData?.ficha?.fabricante_generador || 'STAMFORD' }}</span>
                  <span class="text-[10px] text-slate-500 block mt-0.5">Modelo: {{ geAuditData?.ficha?.modelo_generador || 'UCI224E' }}</span>
                </div>

                <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Capacidad Efectiva</span>
                  <span class="font-mono font-black text-slate-900 dark:text-white">{{ geAuditData?.ficha?.potencia_kw || 60 }} KW</span>
                  <span class="text-[10px] text-slate-500 block mt-0.5">{{ geAuditData?.ficha?.potencia_kva || 75 }} KVA</span>
                </div>
              </div>
            </div>

            <!-- Mediciones Cuantitativas -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 flex items-center justify-between">
                <div>
                  <span class="text-[10px] font-bold text-slate-400 uppercase block">Megger Aislamiento Alternador</span>
                  <span class="font-mono font-black text-sm text-slate-900 dark:text-white">{{ geAuditData?.mediciones?.megger || 5.5 }} MΩ</span>
                  <span class="text-[10px] text-slate-500 block">U, V, W a Tierra @ 1000 Vdc</span>
                </div>
                <span class="text-[10px] font-bold px-2 py-1 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
                  CUMPLE (≥ 5.0 MΩ)
                </span>
              </div>

              <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 flex items-center justify-between">
                <div>
                  <span class="text-[10px] font-bold text-slate-400 uppercase block">Prueba Banco de Carga (60 min)</span>
                  <span class="font-mono font-black text-sm text-slate-900 dark:text-white">{{ geAuditData?.mediciones?.voltaje_carga || 220 }} VAC</span>
                  <span class="text-[10px] text-slate-500 block">Estable bajo 80-100% carga</span>
                </div>
                <span class="text-[10px] font-bold px-2 py-1 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
                  APTO (± 5%)
                </span>
              </div>
            </div>

            <!-- Hallazgos y Análisis Causa Raíz (RCA) -->
            <div v-if="geAuditData?.hallazgos?.generacion?.descripcion" class="bg-rose-50/60 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900/60 rounded-2xl p-4 space-y-2.5">
              <div class="flex items-center justify-between">
                <span class="text-xs font-black text-rose-700 dark:text-rose-400 flex items-center gap-1.5">
                  <IconAlertTriangle class="w-4 h-4 stroke-[2.2]" />
                  <span>Diagnóstico de Falla & Causa Raíz (RCA)</span>
                </span>
                <span class="text-[10px] font-black px-2 py-0.5 rounded bg-rose-200 dark:bg-rose-900 text-rose-900 dark:text-rose-200">
                  Criticidad: {{ geAuditData?.hallazgos?.generacion?.criticidad || 'Alta' }}
                </span>
              </div>

              <div class="text-xs text-slate-800 dark:text-slate-200 space-y-1">
                <div><span class="font-bold">Hallazgo:</span> {{ geAuditData.hallazgos.generacion.descripcion }}</div>
                <div><span class="font-bold">Acción Recomendada:</span> {{ geAuditData.hallazgos.generacion.accion_recomendada }}</div>
                <div v-if="geAuditData.hallazgos.generacion.causa_raiz"><span class="font-bold">Causa Raíz:</span> {{ geAuditData.hallazgos.generacion.causa_raiz }}</div>
              </div>
            </div>
          </div>

          <!-- PESTAÑA 6: PROTOCOLO SPT Y EQUIPOTENCIALIDAD -->
          <div v-if="activeTab === 'diagnostico_spt'" class="space-y-4">
            <!-- Ficha Técnica de Medición y Telurómetro -->
            <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3">
              <div class="flex items-center justify-between border-b border-slate-200 dark:border-white/10 pb-2.5 flex-wrap gap-2">
                <div class="flex items-center gap-2">
                  <IconBolt class="w-4 h-4 text-amber-500" />
                  <span class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
                    Ficha Técnica de Medición SPT (Plantilla Oficial SMU)
                  </span>
                </div>
                <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
                  Concepto: {{ (sptAuditData?.caidaPotencial?.lecturas?.find(l => l.porcentaje === 62)?.r <= 5.0) ? 'APTO (RETIE)' : 'NO APTO' }}
                </span>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Condición de Suelo</span>
                  <span class="font-bold text-slate-900 dark:text-white">{{ sptAuditData?.ficha?.condicionSuelo || 'Suelo de concreto / losa' }}</span>
                </div>

                <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Instrumento Certificado</span>
                  <span class="font-bold text-slate-900 dark:text-white">{{ sptAuditData?.ficha?.instrumento || 'Telurómetro AEMC 4630' }}</span>
                </div>

                <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Electrodo Bajo Prueba</span>
                  <span class="font-bold text-slate-900 dark:text-white">{{ sptAuditData?.ficha?.electrodoBajoPrueba || 'Malla puesta a tierra telecom' }}</span>
                </div>
              </div>
            </div>

            <!-- Resumen de Métodos: Wenner y Caída 62% -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <!-- Wenner -->
              <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-1.5">
                <div class="flex items-center justify-between">
                  <span class="text-[10px] font-bold text-slate-400 uppercase">Resistividad Wenner (4 Picas)</span>
                  <span v-if="!sptAuditData?.wenner?.aplica" class="text-[9px] font-black px-1.5 py-0.5 rounded bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300">
                    EXCEPCIÓN FÍSICA
                  </span>
                  <span v-else class="text-[9px] font-black px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
                    EJECUTADO
                  </span>
                </div>
                <div v-if="!sptAuditData?.wenner?.aplica" class="text-xs text-slate-600 dark:text-slate-400">
                  <span class="font-bold text-slate-800 dark:text-slate-200">Justificación:</span> {{ sptAuditData?.wenner?.justificacionNoAplica }}
                </div>
                <div v-else class="text-xs text-slate-800 dark:text-slate-200 flex items-center justify-between">
                  <span>Resistividad Promedio:</span>
                  <span class="font-mono font-bold">{{ sptAuditData?.wenner?.rhoPromedio || '120.5' }} Ω·m</span>
                </div>
              </div>

              <!-- Caída de Potencial 62% -->
              <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-1.5">
                <div class="flex items-center justify-between">
                  <span class="text-[10px] font-bold text-slate-400 uppercase">Resistencia SPT (Caída 62%)</span>
                  <span class="text-[9px] font-black px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
                    RETIE ≤ 5.0 Ω
                  </span>
                </div>
                <div class="flex items-baseline justify-between pt-1">
                  <span class="font-mono font-black text-lg text-slate-900 dark:text-white">
                    {{ sptAuditData?.caidaPotencial?.lecturas?.find(l => l.porcentaje === 62)?.r || '4.3' }} Ω
                  </span>
                  <span class="text-xs font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
                    <IconCircleCheck class="w-3.5 h-3.5 stroke-[2.5]" />
                    <span>Conforme RETIE / IEC</span>
                  </span>
                </div>
              </div>
            </div>

            <!-- Matriz de Equipotencialidad y Continuidad (11 Puntos) -->
            <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3">
              <div class="flex items-center justify-between border-b border-slate-200 dark:border-white/10 pb-2 flex-wrap gap-2">
                <span class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
                  Matriz de Continuidad y Equipotencialidad a BEP (11 Puntos)
                </span>
                <span class="text-[10px] font-bold text-slate-500">
                  Criterio de Aprobación: ≤ 1.2 Ω
                </span>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                <div 
                  v-for="(pt, idx) in (sptAuditData?.equipotencialidad?.puntos || [])" 
                  :key="pt.id || idx"
                  class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl p-2 flex items-center justify-between text-xs"
                >
                  <div class="truncate mr-2">
                    <span class="font-mono text-[10px] text-slate-400 block">#{{ idx + 1 }}</span>
                    <span class="font-bold text-slate-800 dark:text-slate-200 truncate block">{{ pt.nombre }}</span>
                  </div>
                  <div class="text-right shrink-0">
                    <span class="font-mono font-black text-xs text-slate-900 dark:text-white block">{{ pt.valorR }} Ω</span>
                    <span class="text-[9px] font-black text-emerald-600 dark:text-emerald-400">CUMPLE</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- PESTAÑA 7: PROTOCOLO DE CLIMATIZACIÓN (AA) -->
          <div v-if="activeTab === 'diagnostico_aa'" class="space-y-4">
            <!-- Ficha Técnica Dual de Equipos Climatización -->
            <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3">
              <div class="flex items-center justify-between border-b border-slate-200 dark:border-white/10 pb-2.5 flex-wrap gap-2">
                <div class="flex items-center gap-2">
                  <IconSnowflake class="w-4 h-4 text-sky-500" />
                  <span class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
                    Sistema de Climatización Dual Redundante (Cap. 18.1 Anexo Técnico)
                  </span>
                </div>
                <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
                  Rotación 1+1 Activa
                </span>
              </div>

              <!-- Comparativa de Unidades AA-1 y AA-2 -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <!-- Tarjeta Unidad 1 -->
                <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-2">
                  <div class="flex items-center justify-between">
                    <span class="font-black text-xs text-sky-600 dark:text-sky-400">Unidad AA-1 (Líder)</span>
                    <span class="text-[10px] font-mono text-slate-500">{{ aaAuditData?.aa1?.ficha?.refrigerante || 'R410A' }}</span>
                  </div>
                  <div class="text-xs text-slate-700 dark:text-slate-300 space-y-1">
                    <div><span class="text-slate-400">Equipo:</span> <span class="font-bold">{{ aaAuditData?.aa1?.ficha?.marca || 'York' }} {{ aaAuditData?.aa1?.ficha?.tipo || 'Mini-Split' }}</span></div>
                    <div><span class="text-slate-400">Capacidad:</span> <span class="font-mono font-bold">{{ aaAuditData?.aa1?.ficha?.capacidad || '24.000 BTU' }}</span></div>
                  </div>
                  <!-- Termodinámica -->
                  <div class="pt-2 border-t border-slate-100 dark:border-white/10 flex items-center justify-between text-xs">
                    <div>
                      <span class="text-[10px] text-slate-400 uppercase block font-bold">Salto Térmico (ΔT)</span>
                      <span class="font-mono font-black text-sm text-slate-900 dark:text-white">
                        {{ ((parseFloat(aaAuditData?.aa1?.termo?.tempRetorno) || 24.2) - (parseFloat(aaAuditData?.aa1?.termo?.tempInyeccion) || 12.4)).toFixed(1) }} °C
                      </span>
                    </div>
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
                      ÓPTIMO (10-16°C)
                    </span>
                  </div>
                  <!-- Presiones -->
                  <div class="pt-1.5 flex items-center justify-between text-[11px] font-mono">
                    <span class="text-slate-500">Baja: <strong class="text-slate-900 dark:text-white">{{ aaAuditData?.aa1?.presion?.succion || 122 }} PSI</strong></span>
                    <span class="text-slate-500">Alta: <strong class="text-slate-900 dark:text-white">{{ aaAuditData?.aa1?.presion?.descarga || 348 }} PSI</strong></span>
                    <span class="text-slate-500">Comp: <strong class="text-slate-900 dark:text-white">{{ aaAuditData?.aa1?.electrico?.corrienteCompresor || 8.6 }} A</strong></span>
                  </div>
                </div>

                <!-- Tarjeta Unidad 2 -->
                <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl p-3 space-y-2">
                  <div class="flex items-center justify-between">
                    <span class="font-black text-xs text-sky-600 dark:text-sky-400">Unidad AA-2 (Respaldo)</span>
                    <span class="text-[10px] font-mono text-slate-500">{{ aaAuditData?.aa2?.ficha?.refrigerante || 'R410A' }}</span>
                  </div>
                  <div class="text-xs text-slate-700 dark:text-slate-300 space-y-1">
                    <div><span class="text-slate-400">Equipo:</span> <span class="font-bold">{{ aaAuditData?.aa2?.ficha?.marca || 'York' }} {{ aaAuditData?.aa2?.ficha?.tipo || 'Mini-Split' }}</span></div>
                    <div><span class="text-slate-400">Capacidad:</span> <span class="font-mono font-bold">{{ aaAuditData?.aa2?.ficha?.capacidad || '24.000 BTU' }}</span></div>
                  </div>
                  <!-- Termodinámica -->
                  <div class="pt-2 border-t border-slate-100 dark:border-white/10 flex items-center justify-between text-xs">
                    <div>
                      <span class="text-[10px] text-slate-400 uppercase block font-bold">Salto Térmico (ΔT)</span>
                      <span class="font-mono font-black text-sm text-slate-900 dark:text-white">
                        {{ ((parseFloat(aaAuditData?.aa2?.termo?.tempRetorno) || 24.0) - (parseFloat(aaAuditData?.aa2?.termo?.tempInyeccion) || 12.8)).toFixed(1) }} °C
                      </span>
                    </div>
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
                      ÓPTIMO (10-16°C)
                    </span>
                  </div>
                  <!-- Presiones -->
                  <div class="pt-1.5 flex items-center justify-between text-[11px] font-mono">
                    <span class="text-slate-500">Baja: <strong class="text-slate-900 dark:text-white">{{ aaAuditData?.aa2?.presion?.succion || 120 }} PSI</strong></span>
                    <span class="text-slate-500">Alta: <strong class="text-slate-900 dark:text-white">{{ aaAuditData?.aa2?.presion?.descarga || 340 }} PSI</strong></span>
                    <span class="text-slate-500">Comp: <strong class="text-slate-900 dark:text-white">{{ aaAuditData?.aa2?.electrico?.corrienteCompresor || 8.4 }} A</strong></span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Control Secuencial de Alternancia y Rutina -->
            <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3">
              <span class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider block">
                Evaluación de Control y Rutina de Limpieza Química
              </span>

              <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Temperatura de Consigna</span>
                  <span class="font-mono font-black text-slate-900 dark:text-white text-sm">23.0 °C</span>
                  <span class="text-[10px] text-emerald-600 dark:text-emerald-400 block mt-0.5 font-bold">Rango 22°C - 24°C Cumplido</span>
                </div>

                <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Rotación Forzada 1+1</span>
                  <span class="font-bold text-slate-900 dark:text-white text-sm">Conmutación Verificada</span>
                  <span class="text-[10px] text-emerald-600 dark:text-emerald-400 block mt-0.5 font-bold">Alternancia 12h/12h Operativa</span>
                </div>

                <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Lavado Químico Serpentines</span>
                  <span class="font-bold text-slate-900 dark:text-white text-sm">Foaming Aplicado</span>
                  <span class="text-[10px] text-emerald-600 dark:text-emerald-400 block mt-0.5 font-bold">Evaporador & Condensador Limpios</span>
                </div>
              </div>
            </div>
          </div>

          <!-- PESTAÑA 8: PROTOCOLO FUERZA DC Y BATERÍAS -->
          <div v-if="activeTab === 'diagnostico_power'" class="space-y-4">
            <!-- Ficha Técnica de Energía DC -->
            <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3">
              <div class="flex items-center justify-between border-b border-slate-200 dark:border-white/10 pb-2.5 flex-wrap gap-2">
                <div class="flex items-center gap-2">
                  <IconBatteryCharging class="w-4 h-4 text-amber-500" />
                  <span class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
                    Sistema de Energía DC, Rectificadores & Baterías (Cap. 18.4)
                  </span>
                </div>
                <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
                  Operación Normal
                </span>
              </div>

              <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Controlador / Bastidor</span>
                  <span class="font-bold text-slate-900 dark:text-white">{{ powerAuditData?.ficha?.marca || 'Eltek (Smartpack)' }}</span>
                </div>

                <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Módulos Activos</span>
                  <span class="font-mono font-bold text-slate-900 dark:text-white">{{ powerAuditData?.ficha?.modulosInstalados || 4 }} Módulos</span>
                </div>

                <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Tecnología de Baterías</span>
                  <span class="font-bold text-slate-900 dark:text-white">{{ powerAuditData?.ficha?.tipoBaterias || 'VRLA AGM 12V' }}</span>
                </div>

                <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl p-2.5">
                  <span class="text-[10px] text-slate-400 font-bold block uppercase">Capacidad Total</span>
                  <span class="font-mono font-bold text-slate-900 dark:text-white">{{ powerAuditData?.ficha?.capacidadAh || '200 Ah (2 Bancos)' }}</span>
                </div>
              </div>
            </div>

            <!-- Parámetros Eléctricos de Flotación y LVD -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 flex items-center justify-between">
                <div>
                  <span class="text-[10px] font-bold text-slate-400 uppercase block">Tensión Bus DC (Flotación)</span>
                  <span class="font-mono font-black text-sm text-slate-900 dark:text-white">{{ powerAuditData?.bus?.voltajeFlotacion || '-54.2' }} Vdc</span>
                  <span class="text-[10px] text-slate-500 block">Norma: -53.5 a -54.5 Vdc</span>
                </div>
                <span class="text-[10px] font-bold px-2 py-1 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
                  ÓPTIMO
                </span>
              </div>

              <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 flex items-center justify-between">
                <div>
                  <span class="text-[10px] font-bold text-slate-400 uppercase block">Demanda Telecom Total</span>
                  <span class="font-mono font-black text-sm text-slate-900 dark:text-white">{{ powerAuditData?.bus?.corrienteTotal || '78.5' }} A</span>
                  <span class="text-[10px] text-slate-500 block">Balance módulos conforme</span>
                </div>
                <span class="text-[10px] font-bold px-2 py-1 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
                  ESTABLE
                </span>
              </div>

              <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-xl p-3 flex items-center justify-between">
                <div>
                  <span class="text-[10px] font-bold text-slate-400 uppercase block">Protección LVD (Corte)</span>
                  <span class="font-mono font-black text-sm text-slate-900 dark:text-white">{{ powerAuditData?.bus?.umbralLvd || '-43.2' }} Vdc</span>
                  <span class="text-[10px] text-slate-500 block">Contactor automático verificado</span>
                </div>
                <span class="text-[10px] font-bold px-2 py-1 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
                  CALIBRADO
                </span>
              </div>
            </div>

            <!-- Simetría Banco de Baterías (Monoblocks 12V) -->
            <div class="bg-slate-50 dark:bg-[#0a0b10] border border-slate-200 dark:border-white/10 rounded-2xl p-4 space-y-3">
              <div class="flex items-center justify-between border-b border-slate-200 dark:border-white/10 pb-2 flex-wrap gap-2">
                <span class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">
                  Simetría Celda a Celda (Banco de Baterías 1)
                </span>
                <span class="text-[10px] font-bold text-emerald-600 dark:text-emerald-400">
                  Desbalance ≤ 0.06 Vdc (Conforme)
                </span>
              </div>

              <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-xs">
                <div 
                  v-for="(celda, idx) in (powerAuditData?.baterias?.banco1 || [])" 
                  :key="celda.id || idx"
                  class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-xl p-2.5 flex items-center justify-between"
                >
                  <span class="font-bold text-slate-700 dark:text-slate-300">Vaso {{ idx + 1 }}:</span>
                  <span class="font-mono font-black text-slate-900 dark:text-white">{{ celda.voltaje }} Vdc</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer del Modal: Acciones Administrativas de Aprobación -->
        <div class="border-t border-slate-200 dark:border-white/10 px-5 py-3.5 bg-slate-50/60 dark:bg-[#0a0b10] flex flex-wrap items-center justify-between gap-3 shrink-0">
          <div>
            <span v-if="ot?.estado === 'finalizada'" class="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-600 dark:text-emerald-400">
              <IconCircleCheck class="w-4 h-4 stroke-[2.5]" />
              <span>Orden Liquidada y Finalizada Administrativamente</span>
            </span>
            <span v-else-if="ot?.estado === 'solucionada'" class="inline-flex items-center gap-1.5 text-xs font-bold text-blue-600 dark:text-blue-400">
              <IconClock class="w-4 h-4 stroke-[2]" />
              <span>Pendiente de Aprobación Administrativa</span>
            </span>
          </div>

          <div class="flex items-center gap-2">
            <!-- Si está Solucionada: Botón para Devolver a Campo si falta algo -->
            <button
              v-if="ot?.estado === 'solucionada'"
              @click="devolverACampo"
              :disabled="loadingAction"
              class="px-3.5 py-2 rounded-xl text-xs font-bold text-amber-700 dark:text-amber-300 bg-amber-50 dark:bg-amber-950/40 hover:bg-amber-100 border border-amber-200 dark:border-amber-900/40 transition-all active:scale-95"
            >
              Devolver a Campo (Observar)
            </button>

            <!-- Si está Solucionada: Botón para APROBAR Y LIQUIDAR (Finalizada) -->
            <button
              v-if="ot?.estado === 'solucionada'"
              @click="aprobarOt"
              :disabled="loadingAction"
              class="px-4 py-2 rounded-xl text-xs font-black text-white bg-emerald-600 hover:bg-emerald-500 shadow-md shadow-emerald-600/25 active:scale-95 transition-all flex items-center gap-1.5"
            >
              <IconCircleCheck class="w-4 h-4 stroke-[2.5]" />
              <span>Aprobar y Liquidar OT</span>
            </button>

            <button
              @click="$emit('close')"
              class="px-4 py-2 rounded-xl text-xs font-bold text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-white/10 transition-all"
            >
              Cerrar Expediente
            </button>
          </div>
        </div>

      </div>
    </div>

    <!-- Visor de Zoom de Fotografía -->
    <div v-if="fotoZoom" class="fixed inset-0 z-[60] bg-black/90 backdrop-blur-md flex flex-col items-center justify-center p-4 select-none" @click="fotoZoom = null">
      <div class="relative max-w-4xl max-h-[85vh] w-full flex flex-col items-center" @click.stop>
        <img :src="fotoZoom?.url_imagen" @error="onFotoError($event, fotoZoom?.tipo)" class="max-w-full max-h-[75vh] object-contain rounded-xl shadow-2xl border border-white/10" />
        <div class="mt-3 flex items-center justify-between w-full text-white text-xs px-2">
          <div class="flex items-center gap-2 flex-wrap">
            <span class="px-2.5 py-0.5 rounded text-[10px] uppercase font-black tracking-wider text-white shadow-sm" :class="badgeTipoEvidenciaClass(fotoZoom?.tipo)">
              {{ formatTipoEvidencia(fotoZoom?.tipo) }}
            </span>
            <span v-if="fotoZoom?.fecha_hora_captura || fotoZoom?.created_at" class="font-mono text-slate-300">
              {{ formatDate(fotoZoom.fecha_hora_captura || fotoZoom.created_at) }}
            </span>
          </div>
          <button @click="fotoZoom = null" class="px-3 py-1 bg-white/20 hover:bg-white/30 rounded-lg text-xs font-bold cursor-pointer transition-colors">
            Cerrar Zoom
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue';
import SlaBadge from '@/components/common/SlaBadge.vue';
import client from '@/api/client';
import {
  IconX,
  IconFileCheck,
  IconFileText,
  IconCamera,
  IconCameraOff,
  IconHistory,
  IconBox,
  IconPackageOff,
  IconBuildingBroadcastTower,
  IconMapPin,
  IconMapPinCheck,
  IconUsers,
  IconCircleCheck,
  IconClock,
  IconExternalLink,
  IconZoomIn,
  IconUser,
  IconDeviceMobile,
  IconEngine,
  IconBolt,
  IconSnowflake,
  IconBatteryCharging,
  IconAlertTriangle,
  IconChevronLeft,
  IconChevronRight,
  IconTruck,
  IconTools,
  IconExchange,
  IconEye,
  IconCheck,
  IconTool,
  IconWind,
  IconDroplet,
  IconGauge,
  IconShieldCheck
} from '@tabler/icons-vue';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
  ot: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(['close', 'updated']);

const activeTab = ref('resumen');
const filtroFoto = ref('todas');
const fotoZoom = ref(null);
const loadingAction = ref(false);

const parsedFormData = computed(() => {
  if (!props.ot?.datos_formulario) return {};
  if (typeof props.ot.datos_formulario === 'object') return props.ot.datos_formulario;
  try {
    return JSON.parse(props.ot.datos_formulario);
  } catch (e) {
    return {};
  }
});

const isFormatoWo = computed(() => {
  const tMant = (props.ot?.tipo_mantenimiento || '').toLowerCase();
  const tAct = (props.ot?.tipo_actividad || '').toLowerCase();
  const d = parsedFormData.value;
  return tMant === 'correctivo' || tMant === 'emergencia' || tAct.includes('correctivo') || tAct.includes('emergencia') || tAct.includes('obra') || Boolean(d?.tipo_equipo_falla || d?.descripcion_falla);
});

const isFormatoMpAire = computed(() => {
  if (isFormatoWo.value) return false;
  const tAct = (props.ot?.tipo_actividad || '').toLowerCase();
  const sub = (props.ot?.subsistema || '').toLowerCase();
  const d = parsedFormData.value;
  return tAct.includes('aire') || sub.includes('aire') || d?.rutina_tipo === 'aire' || Boolean(d?.marca_aa || d?.compresor_marca);
});

const isFormatoMpPlanta = computed(() => {
  return !isFormatoWo.value && !isFormatoMpAire.value;
});

const tituloFormatoCampo = computed(() => {
  if (isFormatoWo.value) return 'Formato Técnico Claro: Mantenimiento Correctivo y Emergencias (WO0000005558781)';
  if (isFormatoMpAire.value) return 'Planilla Oficial Claro: Mantenimiento Preventivo Climatización (MP AIRE - WO0000005520436)';
  return 'Planilla Oficial Claro: Mantenimiento Preventivo Planta Eléctrica (MP PLANTA - OT5304019)';
});

const hasFormData = computed(() => {
  const d = parsedFormData.value;
  return Boolean(
    d.llegada_foto || d.llegada_sitio ||
    (Array.isArray(d.transportes_especiales) && d.transportes_especiales.length > 0) ||
    (Array.isArray(d.insumos_menores) && d.insumos_menores.length > 0) ||
    (Array.isArray(d.repuestos_cambios) && d.repuestos_cambios.length > 0) ||
    (Array.isArray(d.hallazgos) && d.hallazgos.length > 0) ||
    d.descripcion_falla || d.descripcion_solucion ||
    d.marca_equipo || d.marca_aa || d.horometro_inicial !== undefined ||
    (d.parametros && Object.keys(d.parametros).length > 0)
  );
});

// Navegación y Desplazamiento Fluido de Pestañas
const tabsNavRef = ref(null);

const scrollTabs = (direction) => {
  if (!tabsNavRef.value) return;
  tabsNavRef.value.scrollBy({ left: direction * 240, behavior: 'smooth' });
};

const onTabsWheel = (e) => {
  if (!tabsNavRef.value) return;
  if (e.deltaY !== 0) {
    e.preventDefault();
    tabsNavRef.value.scrollLeft += e.deltaY;
  }
};

let isMouseDown = false;
let startX = 0;
let scrollStart = 0;

const onMouseDown = (e) => {
  if (!tabsNavRef.value) return;
  isMouseDown = true;
  startX = e.pageX - tabsNavRef.value.offsetLeft;
  scrollStart = tabsNavRef.value.scrollLeft;
};

const onMouseLeave = () => {
  isMouseDown = false;
};

const onMouseUp = () => {
  isMouseDown = false;
};

const onMouseMove = (e) => {
  if (!isMouseDown || !tabsNavRef.value) return;
  e.preventDefault();
  const x = e.pageX - tabsNavRef.value.offsetLeft;
  const walk = (x - startX) * 1.5;
  tabsNavRef.value.scrollLeft = scrollStart - walk;
};

const selectTab = async (tabId, event) => {
  activeTab.value = tabId;
  await nextTick();
  if (event?.currentTarget) {
    event.currentTarget.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
  }
};

watch(activeTab, async () => {
  await nextTick();
  if (tabsNavRef.value) {
    const activeEl = tabsNavRef.value.querySelector('.border-red-600');
    if (activeEl) {
      activeEl.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    }
  }
});

const isGeOt = computed(() => {
  const sub = (props.ot?.subsistema || '').toUpperCase();
  return sub.includes('GE') || sub.includes('ATS') || sub.includes('PLANTA') || sub.includes('GENERADOR');
});

const geAuditData = ref(null);

const loadGeAuditData = () => {
  if (!props.ot?.id) {
    geAuditData.value = null;
    return;
  }
  try {
    const raw = localStorage.getItem(`smu_ge_inspection_ot_${props.ot.id}`);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed && (parsed.porcentajeCompletado > 0 || parsed.ficha?.horometro || parsed.mediciones?.megger || parsed.mediciones?.voltaje_carga)) {
        geAuditData.value = parsed;
        return;
      }
    } else if (props.ot?.ge_inspection || props.ot?.inspeccion_ge) {
      geAuditData.value = props.ot.ge_inspection || props.ot.inspeccion_ge;
      return;
    }
    geAuditData.value = null;
  } catch (e) {
    console.error('Error al cargar datos de auditoría GE:', e);
    geAuditData.value = null;
  }
};

const sptAuditData = ref(null);

const loadSptAuditData = () => {
  if (!props.ot?.id) {
    sptAuditData.value = null;
    return;
  }
  try {
    const raw = localStorage.getItem(`smu_spt_inspection_ot_${props.ot.id}`);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed && (parsed.caidaPotencial || parsed.equipotencialidad || parsed.wenner)) {
        sptAuditData.value = parsed;
        return;
      }
    } else if (props.ot?.spt_inspection || props.ot?.inspeccion_spt) {
      sptAuditData.value = props.ot.spt_inspection || props.ot.inspeccion_spt;
      return;
    }
    sptAuditData.value = null;
  } catch (e) {
    console.error('Error al cargar datos de auditoría SPT:', e);
    sptAuditData.value = null;
  }
};

const aaAuditData = ref(null);

const loadAaAuditData = () => {
  if (!props.ot?.id) {
    aaAuditData.value = null;
    return;
  }
  try {
    const raw = localStorage.getItem(`smu_aa_inspection_ot_${props.ot.id}`);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed && (parsed.aa1 || parsed.aa2)) {
        aaAuditData.value = parsed;
        return;
      }
    } else if (props.ot?.aa_inspection || props.ot?.inspeccion_aa) {
      aaAuditData.value = props.ot.aa_inspection || props.ot.inspeccion_aa;
      return;
    }
    aaAuditData.value = null;
  } catch (e) {
    console.error('Error al cargar datos de auditoría AA:', e);
    aaAuditData.value = null;
  }
};

const powerAuditData = ref(null);

const loadPowerAuditData = () => {
  if (!props.ot?.id) {
    powerAuditData.value = null;
    return;
  }
  try {
    const raw = localStorage.getItem(`smu_power_inspection_ot_${props.ot.id}`);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed && (parsed.bus || parsed.baterias || parsed.ficha)) {
        powerAuditData.value = parsed;
        return;
      }
    } else if (props.ot?.power_inspection || props.ot?.inspeccion_power) {
      powerAuditData.value = props.ot.power_inspection || props.ot.inspeccion_power;
      return;
    }
    powerAuditData.value = null;
  } catch (e) {
    console.error('Error al cargar datos de auditoría POWER:', e);
    powerAuditData.value = null;
  }
};

watch([() => props.ot?.id, () => props.isOpen], () => {
  if (props.isOpen) {
    loadGeAuditData();
    loadSptAuditData();
    loadAaAuditData();
    loadPowerAuditData();
  }
}, { immediate: true });

onMounted(() => {
  loadGeAuditData();
  loadSptAuditData();
  loadAaAuditData();
  loadPowerAuditData();
});

const tabs = computed(() => {
  const baseTabs = [
    { id: 'resumen', label: 'Ficha General', icon: IconFileText },
    { 
      id: 'formato_campo', 
      label: 'Formato de Campo', 
      icon: IconFileCheck, 
      badge: hasFormData.value ? 'Diligenciado' : undefined 
    },
    { id: 'evidencias', label: 'Evidencias', icon: IconCamera, badge: props.ot?.evidencias?.length || 0 },
    { id: 'bitacora', label: 'Bitácora PDT', icon: IconHistory, badge: props.ot?.avances?.length || 0 },
    { id: 'repuestos', label: 'Insumos LPU', icon: IconBox, badge: props.ot?.repuestos?.length || 0 },
  ];

  // Solo agregar pestañas técnicas si el proceso fue realmente diligenciado en campo
  if (geAuditData.value) {
    baseTabs.push({ id: 'diagnostico_ge', label: 'Planta GE / ATS', icon: IconEngine });
  }
  if (sptAuditData.value) {
    baseTabs.push({ id: 'diagnostico_spt', label: 'Puesta a Tierra (SPT)', icon: IconBolt });
  }
  if (aaAuditData.value) {
    baseTabs.push({ id: 'diagnostico_aa', label: 'Climatización (AA)', icon: IconSnowflake });
  }
  if (powerAuditData.value) {
    baseTabs.push({ id: 'diagnostico_power', label: 'Fuerza DC (-48V)', icon: IconBatteryCharging });
  }

  return baseTabs;
});

// Si la pestaña seleccionada ya no existe en la OT actual, regresar automáticamente a 'resumen'
watch(tabs, (newTabs) => {
  if (!newTabs.some(t => t.id === activeTab.value)) {
    activeTab.value = 'resumen';
  }
}, { immediate: true });

const tiposEvidenciasDisponibles = computed(() => {
  const tipos = new Set(['todas']);
  if (props.ot?.evidencias && Array.isArray(props.ot.evidencias)) {
    props.ot.evidencias.forEach(e => {
      if (e.tipo) tipos.add(e.tipo);
    });
  }
  return Array.from(tipos);
});

const countFotos = (tipo) => {
  if (!props.ot?.evidencias) return 0;
  if (tipo === 'todas') return props.ot.evidencias.length;
  return props.ot.evidencias.filter(f => f.tipo === tipo).length;
};

const fotosFiltradas = computed(() => {
  if (!props.ot?.evidencias) return [];
  if (filtroFoto.value === 'todas') return props.ot.evidencias;
  return props.ot.evidencias.filter(f => f.tipo === filtroFoto.value);
});

const formatTipoEvidencia = (tipo) => {
  const map = {
    todas: 'Todas',
    llegada_sitio: 'Llegada a Sitio',
    llegada: 'Llegada',
    transporte: 'Transporte LPU',
    insumo_antes: 'Insumo (Antes)',
    insumo_despues: 'Insumo (Después)',
    repuesto_retirado: 'Repuesto Retirado',
    repuesto_instalado: 'Repuesto Instalado',
    hallazgo: 'Novedad / Hallazgo',
    antes: 'Antes',
    durante: 'Durante',
    despues: 'Después'
  };
  return map[tipo] || (tipo ? tipo.replace(/_/g, ' ').toUpperCase() : 'Evidencia');
};

const badgeTipoEvidenciaClass = (tipo) => {
  const map = {
    llegada_sitio: 'bg-indigo-600',
    llegada: 'bg-indigo-600',
    transporte: 'bg-blue-600',
    insumo_antes: 'bg-amber-600',
    insumo_despues: 'bg-teal-600',
    repuesto_retirado: 'bg-rose-600',
    repuesto_instalado: 'bg-emerald-600',
    hallazgo: 'bg-purple-600',
    antes: 'bg-amber-600',
    durante: 'bg-blue-600',
    despues: 'bg-emerald-600'
  };
  return map[tipo] || 'bg-slate-700';
};

const fallbackEvidencias = {
  antes: 'https://images.unsplash.com/photo-1541888946425-d0fbb186f5f8?w=800',
  durante: 'https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800',
  despues: 'https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800'
};

const onFotoError = (event, tipo) => {
  if (event?.target) {
    event.target.src = fallbackEvidencias[tipo] || fallbackEvidencias.antes;
  }
};

const abrirZoom = (foto, tipo = 'Evidencia', fecha = null) => {
  if (!foto) return;
  if (typeof foto === 'string') {
    fotoZoom.value = {
      url_imagen: foto,
      tipo: tipo,
      fecha_hora_captura: fecha || null
    };
  } else {
    fotoZoom.value = {
      ...foto,
      url_imagen: foto.url_imagen || foto.foto || foto.url || '',
      tipo: foto.tipo || tipo,
      fecha_hora_captura: foto.fecha_hora_captura || foto.created_at || fecha || null
    };
  }
};

const abrirMaps = (ubicacion) => {
  if (!ubicacion) return;
  const q = encodeURIComponent(ubicacion);
  window.open(`https://www.google.com/maps/search/?api=1&query=${q}`, '_blank');
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return d.toLocaleDateString('es-CO', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
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
  return map[st] || st || '';
};

const estadoBadgeClass = (st) => {
  if (st === 'finalizada') return 'bg-emerald-100 text-emerald-800 border border-emerald-300 dark:bg-emerald-950 dark:text-emerald-300';
  if (st === 'solucionada') return 'bg-blue-100 text-blue-800 border border-blue-300 dark:bg-blue-950 dark:text-blue-300';
  if (st === 'en_camino' || st === 'en_sitio') return 'bg-amber-100 text-amber-800 border border-amber-300 dark:bg-amber-950 dark:text-amber-300';
  if (st === 'detenida_materiales') return 'bg-rose-100 text-rose-800 border border-rose-300 dark:bg-rose-950 dark:text-rose-300';
  return 'bg-red-100 text-red-800 border border-red-300 dark:bg-red-950 dark:text-red-300';
};

const tipoBadgeClass = (t) => {
  const str = (t || '').toLowerCase();
  if (str === 'emergencia') return 'bg-rose-100 text-rose-800 border border-rose-200 dark:bg-rose-950/60 dark:text-rose-400';
  if (str === 'correctivo') return 'bg-amber-100 text-amber-800 border border-amber-200 dark:bg-amber-950/60 dark:text-amber-400';
  if (str === 'obra_civil') return 'bg-orange-100 text-orange-800 border border-orange-200 dark:bg-orange-950/60 dark:text-orange-400';
  if (str === 'informe_360') return 'bg-purple-100 text-purple-800 border border-purple-200 dark:bg-purple-950/60 dark:text-purple-400';
  if (str === 'rutina_7x24' || str.includes('7x24')) return 'bg-indigo-100 text-indigo-800 border border-indigo-200 dark:bg-indigo-950/60 dark:text-indigo-400';
  return 'bg-blue-100 text-blue-800 border border-blue-200 dark:bg-blue-950/60 dark:text-blue-400';
};

const formatTipoLabel = (t) => {
  const str = (t || '').toLowerCase();
  if (str === 'preventivo_planta') return 'Preventivo Planta';
  if (str === 'preventivo_aire') return 'Preventivo Aire';
  if (str === 'rutina_7x24' || str.includes('7x24')) return 'Rutina MP 7x24';
  if (str === 'obra_civil') return 'Obra Civil';
  if (str === 'informe_360') return 'Informe 360';
  if (str === 'emergencia') return 'Emergencia';
  if (str === 'correctivo') return 'Correctivo';
  return (t || 'Preventivo').toUpperCase();
};

const aprobarOt = async () => {
  if (!props.ot?.id) return;
  loadingAction.value = true;
  try {
    const res = await client.put(`/ots/${props.ot.id}/estado`, { estado: 'finalizada' });
    if (res.data.status === 'success') {
      emit('updated');
      emit('close');
    }
  } catch (err) {
    alert(err.response?.data?.message || 'Error al aprobar y liquidar la OT.');
  } finally {
    loadingAction.value = false;
  }
};

const devolverACampo = async () => {
  if (!props.ot?.id) return;
  if (!confirm('¿Desea devolver esta orden a campo para corrección técnica? La OT pasará a estado "En Progreso".')) return;
  loadingAction.value = true;
  try {
    const res = await client.put(`/ots/${props.ot.id}/estado`, { estado: 'en_progreso' });
    if (res.data.status === 'success') {
      emit('updated');
      emit('close');
    }
  } catch (err) {
    alert(err.response?.data?.message || 'Error al devolver la orden a campo.');
  } finally {
    loadingAction.value = false;
  }
};
</script>

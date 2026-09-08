<template>
  <Teleport to="body">
    <div v-if="isOpen" class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-3 sm:p-4 overflow-y-auto">
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl w-full max-w-4xl max-h-[92vh] flex flex-col overflow-hidden shadow-2xl transition-colors duration-300 my-auto">
        
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

        <!-- Pestañas del Expediente -->
        <div class="border-b border-slate-200 dark:border-white/10 px-5 pt-2 bg-slate-50/30 dark:bg-[#0a0b10] shrink-0">
          <div class="flex gap-1 sm:gap-2 overflow-x-auto select-none">
            <button
              v-for="t in tabs"
              :key="t.id"
              @click="activeTab = t.id"
              class="px-3 py-2 rounded-t-xl text-xs font-bold transition-all border-b-2 flex items-center gap-1.5 whitespace-nowrap"
              :class="activeTab === t.id 
                ? 'border-red-600 text-red-600 dark:text-red-400 bg-white dark:bg-[#121215]' 
                : 'border-transparent text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-white/5'"
            >
              <component :is="t.icon" class="w-4 h-4 stroke-[2]" />
              <span>{{ t.label }}</span>
              <span 
                v-if="t.badge !== undefined" 
                class="px-1.5 py-0.2 rounded-full text-[10px] font-mono font-black"
                :class="activeTab === t.id ? 'bg-red-500/15 text-red-600 dark:text-red-400' : 'bg-slate-200 dark:bg-white/10 text-slate-600 dark:text-slate-400'"
              >
                {{ t.badge }}
              </span>
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
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase" :class="tipoBadgeClass(ot?.tipo_mantenimiento)">
                    {{ ot?.tipo_mantenimiento || 'Preventivo' }}
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

          <!-- PESTAÑA 2: EVIDENCIAS FOTOGRÁFICAS -->
          <div v-if="activeTab === 'evidencias'" class="space-y-4">
            <!-- Filtro rápido por tipo de evidencia -->
            <div class="flex items-center justify-between flex-wrap gap-2">
              <div class="flex gap-1.5">
                <button
                  v-for="tipo in ['todas', 'antes', 'durante', 'despues']"
                  :key="tipo"
                  @click="filtroFoto = tipo"
                  class="px-2.5 py-1 rounded-lg text-xs font-bold uppercase transition-all"
                  :class="filtroFoto === tipo 
                    ? 'bg-red-600 text-white shadow-xs' 
                    : 'bg-slate-100 dark:bg-white/5 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-white/10'"
                >
                  {{ tipo }} ({{ countFotos(tipo) }})
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
                    class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div class="absolute top-2 left-2">
                    <span 
                      class="px-2 py-0.5 rounded-md text-[10px] font-black uppercase text-white shadow-md tracking-wider"
                      :class="foto.tipo === 'antes' ? 'bg-amber-600' : foto.tipo === 'durante' ? 'bg-blue-600' : 'bg-emerald-600'"
                    >
                      {{ foto.tipo }}
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
        <img :src="fotoZoom.url_imagen" class="max-w-full max-h-[75vh] object-contain rounded-xl shadow-2xl border border-white/10" />
        <div class="mt-3 flex items-center justify-between w-full text-white text-xs px-2">
          <div class="space-x-2">
            <span class="px-2 py-0.5 rounded uppercase font-black" :class="fotoZoom.tipo === 'antes' ? 'bg-amber-600' : fotoZoom.tipo === 'durante' ? 'bg-blue-600' : 'bg-emerald-600'">
              {{ fotoZoom.tipo }}
            </span>
            <span class="font-mono text-slate-300">{{ formatDate(fotoZoom.fecha_hora_captura || fotoZoom.created_at) }}</span>
          </div>
          <button @click="fotoZoom = null" class="px-3 py-1 bg-white/20 hover:bg-white/30 rounded-lg text-xs font-bold">
            Cerrar Zoom
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed } from 'vue';
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
  IconDeviceMobile
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

const tabs = computed(() => [
  { id: 'resumen', label: 'Ficha General', icon: IconFileText },
  { id: 'evidencias', label: 'Fotos Evidencia', icon: IconCamera, badge: props.ot?.evidencias?.length || 0 },
  { id: 'bitacora', label: 'Bitácora PDT', icon: IconHistory, badge: props.ot?.avances?.length || 0 },
  { id: 'repuestos', label: 'Insumos LPU', icon: IconBox, badge: props.ot?.repuestos?.length || 0 },
]);

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

const abrirZoom = (foto) => {
  fotoZoom.value = foto;
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
  if (t === 'emergencia') return 'bg-rose-100 text-rose-800 border border-rose-200 dark:bg-rose-950/60 dark:text-rose-400';
  if (t === 'correctivo') return 'bg-amber-100 text-amber-800 border border-amber-200 dark:bg-amber-950/60 dark:text-amber-400';
  return 'bg-blue-100 text-blue-800 border border-blue-200 dark:bg-blue-950/60 dark:text-blue-400';
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

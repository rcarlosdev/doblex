<script setup>
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from '@/components/ui/table';
import { 
  IconTower, 
  IconMapPin, 
  IconInfoCircle, 
  IconRuler2, 
  IconMail, 
  IconRefresh,
  IconChevronLeft,
  IconChevronRight
} from '@tabler/icons-vue';

defineProps({
  sitios: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  page: {
    type: Number,
    default: 1
  },
  pages: {
    type: Number,
    default: 1
  },
  limit: {
    type: Number,
    default: 25
  }
});

const emit = defineEmits(['view-detail', 'update:page', 'update:limit']);
</script>

<template>
  <Card class="bg-white dark:bg-[#121215] border-neutral-200 dark:border-white/10 shadow-sm overflow-hidden">
    <div class="overflow-x-auto">
      <Table>
        <TableHeader class="bg-neutral-50 dark:bg-white/[0.02]">
          <TableRow class="border-b border-neutral-200 dark:border-white/10">
            <TableHead class="font-bold text-[11px] uppercase tracking-wider text-neutral-500">Sitio / Estación Base</TableHead>
            <TableHead class="font-bold text-[11px] uppercase tracking-wider text-neutral-500">Zona & Técnica</TableHead>
            <TableHead class="font-bold text-[11px] uppercase tracking-wider text-neutral-500">Municipio / Base</TableHead>
            <TableHead class="font-bold text-[11px] uppercase tracking-wider text-neutral-500">Estructura & Altura</TableHead>
            <TableHead class="font-bold text-[11px] uppercase tracking-wider text-neutral-500">Transporte & LPU</TableHead>
            <TableHead class="font-bold text-[11px] uppercase tracking-wider text-neutral-500">Contacto / Supervisor</TableHead>
            <TableHead class="text-right font-bold text-[11px] uppercase tracking-wider text-neutral-500">Acción</TableHead>
          </TableRow>
        </TableHeader>

        <TableBody>
          <!-- Estado cargando -->
          <TableRow v-if="loading">
            <TableCell colspan="7" class="h-32 text-center text-neutral-400">
              <div class="flex flex-col items-center justify-center gap-2">
                <IconRefresh class="w-6 h-6 animate-spin text-primary" />
                <span class="text-xs font-semibold">Consultando base de datos de sitios...</span>
              </div>
            </TableCell>
          </TableRow>

          <!-- Estado vacío -->
          <TableRow v-else-if="sitios.length === 0">
            <TableCell colspan="7" class="h-32 text-center text-neutral-400">
              <div class="flex flex-col items-center justify-center gap-1">
                <IconTower class="w-8 h-8 opacity-40 mb-1" />
                <span class="text-sm font-bold text-neutral-700 dark:text-neutral-300">No se encontraron sitios</span>
                <span class="text-xs text-neutral-500">Intente modificar los términos de búsqueda o filtros seleccionados.</span>
              </div>
            </TableCell>
          </TableRow>

          <!-- Filas de datos -->
          <TableRow 
            v-else 
            v-for="s in sitios" 
            :key="s.id"
            class="border-b border-neutral-100 dark:border-white/5 hover:bg-neutral-50/80 dark:hover:bg-white/[0.02] transition-colors"
          >
            <!-- Nombre y código -->
            <TableCell class="py-3">
              <div class="flex items-center gap-2.5">
                <div class="p-1.5 bg-primary/10 text-primary rounded-lg shrink-0">
                  <IconTower class="w-4 h-4" />
                </div>
                <div>
                  <span class="font-bold text-xs text-neutral-900 dark:text-white block hover:text-primary transition-colors cursor-pointer" @click="emit('view-detail', s)">
                    {{ s.nombre }}
                  </span>
                  <span v-if="s.total_ots > 0" class="text-[10px] text-emerald-600 dark:text-emerald-400 font-semibold">
                    {{ s.total_ots }} {{ s.total_ots === 1 ? 'OT vinculada' : 'OTs vinculadas' }}
                  </span>
                  <span v-else class="text-[10px] text-neutral-400">Sin OTs activas</span>
                </div>
              </div>
            </TableCell>

            <!-- Zona y Zona Técnica -->
            <TableCell class="py-3">
              <div class="flex flex-col gap-1 items-start">
                <Badge 
                  :class="s.zona === 'NORTE' ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20' : 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20'"
                  class="text-[10px] font-bold px-2 py-0.5"
                >
                  {{ s.zona || 'N/A' }}
                </Badge>
                <span v-if="s.zona_tecnica && !s.zona_tecnica.includes('#')" class="text-[11px] text-neutral-500 dark:text-neutral-400 font-medium">
                  {{ s.zona_tecnica }}
                </span>
                <span v-else class="text-[10px] text-neutral-400 italic">Sin zona técnica</span>
              </div>
            </TableCell>

            <!-- Municipio y Ciudad Base -->
            <TableCell class="py-3">
              <div>
                <span class="text-xs font-semibold text-neutral-800 dark:text-neutral-200 block">
                  {{ s.municipio || 'No especificado' }}
                </span>
                <span class="text-[10px] text-neutral-400 flex items-center gap-1 mt-0.5">
                  <IconMapPin class="w-3 h-3 shrink-0" />
                  Base: {{ s.ciudad_base || '-' }}
                </span>
              </div>
            </TableCell>

            <!-- Estructura y Altura -->
            <TableCell class="py-3">
              <div>
                <span class="text-xs font-medium text-neutral-800 dark:text-neutral-200 block">
                  {{ s.estructura || 'Sin estructura' }}
                </span>
                <span v-if="s.altura_estructura" class="text-[10px] font-bold text-primary flex items-center gap-1 mt-0.5">
                  <IconRuler2 class="w-3 h-3 shrink-0" />
                  {{ s.altura_estructura }} metros
                </span>
                <span v-else-if="s.altura_estructura_texto" class="text-[10px] text-neutral-400">
                  {{ s.altura_estructura_texto }}
                </span>
              </div>
            </TableCell>

            <!-- Transporte LPU y Especial -->
            <TableCell class="py-3">
              <div class="space-y-1">
                <span v-if="s.codigo_transporte_lpu" class="text-[11px] font-mono font-medium text-neutral-700 dark:text-neutral-300 block line-clamp-1" :title="s.codigo_transporte_lpu">
                  LPU: {{ s.codigo_transporte_lpu }}
                </span>
                <Badge 
                  v-if="s.transporte_especial && s.transporte_especial !== '0' && s.transporte_especial !== 'N/A'" 
                  variant="outline"
                  class="text-[9px] font-bold border-purple-500/30 text-purple-600 dark:text-purple-400 bg-purple-500/5 block truncate max-w-[150px]"
                  :title="s.transporte_especial"
                >
                  {{ s.transporte_especial }}
                </Badge>
                <span v-if="s.km !== null && s.km !== undefined" class="text-[10px] text-neutral-400 block">
                  Distancia: {{ s.km }} km
                </span>
              </div>
            </TableCell>

            <!-- Supervisor Claro -->
            <TableCell class="py-3">
              <div class="text-[11px]">
                <span class="font-medium text-neutral-800 dark:text-neutral-200 block truncate max-w-[160px]" :title="s.supervisor_operativo">
                  {{ s.supervisor_operativo || '-' }}
                </span>
                <a 
                  v-if="s.correo_so" 
                  :href="`mailto:${s.correo_so}`"
                  class="text-[10px] text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1 mt-0.5 truncate max-w-[160px]"
                  :title="s.correo_so"
                >
                  <IconMail class="w-3 h-3 shrink-0" />
                  {{ s.correo_so }}
                </a>
              </div>
            </TableCell>

            <!-- Botón Acción -->
            <TableCell class="py-3 text-right">
              <Button 
                variant="ghost" 
                size="sm" 
                @click="emit('view-detail', s)"
                class="h-8 text-xs font-semibold text-primary hover:bg-primary/10"
              >
                <IconInfoCircle class="w-4 h-4 mr-1" />
                Ver Ficha
              </Button>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>

    <!-- Paginador Inferior -->
    <div class="p-4 border-t border-neutral-100 dark:border-white/5 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs">
      <div class="flex items-center gap-2 text-neutral-500">
        <span>Registros por página:</span>
        <select 
          :value="limit" 
          @change="emit('update:limit', Number($event.target.value))"
          class="h-8 rounded border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-2 text-neutral-800 dark:text-neutral-300 focus:outline-none focus:border-primary"
        >
          <option :value="15">15</option>
          <option :value="25">25</option>
          <option :value="50">50</option>
          <option :value="100">100</option>
        </select>
        <span class="ml-2">Página {{ page }} de {{ pages }}</span>
      </div>

      <div class="flex items-center gap-1.5">
        <Button 
          variant="outline" 
          size="sm" 
          :disabled="page <= 1 || loading"
          @click="emit('update:page', page - 1)"
          class="h-8 px-3 border-neutral-200 dark:border-white/10 text-xs font-medium"
        >
          <IconChevronLeft class="w-3.5 h-3.5 mr-1" />
          Anterior
        </Button>

        <span class="px-2 font-bold text-neutral-700 dark:text-neutral-300">{{ page }}</span>

        <Button 
          variant="outline" 
          size="sm" 
          :disabled="page >= pages || loading"
          @click="emit('update:page', page + 1)"
          class="h-8 px-3 border-neutral-200 dark:border-white/10 text-xs font-medium"
        >
          Siguiente
          <IconChevronRight class="w-3.5 h-3.5 ml-1" />
        </Button>
      </div>
    </div>
  </Card>
</template>

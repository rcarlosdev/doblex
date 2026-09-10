<script setup>
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  IconTower, 
  IconMapPin, 
  IconTruck, 
  IconUser, 
  IconMail, 
  IconX 
} from '@tabler/icons-vue';

defineProps({
  show: {
    type: Boolean,
    default: false
  },
  sitio: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['close']);
</script>

<template>
  <Teleport to="body">
    <div 
      v-if="show && sitio" 
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-in fade-in duration-200 !m-0"
    >
      <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl w-full max-w-2xl overflow-hidden shadow-2xl animate-in zoom-in-95 duration-200 max-h-[90vh] flex flex-col">
        <!-- Cabecera modal -->
        <div class="p-5 border-b border-neutral-100 dark:border-white/10 flex items-center justify-between bg-neutral-50/50 dark:bg-white/[0.02]">
          <div class="flex items-center gap-3">
            <div class="p-2 bg-primary/10 text-primary rounded-xl">
              <IconTower class="w-5 h-5" />
            </div>
            <div>
              <h2 class="text-base font-black text-neutral-900 dark:text-white">
                {{ sitio.nombre }}
              </h2>
              <div class="flex items-center gap-2 mt-0.5">
                <Badge :class="sitio.zona === 'NORTE' ? 'bg-emerald-500/10 text-emerald-600 border-emerald-500/20' : 'bg-amber-500/10 text-amber-600 border-amber-500/20'" class="text-[10px] font-bold">
                  Zona {{ sitio.zona }}
                </Badge>
                <span v-if="sitio.zona_tecnica && !sitio.zona_tecnica.includes('#')" class="text-xs text-neutral-500">
                  {{ sitio.zona_tecnica }}
                </span>
              </div>
            </div>
          </div>
          <button @click="emit('close')" class="p-1 rounded-lg hover:bg-neutral-100 dark:hover:bg-white/5 text-neutral-400 hover:text-neutral-700 dark:hover:text-white">
            <IconX class="w-5 h-5" />
          </button>
        </div>

        <!-- Contenido modal -->
        <div class="p-6 overflow-y-auto space-y-6 text-xs flex-1">
          <!-- 1. Ubicación y Geografía -->
          <div class="space-y-3">
            <h3 class="text-[11px] font-bold uppercase tracking-wider text-primary flex items-center gap-1.5">
              <IconMapPin class="w-4 h-4" />
              1. Localización y Ubicación Física
            </h3>
            <div class="grid grid-cols-2 gap-3 bg-neutral-50 dark:bg-white/[0.02] p-3.5 rounded-xl border border-neutral-200/60 dark:border-white/5">
              <div>
                <span class="text-neutral-400 block text-[10px] font-semibold uppercase">Municipio</span>
                <span class="font-bold text-neutral-800 dark:text-neutral-200">{{ sitio.municipio || 'No registrado' }}</span>
              </div>
              <div>
                <span class="text-neutral-400 block text-[10px] font-semibold uppercase">Ciudad Base de Despacho</span>
                <span class="font-bold text-neutral-800 dark:text-neutral-200">{{ sitio.ciudad_base || 'No registrada' }}</span>
              </div>
              <div class="col-span-2 pt-2 border-t border-neutral-100 dark:border-white/5">
                <span class="text-neutral-400 block text-[10px] font-semibold uppercase">Dirección / Georreferencia</span>
                <span class="text-neutral-800 dark:text-neutral-200 font-medium leading-relaxed">{{ sitio.ubicacion || 'Sin dirección física registrada en el maestro' }}</span>
              </div>
            </div>
          </div>

          <!-- 2. Logística, Transporte y Facturación -->
          <div class="space-y-3">
            <h3 class="text-[11px] font-bold uppercase tracking-wider text-primary flex items-center gap-1.5">
              <IconTruck class="w-4 h-4" />
              2. Logística, Transporte Contractual y Facturación
            </h3>
            <div class="grid grid-cols-2 gap-3 bg-neutral-50 dark:bg-white/[0.02] p-3.5 rounded-xl border border-neutral-200/60 dark:border-white/5">
              <div>
                <span class="text-neutral-400 block text-[10px] font-semibold uppercase">Distancia desde Base</span>
                <span class="font-bold text-neutral-800 dark:text-neutral-200">
                  {{ sitio.km ? `${sitio.km} Km` : (sitio.km_texto || 'No especificado') }}
                </span>
              </div>
              <div>
                <span class="text-neutral-400 block text-[10px] font-semibold uppercase">Analista de Facturación</span>
                <span class="font-bold text-neutral-800 dark:text-neutral-200">{{ sitio.facturadora || 'Sin asignar' }}</span>
              </div>
              <div class="col-span-2 pt-2 border-t border-neutral-100 dark:border-white/5">
                <span class="text-neutral-400 block text-[10px] font-semibold uppercase">Código(s) Transporte LPU</span>
                <span class="font-mono font-bold text-neutral-800 dark:text-neutral-200">{{ sitio.codigo_transporte_lpu || 'No aplica' }}</span>
              </div>
              <div v-if="sitio.transporte_especial && sitio.transporte_especial !== '0' && sitio.transporte_especial !== 'N/A'" class="col-span-2 pt-2 border-t border-neutral-100 dark:border-white/5">
                <span class="text-neutral-400 block text-[10px] font-semibold uppercase">Transporte Especial Requerido</span>
                <Badge class="bg-purple-500/10 text-purple-600 dark:text-purple-400 border-purple-500/20 font-bold mt-0.5">
                  {{ sitio.transporte_especial }}
                </Badge>
              </div>
            </div>
          </div>

          <!-- 3. Infraestructura y Seguridad en Alturas (SST) -->
          <div class="space-y-3">
            <h3 class="text-[11px] font-bold uppercase tracking-wider text-primary flex items-center gap-1.5">
              <IconTower class="w-4 h-4" />
              3. Infraestructura y Seguridad en Alturas (SST)
            </h3>
            <div class="grid grid-cols-2 gap-3 bg-neutral-50 dark:bg-white/[0.02] p-3.5 rounded-xl border border-neutral-200/60 dark:border-white/5">
              <div>
                <span class="text-neutral-400 block text-[10px] font-semibold uppercase">Tipo de Estructura</span>
                <span class="font-bold text-neutral-800 dark:text-neutral-200">{{ sitio.estructura || 'No clasificada' }}</span>
              </div>
              <div>
                <span class="text-neutral-400 block text-[10px] font-semibold uppercase">Altura de Estructura</span>
                <span v-if="sitio.altura_estructura" class="font-bold text-primary text-sm">
                  {{ sitio.altura_estructura }} metros
                </span>
                <span v-else class="text-neutral-500">
                  {{ sitio.altura_estructura_texto || 'No especificada' }}
                </span>
              </div>
            </div>
          </div>

          <!-- 4. Directorio de Contactos Claro -->
          <div class="space-y-3">
            <h3 class="text-[11px] font-bold uppercase tracking-wider text-primary flex items-center gap-1.5">
              <IconUser class="w-4 h-4" />
              4. Directorio Operativo de Contactos
            </h3>
            <div class="space-y-2 bg-neutral-50 dark:bg-white/[0.02] p-3.5 rounded-xl border border-neutral-200/60 dark:border-white/5">
              <!-- Supervisor Operativo -->
              <div class="flex items-center justify-between">
                <div>
                  <span class="text-[10px] text-neutral-400 block font-semibold uppercase">Supervisor Operativo (SO)</span>
                  <span class="font-bold text-neutral-800 dark:text-neutral-200">{{ sitio.supervisor_operativo || 'No asignado' }}</span>
                </div>
                <a v-if="sitio.correo_so && sitio.correo_so.includes('@') && !sitio.correo_so.includes('#')" :href="`mailto:${sitio.correo_so}`" class="text-blue-600 hover:underline flex items-center gap-1 text-[11px]">
                  <IconMail class="w-3.5 h-3.5" />
                  {{ sitio.correo_so }}
                </a>
              </div>

              <!-- Jefe de Zona -->
              <div class="flex items-center justify-between pt-2 border-t border-neutral-100 dark:border-white/5">
                <div>
                  <span class="text-[10px] text-neutral-400 block font-semibold uppercase">Jefe de Zona</span>
                  <span class="font-bold text-neutral-800 dark:text-neutral-200">{{ sitio.jefe_zona || 'No asignado' }}</span>
                </div>
                <a v-if="sitio.correo_jefe_zona && sitio.correo_jefe_zona.includes('@') && !sitio.correo_jefe_zona.includes('#')" :href="`mailto:${sitio.correo_jefe_zona}`" class="text-blue-600 hover:underline flex items-center gap-1 text-[11px]">
                  <IconMail class="w-3.5 h-3.5" />
                  {{ sitio.correo_jefe_zona }}
                </a>
              </div>

              <!-- Ingeniero de Soporte -->
              <div class="flex items-center justify-between pt-2 border-t border-neutral-100 dark:border-white/5">
                <div>
                  <span class="text-[10px] text-neutral-400 block font-semibold uppercase">Ingeniero de Soporte</span>
                  <span class="font-bold text-neutral-800 dark:text-neutral-200">{{ sitio.ingeniero_soporte || 'No asignado' }}</span>
                </div>
                <a v-if="sitio.correo_ing_soporte && sitio.correo_ing_soporte.includes('@') && !sitio.correo_ing_soporte.includes('#')" :href="`mailto:${sitio.correo_ing_soporte}`" class="text-blue-600 hover:underline flex items-center gap-1 text-[11px]">
                  <IconMail class="w-3.5 h-3.5" />
                  {{ sitio.correo_ing_soporte }}
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- Pie modal -->
        <div class="p-4 border-t border-neutral-100 dark:border-white/10 flex justify-end bg-neutral-50/50 dark:bg-white/[0.02]">
          <Button variant="outline" size="sm" @click="emit('close')" class="text-xs">
            Cerrar Ficha
          </Button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

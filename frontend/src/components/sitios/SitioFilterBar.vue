<script setup>
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { IconSearch, IconX } from '@tabler/icons-vue';

defineProps({
  filters: {
    type: Object,
    required: true
  },
  filterOptions: {
    type: Object,
    default: () => ({
      zonas: [],
      zonas_tecnicas: [],
      ciudades_base: [],
      estructuras: []
    })
  },
  currentCount: {
    type: Number,
    default: 0
  },
  totalCount: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(['search-input', 'reset']);
</script>

<template>
  <Card class="p-4 md:p-5 bg-white dark:bg-[#121215] border-neutral-200 dark:border-white/10 shadow-sm space-y-4">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
      <!-- Input de Búsqueda -->
      <div class="relative lg:col-span-2">
        <IconSearch class="absolute left-3 top-2.5 w-4 h-4 text-neutral-400" />
        <Input 
          type="text" 
          v-model="filters.search"
          @input="emit('search-input')"
          placeholder="Buscar por nombre, municipio, ubicación o código LPU..."
          class="pl-9 bg-neutral-50 dark:bg-[#0a0b10] border-neutral-200 dark:border-white/10 text-xs text-neutral-900 dark:text-white"
        />
      </div>

      <!-- Filtro Macro Zona -->
      <div>
        <select 
          v-model="filters.zona"
          class="h-9 w-full rounded-md border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 shadow-sm transition-colors focus-visible:outline-none focus:border-primary focus:ring-1 focus:ring-primary cursor-pointer"
        >
          <option value="">Todas las Zonas</option>
          <option v-for="z in filterOptions.zonas" :key="z" :value="z">{{ z }}</option>
        </select>
      </div>

      <!-- Filtro Zona Técnica -->
      <div>
        <select 
          v-model="filters.zona_tecnica"
          class="h-9 w-full rounded-md border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 shadow-sm transition-colors focus-visible:outline-none focus:border-primary focus:ring-1 focus:ring-primary cursor-pointer"
        >
          <option value="">Zona Técnica (Todas)</option>
          <option v-for="zt in filterOptions.zonas_tecnicas" :key="zt" :value="zt">{{ zt }}</option>
        </select>
      </div>

      <!-- Filtro Estructura -->
      <div>
        <select 
          v-model="filters.estructura"
          class="h-9 w-full rounded-md border border-neutral-200 dark:border-white/10 bg-neutral-50 dark:bg-[#0a0b10] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 shadow-sm transition-colors focus-visible:outline-none focus:border-primary focus:ring-1 focus:ring-primary cursor-pointer"
        >
          <option value="">Estructura (Todas)</option>
          <option v-for="est in filterOptions.estructuras" :key="est" :value="est">{{ est }}</option>
        </select>
      </div>
    </div>

    <!-- Indicador de filtros activos & Reset -->
    <div class="flex items-center justify-between pt-1 border-t border-neutral-100 dark:border-white/5 text-xs text-neutral-500">
      <div class="flex items-center gap-2">
        <span>Mostrando <strong>{{ currentCount }}</strong> de <strong>{{ totalCount.toLocaleString() }}</strong> sitios registrados</span>
      </div>
      <button 
        v-if="filters.search || filters.zona || filters.zona_tecnica || filters.estructura || filters.ciudad_base"
        @click="emit('reset')"
        class="text-primary hover:underline font-semibold flex items-center gap-1"
      >
        <IconX class="w-3.5 h-3.5" />
        Limpiar filtros
      </button>
    </div>
  </Card>
</template>

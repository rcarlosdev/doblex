<script setup>
import { Card } from '@/components/ui/card';
import { 
  IconTower, 
  IconMapPin, 
  IconTruck, 
  IconBuildingCommunity 
} from '@tabler/icons-vue';

defineProps({
  stats: {
    type: Object,
    default: () => ({
      total_sitios: 0,
      zonas: {},
      zonas_tecnicas: {},
      estructuras_principales: {},
      con_transporte_especial: 0
    })
  }
});
</script>

<template>
  <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
    <!-- Total Sitios -->
    <Card class="p-4 bg-white dark:bg-[#121215] border-neutral-200 dark:border-white/10 shadow-sm flex flex-col justify-between">
      <div class="flex items-center justify-between text-neutral-500 dark:text-neutral-400">
        <span class="text-xs font-bold uppercase tracking-wider">Total Sitios</span>
        <div class="p-1.5 bg-blue-500/10 text-blue-500 rounded-lg">
          <IconTower class="w-4 h-4" />
        </div>
      </div>
      <div class="mt-2">
        <span class="text-2xl font-black text-neutral-900 dark:text-white">
          {{ (stats.total_sitios || 0).toLocaleString() }}
        </span>
        <p class="text-[10px] text-neutral-400 mt-0.5">Estaciones Base activas</p>
      </div>
    </Card>

    <!-- Zona Norte -->
    <Card class="p-4 bg-white dark:bg-[#121215] border-neutral-200 dark:border-white/10 shadow-sm flex flex-col justify-between">
      <div class="flex items-center justify-between text-neutral-500 dark:text-neutral-400">
        <span class="text-xs font-bold uppercase tracking-wider">Zona Norte</span>
        <div class="p-1.5 bg-emerald-500/10 text-emerald-500 rounded-lg">
          <IconMapPin class="w-4 h-4" />
        </div>
      </div>
      <div class="mt-2">
        <span class="text-2xl font-black text-neutral-900 dark:text-white">
          {{ (stats.zonas?.['NORTE'] || 0).toLocaleString() }}
        </span>
        <p class="text-[10px] text-neutral-400 mt-0.5">Antioquia, Chocó y Eje Cafetero</p>
      </div>
    </Card>

    <!-- Zona Costa -->
    <Card class="p-4 bg-white dark:bg-[#121215] border-neutral-200 dark:border-white/10 shadow-sm flex flex-col justify-between">
      <div class="flex items-center justify-between text-neutral-500 dark:text-neutral-400">
        <span class="text-xs font-bold uppercase tracking-wider">Zona Costa</span>
        <div class="p-1.5 bg-amber-500/10 text-amber-500 rounded-lg">
          <IconBuildingCommunity class="w-4 h-4" />
        </div>
      </div>
      <div class="mt-2">
        <span class="text-2xl font-black text-neutral-900 dark:text-white">
          {{ (stats.zonas?.['COSTA'] || 0).toLocaleString() }}
        </span>
        <p class="text-[10px] text-neutral-400 mt-0.5">Atlántico, Bolívar, Córdoba, Sucre</p>
      </div>
    </Card>

    <!-- Transporte Especial -->
    <Card class="p-4 bg-white dark:bg-[#121215] border-neutral-200 dark:border-white/10 shadow-sm flex flex-col justify-between">
      <div class="flex items-center justify-between text-neutral-500 dark:text-neutral-400">
        <span class="text-xs font-bold uppercase tracking-wider">Transporte Especial</span>
        <div class="p-1.5 bg-purple-500/10 text-purple-500 rounded-lg">
          <IconTruck class="w-4 h-4" />
        </div>
      </div>
      <div class="mt-2">
        <span class="text-2xl font-black text-neutral-900 dark:text-white">
          {{ (stats.con_transporte_especial || 0).toLocaleString() }}
        </span>
        <p class="text-[10px] text-neutral-400 mt-0.5">Mular, fluvial, nocturno, ayudantía</p>
      </div>
    </Card>
  </div>
</template>

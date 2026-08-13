<template>
  <div class="bg-slate-900/80 border border-slate-800 rounded-xl p-4 space-y-3">
    <div class="flex items-center justify-between border-b border-slate-800 pb-2">
      <h4 class="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
        </svg>
        Checklist de Intervención: {{ subsistema }}
      </h4>
      <span class="text-xs text-blue-400 font-bold">{{ completadosCount }} / {{ tasks.length }}</span>
    </div>

    <div class="space-y-2">
      <div
        v-for="(task, idx) in tasks"
        :key="idx"
        @click="toggleTask(idx)"
        class="flex items-center justify-between p-2.5 rounded-lg border transition-all cursor-pointer select-none"
        :class="task.completado ? 'bg-emerald-950/20 border-emerald-500/30 text-emerald-200' : 'bg-slate-950/60 border-slate-800 text-slate-300 hover:border-slate-700'"
      >
        <div class="flex items-center gap-3">
          <div
            class="w-5 h-5 rounded flex items-center justify-center border transition-all"
            :class="task.completado ? 'bg-emerald-500 border-emerald-400 text-black' : 'border-slate-600 bg-slate-900'"
          >
            <svg v-if="task.completado" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 stroke-[3]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <div>
            <div class="text-xs font-semibold">{{ task.tarea }}</div>
            <div class="text-[10px] text-slate-400 font-mono">Acción: {{ task.accion }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  subsistema: {
    type: String,
    default: 'Mantenimiento General',
  },
});

const tasks = ref([
  { tarea: 'Inspección visual de bornes y conexiones', accion: 'Ajustar', completado: false },
  { tarea: 'Limpieza de filtros y disipadores de calor', accion: 'Limpiar', completado: false },
  { tarea: 'Verificación de tensión de batería / voltaje', accion: 'Probar', completado: false },
  { tarea: 'Reemplazo de fusibles dañados o desgastados', accion: 'Reemplazar', completado: false },
]);

const completadosCount = computed(() => {
  return tasks.value.filter(t => t.completado).length;
});

const toggleTask = (index) => {
  tasks.value[index].completado = !tasks.value[index].completado;
};
</script>

<template>
  <div :class="badgeClass" class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold shadow-sm transition-all">
    <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
    <span>{{ labelText }}</span>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  fechaLimite: {
    type: String,
    required: true,
  },
  estado: {
    type: String,
    default: 'asignada',
  },
});

const now = ref(new Date());
let timer = null;

onMounted(() => {
  timer = setInterval(() => {
    now.value = new Date();
  }, 30000); // Actualizar cada 30s
});

onUnmounted(() => {
  if (timer) clearInterval(timer);
});

const diffMinutes = computed(() => {
  if (!props.fechaLimite) return 0;
  const target = new Date(props.fechaLimite);
  return Math.floor((target - now.value) / (1000 * 60));
});

const isFinalizado = computed(() => {
  return ['solucionada', 'finalizada'].includes(props.estado);
});

const labelText = computed(() => {
  if (isFinalizado.value) return 'SLA Cumplido';
  if (!props.fechaLimite) return 'Sin SLA';
  
  const mins = diffMinutes.value;
  if (mins < 0) {
    const absMins = Math.abs(mins);
    const hrs = Math.floor(absMins / 60);
    const m = absMins % 60;
    return `¡Vencido por ${hrs}h ${m}m!`;
  } else {
    const hrs = Math.floor(mins / 60);
    const m = mins % 60;
    return `SLA: ${hrs}h ${m}m restantes`;
  }
});

const badgeClass = computed(() => {
  if (isFinalizado.value) {
    return 'bg-emerald-50 text-emerald-700 border border-emerald-300 dark:bg-emerald-950/40 dark:text-emerald-400 dark:border-emerald-500/30';
  }
  const mins = diffMinutes.value;
  if (mins < 0) {
    return 'bg-rose-50 text-rose-700 border border-rose-300 dark:bg-rose-950/60 dark:text-rose-400 dark:border-rose-500/50 animate-bounce';
  } else if (mins < 180) { // menos de 3h
    return 'bg-amber-50 text-amber-800 border border-amber-300 dark:bg-amber-950/50 dark:text-amber-300 dark:border-amber-500/40';
  } else {
    return 'bg-sky-50 text-sky-700 border border-sky-300 dark:bg-sky-950/40 dark:text-sky-300 dark:border-sky-500/30';
  }
});
</script>

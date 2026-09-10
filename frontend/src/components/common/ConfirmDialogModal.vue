<template>
  <Teleport to="body">
    <div v-if="isOpen" class="fixed inset-0 z-[120] bg-black/70 backdrop-blur-sm flex items-center justify-center p-3 sm:p-4 overflow-y-auto">
      <div class="bg-white dark:bg-[#121215] border border-slate-200 dark:border-white/10 rounded-2xl w-full max-w-md p-5 sm:p-6 space-y-4 shadow-2xl max-h-[90vh] overflow-y-auto my-auto transition-colors duration-300">
        <div class="flex items-center gap-3">
          <div :class="iconBgClass" class="w-10 h-10 rounded-xl flex items-center justify-center shrink-0 shadow-xs">
            <IconAlertTriangle v-if="type === 'warning'" class="w-5 h-5 text-amber-600 dark:text-amber-400 stroke-[2]" />
            <IconCircleCheck v-else-if="type === 'success'" class="w-5 h-5 text-emerald-600 dark:text-emerald-400 stroke-[2]" />
            <IconAlertCircle v-else-if="type === 'danger'" class="w-5 h-5 text-rose-600 dark:text-rose-400 stroke-[2]" />
            <IconInfoCircle v-else class="w-5 h-5 text-red-600 dark:text-red-400 stroke-[2]" />
          </div>
          <div>
            <h3 class="text-sm font-extrabold text-slate-900 dark:text-white leading-tight">{{ title }}</h3>
            <p class="text-[11px] text-slate-500 dark:text-slate-400 font-medium">{{ subtitle }}</p>
          </div>
        </div>

        <p class="text-xs text-slate-700 dark:text-slate-300 leading-relaxed font-medium bg-slate-50 dark:bg-[#0a0b10] p-3.5 rounded-xl border border-slate-200/80 dark:border-white/10">
          {{ message }}
        </p>

        <div class="flex items-center justify-end gap-2.5 pt-1">
          <button
            @click="$emit('cancel')"
            :disabled="loading"
            class="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-white/5 transition-colors"
          >
            {{ cancelText }}
          </button>
          <button
            @click="$emit('confirm')"
            :disabled="loading"
            :class="confirmBtnClass"
            class="px-4 py-2 rounded-xl text-xs font-bold text-white shadow-md active:scale-95 transition-all flex items-center gap-1.5"
          >
            <span>{{ loading ? 'Procesando...' : confirmText }}</span>
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue';
import { IconAlertTriangle, IconCircleCheck, IconAlertCircle, IconInfoCircle } from '@tabler/icons-vue';

const props = defineProps({
  isOpen: Boolean,
  title: { type: String, default: 'Confirmar Acción' },
  subtitle: { type: String, default: 'Por favor verifique antes de continuar' },
  message: { type: String, default: '¿Desea proceder con esta acción?' },
  confirmText: { type: String, default: 'Sí, Confirmar' },
  cancelText: { type: String, default: 'Cancelar' },
  type: { type: String, default: 'info' }, // 'info', 'warning', 'danger', 'success'
  loading: Boolean,
});

defineEmits(['confirm', 'cancel']);

const iconBgClass = computed(() => {
  if (props.type === 'danger') return 'bg-rose-100 dark:bg-rose-950/60 border border-rose-200 dark:border-rose-800';
  if (props.type === 'warning') return 'bg-amber-100 dark:bg-amber-950/60 border border-amber-200 dark:border-amber-800';
  if (props.type === 'success') return 'bg-emerald-100 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800';
  return 'bg-red-100 dark:bg-red-950/60 border border-red-200 dark:border-red-800';
});

const confirmBtnClass = computed(() => {
  if (props.type === 'danger') return 'bg-rose-600 hover:bg-rose-500 shadow-rose-600/20';
  if (props.type === 'warning') return 'bg-amber-600 hover:bg-amber-500 shadow-amber-600/20';
  if (props.type === 'success') return 'bg-emerald-600 hover:bg-emerald-500 shadow-emerald-600/20';
  return 'bg-red-600 hover:bg-red-500 shadow-red-600/20';
});
</script>

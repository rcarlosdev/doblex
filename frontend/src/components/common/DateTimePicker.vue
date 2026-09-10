<template>
  <div class="space-y-1.5">
    <div v-if="label" class="flex items-center justify-between">
      <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider flex items-center gap-1">
        <span>{{ label }}</span>
        <span v-if="required" class="text-rose-500 font-black">*</span>
      </label>
      <button 
        type="button" 
        @click="setNow" 
        class="text-[9px] font-bold text-primary hover:underline flex items-center gap-1 cursor-pointer transition-colors"
        title="Establecer fecha y hora actual"
      >
        <IconClock class="w-3 h-3" />
        <span>Ahora</span>
      </button>
    </div>

    <!-- Contenedor con Fecha y Hora separadas para selección con 1 clic en Calendario y Reloj -->
    <div class="grid grid-cols-5 gap-2">
      <!-- Selector de Fecha (3 columnas) con Calendario Emergente -->
      <div 
        class="col-span-3 relative flex items-center group cursor-pointer"
        @click="triggerDatePicker"
      >
        <IconCalendar class="w-4 h-4 text-neutral-400 group-hover:text-primary transition-colors absolute left-2.5 pointer-events-none stroke-[2]" />
        <input
          ref="dateInputRef"
          type="date"
          v-model="fechaPart"
          :required="required"
          :disabled="disabled"
          @change="emitCombinedValue"
          @click.stop="triggerDatePicker"
          class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-950 pl-8 pr-2 py-1 text-xs text-neutral-800 dark:text-neutral-200 font-medium cursor-pointer focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all [&::-webkit-calendar-picker-indicator]:cursor-pointer [&::-webkit-calendar-picker-indicator]:opacity-70 group-hover:[&::-webkit-calendar-picker-indicator]:opacity-100"
        />
      </div>

      <!-- Selector de Hora (2 columnas) con Reloj Emergente -->
      <div 
        class="col-span-2 relative flex items-center group cursor-pointer"
        @click="triggerTimePicker"
      >
        <IconClock class="w-3.5 h-3.5 text-neutral-400 group-hover:text-primary transition-colors absolute left-2.5 pointer-events-none stroke-[2]" />
        <input
          ref="timeInputRef"
          type="time"
          v-model="horaPart"
          :required="required"
          :disabled="disabled"
          @change="emitCombinedValue"
          @click.stop="triggerTimePicker"
          class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-950 pl-7 pr-1 py-1 text-xs text-neutral-800 dark:text-neutral-200 font-medium cursor-pointer focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all [&::-webkit-calendar-picker-indicator]:cursor-pointer [&::-webkit-calendar-picker-indicator]:opacity-70 group-hover:[&::-webkit-calendar-picker-indicator]:opacity-100"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { IconCalendar, IconClock } from '@tabler/icons-vue';

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  required: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue', 'change']);

const dateInputRef = ref(null);
const timeInputRef = ref(null);

const fechaPart = ref('');
const horaPart = ref('');

const pad = (n) => String(n).padStart(2, '0');

const parseValue = (val) => {
  if (!val) {
    const now = new Date();
    fechaPart.value = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
    horaPart.value = `${pad(now.getHours())}:${pad(now.getMinutes())}`;
    return;
  }

  if (val.includes('T')) {
    const [d, t] = val.split('T');
    fechaPart.value = d || '';
    horaPart.value = (t || '08:00').slice(0, 5);
  } else if (val.includes(' ')) {
    const [d, t] = val.split(' ');
    fechaPart.value = d || '';
    horaPart.value = (t || '08:00').slice(0, 5);
  } else {
    fechaPart.value = val;
    horaPart.value = '08:00';
  }
};

const emitCombinedValue = () => {
  if (!fechaPart.value) return;
  const hora = horaPart.value || '08:00';
  const combined = `${fechaPart.value}T${hora}`;
  emit('update:modelValue', combined);
  emit('change', combined);
};

const setNow = () => {
  const now = new Date();
  fechaPart.value = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
  horaPart.value = `${pad(now.getHours())}:${pad(now.getMinutes())}`;
  emitCombinedValue();
};

const triggerDatePicker = () => {
  if (props.disabled) return;
  if (dateInputRef.value && typeof dateInputRef.value.showPicker === 'function') {
    dateInputRef.value.showPicker();
  } else if (dateInputRef.value) {
    dateInputRef.value.focus();
  }
};

const triggerTimePicker = () => {
  if (props.disabled) return;
  if (timeInputRef.value && typeof timeInputRef.value.showPicker === 'function') {
    timeInputRef.value.showPicker();
  } else if (timeInputRef.value) {
    timeInputRef.value.focus();
  }
};

watch(() => props.modelValue, (newVal) => {
  parseValue(newVal);
});

onMounted(() => {
  parseValue(props.modelValue);
  if (!props.modelValue) {
    emitCombinedValue();
  }
});
</script>

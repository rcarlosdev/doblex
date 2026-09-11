<template>
  <div class="space-y-2 relative" ref="containerRef">
    <!-- Encabezado con Label y Contador -->
    <div class="flex items-center justify-between">
      <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider flex items-center gap-1.5">
        <span>{{ label }}</span>
        <span v-if="required" class="text-rose-500 font-black">*</span>
      </label>
      <span class="text-[10px] font-mono font-bold" :class="selectedEmpleados.length > 0 ? (multiple ? 'text-primary' : 'text-emerald-600 dark:text-emerald-400') : 'text-neutral-400'">
        <template v-if="multiple">
          {{ selectedEmpleados.length }} {{ selectedEmpleados.length === 1 ? roleLabel + ' asignado' : roleLabel + 's asignados' }}
        </template>
        <template v-else>
          {{ selectedEmpleados.length === 1 ? '1 ' + roleLabel + ' asignado' : 'Sin ' + roleLabel + ' asignado' }}
        </template>
      </span>
    </div>

    <!-- MODO SINGLE: Tarjeta del Empleado Seleccionado (Coordinador) -->
    <div 
      v-if="!multiple && selectedEmpleados.length > 0" 
      class="flex items-center justify-between p-2.5 bg-neutral-50 dark:bg-neutral-900/60 border border-neutral-200 dark:border-white/10 rounded-xl shadow-xs"
    >
      <div class="flex items-center gap-2.5 min-w-0">
        <div class="w-7 h-7 rounded-full flex items-center justify-center text-[10px] font-black shrink-0 bg-primary/10 text-primary border border-primary/20">
          {{ getInitials(selectedEmpleados[0].nombre || selectedEmpleados[0].name) }}
        </div>
        <div class="flex flex-col min-w-0">
          <div class="flex items-center gap-2">
            <span class="font-bold text-xs text-neutral-900 dark:text-white truncate">
              {{ selectedEmpleados[0].nombre || selectedEmpleados[0].name }}
            </span>
            <span v-if="selectedEmpleados[0].documento" class="text-[10px] font-mono font-bold text-neutral-600 dark:text-neutral-300 bg-neutral-200/60 dark:bg-neutral-800 px-1.5 py-0.2 rounded shrink-0">
              CC {{ selectedEmpleados[0].documento }}
            </span>
          </div>
          <span class="text-[10px] text-neutral-500 dark:text-neutral-400 truncate">
            {{ selectedEmpleados[0].cargo || (roleLabel === 'coordinador' ? 'Coordinador' : 'Empleado') }}
          </span>
        </div>
      </div>

      <div class="flex items-center gap-1 shrink-0">
        <button
          v-if="!disabled"
          type="button"
          @click.stop="removeEmpleado(0)"
          class="p-1 rounded-md hover:bg-rose-100 hover:text-rose-600 dark:hover:bg-rose-950/60 dark:hover:text-rose-400 text-neutral-400 transition-colors cursor-pointer"
          :title="'Quitar ' + roleLabel"
        >
          <IconX class="w-4 h-4 stroke-[2]" />
        </button>
      </div>
    </div>

    <!-- MODO MULTIPLE: Chips de Empleados Seleccionados (Operadores) -->
    <div v-if="multiple && selectedEmpleados.length > 0" class="flex flex-wrap gap-1.5 p-2 bg-neutral-50 dark:bg-neutral-900/60 border border-neutral-200 dark:border-white/10 rounded-xl">
      <div
        v-for="(emp, idx) in selectedEmpleados"
        :key="emp.id || emp.user_id || idx"
        class="inline-flex items-center gap-2 px-2.5 py-1.5 rounded-lg border text-xs shadow-xs transition-all animate-in fade-in bg-white dark:bg-[#18181b] border-neutral-200 dark:border-white/10 text-neutral-800 dark:text-neutral-200 hover:border-neutral-300 dark:hover:border-white/20"
      >
        <div 
          class="w-5 h-5 rounded-full flex items-center justify-center text-[9px] font-black shrink-0 bg-neutral-200 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300"
        >
          {{ getInitials(emp.nombre || emp.name) }}
        </div>

        <div class="flex flex-col min-w-0">
          <div class="flex items-center gap-1.5">
            <span class="font-bold text-xs truncate max-w-[150px] sm:max-w-[220px]">
              {{ emp.nombre || emp.name }}
            </span>
          </div>
          <div class="flex items-center gap-1 text-[10px] text-neutral-500 dark:text-neutral-400 truncate max-w-[240px]">
            <span v-if="emp.documento" class="font-mono font-medium">CC: {{ emp.documento }}</span>
            <span v-if="emp.documento && emp.cargo">•</span>
            <span v-if="emp.cargo" class="truncate">{{ emp.cargo }}</span>
          </div>
        </div>

        <button
          v-if="!disabled"
          type="button"
          @click.stop="removeEmpleado(idx)"
          class="p-1 rounded-md hover:bg-rose-100 hover:text-rose-600 dark:hover:bg-rose-950/60 dark:hover:text-rose-400 text-neutral-400 transition-colors ml-1 cursor-pointer"
          :title="'Quitar ' + roleLabel"
        >
          <IconX class="w-3.5 h-3.5 stroke-[2.5]" />
        </button>
      </div>
    </div>

    <!-- Input de Búsqueda y Dropdown (Visible si es multiple o si no se ha elegido aún el único) -->
    <div class="relative" v-if="!disabled && (multiple || selectedEmpleados.length === 0)">
      <div class="relative flex items-center">
        <IconSearch class="w-4 h-4 text-neutral-400 absolute left-3 pointer-events-none stroke-[2]" />
        <input
          ref="searchInputRef"
          type="text"
          v-model="searchQuery"
          @focus="handleFocus"
          @input="isOpen = true"
          @keydown.esc="isOpen = false"
          :placeholder="inputPlaceholder"
          class="flex h-9 w-full rounded-md border bg-white dark:bg-neutral-950 pl-9 pr-14 py-1 text-xs text-neutral-800 dark:text-neutral-200 placeholder:text-neutral-400 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all"
          :class="{
            'border-rose-300 dark:border-rose-700': required && selectedEmpleados.length === 0 && touched,
            'border-neutral-200 dark:border-white/10': !(required && selectedEmpleados.length === 0 && touched)
          }"
        />
        <div class="absolute right-2 flex items-center gap-1">
          <button
            v-if="searchQuery"
            type="button"
            @click="searchQuery = ''"
            class="text-neutral-400 hover:text-neutral-600 dark:hover:text-white p-0.5 cursor-pointer rounded"
            title="Limpiar búsqueda"
          >
            <IconX class="w-3.5 h-3.5 stroke-[2]" />
          </button>
          <button
            v-if="isOpen"
            type="button"
            @click="isOpen = false"
            class="text-[10px] font-bold text-neutral-400 hover:text-neutral-700 dark:hover:text-white px-1.5 py-0.5 rounded hover:bg-neutral-100 dark:hover:bg-neutral-800 cursor-pointer"
            title="Cerrar lista"
          >
            Cerrar
          </button>
        </div>
      </div>

      <!-- Menú Desplegable con Resultados -->
      <div
        v-if="isOpen && (filteredEmpleados.length > 0 || searchQuery.trim().length > 0)"
        class="absolute left-0 top-full mt-1.5 w-full min-w-[340px] sm:min-w-[420px] max-w-[calc(100vw-2.5rem)] bg-white dark:bg-[#18181b] border border-neutral-200 dark:border-neutral-700 rounded-xl shadow-2xl z-50 max-h-60 overflow-y-auto divide-y divide-neutral-100 dark:divide-neutral-800 custom-scrollbar"
      >
        <!-- Barra de cierre rápido -->
        <div class="flex items-center justify-between px-3 py-1.5 bg-neutral-50 dark:bg-neutral-900 text-[10px] text-neutral-500 font-bold border-b border-neutral-100 dark:border-neutral-800 sticky top-0 z-10">
          <span>Selecciona un {{ roleLabel }} para asignarlo</span>
          <button 
            type="button" 
            @click="isOpen = false" 
            class="hover:text-neutral-800 dark:hover:text-white flex items-center gap-0.5 cursor-pointer px-1 py-0.5 rounded hover:bg-neutral-200/50 dark:hover:bg-neutral-800"
          >
            <span>Cerrar</span>
            <IconX class="w-3 h-3" />
          </button>
        </div>

        <div
          v-for="emp in filteredEmpleados"
          :key="emp.id || emp.user_id"
          @click="selectEmpleado(emp)"
          class="p-2.5 hover:bg-neutral-50 dark:hover:bg-neutral-800/80 cursor-pointer transition-colors flex items-center justify-between gap-3 text-left"
          :class="isEmpleadoSelected(emp) ? 'bg-primary/5 dark:bg-primary/10' : ''"
        >
          <div class="flex items-center gap-2.5 min-w-0 flex-1">
            <div class="w-8 h-8 rounded-full bg-neutral-100 dark:bg-neutral-800 border border-neutral-200 dark:border-white/10 flex items-center justify-center text-[10px] font-black text-neutral-700 dark:text-neutral-300 shrink-0 shadow-xs">
              {{ getInitials(emp.nombre || emp.name) }}
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex items-center gap-2 flex-wrap">
                <span class="font-bold text-xs text-neutral-900 dark:text-white">
                  {{ emp.nombre || emp.name }}
                </span>
                <span v-if="emp.documento" class="text-[10px] font-mono font-bold text-neutral-600 dark:text-neutral-300 bg-neutral-100 dark:bg-neutral-800 px-1.5 py-0.5 rounded shrink-0">
                  CC {{ emp.documento }}
                </span>
              </div>
              <div class="flex items-center gap-1.5 text-[10px] text-neutral-500 dark:text-neutral-400 truncate mt-0.5">
                <span class="truncate font-medium">{{ emp.cargo || (roleLabel === 'coordinador' ? 'Coordinador' : 'Técnico Operativo') }}</span>
                <span v-if="emp.username" class="shrink-0">• @{{ emp.username }}</span>
              </div>
            </div>
          </div>

          <div class="shrink-0 flex items-center pl-1">
            <span v-if="isEmpleadoSelected(emp)" class="text-xs font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1 bg-emerald-50 dark:bg-emerald-950/40 px-2 py-1 rounded-lg">
              <IconCheck class="w-4 h-4 stroke-[2.5]" />
              <span class="text-[10px]">Asignado</span>
            </span>
            <span v-else class="text-[10px] font-semibold text-neutral-500 hover:text-primary flex items-center gap-1 bg-neutral-100/80 dark:bg-neutral-800/80 hover:bg-primary/10 px-2.5 py-1 rounded-lg transition-colors">
              <IconPlus class="w-3.5 h-3.5" />
              <span>Seleccionar</span>
            </span>
          </div>
        </div>

        <!-- Opción de texto libre si no está en la base de datos -->
        <div
          v-if="searchQuery.trim().length > 0"
          @click="selectCustomText(searchQuery.trim())"
          class="p-2.5 bg-neutral-50/70 dark:bg-neutral-900/70 hover:bg-primary/10 cursor-pointer text-left text-xs flex items-center justify-between border-t border-neutral-100 dark:border-neutral-800 transition-colors"
        >
          <span class="text-neutral-700 dark:text-neutral-300 text-[11px]">
            Asignar nombre personalizado: <strong>"{{ searchQuery.trim() }}"</strong>
          </span>
          <span class="text-[10px] text-primary font-bold shrink-0">Asignar</span>
        </div>
      </div>

      <!-- Estado cuando no hay resultados de búsqueda -->
      <div
        v-else-if="isOpen && searchQuery.trim().length > 0 && filteredEmpleados.length === 0"
        class="absolute left-0 top-full mt-1.5 w-full min-w-[340px] sm:min-w-[420px] max-w-[calc(100vw-2.5rem)] bg-white dark:bg-[#18181b] border border-neutral-200 dark:border-neutral-700 rounded-xl shadow-xl z-50 p-4 text-center space-y-2"
      >
        <p class="text-xs font-bold text-neutral-700 dark:text-neutral-300">
          No se encontraron registros coincidentes
        </p>
        <p class="text-[10px] text-neutral-400">
          No hay registros con cédula, nombre o cargo "{{ searchQuery }}"
        </p>
        <button
          type="button"
          @click="selectCustomText(searchQuery.trim())"
          class="text-xs font-bold text-primary hover:underline cursor-pointer block mx-auto"
        >
          Usar "{{ searchQuery }}" como {{ roleLabel }}
        </button>
      </div>
    </div>

    <!-- Mensaje de Validación Si es Requerido y no hay ninguno -->
    <p v-if="required && selectedEmpleados.length === 0 && touched" class="text-[10px] font-bold text-rose-500 flex items-center gap-1">
      <IconAlertCircle class="w-3 h-3 stroke-[2.5]" />
      <span>Debe asignar un {{ roleLabel }} responsable a la orden de trabajo.</span>
    </p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import client from '@/api/client';
import { IconSearch, IconX, IconPlus, IconCheck, IconAlertCircle } from '@tabler/icons-vue';

const props = defineProps({
  // Puede recibir array de IDs/objetos, o un string con el nombre (para single select)
  modelValue: {
    type: [Array, String, Object, Number],
    default: () => []
  },
  label: {
    type: String,
    default: 'Técnico'
  },
  roleLabel: {
    type: String,
    default: 'técnico'
  },
  placeholder: {
    type: String,
    default: ''
  },
  multiple: {
    type: Boolean,
    default: true
  },
  required: {
    type: Boolean,
    default: true
  },
  disabled: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue', 'change', 'leader-change']);

const containerRef = ref(null);
const searchInputRef = ref(null);
const searchQuery = ref('');
const isOpen = ref(false);
const touched = ref(false);
const empleados = ref([]);
const loading = ref(false);

const selectedEmpleados = ref([]);

const inputPlaceholder = computed(() => {
  if (props.placeholder) return props.placeholder;
  if (props.multiple) {
    return selectedEmpleados.value.length === 0
      ? `Buscar ${props.roleLabel} por cédula, nombre o cargo...`
      : `+ Agregar otro ${props.roleLabel} (cédula, nombre, cargo)...`;
  }
  return `Buscar ${props.roleLabel} por cédula, nombre o cargo...`;
});

// Cargar catálogo de empleados
const fetchEmpleados = async () => {
  loading.value = true;
  try {
    const res = await client.get('/empleados');
    if (res.data?.status === 'success' && Array.isArray(res.data?.data)) {
      empleados.value = res.data.data.map(e => ({
        id: e.id,
        user_id: e.user_id || e.user?.id,
        nombre: e.nombre,
        name: e.nombre,
        documento: e.documento || '',
        cargo: e.cargo || '',
        username: e.user?.username || '',
        cuadrilla_id: e.cuadrilla_id,
        telefono: e.telefono || ''
      }));
    } else {
      const fallback = await client.get('/ots/operadores');
      if (fallback.data?.status === 'success' && Array.isArray(fallback.data?.data)) {
        empleados.value = fallback.data.data.map(o => ({
          id: o.id,
          user_id: o.user_id || o.id,
          nombre: o.name,
          name: o.name,
          documento: o.documento || '',
          cargo: o.cargo || 'Técnico de Campo',
          username: o.username || '',
          cuadrilla_id: o.cuadrilla_id
        }));
      }
    }
  } catch (err) {
    console.warn('Error al cargar empleados, usando operadores de respaldo:', err);
    try {
      const fallback = await client.get('/ots/operadores');
      if (fallback.data?.status === 'success' && Array.isArray(fallback.data?.data)) {
        empleados.value = fallback.data.data.map(o => ({
          id: o.id,
          user_id: o.user_id || o.id,
          nombre: o.name,
          name: o.name,
          documento: o.documento || '',
          cargo: o.cargo || 'Técnico de Campo',
          username: o.username || '',
          cuadrilla_id: o.cuadrilla_id
        }));
      }
    } catch (e2) {
      console.error('Fallo definitivo al cargar directorio técnico:', e2);
    }
  } finally {
    loading.value = false;
    syncFromModelValue();
  }
};

// Sincronizar selección inicial
const syncFromModelValue = () => {
  if (!props.multiple) {
    if (!props.modelValue && props.modelValue !== 0) {
      selectedEmpleados.value = [];
      return;
    }
    if (typeof props.modelValue === 'string') {
      const valStr = props.modelValue.trim();
      if (!valStr) {
        selectedEmpleados.value = [];
        return;
      }
      const query = normalizeText(valStr);
      const found = empleados.value.find(e => {
        const nom = normalizeText(e.nombre || e.name);
        return nom === query || nom.includes(query) || query.includes(nom);
      });
      if (found) {
        selectedEmpleados.value = [{ ...found }];
      } else {
        selectedEmpleados.value = [{
          id: 'custom',
          nombre: valStr,
          name: valStr,
          cargo: props.roleLabel === 'coordinador' ? 'Coordinador' : 'Personal',
          documento: ''
        }];
      }
      return;
    }
    if (typeof props.modelValue === 'number') {
      const found = empleados.value.find(e => e.id === props.modelValue || e.user_id === props.modelValue);
      if (found) selectedEmpleados.value = [{ ...found }];
      return;
    }
    if (typeof props.modelValue === 'object') {
      if (Array.isArray(props.modelValue)) {
        selectedEmpleados.value = props.modelValue.slice(0, 1);
      } else {
        selectedEmpleados.value = [{ ...props.modelValue }];
      }
      return;
    }
  }

  // Modo Multiple
  if (!props.modelValue || !Array.isArray(props.modelValue)) {
    selectedEmpleados.value = [];
    return;
  }

  if (props.modelValue.length > 0 && typeof props.modelValue[0] === 'number') {
    const list = [];
    for (const val of props.modelValue) {
      const found = empleados.value.find(e => e.id === val || e.user_id === val);
      if (found) list.push(found);
      else list.push({ id: val, user_id: val, nombre: `Técnico #${val}`, documento: '', cargo: 'Técnico' });
    }
    selectedEmpleados.value = list;
  } else if (props.modelValue.length > 0 && typeof props.modelValue[0] === 'object') {
    selectedEmpleados.value = [...props.modelValue];
  } else {
    selectedEmpleados.value = [];
  }
};

watch(() => props.modelValue, () => {
  syncFromModelValue();
}, { deep: true });

onMounted(() => {
  fetchEmpleados();
  document.addEventListener('click', handleClickOutside);
  document.addEventListener('mousedown', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
  document.removeEventListener('mousedown', handleClickOutside);
});

const hasBeenFocused = ref(false);

const handleFocus = () => {
  isOpen.value = true;
  hasBeenFocused.value = true;
};

const handleClickOutside = (e) => {
  if (containerRef.value && !containerRef.value.contains(e.target)) {
    isOpen.value = false;
    if (hasBeenFocused.value) {
      touched.value = true;
    }
  }
};

// Normalizar texto sin tildes para búsqueda flexible
const normalizeText = (text) => {
  if (!text) return '';
  return text
    .toString()
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '');
};

// Filtro en tiempo real por Cédula, Nombre o Cargo
const filteredEmpleados = computed(() => {
  const q = normalizeText(searchQuery.value.trim());
  if (!q) {
    return empleados.value.slice(0, 8);
  }

  return empleados.value.filter(emp => {
    const doc = normalizeText(emp.documento);
    const nom = normalizeText(emp.nombre || emp.name);
    const car = normalizeText(emp.cargo);
    const usr = normalizeText(emp.username);

    return doc.includes(q) || nom.includes(q) || car.includes(q) || usr.includes(q);
  });
});

const isEmpleadoSelected = (emp) => {
  return selectedEmpleados.value.some(s => 
    (s.id && s.id === emp.id) || 
    (s.user_id && s.user_id === emp.user_id && emp.user_id != null) ||
    (s.documento && emp.documento && s.documento === emp.documento)
  );
};

const selectEmpleado = (emp) => {
  touched.value = true;
  if (!props.multiple) {
    selectedEmpleados.value = [{ ...emp }];
    searchQuery.value = '';
    isOpen.value = false;
    emitChanges();
    return;
  }

  if (isEmpleadoSelected(emp)) {
    const idx = selectedEmpleados.value.findIndex(s => s.id === emp.id || (s.user_id && s.user_id === emp.user_id));
    if (idx >= 0) removeEmpleado(idx);
    isOpen.value = false;
    return;
  }

  selectedEmpleados.value.push({ ...emp });
  searchQuery.value = '';
  isOpen.value = false;
  emitChanges();
};

const selectCustomText = (text) => {
  if (!text) return;
  touched.value = true;
  const customEmp = {
    id: 'custom-' + Date.now(),
    nombre: text,
    name: text,
    cargo: props.roleLabel === 'coordinador' ? 'Coordinador' : 'Personal',
    documento: ''
  };
  if (!props.multiple) {
    selectedEmpleados.value = [customEmp];
  } else {
    selectedEmpleados.value.push(customEmp);
  }
  searchQuery.value = '';
  isOpen.value = false;
  emitChanges();
};

const removeEmpleado = (index) => {
  selectedEmpleados.value.splice(index, 1);
  emitChanges();
};

const emitChanges = () => {
  if (!props.multiple) {
    const selected = selectedEmpleados.value[0] || null;
    const val = selected ? (selected.nombre || selected.name || '') : '';
    emit('update:modelValue', val);
    emit('change', selected);
    emit('leader-change', selected);
  } else {
    emit('update:modelValue', [...selectedEmpleados.value]);
    emit('change', [...selectedEmpleados.value]);
    const primary = selectedEmpleados.value[0] || null;
    emit('leader-change', primary);
  }
};

const getInitials = (name) => {
  if (!name) return 'OP';
  const parts = name.trim().split(' ').filter(Boolean);
  if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
  return (parts[0][0] + parts[1][0]).toUpperCase();
};
</script>

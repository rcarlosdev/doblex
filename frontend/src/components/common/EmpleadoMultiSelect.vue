<template>
  <div class="space-y-2 relative" ref="containerRef">
    <!-- Encabezado con Label y Contador -->
    <div class="flex items-center justify-between">
      <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider flex items-center gap-1.5">
        <span>{{ label }}</span>
        <span v-if="required" class="text-rose-500 font-black">*</span>
      </label>
      <span class="text-[10px] font-mono font-bold" :class="selectedEmpleados.length > 0 ? 'text-primary' : 'text-neutral-400'">
        {{ selectedEmpleados.length }} {{ selectedEmpleados.length === 1 ? 'técnico asignado' : 'técnicos asignados' }}
      </span>
    </div>

    <!-- Chips / Tarjetas de Empleados Seleccionados (Sin marcar a nadie como líder) -->
    <div v-if="selectedEmpleados.length > 0" class="flex flex-wrap gap-1.5 p-2 bg-neutral-50 dark:bg-neutral-900/60 border border-neutral-200 dark:border-white/10 rounded-xl">
      <div
        v-for="(emp, idx) in selectedEmpleados"
        :key="emp.id || emp.user_id || idx"
        class="inline-flex items-center gap-2 px-2.5 py-1.5 rounded-lg border text-xs shadow-xs transition-all animate-in fade-in bg-white dark:bg-[#18181b] border-neutral-200 dark:border-white/10 text-neutral-800 dark:text-neutral-200 hover:border-neutral-300 dark:hover:border-white/20"
      >
        <!-- Icono de usuario / avatar iniciales neutral -->
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

        <!-- Botón para remover empleado -->
        <button
          v-if="!disabled"
          type="button"
          @click.stop="removeEmpleado(idx)"
          class="p-1 rounded-md hover:bg-rose-100 hover:text-rose-600 dark:hover:bg-rose-950/60 dark:hover:text-rose-400 text-neutral-400 transition-colors ml-1 cursor-pointer"
          title="Quitar técnico"
        >
          <IconX class="w-3.5 h-3.5 stroke-[2.5]" />
        </button>
      </div>
    </div>

    <!-- Input de Búsqueda y Dropdown -->
    <div class="relative" v-if="!disabled">
      <div class="relative flex items-center">
        <IconSearch class="w-4 h-4 text-neutral-400 absolute left-3 pointer-events-none stroke-[2]" />
        <input
          ref="searchInputRef"
          type="text"
          v-model="searchQuery"
          @focus="isOpen = true"
          @input="isOpen = true"
          @keydown.esc="isOpen = false"
          :placeholder="selectedEmpleados.length === 0 ? 'Buscar técnico por cédula, nombre o cargo...' : '+ Agregar otro técnico (cédula, nombre, cargo)...'"
          class="flex h-9 w-full rounded-md border bg-white dark:bg-neutral-950 pl-9 pr-16 py-1 text-xs text-neutral-800 dark:text-neutral-200 placeholder:text-neutral-400 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all"
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
            class="text-neutral-400 hover:text-neutral-600 dark:hover:text-white p-0.5 cursor-pointer"
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
        v-if="isOpen && filteredEmpleados.length > 0"
        class="absolute left-0 right-0 top-full mt-1.5 bg-white dark:bg-[#18181b] border border-neutral-200 dark:border-neutral-700 rounded-xl shadow-2xl z-50 max-h-56 overflow-y-auto divide-y divide-neutral-100 dark:divide-neutral-800"
      >
        <!-- Barra de cierre rápido -->
        <div class="flex items-center justify-between px-3 py-1.5 bg-neutral-50 dark:bg-neutral-900 text-[10px] text-neutral-500 font-bold border-b border-neutral-100 dark:border-neutral-800">
          <span>Selecciona un técnico para agregarlo</span>
          <button 
            type="button" 
            @click="isOpen = false" 
            class="hover:text-neutral-800 dark:hover:text-white flex items-center gap-0.5 cursor-pointer"
          >
            <span>Cerrar</span>
            <IconX class="w-3 h-3" />
          </button>
        </div>

        <div
          v-for="emp in filteredEmpleados"
          :key="emp.id"
          @click="selectEmpleado(emp)"
          class="p-2.5 hover:bg-neutral-50 dark:hover:bg-neutral-800/80 cursor-pointer transition-colors flex items-center justify-between gap-3 text-left"
          :class="isEmpleadoSelected(emp) ? 'bg-primary/5 dark:bg-primary/10' : ''"
        >
          <div class="flex items-center gap-2.5 min-w-0">
            <div class="w-7 h-7 rounded-full bg-neutral-100 dark:bg-neutral-800 border border-neutral-200 dark:border-white/10 flex items-center justify-center text-[10px] font-black text-neutral-700 dark:text-neutral-300 shrink-0">
              {{ getInitials(emp.nombre || emp.name) }}
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <span class="font-bold text-xs text-neutral-900 dark:text-white truncate">
                  {{ emp.nombre || emp.name }}
                </span>
                <span v-if="emp.documento" class="text-[10px] font-mono font-bold text-neutral-600 dark:text-neutral-300 bg-neutral-100 dark:bg-neutral-800 px-1.5 py-0.2 rounded shrink-0">
                  CC {{ emp.documento }}
                </span>
              </div>
              <div class="flex items-center gap-2 text-[10px] text-neutral-500 dark:text-neutral-400 truncate mt-0.5">
                <span class="truncate font-medium">{{ emp.cargo || 'Técnico Operativo' }}</span>
                <span v-if="emp.username">• @{{ emp.username }}</span>
              </div>
            </div>
          </div>

          <div class="shrink-0 flex items-center">
            <span v-if="isEmpleadoSelected(emp)" class="text-xs font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
              <IconCheck class="w-4 h-4 stroke-[2.5]" />
              <span class="text-[10px] hidden xs:inline">Asignado</span>
            </span>
            <span v-else class="text-[10px] font-semibold text-neutral-400 group-hover:text-primary flex items-center gap-1">
              <IconPlus class="w-3.5 h-3.5" />
              <span>Agregar</span>
            </span>
          </div>
        </div>
      </div>

      <!-- Estado cuando no hay resultados de búsqueda -->
      <div
        v-else-if="isOpen && searchQuery.trim().length > 0 && filteredEmpleados.length === 0"
        class="absolute left-0 right-0 top-full mt-1.5 bg-white dark:bg-[#18181b] border border-neutral-200 dark:border-neutral-700 rounded-xl shadow-xl z-50 p-4 text-center space-y-1"
      >
        <p class="text-xs font-bold text-neutral-700 dark:text-neutral-300">
          No se encontraron técnicos coincidentes
        </p>
        <p class="text-[10px] text-neutral-400">
          No hay registros con cédula, nombre o cargo "{{ searchQuery }}"
        </p>
        <button 
          type="button" 
          @click="isOpen = false" 
          class="mt-2 text-xs font-bold text-primary hover:underline cursor-pointer"
        >
          Cerrar lista
        </button>
      </div>
    </div>

    <!-- Mensaje de Validación Si es Requerido y no hay ninguno -->
    <p v-if="required && selectedEmpleados.length === 0 && touched" class="text-[10px] font-bold text-rose-500 flex items-center gap-1">
      <IconAlertCircle class="w-3 h-3 stroke-[2.5]" />
      <span>Debe asignar al menos un técnico responsable a la orden de trabajo.</span>
    </p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import client from '@/api/client';
import { IconSearch, IconX, IconPlus, IconCheck, IconAlertCircle } from '@tabler/icons-vue';

const props = defineProps({
  // Puede recibir array de IDs o array de objetos completos
  modelValue: {
    type: Array,
    default: () => []
  },
  label: {
    type: String,
    default: 'Operador(es) Asignado(s) *'
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

// Cargar catálogo de empleados
const fetchEmpleados = async () => {
  loading.value = true;
  try {
    // Intentar cargar desde /api/empleados
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
      // Fallback a /ots/operadores
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
  if (!props.modelValue || !Array.isArray(props.modelValue)) {
    selectedEmpleados.value = [];
    return;
  }

  // Si modelValue contiene números/IDs
  if (props.modelValue.length > 0 && typeof props.modelValue[0] === 'number') {
    const list = [];
    for (const val of props.modelValue) {
      const found = empleados.value.find(e => e.id === val || e.user_id === val);
      if (found) list.push(found);
      else list.push({ id: val, user_id: val, nombre: `Técnico #${val}`, documento: '', cargo: 'Técnico' });
    }
    selectedEmpleados.value = list;
  } else if (props.modelValue.length > 0 && typeof props.modelValue[0] === 'object') {
    // Si ya son objetos
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

const handleClickOutside = (e) => {
  if (containerRef.value && !containerRef.value.contains(e.target)) {
    isOpen.value = false;
    touched.value = true;
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
    // Si no hay búsqueda, mostrar los primeros 8 empleados disponibles
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
  if (isEmpleadoSelected(emp)) {
    // Si ya está, removerlo (toggle)
    const idx = selectedEmpleados.value.findIndex(s => s.id === emp.id || (s.user_id && s.user_id === emp.user_id));
    if (idx >= 0) removeEmpleado(idx);
    isOpen.value = false;
    return;
  }

  selectedEmpleados.value.push({ ...emp });
  searchQuery.value = '';
  isOpen.value = false; // Cierra el menú inmediatamente al agregar el técnico
  emitChanges();
};

const removeEmpleado = (index) => {
  selectedEmpleados.value.splice(index, 1);
  emitChanges();
};

const emitChanges = () => {
  emit('update:modelValue', [...selectedEmpleados.value]);
  emit('change', [...selectedEmpleados.value]);
  const primary = selectedEmpleados.value[0] || null;
  emit('leader-change', primary);
};

const getInitials = (name) => {
  if (!name) return 'OP';
  const parts = name.trim().split(' ').filter(Boolean);
  if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
  return (parts[0][0] + parts[1][0]).toUpperCase();
};
</script>

<script setup>
import { ref, onMounted, computed } from 'vue';
import client from '@/api/client';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

const activeTab = ref('empleados'); // 'empleados' | 'cuadrillas'
const empleados = ref([]);
const cuadrillas = ref([]);
const loading = ref(false);
const errorMsg = ref('');
const successMsg = ref('');

// Filtros y búsquedas
const searchQuery = ref('');
const selectedRolFilter = ref('todos');
const selectedEstadoFilter = ref('todos');

// Estado Modal Empleado
const showModalEmpleado = ref(false);
const editingEmpleadoId = ref(null);
const formEmpleado = ref({
  documento: '',
  nombre: '',
  cargo: '',
  telefono: '',
  email: '',
  rol: 'operativo',
  cuadrilla_id: '',
  estado: 'activo'
});

// Estado Modal Cuadrilla
const showModalCuadrilla = ref(false);
const formCuadrilla = ref({
  nombre: '',
  especialidad: '',
  lider_id: ''
});

const userRole = ref(localStorage.getItem('smu_role') || 'admin');

onMounted(() => {
  fetchData();
});

const fetchData = async () => {
  loading.value = true;
  errorMsg.value = '';
  try {
    const [resEmp, resCuad] = await Promise.all([
      client.get('/empleados'),
      client.get('/cuadrillas')
    ]);
    if (resEmp.data.status === 'success') {
      empleados.value = resEmp.data.data;
    }
    if (resCuad.data.status === 'success') {
      cuadrillas.value = resCuad.data.data;
    }
  } catch (err) {
    errorMsg.value = 'Error al cargar los datos de personal y cuadrillas.';
  } finally {
    loading.value = false;
  }
};

// Computados
const filteredEmpleados = computed(() => {
  return empleados.value.filter(emp => {
    const matchesSearch = emp.nombre.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          emp.documento.includes(searchQuery.value) ||
                          emp.cargo.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesRol = selectedRolFilter.value === 'todos' || emp.rol === selectedRolFilter.value;
    const matchesEstado = selectedEstadoFilter.value === 'todos' || emp.estado === selectedEstadoFilter.value;
    return matchesSearch && matchesRol && matchesEstado;
  });
});

const totalPersonal = computed(() => empleados.value.length);
const totalOperativos = computed(() => empleados.value.filter(e => e.rol === 'operativo').length);
const totalCuadrillas = computed(() => cuadrillas.value.length);

// Operadores con perfil operativo que pueden liderar cuadrillas
const posiblesLideres = computed(() => {
  return empleados.value.filter(e => e.rol === 'operativo' || e.rol === 'admin');
});

// Abrir Modal Empleado
const openModalEmpleado = (emp = null) => {
  if (emp) {
    editingEmpleadoId.value = emp.id;
    formEmpleado.value = {
      documento: emp.documento,
      nombre: emp.nombre,
      cargo: emp.cargo,
      telefono: emp.telefono || '',
      email: emp.email || '',
      rol: emp.rol,
      cuadrilla_id: emp.cuadrilla_id || '',
      estado: emp.estado
    };
  } else {
    editingEmpleadoId.value = null;
    formEmpleado.value = {
      documento: '',
      nombre: '',
      cargo: '',
      telefono: '',
      email: '',
      rol: 'operativo',
      cuadrilla_id: '',
      estado: 'activo'
    };
  }
  showModalEmpleado.value = true;
};

// Guardar Empleado
const saveEmpleado = async () => {
  errorMsg.value = '';
  successMsg.value = '';
  try {
    const payload = { ...formEmpleado.value };
    if (!payload.cuadrilla_id) payload.cuadrilla_id = null;

    if (editingEmpleadoId.value) {
      const res = await client.put(`/empleados/${editingEmpleadoId.value}`, payload);
      if (res.data.status === 'success') {
        successMsg.value = 'Empleado actualizado correctamente.';
      }
    } else {
      const res = await client.post('/empleados', payload);
      if (res.data.status === 'success') {
        successMsg.value = 'Empleado registrado correctamente.';
      }
    }
    showModalEmpleado.value = false;
    fetchData();
  } catch (err) {
    if (err.response && err.response.data && err.response.data.message) {
      errorMsg.value = err.response.data.message;
    } else {
      errorMsg.value = 'Error al guardar el empleado.';
    }
  }
};

// Guardar Cuadrilla
const saveCuadrilla = async () => {
  errorMsg.value = '';
  successMsg.value = '';
  try {
    const payload = { ...formCuadrilla.value };
    if (!payload.lider_id) payload.lider_id = null;

    const res = await client.post('/cuadrillas', payload);
    if (res.data.status === 'success') {
      successMsg.value = 'Cuadrilla creada correctamente.';
      showModalCuadrilla.value = false;
      formCuadrilla.value = { nombre: '', especialidad: '', lider_id: '' };
      fetchData();
    }
  } catch (err) {
    errorMsg.value = 'Error al registrar la cuadrilla.';
  }
};

// Cambiar estado de empleado
const toggleEstadoEmpleado = async (emp) => {
  const nuevoEstado = emp.estado === 'activo' ? 'inactivo' : 'activo';
  try {
    await client.put(`/empleados/${emp.id}`, { ...emp, estado: nuevoEstado });
    fetchData();
  } catch (err) {
    errorMsg.value = 'No se pudo cambiar el estado del empleado.';
  }
};
</script>

<template>
  <div class="space-y-6">
    <!-- Encabezado Principal -->
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 select-none">
      <div>
        <h1 class="text-2xl font-bold tracking-tight text-neutral-900 dark:text-white flex items-center gap-2">
          <span>👥</span> Gestión de Personal y Cuadrillas
        </h1>
        <p class="text-xs text-neutral-500 dark:text-neutral-400 mt-1">
          Módulo 7 (Base) — Registro Maestro de Empleados, Roles, Cargos y Asignación a Obras
        </p>
      </div>

      <div class="flex items-center gap-3">
        <Button 
          v-if="activeTab === 'empleados' && (userRole === 'admin' || userRole === 'administrativo')" 
          @click="openModalEmpleado()" 
          class="bg-primary text-primary-foreground hover:bg-primary/90 font-medium text-xs gap-2"
        >
          <span>➕</span> Nuevo Empleado
        </Button>
        <Button 
          v-if="activeTab === 'cuadrillas' && (userRole === 'admin' || userRole === 'administrativo')" 
          @click="showModalCuadrilla = true" 
          class="bg-primary text-primary-foreground hover:bg-primary/90 font-medium text-xs gap-2"
        >
          <span>🏗️</span> Nueva Cuadrilla
        </Button>
      </div>
    </div>

    <!-- Alertas de estado -->
    <div v-if="successMsg" class="bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-xs p-3 rounded-lg flex items-center justify-between">
      <span>✅ {{ successMsg }}</span>
      <button @click="successMsg = ''" class="font-bold">✕</button>
    </div>
    <div v-if="errorMsg" class="bg-red-500/10 border border-red-500/20 text-red-600 dark:text-red-400 text-xs p-3 rounded-lg flex items-center justify-between">
      <span>⚠️ {{ errorMsg }}</span>
      <button @click="errorMsg = ''" class="font-bold">✕</button>
    </div>

    <!-- Tarjetas resumen KPI -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <Card class="bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900">
        <CardContent class="p-4 flex items-center gap-4">
          <div class="p-3 bg-blue-500/10 text-blue-600 dark:text-blue-400 rounded-xl text-xl">👥</div>
          <div>
            <p class="text-xs font-semibold text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Total Personal</p>
            <h3 class="text-2xl font-bold text-neutral-900 dark:text-white">{{ totalPersonal }}</h3>
          </div>
        </CardContent>
      </Card>

      <Card class="bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900">
        <CardContent class="p-4 flex items-center gap-4">
          <div class="p-3 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 rounded-xl text-xl">👷</div>
          <div>
            <p class="text-xs font-semibold text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Personal Operativo</p>
            <h3 class="text-2xl font-bold text-neutral-900 dark:text-white">{{ totalOperativos }}</h3>
          </div>
        </CardContent>
      </Card>

      <Card class="bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900">
        <CardContent class="p-4 flex items-center gap-4">
          <div class="p-3 bg-amber-500/10 text-amber-600 dark:text-amber-400 rounded-xl text-xl">🏗️</div>
          <div>
            <p class="text-xs font-semibold text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Cuadrillas Activas</p>
            <h3 class="text-2xl font-bold text-neutral-900 dark:text-white">{{ totalCuadrillas }}</h3>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Pestañas de Navegación -->
    <div class="flex items-center gap-2 border-b border-neutral-200 dark:border-neutral-800 pb-2">
      <button 
        @click="activeTab = 'empleados'" 
        class="px-4 py-2 text-xs font-semibold rounded-lg transition-colors"
        :class="activeTab === 'empleados' 
          ? 'bg-neutral-900 text-white dark:bg-white dark:text-neutral-900 shadow-sm' 
          : 'text-neutral-500 hover:text-neutral-900 dark:hover:text-white'"
      >
        📁 Registro Maestro de Empleados
      </button>
      <button 
        @click="activeTab = 'cuadrillas'" 
        class="px-4 py-2 text-xs font-semibold rounded-lg transition-colors"
        :class="activeTab === 'cuadrillas' 
          ? 'bg-neutral-900 text-white dark:bg-white dark:text-neutral-900 shadow-sm' 
          : 'text-neutral-500 hover:text-neutral-900 dark:hover:text-white'"
      >
        🏗️ Cuadrillas de Obra ({{ totalCuadrillas }})
      </button>
    </div>

    <!-- VISTA TAB 1: EMPLEADOS -->
    <div v-if="activeTab === 'empleados'" class="space-y-4">
      <!-- Filtros -->
      <div class="flex flex-col sm:flex-row items-center gap-3 bg-white dark:bg-neutral-950/40 p-4 rounded-xl border border-neutral-200 dark:border-neutral-900">
        <div class="w-full sm:flex-1">
          <Input 
            v-model="searchQuery" 
            placeholder="🔍 Buscar por nombre, cédula o cargo..." 
            class="bg-slate-50 dark:bg-neutral-900 border-neutral-200 dark:border-neutral-800 text-xs"
          />
        </div>
        <div class="flex items-center gap-2 w-full sm:w-auto">
          <select 
            v-model="selectedRolFilter" 
            class="bg-slate-50 dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 text-neutral-900 dark:text-white text-xs rounded-lg px-3 py-2 outline-none"
          >
            <option value="todos">Todos los Roles</option>
            <option value="admin">Administrador</option>
            <option value="administrativo">Administrativo</option>
            <option value="operativo">Operativo</option>
          </select>

          <select 
            v-model="selectedEstadoFilter" 
            class="bg-slate-50 dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 text-neutral-900 dark:text-white text-xs rounded-lg px-3 py-2 outline-none"
          >
            <option value="todos">Todos los Estados</option>
            <option value="activo">Activo</option>
            <option value="inactivo">Inactivo</option>
          </select>
        </div>
      </div>

      <!-- Tabla de Empleados -->
      <Card class="bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900 overflow-hidden">
        <CardContent class="p-0">
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs">
              <thead class="bg-slate-50 dark:bg-neutral-900/60 text-neutral-500 dark:text-neutral-400 font-semibold border-b border-neutral-200 dark:border-neutral-900 uppercase tracking-wider">
                <tr>
                  <th class="py-3.5 px-4">Empleado</th>
                  <th class="py-3.5 px-4">Cédula</th>
                  <th class="py-3.5 px-4">Cargo</th>
                  <th class="py-3.5 px-4">Rol</th>
                  <th class="py-3.5 px-4">Cuadrilla Asignada</th>
                  <th class="py-3.5 px-4">Estado</th>
                  <th class="py-3.5 px-4 text-right">Acciones</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-neutral-200 dark:divide-neutral-900 text-neutral-800 dark:text-neutral-200">
                <tr v-if="loading" class="text-center py-8">
                  <td colspan="7" class="py-8 text-neutral-400">Cargando personal...</td>
                </tr>
                <tr v-else-if="filteredEmpleados.length === 0" class="text-center py-8">
                  <td colspan="7" class="py-8 text-neutral-400">No se encontraron empleados registrados.</td>
                </tr>
                <tr v-for="emp in filteredEmpleados" :key="emp.id" class="hover:bg-slate-50 dark:hover:bg-neutral-900/40 transition-colors">
                  <td class="py-3.5 px-4 font-semibold text-neutral-900 dark:text-white">
                    {{ emp.nombre }}
                    <span v-if="emp.email" class="block text-[10px] text-neutral-400 font-normal">{{ emp.email }}</span>
                  </td>
                  <td class="py-3.5 px-4 font-mono text-neutral-500 dark:text-neutral-400">{{ emp.documento }}</td>
                  <td class="py-3.5 px-4">{{ emp.cargo }}</td>
                  <td class="py-3.5 px-4">
                    <span 
                      class="px-2 py-0.5 rounded-full text-[10px] font-semibold tracking-wide uppercase"
                      :class="{
                        'bg-purple-500/10 text-purple-600 dark:text-purple-400 border border-purple-500/20': emp.rol === 'admin',
                        'bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20': emp.rol === 'administrativo',
                        'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20': emp.rol === 'operativo'
                      }"
                    >
                      {{ emp.rol }}
                    </span>
                  </td>
                  <td class="py-3.5 px-4">
                    <span v-if="emp.cuadrilla" class="text-xs font-medium text-neutral-700 dark:text-neutral-300">
                      🏗️ {{ emp.cuadrilla.nombre }}
                    </span>
                    <span v-else class="text-neutral-400 italic">Sin asignar</span>
                  </td>
                  <td class="py-3.5 px-4">
                    <span 
                      class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[10px] font-semibold"
                      :class="emp.estado === 'activo' ? 'bg-emerald-500/10 text-emerald-500' : 'bg-red-500/10 text-red-400'"
                    >
                      <span class="w-1.5 h-1.5 rounded-full" :class="emp.estado === 'activo' ? 'bg-emerald-500' : 'bg-red-400'"></span>
                      {{ emp.estado }}
                    </span>
                  </td>
                  <td class="py-3.5 px-4 text-right space-x-2">
                    <button 
                      @click="openModalEmpleado(emp)" 
                      class="px-2.5 py-1 text-xs bg-slate-100 dark:bg-neutral-800 hover:bg-slate-200 dark:hover:bg-neutral-700 text-neutral-700 dark:text-neutral-300 rounded transition-colors"
                      title="Editar Empleado"
                    >
                      ✏️ Editar
                    </button>
                    <button 
                      @click="toggleEstadoEmpleado(emp)" 
                      class="px-2.5 py-1 text-xs rounded transition-colors"
                      :class="emp.estado === 'activo' ? 'bg-red-500/10 text-red-500 hover:bg-red-500/20' : 'bg-emerald-500/10 text-emerald-500 hover:bg-emerald-500/20'"
                    >
                      {{ emp.estado === 'activo' ? 'Desactivar' : 'Activar' }}
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- VISTA TAB 2: CUADRILLAS -->
    <div v-if="activeTab === 'cuadrillas'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-if="cuadrillas.length === 0" class="col-span-full text-center py-12 text-neutral-400">
        No hay cuadrillas registradas. ¡Crea la primera cuadrilla para organizar tu personal!
      </div>
      
      <Card v-for="cuad in cuadrillas" :key="cuad.id" class="bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900 flex flex-col justify-between">
        <CardHeader class="pb-3">
          <div class="flex items-start justify-between">
            <div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-primary bg-primary/10 px-2 py-0.5 rounded">Cuadrilla</span>
              <CardTitle class="text-base font-bold text-neutral-900 dark:text-white mt-1">{{ cuad.nombre }}</CardTitle>
            </div>
            <span class="text-xl">🏗️</span>
          </div>
          <p class="text-xs text-neutral-500 dark:text-neutral-400 mt-1">{{ cuad.especialidad || 'Sin especialidad definida' }}</p>
        </CardHeader>

        <CardContent class="space-y-4 text-xs">
          <div class="bg-slate-50 dark:bg-neutral-900/60 p-3 rounded-lg border border-neutral-200 dark:border-neutral-800">
            <span class="block text-[10px] font-semibold uppercase text-neutral-400">Líder / Encargado:</span>
            <span class="font-semibold text-neutral-900 dark:text-white">{{ cuad.lider ? cuad.lider.name : 'Sin asignar' }}</span>
          </div>

          <div>
            <span class="block text-[10px] font-semibold uppercase text-neutral-400 mb-2">Integrantes ({{ cuad.empleados ? cuad.empleados.length : 0 }}):</span>
            <div class="space-y-1.5 max-h-36 overflow-y-auto pr-1">
              <div 
                v-for="miembro in cuad.empleados" 
                :key="miembro.id" 
                class="flex items-center justify-between bg-slate-100 dark:bg-neutral-900/40 px-2.5 py-1.5 rounded text-neutral-700 dark:text-neutral-300"
              >
                <span>👷 {{ miembro.nombre }}</span>
                <span class="text-[10px] text-neutral-400">{{ miembro.cargo }}</span>
              </div>
              <div v-if="!cuad.empleados || cuad.empleados.length === 0" class="text-neutral-400 italic">
                Sin miembros asignados.
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- MODAL REGISTRO / EDICIÓN EMPLEADO -->
    <Teleport to="body">
      <div v-if="showModalEmpleado" class="fixed inset-0 z-50 flex items-center justify-center p-4 overflow-y-auto">
        <!-- Overlay oscuro que cubre 100% de la pantalla incluyendo Navbar -->
        <div class="fixed inset-0 bg-black/60 backdrop-blur-sm" @click="showModalEmpleado = false"></div>

        <!-- Contenido Modal -->
        <div class="relative z-10 bg-white dark:bg-neutral-900 border border-slate-200 dark:border-neutral-800 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4 my-auto">
          <h2 class="text-lg font-bold text-slate-900 dark:text-white">
            {{ editingEmpleadoId ? 'Editar Empleado' : 'Registrar Nuevo Empleado' }}
          </h2>

          <form @submit.prevent="saveEmpleado" class="space-y-3 text-xs">
            <div>
              <label class="block font-semibold mb-1 text-slate-700 dark:text-neutral-300">Cédula / Documento *</label>
              <Input v-model="formEmpleado.documento" required placeholder="Ej: 1090887123" class="bg-slate-50 dark:bg-neutral-950 border-slate-300 dark:border-neutral-800 text-slate-900 dark:text-white" />
            </div>

            <div>
              <label class="block font-semibold mb-1 text-slate-700 dark:text-neutral-300">Nombre Completo *</label>
              <Input v-model="formEmpleado.nombre" required placeholder="Ej: Carlos Pérez" class="bg-slate-50 dark:bg-neutral-950 border-slate-300 dark:border-neutral-800 text-slate-900 dark:text-white" />
            </div>

            <div>
              <label class="block font-semibold mb-1 text-slate-700 dark:text-neutral-300">Cargo / Posición *</label>
              <Input v-model="formEmpleado.cargo" required placeholder="Ej: Ingeniero Residente / Maestro de Obra" class="bg-slate-50 dark:bg-neutral-950 border-slate-300 dark:border-neutral-800 text-slate-900 dark:text-white" />
            </div>

            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="block font-semibold mb-1 text-slate-700 dark:text-neutral-300">Teléfono</label>
                <Input v-model="formEmpleado.telefono" placeholder="3001234567" class="bg-slate-50 dark:bg-neutral-950 border-slate-300 dark:border-neutral-800 text-slate-900 dark:text-white" />
              </div>
              <div>
                <label class="block font-semibold mb-1 text-slate-700 dark:text-neutral-300">Rol Sistema *</label>
                <select v-model="formEmpleado.rol" class="w-full bg-slate-50 dark:bg-neutral-950 border border-slate-300 dark:border-neutral-800 rounded-md p-2 text-slate-900 dark:text-white">
                  <option value="operativo">Operativo (Campo)</option>
                  <option value="administrativo">Administrativo</option>
                  <option value="admin">Administrador</option>
                </select>
              </div>
            </div>

            <div>
              <label class="block font-semibold mb-1 text-slate-700 dark:text-neutral-300">Cuadrilla Asignada</label>
              <select v-model="formEmpleado.cuadrilla_id" class="w-full bg-slate-50 dark:bg-neutral-950 border border-slate-300 dark:border-neutral-800 rounded-md p-2 text-slate-900 dark:text-white">
                <option value="">-- Sin Cuadrilla --</option>
                <option v-for="c in cuadrillas" :key="c.id" :value="c.id">{{ c.nombre }}</option>
              </select>
            </div>

            <div class="flex items-center justify-end gap-2 pt-4 border-t border-slate-200 dark:border-neutral-800 mt-4">
              <button 
                type="button" 
                @click="showModalEmpleado = false" 
                class="px-4 py-2 text-xs font-semibold rounded-lg border border-slate-300 dark:border-neutral-700 text-slate-700 dark:text-neutral-300 bg-slate-100 dark:bg-neutral-800 hover:bg-slate-200 dark:hover:bg-neutral-700 transition-colors"
              >
                Cancelar
              </button>
              <button 
                type="submit" 
                class="px-4 py-2 text-xs font-semibold rounded-lg bg-primary text-white hover:bg-primary/90 shadow-sm transition-colors"
              >
                Guardar
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- MODAL NUEVA CUADRILLA -->
    <Teleport to="body">
      <div v-if="showModalCuadrilla" class="fixed inset-0 z-50 flex items-center justify-center p-4 overflow-y-auto">
        <!-- Overlay oscuro que cubre 100% de la pantalla incluyendo Navbar -->
        <div class="fixed inset-0 bg-black/60 backdrop-blur-sm" @click="showModalCuadrilla = false"></div>

        <!-- Contenido Modal -->
        <div class="relative z-10 bg-white dark:bg-neutral-900 border border-slate-200 dark:border-neutral-800 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4 my-auto">
          <h2 class="text-lg font-bold text-slate-900 dark:text-white">Crear Nueva Cuadrilla de Obra</h2>

          <form @submit.prevent="saveCuadrilla" class="space-y-3 text-xs">
            <div>
              <label class="block font-semibold mb-1 text-slate-700 dark:text-neutral-300">Nombre de la Cuadrilla *</label>
              <Input v-model="formCuadrilla.nombre" required placeholder="Ej: Cuadrilla Vías A" class="bg-slate-50 dark:bg-neutral-950 border-slate-300 dark:border-neutral-800 text-slate-900 dark:text-white" />
            </div>

            <div>
              <label class="block font-semibold mb-1 text-slate-700 dark:text-neutral-300">Especialidad</label>
              <Input v-model="formCuadrilla.especialidad" placeholder="Ej: Excavación y Movimiento de Tierra" class="bg-slate-50 dark:bg-neutral-950 border-slate-300 dark:border-neutral-800 text-slate-900 dark:text-white" />
            </div>

            <div>
              <label class="block font-semibold mb-1 text-slate-700 dark:text-neutral-300">Líder / Ingeniero Encargado</label>
              <select v-model="formCuadrilla.lider_id" class="w-full bg-slate-50 dark:bg-neutral-950 border border-slate-300 dark:border-neutral-800 rounded-md p-2 text-slate-900 dark:text-white">
                <option value="">-- Sin Líder Asignado --</option>
                <option v-for="l in posiblesLideres" :key="l.user_id || l.id" :value="l.user_id || l.id">{{ l.nombre }}</option>
              </select>
            </div>

            <div class="flex items-center justify-end gap-2 pt-4 border-t border-slate-200 dark:border-neutral-800 mt-4">
              <button 
                type="button" 
                @click="showModalCuadrilla = false" 
                class="px-4 py-2 text-xs font-semibold rounded-lg border border-slate-300 dark:border-neutral-700 text-slate-700 dark:text-neutral-300 bg-slate-100 dark:bg-neutral-800 hover:bg-slate-200 dark:hover:bg-neutral-700 transition-colors"
              >
                Cancelar
              </button>
              <button 
                type="submit" 
                class="px-4 py-2 text-xs font-semibold rounded-lg bg-primary text-white hover:bg-primary/90 shadow-sm transition-colors"
              >
                Crear Cuadrilla
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </div>
</template>

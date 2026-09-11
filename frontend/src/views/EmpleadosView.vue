<script setup>
import { ref, onMounted, computed } from 'vue';
import client from '@/api/client';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import {
  IconUsers,
  IconUserPlus,
  IconUsersGroup,
  IconCheck,
  IconAlertTriangle,
  IconX,
  IconUserCheck,
  IconFolder,
  IconPencil,
  IconKey,
  IconEye,
  IconEyeOff,
  IconShieldCheck
} from '@tabler/icons-vue';

const activeTab = ref('empleados'); // 'empleados' | 'cuadrillas'
const empleados = ref([]);
const cuadrillas = ref([]);
const loading = ref(false);
const errorMsg = ref('');
const successMsg = ref('');

// Sistema de Notificaciones Toast Reactivas y Flotantes
const toastError = ref('');
const toastSuccess = ref('');
const savingEmpleado = ref(false);
const savingCuadrilla = ref(false);

let toastErrorTimeout = null;
let toastSuccessTimeout = null;

const showToastError = (msg) => {
  errorMsg.value = msg;
  toastError.value = msg;
  if (toastErrorTimeout) clearTimeout(toastErrorTimeout);
  toastErrorTimeout = setTimeout(() => {
    toastError.value = '';
  }, 7000);
};

const showToastSuccess = (msg) => {
  successMsg.value = msg;
  toastSuccess.value = msg;
  if (toastSuccessTimeout) clearTimeout(toastSuccessTimeout);
  toastSuccessTimeout = setTimeout(() => {
    toastSuccess.value = '';
  }, 5000);
};

// Filtros y búsquedas
const searchQuery = ref('');
const selectedRolFilter = ref('todos');
const selectedEstadoFilter = ref('todos');

// Estado Modal Empleado
const showModalEmpleado = ref(false);
const editingEmpleadoId = ref(null);
const showPassword = ref(false);
const formEmpleado = ref({
  documento: '',
  nombre: '',
  cargo: '',
  telefono: '',
  email: '',
  rol: 'operativo',
  cuadrilla_id: '',
  estado: 'activo',
  habilitar_acceso: false,
  username: '',
  password: '',
  tiene_usuario_previo: false
});

// Estado Modal Cuadrilla
const showModalCuadrilla = ref(false);
const formCuadrilla = ref({
  nombre: '',
  especialidad: '',
  lider_id: ''
});

const userRole = ref(localStorage.getItem('smu_role') || 'operativo');

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
    errorMsg.value = 'Error al cargar la información de personal y cuadrillas.';
  } finally {
    loading.value = false;
  }
};

// Computados
const filteredEmpleados = computed(() => {
  return empleados.value.filter(emp => {
    const matchSearch = emp.nombre.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                        emp.documento.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                        emp.cargo.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchRol = selectedRolFilter.value === 'todos' || emp.rol === selectedRolFilter.value;
    const matchEstado = selectedEstadoFilter.value === 'todos' || emp.estado === selectedEstadoFilter.value;
    return matchSearch && matchRol && matchEstado;
  });
});

const totalPersonal = computed(() => empleados.value.length);
const totalOperativos = computed(() => empleados.value.filter(e => e.rol === 'operativo').length);
const totalAdministrativos = computed(() => empleados.value.filter(e => e.rol === 'administrativo' || e.rol === 'admin').length);
const totalActivos = computed(() => empleados.value.filter(e => e.estado === 'activo').length);
const totalCuadrillas = computed(() => cuadrillas.value.length);

// Operadores con perfil operativo que pueden liderar cuadrillas
const posiblesLideres = computed(() => {
  return empleados.value.filter(e => e.rol === 'operativo' || e.rol === 'admin');
});

// Sugerir nombre de usuario limpio
const suggestUsername = () => {
  if (formEmpleado.value.nombre) {
    const clean = formEmpleado.value.nombre
      .trim()
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/[^a-z0-9\s]/g, "")
      .split(/\s+/);
    if (clean.length >= 2) {
      formEmpleado.value.username = `${clean[0]}.${clean[1]}`;
      return;
    } else if (clean.length === 1 && clean[0]) {
      formEmpleado.value.username = clean[0];
      return;
    }
  }
  if (formEmpleado.value.documento) {
    formEmpleado.value.username = `user.${formEmpleado.value.documento.trim()}`;
  }
};

const onToggleHabilitarAcceso = () => {
  if (formEmpleado.value.habilitar_acceso && !formEmpleado.value.username) {
    suggestUsername();
  }
};

// Abrir Modal Empleado
const openModalEmpleado = (emp = null) => {
  userRole.value = localStorage.getItem('smu_role') || 'operativo';
  showPassword.value = false;
  errorMsg.value = '';
  toastError.value = '';
  if (emp) {
    editingEmpleadoId.value = emp.id;
    const tieneUser = !!(emp.user && emp.user.username);
    formEmpleado.value = {
      documento: emp.documento,
      nombre: emp.nombre,
      cargo: emp.cargo,
      telefono: emp.telefono || '',
      email: emp.email || '',
      rol: emp.rol,
      cuadrilla_id: emp.cuadrilla_id || '',
      estado: emp.estado,
      habilitar_acceso: tieneUser,
      username: emp.user ? emp.user.username : '',
      password: '',
      tiene_usuario_previo: tieneUser
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
      estado: 'activo',
      habilitar_acceso: false,
      username: '',
      password: '',
      tiene_usuario_previo: false
    };
  }
  showModalEmpleado.value = true;
};

// Guardar Empleado
const saveEmpleado = async () => {
  errorMsg.value = '';
  toastError.value = '';

  // Solo un admin puede asignar el rol admin
  if (formEmpleado.value.rol === 'admin' && userRole.value !== 'admin') {
    showToastError('Solo los usuarios con rol de Administrador pueden asignar el rol de Administrador.');
    return;
  }

  // Validaciones de credenciales si se habilita acceso
  if (formEmpleado.value.habilitar_acceso) {
    if (!formEmpleado.value.username || !formEmpleado.value.username.trim()) {
      showToastError('Debe especificar un nombre de usuario para habilitar el acceso al sistema.');
      return;
    }

    if (!formEmpleado.value.tiene_usuario_previo && (!formEmpleado.value.password || !formEmpleado.value.password.trim())) {
      showToastError('Debe especificar una contraseña de acceso para el nuevo usuario.');
      return;
    }

    if (formEmpleado.value.password && formEmpleado.value.password.trim()) {
      const pwd = formEmpleado.value.password.trim();
      if (pwd.length < 8) {
        showToastError('La contraseña debe tener al menos 8 caracteres.');
        return;
      }
      if (!/[a-zA-Z]/.test(pwd)) {
        showToastError('La contraseña debe contener al menos una letra.');
        return;
      }
      if (!/[0-9]/.test(pwd)) {
        showToastError('La contraseña debe contener al menos un número.');
        return;
      }
    }
  }

  savingEmpleado.value = true;
  try {
    const payload = { ...formEmpleado.value };
    if (!payload.cuadrilla_id) payload.cuadrilla_id = null;
    delete payload.tiene_usuario_previo;

    if (editingEmpleadoId.value) {
      const res = await client.put(`/empleados/${editingEmpleadoId.value}`, payload);
      if (res.data.status === 'success') {
        showToastSuccess('Empleado actualizado correctamente.');
        showModalEmpleado.value = false;
        fetchData();
      }
    } else {
      const res = await client.post('/empleados', payload);
      if (res.data.status === 'success') {
        showToastSuccess('Empleado registrado correctamente.');
        showModalEmpleado.value = false;
        fetchData();
      }
    }
  } catch (err) {
    let msg = 'Error al guardar el empleado.';
    if (err.response && err.response.data) {
      if (err.response.data.message) {
        msg = err.response.data.message;
      } else if (err.response.data.detail) {
        msg = typeof err.response.data.detail === 'string' ? err.response.data.detail : JSON.stringify(err.response.data.detail);
      }
    }
    showToastError(msg);
  } finally {
    savingEmpleado.value = false;
  }
};

// Guardar Cuadrilla
const saveCuadrilla = async () => {
  errorMsg.value = '';
  toastError.value = '';
  savingCuadrilla.value = true;
  try {
    const payload = { ...formCuadrilla.value };
    if (!payload.lider_id) payload.lider_id = null;

    const res = await client.post('/cuadrillas', payload);
    if (res.data.status === 'success') {
      showToastSuccess('Cuadrilla creada correctamente.');
      showModalCuadrilla.value = false;
      formCuadrilla.value = { nombre: '', especialidad: '', lider_id: '' };
      fetchData();
    }
  } catch (err) {
    let msg = 'Error al registrar la cuadrilla.';
    if (err.response && err.response.data) {
      if (err.response.data.message) {
        msg = err.response.data.message;
      } else if (err.response.data.detail) {
        msg = err.response.data.detail;
      }
    }
    showToastError(msg);
  } finally {
    savingCuadrilla.value = false;
  }
};

// Cambiar estado de empleado
const toggleEstadoEmpleado = async (emp) => {
  if (emp.rol === 'admin' && userRole.value !== 'admin') {
    showToastError('Solo un usuario con rol de Administrador puede modificar a un usuario Administrador.');
    return;
  }
  const nuevoEstado = emp.estado === 'activo' ? 'inactivo' : 'activo';
  try {
    await client.put(`/empleados/${emp.id}`, { ...emp, estado: nuevoEstado });
    showToastSuccess(`Empleado ${emp.nombre} ${nuevoEstado === 'activo' ? 'activado' : 'desactivado'} exitosamente.`);
    fetchData();
  } catch (err) {
    let msg = 'No se pudo cambiar el estado del empleado.';
    if (err.response && err.response.data) {
      if (err.response.data.message) msg = err.response.data.message;
      else if (err.response.data.detail) msg = err.response.data.detail;
    }
    showToastError(msg);
  }
};
</script>

<template>
  <div class="space-y-6">
    <!-- Encabezado Principal -->
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 select-none">
      <div>
        <h1 class="text-2xl font-bold tracking-tight text-neutral-900 dark:text-white flex items-center gap-2">
          <IconUsers class="w-6 h-6 text-primary stroke-[1.75]" />
          <span>Gestión de Personal y Cuadrillas</span>
        </h1>
        <p class="text-xs text-neutral-500 dark:text-neutral-400 mt-1">
          Módulo 7 (Base) — Registro Maestro de Empleados, Roles, Cargos y Asignación a Obras
        </p>
      </div>

      <div class="flex items-center gap-3">
        <Button 
          v-if="activeTab === 'empleados' && (userRole === 'admin' || userRole === 'administrativo')" 
          @click="openModalEmpleado()" 
          class="bg-primary text-primary-foreground hover:bg-primary/90 font-medium text-xs flex items-center gap-2"
        >
          <IconUserPlus class="w-4 h-4 stroke-[1.75]" />
          <span>Nuevo Empleado</span>
        </Button>
        <Button 
          v-if="activeTab === 'cuadrillas' && (userRole === 'admin' || userRole === 'administrativo')" 
          @click="showModalCuadrilla = true" 
          class="bg-primary text-primary-foreground hover:bg-primary/90 font-medium text-xs flex items-center gap-2"
        >
          <IconUsersGroup class="w-4 h-4 stroke-[1.75]" />
          <span>Nueva Cuadrilla</span>
        </Button>
      </div>
    </div>

    <!-- Alertas de estado -->
    <div v-if="successMsg" class="bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-xs p-3 rounded-lg flex items-center justify-between">
      <span class="flex items-center gap-1.5"><IconCheck class="w-4 h-4 stroke-[2]" /> {{ successMsg }}</span>
      <button @click="successMsg = ''" class="font-bold p-1 hover:bg-emerald-500/20 rounded transition-colors"><IconX class="w-4 h-4" /></button>
    </div>
    <div v-if="errorMsg" class="bg-red-500/10 border border-red-500/20 text-red-600 dark:text-red-400 text-xs p-3 rounded-lg flex items-center justify-between">
      <span class="flex items-center gap-1.5"><IconAlertTriangle class="w-4 h-4 stroke-[2]" /> {{ errorMsg }}</span>
      <button @click="errorMsg = ''" class="font-bold p-1 hover:bg-red-500/20 rounded transition-colors"><IconX class="w-4 h-4" /></button>
    </div>

    <!-- Tarjetas resumen KPI -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <Card class="bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900">
        <CardContent class="p-4 flex items-center gap-4">
          <div class="p-3 bg-blue-500/10 text-blue-600 dark:text-blue-400 rounded-xl">
            <IconUsers class="w-6 h-6 stroke-[1.75]" />
          </div>
          <div>
            <p class="text-xs font-semibold text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Total Personal</p>
            <h3 class="text-2xl font-bold text-neutral-900 dark:text-white">{{ totalPersonal }}</h3>
          </div>
        </CardContent>
      </Card>

      <Card class="bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900">
        <CardContent class="p-4 flex items-center gap-4">
          <div class="p-3 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 rounded-xl">
            <IconUserCheck class="w-6 h-6 stroke-[1.75]" />
          </div>
          <div>
            <p class="text-xs font-semibold text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Personal Operativo</p>
            <h3 class="text-2xl font-bold text-neutral-900 dark:text-white">{{ totalOperativos }}</h3>
          </div>
        </CardContent>
      </Card>

      <Card class="bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900">
        <CardContent class="p-4 flex items-center gap-4">
          <div class="p-3 bg-amber-500/10 text-amber-600 dark:text-amber-400 rounded-xl">
            <IconUsersGroup class="w-6 h-6 stroke-[1.75]" />
          </div>
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
        class="px-4 py-2 text-xs font-semibold rounded-lg transition-colors flex items-center gap-2"
        :class="activeTab === 'empleados' 
          ? 'bg-neutral-900 text-white dark:bg-white dark:text-neutral-900 shadow-sm' 
          : 'text-neutral-500 hover:text-neutral-900 dark:hover:text-white'"
      >
        <IconFolder class="w-4 h-4 stroke-[1.75]" />
        <span>Registro Maestro de Empleados</span>
      </button>
      <button 
        @click="activeTab = 'cuadrillas'" 
        class="px-4 py-2 text-xs font-semibold rounded-lg transition-colors flex items-center gap-2"
        :class="activeTab === 'cuadrillas' 
          ? 'bg-neutral-900 text-white dark:bg-white dark:text-neutral-900 shadow-sm' 
          : 'text-neutral-500 hover:text-neutral-900 dark:hover:text-white'"
      >
        <IconUsersGroup class="w-4 h-4 stroke-[1.75]" />
        <span>Cuadrillas de Obra ({{ totalCuadrillas }})</span>
      </button>
    </div>

    <!-- VISTA TAB 1: EMPLEADOS -->
    <div v-if="activeTab === 'empleados'" class="space-y-4">
      <!-- Filtros -->
      <div class="flex flex-col sm:flex-row items-center gap-3 bg-white dark:bg-neutral-950/40 p-4 rounded-xl border border-neutral-200 dark:border-neutral-900">
        <div class="w-full sm:flex-1">
          <Input 
            v-model="searchQuery" 
            placeholder="Buscar por nombre, cédula o cargo..." 
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
                    <div class="flex flex-col gap-1 items-start">
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
                      <span 
                        v-if="emp.user" 
                        class="inline-flex items-center gap-1 text-[10px] text-emerald-600 dark:text-emerald-400 font-mono bg-emerald-500/10 border border-emerald-500/20 px-1.5 py-0.5 rounded"
                        title="Usuario con credenciales activas"
                      >
                        <IconKey class="w-3 h-3 stroke-[2]" />
                        <span>@{{ emp.user.username }}</span>
                      </span>
                      <span 
                        v-else 
                        class="text-[10px] text-neutral-400 italic"
                        title="Sin cuenta de acceso al software"
                      >
                        Sin cuenta
                      </span>
                    </div>
                  </td>
                  <td class="py-3.5 px-4">
                    <span v-if="emp.cuadrilla" class="text-xs font-medium text-neutral-700 dark:text-neutral-300 flex items-center gap-1">
                      <IconUsersGroup class="w-3.5 h-3.5 text-neutral-400 shrink-0 stroke-[1.75]" />
                      <span>{{ emp.cuadrilla.nombre }}</span>
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
                      v-if="userRole === 'admin' || emp.rol !== 'admin'"
                      @click="openModalEmpleado(emp)" 
                      class="px-2.5 py-1 text-xs bg-slate-100 dark:bg-neutral-800 hover:bg-slate-200 dark:hover:bg-neutral-700 text-neutral-700 dark:text-neutral-300 rounded transition-colors inline-flex items-center gap-1"
                      title="Editar Empleado"
                    >
                      <IconPencil class="w-3.5 h-3.5 stroke-[1.75]" />
                      <span>Editar</span>
                    </button>
                    <span 
                      v-else 
                      class="px-2 py-1 text-[10px] text-neutral-400 dark:text-neutral-500 italic bg-neutral-100 dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded inline-block"
                      title="Solo un Administrador puede gestionar este perfil"
                    >
                      Protegido (Admin)
                    </span>
                    <button 
                      v-if="userRole === 'admin' || emp.rol !== 'admin'"
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
            <IconUsersGroup class="w-6 h-6 text-amber-500 stroke-[1.75]" />
          </div>
        </CardHeader>
        <CardContent class="space-y-3">
          <p class="text-xs text-neutral-500 dark:text-neutral-400">
            {{ cuad.especialidad || 'Mantenimiento preventivo y correctivo' }}
          </p>

          <div class="pt-2 border-t border-neutral-100 dark:border-neutral-900 text-xs">
            <span class="text-[10px] font-semibold uppercase text-neutral-400">Líder:</span>
            <div class="font-medium text-neutral-800 dark:text-neutral-200 mt-0.5">
              {{ cuad.lider ? cuad.lider.name : 'Sin asignar' }}
            </div>
          </div>

          <div class="pt-2 border-t border-neutral-100 dark:border-neutral-900 text-xs">
            <span class="block text-[10px] font-semibold uppercase text-neutral-400 mb-2">Integrantes ({{ cuad.empleados ? cuad.empleados.length : 0 }}):</span>
            <div class="space-y-1 max-h-32 overflow-y-auto">
              <div 
                v-for="miembro in cuad.empleados" 
                :key="miembro.id"
                class="flex items-center justify-between text-xs py-1 px-2 rounded bg-slate-50 dark:bg-neutral-900/60"
              >
                <span class="flex items-center gap-1.5"><IconUserCheck class="w-3.5 h-3.5 text-neutral-400 shrink-0 stroke-[1.75]" /> {{ miembro.nombre }}</span>
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
      <div v-if="showModalEmpleado" class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 overflow-y-auto">
        <!-- Overlay oscuro que cubre 100% de la pantalla incluyendo Navbar -->
        <div class="fixed inset-0 bg-black/70 backdrop-blur-sm" @click="showModalEmpleado = false"></div>

        <!-- Contenido Modal -->
        <div class="relative z-10 bg-white dark:bg-neutral-900 border border-slate-200 dark:border-neutral-800 rounded-2xl max-w-md w-full p-4 sm:p-6 shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto my-auto">
          <h2 class="text-lg font-bold text-slate-900 dark:text-white">
            {{ editingEmpleadoId ? 'Editar Empleado' : 'Registrar Nuevo Empleado' }}
          </h2>

          <!-- Alerta de Error Visible dentro del Modal -->
          <div v-if="errorMsg" class="bg-rose-500/10 border border-rose-500/30 text-rose-600 dark:text-rose-400 text-xs p-3 rounded-xl flex items-start gap-2.5 animate-in fade-in">
            <IconAlertTriangle class="w-4 h-4 shrink-0 mt-0.5 stroke-[2]" />
            <div class="flex-1 font-medium leading-relaxed">{{ errorMsg }}</div>
            <button type="button" @click="errorMsg = ''" class="text-rose-500 hover:text-rose-700 dark:hover:text-rose-300 p-0.5">
              <IconX class="w-3.5 h-3.5" />
            </button>
          </div>

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
                <label class="block font-semibold mb-1 text-slate-700 dark:text-neutral-300">Correo Electrónico</label>
                <Input v-model="formEmpleado.email" type="email" placeholder="correo@doblex.com" class="bg-slate-50 dark:bg-neutral-950 border-slate-300 dark:border-neutral-800 text-slate-900 dark:text-white" />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="block font-semibold mb-1 text-slate-700 dark:text-neutral-300">Rol Sistema *</label>
                <select v-model="formEmpleado.rol" class="w-full bg-slate-50 dark:bg-neutral-950 border border-slate-300 dark:border-neutral-800 rounded-md p-2 text-slate-900 dark:text-white">
                  <option value="operativo">Operativo (Campo)</option>
                  <option value="administrativo">Administrativo</option>
                  <option v-if="userRole === 'admin'" value="admin">Administrador</option>
                  <option v-else-if="formEmpleado.rol === 'admin'" value="admin" disabled>Administrador (Solo Admin)</option>
                </select>
              </div>
              <div>
                <label class="block font-semibold mb-1 text-slate-700 dark:text-neutral-300">Cuadrilla Asignada</label>
                <select v-model="formEmpleado.cuadrilla_id" class="w-full bg-slate-50 dark:bg-neutral-950 border border-slate-300 dark:border-neutral-800 rounded-md p-2 text-slate-900 dark:text-white">
                  <option value="">-- Sin Cuadrilla --</option>
                  <option v-for="c in cuadrillas" :key="c.id" :value="c.id">{{ c.nombre }}</option>
                </select>
              </div>
            </div>

            <!-- SECCIÓN ACCESO AL SISTEMA / CREDENCIALES -->
            <div class="p-3 bg-slate-50 dark:bg-neutral-950/70 border border-slate-200 dark:border-neutral-800 rounded-xl space-y-3 mt-1">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <IconKey class="w-4 h-4 text-primary shrink-0" />
                  <div>
                    <span class="block font-semibold text-slate-800 dark:text-neutral-200">Habilitar Acceso al Sistema</span>
                    <span class="block text-[11px] text-neutral-400">Crear o activar cuenta de usuario para login</span>
                  </div>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input 
                    type="checkbox" 
                    v-model="formEmpleado.habilitar_acceso" 
                    @change="onToggleHabilitarAcceso"
                    class="sr-only peer"
                  >
                  <div class="w-9 h-5 bg-neutral-300 peer-focus:outline-none rounded-full peer dark:bg-neutral-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-primary"></div>
                </label>
              </div>

              <div v-if="formEmpleado.habilitar_acceso" class="space-y-2.5 pt-2 border-t border-slate-200 dark:border-neutral-800/80">
                <div v-if="formEmpleado.tiene_usuario_previo" class="flex items-center gap-1.5 text-[11px] text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-2.5 py-1.5 rounded-lg border border-emerald-500/20">
                  <IconShieldCheck class="w-3.5 h-3.5 shrink-0" />
                  <span>Usuario activo: <strong>@{{ formEmpleado.username }}</strong>. Deja la clave en blanco si deseas conservarla.</span>
                </div>

                <div>
                  <div class="flex items-center justify-between mb-1">
                    <label class="font-semibold text-slate-700 dark:text-neutral-300">Usuario de Inicio de Sesión *</label>
                    <button 
                      v-if="!formEmpleado.tiene_usuario_previo" 
                      type="button" 
                      @click="suggestUsername" 
                      class="text-[10px] text-primary hover:underline"
                    >
                      Sugerir usuario
                    </button>
                  </div>
                  <Input 
                    v-model="formEmpleado.username" 
                    :required="formEmpleado.habilitar_acceso && !formEmpleado.tiene_usuario_previo" 
                    placeholder="Ej: carlos.perez o 1090887123" 
                    class="bg-white dark:bg-neutral-900 border-slate-300 dark:border-neutral-800 text-slate-900 dark:text-white" 
                  />
                </div>

                <div>
                  <label class="block font-semibold mb-1 text-slate-700 dark:text-neutral-300">
                    {{ formEmpleado.tiene_usuario_previo ? 'Nueva Contraseña (Opcional)' : 'Contraseña de Inicio de Sesión *' }}
                  </label>
                  <div class="relative">
                    <Input 
                      :type="showPassword ? 'text' : 'password'" 
                      v-model="formEmpleado.password" 
                      :required="formEmpleado.habilitar_acceso && !formEmpleado.tiene_usuario_previo" 
                      placeholder="Mínimo 8 caracteres (letras y números)" 
                      class="bg-white dark:bg-neutral-900 border-slate-300 dark:border-neutral-800 text-slate-900 dark:text-white pr-9" 
                    />
                    <button 
                      type="button" 
                      @click="showPassword = !showPassword" 
                      class="absolute right-2.5 top-1/2 -translate-y-1/2 text-neutral-400 hover:text-neutral-200"
                      tabindex="-1"
                    >
                      <IconEyeOff v-if="showPassword" class="w-4 h-4" />
                      <IconEye v-else class="w-4 h-4" />
                    </button>
                  </div>
                  <span class="block text-[10px] text-neutral-400 mt-1">
                    Requisito de seguridad: mínimo 8 caracteres, al menos una letra y un número.
                  </span>
                </div>
              </div>
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
                :disabled="savingEmpleado"
                class="px-4 py-2 text-xs font-semibold rounded-lg bg-primary text-white hover:bg-primary/90 shadow-sm transition-colors flex items-center gap-1.5 disabled:opacity-60 disabled:cursor-not-allowed"
              >
                <span v-if="savingEmpleado" class="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                <span>{{ savingEmpleado ? 'Guardando...' : 'Guardar' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- MODAL NUEVA CUADRILLA -->
    <Teleport to="body">
      <div v-if="showModalCuadrilla" class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 overflow-y-auto">
        <!-- Overlay oscuro que cubre 100% de la pantalla incluyendo Navbar -->
        <div class="fixed inset-0 bg-black/70 backdrop-blur-sm" @click="showModalCuadrilla = false"></div>

        <!-- Contenido Modal -->
        <div class="relative z-10 bg-white dark:bg-neutral-900 border border-slate-200 dark:border-neutral-800 rounded-2xl max-w-md w-full p-4 sm:p-6 shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto my-auto">
          <h2 class="text-lg font-bold text-slate-900 dark:text-white">Crear Nueva Cuadrilla de Obra</h2>

          <!-- Alerta de Error Visible dentro del Modal -->
          <div v-if="errorMsg" class="bg-rose-500/10 border border-rose-500/30 text-rose-600 dark:text-rose-400 text-xs p-3 rounded-xl flex items-start gap-2.5 animate-in fade-in">
            <IconAlertTriangle class="w-4 h-4 shrink-0 mt-0.5 stroke-[2]" />
            <div class="flex-1 font-medium leading-relaxed">{{ errorMsg }}</div>
            <button type="button" @click="errorMsg = ''" class="text-rose-500 hover:text-rose-700 dark:hover:text-rose-300 p-0.5">
              <IconX class="w-3.5 h-3.5" />
            </button>
          </div>

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
                :disabled="savingCuadrilla"
                class="px-4 py-2 text-xs font-semibold rounded-lg bg-primary text-white hover:bg-primary/90 shadow-sm transition-colors flex items-center gap-1.5 disabled:opacity-60 disabled:cursor-not-allowed"
              >
                <span v-if="savingCuadrilla" class="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                <span>{{ savingCuadrilla ? 'Creando...' : 'Crear Cuadrilla' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- NOTIFICACIONES TOAST FLOTANTES GLOBALES (SIEMPRE VISIBLES SOBRE CUALQUIER MODAL) -->
    <Teleport to="body">
      <div class="fixed top-5 right-5 z-[9999] flex flex-col gap-2.5 max-w-sm w-full pointer-events-none px-4 sm:px-0">
        <!-- Toast Error -->
        <transition
          enter-active-class="transform ease-out duration-300 transition"
          enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
          enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
          leave-active-class="transition ease-in duration-200"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
        >
          <div 
            v-if="toastError" 
            class="pointer-events-auto bg-rose-600 text-white p-4 rounded-xl shadow-2xl flex items-start gap-3 border border-rose-700/50"
          >
            <IconAlertTriangle class="w-5 h-5 shrink-0 stroke-[2] mt-0.5 text-rose-100" />
            <div class="flex-1 text-xs font-medium leading-relaxed">
              <span class="block font-bold text-sm mb-0.5 text-white">Error en la Operación</span>
              {{ toastError }}
            </div>
            <button @click="toastError = ''" class="text-white/80 hover:text-white p-1 rounded-md hover:bg-white/10 transition-colors">
              <IconX class="w-4 h-4" />
            </button>
          </div>
        </transition>

        <!-- Toast Success -->
        <transition
          enter-active-class="transform ease-out duration-300 transition"
          enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
          enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
          leave-active-class="transition ease-in duration-200"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
        >
          <div 
            v-if="toastSuccess" 
            class="pointer-events-auto bg-emerald-600 text-white p-4 rounded-xl shadow-2xl flex items-start gap-3 border border-emerald-700/50"
          >
            <IconCheck class="w-5 h-5 shrink-0 stroke-[2] mt-0.5 text-emerald-100" />
            <div class="flex-1 text-xs font-medium leading-relaxed">
              <span class="block font-bold text-sm mb-0.5 text-white">Operación Exitosa</span>
              {{ toastSuccess }}
            </div>
            <button @click="toastSuccess = ''" class="text-white/80 hover:text-white p-1 rounded-md hover:bg-white/10 transition-colors">
              <IconX class="w-4 h-4" />
            </button>
          </div>
        </transition>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import client from '@/api/client';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Dialog } from '@/components/ui/dialog';
import { Card } from '@/components/ui/card';
import SlaBadge from '@/components/common/SlaBadge.vue';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

const openCreateModal = ref(false);
const openEditModal = ref(false);
const openAvanceModal = ref(false);

const searchQuery = ref('');
const statusFilter = ref('todos');

const ots = ref([]);
const operadores = ref([]);
const cuadrillas = ref([]);
const userRole = ref('operativo');
const currentUsername = ref('');
const loading = ref(false);
const errorMsg = ref('');

// Datos para registrar nueva OT (Administración)
const newOt = ref({
  codigo: '',
  descripcion: '',
  sitio: '',
  ubicacion: '',
  user_id: '', // Operador asignado
  cuadrilla_id: '',
  prioridad: 'P2',
  tipo_ubicacion: 'urbana',
  tipo_mantenimiento: 'preventivo',
  subsistema: 'Movil Sistema Eléctrico',
  tipo_gasto: 'OPEX',
  fecha_inicio: new Date().toISOString().split('T')[0]
});

// Datos para editar OT (Administración)
const editingOt = ref({
  id: null,
  codigo: '',
  descripcion: '',
  sitio: '',
  ubicacion: '',
  user_id: '',
  cuadrilla_id: '',
  prioridad: 'P2',
  tipo_ubicacion: 'urbana',
  tipo_mantenimiento: 'preventivo',
  subsistema: 'Movil Sistema Eléctrico',
  tipo_gasto: 'OPEX',
  estado: 'asignada',
  fecha_inicio: new Date().toISOString().split('T')[0]
});

// Abrir modal de edición con datos precargados
const openEditOt = (ot) => {
  editingOt.value = {
    id: ot.id,
    codigo: ot.codigo,
    descripcion: ot.descripcion,
    sitio: ot.sitio || '',
    ubicacion: ot.ubicacion,
    user_id: ot.user_id || (ot.assigned_user ? ot.assigned_user.id : ''),
    cuadrilla_id: ot.cuadrilla_id || '',
    prioridad: ot.prioridad || 'P2',
    tipo_ubicacion: ot.tipo_ubicacion || 'urbana',
    tipo_mantenimiento: ot.tipo_mantenimiento || 'preventivo',
    subsistema: ot.subsistema || 'Movil Sistema Eléctrico',
    tipo_gasto: ot.tipo_gasto || 'OPEX',
    estado: ot.estado || 'asignada',
    fecha_inicio: ot.fecha_inicio ? ot.fecha_inicio.split(' ')[0] : new Date().toISOString().split('T')[0]
  };
  openEditModal.value = true;
};

const updateOt = async () => {
  errorMsg.value = '';
  try {
    const payload = { ...editingOt.value };
    if (!payload.cuadrilla_id) payload.cuadrilla_id = null;

    const response = await client.put(`/ots/${editingOt.value.id}`, payload);
    if (response.data.status === 'success') {
      await loadOts();
      openEditModal.value = false;
    }
  } catch (err) {
    if (err.response && err.response.data && err.response.data.message) {
      errorMsg.value = err.response.data.message;
    } else {
      errorMsg.value = 'Error al actualizar la Orden de Trabajo.';
    }
  }
};

// Al seleccionar un operador, auto-seleccionar la cuadrilla a la que pertenece
const onOperatorChange = (userId, mode = 'create') => {
  if (!userId) return;
  const selectedOp = operadores.value.find(op => op.id === userId || op.id === Number(userId));
  if (selectedOp && selectedOp.cuadrilla_id) {
    if (mode === 'create') {
      newOt.value.cuadrilla_id = selectedOp.cuadrilla_id;
    } else if (mode === 'edit') {
      editingOt.value.cuadrilla_id = selectedOp.cuadrilla_id;
    }
  }
};

// Datos para registrar avance (Operario)
const selectedOt = ref(null);
const newAvance = ref({
  descripcion: '',
  porcentaje: 10,
  fecha_reporte: new Date().toISOString().split('T')[0]
});

const loadOts = async () => {
  loading.value = true;
  errorMsg.value = '';
  try {
    const response = await client.get('/ots');
    if (response.data.status === 'success') {
      ots.value = response.data.data;
    }
  } catch (err) {
    errorMsg.value = 'Error al cargar las Órdenes de Trabajo del servidor.';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const loadOperadores = async () => {
  try {
    const response = await client.get('/operadores');
    if (response.data.status === 'success') {
      operadores.value = response.data.data;
    }
  } catch (err) {
    console.error('Error al cargar operadores:', err);
  }
};

const loadCuadrillas = async () => {
  try {
    const response = await client.get('/cuadrillas');
    if (response.data.status === 'success') {
      cuadrillas.value = response.data.data;
    }
  } catch (err) {
    console.error('Error al cargar cuadrillas:', err);
  }
};

onMounted(() => {
  userRole.value = localStorage.getItem('smu_role') || 'operativo';
  currentUsername.value = localStorage.getItem('smu_username') || '';
  
  loadOts();
  loadCuadrillas();
  
  if (userRole.value === 'admin' || userRole.value === 'administrativo') {
    loadOperadores();
  }
});

const filteredOts = computed(() => {
  return ots.value.filter(ot => {
    const searchLower = searchQuery.value.toLowerCase();
    
    // Búsqueda por código, descripción, ubicación o por el nombre del encargado
    const matchesSearch = ot.codigo.toLowerCase().includes(searchLower) || 
                         ot.descripcion.toLowerCase().includes(searchLower) ||
                         ot.ubicacion.toLowerCase().includes(searchLower) ||
                         (ot.assigned_user && ot.assigned_user.name.toLowerCase().includes(searchLower)) ||
                         (ot.cuadrilla && ot.cuadrilla.nombre.toLowerCase().includes(searchLower));
    
    const matchesStatus = statusFilter.value === 'todos' || ot.estado === statusFilter.value;

    return matchesSearch && matchesStatus;
  });
});

const createOt = async () => {
  errorMsg.value = '';
  try {
    const payload = { ...newOt.value };
    if (!payload.cuadrilla_id) payload.cuadrilla_id = null;

    const response = await client.post('/ots', payload);
    if (response.data.status === 'success') {
      // Recargar OTs y cerrar modal
      await loadOts();
      openCreateModal.value = false;
      
      // Limpiar formulario
      newOt.value = {
        codigo: '',
        descripcion: '',
        sitio: '',
        ubicacion: '',
        user_id: '',
        cuadrilla_id: '',
        prioridad: 'P2',
        tipo_ubicacion: 'urbana',
        tipo_mantenimiento: 'preventivo',
        subsistema: 'Movil Sistema Eléctrico',
        tipo_gasto: 'OPEX',
        fecha_inicio: new Date().toISOString().split('T')[0]
      };
    }
  } catch (err) {
    if (err.response && err.response.data && err.response.data.message) {
      errorMsg.value = err.response.data.message;
    } else {
      errorMsg.value = 'Error al crear la Orden de Trabajo.';
    }
  }
};

const openReportAvance = (ot) => {
  selectedOt.value = ot;
  newAvance.value = {
    descripcion: '',
    porcentaje: Math.min(10, 100 - ot.progreso), // Valor por defecto sensato
    fecha_reporte: new Date().toISOString().split('T')[0]
  };
  openAvanceModal.value = true;
};

const submitAvance = async () => {
  errorMsg.value = '';
  try {
    const response = await client.post('/avances', {
      ot_id: selectedOt.value.id,
      descripcion: newAvance.value.descripcion,
      porcentaje: newAvance.value.porcentaje,
      fecha_reporte: newAvance.value.fecha_reporte
    });
    
    if (response.data.status === 'success') {
      await loadOts();
      openAvanceModal.value = false;
      selectedOt.value = null;
    }
  } catch (err) {
    if (err.response && err.response.data && err.response.data.message) {
      errorMsg.value = err.response.data.message;
    } else {
      errorMsg.value = 'Error al registrar el avance en el servidor.';
    }
  }
};

const getStatusBadgeVariant = (status) => {
  switch (status) {
    case 'finalizado': return 'secondary';
    case 'en_progreso': return 'default';
    case 'pendiente': return 'outline';
    default: return 'outline';
  }
};

const getStatusLabel = (status) => {
  switch (status) {
    case 'pendiente': return 'Pendiente';
    case 'en_progreso': return 'En Progreso';
    case 'finalizado': return 'Finalizado';
    default: return status;
  }
};
</script>

<template>
  <div class="flex flex-col gap-6 select-none">
    <!-- Encabezado de la Sección -->
    <div class="flex flex-col gap-4 sm:flex-row sm:justify-between sm:items-center bg-white dark:bg-[#1b2030] border border-neutral-200 dark:border-neutral-800 p-4 md:p-6 rounded-xl relative overflow-hidden shadow-sm transition-colors duration-300">
      <div>
        <h1 class="text-xl font-bold tracking-tight text-neutral-900 dark:text-white mb-0.5">Listado de Órdenes (OT)</h1>
        <p class="text-xs text-neutral-500">
          <span v-if="userRole === 'admin'">Gestión de actividades y asignación global de OTs a operadores</span>
          <span v-else-if="userRole === 'administrativo'">Control de OTs creadas por tu usuario administrativo</span>
          <span v-else>Panel de actividades asignadas y reporte diario de avance en campo</span>
        </p>
      </div>
      <Button 
        v-if="userRole === 'admin' || userRole === 'administrativo'"
        @click="openCreateModal = true" 
        class="bg-primary text-primary-foreground hover:bg-primary/95 flex items-center gap-2 font-semibold w-full sm:w-auto justify-center"
      >
        <span class="text-sm">➕</span> Nueva OT
      </Button>
    </div>

    <!-- Panel de Registro de Órdenes -->
    <Card class="bg-white dark:bg-[#1b2030] border-neutral-200 dark:border-neutral-800 p-4 md:p-6 flex flex-col gap-4 shadow-sm transition-colors duration-300">
      <div class="flex flex-col lg:flex-row justify-between lg:items-center gap-4 border-b border-neutral-100 dark:border-neutral-800 pb-5">
        <div>
          <h2 class="text-base font-bold text-neutral-900 dark:text-white mb-0.5">Registro de Órdenes</h2>
          <p class="text-xs text-neutral-500">Control de OTs y avances del personal en campo</p>
        </div>
        
        <!-- Filtros -->
        <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 w-full lg:w-auto">
          <Input 
            type="text" 
            placeholder="Buscar por código, descripción u operador..." 
            v-model="searchQuery" 
            class="w-full lg:w-72 bg-white dark:bg-[#141824] border-neutral-200 dark:border-neutral-800 text-neutral-800 dark:text-white text-xs placeholder:text-neutral-450 focus-visible:ring-primary focus-visible:border-primary"
          />
          <select 
            v-model="statusFilter" 
            class="flex h-9 w-full sm:w-40 rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#141824] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring focus:border-primary focus:ring-primary cursor-pointer"
          >
            <option value="todos">Todos los Estados</option>
            <option value="pendiente">Pendientes</option>
            <option value="en_progreso">En Progreso</option>
            <option value="finalizado">Finalizados</option>
          </select>
        </div>
      </div>

      <div v-if="errorMsg" class="bg-red-500/10 border border-red-500/20 text-red-500 dark:text-red-400 text-xs py-2 px-3 rounded-md text-center font-medium">
        {{ errorMsg }}
      </div>

      <!-- Tabla de Órdenes con scroll horizontal responsivo -->
      <div class="overflow-x-auto -mx-4 px-4 sm:mx-0 sm:px-0">
        <div class="inline-block min-w-full align-middle">
          <Table>
            <TableHeader class="border-neutral-100 dark:border-neutral-900">
              <TableRow class="hover:bg-transparent border-neutral-100 dark:border-neutral-900">
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase pl-4">Código / SLA</TableHead>
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase">Sitio / Alcance</TableHead>
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase">Tipo & Criticidad</TableHead>
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase">Subsistema & Gasto</TableHead>
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase">Ubicación</TableHead>
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase">Encargado (Operador)</TableHead>
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase w-[130px]">Progreso</TableHead>
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase text-center">Estado</TableHead>
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase text-right pr-4">Acciones</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow v-for="ot in filteredOts" :key="ot.id" class="border-neutral-100 dark:border-neutral-900 hover:bg-neutral-50 dark:hover:bg-white/[0.02]">
                <TableCell class="pl-4 py-4">
                  <div class="flex flex-col gap-1">
                    <span class="font-mono font-bold text-primary text-xs">{{ ot.codigo }}</span>
                    <SlaBadge v-if="ot.fecha_limite_sla" :fecha-limite="ot.fecha_limite_sla" :estado="ot.estado" />
                  </div>
                </TableCell>
                <TableCell class="py-4">
                  <div class="flex flex-col max-w-xs">
                    <span v-if="ot.sitio" class="font-bold text-neutral-900 dark:text-white text-xs line-clamp-1">📡 {{ ot.sitio }}</span>
                    <span class="text-xs text-neutral-600 dark:text-neutral-300 line-clamp-1">{{ ot.descripcion }}</span>
                    <span class="text-[10px] text-neutral-400 mt-0.5">Inicio: {{ ot.fecha_inicio }}</span>
                  </div>
                </TableCell>
                <TableCell class="py-4 whitespace-nowrap">
                  <div class="flex flex-col gap-1 items-start">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase shadow-sm" :class="ot.tipo_mantenimiento === 'emergencia' ? 'bg-rose-100 text-rose-800 border border-rose-200 dark:bg-rose-950/60 dark:text-rose-400 dark:border-rose-500/30' : ot.tipo_mantenimiento === 'correctivo' ? 'bg-amber-100 text-amber-800 border border-amber-200 dark:bg-amber-950/60 dark:text-amber-400 dark:border-amber-500/30' : 'bg-blue-100 text-blue-800 border border-blue-200 dark:bg-blue-950/60 dark:text-blue-400 dark:border-blue-500/30'">
                      {{ ot.tipo_mantenimiento || 'Preventivo' }}
                    </span>
                    <span class="text-[10px] font-semibold text-neutral-600 dark:text-slate-400">
                      Prioridad {{ ot.prioridad || 'P2' }} ({{ (ot.tipo_ubicacion || 'urbana').toUpperCase() }})
                    </span>
                  </div>
                </TableCell>
                <TableCell class="py-4 whitespace-nowrap">
                  <div class="flex flex-col text-xs">
                    <span class="font-semibold text-neutral-900 dark:text-neutral-200">{{ ot.subsistema || 'Sistema Eléctrico' }}</span>
                    <span class="text-[10px] font-mono text-neutral-500 dark:text-neutral-400 uppercase font-bold">{{ ot.tipo_gasto || 'OPEX' }}</span>
                  </div>
                </TableCell>
                <TableCell class="text-neutral-700 dark:text-neutral-350 py-4 whitespace-nowrap text-xs">📍 {{ ot.ubicacion }}</TableCell>
                <TableCell class="text-neutral-700 dark:text-neutral-350 py-4 whitespace-nowrap text-xs font-medium">
                  <div>{{ ot.assigned_user ? ot.assigned_user.name : 'No Asignado' }}</div>
                  <span v-if="ot.cuadrilla" class="block text-[10px] text-neutral-400 font-normal">🏗️ {{ ot.cuadrilla.nombre }}</span>
                </TableCell>
                <TableCell class="py-4">
                  <div class="flex items-center gap-2">
                    <Progress :model-value="ot.progreso" class="h-1.5 w-16 bg-neutral-100 dark:bg-white/5" />
                    <span class="text-xs font-semibold text-neutral-600 dark:text-neutral-400">{{ ot.progreso }}%</span>
                  </div>
                </TableCell>
                <TableCell class="text-center py-4">
                  <Badge 
                    :variant="getStatusBadgeVariant(ot.estado)" 
                    class="text-[10px] font-bold px-2 py-0.5 uppercase tracking-wider"
                    :class="{
                      'bg-emerald-500/10 border-emerald-500/20 text-emerald-600 dark:text-emerald-400 hover:bg-emerald-500/10': ['finalizado', 'solucionada'].includes(ot.estado),
                      'bg-primary/10 border-primary/20 text-primary hover:bg-primary/10': ['en_progreso', 'en_sitio', 'en_camino'].includes(ot.estado),
                      'bg-amber-500/10 border-amber-500/20 text-amber-600 dark:text-amber-400 hover:bg-amber-500/10': ['pendiente', 'asignada'].includes(ot.estado),
                    }"
                  >
                    {{ getStatusLabel(ot.estado) }}
                  </Badge>
                </TableCell>
                <TableCell class="text-right pr-4 py-4">
                  <div class="inline-flex gap-1">
                    <Button 
                      v-if="userRole === 'admin' || userRole === 'administrativo'"
                      @click="openEditOt(ot)"
                      variant="ghost" 
                      size="icon" 
                      class="h-8 w-8 text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white hover:bg-neutral-100 dark:hover:bg-white/5" 
                      title="Detalles / Editar"
                    >
                      ✏️
                    </Button>
                    <Button 
                      v-if="userRole === 'operativo' && !['finalizado', 'solucionada'].includes(ot.estado)"
                      @click="openReportAvance(ot)"
                      variant="outline" 
                      size="sm" 
                      class="h-8 border-primary/25 hover:bg-primary/10 hover:border-primary/50 text-primary font-semibold text-xs px-2.5 flex items-center gap-1.5" 
                      title="Reportar Avance Diario"
                    >
                      <span>🛠️</span> Avance
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
              <TableRow v-if="filteredOts.length === 0" class="hover:bg-transparent">
                <TableCell colspan="7" class="text-center text-neutral-500 py-10">
                  <span v-if="loading">Cargando registros desde el servidor de base de datos...</span>
                  <span v-else>No se encontraron órdenes de trabajo para mostrar.</span>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </div>
      </div>
    </Card>

    <!-- Modal 1: Registrar Nueva OT (Administrador/Administrativo) -->
    <Dialog :open="openCreateModal" @close="openCreateModal = false">
      <div class="flex items-center justify-between border-b border-neutral-200 dark:border-neutral-900 pb-4 mb-5">
        <div>
          <h3 class="text-base font-bold text-neutral-900 dark:text-white">Crear Nueva Orden de Trabajo</h3>
          <p class="text-[11px] text-neutral-500">Completa los campos para registrar una nueva orden de trabajo</p>
        </div>
        <button @click="openCreateModal = false" class="text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white text-lg font-bold">&times;</button>
      </div>

      <form @submit.prevent="createOt" class="space-y-4">
        <!-- Fila 1: Código OT & Sitio / Estación Base -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Código OT *</label>
            <Input type="text" v-model="newOt.codigo" required placeholder="OT-2026-004" class="bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-850 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
          </div>
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Sitio / Estación Base (EB)</label>
            <Input type="text" v-model="newOt.sitio" placeholder="Ej. ANT.TITIRIBI LA ALBANIA" class="bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-850 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
          </div>
        </div>

        <!-- Fila 2: Descripción de la Obra -->
        <div class="space-y-1.5">
          <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Descripción de la Obra / Falla *</label>
          <Input type="text" v-model="newOt.descripcion" required placeholder="Mantenimiento correctivo de planta eléctrica y rectificador" class="bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-850 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
        </div>

        <!-- Fila 3: Tipo de Mantenimiento, Prioridad & Ubicación -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Tipo Mantenimiento *</label>
            <select 
              v-model="newOt.tipo_mantenimiento" 
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-950 px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
            >
              <option value="preventivo">Preventivo (Rutinario)</option>
              <option value="correctivo">Correctivo (Planificado)</option>
              <option value="emergencia">Atención de Emergencia</option>
            </select>
          </div>

          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Prioridad / Criticidad *</label>
            <select 
              v-model="newOt.prioridad" 
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-950 px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
            >
              <option value="P1">P1 - Alta (Falla Crítica)</option>
              <option value="P2">P2 - Media (Convencional)</option>
              <option value="P3">P3 - Baja (Difícil Acceso)</option>
            </select>
          </div>

          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Zona de Ubicación *</label>
            <select 
              v-model="newOt.tipo_ubicacion" 
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-950 px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
            >
              <option value="urbana">Urbana</option>
              <option value="rural">Rural / Difícil Acceso</option>
            </select>
          </div>
        </div>

        <!-- Fila 4: Subsistema & Tipo de Gasto -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Subsistema Intervenido</label>
            <select 
              v-model="newOt.subsistema" 
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-950 px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
            >
              <option value="Movil Aires Acondicionados">Móvil Aires Acondicionados</option>
              <option value="Movil Plantas Eléctricas">Móvil Plantas Eléctricas</option>
              <option value="Movil Sistema Eléctrico">Móvil Sistema Eléctrico (MT/BT/SPT)</option>
              <option value="Movil Power">Móvil Power (Rectificadores/Baterías)</option>
              <option value="Móvil Acceso-Transmisión">Móvil Acceso - Transmisión</option>
              <option value="Móvil Apoyo Integral">Móvil Apoyo Integral</option>
              <option value="Móvil Híbridos SFV">Móvil Híbridos o SFV (Solar)</option>
            </select>
          </div>

          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Tipo de Gasto</label>
            <select 
              v-model="newOt.tipo_gasto" 
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-950 px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
            >
              <option value="OPEX">OPEX (Operativo)</option>
              <option value="CAPEX">CAPEX (Inversión)</option>
            </select>
          </div>
        </div>

        <!-- Fila 5: Ubicación Geográfica, Operador & Cuadrilla -->
        <div class="space-y-1.5">
          <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Ubicación / Municipio *</label>
          <Input type="text" v-model="newOt.ubicacion" required placeholder="Titiribí, Antioquia - Zona R3-Occidente" class="bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-850 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Operador Asignado *</label>
            <select 
              v-model="newOt.user_id" 
              @change="onOperatorChange(newOt.user_id, 'create')"
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-950 px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
            >
              <option value="" disabled>Selecciona el encargado</option>
              <option v-for="op in operadores" :key="op.id" :value="op.id">
                {{ op.name }} ({{ op.username }})
              </option>
            </select>
          </div>
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Cuadrilla Asignada (Opcional)</label>
            <select 
              v-model="newOt.cuadrilla_id" 
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-950 px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
            >
              <option value="">Sin cuadrilla específica</option>
              <option v-for="c in cuadrillas" :key="c.id" :value="c.id">
                🏗️ {{ c.nombre }}
              </option>
            </select>
          </div>
        </div>

        <div class="space-y-1.5">
          <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Fecha de Inicio *</label>
          <Input type="date" v-model="newOt.fecha_inicio" required class="bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-850 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
        </div>

        <div class="flex flex-col sm:flex-row justify-end gap-2 border-t border-neutral-200 dark:border-neutral-900 pt-5 mt-6">
          <Button type="button" variant="outline" @click="openCreateModal = false" class="border-neutral-200 dark:border-neutral-800 hover:bg-neutral-100 dark:hover:bg-white/5 text-neutral-700 dark:text-neutral-300 w-full sm:w-auto">
            Cancelar
          </Button>
          <Button type="submit" class="bg-primary text-primary-foreground hover:bg-primary/95 font-semibold w-full sm:w-auto">
            Registrar OT
          </Button>
        </div>
      </form>
    </Dialog>

    <!-- Modal de Editar OT (Administrador/Administrativo) -->
    <Dialog :open="openEditModal" @close="openEditModal = false">
      <div class="flex items-center justify-between border-b border-neutral-200 dark:border-neutral-800 pb-4 mb-5">
        <div>
          <h3 class="text-base font-bold text-neutral-900 dark:text-white">Editar Orden de Trabajo</h3>
          <p class="text-[11px] text-neutral-500">Actualiza los datos y asignación de la OT {{ editingOt.codigo }}</p>
        </div>
        <button @click="openEditModal = false" class="text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white text-lg font-bold">&times;</button>
      </div>

      <form @submit.prevent="updateOt" class="space-y-4">
        <!-- Fila 1: Código OT & Sitio / Estación Base -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Código OT *</label>
            <Input type="text" v-model="editingOt.codigo" required class="bg-white dark:bg-[#141824] border-neutral-200 dark:border-neutral-800 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
          </div>
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Sitio / Estación Base (EB)</label>
            <Input type="text" v-model="editingOt.sitio" placeholder="Ej. ANT.TITIRIBI LA ALBANIA" class="bg-white dark:bg-[#141824] border-neutral-200 dark:border-neutral-800 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
          </div>
        </div>

        <!-- Fila 2: Descripción de la Obra -->
        <div class="space-y-1.5">
          <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Descripción de la Obra / Falla *</label>
          <Input type="text" v-model="editingOt.descripcion" required class="bg-white dark:bg-[#141824] border-neutral-200 dark:border-neutral-800 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
        </div>

        <!-- Fila 3: Tipo de Mantenimiento, Prioridad & Ubicación -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Tipo Mantenimiento *</label>
            <select 
              v-model="editingOt.tipo_mantenimiento" 
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#141824] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
            >
              <option value="preventivo">Preventivo (Rutinario)</option>
              <option value="correctivo">Correctivo (Planificado)</option>
              <option value="emergencia">Atención de Emergencia</option>
            </select>
          </div>

          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Prioridad / Criticidad *</label>
            <select 
              v-model="editingOt.prioridad" 
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#141824] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
            >
              <option value="P1">P1 - Alta (Falla Crítica)</option>
              <option value="P2">P2 - Media (Convencional)</option>
              <option value="P3">P3 - Baja (Difícil Acceso)</option>
            </select>
          </div>

          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Zona de Ubicación *</label>
            <select 
              v-model="editingOt.tipo_ubicacion" 
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#141824] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
            >
              <option value="urbana">Urbana</option>
              <option value="rural">Rural / Difícil Acceso</option>
            </select>
          </div>
        </div>

        <!-- Fila 4: Subsistema, Tipo de Gasto & Estado -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Subsistema Intervenido</label>
            <select 
              v-model="editingOt.subsistema" 
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#141824] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
            >
              <option value="Movil Aires Acondicionados">Móvil Aires Acondicionados</option>
              <option value="Movil Plantas Eléctricas">Móvil Plantas Eléctricas</option>
              <option value="Movil Sistema Eléctrico">Móvil Sistema Eléctrico (MT/BT/SPT)</option>
              <option value="Movil Power">Móvil Power (Rectificadores/Baterías)</option>
              <option value="Móvil Acceso-Transmisión">Móvil Acceso - Transmisión</option>
              <option value="Móvil Apoyo Integral">Móvil Apoyo Integral</option>
              <option value="Móvil Híbridos SFV">Móvil Híbridos o SFV (Solar)</option>
            </select>
          </div>

          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Tipo de Gasto</label>
            <select 
              v-model="editingOt.tipo_gasto" 
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#141824] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
            >
              <option value="OPEX">OPEX (Operativo)</option>
              <option value="CAPEX">CAPEX (Inversión)</option>
            </select>
          </div>

          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Estado de la OT *</label>
            <select 
              v-model="editingOt.estado" 
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#141824] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
            >
              <option value="asignada">Asignada / Pendiente</option>
              <option value="en_camino">En Camino</option>
              <option value="en_sitio">En Sitio</option>
              <option value="en_progreso">En Progreso</option>
              <option value="detenida_materiales">Detenida por Materiales</option>
              <option value="solucionada">Solucionada</option>
              <option value="finalizada">Finalizada</option>
            </select>
          </div>
        </div>

        <!-- Fila 5: Ubicación Geográfica, Operador & Cuadrilla -->
        <div class="space-y-1.5">
          <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Ubicación / Municipio *</label>
          <Input type="text" v-model="editingOt.ubicacion" required class="bg-white dark:bg-[#141824] border-neutral-200 dark:border-neutral-800 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Operador Asignado *</label>
            <select 
              v-model="editingOt.user_id" 
              @change="onOperatorChange(editingOt.user_id, 'edit')"
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#141824] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
            >
              <option value="" disabled>Selecciona el encargado</option>
              <option v-for="op in operadores" :key="op.id" :value="op.id">
                {{ op.name }} ({{ op.username }})
              </option>
            </select>
          </div>
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Cuadrilla Asignada (Opcional)</label>
            <select 
              v-model="editingOt.cuadrilla_id" 
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#141824] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
            >
              <option value="">Sin cuadrilla específica</option>
              <option v-for="c in cuadrillas" :key="c.id" :value="c.id">
                🏗️ {{ c.nombre }}
              </option>
            </select>
          </div>
        </div>

        <div class="space-y-1.5">
          <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Fecha de Inicio *</label>
          <Input type="date" v-model="editingOt.fecha_inicio" required class="bg-white dark:bg-[#141824] border-neutral-200 dark:border-neutral-800 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
        </div>

        <div class="flex flex-col sm:flex-row justify-end gap-2 border-t border-neutral-200 dark:border-neutral-800 pt-5 mt-6">
          <Button type="button" variant="outline" @click="openEditModal = false" class="border-neutral-200 dark:border-neutral-800 hover:bg-neutral-100 dark:hover:bg-white/5 text-neutral-700 dark:text-neutral-300 w-full sm:w-auto">
            Cancelar
          </Button>
          <Button type="submit" class="bg-primary text-primary-foreground hover:bg-primary/95 font-semibold w-full sm:w-auto">
            Guardar Cambios
          </Button>
        </div>
      </form>
    </Dialog>

    <!-- Modal 2: Reportar Avance Diario (Solo Operativo) -->
    <Dialog :open="openAvanceModal" @close="openAvanceModal = false">
      <div class="flex items-center justify-between border-b border-neutral-200 dark:border-neutral-900 pb-4 mb-5">
        <div>
          <h3 class="text-base font-bold text-neutral-900 dark:text-white">Reportar Avance en Campo</h3>
          <p class="text-[11px] text-neutral-500">Registra el progreso diario de las actividades de hoy</p>
        </div>
        <button @click="openAvanceModal = false" class="text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white text-lg font-bold">&times;</button>
      </div>

      <div v-if="selectedOt" class="mb-4 bg-neutral-100 dark:bg-neutral-900/60 border border-neutral-200 dark:border-neutral-850 p-4 rounded-lg">
        <div class="text-[10px] font-bold text-neutral-400 dark:text-neutral-550 uppercase tracking-wider">Orden de Trabajo Seleccionada</div>
        <div class="text-sm font-bold text-primary mt-1">{{ selectedOt.codigo }}</div>
        <div class="text-xs text-neutral-700 dark:text-neutral-300 mt-1">{{ selectedOt.descripcion }}</div>
        <div class="flex justify-between items-center mt-3 text-xs text-neutral-500">
          <span>Progreso Actual: <b>{{ selectedOt.progreso }}%</b></span>
          <span>Máximo a Reportar: <b>{{ 100 - selectedOt.progreso }}%</b></span>
        </div>
      </div>

      <form @submit.prevent="submitAvance" class="space-y-4">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Porcentaje de Avance Hoy (%)</label>
            <Input 
              type="number" 
              v-model="newAvance.porcentaje" 
              required 
              min="1" 
              :max="100 - (selectedOt ? selectedOt.progreso : 0)" 
              placeholder="10" 
              class="bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-850 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" 
            />
          </div>
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Fecha del Reporte</label>
            <Input type="date" v-model="newAvance.fecha_reporte" required class="bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-850 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
          </div>
        </div>

        <div class="space-y-1.5">
          <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Descripción detallada de la Actividad Realizada</label>
          <textarea 
            v-model="newAvance.descripcion" 
            required 
            rows="3" 
            placeholder="Ej: Armado y replanteo de zapatas en sector Norte. Vaciado de 3 metros cubicos de concreto."
            class="flex min-h-[80px] w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-950 px-3 py-2 text-xs ring-offset-background placeholder:text-neutral-400 dark:placeholder:text-neutral-600 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring focus-visible:ring-primary focus:border-primary text-neutral-900 dark:text-white"
          ></textarea>
        </div>

        <div class="flex flex-col sm:flex-row justify-end gap-2 border-t border-neutral-200 dark:border-neutral-900 pt-5 mt-6">
          <Button type="button" variant="outline" @click="openAvanceModal = false" class="border-neutral-200 dark:border-neutral-800 hover:bg-neutral-100 dark:hover:bg-white/5 text-neutral-700 dark:text-neutral-300 w-full sm:w-auto">
            Cancelar
          </Button>
          <Button type="submit" class="bg-primary text-primary-foreground hover:bg-primary/95 font-semibold w-full sm:w-auto">
            Enviar Reporte
          </Button>
        </div>
      </form>
    </Dialog>
  </div>
</template>

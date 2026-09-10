<script setup>
import { ref, computed, onMounted } from 'vue';
import client from '@/api/client';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
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
import {
  IconPlus,
  IconBuildingBroadcastTower,
  IconMapPin,
  IconUsersGroup,
  IconPencil,
  IconX,
  IconFileCheck,
  IconCheck
} from '@tabler/icons-vue';
import { selectSitios } from '@/api/sitios';
import OtAuditModal from '@/components/admin/OtAuditModal.vue';

const openCreateModal = ref(false);
const openEditModal = ref(false);
const openAuditModal = ref(false);
const auditingOt = ref(null);

const openAuditOt = (ot) => {
  auditingOt.value = ot;
  openAuditModal.value = true;
};

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
  sitio_id: null,
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
  sitio_id: null,
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

// Autocompletado de Sitios
const sitioSuggestions = ref([]);
const showSitioSuggestions = ref(false);
const activeInputTarget = ref('create');
let sitioDebounce = null;

const onSitioInput = (query, target = 'create') => {
  activeInputTarget.value = target;
  clearTimeout(sitioDebounce);
  if (!query || query.trim().length < 2) {
    sitioSuggestions.value = [];
    showSitioSuggestions.value = false;
    return;
  }
  sitioDebounce = setTimeout(async () => {
    try {
      sitioSuggestions.value = await selectSitios(query.trim(), 12);
      showSitioSuggestions.value = sitioSuggestions.value.length > 0;
    } catch (e) {
      console.error('Error buscando sitios para autocompletar:', e);
    }
  }, 250);
};

const chooseSitio = (sitio, target = 'create') => {
  const model = target === 'create' ? newOt.value : editingOt.value;
  model.sitio = sitio.nombre;
  model.sitio_id = sitio.id;
  if (sitio.ubicacion) {
    model.ubicacion = sitio.ubicacion;
  } else if (sitio.municipio) {
    model.ubicacion = `${sitio.municipio}${sitio.ciudad_base ? ' - Base ' + sitio.ciudad_base : ''}`;
  }
  if (sitio.transporte_especial) {
    model.tipo_ubicacion = 'rural';
  }
  showSitioSuggestions.value = false;
};

// Abrir modal de edición con datos precargados
const openEditOt = (ot) => {
  editingOt.value = {
    id: ot.id,
    codigo: ot.codigo,
    descripcion: ot.descripcion,
    sitio: ot.sitio || '',
    sitio_id: ot.sitio_id || null,
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

const estadoBadgeClass = (st) => {
  switch (st) {
    case 'finalizada':
    case 'finalizado':
      return 'bg-emerald-50 text-emerald-700 border border-emerald-300 dark:bg-emerald-950/60 dark:text-emerald-300 dark:border-emerald-800/80';
    case 'solucionada':
      return 'bg-blue-50 text-blue-700 border border-blue-300 dark:bg-blue-950/60 dark:text-blue-300 dark:border-blue-800/80';
    case 'en_progreso':
      return 'bg-indigo-50 text-indigo-700 border border-indigo-300 dark:bg-indigo-950/60 dark:text-indigo-300 dark:border-indigo-800/80';
    case 'en_sitio':
      return 'bg-cyan-50 text-cyan-700 border border-cyan-300 dark:bg-cyan-950/60 dark:text-cyan-300 dark:border-cyan-800/80';
    case 'en_camino':
      return 'bg-amber-50 text-amber-700 border border-amber-300 dark:bg-amber-950/60 dark:text-amber-300 dark:border-amber-800/80';
    case 'detenida_materiales':
      return 'bg-rose-50 text-rose-700 border border-rose-300 dark:bg-rose-950/60 dark:text-rose-300 dark:border-rose-800/80';
    case 'asignada':
    case 'pendiente':
    default:
      return 'bg-slate-100 text-slate-700 border border-slate-300 dark:bg-slate-900/60 dark:text-slate-300 dark:border-slate-700/80';
  }
};

const getStatusLabel = (status) => {
  switch (status) {
    case 'asignada':
    case 'pendiente': return 'Asignada';
    case 'en_camino': return 'En Camino';
    case 'en_sitio': return 'En Sitio';
    case 'en_progreso': return 'En Progreso';
    case 'detenida_materiales': return 'Detenida Materiales';
    case 'solucionada': return 'Solucionada';
    case 'finalizada':
    case 'finalizado': return 'Finalizada';
    default: return status;
  }
};
</script>

<template>
  <div class="flex flex-col gap-6 select-none">
    <!-- Encabezado de la Sección -->
    <div class="flex flex-col gap-4 sm:flex-row sm:justify-between sm:items-center bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 p-4 md:p-6 rounded-xl relative overflow-hidden shadow-sm transition-colors duration-300">
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
        <IconPlus class="w-4 h-4 stroke-[2]" /> Nueva OT
      </Button>
    </div>

    <!-- Panel de Registro de Órdenes -->
    <Card class="bg-white dark:bg-[#121215] border-neutral-200 dark:border-white/10 p-4 md:p-6 flex flex-col gap-4 shadow-sm transition-colors duration-300">
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
            class="w-full lg:w-72 bg-white dark:bg-[#0a0b10] border-neutral-200 dark:border-white/10 text-neutral-800 dark:text-white text-xs placeholder:text-neutral-450 focus-visible:ring-primary focus-visible:border-primary"
          />
          <select 
            v-model="statusFilter" 
            class="flex h-9 w-full sm:w-48 rounded-md border border-neutral-200 dark:border-white/10 bg-white dark:bg-[#0a0b10] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring focus:border-primary focus:ring-primary cursor-pointer"
          >
            <option value="todos">Todos los Estados</option>
            <option value="asignada">Asignadas</option>
            <option value="en_camino">En Camino</option>
            <option value="en_sitio">En Sitio</option>
            <option value="en_progreso">En Progreso</option>
            <option value="detenida_materiales">Detenidas por Materiales</option>
            <option value="solucionada">Solucionadas (Por Aprobar)</option>
            <option value="finalizada">Finalizadas / Liquidadas</option>
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
                    <span v-if="ot.sitio" class="font-bold text-neutral-900 dark:text-white text-xs line-clamp-1 flex items-center gap-1">
                      <IconBuildingBroadcastTower class="w-3.5 h-3.5 text-primary shrink-0 stroke-[1.75]" />
                      <span>{{ ot.sitio }}</span>
                    </span>
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
                <TableCell class="text-neutral-700 dark:text-neutral-350 py-4 whitespace-nowrap text-xs">
                  <span class="inline-flex items-center gap-1">
                    <IconMapPin class="w-3.5 h-3.5 text-rose-500 shrink-0 stroke-[1.75]" />
                    <span>{{ ot.ubicacion }}</span>
                  </span>
                </TableCell>
                <TableCell class="text-neutral-700 dark:text-neutral-350 py-4 whitespace-nowrap text-xs font-medium">
                  <div>{{ ot.assigned_user ? ot.assigned_user.name : 'No Asignado' }}</div>
                  <span v-if="ot.cuadrilla" class="flex items-center gap-1 text-[10px] text-neutral-400 font-normal">
                    <IconUsersGroup class="w-3 h-3 text-neutral-400 shrink-0 stroke-[1.75]" />
                    <span>{{ ot.cuadrilla.nombre }}</span>
                  </span>
                </TableCell>
                <TableCell class="py-4">
                  <div class="flex items-center gap-2">
                    <Progress :model-value="ot.progreso" class="h-1.5 w-16 bg-neutral-100 dark:bg-white/5" />
                    <span class="text-xs font-semibold text-neutral-600 dark:text-neutral-400">{{ ot.progreso }}%</span>
                  </div>
                </TableCell>
                <TableCell class="text-center py-4">
                  <span 
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-wider select-none shadow-2xs"
                    :class="estadoBadgeClass(ot.estado)"
                  >
                    {{ getStatusLabel(ot.estado) }}
                  </span>
                </TableCell>
                <TableCell class="text-right pr-4 py-4">
                  <div class="inline-flex gap-1.5 items-center justify-end">
                    <!-- Botón de Auditoría del Expediente Técnico -->
                    <Button 
                      @click="openAuditOt(ot)"
                      variant="default" 
                      size="sm" 
                      class="h-8 bg-emerald-600 hover:bg-emerald-500 text-white font-black text-xs px-3 flex items-center gap-1.5 shadow-xs active:scale-95 transition-all cursor-pointer" 
                      title="Auditar Fotografías, Bitácora y Liquidación de Insumos"
                    >
                      <IconFileCheck class="w-4 h-4 stroke-[2]" />
                      <span>Auditar</span>
                    </Button>

                    <!-- Botón de Edición Administrativa -->
                    <Button 
                      v-if="userRole === 'admin' || userRole === 'administrativo'"
                      @click="openEditOt(ot)"
                      variant="outline" 
                      size="sm" 
                      class="h-8 border-neutral-200 dark:border-white/10 hover:border-neutral-300 dark:hover:border-white/20 text-neutral-700 dark:text-neutral-300 font-bold text-xs px-2.5 flex items-center gap-1 active:scale-95 transition-all cursor-pointer" 
                      title="Editar datos generales de la OT"
                    >
                      <IconPencil class="w-3.5 h-3.5 stroke-[1.75]" />
                      <span>Editar</span>
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
        <button @click="openCreateModal = false" class="text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white p-1 rounded-lg hover:bg-neutral-100 dark:hover:bg-white/5 transition-colors">
          <IconX class="w-5 h-5 stroke-[2]" />
        </button>
      </div>

      <form @submit.prevent="createOt" class="space-y-4">
        <!-- Fila 1: Código OT & Sitio / Estación Base -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Código OT *</label>
            <Input type="text" v-model="newOt.codigo" required placeholder="OT-2026-004" class="bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-850 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
          </div>
          <div class="space-y-1.5 relative">
            <div class="flex items-center justify-between">
              <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Sitio / Estación Base (EB)</label>
              <span v-if="newOt.sitio_id" class="text-[9px] text-emerald-500 font-bold flex items-center gap-0.5">
                <IconCheck class="w-3 h-3" /> Vinculado a Sitio Maestro
              </span>
            </div>
            <div class="relative">
              <Input 
                type="text" 
                v-model="newOt.sitio" 
                @input="onSitioInput(newOt.sitio, 'create')"
                @focus="onSitioInput(newOt.sitio, 'create')"
                placeholder="Escriba para buscar en 1,819 sitios..." 
                class="bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-850 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary uppercase text-xs" 
              />
              <!-- Desplegable reactivo de sugerencias de sitios -->
              <div 
                v-if="showSitioSuggestions && activeInputTarget === 'create' && sitioSuggestions.length > 0"
                class="absolute left-0 right-0 top-full mt-1 bg-white dark:bg-[#18181b] border border-neutral-200 dark:border-neutral-700 rounded-xl shadow-xl z-50 max-h-48 overflow-y-auto divide-y divide-neutral-100 dark:divide-neutral-800"
              >
                <div 
                  v-for="s in sitioSuggestions" 
                  :key="s.id"
                  @click="chooseSitio(s, 'create')"
                  class="p-2.5 hover:bg-neutral-50 dark:hover:bg-neutral-800/60 cursor-pointer transition-colors text-left flex items-start justify-between gap-2"
                >
                  <div class="min-w-0">
                    <span class="font-bold text-xs text-neutral-900 dark:text-white block truncate">{{ s.nombre }}</span>
                    <span class="text-[10px] text-neutral-500 block truncate">
                      {{ s.municipio || s.ciudad_base || 'Sin municipio' }} • {{ s.zona_tecnica || s.zona || '' }}
                    </span>
                  </div>
                  <span v-if="s.transporte_especial" class="text-[9px] font-bold text-purple-600 bg-purple-500/10 px-1.5 py-0.5 rounded shrink-0">
                    {{ s.transporte_especial }}
                  </span>
                </div>
              </div>
            </div>
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
                {{ c.nombre }}
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
        <button @click="openEditModal = false" class="text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white p-1 rounded-lg hover:bg-neutral-100 dark:hover:bg-white/5 transition-colors">
          <IconX class="w-5 h-5 stroke-[2]" />
        </button>
      </div>

      <form @submit.prevent="updateOt" class="space-y-4">
        <!-- Fila 1: Código OT & Sitio / Estación Base -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Código OT *</label>
            <Input type="text" v-model="editingOt.codigo" required class="bg-white dark:bg-[#0a0b10] border-neutral-200 dark:border-white/10 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
          </div>
          <div class="space-y-1.5 relative">
            <div class="flex items-center justify-between">
              <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Sitio / Estación Base (EB)</label>
              <span v-if="editingOt.sitio_id" class="text-[9px] text-emerald-500 font-bold flex items-center gap-0.5">
                <IconCheck class="w-3 h-3" /> Vinculado a Sitio Maestro
              </span>
            </div>
            <div class="relative">
              <Input 
                type="text" 
                v-model="editingOt.sitio" 
                @input="onSitioInput(editingOt.sitio, 'edit')"
                @focus="onSitioInput(editingOt.sitio, 'edit')"
                placeholder="Escriba para buscar en 1,819 sitios..." 
                class="bg-white dark:bg-[#0a0b10] border-neutral-200 dark:border-white/10 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary uppercase text-xs" 
              />
              <!-- Desplegable reactivo de sugerencias de sitios -->
              <div 
                v-if="showSitioSuggestions && activeInputTarget === 'edit' && sitioSuggestions.length > 0"
                class="absolute left-0 right-0 top-full mt-1 bg-white dark:bg-[#18181b] border border-neutral-200 dark:border-neutral-700 rounded-xl shadow-xl z-50 max-h-48 overflow-y-auto divide-y divide-neutral-100 dark:divide-neutral-800"
              >
                <div 
                  v-for="s in sitioSuggestions" 
                  :key="s.id"
                  @click="chooseSitio(s, 'edit')"
                  class="p-2.5 hover:bg-neutral-50 dark:hover:bg-neutral-800/60 cursor-pointer transition-colors text-left flex items-start justify-between gap-2"
                >
                  <div class="min-w-0">
                    <span class="font-bold text-xs text-neutral-900 dark:text-white block truncate">{{ s.nombre }}</span>
                    <span class="text-[10px] text-neutral-500 block truncate">
                      {{ s.municipio || s.ciudad_base || 'Sin municipio' }} • {{ s.zona_tecnica || s.zona || '' }}
                    </span>
                  </div>
                  <span v-if="s.transporte_especial" class="text-[9px] font-bold text-purple-600 bg-purple-500/10 px-1.5 py-0.5 rounded shrink-0">
                    {{ s.transporte_especial }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Fila 2: Descripción de la Obra -->
        <div class="space-y-1.5">
          <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Descripción de la Obra / Falla *</label>
          <Input type="text" v-model="editingOt.descripcion" required class="bg-white dark:bg-[#0a0b10] border-neutral-200 dark:border-white/10 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
        </div>

        <!-- Fila 3: Tipo de Mantenimiento, Prioridad & Ubicación -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Tipo Mantenimiento *</label>
            <select 
              v-model="editingOt.tipo_mantenimiento" 
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-white/10 bg-white dark:bg-[#0a0b10] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
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
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-white/10 bg-white dark:bg-[#0a0b10] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
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
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-white/10 bg-white dark:bg-[#0a0b10] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
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
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-white/10 bg-white dark:bg-[#0a0b10] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
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
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-white/10 bg-white dark:bg-[#0a0b10] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
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
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-white/10 bg-white dark:bg-[#0a0b10] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
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
          <Input type="text" v-model="editingOt.ubicacion" required class="bg-white dark:bg-[#0a0b10] border-neutral-200 dark:border-white/10 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Operador Asignado *</label>
            <select 
              v-model="editingOt.user_id" 
              @change="onOperatorChange(editingOt.user_id, 'edit')"
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-white/10 bg-white dark:bg-[#0a0b10] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
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
                {{ c.nombre }}
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

    <!-- Modal 2: Auditoría y Expediente Técnico de la OT (Fotos GPS, Bitácora, LPU) -->
    <OtAuditModal
      :is-open="openAuditModal"
      :ot="auditingOt"
      @close="openAuditModal = false"
      @updated="loadOts"
    />
  </div>
</template>

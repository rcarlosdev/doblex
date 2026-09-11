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
  IconCheck,
  IconTool,
  IconEngine,
  IconWind,
  IconCalendar
} from '@tabler/icons-vue';
import { selectSitios } from '@/api/sitios';
import OtAuditModal from '@/components/admin/OtAuditModal.vue';
import EmpleadoMultiSelect from '@/components/common/EmpleadoMultiSelect.vue';

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

// Lista reactiva de operadores asignados (Multi-técnico)
const newOtOperadores = ref([]);
const editingOtOperadores = ref([]);
const newDateInputRef = ref(null);
const editDateInputRef = ref(null);

const triggerDateInput = (target = 'create') => {
  const el = target === 'create' ? newDateInputRef.value : editDateInputRef.value;
  if (el && typeof el.showPicker === 'function') {
    el.showPicker();
  } else if (el) {
    el.focus();
  }
};

const getNowDate = () => {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
};

const formatToDate = (str) => {
  if (!str) return getNowDate();
  if (str.includes('T')) return str.slice(0, 10);
  if (str.includes(' ')) return str.split(' ')[0];
  return str.slice(0, 10);
};

// Generador de ID de actividad independiente
const generateActivityId = () => {
  const year = new Date().getFullYear();
  const rnd = Math.floor(100000 + Math.random() * 900000);
  return `ACT-${year}-${rnd}`;
};

// Datos para registrar nueva OT (Administración - Asignación y Logística)
const newOt = ref({
  codigo: '',
  id_actividad: generateActivityId(),
  tipo_actividad: 'correctivo',
  descripcion: '',
  sitio: '',
  sitio_id: null,
  ubicacion: '',
  departamento: 'Antioquia',
  regional: 'R1',
  categoria: 'normal',
  tipo_estacion: 'MOVIL',
  site_owner: '', // Se llena automáticamente de New_SO al seleccionar el sitio
  coordinador: '',
  user_id: '', // Operador por persona principal
  prioridad: 'P2',
  tipo_ubicacion: 'urbana',
  tipo_mantenimiento: 'correctivo',
  subsistema: 'Movil Sistema Eléctrico',
  fecha_inicio: getNowDate()
});

// Datos para editar OT (Administración)
const editingOt = ref({
  id: null,
  codigo: '',
  id_actividad: '',
  tipo_actividad: 'correctivo',
  descripcion: '',
  sitio: '',
  sitio_id: null,
  ubicacion: '',
  departamento: '',
  regional: 'R1',
  categoria: 'normal',
  tipo_estacion: 'MOVIL',
  site_owner: '',
  coordinador: '',
  user_id: '',
  prioridad: 'P2',
  tipo_ubicacion: 'urbana',
  tipo_mantenimiento: 'correctivo',
  subsistema: 'Movil Sistema Eléctrico',
  estado: 'asignada',
  fecha_inicio: getNowDate()
});

const syncOtModel = (model) => {
  if (model.tipo_actividad === 'preventivo_planta') {
    model.tipo_mantenimiento = 'preventivo';
    if (!model.subsistema || model.subsistema === 'Movil Sistema Eléctrico') {
      model.subsistema = 'Movil Plantas Eléctricas';
    }
  } else if (model.tipo_actividad === 'preventivo_aire') {
    model.tipo_mantenimiento = 'preventivo';
    if (!model.subsistema || model.subsistema === 'Movil Sistema Eléctrico') {
      model.subsistema = 'Movil Aires Acondicionados';
    }
  } else if (model.tipo_actividad === 'correctivo') {
    model.tipo_mantenimiento = 'correctivo';
  } else if (model.tipo_actividad === 'emergencia') {
    model.tipo_mantenimiento = 'emergencia';
  }

  if (model.categoria === 'rural') {
    model.tipo_ubicacion = 'rural';
  } else {
    model.tipo_ubicacion = 'urbana';
  }
};

// Manejo de Tipo de Actividad (Correctivo, Preventivo, Emergencia) y Planta/Aire
const newOtTipoPrincipal = ref('correctivo');
const newOtSubtipoPreventivo = ref('planta');
const editingOtTipoPrincipal = ref('correctivo');
const editingOtSubtipoPreventivo = ref('planta');

const openCreateOtModal = () => {
  newOtTipoPrincipal.value = 'correctivo';
  newOtSubtipoPreventivo.value = 'planta';
  newOt.value.tipo_actividad = 'correctivo';
  openCreateModal.value = true;
};

const onNewOtTipoPrincipalChange = () => {
  if (newOtTipoPrincipal.value === 'preventivo') {
    newOt.value.tipo_actividad = newOtSubtipoPreventivo.value === 'aire' ? 'preventivo_aire' : 'preventivo_planta';
  } else {
    newOt.value.tipo_actividad = newOtTipoPrincipal.value;
  }
  onTipoActividadChange('create');
};

const onNewOtSubtipoChange = () => {
  if (newOtTipoPrincipal.value === 'preventivo') {
    newOt.value.tipo_actividad = newOtSubtipoPreventivo.value === 'aire' ? 'preventivo_aire' : 'preventivo_planta';
    onTipoActividadChange('create');
  }
};

const onEditingOtTipoPrincipalChange = () => {
  if (editingOtTipoPrincipal.value === 'preventivo') {
    editingOt.value.tipo_actividad = editingOtSubtipoPreventivo.value === 'aire' ? 'preventivo_aire' : 'preventivo_planta';
  } else {
    editingOt.value.tipo_actividad = editingOtTipoPrincipal.value;
  }
  onTipoActividadChange('edit');
};

const onEditingOtSubtipoChange = () => {
  if (editingOtTipoPrincipal.value === 'preventivo') {
    editingOt.value.tipo_actividad = editingOtSubtipoPreventivo.value === 'aire' ? 'preventivo_aire' : 'preventivo_planta';
    onTipoActividadChange('edit');
  }
};

const onTipoActividadChange = (target = 'create') => {
  const model = target === 'create' ? newOt.value : editingOt.value;
  syncOtModel(model);
};

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
  if (sitio.departamento) {
    model.departamento = sitio.departamento;
  }
  if (sitio.regional) {
    model.regional = (sitio.regional.toUpperCase().includes('2') || sitio.regional.toUpperCase().includes('R2')) ? 'R2' : 'R1';
  }
  if (sitio.tipo_estacion) {
    model.tipo_estacion = sitio.tipo_estacion;
  }

  // Site Owner: Se toma específicamente de la columna New_SO (supervisor_operativo) de la base de datos de sitios
  model.site_owner = sitio.supervisor_operativo || sitio.new_so || sitio.site_owner || '';

  if (sitio.transporte_especial || sitio.categoria === 'rural') {
    model.categoria = 'rural';
    model.tipo_ubicacion = 'rural';
  } else {
    model.categoria = 'normal';
    model.tipo_ubicacion = 'urbana';
  }
  showSitioSuggestions.value = false;
};

// Abrir modal de edición con datos generales
const openEditOt = (ot) => {
  // Sincronizar lista de operadores (Multi-técnico)
  if (Array.isArray(ot.operadores_asignados) && ot.operadores_asignados.length > 0) {
    editingOtOperadores.value = [...ot.operadores_asignados];
  } else if (ot.assigned_user) {
    editingOtOperadores.value = [{
      id: ot.assigned_user.id,
      user_id: ot.assigned_user.id,
      name: ot.assigned_user.name,
      nombre: ot.assigned_user.name,
      username: ot.assigned_user.username
    }];
  } else {
    editingOtOperadores.value = [];
  }

  // Parsear Tipo de Actividad y Subtipo (Planta/Aire)
  const tAct = ot.tipo_actividad || ot.tipo_mantenimiento || 'correctivo';
  if (tAct === 'preventivo_aire' || (tAct === 'preventivo' && (ot.subsistema || '').toLowerCase().includes('aire'))) {
    editingOtTipoPrincipal.value = 'preventivo';
    editingOtSubtipoPreventivo.value = 'aire';
  } else if (tAct === 'preventivo_planta' || tAct === 'preventivo') {
    editingOtTipoPrincipal.value = 'preventivo';
    editingOtSubtipoPreventivo.value = 'planta';
  } else if (tAct === 'emergencia') {
    editingOtTipoPrincipal.value = 'emergencia';
    editingOtSubtipoPreventivo.value = 'planta';
  } else {
    editingOtTipoPrincipal.value = 'correctivo';
    editingOtSubtipoPreventivo.value = 'planta';
  }

  editingOt.value = {
    id: ot.id,
    codigo: ot.codigo,
    id_actividad: ot.id_actividad || generateActivityId(),
    tipo_actividad: ot.tipo_actividad || ot.tipo_mantenimiento || 'correctivo',
    descripcion: ot.descripcion,
    sitio: ot.sitio || '',
    sitio_id: ot.sitio_id || null,
    ubicacion: ot.ubicacion,
    departamento: ot.departamento || '',
    regional: ot.regional || 'R1',
    categoria: ot.categoria || (ot.tipo_ubicacion === 'rural' ? 'rural' : 'normal'),
    tipo_estacion: ot.tipo_estacion || 'MOVIL',
    site_owner: ot.site_owner || 'CLARO',
    coordinador: ot.coordinador || '',
    user_id: ot.user_id || (ot.assigned_user ? ot.assigned_user.id : ''),
    prioridad: ot.prioridad || 'P2',
    tipo_ubicacion: ot.tipo_ubicacion || 'urbana',
    tipo_mantenimiento: ot.tipo_mantenimiento || 'correctivo',
    subsistema: ot.subsistema || 'Movil Sistema Eléctrico',
    estado: ot.estado || 'asignada',
    fecha_inicio: formatToDate(ot.fecha_inicio)
  };
  openEditModal.value = true;
};

const updateOt = async () => {
  errorMsg.value = '';
  if (editingOtOperadores.value.length === 0) {
    errorMsg.value = 'Debes asignar al menos un técnico responsable.';
    return;
  }
  try {
    const payload = { ...editingOt.value };
    syncOtModel(payload);

    // Operador líder y lista de operadores acompañantes
    const leadOp = editingOtOperadores.value[0];
    payload.user_id = leadOp.user_id || leadOp.id;
    payload.operadores_asignados = editingOtOperadores.value;
    payload.operadores_ids = editingOtOperadores.value.map(o => o.user_id || o.id);

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
    
    // Búsqueda por código, ID de actividad, descripción, ubicación, coordinador o por el nombre del encargado
    const matchesSearch = (ot.codigo && ot.codigo.toLowerCase().includes(searchLower)) || 
                         (ot.id_actividad && ot.id_actividad.toLowerCase().includes(searchLower)) ||
                         (ot.descripcion && ot.descripcion.toLowerCase().includes(searchLower)) ||
                         (ot.ubicacion && ot.ubicacion.toLowerCase().includes(searchLower)) ||
                         (ot.coordinador && ot.coordinador.toLowerCase().includes(searchLower)) ||
                         (ot.departamento && ot.departamento.toLowerCase().includes(searchLower)) ||
                         (ot.assigned_user && ot.assigned_user.name.toLowerCase().includes(searchLower)) ||
                         (ot.cuadrilla && ot.cuadrilla.nombre.toLowerCase().includes(searchLower));
    
    const matchesStatus = statusFilter.value === 'todos' || ot.estado === statusFilter.value;

    return matchesSearch && matchesStatus;
  });
});

const createOt = async () => {
  errorMsg.value = '';
  if (newOtOperadores.value.length === 0) {
    errorMsg.value = 'Debes asignar al menos un técnico responsable a la Orden de Trabajo.';
    return;
  }
  try {
    const payload = { ...newOt.value };
    syncOtModel(payload);

    // Operador líder asignado como user_id y lista completa de operadores
    const leadOp = newOtOperadores.value[0];
    payload.user_id = leadOp.user_id || leadOp.id;
    payload.operadores_asignados = newOtOperadores.value;
    payload.operadores_ids = newOtOperadores.value.map(o => o.user_id || o.id);
    payload.datos_formulario = {
      operadores_asignados: newOtOperadores.value
    };

    const response = await client.post('/ots', payload);
    if (response.data.status === 'success') {
      // Recargar OTs y cerrar modal
      await loadOts();
      openCreateModal.value = false;
      newOtOperadores.value = [];
      newOtTipoPrincipal.value = 'correctivo';
      newOtSubtipoPreventivo.value = 'planta';
      
      // Limpiar formulario con nuevo ID de actividad generado
      newOt.value = {
        codigo: '',
        id_actividad: generateActivityId(),
        tipo_actividad: 'correctivo',
        descripcion: '',
        sitio: '',
        sitio_id: null,
        ubicacion: '',
        departamento: 'Antioquia',
        regional: 'R1',
        categoria: 'normal',
        tipo_estacion: 'MOVIL',
        site_owner: '',
        coordinador: '',
        user_id: '',
        prioridad: 'P2',
        tipo_ubicacion: 'urbana',
        tipo_mantenimiento: 'correctivo',
        subsistema: 'Movil Sistema Eléctrico',
        fecha_inicio: getNowDate()
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
        @click="openCreateOtModal" 
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
            placeholder="Buscar por código, descripción o técnico..." 
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
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase pl-4">Código / ID Actividad</TableHead>
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase">Sitio & Estación</TableHead>
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase">Tipo & Clasificación</TableHead>
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase">Coordinador & Técnico</TableHead>
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase">Ubicación / Dpto</TableHead>
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase w-[120px]">Progreso</TableHead>
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase text-center">Estado</TableHead>
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase text-right pr-4">Acciones</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow v-for="ot in filteredOts" :key="ot.id" class="border-neutral-100 dark:border-neutral-900 hover:bg-neutral-50 dark:hover:bg-white/[0.02]">
                <TableCell class="pl-4 py-4">
                  <div class="flex flex-col gap-1">
                    <span class="font-mono font-bold text-primary text-xs">{{ ot.codigo }}</span>
                    <span v-if="ot.id_actividad" class="font-mono text-[10px] text-neutral-500 bg-neutral-100 dark:bg-neutral-900 px-1.5 py-0.5 rounded border border-neutral-200 dark:border-neutral-800 w-fit">
                      {{ ot.id_actividad }}
                    </span>
                    <SlaBadge v-if="ot.fecha_limite_sla" :fecha-limite="ot.fecha_limite_sla" :estado="ot.estado" />
                  </div>
                </TableCell>
                <TableCell class="py-4">
                  <div class="flex flex-col max-w-xs">
                    <span v-if="ot.sitio" class="font-bold text-neutral-900 dark:text-white text-xs line-clamp-1 flex items-center gap-1">
                      <IconBuildingBroadcastTower class="w-3.5 h-3.5 text-primary shrink-0 stroke-[1.75]" />
                      <span>{{ ot.sitio }}</span>
                    </span>
                    <div class="flex items-center gap-1.5 text-[10px] text-neutral-500 mt-0.5">
                      <span class="font-bold text-neutral-700 dark:text-neutral-300">{{ ot.tipo_estacion || 'MOVIL' }}</span>
                      <span>•</span>
                      <span>Owner: {{ ot.site_owner || 'CLARO' }}</span>
                    </div>
                    <span class="text-xs text-neutral-600 dark:text-neutral-300 line-clamp-1 mt-0.5">{{ ot.descripcion }}</span>
                    <span class="text-[10px] text-neutral-400 mt-0.5">Inicio: {{ ot.fecha_inicio }}</span>
                  </div>
                </TableCell>
                <TableCell class="py-4 whitespace-nowrap">
                  <div class="flex flex-col gap-1 items-start">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase shadow-sm" :class="{
                      'bg-rose-100 text-rose-800 border border-rose-200 dark:bg-rose-950/60 dark:text-rose-400 dark:border-rose-500/30': ot.tipo_actividad === 'emergencia' || ot.tipo_mantenimiento === 'emergencia',
                      'bg-amber-100 text-amber-800 border border-amber-200 dark:bg-amber-950/60 dark:text-amber-400 dark:border-amber-500/30': ot.tipo_actividad === 'correctivo' || ot.tipo_mantenimiento === 'correctivo',
                      'bg-emerald-100 text-emerald-800 border border-emerald-200 dark:bg-emerald-950/60 dark:text-emerald-400 dark:border-emerald-500/30': ot.tipo_actividad === 'preventivo_planta',
                      'bg-cyan-100 text-cyan-800 border border-cyan-200 dark:bg-cyan-950/60 dark:text-cyan-400 dark:border-cyan-500/30': ot.tipo_actividad === 'preventivo_aire',
                      'bg-blue-100 text-blue-800 border border-blue-200 dark:bg-blue-950/60 dark:text-blue-400 dark:border-blue-500/30': !ot.tipo_actividad || ot.tipo_mantenimiento === 'preventivo'
                    }">
                      {{ ot.tipo_actividad === 'preventivo_planta' ? 'Preventivo - PLANTA' : ot.tipo_actividad === 'preventivo_aire' ? 'Preventivo - AIRE' : (ot.tipo_actividad || ot.tipo_mantenimiento || 'Correctivo').toUpperCase() }}
                    </span>
                    <div class="flex items-center gap-1 text-[10px] font-semibold text-neutral-600 dark:text-slate-400">
                      <span class="px-1.5 py-0.2 rounded bg-neutral-100 dark:bg-neutral-800 uppercase text-[9px]">{{ ot.categoria || 'normal' }}</span>
                      <span>{{ ot.regional || 'R1' }}</span>
                      <span>•</span>
                      <span>{{ ot.prioridad || 'P2' }}</span>
                    </div>
                    <div class="text-[9px] font-mono text-neutral-400 dark:text-neutral-500 truncate max-w-[150px]">
                      <span class="font-bold text-neutral-600 dark:text-neutral-300">
                        {{ (['correctivo', 'emergencia'].includes(ot.tipo_actividad || ot.tipo_mantenimiento)) ? 'Fmt WO' : 'Fmt MP' }}
                      </span>
                      <span v-if="ot.datos_formulario?.tipo_equipo_falla || ot.datos_formulario?.marca_equipo">
                        : {{ ot.datos_formulario?.tipo_equipo_falla || ot.datos_formulario?.marca_equipo }}
                      </span>
                    </div>
                  </div>
                </TableCell>
                <TableCell class="py-4 whitespace-nowrap text-xs">
                  <div class="flex flex-col gap-0.5">
                    <span class="text-neutral-500 text-[10px]">Coord: <strong class="text-neutral-800 dark:text-neutral-200 font-semibold">{{ ot.coordinador || 'Sin asignar' }}</strong></span>
                    <div class="flex items-center gap-1.5 flex-wrap">
                      <span class="font-medium text-neutral-900 dark:text-white">
                        Téc: {{ ot.assigned_user ? ot.assigned_user.name : 'No Asignado' }}
                      </span>
                      <span 
                        v-if="ot.operadores_asignados && ot.operadores_asignados.length > 1" 
                        class="text-[9px] bg-primary/10 text-primary font-black px-1.5 py-0.2 rounded border border-primary/20"
                        :title="ot.operadores_asignados.map(o => (o.nombre || o.name) + (o.cargo ? ' (' + o.cargo + ')' : '')).join('\n')"
                      >
                        +{{ ot.operadores_asignados.length - 1 }} apoyo(s)
                      </span>
                    </div>
                  </div>
                </TableCell>
                <TableCell class="text-neutral-700 dark:text-neutral-350 py-4 whitespace-nowrap text-xs">
                  <div class="flex flex-col gap-0.5">
                    <span class="inline-flex items-center gap-1">
                      <IconMapPin class="w-3.5 h-3.5 text-rose-500 shrink-0 stroke-[1.75]" />
                      <span class="font-medium">{{ ot.ubicacion }}</span>
                    </span>
                    <span v-if="ot.departamento" class="text-[10px] text-neutral-400 pl-4.5">
                      Dpto: {{ ot.departamento }}
                    </span>
                  </div>
                </TableCell>
                <TableCell class="py-4">
                  <div class="flex items-center gap-2">
                    <Progress :model-value="ot.progreso" class="h-1.5 w-14 bg-neutral-100 dark:bg-white/5" />
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
                <TableCell colspan="8" class="text-center text-neutral-500 py-10">
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
      <div class="flex items-center justify-between border-b border-neutral-200 dark:border-neutral-800 pb-3 mb-3 shrink-0">
        <div class="min-w-0 pr-2">
          <div class="flex items-center gap-2 flex-wrap">
            <h3 class="text-sm sm:text-base font-bold text-neutral-900 dark:text-white">Crear Nueva Orden de Trabajo</h3>
            <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[11px] font-mono font-bold bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20" title="ID de Actividad Independiente - Control Interno">
              <span class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></span>
              {{ newOt.id_actividad }}
            </span>
          </div>
          <p class="text-[10px] sm:text-[11px] text-neutral-500 mt-0.5 truncate">Completa los campos técnicos para la asignación y diligenciamiento en campo</p>
        </div>
        <button @click="openCreateModal = false" class="text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white p-1.5 rounded-lg hover:bg-neutral-100 dark:hover:bg-white/5 transition-colors shrink-0">
          <IconX class="w-5 h-5 stroke-[2]" />
        </button>
      </div>

      <form @submit.prevent="createOt" class="flex flex-col flex-1 min-h-0 overflow-hidden">
        <div class="space-y-3 sm:space-y-3.5 overflow-y-auto pr-1 sm:pr-2 flex-1 custom-scrollbar">
          <!-- Fila 1: Código OT & Tipo Actividad -->
        <div class="grid grid-cols-1 gap-3" :class="newOtTipoPrincipal === 'preventivo' ? 'sm:grid-cols-3' : 'sm:grid-cols-2'">
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Código OT *</label>
            <Input type="text" v-model="newOt.codigo" required placeholder="WO0000005558781 o OT5304019" class="bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-850 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary uppercase" />
          </div>
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Tipo Actividad *</label>
            <select 
              v-model="newOtTipoPrincipal" 
              @change="onNewOtTipoPrincipalChange"
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-950 px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer font-medium"
            >
              <option value="correctivo">Correctivo</option>
              <option value="preventivo">Preventivo</option>
              <option value="emergencia">Emergencia</option>
            </select>
          </div>
          <div v-if="newOtTipoPrincipal === 'preventivo'" class="space-y-1.5 animate-in fade-in slide-in-from-left-2 duration-200">
            <label class="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">Planta o Aire *</label>
            <select 
              v-model="newOtSubtipoPreventivo" 
              @change="onNewOtSubtipoChange"
              required
              class="flex h-9 w-full rounded-md border border-emerald-300 dark:border-emerald-700 bg-white dark:bg-neutral-950 px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer font-semibold"
            >
              <option value="planta">Planta</option>
              <option value="aire">Aire</option>
            </select>
          </div>
        </div>

        <!-- Fila 2: Sitio / Estación Base & Site Owner (New_SO del sitio autocompletado) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div class="space-y-1.5 relative">
            <div class="flex items-center justify-between">
              <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Sitio / Estación Base (EB) *</label>
              <span v-if="newOt.sitio_id" class="text-[9px] text-emerald-500 font-bold flex items-center gap-0.5">
                <IconCheck class="w-3 h-3" /> Vinculado a Maestro
              </span>
            </div>
            <div class="relative">
              <Input 
                type="text" 
                v-model="newOt.sitio" 
                @input="onSitioInput(newOt.sitio, 'create')"
                @focus="onSitioInput(newOt.sitio, 'create')"
                placeholder="Escriba para buscar sitio (ej. ANT.ACUARIO)..." 
                class="bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-850 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary uppercase text-xs" 
              />
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
                      {{ s.municipio || s.ciudad_base || 'Sin municipio' }} • {{ s.departamento || '' }} • {{ s.regional || '' }} <span v-if="s.supervisor_operativo || s.new_so">• SO: <strong class="text-neutral-700 dark:text-neutral-300">{{ s.supervisor_operativo || s.new_so }}</strong></span>
                    </span>
                  </div>
                  <span v-if="s.transporte_especial" class="text-[9px] font-bold text-purple-600 bg-purple-500/10 px-1.5 py-0.5 rounded shrink-0">
                    {{ s.transporte_especial }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div class="space-y-1.5">
            <div class="flex items-center justify-between">
              <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Site Owner (New_SO) *</label>
              <span class="text-[9px] font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60 px-1.5 py-0.2 rounded border border-emerald-200 dark:border-emerald-800">
                Auto de New_SO
              </span>
            </div>
            <Input 
              type="text" 
              v-model="newOt.site_owner" 
              required 
              placeholder="Se autocompleta con el sitio (ej. ALFONSO SUAREZ)" 
              class="bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-850 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary text-xs uppercase font-medium" 
            />
          </div>
        </div>

        <!-- Fila 3: Coordinador & Fecha Inicio -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 items-start">
          <div>
            <EmpleadoMultiSelect
              v-model="newOt.coordinador"
              :multiple="false"
              label="Coordinador"
              role-label="coordinador"
              placeholder="Buscar coordinador por cédula, nombre o cargo..."
              :required="true"
            />
          </div>

          <div class="space-y-1.5">
            <div class="flex items-center justify-between">
              <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Fecha Inicio *</label>
              <button 
                type="button" 
                @click="newOt.fecha_inicio = getNowDate()" 
                class="text-[10px] font-semibold text-primary hover:underline flex items-center gap-1"
              >
                Hoy
              </button>
            </div>
            <div class="relative flex items-center cursor-pointer" @click="triggerDateInput('create')">
              <div class="absolute left-3 text-neutral-400 pointer-events-none">
                <IconCalendar class="w-4 h-4" />
              </div>
              <input 
                ref="newDateInputRef"
                type="date" 
                v-model="newOt.fecha_inicio" 
                required 
                class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-850 bg-white dark:bg-neutral-950 pl-9 pr-3 py-1 text-xs text-neutral-800 dark:text-neutral-200 focus:border-primary focus:ring-primary font-medium cursor-pointer" 
              />
            </div>
          </div>
        </div>

        <!-- Fila 4: Técnico (Multi-técnico) -->
        <div>
          <EmpleadoMultiSelect
            v-model="newOtOperadores"
            label="Técnico"
            :required="true"
          />
        </div>

        <!-- Fila 5: Parámetros Técnicos (Categoría, Regional, Tipo Estación, Prioridad) -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Categoría *</label>
            <select 
              v-model="newOt.categoria" 
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-950 px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer font-medium"
            >
              <option value="normal">Normal</option>
              <option value="rural">Rural (Difícil Acceso)</option>
            </select>
          </div>
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Regional *</label>
            <select 
              v-model="newOt.regional" 
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-950 px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer font-medium"
            >
              <option value="R1">R1 (Regional 1)</option>
              <option value="R2">R2 (Regional 2)</option>
            </select>
          </div>
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Tipo Estación *</label>
            <select 
              v-model="newOt.tipo_estacion" 
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-950 px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
            >
              <option value="MOVIL">MOVIL</option>
              <option value="FIJA">FIJA</option>
              <option value="REPETIDORA">REPETIDORA</option>
              <option value="NODO">NODO</option>
              <option value="CENTRO_DE_DATOS">CENTRO DE DATOS</option>
            </select>
          </div>
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Prioridad *</label>
            <select 
              v-model="newOt.prioridad" 
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-950 px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
            >
              <option value="P1">P1 - Alta (Crítica)</option>
              <option value="P2">P2 - Media (Normal)</option>
              <option value="P3">P3 - Baja (Planificada)</option>
            </select>
          </div>
        </div>

        <!-- Fila 6: Departamento & Ubicación / Municipio -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Departamento *</label>
            <Input type="text" v-model="newOt.departamento" required placeholder="Antioquia, Chocó, etc." class="bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-850 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
          </div>
          <div class="sm:col-span-2 space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Ubicación / Municipio *</label>
            <Input type="text" v-model="newOt.ubicacion" required placeholder="Ej: Sitio El Veinte, Finca La Herradura, Apartadó" class="bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-850 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
          </div>
        </div>

        <!-- Fila 7: Descripción de la Obra / Falla -->
        <div class="space-y-1.5">
          <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Descripción de la Obra / Falla *</label>
          <Input type="text" v-model="newOt.descripcion" required placeholder="Ej: Reparación de tarjeta AVR y bobinado Selmec 40SC" class="bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-850 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
        </div>
        </div>

        <!-- Botones de Acción (Fijo al pie del modal) -->
        <div class="flex flex-col sm:flex-row justify-end gap-2 border-t border-neutral-200 dark:border-neutral-800 pt-3 mt-2 shrink-0">
          <Button type="button" variant="outline" @click="openCreateModal = false" class="border-neutral-200 dark:border-neutral-800 hover:bg-neutral-100 dark:hover:bg-white/5 text-neutral-700 dark:text-neutral-300 w-full sm:w-auto h-9 text-xs">
            Cancelar
          </Button>
          <Button type="submit" class="bg-primary text-primary-foreground hover:bg-primary/95 font-semibold w-full sm:w-auto h-9 text-xs">
            Registrar OT
          </Button>
        </div>
      </form>
    </Dialog>

    <!-- Modal de Editar OT (Administrador/Administrativo) -->
    <Dialog :open="openEditModal" @close="openEditModal = false">
      <div class="flex items-center justify-between border-b border-neutral-200 dark:border-neutral-800 pb-3 mb-3 shrink-0">
        <div class="min-w-0 pr-2">
          <div class="flex items-center gap-2 flex-wrap">
            <h3 class="text-sm sm:text-base font-bold text-neutral-900 dark:text-white">Editar Orden de Trabajo</h3>
            <span v-if="editingOt.id_actividad" class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[11px] font-mono font-bold bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20" title="ID de Actividad Independiente - Control Interno">
              <span class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></span>
              {{ editingOt.id_actividad }}
            </span>
          </div>
          <p class="text-[10px] sm:text-[11px] text-neutral-500 mt-0.5 truncate">Actualiza los datos técnicos y asignación de la OT {{ editingOt.codigo }}</p>
        </div>
        <button @click="openEditModal = false" class="text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white p-1.5 rounded-lg hover:bg-neutral-100 dark:hover:bg-white/5 transition-colors shrink-0">
          <IconX class="w-5 h-5 stroke-[2]" />
        </button>
      </div>

      <form @submit.prevent="updateOt" class="flex flex-col flex-1 min-h-0 overflow-hidden">
        <div class="space-y-3 sm:space-y-3.5 overflow-y-auto pr-1 sm:pr-2 flex-1 custom-scrollbar">
          <!-- Fila 1: Código OT & Tipo Actividad -->
        <div class="grid grid-cols-1 gap-3" :class="editingOtTipoPrincipal === 'preventivo' ? 'sm:grid-cols-3' : 'sm:grid-cols-2'">
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Código OT *</label>
            <Input type="text" v-model="editingOt.codigo" required class="bg-white dark:bg-[#0a0b10] border-neutral-200 dark:border-white/10 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary uppercase" />
          </div>
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Tipo Actividad *</label>
            <select 
              v-model="editingOtTipoPrincipal" 
              @change="onEditingOtTipoPrincipalChange"
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-white/10 bg-white dark:bg-[#0a0b10] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer font-medium"
            >
              <option value="correctivo">Correctivo</option>
              <option value="preventivo">Preventivo</option>
              <option value="emergencia">Emergencia</option>
            </select>
          </div>
          <div v-if="editingOtTipoPrincipal === 'preventivo'" class="space-y-1.5 animate-in fade-in slide-in-from-left-2 duration-200">
            <label class="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">Planta o Aire *</label>
            <select 
              v-model="editingOtSubtipoPreventivo" 
              @change="onEditingOtSubtipoChange"
              required
              class="flex h-9 w-full rounded-md border border-emerald-300 dark:border-emerald-700 bg-white dark:bg-[#0a0b10] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer font-semibold"
            >
              <option value="planta">Planta</option>
              <option value="aire">Aire</option>
            </select>
          </div>
        </div>

        <!-- Fila 2: Sitio / Estación Base & Site Owner (New_SO del sitio) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div class="space-y-1.5 relative">
            <div class="flex items-center justify-between">
              <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Sitio / Estación Base (EB)</label>
              <span v-if="editingOt.sitio_id" class="text-[9px] text-emerald-500 font-bold flex items-center gap-0.5">
                <IconCheck class="w-3 h-3" /> Vinculado a Maestro
              </span>
            </div>
            <div class="relative">
              <Input 
                type="text" 
                v-model="editingOt.sitio" 
                @input="onSitioInput(editingOt.sitio, 'edit')"
                @focus="onSitioInput(editingOt.sitio, 'edit')"
                placeholder="Escriba para buscar sitio (ej. ANT.ACUARIO)..." 
                class="bg-white dark:bg-[#0a0b10] border-neutral-200 dark:border-white/10 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary uppercase text-xs" 
              />
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
                      {{ s.municipio || s.ciudad_base || 'Sin municipio' }} • {{ s.departamento || '' }} • {{ s.regional || '' }} <span v-if="s.supervisor_operativo || s.new_so">• SO: <strong class="text-neutral-700 dark:text-neutral-300">{{ s.supervisor_operativo || s.new_so }}</strong></span>
                    </span>
                  </div>
                  <span v-if="s.transporte_especial" class="text-[9px] font-bold text-purple-600 bg-purple-500/10 px-1.5 py-0.5 rounded shrink-0">
                    {{ s.transporte_especial }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div class="space-y-1.5">
            <div class="flex items-center justify-between">
              <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Site Owner (New_SO) *</label>
              <span class="text-[9px] font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60 px-1.5 py-0.2 rounded border border-emerald-200 dark:border-emerald-800">
                Auto de New_SO
              </span>
            </div>
            <Input 
              type="text" 
              v-model="editingOt.site_owner" 
              required 
              placeholder="Ej: ALFONSO SUAREZ JOSE ELEAZAR" 
              class="bg-white dark:bg-[#0a0b10] border-neutral-200 dark:border-white/10 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary text-xs uppercase font-medium" 
            />
          </div>
        </div>

        <!-- Fila 3: Coordinador & Fecha Inicio -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 items-start">
          <div>
            <EmpleadoMultiSelect
              v-model="editingOt.coordinador"
              :multiple="false"
              label="Coordinador"
              role-label="coordinador"
              placeholder="Buscar coordinador por cédula, nombre o cargo..."
              :required="true"
            />
          </div>

          <div class="space-y-1.5">
            <div class="flex items-center justify-between">
              <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Fecha Inicio *</label>
              <button 
                type="button" 
                @click="editingOt.fecha_inicio = getNowDate()" 
                class="text-[10px] font-semibold text-primary hover:underline flex items-center gap-1"
              >
                Hoy
              </button>
            </div>
            <div class="relative flex items-center cursor-pointer" @click="triggerDateInput('edit')">
              <div class="absolute left-3 text-neutral-400 pointer-events-none">
                <IconCalendar class="w-4 h-4" />
              </div>
              <input 
                ref="editDateInputRef"
                type="date" 
                v-model="editingOt.fecha_inicio" 
                required 
                class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#0a0b10] pl-9 pr-3 py-1 text-xs text-neutral-800 dark:text-neutral-200 focus:border-primary focus:ring-primary font-medium cursor-pointer" 
              />
            </div>
          </div>
        </div>

        <!-- Fila 4: Técnico (Multi-técnico) -->
        <div>
          <EmpleadoMultiSelect
            v-model="editingOtOperadores"
            label="Técnico"
            :required="true"
          />
        </div>

        <!-- Fila 5: Parámetros Técnicos (Categoría, Regional, Tipo Estación, Prioridad & Estado) -->
        <div class="grid grid-cols-2 sm:grid-cols-5 gap-3">
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Categoría *</label>
            <select 
              v-model="editingOt.categoria" 
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-white/10 bg-white dark:bg-[#0a0b10] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer font-medium"
            >
              <option value="normal">Normal</option>
              <option value="rural">Rural (Difícil Acceso)</option>
            </select>
          </div>
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Regional *</label>
            <select 
              v-model="editingOt.regional" 
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-white/10 bg-white dark:bg-[#0a0b10] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer font-medium"
            >
              <option value="R1">R1 (Regional 1)</option>
              <option value="R2">R2 (Regional 2)</option>
            </select>
          </div>
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Tipo Estación *</label>
            <select 
              v-model="editingOt.tipo_estacion" 
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-white/10 bg-white dark:bg-[#0a0b10] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
            >
              <option value="MOVIL">MOVIL</option>
              <option value="FIJA">FIJA</option>
              <option value="REPETIDORA">REPETIDORA</option>
              <option value="NODO">NODO</option>
              <option value="CENTRO_DE_DATOS">CENTRO DE DATOS</option>
            </select>
          </div>
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Prioridad *</label>
            <select 
              v-model="editingOt.prioridad" 
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-white/10 bg-white dark:bg-[#0a0b10] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer"
            >
              <option value="P1">P1 - Alta (Crítica)</option>
              <option value="P2">P2 - Media (Normal)</option>
              <option value="P3">P3 - Baja (Planificada)</option>
            </select>
          </div>
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Estado *</label>
            <select 
              v-model="editingOt.estado" 
              required
              class="flex h-9 w-full rounded-md border border-neutral-200 dark:border-white/10 bg-white dark:bg-[#0a0b10] px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 focus:border-primary focus:ring-primary cursor-pointer font-medium"
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

        <!-- Fila 6: Departamento & Ubicación / Municipio -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Departamento *</label>
            <Input type="text" v-model="editingOt.departamento" required class="bg-white dark:bg-[#0a0b10] border-neutral-200 dark:border-white/10 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
          </div>
          <div class="sm:col-span-2 space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Ubicación / Municipio *</label>
            <Input type="text" v-model="editingOt.ubicacion" required class="bg-white dark:bg-[#0a0b10] border-neutral-200 dark:border-white/10 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
          </div>
        </div>

        <!-- Fila 7: Descripción de la Obra / Falla -->
        <div class="space-y-1.5">
          <label class="text-[10px] font-bold text-neutral-550 dark:text-neutral-400 uppercase tracking-wider">Descripción de la Obra / Falla *</label>
          <Input type="text" v-model="editingOt.descripcion" required class="bg-white dark:bg-[#0a0b10] border-neutral-200 dark:border-white/10 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
        </div>
        </div>

        <!-- Botones de Acción (Fijo al pie del modal) -->
        <div class="flex flex-col sm:flex-row justify-end gap-2 border-t border-neutral-200 dark:border-neutral-800 pt-3 mt-2 shrink-0">
          <Button type="button" variant="outline" @click="openEditModal = false" class="border-neutral-200 dark:border-neutral-800 hover:bg-neutral-100 dark:hover:bg-white/5 text-neutral-700 dark:text-neutral-300 w-full sm:w-auto h-9 text-xs">
            Cancelar
          </Button>
          <Button type="submit" class="bg-primary text-primary-foreground hover:bg-primary/95 font-semibold w-full sm:w-auto h-9 text-xs">
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

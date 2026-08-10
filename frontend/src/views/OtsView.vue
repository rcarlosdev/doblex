<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Dialog } from '@/components/ui/dialog';
import { Card } from '@/components/ui/card';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

const username = ref('Usuario');
const router = useRouter();
const openCreateModal = ref(false);
const searchQuery = ref('');
const statusFilter = ref('todos');

const ots = ref([
  { id: 1, code: 'OT-2026-001', description: 'Excavación y Movimiento de Tierra', location: 'Autopista Sur Km 5', manager: 'Ing. Luis Martínez', progress: 100, status: 'finalizado', startDate: '2026-08-01' },
  { id: 2, code: 'OT-2026-002', description: 'Cimentación y Fundición de Zapatas', location: 'Sede Principal Norte', manager: 'Ing. Carlos Pérez', progress: 45, status: 'en_progreso', startDate: '2026-08-05' },
  { id: 3, code: 'OT-2026-003', description: 'Armado de Estructuras Metálicas', location: 'Sede Principal Norte', manager: 'Arq. Sofía Castro', progress: 0, status: 'pendiente', startDate: '2026-08-15' }
]);

const newOt = ref({
  code: '',
  description: '',
  location: '',
  manager: '',
  startDate: new Date().toISOString().split('T')[0]
});

onMounted(() => {
  username.value = localStorage.getItem('smu_username') || 'Administrador Doblex';
});

const handleLogout = () => {
  localStorage.removeItem('smu_authenticated');
  localStorage.removeItem('smu_username');
  router.push({ name: 'login' });
};

const filteredOts = computed(() => {
  return ots.value.filter(ot => {
    const matchesSearch = ot.code.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                         ot.description.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         ot.location.toLowerCase().includes(searchQuery.value.toLowerCase());
    
    const matchesStatus = statusFilter.value === 'todos' || ot.status === statusFilter.value;

    return matchesSearch && matchesStatus;
  });
});

const createOt = () => {
  const id = ots.value.length + 1;
  ots.value.push({
    id,
    code: newOt.value.code,
    description: newOt.value.description,
    location: newOt.value.location,
    manager: newOt.value.manager,
    progress: 0,
    status: 'pendiente',
    startDate: newOt.value.startDate
  });

  // Limpiar formulario y cerrar modal
  newOt.value = {
    code: '',
    description: '',
    location: '',
    manager: '',
    startDate: new Date().toISOString().split('T')[0]
  };
  openCreateModal.value = false;
};

const getStatusBadgeVariant = (status) => {
  switch (status) {
    case 'finalizado': return 'secondary'; // fondo gris oscuro, texto claro
    case 'en_progreso': return 'default'; // fondo rojo (tema primary)
    case 'pendiente': return 'outline'; // borde transparente / borde sutil
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
  <div class="flex min-h-screen bg-neutral-950 text-neutral-100 font-sans">
    <!-- Sidebar de navegación -->
    <aside class="w-64 border-r border-neutral-900 bg-neutral-950/80 backdrop-blur-md flex flex-col p-6">
      <div class="flex items-center gap-2 mb-10 pl-2">
        <span class="text-primary text-xl font-bold filter drop-shadow-[0_0_8px_rgba(239,68,68,0.5)]">▲</span>
        <span class="font-bold tracking-wider text-sm bg-gradient-to-r from-white to-neutral-400 bg-clip-text text-transparent">SMU DOBLEX</span>
      </div>

      <nav class="flex-1 flex flex-col gap-1">
        <router-link to="/" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 text-neutral-400 hover:text-white hover:bg-white/5">
          <span class="text-lg">📊</span>
          <span>Dashboard</span>
        </router-link>

        <router-link to="/ordenes-trabajo" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 bg-primary/10 border border-primary/20 text-white">
          <span class="text-lg">📋</span>
          <span>Órdenes de Trabajo</span>
        </router-link>

        <div class="text-[10px] font-bold text-neutral-600 mt-6 mb-2 tracking-wider uppercase">LOGÍSTICA Y RECURSOS</div>
        <a class="flex items-center justify-between gap-3 px-3 py-2.5 rounded-lg text-sm font-medium opacity-40 cursor-not-allowed text-neutral-400">
          <div class="flex items-center gap-3">
            <span class="text-lg">📦</span>
            <span>Inventarios</span>
          </div>
          <span class="text-[9px] bg-neutral-900 border border-white/5 px-1.5 py-0.5 rounded text-neutral-400">F2</span>
        </a>
        <a class="flex items-center justify-between gap-3 px-3 py-2.5 rounded-lg text-sm font-medium opacity-40 cursor-not-allowed text-neutral-400">
          <div class="flex items-center gap-3">
            <span class="text-lg">🚚</span>
            <span>Vehículos</span>
          </div>
          <span class="text-[9px] bg-neutral-900 border border-white/5 px-1.5 py-0.5 rounded text-neutral-400">F2</span>
        </a>

        <div class="text-[10px] font-bold text-neutral-600 mt-6 mb-2 tracking-wider uppercase">FINANZAS Y RRHH</div>
        <a class="flex items-center justify-between gap-3 px-3 py-2.5 rounded-lg text-sm font-medium opacity-40 cursor-not-allowed text-neutral-400">
          <div class="flex items-center gap-3">
            <span class="text-lg">💵</span>
            <span>Viáticos</span>
          </div>
          <span class="text-[9px] bg-neutral-900 border border-white/5 px-1.5 py-0.5 rounded text-neutral-400">F3</span>
        </a>
        <a class="flex items-center justify-between gap-3 px-3 py-2.5 rounded-lg text-sm font-medium opacity-40 cursor-not-allowed text-neutral-400">
          <div class="flex items-center gap-3">
            <span class="text-lg">👥</span>
            <span>Personal</span>
          </div>
          <span class="text-[9px] bg-neutral-900 border border-white/5 px-1.5 py-0.5 rounded text-neutral-400">F4</span>
        </a>
      </nav>

      <div class="border-t border-neutral-900 pt-5 mt-auto flex flex-col gap-4">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-full bg-gradient-to-br from-primary to-rose-600 text-white flex items-center justify-center font-bold text-xs">
            AD
          </div>
          <div class="flex flex-col">
            <span class="text-xs font-semibold text-white">{{ username }}</span>
            <span class="text-[10px] text-neutral-500">Super Admin</span>
          </div>
        </div>
        <Button @click="handleLogout" variant="ghost" class="w-full text-left justify-start hover:bg-white/5 text-neutral-400 hover:text-white px-3 h-9 text-xs">
          🚪 Cerrar Sesión
        </Button>
      </div>
    </aside>

    <!-- Área principal -->
    <main class="flex-1 p-8 flex flex-col gap-6 overflow-y-auto bg-[#08080c] bg-radial-at-c-ots">
      <!-- Encabezado superior -->
      <header class="border border-neutral-900 bg-neutral-950/60 backdrop-blur-md p-6 rounded-xl flex justify-between items-center relative overflow-hidden">
        <div class="absolute -right-24 -top-24 w-48 h-48 rounded-full bg-primary/5 blur-3xl pointer-events-none"></div>
        <div>
          <h1 class="text-2xl font-bold tracking-tight text-white">Órdenes de Trabajo (OT)</h1>
          <p class="text-xs text-neutral-400">Módulo 1: Control, Asignación y Seguimiento Operativo</p>
        </div>
        <Button @click="openCreateModal = true" class="bg-primary text-primary-foreground hover:bg-primary/95 flex items-center gap-2 font-semibold">
          <span class="text-sm">➕</span> Nueva OT
        </Button>
      </header>

      <!-- Panel de Registro de Órdenes -->
      <Card class="bg-neutral-950/40 border-neutral-900 p-6 flex flex-col gap-4">
        <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-4 border-b border-neutral-900 pb-5">
          <div>
            <h2 class="text-lg font-bold text-white mb-0.5">Registro de Órdenes</h2>
            <p class="text-xs text-neutral-500">Control de OTs y avances del personal en campo</p>
          </div>
          
          <!-- Filtros de Búsqueda y Estados -->
          <div class="flex items-center gap-3">
            <Input 
              type="text" 
              placeholder="Buscar OT..." 
              v-model="searchQuery" 
              class="w-48 sm:w-60 bg-neutral-950/60 border-neutral-800 text-white text-xs placeholder:text-neutral-500"
            />
            <select 
              v-model="statusFilter" 
              class="flex h-9 w-40 rounded-md border border-neutral-800 bg-neutral-950/60 px-3 py-1 text-xs text-neutral-300 shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring focus:border-primary focus:ring-primary"
            >
              <option value="todos">Todos los Estados</option>
              <option value="pendiente">Pendientes</option>
              <option value="en_progreso">En Progreso</option>
              <option value="finalizado">Finalizados</option>
            </select>
          </div>
        </div>

        <!-- Tabla de Órdenes (con shadcn-vue) -->
        <div class="overflow-x-auto">
          <Table>
            <TableHeader class="border-neutral-900">
              <TableRow class="hover:bg-transparent border-neutral-900">
                <TableHead class="text-neutral-500 font-semibold text-xs tracking-wider uppercase pl-4">Código</TableHead>
                <TableHead class="text-neutral-500 font-semibold text-xs tracking-wider uppercase">Descripción / Obra</TableHead>
                <TableHead class="text-neutral-500 font-semibold text-xs tracking-wider uppercase">Ubicación</TableHead>
                <TableHead class="text-neutral-500 font-semibold text-xs tracking-wider uppercase">Encargado</TableHead>
                <TableHead class="text-neutral-500 font-semibold text-xs tracking-wider uppercase w-[150px]">Progreso</TableHead>
                <TableHead class="text-neutral-500 font-semibold text-xs tracking-wider uppercase text-center w-[120px]">Estado</TableHead>
                <TableHead class="text-neutral-500 font-semibold text-xs tracking-wider uppercase text-right pr-4">Acciones</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow v-for="ot in filteredOts" :key="ot.id" class="border-neutral-900 hover:bg-white/[0.02]">
                <TableCell class="font-mono font-bold text-primary pl-4 py-4">{{ ot.code }}</TableCell>
                <TableCell class="py-4">
                  <div class="flex flex-col">
                    <span class="font-medium text-white">{{ ot.description }}</span>
                    <span class="text-[10px] text-neutral-500 mt-0.5">Inicio: {{ ot.startDate }}</span>
                  </div>
                </TableCell>
                <TableCell class="text-neutral-300 py-4">{{ ot.location }}</TableCell>
                <TableCell class="text-neutral-300 py-4">{{ ot.manager }}</TableCell>
                <TableCell class="py-4">
                  <div class="flex items-center gap-3">
                    <Progress :model-value="ot.progress" class="h-1.5 w-24 bg-white/5" />
                    <span class="text-xs font-semibold text-neutral-400">{{ ot.progress }}%</span>
                  </div>
                </TableCell>
                <TableCell class="text-center py-4">
                  <Badge 
                    :variant="getStatusBadgeVariant(ot.status)" 
                    class="text-[10px] font-bold px-2 py-0.5 uppercase tracking-wider"
                    :class="{
                      'bg-emerald-500/10 border-emerald-500/20 text-emerald-400 hover:bg-emerald-500/10': ot.status === 'finalizado',
                      'bg-primary/10 border-primary/20 text-primary hover:bg-primary/10': ot.status === 'en_progreso',
                      'bg-amber-500/10 border-amber-500/20 text-amber-400 hover:bg-amber-500/10': ot.status === 'pendiente',
                    }"
                  >
                    {{ getStatusLabel(ot.status) }}
                  </Badge>
                </TableCell>
                <TableCell class="text-right pr-4 py-4">
                  <div class="inline-flex gap-1">
                    <Button variant="ghost" size="icon" class="h-8 w-8 text-neutral-400 hover:text-white hover:bg-white/5" title="Editar OT">
                      ✏️
                    </Button>
                    <Button variant="ghost" size="icon" class="h-8 w-8 text-neutral-400 hover:text-white hover:bg-white/5" title="Seguimiento Campo">
                      🔧
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
              <TableRow v-if="filteredOts.length === 0" class="hover:bg-transparent">
                <TableCell colspan="7" class="text-center text-neutral-500 py-10">
                  No se encontraron órdenes de trabajo registradas.
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </div>
      </Card>

      <!-- Modal de Registro (Dialog con shadcn-vue) -->
      <Dialog :open="openCreateModal" @close="openCreateModal = false">
        <div class="flex items-center justify-between border-b border-neutral-900 pb-4 mb-5">
          <div>
            <h3 class="text-base font-bold text-white">Crear Nueva Orden de Trabajo</h3>
            <p class="text-[11px] text-neutral-500">Completa los campos para registrar una nueva orden de trabajo</p>
          </div>
          <button @click="openCreateModal = false" class="text-neutral-400 hover:text-white text-lg font-bold">&times;</button>
        </div>

        <form @submit.prevent="createOt" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-1.5">
              <label class="text-[10px] font-bold text-neutral-400 uppercase tracking-wider">Código OT</label>
              <Input type="text" v-model="newOt.code" required placeholder="OT-2026-003" class="bg-neutral-950 border-neutral-850 text-white placeholder:text-neutral-600 focus-visible:ring-primary focus-visible:border-primary" />
            </div>
            <div class="space-y-1.5">
              <label class="text-[10px] font-bold text-neutral-400 uppercase tracking-wider">Ubicación</label>
              <Input type="text" v-model="newOt.location" required placeholder="Zona Norte - Sector B" class="bg-neutral-950 border-neutral-850 text-white placeholder:text-neutral-600 focus-visible:ring-primary focus-visible:border-primary" />
            </div>
          </div>

          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-400 uppercase tracking-wider">Descripción de la Obra</label>
            <Input type="text" v-model="newOt.description" required placeholder="Cimentación y fundición de pilotes" class="bg-neutral-950 border-neutral-850 text-white placeholder:text-neutral-600 focus-visible:ring-primary focus-visible:border-primary" />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-1.5">
              <label class="text-[10px] font-bold text-neutral-400 uppercase tracking-wider">Encargado de Obra</label>
              <Input type="text" v-model="newOt.manager" required placeholder="Ing. Carlos Pérez" class="bg-neutral-950 border-neutral-850 text-white placeholder:text-neutral-600 focus-visible:ring-primary focus-visible:border-primary" />
            </div>
            <div class="space-y-1.5">
              <label class="text-[10px] font-bold text-neutral-400 uppercase tracking-wider">Fecha de Inicio</label>
              <Input type="date" v-model="newOt.startDate" required class="bg-neutral-950 border-neutral-850 text-white focus-visible:ring-primary focus-visible:border-primary" />
            </div>
          </div>

          <div class="flex justify-end gap-2 border-t border-neutral-900 pt-5 mt-6">
            <Button type="button" variant="outline" @click="openCreateModal = false" class="border-neutral-800 hover:bg-white/5 text-neutral-300">
              Cancelar
            </Button>
            <Button type="submit" class="bg-primary text-primary-foreground hover:bg-primary/95 font-semibold">
              Registrar OT
            </Button>
          </div>
        </form>
      </Dialog>
    </main>
  </div>
</template>

<style scoped>
.bg-radial-at-c-ots {
  background-image: radial-gradient(circle at 50% 0%, rgba(239, 68, 68, 0.02) 0%, transparent 50%),
                    linear-gradient(to bottom, #08080c, #030305);
}
</style>

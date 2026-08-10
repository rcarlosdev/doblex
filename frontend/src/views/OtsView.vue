<script setup>
import { ref, computed } from 'vue';
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
    <!-- Encabezado de la Sección (Adaptativo Claro/Oscuro) -->
    <div class="flex flex-col gap-4 sm:flex-row sm:justify-between sm:items-center bg-white dark:bg-neutral-950/45 border border-neutral-200 dark:border-neutral-900 p-4 md:p-6 rounded-xl relative overflow-hidden">
      <div>
        <h1 class="text-xl font-bold tracking-tight text-neutral-900 dark:text-white mb-0.5">Listado de Órdenes (OT)</h1>
        <p class="text-xs text-neutral-500">Gestión de actividades y órdenes de trabajo asignadas</p>
      </div>
      <Button @click="openCreateModal = true" class="bg-primary text-primary-foreground hover:bg-primary/95 flex items-center gap-2 font-semibold w-full sm:w-auto justify-center">
        <span class="text-sm">➕</span> Nueva OT
      </Button>
    </div>

    <!-- Panel de Registro de Órdenes -->
    <Card class="bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900 p-4 md:p-6 flex flex-col gap-4">
      <!-- Encabezado y Filtros (Adaptativos) -->
      <div class="flex flex-col lg:flex-row justify-between lg:items-center gap-4 border-b border-neutral-100 dark:border-neutral-900 pb-5">
        <div>
          <h2 class="text-base font-bold text-neutral-900 dark:text-white mb-0.5">Registro de Órdenes</h2>
          <p class="text-xs text-neutral-500">Control de OTs y avances del personal en campo</p>
        </div>
        
        <!-- Filtros -->
        <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 w-full lg:w-auto">
          <Input 
            type="text" 
            placeholder="Buscar OT..." 
            v-model="searchQuery" 
            class="w-full sm:w-60 bg-white dark:bg-neutral-950/60 border-neutral-200 dark:border-neutral-800 text-neutral-800 dark:text-white text-xs placeholder:text-neutral-450 focus-visible:ring-primary focus-visible:border-primary"
          />
          <select 
            v-model="statusFilter" 
            class="flex h-9 w-full sm:w-40 rounded-md border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-950/60 px-3 py-1 text-xs text-neutral-800 dark:text-neutral-300 shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring focus:border-primary focus:ring-primary cursor-pointer"
          >
            <option value="todos">Todos los Estados</option>
            <option value="pendiente">Pendientes</option>
            <option value="en_progreso">En Progreso</option>
            <option value="finalizado">Finalizados</option>
          </select>
        </div>
      </div>

      <!-- Tabla de Órdenes con soporte responsivo y adaptabilidad de tema -->
      <div class="overflow-x-auto -mx-4 px-4 sm:mx-0 sm:px-0">
        <div class="inline-block min-w-full align-middle">
          <Table>
            <TableHeader class="border-neutral-100 dark:border-neutral-900">
              <TableRow class="hover:bg-transparent border-neutral-100 dark:border-neutral-900">
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase pl-4">Código</TableHead>
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase">Descripción / Obra</TableHead>
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase">Ubicación</TableHead>
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase">Encargado</TableHead>
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase w-[150px]">Progreso</TableHead>
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase text-center w-[120px]">Estado</TableHead>
                <TableHead class="text-neutral-500 dark:text-neutral-500 font-semibold text-xs tracking-wider uppercase text-right pr-4">Acciones</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow v-for="ot in filteredOts" :key="ot.id" class="border-neutral-100 dark:border-neutral-900 hover:bg-neutral-50 dark:hover:bg-white/[0.02]">
                <TableCell class="font-mono font-bold text-primary pl-4 py-4">{{ ot.code }}</TableCell>
                <TableCell class="py-4">
                  <div class="flex flex-col">
                    <span class="font-medium text-neutral-900 dark:text-white whitespace-nowrap">{{ ot.description }}</span>
                    <span class="text-[10px] text-neutral-500 mt-0.5 whitespace-nowrap">Inicio: {{ ot.startDate }}</span>
                  </div>
                </TableCell>
                <TableCell class="text-neutral-700 dark:text-neutral-350 py-4 whitespace-nowrap">{{ ot.location }}</TableCell>
                <TableCell class="text-neutral-700 dark:text-neutral-350 py-4 whitespace-nowrap">{{ ot.manager }}</TableCell>
                <TableCell class="py-4">
                  <div class="flex items-center gap-3">
                    <Progress :model-value="ot.progress" class="h-1.5 w-20 bg-neutral-100 dark:bg-white/5" />
                    <span class="text-xs font-semibold text-neutral-600 dark:text-neutral-400">{{ ot.progress }}%</span>
                  </div>
                </TableCell>
                <TableCell class="text-center py-4">
                  <Badge 
                    :variant="getStatusBadgeVariant(ot.status)" 
                    class="text-[10px] font-bold px-2 py-0.5 uppercase tracking-wider"
                    :class="{
                      'bg-emerald-500/10 border-emerald-500/20 text-emerald-600 dark:text-emerald-400 hover:bg-emerald-500/10': ot.status === 'finalizado',
                      'bg-primary/10 border-primary/20 text-primary hover:bg-primary/10': ot.status === 'en_progreso',
                      'bg-amber-500/10 border-amber-500/20 text-amber-600 dark:text-amber-400 hover:bg-amber-500/10': ot.status === 'pendiente',
                    }"
                  >
                    {{ getStatusLabel(ot.status) }}
                  </Badge>
                </TableCell>
                <TableCell class="text-right pr-4 py-4">
                  <div class="inline-flex gap-1">
                    <Button variant="ghost" size="icon" class="h-8 w-8 text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white hover:bg-neutral-100 dark:hover:bg-white/5" title="Editar OT">
                      ✏️
                    </Button>
                    <Button variant="ghost" size="icon" class="h-8 w-8 text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white hover:bg-neutral-100 dark:hover:bg-white/5" title="Seguimiento Campo">
                      🔧
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
              <TableRow v-if="filteredOts.length === 0" class="hover:bg-transparent">
                <TableCell colspan="7" class="text-center text-neutral-550 py-10">
                  No se encontraron órdenes de trabajo registradas.
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </div>
      </div>
    </Card>

    <!-- Modal de Registro (Dialog responsivo y adaptativo) -->
    <Dialog :open="openCreateModal" @close="openCreateModal = false">
      <div class="flex items-center justify-between border-b border-neutral-200 dark:border-neutral-900 pb-4 mb-5">
        <div>
          <h3 class="text-base font-bold text-neutral-900 dark:text-white">Crear Nueva Orden de Trabajo</h3>
          <p class="text-[11px] text-neutral-500">Completa los campos para registrar una nueva orden de trabajo</p>
        </div>
        <button @click="openCreateModal = false" class="text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white text-lg font-bold">&times;</button>
      </div>

      <form @submit.prevent="createOt" class="space-y-4">
        <!-- Form Row -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Código OT</label>
            <Input type="text" v-model="newOt.code" required placeholder="OT-2026-003" class="bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-850 text-neutral-900 dark:text-white placeholder:text-neutral-400 dark:placeholder:text-neutral-600 focus-visible:ring-primary focus-visible:border-primary" />
          </div>
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Ubicación</label>
            <Input type="text" v-model="newOt.location" required placeholder="Zona Norte - Sector B" class="bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-850 text-neutral-900 dark:text-white placeholder:text-neutral-400 dark:placeholder:text-neutral-600 focus-visible:ring-primary focus-visible:border-primary" />
          </div>
        </div>

        <div class="space-y-1.5">
          <label class="text-[10px] font-bold text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Descripción de la Obra</label>
          <Input type="text" v-model="newOt.description" required placeholder="Cimentación y fundición de pilotes" class="bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-850 text-neutral-900 dark:text-white placeholder:text-neutral-400 dark:placeholder:text-neutral-600 focus-visible:ring-primary focus-visible:border-primary" />
        </div>

        <!-- Form Row -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Encargado de Obra</label>
            <Input type="text" v-model="newOt.manager" required placeholder="Ing. Carlos Pérez" class="bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-850 text-neutral-900 dark:text-white placeholder:text-neutral-400 dark:placeholder:text-neutral-600 focus-visible:ring-primary focus-visible:border-primary" />
          </div>
          <div class="space-y-1.5">
            <label class="text-[10px] font-bold text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Fecha de Inicio</label>
            <Input type="date" v-model="newOt.startDate" required class="bg-white dark:bg-neutral-950 border-neutral-200 dark:border-neutral-850 text-neutral-900 dark:text-white focus-visible:ring-primary focus-visible:border-primary" />
          </div>
        </div>

        <!-- Botones de Acción -->
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
  </div>
</template>

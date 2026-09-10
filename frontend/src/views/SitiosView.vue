<script setup>
import { ref, reactive, onMounted, watch } from 'vue';
import { 
  getSitios, 
  getSitiosStats, 
  getSitiosFiltros, 
  createSitio 
} from '@/api/sitios';
import { usePagination } from '@/composables/usePagination';
import { useNotification } from '@/composables/useNotification';

// UI & Icons
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  IconTower, 
  IconRefresh, 
  IconPlus, 
  IconAlertCircle, 
  IconCheck, 
  IconX 
} from '@tabler/icons-vue';

// Feature Components
import SitioStatsCards from '@/components/sitios/SitioStatsCards.vue';
import SitioFilterBar from '@/components/sitios/SitioFilterBar.vue';
import SitioTable from '@/components/sitios/SitioTable.vue';
import SitioDetailModal from '@/components/sitios/SitioDetailModal.vue';
import SitioFormModal from '@/components/sitios/SitioFormModal.vue';

// Estado de carga y datos
const loading = ref(false);
const sitios = ref([]);
const pagination = usePagination(25);
const { notification, showSuccess, showError, clearNotification } = useNotification();

// Estadísticas y opciones dinámicas
const stats = ref({
  total_sitios: 0,
  zonas: {},
  zonas_tecnicas: {},
  estructuras_principales: {},
  con_transporte_especial: 0
});

const filterOptions = ref({
  zonas: [],
  zonas_tecnicas: [],
  ciudades_base: [],
  estructuras: []
});

// Filtros reactivos
const filters = reactive({
  search: '',
  zona: '',
  zona_tecnica: '',
  ciudad_base: '',
  estructura: ''
});

// Modales
const selectedSitio = ref(null);
const showDetailModal = ref(false);
const showCreateModal = ref(false);
const submitting = ref(false);

let searchTimeout = null;

// Carga de sitios
const fetchSitios = async () => {
  loading.value = true;
  try {
    const params = {
      page: pagination.page.value,
      limit: pagination.limit.value,
      search: filters.search.trim() || undefined,
      zona: filters.zona || undefined,
      zona_tecnica: filters.zona_tecnica || undefined,
      ciudad_base: filters.ciudad_base || undefined,
      estructura: filters.estructura || undefined
    };
    const res = await getSitios(params);
    sitios.value = res.items || [];
    pagination.total.value = res.total || 0;
  } catch (err) {
    console.error('Error al cargar sitios:', err);
    showError('Error al conectar con el servidor de sitios.');
  } finally {
    loading.value = false;
  }
};

// Carga de metadatos y filtros
const fetchMetadata = async () => {
  try {
    const [statsRes, filtrosRes] = await Promise.all([
      getSitiosStats(),
      getSitiosFiltros()
    ]);
    stats.value = statsRes;
    filterOptions.value = filtrosRes;
  } catch (err) {
    console.error('Error al cargar metadatos de sitios:', err);
  }
};

// Manejo de búsqueda y debounce
const handleSearchInput = () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    pagination.resetPage();
    fetchSitios();
  }, 350);
};

const resetFilters = () => {
  filters.search = '';
  filters.zona = '';
  filters.zona_tecnica = '';
  filters.ciudad_base = '';
  filters.estructura = '';
  pagination.resetPage();
  fetchSitios();
};

const openDetail = (sitio) => {
  selectedSitio.value = sitio;
  showDetailModal.value = true;
};

// Creación de sitio
const handleCreateSitio = async (formData) => {
  if (!formData.nombre.trim()) {
    showError('El nombre del sitio es obligatorio.');
    return;
  }
  submitting.value = true;
  try {
    await createSitio(formData);
    showSuccess('Sitio creado exitosamente en la base de datos.');
    showCreateModal.value = false;
    fetchSitios();
    fetchMetadata();
  } catch (err) {
    const msg = err.response?.data?.message || 'Error al guardar el sitio.';
    showError(msg);
  } finally {
    submitting.value = false;
  }
};

// Reactividad ante cambios de filtros y paginación
watch(
  () => [filters.zona, filters.zona_tecnica, filters.ciudad_base, filters.estructura],
  () => {
    pagination.resetPage();
    fetchSitios();
  }
);

watch(pagination.page, () => fetchSitios());

onMounted(() => {
  fetchSitios();
  fetchMetadata();
});
</script>

<template>
  <div class="space-y-6 max-w-[1600px] mx-auto pb-12">
    <!-- Banner de notificación unificado -->
    <div 
      v-if="notification.visible" 
      class="p-4 rounded-xl flex items-center justify-between text-sm transition-all duration-300"
      :class="notification.type === 'error' 
        ? 'bg-red-50 dark:bg-red-950/40 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-900/50' 
        : 'bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-900/50'"
    >
      <div class="flex items-center gap-2 font-medium">
        <IconAlertCircle v-if="notification.type === 'error'" class="w-5 h-5 shrink-0" />
        <IconCheck v-else class="w-5 h-5 shrink-0" />
        <span>{{ notification.text }}</span>
      </div>
      <button @click="clearNotification" class="hover:opacity-75">
        <IconX class="w-4 h-4" />
      </button>
    </div>

    <!-- Cabecera principal -->
    <div class="flex flex-col gap-4 sm:flex-row sm:justify-between sm:items-center bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 p-5 md:p-6 rounded-2xl relative overflow-hidden shadow-sm">
      <div>
        <div class="flex items-center gap-2.5 mb-1">
          <div class="p-2 bg-primary/10 text-primary rounded-xl">
            <IconTower class="w-6 h-6" />
          </div>
          <h1 class="text-xl md:text-2xl font-black text-neutral-900 dark:text-white tracking-tight">
            Base de Datos de Sitios
          </h1>
          <Badge variant="outline" class="border-primary/30 text-primary font-bold text-[11px] uppercase tracking-wider">
            Estaciones Base
          </Badge>
        </div>
        <p class="text-xs md:text-sm text-neutral-500 dark:text-neutral-400">
          Catálogo maestro de telecomunicaciones: infraestructura, códigos de transporte LPU, alturas SST y directorio operativo Claro.
        </p>
      </div>

      <div class="flex items-center gap-2.5">
        <Button 
          variant="outline" 
          size="sm" 
          @click="fetchSitios(); fetchMetadata();"
          :disabled="loading"
          class="h-9 border-neutral-200 dark:border-white/10 text-xs font-semibold hover:bg-neutral-100 dark:hover:bg-white/5"
        >
          <IconRefresh class="w-4 h-4 mr-1.5" :class="{'animate-spin': loading}" />
          Actualizar
        </Button>
        <Button 
          size="sm" 
          @click="showCreateModal = true"
          class="h-9 bg-primary hover:bg-primary/90 text-white font-bold text-xs shadow-sm"
        >
          <IconPlus class="w-4 h-4 mr-1.5" />
          Nuevo Sitio
        </Button>
      </div>
    </div>

    <!-- Métricas y KPIs de Sitios -->
    <SitioStatsCards :stats="stats" />

    <!-- Barra de Filtros y Búsqueda -->
    <SitioFilterBar 
      :filters="filters"
      :filter-options="filterOptions"
      :current-count="sitios.length"
      :total-count="pagination.total.value"
      @search-input="handleSearchInput"
      @reset="resetFilters"
    />

    <!-- Tabla Principal de Sitios y Paginación -->
    <SitioTable 
      :sitios="sitios"
      :loading="loading"
      :page="pagination.page.value"
      :pages="pagination.pages.value"
      :limit="pagination.limit.value"
      @view-detail="openDetail"
      @update:page="pagination.setPage"
      @update:limit="pagination.setLimit"
    />

    <!-- Modal Detalle Completo de Ficha Técnica -->
    <SitioDetailModal 
      :show="showDetailModal"
      :sitio="selectedSitio"
      @close="showDetailModal = false"
    />

    <!-- Modal Crear Nuevo Sitio -->
    <SitioFormModal 
      :show="showCreateModal"
      :submitting="submitting"
      @close="showCreateModal = false"
      @submit="handleCreateSitio"
    />
  </div>
</template>

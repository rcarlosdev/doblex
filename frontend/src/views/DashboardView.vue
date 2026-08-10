<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';

const username = ref('Usuario');
const router = useRouter();

onMounted(() => {
  username.value = localStorage.getItem('smu_username') || 'Administrador Doblex';
});

const handleLogout = () => {
  localStorage.removeItem('smu_authenticated');
  localStorage.removeItem('smu_username');
  router.push({ name: 'login' });
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
        <router-link to="/" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 bg-primary/10 border border-primary/20 text-white">
          <span class="text-lg">📊</span>
          <span>Dashboard</span>
        </router-link>

        <router-link to="/ordenes-trabajo" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 text-neutral-400 hover:text-white hover:bg-white/5">
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
    <main class="flex-1 p-8 flex flex-col gap-6 overflow-y-auto bg-[#08080c] bg-radial-at-c-dash">
      <!-- Encabezado superior -->
      <header class="border border-neutral-900 bg-neutral-950/60 backdrop-blur-md p-6 rounded-xl flex justify-between items-center relative overflow-hidden">
        <div class="absolute -right-24 -top-24 w-48 h-48 rounded-full bg-primary/5 blur-3xl pointer-events-none"></div>
        <div>
          <h1 class="text-2xl font-bold tracking-tight text-white">Panel de Control</h1>
          <p class="text-xs text-neutral-400">Bienvenido de nuevo al Sistema de Gestión de Obra (SMU)</p>
        </div>
        <div class="flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold px-3 py-1.5 rounded-full">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          Servidor API Online
        </div>
      </header>

      <!-- Grid de KPIs (Tarjetas con shadcn-vue) -->
      <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card class="bg-neutral-950/40 border-neutral-900 hover:border-neutral-800 transition-all duration-200 hover:-translate-y-1">
          <CardHeader class="flex flex-row items-center justify-between pb-2 space-y-0">
            <CardTitle class="text-xs font-semibold uppercase tracking-wider text-neutral-400">Órdenes Activas</CardTitle>
            <div class="text-xl bg-primary/10 border border-primary/20 text-primary w-8 h-8 rounded-lg flex items-center justify-center">📋</div>
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold text-white mb-1">12</div>
            <p class="text-[10px] text-neutral-500">+3 esta semana</p>
          </CardContent>
        </Card>

        <Card class="bg-neutral-950/40 border-neutral-900 hover:border-neutral-800 transition-all duration-200 hover:-translate-y-1">
          <CardHeader class="flex flex-row items-center justify-between pb-2 space-y-0">
            <CardTitle class="text-xs font-semibold uppercase tracking-wider text-neutral-400">Actividades en Campo</CardTitle>
            <div class="text-xl bg-primary/10 border border-primary/20 text-primary w-8 h-8 rounded-lg flex items-center justify-center">🛠️</div>
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold text-white mb-1">34</div>
            <p class="text-[10px] text-neutral-500">87% ejecutado</p>
          </CardContent>
        </Card>

        <Card class="bg-neutral-950/40 border-neutral-900 hover:border-neutral-800 transition-all duration-200 hover:-translate-y-1">
          <CardHeader class="flex flex-row items-center justify-between pb-2 space-y-0">
            <CardTitle class="text-xs font-semibold uppercase tracking-wider text-neutral-400">Alertas de Obra</CardTitle>
            <div class="text-xl bg-red-500/10 border border-red-500/20 text-red-500 w-8 h-8 rounded-lg flex items-center justify-center">⚠️</div>
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold text-white mb-1">2</div>
            <p class="text-[10px] text-red-400 font-medium">Requiere atención</p>
          </CardContent>
        </Card>

        <Card class="bg-neutral-950/40 border-neutral-900 hover:border-neutral-800 transition-all duration-200 hover:-translate-y-1">
          <CardHeader class="flex flex-row items-center justify-between pb-2 space-y-0">
            <CardTitle class="text-xs font-semibold uppercase tracking-wider text-neutral-400">Equipos Asignados</CardTitle>
            <div class="text-xl bg-primary/10 border border-primary/20 text-primary w-8 h-8 rounded-lg flex items-center justify-center">🚚</div>
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold text-white mb-1">8</div>
            <p class="text-[10px] text-neutral-500">En tránsito o uso</p>
          </CardContent>
        </Card>
      </section>

      <!-- Cuerpo del Dashboard: Layout de Dos Columnas -->
      <section class="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1">
        <!-- Panel de Estado (Fase 1) -->
        <Card class="lg:col-span-2 bg-neutral-950/40 border-neutral-900 p-6 flex flex-col gap-6">
          <div>
            <h2 class="text-lg font-bold text-white mb-1">Fase 1: Configuración Base y Núcleo Operativo</h2>
            <p class="text-xs text-neutral-500">Avance de los hitos y metas establecidos en el plan de desarrollo</p>
          </div>
          
          <div class="space-y-5">
            <div class="space-y-2">
              <div class="flex justify-between text-xs text-neutral-300">
                <span>Hito 1.1: Inicialización Arquitectura</span>
                <span class="font-semibold text-primary">100%</span>
              </div>
              <Progress :model-value="100" />
            </div>

            <div class="space-y-2">
              <div class="flex justify-between text-xs text-neutral-300">
                <span>Hito 1.2: CRUD Órdenes de Trabajo (OT) y Actividades</span>
                <span class="font-semibold text-primary">40%</span>
              </div>
              <Progress :model-value="40" />
            </div>

            <div class="space-y-2">
              <div class="flex justify-between text-xs text-neutral-300">
                <span>Hito 1.3: Control de Campo y Avance Diario</span>
                <span class="font-semibold text-primary">10%</span>
              </div>
              <Progress :model-value="10" />
            </div>
          </div>
        </Card>

        <!-- Panel Lateral: Actividades Recientes -->
        <Card class="bg-neutral-950/40 border-neutral-900 p-6 flex flex-col gap-6">
          <div>
            <h2 class="text-lg font-bold text-white mb-1">Actividades Recientes</h2>
            <p class="text-xs text-neutral-500">Log de eventos y configuraciones en el entorno</p>
          </div>

          <div class="flex-1 flex flex-col gap-5 relative pl-4 border-l border-neutral-900">
            <div class="relative">
              <span class="absolute -left-[21px] top-1.5 w-2.5 h-2.5 rounded-full bg-primary border-2 border-neutral-950 ring-4 ring-primary/20"></span>
              <div class="space-y-0.5">
                <h4 class="text-xs font-semibold text-white">Componentes shadcn integrados</h4>
                <p class="text-[11px] text-neutral-400">Configurado TailwindCSS, alias de rutas y componentes base con el tema Red.</p>
                <span class="block text-[9px] text-neutral-600">Hace unos instantes</span>
              </div>
            </div>

            <div class="relative">
              <span class="absolute -left-[21px] top-1.5 w-2.5 h-2.5 rounded-full bg-neutral-800 border-2 border-neutral-950"></span>
              <div class="space-y-0.5">
                <h4 class="text-xs font-semibold text-white">Base de datos conectada</h4>
                <p class="text-[11px] text-neutral-400">Contenedor de PostgreSQL en ejecución y migraciones de Laravel aplicadas.</p>
                <span class="block text-[9px] text-neutral-600">Hace 30 minutos</span>
              </div>
            </div>

            <div class="relative">
              <span class="absolute -left-[21px] top-1.5 w-2.5 h-2.5 rounded-full bg-neutral-800 border-2 border-neutral-950"></span>
              <div class="space-y-0.5">
                <h4 class="text-xs font-semibold text-white">Configuración del Backend lista</h4>
                <p class="text-[11px] text-neutral-400">Laravel API configurado con soporte para CORS y Sanctum para el Frontend.</p>
                <span class="block text-[9px] text-neutral-600">Hace 1 hora</span>
              </div>
            </div>
          </div>
        </Card>
      </section>
    </main>
  </div>
</template>

<style scoped>
.bg-radial-at-c-dash {
  background-image: radial-gradient(circle at 50% 0%, rgba(239, 68, 68, 0.02) 0%, transparent 50%),
                    linear-gradient(to bottom, #08080c, #030305);
}
</style>

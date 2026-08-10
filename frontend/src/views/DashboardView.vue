<script setup>
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
</script>

<template>
  <div class="flex flex-col gap-6 select-none">
    <!-- Grid de KPIs (Tarjetas con shadcn-vue adaptativas Claro/Oscuro) -->
    <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <Card class="bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900 hover:border-neutral-300 dark:hover:border-neutral-800 transition-all duration-200 hover:-translate-y-1">
        <CardHeader class="flex flex-row items-center justify-between pb-2 space-y-0">
          <CardTitle class="text-xs font-semibold uppercase tracking-wider text-neutral-500 dark:text-neutral-400">Órdenes Activas</CardTitle>
          <div class="text-xl bg-primary/10 border border-primary/20 text-primary w-8 h-8 rounded-lg flex items-center justify-center">📋</div>
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold text-neutral-900 dark:text-white mb-1">12</div>
          <p class="text-[10px] text-neutral-500">➕3 esta semana</p>
        </CardContent>
      </Card>

      <Card class="bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900 hover:border-neutral-300 dark:hover:border-neutral-800 transition-all duration-200 hover:-translate-y-1">
        <CardHeader class="flex flex-row items-center justify-between pb-2 space-y-0">
          <CardTitle class="text-xs font-semibold uppercase tracking-wider text-neutral-500 dark:text-neutral-400">Actividades en Campo</CardTitle>
          <div class="text-xl bg-primary/10 border border-primary/20 text-primary w-8 h-8 rounded-lg flex items-center justify-center">🛠️</div>
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold text-neutral-900 dark:text-white mb-1">34</div>
          <p class="text-[10px] text-neutral-500">87% ejecutado</p>
        </CardContent>
      </Card>

      <Card class="bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900 hover:border-neutral-300 dark:hover:border-neutral-800 transition-all duration-200 hover:-translate-y-1">
        <CardHeader class="flex flex-row items-center justify-between pb-2 space-y-0">
          <CardTitle class="text-xs font-semibold uppercase tracking-wider text-neutral-500 dark:text-neutral-400">Alertas de Obra</CardTitle>
          <div class="text-xl bg-red-500/10 border border-red-500/20 text-red-500 w-8 h-8 rounded-lg flex items-center justify-center">⚠️</div>
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold text-neutral-900 dark:text-white mb-1">2</div>
          <p class="text-[10px] text-red-500 font-medium">Requiere atención</p>
        </CardContent>
      </Card>

      <Card class="bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900 hover:border-neutral-300 dark:hover:border-neutral-800 transition-all duration-200 hover:-translate-y-1">
        <CardHeader class="flex flex-row items-center justify-between pb-2 space-y-0">
          <CardTitle class="text-xs font-semibold uppercase tracking-wider text-neutral-500 dark:text-neutral-400">Equipos Asignados</CardTitle>
          <div class="text-xl bg-primary/10 border border-primary/20 text-primary w-8 h-8 rounded-lg flex items-center justify-center">🚚</div>
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold text-neutral-900 dark:text-white mb-1">8</div>
          <p class="text-[10px] text-neutral-500">En tránsito o uso</p>
        </CardContent>
      </Card>
    </section>

    <!-- Cuerpo del Dashboard: Layout de Dos Columnas -->
    <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Panel de Avance de Obras Principales (Datos de Negocio) -->
      <Card class="lg:col-span-2 bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900 p-6 flex flex-col gap-6">
        <div>
          <h2 class="text-lg font-bold text-neutral-900 dark:text-white mb-1">Avance de Obras Principales</h2>
          <p class="text-xs text-neutral-500">Seguimiento de frentes de trabajo y estado de avance operativo</p>
        </div>
        
        <div class="space-y-5">
          <div class="space-y-2">
            <div class="flex justify-between text-xs text-neutral-700 dark:text-neutral-300">
              <span>OT-2026-001: Excavación y Movimiento de Tierra (Autopista Sur Km 5)</span>
              <span class="font-semibold text-primary">100%</span>
            </div>
            <Progress :model-value="100" />
          </div>

          <div class="space-y-2">
            <div class="flex justify-between text-xs text-neutral-700 dark:text-neutral-300">
              <span>OT-2026-002: Cimentación y Fundición de Zapatas (Sede Principal Norte)</span>
              <span class="font-semibold text-primary">45%</span>
            </div>
            <Progress :model-value="45" />
          </div>

          <div class="space-y-2">
            <div class="flex justify-between text-xs text-neutral-700 dark:text-neutral-300">
              <span>OT-2026-003: Armado de Estructuras Metálicas (Sede Principal Norte)</span>
              <span class="font-semibold text-primary">0%</span>
            </div>
            <Progress :model-value="0" />
          </div>
        </div>
      </Card>

      <!-- Panel Lateral: Actividades Recientes en Campo (Eventos de Negocio) -->
      <Card class="bg-white dark:bg-neutral-950/40 border-neutral-200 dark:border-neutral-900 p-6 flex flex-col gap-6">
        <div>
          <h2 class="text-lg font-bold text-neutral-900 dark:text-white mb-1">Actividades de Campo</h2>
          <p class="text-xs text-neutral-500">Registro de reportes diarios y eventos en los frentes de obra</p>
        </div>

        <div class="flex-grow flex flex-col gap-5 relative pl-4 border-l border-neutral-200 dark:border-neutral-900">
          <div class="relative">
            <span class="absolute -left-[21px] top-1.5 w-2.5 h-2.5 rounded-full bg-primary border-2 border-white dark:border-neutral-950 ring-4 ring-primary/20"></span>
            <div class="space-y-0.5">
              <h4 class="text-xs font-semibold text-neutral-900 dark:text-white">Avance registrado en OT-2026-002</h4>
              <p class="text-[11px] text-neutral-600 dark:text-neutral-400">Ing. Carlos Pérez reportó el armado de vigas de amarre del sector A.</p>
              <span class="block text-[9px] text-neutral-400 dark:text-neutral-600">Hace 15 minutos</span>
            </div>
          </div>

          <div class="relative">
            <span class="absolute -left-[21px] top-1.5 w-2.5 h-2.5 rounded-full bg-amber-500 border-2 border-white dark:border-neutral-950"></span>
            <div class="space-y-0.5">
              <h4 class="text-xs font-semibold text-neutral-900 dark:text-white">Alerta: Novedad climatológica</h4>
              <p class="text-[11px] text-neutral-600 dark:text-neutral-400">Retraso reportado en vaciado de concreto en frente Norte por lluvias fuertes.</p>
              <span class="block text-[9px] text-neutral-400 dark:text-neutral-600">Hace 2 horas</span>
            </div>
          </div>

          <div class="relative">
            <span class="absolute -left-[21px] top-1.5 w-2.5 h-2.5 rounded-full bg-emerald-500 border-2 border-white dark:border-neutral-950"></span>
            <div class="space-y-0.5">
              <h4 class="text-xs font-semibold text-neutral-900 dark:text-white">OT-2026-001 finalizada</h4>
              <p class="text-[11px] text-neutral-600 dark:text-neutral-400">Ing. Luis Martínez completó la entrega del tramo vial y retiró maquinaria pesada.</p>
              <span class="block text-[9px] text-neutral-400 dark:text-neutral-600">Ayer, 17:30</span>
            </div>
          </div>
        </div>
      </Card>
    </section>
  </div>
</template>

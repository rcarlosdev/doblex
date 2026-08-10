<script setup>
import { onMounted } from 'vue';

onMounted(() => {
  // Inicialización inteligente del Tema (Claro / Oscuro)
  const savedTheme = localStorage.getItem('smu_theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

  // Por defecto adoptamos el tema oscuro o la preferencia guardada, respetando la estetica premium red
  if (savedTheme === 'dark' || (!savedTheme && prefersDark) || !savedTheme) {
    document.documentElement.classList.add('dark');
    localStorage.setItem('smu_theme', 'dark');
  } else {
    document.documentElement.classList.remove('dark');
    localStorage.setItem('smu_theme', 'light');
  }
});
</script>

<template>
  <div class="min-h-screen bg-background text-foreground transition-colors duration-300">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<style>
/* Transición global fade de rutas principales */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

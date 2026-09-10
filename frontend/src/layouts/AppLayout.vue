<script setup>
import { ref, onMounted } from 'vue';
import Sidebar from '@/components/Sidebar.vue';
import Navbar from '@/components/Navbar.vue';

const isSidebarOpen = ref(true);

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
  if (typeof window !== 'undefined' && window.innerWidth >= 768) {
    localStorage.setItem('smu_sidebar_desktop', String(isSidebarOpen.value));
  }
};

const handleMobileClose = () => {
  if (typeof window !== 'undefined' && window.innerWidth < 768) {
    isSidebarOpen.value = false;
  }
};

onMounted(() => {
  if (typeof window !== 'undefined') {
    if (window.innerWidth >= 768) {
      const saved = localStorage.getItem('smu_sidebar_desktop');
      isSidebarOpen.value = saved !== null ? saved === 'true' : true;
    } else {
      isSidebarOpen.value = false;
    }
  }
});
</script>

<template>
  <div class="flex h-screen bg-slate-100 dark:bg-[#0a0b10] text-neutral-900 dark:text-neutral-100 font-sans overflow-hidden transition-colors duration-300">
    <!-- Overlay oscuro de fondo en móviles cuando el Sidebar está abierto -->
    <div 
      v-if="isSidebarOpen" 
      class="fixed inset-0 z-40 bg-black/70 backdrop-blur-sm md:hidden transition-opacity duration-300"
      @click="isSidebarOpen = false"
    ></div>

    <!-- Sidebar de navegación lateral responsivo y colapsable -->
    <Sidebar 
      :open="isSidebarOpen" 
      @close="handleMobileClose" 
    />

    <!-- Contenedor del contenido principal -->
    <div class="flex-1 flex flex-col min-w-0 h-full overflow-hidden transition-all duration-300">
      <!-- Navbar superior (envía evento para alternar el estado del Sidebar) -->
      <Navbar @toggle-sidebar="toggleSidebar" class="shrink-0" />

      <!-- Cuerpo principal de contenido -->
      <main class="flex-1 p-4 md:p-8 overflow-y-auto bg-neutral-50 dark:bg-[#0a0b10] bg-radial-at-c-layout transition-colors duration-350">
        <router-view v-slot="{ Component }">
          <transition name="layout-fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<style scoped>
.bg-radial-at-c-layout {
  background-image: radial-gradient(circle at 50% 0%, rgba(239, 68, 68, 0.015) 0%, transparent 50%);
}

/* Transición interna de vistas hijas */
.layout-fade-enter-active,
.layout-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.layout-fade-enter-from {
  opacity: 0;
  transform: translateY(4px);
}
.layout-fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>

<script setup>
defineProps({
  open: { type: Boolean, default: false },
});

defineEmits(["close"]);
</script>

<template>
  <Teleport to="body">
    <Transition name="dialog-fade">
      <div v-if="open" class="fixed inset-0 z-50 flex items-center justify-center p-2.5 sm:p-4 md:p-6 overflow-y-auto">
        <!-- Overlay -->
        <div class="fixed inset-0 bg-black/70 backdrop-blur-sm" @click="$emit('close')"></div>
        
        <!-- Content Wrapper -->
        <div class="relative z-50 w-full max-w-xl border bg-white dark:bg-[#121215] p-3.5 sm:p-6 shadow-2xl duration-200 rounded-2xl border-neutral-200 dark:border-white/10 max-h-[94vh] flex flex-col my-auto transition-all overflow-hidden">
          <slot />
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.dialog-fade-enter-active,
.dialog-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.dialog-fade-enter-from,
.dialog-fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>

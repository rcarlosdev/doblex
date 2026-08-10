<script setup>
defineProps({
  open: { type: Boolean, default: false },
});

defineEmits(["close"]);
</script>

<template>
  <Teleport to="body">
    <Transition name="dialog-fade">
      <div v-if="open" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <!-- Overlay -->
        <div class="fixed inset-0 bg-black/80 backdrop-blur-sm" @click="$emit('close')"></div>
        
        <!-- Content Wrapper -->
        <div class="relative z-50 w-full max-w-lg border bg-background p-6 shadow-lg duration-200 rounded-lg md:w-full border-border">
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

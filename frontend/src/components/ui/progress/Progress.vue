<script setup>
import { computed } from "vue";
import { ProgressIndicator, ProgressRoot } from "radix-vue";
import { cn } from "@/lib/utils";

const props = defineProps({
  modelValue: { type: [Number, null], default: 0 },
  max: { type: Number, default: 100 },
  class: { type: String, default: "" },
});

const value = computed(() => (typeof props.modelValue === "number" ? props.modelValue : 0));
</script>

<template>
  <ProgressRoot
    :class="
      cn(
        'relative h-2 w-full overflow-hidden rounded-full bg-primary/20',
        props.class
      )
    "
    :value="value"
    :max="max"
  >
    <ProgressIndicator
      class="h-full w-full flex-1 bg-primary transition-all duration-300"
      :style="`transform: translateX(-${100 - (value / props.max) * 100}%)`"
    />
  </ProgressRoot>
</template>

import { ref, computed } from 'vue';

export function usePagination(initialLimit = 25) {
  const page = ref(1);
  const limit = ref(initialLimit);
  const total = ref(0);

  const pages = computed(() => {
    return total.value > 0 ? Math.ceil(total.value / limit.value) : 1;
  });

  const hasPrev = computed(() => page.value > 1);
  const hasNext = computed(() => page.value < pages.value);

  const nextPage = () => {
    if (hasNext.value) {
      page.value++;
    }
  };

  const prevPage = () => {
    if (hasPrev.value) {
      page.value--;
    }
  };

  const setPage = (p) => {
    const target = Number(p);
    if (target >= 1 && target <= pages.value) {
      page.value = target;
    }
  };

  const setLimit = (l) => {
    limit.value = Number(l);
    page.value = 1;
  };

  const resetPage = () => {
    page.value = 1;
  };

  return {
    page,
    limit,
    total,
    pages,
    hasPrev,
    hasNext,
    nextPage,
    prevPage,
    setPage,
    setLimit,
    resetPage
  };
}

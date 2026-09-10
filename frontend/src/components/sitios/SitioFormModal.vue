<script setup>
import { reactive, watch } from 'vue';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { IconTower, IconX } from '@tabler/icons-vue';

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  submitting: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close', 'submit']);

const formData = reactive({
  nombre: '',
  zona: 'NORTE',
  zona_tecnica: '',
  ciudad_base: '',
  municipio: '',
  ubicacion: '',
  codigo_transporte_lpu: '',
  km: null,
  transporte_especial: '',
  estructura: 'Torre',
  altura_estructura: null,
  supervisor_operativo: '',
  correo_so: '',
  jefe_zona: '',
  correo_jefe_zona: '',
  ingeniero_soporte: '',
  correo_ing_soporte: '',
  facturadora: 'Daniela'
});

const resetForm = () => {
  Object.assign(formData, {
    nombre: '',
    zona: 'NORTE',
    zona_tecnica: '',
    ciudad_base: '',
    municipio: '',
    ubicacion: '',
    codigo_transporte_lpu: '',
    km: null,
    transporte_especial: '',
    estructura: 'Torre',
    altura_estructura: null,
    supervisor_operativo: '',
    correo_so: '',
    jefe_zona: '',
    correo_jefe_zona: '',
    ingeniero_soporte: '',
    correo_ing_soporte: '',
    facturadora: 'Daniela'
  });
};

watch(() => props.show, (newVal) => {
  if (newVal) {
    resetForm();
  }
});

const handleSubmit = () => {
  emit('submit', { ...formData });
};
</script>

<template>
  <Teleport to="body">
    <div 
      v-if="show" 
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-in fade-in duration-200 !m-0"
    >
      <div class="bg-white dark:bg-[#121215] border border-neutral-200 dark:border-white/10 rounded-2xl w-full max-w-xl overflow-hidden shadow-2xl animate-in zoom-in-95 duration-200 max-h-[90vh] flex flex-col">
        <div class="p-5 border-b border-neutral-100 dark:border-white/10 flex items-center justify-between">
          <h2 class="text-base font-bold text-neutral-900 dark:text-white flex items-center gap-2">
            <IconTower class="w-5 h-5 text-primary" />
            Registrar Nuevo Sitio / Estación Base
          </h2>
          <button @click="emit('close')" class="text-neutral-400 hover:text-neutral-700 dark:hover:text-white">
            <IconX class="w-5 h-5" />
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="p-6 overflow-y-auto space-y-4 text-xs flex-1">
          <div>
            <label class="block font-bold text-neutral-700 dark:text-neutral-300 uppercase tracking-wider text-[10px] mb-1">Nombre del Sitio (EB) *</label>
            <Input v-model="formData.nombre" placeholder="Ej. ANT.MEDELLIN CENTRO" required class="text-xs uppercase" />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-neutral-700 dark:text-neutral-300 uppercase tracking-wider text-[10px] mb-1">Macro Zona *</label>
              <select v-model="formData.zona" class="h-9 w-full rounded-md border border-neutral-200 dark:border-white/10 bg-white dark:bg-[#0a0b10] px-3 py-1 text-xs">
                <option value="NORTE">NORTE</option>
                <option value="COSTA">COSTA</option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-neutral-700 dark:text-neutral-300 uppercase tracking-wider text-[10px] mb-1">Zona Técnica</label>
              <Input v-model="formData.zona_tecnica" placeholder="Ej. ANTIOQUIA" class="text-xs" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-neutral-700 dark:text-neutral-300 uppercase tracking-wider text-[10px] mb-1">Municipio</label>
              <Input v-model="formData.municipio" placeholder="Ej. Medellín" class="text-xs" />
            </div>
            <div>
              <label class="block font-bold text-neutral-700 dark:text-neutral-300 uppercase tracking-wider text-[10px] mb-1">Ciudad Base</label>
              <Input v-model="formData.ciudad_base" placeholder="Ej. MEDELLIN" class="text-xs uppercase" />
            </div>
          </div>

          <div>
            <label class="block font-bold text-neutral-700 dark:text-neutral-300 uppercase tracking-wider text-[10px] mb-1">Dirección / Ubicación Física</label>
            <Input v-model="formData.ubicacion" placeholder="Ej. Cra 50 # 50-20 Barrio La Candelaria" class="text-xs" />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-neutral-700 dark:text-neutral-300 uppercase tracking-wider text-[10px] mb-1">Estructura</label>
              <Input v-model="formData.estructura" placeholder="Ej. Torre, Poste, C2" class="text-xs" />
            </div>
            <div>
              <label class="block font-bold text-neutral-700 dark:text-neutral-300 uppercase tracking-wider text-[10px] mb-1">Altura Estructura (m)</label>
              <Input type="number" step="0.1" v-model="formData.altura_estructura" placeholder="Ej. 45.0" class="text-xs" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-neutral-700 dark:text-neutral-300 uppercase tracking-wider text-[10px] mb-1">Código Transporte LPU</label>
              <Input v-model="formData.codigo_transporte_lpu" placeholder="Ej. 3042113" class="text-xs" />
            </div>
            <div>
              <label class="block font-bold text-neutral-700 dark:text-neutral-300 uppercase tracking-wider text-[10px] mb-1">Transporte Especial</label>
              <Input v-model="formData.transporte_especial" placeholder="Ej. MULA 2X150" class="text-xs" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-neutral-700 dark:text-neutral-300 uppercase tracking-wider text-[10px] mb-1">Supervisor Operativo Claro</label>
              <Input v-model="formData.supervisor_operativo" placeholder="Nombre completo" class="text-xs" />
            </div>
            <div>
              <label class="block font-bold text-neutral-700 dark:text-neutral-300 uppercase tracking-wider text-[10px] mb-1">Correo SO</label>
              <Input type="email" v-model="formData.correo_so" placeholder="ejemplo@claro.com.co" class="text-xs" />
            </div>
          </div>

          <div class="p-4 border-t border-neutral-100 dark:border-white/10 flex justify-end gap-2 -mx-6 -mb-6 bg-neutral-50/50 dark:bg-white/[0.02]">
            <Button variant="outline" size="sm" type="button" @click="emit('close')">
              Cancelar
            </Button>
            <Button size="sm" type="submit" :disabled="submitting" class="bg-primary text-white font-bold">
              Guardar Sitio
            </Button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

const username = ref('admin@doblex.com');
const password = ref('admin123');
const error = ref('');
const loading = ref(false);
const router = useRouter();

const handleLogin = async () => {
  loading.value = true;
  error.value = '';
  
  setTimeout(() => {
    if (username.value === 'admin@doblex.com' && password.value === 'admin123') {
      localStorage.setItem('smu_authenticated', 'true');
      localStorage.setItem('smu_username', 'Administrador Doblex');
      router.push({ name: 'dashboard' });
    } else {
      error.value = 'Credenciales de prueba inválidas. Use admin@doblex.com y admin123';
    }
    loading.value = false;
  }, 800);
};
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-[#0a0b10] bg-radial-at-c-login px-4 py-8">
    <div class="w-full max-w-[420px] rounded-xl border border-white/5 bg-neutral-900/60 backdrop-blur-xl p-8 shadow-2xl relative overflow-hidden transition-all duration-300 hover:shadow-primary/5">
      <!-- Decoración de fondo brillo rojo sutil -->
      <div class="absolute -top-24 -left-24 w-48 h-48 rounded-full bg-primary/10 blur-3xl pointer-events-none"></div>
      
      <div class="text-center mb-8 relative z-10">
        <div class="inline-flex items-center gap-2 bg-white/5 px-4 py-1.5 rounded-full border border-white/10 mb-4">
          <span class="text-primary text-sm filter drop-shadow-[0_0_8px_rgba(239,68,68,0.5)]">▲</span>
          <span class="font-semibold tracking-wider text-xs text-white">SMU DOBLEX</span>
        </div>
        <h1 class="text-2xl font-bold tracking-tight text-white mb-1">Gestión de Obra</h1>
        <p class="text-xs text-neutral-400">Sistema de Control y Asignación de Campo</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-4 relative z-10">
        <div class="space-y-2">
          <label class="text-xs font-semibold uppercase tracking-wider text-neutral-400" for="username">Usuario o Correo</label>
          <Input 
            type="email" 
            id="username" 
            v-model="username" 
            required 
            placeholder="admin@doblex.com"
            class="bg-neutral-950/40 border-white/10 text-white placeholder:text-neutral-500 focus-visible:ring-primary focus-visible:border-primary"
          />
        </div>

        <div class="space-y-2">
          <label class="text-xs font-semibold uppercase tracking-wider text-neutral-400" for="password">Contraseña</label>
          <Input 
            type="password" 
            id="password" 
            v-model="password" 
            required 
            placeholder="••••••••"
            class="bg-neutral-950/40 border-white/10 text-white placeholder:text-neutral-500 focus-visible:ring-primary focus-visible:border-primary"
          />
        </div>

        <div v-if="error" class="bg-red-500/10 border border-red-500/20 text-red-500 text-xs py-2 px-3 rounded-md text-center">
          {{ error }}
        </div>

        <Button type="submit" class="w-full bg-primary text-primary-foreground hover:bg-primary/90 mt-2 font-semibold tracking-wide" :disabled="loading">
          <span v-if="loading">Iniciando sesión...</span>
          <span v-else>Ingresar al Sistema</span>
        </Button>
      </form>

      <div class="text-center mt-8 relative z-10">
        <p class="text-[10px] text-neutral-500">&copy; 2026 DOBLEX. Todos los derechos reservados.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.bg-radial-at-c-login {
  background-image: radial-gradient(circle at 10% 20%, rgba(239, 68, 68, 0.05) 0%, transparent 40%),
                    radial-gradient(circle at 90% 80%, rgba(239, 68, 68, 0.03) 0%, transparent 40%),
                    linear-gradient(to bottom, #0a0b10, #030406);
}
</style>

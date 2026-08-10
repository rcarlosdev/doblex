import { createRouter, createWebHistory } from 'vue-router';
// Importamos las vistas directamente (lazy load puede hacerse después)
import LoginView from '../views/LoginView.vue';
import DashboardView from '../views/DashboardView.vue';
import OtsView from '../views/OtsView.vue';

const routes = [
    {
        path: '/login',
        name: 'login',
        component: LoginView,
        meta: { guestOnly: true }
    },
    {
        path: '/',
        name: 'dashboard',
        component: DashboardView,
        meta: { requiresAuth: true }
    },
    {
        path: '/ordenes-trabajo',
        name: 'ots',
        component: OtsView,
        meta: { requiresAuth: true }
    },
    // Redirección por defecto
    {
        path: '/:pathMatch(.*)*',
        redirect: '/'
    }
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
});

// Guard de navegación simple para verificar autenticación simulada
router.beforeEach((to, from, next) => {
    // Simulamos autenticación leyendo de localStorage temporalmente hasta integrar Pinia y la API
    const isAuthenticated = localStorage.getItem('smu_authenticated') === 'true';

    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!isAuthenticated) {
            next({ name: 'login' });
        } else {
            next();
        }
    } else if (to.matched.some(record => record.meta.guestOnly)) {
        if (isAuthenticated) {
            next({ name: 'dashboard' });
        } else {
            next();
        }
    } else {
        next();
    }
});

export default router;

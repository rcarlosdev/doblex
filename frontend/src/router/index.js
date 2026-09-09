import { createRouter, createWebHistory } from 'vue-router';
// Importamos las vistas directamente (lazy load puede hacerse después)
import LoginView from '../views/LoginView.vue';
import AppLayout from '../layouts/AppLayout.vue';
import DashboardView from '../views/DashboardView.vue';
import OtsView from '../views/OtsView.vue';
import EmpleadosView from '../views/EmpleadosView.vue';

const routes = [
    {
        path: '/login',
        name: 'login',
        component: LoginView,
        meta: { guestOnly: true }
    },
    {
        path: '/',
        component: AppLayout,
        meta: { requiresAuth: true },
        children: [
            {
                path: '',
                name: 'dashboard',
                component: DashboardView
            },
            {
                path: 'ordenes-trabajo',
                alias: ['ots', '/ots'],
                name: 'ots',
                component: OtsView
            },
            {
                path: 'empleados',
                name: 'empleados',
                component: EmpleadosView
            },
            {
                path: 'mobile/dashboard',
                name: 'mobile-dashboard',
                component: () => import('../views/mobile/TechDashboardView.vue')
            },
            {
                path: 'mobile/ot/:id',
                name: 'mobile-ot-detail',
                component: () => import('../views/mobile/TechOtDetailView.vue')
            }
        ]
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

// Guard de navegación para verificar autenticación y redirigir rol operativo a entorno móvil
router.beforeEach((to, from) => {
    const isAuthenticated = localStorage.getItem('smu_authenticated') === 'true';
    const userRole = localStorage.getItem('smu_role');

    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!isAuthenticated) {
            return { name: 'login' };
        }
        if (userRole === 'operativo' && ['dashboard', 'ots', 'empleados'].includes(to.name)) {
            // El módulo operativo es primariamente móvil
            return { name: 'mobile-dashboard' };
        }
        return true;
    }

    if (to.matched.some(record => record.meta.guestOnly)) {
        if (isAuthenticated) {
            if (userRole === 'operativo') {
                return { name: 'mobile-dashboard' };
            }
            return { name: 'dashboard' };
        }
        return true;
    }

    return true;
});

export default router;

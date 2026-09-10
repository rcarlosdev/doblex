import { createRouter, createWebHistory } from 'vue-router';
import { verifyRoleIntegrity } from '../lib/security';
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

// Guard de navegación seguro: verifica autenticación, integridad del token y control de acceso (RBAC)
router.beforeEach((to, from) => {
    const { isValid, role: userRole } = verifyRoleIntegrity();

    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!isValid) {
            return { name: 'login' };
        }
        if (userRole === 'operativo' && ['dashboard', 'ots', 'empleados'].includes(to.name)) {
            // El personal operativo es redirigido automáticamente a la interfaz de campo móvil
            return { name: 'mobile-dashboard' };
        }
        return true;
    }

    if (to.matched.some(record => record.meta.guestOnly)) {
        if (isValid) {
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


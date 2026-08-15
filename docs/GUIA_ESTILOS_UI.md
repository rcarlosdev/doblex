# Guía de Estilos UI/UX y Sistema de Diseño (SMU DOBLEX)

Este documento sirve como memoria técnica y manual de directrices visuales para garantizar que todos los módulos actuales y futuros (Dashboard, OTs, Perfil Operativo Móvil, Empleados, Logística y Finanzas) mantengan una estética homogénea, elegante y profesional.

---

## 1. Principios Fundamentales de Diseño

## 2. Paleta de Colores & Modo Oscuro Unificado (Onyx Theme)

Para mantener una experiencia estéticamente deslumbrante y coherente al 100% con la pantalla de inicio de sesión (Login):

- **Fondo Global Oscuro (App & Módulos):** `#0a0b10` / `dark:bg-[#0a0b10]` (`--background: 240 10% 4%`).
- **Tarjetas, Paneles y Navbar:** `#121215` / `dark:bg-[#121215]` (`--card: 240 6% 9%`) con bordes sutiles `border-white/10` o `border-neutral-800`.
- **Inputs & Contenedores Secundarios:** `dark:bg-[#0a0b10]` o `dark:bg-neutral-950/60` con `border-white/10`.
- **Color Principal de Acción (Shadcn Red):** `--primary: 346.8 77.2% 49.8%` (`#EF4444` / `bg-red-600` / `bg-primary`).
- **Queda Prohibido:** El uso de tonos azulados oscuros (`#141824`, `#1b2030` o `slate-900/950`) en nuevos componentes o vistas. Todos los módulos deben heredar la paleta Onyx pura del Login.) e íconos destacados deben utilizar exclusivamente el tono rojo de la marca Doblex.
   - Base de contraste apoyada en Slate/Neutral (`bg-slate-100 dark:bg-slate-950`, `bg-white dark:bg-slate-900`).
   - Interactividad táctil con animaciones de micro-interacción (`active:scale-95`, `transition-all duration-200`).

2. **Soporte Transversal Claro / Oscuro (Light / Dark Mode):**
   - Todos los componentes y vistas deben incluir variantes Tailwind CSS `dark:` para responder al tema del documento (`document.documentElement.classList.contains('dark')`).
   - La preferencia se persiste automáticamente en `localStorage.getItem('smu_theme')`.

3. **Enfoque Móvil-Primero (Mobile-First) en Campo:**
   - El módulo operativo ([/mobile/dashboard](file:///d:/DEV/CLIENTS/doblex/frontend/src/views/mobile/TechDashboardView.vue)) está diseñado para su utilización primaria en smartphones de los técnicos e ingenieros en sitio.

---

## 2. Estandarización de Iconografía (Uso Exclusivo de `@tabler/icons-vue`)

> [!IMPORTANT]
> **Regla de Iconografía:** Queda estrictamente prohibido el uso de emojis planos en texto (e.g. ☀️, 🌙, 🚪, 🏢, 📍, 🔄, 📋, 🚗, ✅) o SVGs inline ad-hoc. Toda la iconografía del sistema debe ser importada exclusivamente desde `@tabler/icons-vue`.

### Mapeo Oficial de Iconos:

| Función / Módulo | Icono Tabler Recomendado | Componente / Vista |
| :--- | :--- | :--- |
| **Dashboard Principal** | `<IconLayoutDashboard>` | `Sidebar.vue`, `Navbar.vue` |
| **Órdenes de Trabajo** | `<IconClipboardList>` | `Sidebar.vue`, `OtsView.vue` |
| **Gestión de Campo** | `<IconDeviceMobile>` | `Sidebar.vue`, `LoginView.vue` |
| **Gestión de Empleados** | `<IconUsers>` | `Sidebar.vue`, `EmpleadosView.vue` |
| **Filtro Todas** | `<IconListCheck>` | `TechDashboardView.vue` |
| **Filtro Emergencias (MEE)** | `<IconAlertTriangle>` | `TechDashboardView.vue` |
| **Filtro Preventivos (MP)** | `<IconShieldCheck>` | `TechDashboardView.vue` |
| **Filtro Correctivos (MC)** | `<IconTools>` | `TechDashboardView.vue` |
| **Filtro Solucionadas** | `<IconCircleCheck>` | `TechDashboardView.vue` |
| **Estación / Sitio Telecom** | `<IconBuildingBroadcastTower>` | `TechDashboardView.vue`, `TechOtDetailView.vue` |
| **Ubicación / GPS** | `<IconMapPin>`, `<IconMapPinCheck>` | `TechDashboardView.vue`, `PhotoUploader.vue` |
| **Flujo & Acción (Pestaña 1)**| `<IconSteeringWheel>` | `TechOtDetailView.vue` |
| **Minutograma PDT (Pestaña 2)**| `<IconActivity>` | `TechOtDetailView.vue` |
| **Evidencias (Pestaña 3)** | `<IconCamera>` | `TechOtDetailView.vue`, `PhotoUploader.vue` |
| **Repuestos LPU (Pestaña 4)** | `<IconBox>` | `TechOtDetailView.vue`, `CloseOtModal.vue` |
| **Checklist (Pestaña 5)** | `<IconListCheck>` | `TechOtDetailView.vue`, `DynamicChecklist.vue` |
| **Desplazamiento Técnico** | `<IconCar>` | `TechOtDetailView.vue` |
| **Actualizar / Recargar** | `<IconRefresh>` | `TechDashboardView.vue`, `TechOtDetailView.vue` |
| **Conmutador de Tema** | `<IconSun>`, `<IconMoon>` | `Navbar.vue` |
| **Cerrar Sesión** | `<IconLogout>` | `Navbar.vue` |

---

## 3. Reglas de Arquitectura Visual y No-Duplicidad de UI

1. **No Duplicar Controles ni Badges Globales en Vistas:**
   - La barra de navegación superior global ([Navbar.vue](file:///d:/DEV/CLIENTS/doblex/frontend/src/components/Navbar.vue)) contiene el conmutador de tema visual (Sol/Luna), las iniciales/nombre del perfil autenticado (`IC`, `OPERATIVO`) y el botón de salida (`Logout`).
   - Las vistas internas (`TechDashboardView.vue`, `TechOtDetailView.vue`) **no deben duplicar** el badge de perfil de usuario (`[OPERATIVO] Nombre`), el botón de tema ni el botón de salir dentro de sus encabezados de contenido.

2. **Diseño de Barras de Filtros y Navegación Segmentada:**
   - Utilizar contenedores redondeados tipo *segmented control* (`bg-slate-200/60 dark:bg-slate-900/80 p-1 rounded-2xl border border-slate-200/80 dark:border-slate-800`).
   - Cada pestaña o filtro activo utiliza el tema **Shadcn Red** (`bg-red-600 text-white shadow-md shadow-red-600/20`).

3. **Cuadrícula Responsiva Móvil (grid-cols-5 & shortLabel):**
   - Las barras de filtros y pestañas móviles deben organizarse en una cuadrícula de 5 columnas (`grid grid-cols-5 gap-1`).
   - Para adaptarse a pantallas estrechas de smartphones (< 640px), se deben utilizar etiquetas cortas (`shortLabel`): `Todas`, `MEE`, `MP`, `MC`, `Solución` en móvil, expandiéndose a títulos completos en pantallas mayores (`sm:`).

4. **Unificación de Formularios e Insumos en Modales (Single-Row Autocomplete):**
   - Queda prohibido duplicar controles desplegables (`<select>`) y cajas de entrada de texto (`<input>`) en la misma fila binding al mismo modelo.
   - Usar un único campo de texto inteligente con lista de sugerencias nativa (`<input list="catalog" v-model="...">` + `<datalist id="catalog">`), permitiendo seleccionar del catálogo LPU o ingresar descripciones personalizadas en 1 sola fila limpia.

5. **Insignias e Indicadores Multitema (Light & Dark Explicit Classes):**
   - Toda insignia o badge de estado (SLA, tipo de evidencia, subsistema) debe definir explícitamente sus clases para **Modo Claro** y **Modo Oscuro**.
   - Ejemplo: `bg-red-50 text-red-700 border-red-200 dark:bg-red-950/60 dark:text-red-300 dark:border-red-500/30`. Se prohíbe usar clases oscuras fijas (e.g. `bg-amber-950`) sin prefijo `dark:` ya que ensucian la interfaz en modo claro.

6. **Colores Semánticos de Estado (SLA & Mantenimiento):**
   - **Emergencia / MEE / Vencido:** Rose (`bg-rose-50 dark:bg-rose-950/60 text-rose-700 dark:text-rose-400 border-rose-200 dark:border-rose-500/50`).
   - **Correctivo / MC / Pendiente:** Amber (`bg-amber-50 dark:bg-amber-950/50 text-amber-800 dark:text-amber-300 border-amber-200 dark:border-amber-500/40`).
   - **Preventivo / MP / Asignada:** Red Shadcn (`bg-red-50 dark:bg-red-950/60 text-red-700 dark:text-red-400 border-red-200 dark:border-red-500/30`).
   - **Solucionada / Finalizada / Cumplido:** Emerald (`bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border-emerald-200 dark:border-emerald-500/30`).

7. **Teleport a Body para Modales y Superposiciones (`<Teleport to="body">`):**
   - Todo modal, diálogo emergente o lightbox de imagen debe envolver obligatoriamente su plantilla en `<Teleport to="body">`.
   - Esto evita que los contenedores hijos con scroll o trasformaciones contengan la posición `fixed inset-0 z-50 bg-black/60`, asegurando que el sombreado cubra el 100% de la ventana desde el píxel `0` superior sin dejar espacio blanco sobre el Navbar.

8. **Notificaciones y Mensajes de Feedback Visual al Usuario (Toast Alerts):**
   - Toda petición asíncrona a la API (cambio de estado, guardado de bitácora, carga de fotos o cierre de OT) debe proporcionar un aviso visual en pantalla (Toast Banner) indicando el resultado.
   - En caso de error (e.g. `HTTP 422 Unprocessable Content`), se debe capturar `err.response?.data?.message` y mostrarlo explícitamente en tono rojo (`bg-rose-50 dark:bg-rose-950/90 text-rose-950 dark:text-rose-100 border-rose-300 dark:border-rose-700`) tanto en el banner de notificación como dentro de la tarjeta de error del modal activo.

9. **Confirmación Previa Obligatoria en Acciones de Guardado o Finalización (`ConfirmDialogModal`):**
   - Todo evento de guardado, envío de evidencias, actualización de estado o finalización técnica de módulo debe requerir confirmación explícita mediante el componente `<ConfirmDialogModal>`.
   - El diálogo de confirmación debe detallar el título de la acción, una breve explicación de las consecuencias y botones de acción rápida (*"Sí, Confirmar" / "Cancelar"*).

---

## 4. Control de Acceso en Navegación (Sidebar)

- Los módulos visibles en [Sidebar.vue](file:///d:/DEV/CLIENTS/doblex/frontend/src/components/Sidebar.vue) deben responder a la propiedad computada `menuItems` evaluada contra `localStorage.getItem('smu_role')`.
- El perfil `operativo` solo tiene permitido visualizar **Gestión de Campo**, manteniendo una barra lateral limpia y enfocada en su labor técnica.



# Plan de Implementación: Sistema de Gestión de Obra Civil (SMU DOBLEX)

Este documento detalla el plan de implementación para el desarrollo a la medida del **Sistema de Gestión de Obra Civil (SMU DOBLEX)**, estructurado bajo la modalidad de fases e hitos funcionales con entregas progresivas de acuerdo con la **Propuesta Comercial Oficial (`docs/Propuesta_app_doblex.docx`)**.

---

## 1. Stack Tecnológico Elegido

* **Backend:** **Laravel 11** (Framework de PHP de alto rendimiento para APIs RESTful seguras, arquitectura limpia y manejo eficiente de lógica transaccional).
* **Frontend:** **Vue.js 3** + **TailwindCSS** + **Vite** (Interfaz de usuario reactiva, moderna, adaptativa en modo Claro/Oscuro y optimizada para dispositivos de campo y escritorio).
* **Base de Datos:** **PostgreSQL 16** (Sistema de gestión de bases de datos relacionales, robusto y altamente eficiente para la integridad transaccional).

---

## 2. Alcance y Estructura de Fases

El desarrollo se divide en **5 fases secuenciales**, diseñadas para permitir validaciones progresivas y mitigar riesgos en la implementación.

### Fase 1: Configuración Base, Núcleo Operativo y Gestión de Personal (En Desarrollo)
* **Objetivo:** Establecer la arquitectura del backend y frontend, desarrollar la base operativa de control de trabajo en campo y la gestión maestro de empleados/cuadrillas.
* **Entregables:**
  * Diseño de arquitectura de software y Base de Datos relacional en PostgreSQL.
  * **Módulo 1:** Creación y Control de Órdenes de Trabajo (OT) y Actividades.
  * **Módulo 2:** Seguimiento de Actividades en campo (Avances, reportes, novedades).
  * **Módulo 7 (Base):** Gestión Base de Empleados (Registro maestro, roles, perfiles y asignación a cuadrillas/obras).
* **Tiempo Estimado:** 5 semanas.
* **Fecha de Entrega Estimada:** 12 de Septiembre de 2026.

### Fase 2: Logística y Recursos
* **Objetivo:** Controlar los materiales, equipos y la flota de vehículos necesarios para la ejecución de las obras.
* **Entregables:**
  * **Módulo 5:** Logística (Gestión de inventario de Materiales y Equipos).
  * **Módulo 6:** Vehículos y Transporte (Asignación, mantenimiento básico).
  * *Nota: A partir de esta fase se habilitará el entorno de pruebas (Staging) para validaciones continuas.*
* **Tiempo Estimado:** 4 semanas.
* **Fecha de Entrega Estimada:** 10 de Octubre de 2026.

### Fase 3: Finanzas y Viáticos
* **Objetivo:** Facilitar la gestión de gastos de viaje, solicitudes de viáticos y legalizaciones con facturas del personal en obra.
* **Entregables:**
  * **Módulo 4:** Viáticos (Solicitud, aprobación por administración y legalización).
* **Tiempo Estimado:** 5 semanas.
* **Fecha de Entrega Estimada:** 14 de Noviembre de 2026.

### Fase 4: Módulos Corporativos Avanzados y Control
* **Objetivo:** Centralizar la seguridad y salud en el trabajo (SST), la gestión documental jurídica y la visualización de métricas analíticas globales.
* **Entregables:**
  * **Módulo 8:** SST (Registro de incidentes, control de dotación y EPP vinculado a empleados).
  * **Módulo 9:** Jurídica (Repositorio y control de contratos de obra, pólizas con alertas de vencimiento).
  * **Módulo 3:** Dashboard de KPIs (Indicadores de rendimiento generales del sistema consumiendo las APIs).
* **Tiempo Estimado:** 6 semanas.
* **Fecha de Entrega Estimada:** 26 de Diciembre de 2026.

### Fase 5: Pruebas, Ajustes y Despliegue Final
* **Objetivo:** Pruebas integrales de extremo a extremo, optimización del paquete cliente, ajustes de experiencia de usuario y despliegue final en servidor VPS.
* **Tiempo Estimado:** 2 semanas.
* **Fecha de Entrega Estimada:** 9 de Enero de 2027.

---

## 3. Cronograma y Fechas de Entrega

El proyecto completo está proyectado para ejecutarse en **22 semanas (~5.5 meses)**:

| Hito / Fase | Duración | Fecha de Entrega Estimada |
| :--- | :---: | :---: |
| **Inicio del Proyecto** | — | 8 de Agosto de 2026 |
| **Fase 1: Base, OT y Empleados** | 5 semanas | 12 de Septiembre de 2026 |
| **Fase 2: Logística y Vehículos** | 4 semanas | 10 de Octubre de 2026 |
| **Fase 3: Viáticos y Finanzas** | 5 semanas | 14 de Noviembre de 2026 |
| **Fase 4: SST, Jurídica y KPIs** | 6 semanas | 26 de Diciembre de 2026 |
| **Fase 5: Pruebas y Despliegue Final** | 2 semanas | 9 de Enero de 2027 |
| **TOTAL ESTIMADO** | **22 semanas** | **9 de Enero de 2027** |

---

## 4. Presupuesto y Condiciones de Pago

* **Costo Total de Desarrollo (MVP):** **$33,000,000 COP**

### Estructura de Pagos por Hitos
1. **20% de Anticipo ($6,600,000 COP):** Firma del acuerdo e inicio de arquitectura.
2. **20% Fase 1 ($6,600,000 COP):** Entrega y validación de Base, OT y Empleados.
3. **20% Fase 2 ($6,600,000 COP):** Entrega y validación de Logística y Vehículos.
4. **20% Fase 3 ($6,600,000 COP):** Entrega y validación de Viáticos.
5. **20% Fase 4 y Final ($6,600,000 COP):** SST, Jurídica, KPIs y paso a producción en VPS.

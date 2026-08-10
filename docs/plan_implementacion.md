# Plan de Implementación: Sistema de Gestión de Obra Civil (SMU)

Este documento detalla el plan de implementación para el desarrollo a la medida del **Sistema de Gestión de Obra Civil (SMU)**, estructurado bajo la modalidad de fases e hitos funcionales con entregas progresivas.

---

## 1. Stack Tecnológico Elegido

Para garantizar la robustez, escalabilidad y mantenibilidad del sistema, se ha seleccionado el siguiente stack de desarrollo:

* **Backend:** **Laravel** (Framework de PHP de alto rendimiento, ideal para estructurar APIs REST seguras y manejar la lógica de negocio).
* **Frontend:** **Vue.js** (Framework de JavaScript progresivo para una interfaz de usuario reactiva, moderna y de alto rendimiento).
* **Base de Datos:** **PostgreSQL** (Sistema de gestión de bases de datos relacionales, robusto y altamente eficiente para la integridad de datos transaccionales y de georreferenciación si se requiere en el campo).

---

## 2. Alcance y Estructura de Fases

El desarrollo se divide en **5 fases secuenciales**, diseñadas para permitir validaciones progresivas y mitigar riesgos en la implementación.

### Fase 1: Configuración Base y Núcleo Operativo (El "Baseline")
* **Objetivo:** Establecer la arquitectura del backend y frontend, y desarrollar la base operativa de asignación y control de trabajo.
* **Entregables:**
  * Diseño de arquitectura de software (Laravel API + Vue.js Frontend) y Base de Datos relacional en PostgreSQL.
  * **Módulo 1:** Creación y Control de Órdenes de Trabajo (OT) y Actividades.
  * **Módulo 2:** Seguimiento de Actividades en campo.
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

### Fase 3: Finanzas y Facturación
* **Objetivo:** Facilitar la gestión de gastos de viaje y reembolsos del personal en obra.
* **Entregables:**
  * **Módulo 4:** Viáticos (Solicitud, aprobación y legalización).
* **Tiempo Estimado:** 5 semanas.
* **Fecha de Entrega Estimada:** 14 de Noviembre de 2026.

### Fase 4: Módulos Corporativos y Control
* **Objetivo:** Centralizar el talento humano, el control de seguridad y salud, la gestión documental jurídica y la visualización de métricas críticas en un panel centralizado.
* **Entregables:**
  * **Módulo 7:** Gestión Humana (Perfiles, asignación a obras).
  * **Módulo 8:** SST (Registro de incidentes, control de dotación).
  * **Módulo 9:** Jurídica (Repositorio y control de contratos, pólizas).
  * **Módulo 3:** Dashboard de KPIs (Indicadores de rendimiento generales del sistema consumiendo las APIs de Laravel).
* **Tiempo Estimado:** 6 semanas.
* **Fecha de Entrega Estimada:** 26 de Diciembre de 2026.

### Fase 5: Pruebas, Ajustes y Despliegue Final
* **Objetivo:** Realizar pruebas integrales de extremo a extremo, optimización del bundle de Vue.js, ajustes finales y despliegue inicial en producción.
* **Tiempo Estimado:** 2 semanas.
* **Fecha de Entrega Estimada:** 9 de Enero de 2027.

---

## 3. Cronograma y Fechas de Entrega

El proyecto completo está proyectado para ejecutarse en un lapso de **22 semanas (~5.5 meses)**:

| Hito / Fase | Duración | Fecha de Entrega Estimada |
| :--- | :---: | :---: |
| **Inicio del Proyecto** | — | 8 de Agosto de 2026 |
| **Fase 1: Base y OT** | 5 semanas | 12 de Septiembre de 2026 |
| **Fase 2: Logística y Vehículos** | 4 semanas | 10 de Octubre de 2026 |
| **Fase 3: Viáticos y Facturación** | 5 semanas | 14 de Noviembre de 2026 |
| **Fase 4: RRHH, SST, Jurídica y KPIs** | 6 semanas | 26 de Diciembre de 2026 |
| **Fase 5: Pruebas, Ajustes y Despliegue** | 2 semanas | 9 de Enero de 2027 |
| **TOTAL ESTIMADO** | **22 semanas** | **9 de Enero de 2027** |

---

## 4. Presupuesto y Condiciones de Pago

El costo total de desarrollo corresponde al MVP (Producto Mínimo Viable) completamente funcional:

* **Costo Total de Desarrollo:** **$33,000,000 COP**
* *Nota: Excluye costos de adquisición/arrendamiento del VPS, dominios, certificados SSL pagos u otros servicios de terceros, los cuales serán asumidos por el cliente.*

### Plan de Pagos (Estructura de Hitos)
Los pagos se realizarán contra entrega y validación de cada hito:

1. **20% de Anticipo ($6,600,000 COP):** Al firmar el acuerdo e iniciar el diseño de arquitectura.
2. **20% a la Entrega de la Fase 1 ($6,600,000 COP):** Validación de Base y OT.
3. **20% a la Entrega de la Fase 2 ($6,600,000 COP):** Validación de Logística y Vehículos.
4. **20% a la Entrega de la Fase 3 ($6,600,000 COP):** Validación de Viáticos.
5. **20% a la Entrega Final ($6,600,000 COP):** Fase 4, pruebas integrales y paso a producción en el VPS.

### Opción Alternativa: Contratación de Piloto (Fase 1 únicamente)
* Si se desea validar únicamente el primer hito como prueba de concepto:
  * **Costo Proyecto Independiente:** **$7,500,000 COP** (incluye recargo por diseño de arquitectura inicial independiente).
  * Si se decide continuar con las siguientes fases tras el piloto, estas retomarían su valor estándar de **$6,600,000 COP** cada una.

---

## 5. Estrategia de Despliegue e Infraestructura (VPS)

Para maximizar el rendimiento y el control sobre la plataforma, el despliegue se realizará bajo el siguiente esquema:

* **Entorno de Servidor:** Servidor Virtual Privado (VPS) con sistema operativo Linux (Ubuntu Server LTS recomendado). El proveedor específico de VPS está pendiente de definición por el cliente (ej. DigitalOcean, AWS Lightsail, Linode, Hetzner, etc.).
* **Servidor Web:** Nginx o Apache configurado para servir la aplicación Vue.js compilada como estática y direccionar las solicitudes `/api` al backend de Laravel mediante PHP-FPM.
* **Base de Datos:** Instancia local o remota de PostgreSQL optimizada para la escala del proyecto.
* **Seguridad:** Certificado SSL (Let's Encrypt o similar) para encriptación HTTPS de todo el tráfico, configuración de firewall básico (UFW) y aislamiento de puertos sensibles.
* **Entorno de Pruebas (Staging):** A partir de la Fase 2, se habilitará un subdominio o puerto de pruebas en el VPS (o un VPS de menor escala de pruebas) para validación progresiva por parte del cliente antes de los despliegues de producción.

---

## 6. Metodología de Entrega por Fases y Proceso de Aceptación

Para asegurar que cada módulo cumpla rigurosamente con los requisitos acordados y que el cliente tenga visibilidad y control absoluto, el desarrollo se ejecutará bajo el siguiente flujo metodológico estricto para cada fase:

1. **Desarrollo y Pruebas Internas:**
   * El equipo realiza el diseño y codificación del backend (Laravel) y frontend (Vue.js) de los módulos correspondientes a la fase actual.
   * Se realizan pruebas automáticas y manuales previas al despliegue.

2. **Despliegue en Entorno de Pruebas (Staging):**
   * Al finalizar el tiempo estimado de la fase, el código estable se desplegará en el entorno de pruebas en el VPS.
   * Se entregará un enlace de acceso exclusivo y credenciales de prueba al cliente.

3. **Período de Validación (UAT - User Acceptance Testing):**
   * El cliente dispondrá de un período de **5 a 7 días hábiles** para interactuar con la plataforma en el VPS de pruebas, registrar datos reales y validar las funcionalidades entregadas.

4. **Iteración de Ajustes y Corrección de Bugs:**
   * En caso de encontrarse errores (bugs) o desviaciones respecto al alcance definido para la fase, el equipo de desarrollo priorizará su resolución inmediata sin costos adicionales.

5. **Cierre de Fase y Pago:**
   * Una vez validadas y aprobadas todas las funcionalidades correspondientes, se firmará un acta de conformidad de fase (o aceptación escrita).
   * Esta firma autoriza la liberación del **20% de pago correspondiente a la fase entregada** y da inicio formal al cronograma y desarrollo de la fase subsiguiente.

6. **Acumulación de Cambios Estables:**
   * Los entregables de la fase aprobada permanecen estables y listos, sirviendo de base directa para los módulos de las siguientes fases, minimizando riesgos de regresión.

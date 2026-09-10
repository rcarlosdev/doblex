# Protocolos de Inspección Técnica en Campo (Resguardo para Futura Implementación)

Este directorio resguarda los componentes de formularios y protocolos de inspección técnica especializada que fueron retirados de la vista operativa de OTs actual, dado que corresponden a otro tipo de trabajos específicos para los cuales aún está pendiente recibir la documentación técnica oficial.

## Componentes Resguardados

1. **`DynamicChecklist.vue`**:
   - Contenedor dinámico y consolidador de porcentaje de cumplimiento de protocolos.
   - Pestañas conmutables para SPT, GE 360, AIRES AA y FUERZA DC.
   - Tareas y criterios normativos (celda amarilla de entrada, verde de criterio norma).

2. **`SptInspectionProtocol.vue` (SPT - Puesta a Tierra)**:
   - Protocolo de medición de resistencia de puesta a tierra.
   - Mediciones con método Wenner / Telurómetro (separación de picas, resistividad aparente).
   - Inspección de barra colectora BEP, bajantes pararrayos y uniones exotérmicas Cadweld.

3. **`GeInspectionProtocol.vue` (GE 360 - Planta Eléctrica)**:
   - Protocolo integral para Grupo Electrógeno y ATS.
   - Pruebas de aislamiento Megger (bobinados estator/rotor en Megaohmios).
   - Banco de carga resistivo, pruebas en vacío y bajo carga, tiempos de transferencia.

4. **`AaInspectionProtocol.vue` (AIRES AA - Climatización y Refrigeración)**:
   - Inspección de circuitos frigoríficos, presiones manométricas baja y alta.
   - Sobrecalentamiento y subenfriamiento, corriente de compresor y motores ventiladores.

5. **`PowerInspectionProtocol.vue` (FUERZA DC - Rectificadores y Baterías)**:
   - Medición de rizado AC en barraje DC, voltaje de flotación e igualación.
   - Capacidad y conductancia de bancos de baterías estacionarias (VRLA/OPzV).

## Instrucciones para Futura Activación

Cuando se cuente con los formatos oficiales y procedimientos para estos trabajos especializados, estos componentes pueden reactivarse importándolos directamente en la vista correspondiente o en un módulo dedicado de inspecciones periódicas de subestaciones.

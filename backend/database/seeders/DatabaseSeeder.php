<?php

namespace Database\Seeders;

use App\Models\User;
use App\Models\Empleado;
use App\Models\Cuadrilla;
use App\Models\Ot;
use App\Models\EvidenciaFotografica;
use App\Models\Avance;
use App\Models\RepuestoUtilizado;
use App\Models\ActividadOt;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     * Ejemplos tipificados para las 4 zonas operativas:
     * - Antioquia (Apartadó, Medellín, Titiribí)
     * - Chocó (Quibdó, Cantón de San Pablo)
     * - Córdoba (Montería, Cereté)
     * - Atlántico (Barranquilla, Soledad)
     */
    public function run(): void
    {
        // 1. Usuarios del Sistema (Roles Administrativos y Operativos)
        $admin = User::create([
            'name' => 'Admin General',
            'username' => 'admin.doblex',
            'email' => 'admin@doblex.com',
            'role' => 'admin',
            'password' => Hash::make('admin123'),
        ]);

        $adminis = User::create([
            'name' => 'Auxiliar Técnico',
            'username' => 'adminis.doblex',
            'email' => 'adminis@doblex.com',
            'role' => 'administrativo',
            'password' => Hash::make('adminis123'),
        ]);

        $carlos = User::create([
            'name' => 'Ing. Carlos Pérez',
            'username' => 'carlos.doblex',
            'email' => 'carlos@doblex.com',
            'role' => 'operativo',
            'password' => Hash::make('operador123'),
        ]);

        $luis = User::create([
            'name' => 'Ing. Luis Martínez',
            'username' => 'luis.doblex',
            'email' => 'luis@doblex.com',
            'role' => 'operativo',
            'password' => Hash::make('operador123'),
        ]);

        $jasmin = User::create([
            'name' => 'Jasmin Ariel Mosquera',
            'username' => 'jasmin.doblex',
            'email' => 'jasmin@doblex.com',
            'role' => 'operativo',
            'password' => Hash::make('operador123'),
        ]);

        $eliseo = User::create([
            'name' => 'Eliseo Smith Granados',
            'username' => 'eliseo.doblex',
            'email' => 'eliseo@doblex.com',
            'role' => 'operativo',
            'password' => Hash::make('operador123'),
        ]);

        // 2. Cuadrillas Regionales según Documentación Operativa
        $cuadrillaAntioquia = Cuadrilla::create([
            'nombre' => 'Cuadrilla Regional Antioquia & Urabá',
            'especialidad' => 'Grupos Electrógenos GE/ATS & Mantenimiento Integral',
            'lider_id' => $carlos->id,
        ]);

        $cuadrillaChoco = Cuadrilla::create([
            'nombre' => 'Cuadrilla Regional Chocó',
            'especialidad' => 'Sistemas Híbridos SFV & Redes Aisladas ZNI',
            'lider_id' => $jasmin->id,
        ]);

        $cuadrillaCordoba = Cuadrilla::create([
            'nombre' => 'Cuadrilla Regional Córdoba',
            'especialidad' => 'Climatización de Precisión & Fuerza DC',
            'lider_id' => $carlos->id,
        ]);

        $cuadrillaAtlantico = Cuadrilla::create([
            'nombre' => 'Cuadrilla Regional Atlántico',
            'especialidad' => 'Media Tensión, Subestaciones & Balizamiento en Altura',
            'lider_id' => $eliseo->id,
        ]);

        // 3. Empleados / Registro Maestro de Personal (Directorio Oficial)
        Empleado::create([
            'documento' => '1090887123',
            'nombre' => 'Admin General',
            'cargo' => 'Director General de Obra',
            'telefono' => '3001234567',
            'email' => 'admin@doblex.com',
            'rol' => 'admin',
            'user_id' => $admin->id,
            'estado' => 'activo',
        ]);

        Empleado::create([
            'documento' => '1090887456',
            'nombre' => 'Auxiliar Técnico',
            'cargo' => 'Asistente Administrativo de Campo',
            'telefono' => '3109876543',
            'email' => 'adminis@doblex.com',
            'rol' => 'administrativo',
            'user_id' => $adminis->id,
            'estado' => 'activo',
        ]);

        // Antioquia
        Empleado::create([
            'documento' => '1018445990',
            'nombre' => 'Ing. Carlos Pérez',
            'cargo' => 'Ingeniero Residente Electromecánico',
            'telefono' => '3157778899',
            'email' => 'carlos@doblex.com',
            'rol' => 'operativo',
            'cuadrilla_id' => $cuadrillaAntioquia->id,
            'user_id' => $carlos->id,
            'estado' => 'activo',
        ]);

        Empleado::create([
            'documento' => '71175427',
            'nombre' => 'Julián Alexander Rivillas Meneses',
            'cargo' => 'Técnico Integral (Medellín-Urabá)',
            'telefono' => '3114567890',
            'email' => 'julian.rivillas@doblex.com',
            'rol' => 'operativo',
            'cuadrilla_id' => $cuadrillaAntioquia->id,
            'estado' => 'activo',
        ]);

        Empleado::create([
            'documento' => '8167017',
            'nombre' => 'Manuel Francisco Tapias Urango',
            'cargo' => 'Técnico Electromecánico (Urabá)',
            'telefono' => '3145678901',
            'email' => 'manuel.tapias@doblex.com',
            'rol' => 'operativo',
            'cuadrilla_id' => $cuadrillaAntioquia->id,
            'estado' => 'activo',
        ]);

        // Chocó
        Empleado::create([
            'documento' => '8336030',
            'nombre' => 'Jasmin Ariel Mosquera Rosero',
            'cargo' => 'Técnico Electromecánico (Chocó)',
            'telefono' => '3216549870',
            'email' => 'jasmin@doblex.com',
            'rol' => 'operativo',
            'cuadrilla_id' => $cuadrillaChoco->id,
            'user_id' => $jasmin->id,
            'estado' => 'activo',
        ]);

        Empleado::create([
            'documento' => '1077173308',
            'nombre' => 'Carlos Rafael Lozano Hinestroza',
            'cargo' => 'Técnico Transmisión (Chocó)',
            'telefono' => '3108765432',
            'email' => 'carlos.lozano@doblex.com',
            'rol' => 'operativo',
            'cuadrilla_id' => $cuadrillaChoco->id,
            'estado' => 'activo',
        ]);

        // Córdoba
        Empleado::create([
            'documento' => '78705371',
            'nombre' => 'Ancízar Manuel Pérez Ortiz',
            'cargo' => 'Técnico Electricista (Córdoba)',
            'telefono' => '3137894561',
            'email' => 'ancizar.perez@doblex.com',
            'rol' => 'operativo',
            'cuadrilla_id' => $cuadrillaCordoba->id,
            'estado' => 'activo',
        ]);

        Empleado::create([
            'documento' => '94466010',
            'nombre' => 'Ramón Elías Yepes Jaramillo',
            'cargo' => 'Técnico Electromecánico (Córdoba)',
            'telefono' => '3123456789',
            'email' => 'ramon.yepes@doblex.com',
            'rol' => 'operativo',
            'cuadrilla_id' => $cuadrillaCordoba->id,
            'estado' => 'activo',
        ]);

        // Atlántico
        Empleado::create([
            'documento' => '8567519',
            'nombre' => 'Eliseo Smith Granados Vanegas',
            'cargo' => 'Técnico Electricista (Barranquilla)',
            'telefono' => '3012345678',
            'email' => 'eliseo@doblex.com',
            'rol' => 'operativo',
            'cuadrilla_id' => $cuadrillaAtlantico->id,
            'user_id' => $eliseo->id,
            'estado' => 'activo',
        ]);

        Empleado::create([
            'documento' => '1018445112',
            'nombre' => 'Ing. Luis Martínez',
            'cargo' => 'Ingeniero de Energía y Climatización',
            'telefono' => '3186665544',
            'email' => 'luis@doblex.com',
            'rol' => 'operativo',
            'cuadrilla_id' => $cuadrillaAtlantico->id,
            'user_id' => $luis->id,
            'estado' => 'activo',
        ]);

        // 4. Órdenes de Trabajo (OT) con Ciudades de la Documentación

        // --- ANTIOQUIA (Apartadó - Urabá) ---
        $otAntioquia = Ot::create([
            'codigo' => 'OT-2026-101',
            'descripcion' => 'Mantenimiento Correctivo GE/ATS - Diagnóstico de Tarjeta AVR y Reparación de Aislamientos en Bobinado de Generador Stamford',
            'sitio' => 'ANT.APARTADO - EB Apartadó Centro (ANT-028)',
            'ubicacion' => 'Cra. 100 # 98-45, Apartadó, Antioquia',
            'created_by' => $admin->id,
            'user_id' => $carlos->id,
            'cuadrilla_id' => $cuadrillaAntioquia->id,
            'prioridad' => 'P1',
            'tipo_ubicacion' => 'urbana',
            'tipo_mantenimiento' => 'correctivo',
            'subsistema' => 'Movil Plantas Eléctricas',
            'tipo_gasto' => 'OPEX',
            'progreso' => 15,
            'estado' => 'asignada',
            'fecha_inicio' => '2026-08-14 08:00:00',
            'fecha_limite_sla' => '2026-08-15 18:00:00',
        ]);

        // --- CHOCÓ (Cantón de San Pablo / ZNI Atrato) ---
        $otChoco = Ot::create([
            'codigo' => 'OT-2026-102',
            'descripcion' => 'Mantenimiento de Emergencia Híbrido SFV & Power DC - Falla en Inversor y Banco de Baterías de Repetidora ZNI',
            'sitio' => 'CHO.CANTON DE SAN PABLO - EB Managrú (CHO-014)',
            'ubicacion' => 'Sector Río Atrato, Cantón de San Pablo, Chocó',
            'created_by' => $adminis->id,
            'user_id' => $jasmin->id,
            'cuadrilla_id' => $cuadrillaChoco->id,
            'prioridad' => 'P1',
            'tipo_ubicacion' => 'rural',
            'tipo_mantenimiento' => 'emergencia',
            'subsistema' => 'Móvil Híbridos SFV',
            'tipo_gasto' => 'OPEX',
            'progreso' => 35,
            'estado' => 'en_camino',
            'fecha_inicio' => '2026-08-14 10:00:00',
            'fecha_limite_sla' => '2026-08-15 06:00:00',
        ]);

        // --- CÓRDOBA (Montería) ---
        $otCordoba = Ot::create([
            'codigo' => 'OT-2026-103',
            'descripcion' => 'Mantenimiento Preventivo & Climatización AA Móvil - Servicio a Compresores y Condensadoras de Precisión en Shelter de Transmisión',
            'sitio' => 'COR.MONTERIA - EB Ronda del Sinú (MON-019)',
            'ubicacion' => 'Calle 27 # 4-50, Centro, Montería, Córdoba',
            'created_by' => $adminis->id,
            'user_id' => $carlos->id,
            'cuadrilla_id' => $cuadrillaCordoba->id,
            'prioridad' => 'P2',
            'tipo_ubicacion' => 'urbana',
            'tipo_mantenimiento' => 'preventivo',
            'subsistema' => 'Movil Aires Acondicionados',
            'tipo_gasto' => 'OPEX',
            'progreso' => 65,
            'estado' => 'en_sitio',
            'fecha_inicio' => '2026-08-14 13:00:00',
            'fecha_limite_sla' => '2026-08-15 17:00:00',
            'fecha_llegada_sitio' => '2026-08-14 14:15:00',
        ]);

        // --- ATLÁNTICO (Barranquilla) ---
        $otAtlantico = Ot::create([
            'codigo' => 'OT-2026-104',
            'descripcion' => 'Mantenimiento en Altura y Media Tensión - Retorque de Pernería en Torre de 45m, Balizamiento y Medición de Resistencia de Puesta a Tierra (SPT)',
            'sitio' => 'ATL.BARRANQUILLA - EB Riomar Industrial (BQ-042)',
            'ubicacion' => 'Vía 40 # 76-12, Barranquilla, Atlántico',
            'created_by' => $admin->id,
            'user_id' => $eliseo->id,
            'cuadrilla_id' => $cuadrillaAtlantico->id,
            'prioridad' => 'P3',
            'tipo_ubicacion' => 'urbana',
            'tipo_mantenimiento' => 'preventivo',
            'subsistema' => 'Movil Sistema Eléctrico',
            'tipo_gasto' => 'CAPEX',
            'progreso' => 100,
            'estado' => 'solucionada',
            'fecha_inicio' => '2026-08-10 08:00:00',
            'fecha_limite_sla' => '2026-08-12 18:00:00',
            'fecha_llegada_sitio' => '2026-08-10 09:30:00',
            'fecha_solucion' => '2026-08-10 16:45:00',
            'causa_falla' => 'desgaste',
            'observaciones_cierre' => 'Inspección de SPT con telurómetro arrojando 3.8 Ohms. Se aplicó pintura anticorrosiva epóxica y torque de pernería según protocolo de torre.',
        ]);

        // --- ANTIOQUIA (Titiribí - Suroeste Antioqueño) ---
        $otTitiribi = Ot::create([
            'codigo' => 'OT-2026-105',
            'descripcion' => 'Mantenimiento Preventivo Integral de Acceso & Enlace de Transmisión PTP de Microondas',
            'sitio' => 'ANT.TITIRIBI LA ALBANIA - EB La Albania (ANT-072)',
            'ubicacion' => 'Vereda La Albania, Titiribí, Antioquia',
            'created_by' => $admin->id,
            'user_id' => $luis->id,
            'cuadrilla_id' => $cuadrillaAntioquia->id,
            'prioridad' => 'P2',
            'tipo_ubicacion' => 'rural',
            'tipo_mantenimiento' => 'preventivo',
            'subsistema' => 'Móvil Acceso-Transmisión',
            'tipo_gasto' => 'OPEX',
            'progreso' => 100,
            'estado' => 'finalizada',
            'fecha_inicio' => '2026-08-08 07:00:00',
            'fecha_limite_sla' => '2026-08-09 18:00:00',
            'fecha_llegada_sitio' => '2026-08-08 09:00:00',
            'fecha_solucion' => '2026-08-08 17:00:00',
            'causa_falla' => 'desgaste',
            'observaciones_cierre' => 'Alineación de antenas parabólicas de 0.6m, sellado de conectores Heliax y prueba de tasa de error de transmisión aprobada.',
        ]);

        // 5. Evidencias Fotográficas con Georreferenciación Real (Atlántico - Barranquilla)
        EvidenciaFotografica::create([
            'ot_id' => $otAtlantico->id,
            'tipo' => 'antes',
            'url_imagen' => 'https://images.unsplash.com/photo-1541888946425-d0fbb186f5f8?w=800',
            'latitud' => 11.01825400,
            'longitud' => -74.82142000,
            'fecha_hora_captura' => '2026-08-10 09:45:00',
        ]);

        EvidenciaFotografica::create([
            'ot_id' => $otAtlantico->id,
            'tipo' => 'durante',
            'url_imagen' => 'https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800',
            'latitud' => 11.01827000,
            'longitud' => -74.82141500,
            'fecha_hora_captura' => '2026-08-10 13:15:00',
        ]);

        EvidenciaFotografica::create([
            'ot_id' => $otAtlantico->id,
            'tipo' => 'despues',
            'url_imagen' => 'https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800',
            'latitud' => 11.01826000,
            'longitud' => -74.82141000,
            'fecha_hora_captura' => '2026-08-10 16:30:00',
        ]);

        // 6. Repuestos / Insumos LPU Utilizados
        RepuestoUtilizado::create([
            'ot_id' => $otAtlantico->id,
            'nombre_item' => 'Pintura Epóxica Balizamiento Naranja Aeronáutico',
            'cantidad' => 2.00,
            'unidad_medida' => 'Galón',
        ]);

        RepuestoUtilizado::create([
            'ot_id' => $otAtlantico->id,
            'nombre_item' => 'Tornillería Galvanizada de Alta Resistencia A325 5/8" x 2"',
            'cantidad' => 24.00,
            'unidad_medida' => 'Unidad',
        ]);

        RepuestoUtilizado::create([
            'ot_id' => $otAtlantico->id,
            'nombre_item' => 'Cartucho Soldadura Exotérmica Cadweld 90g',
            'cantidad' => 4.00,
            'unidad_medida' => 'Unidad',
        ]);

        RepuestoUtilizado::create([
            'ot_id' => $otCordoba->id,
            'nombre_item' => 'Gas Refrigerante Ecológico R410A',
            'cantidad' => 3.50,
            'unidad_medida' => 'Kg',
        ]);

        RepuestoUtilizado::create([
            'ot_id' => $otCordoba->id,
            'nombre_item' => 'Filtro Secador Deshidratador 3/8 Soldable',
            'cantidad' => 2.00,
            'unidad_medida' => 'Unidad',
        ]);

        // 7. Bitácora de Campo (Historial de Avances PDT)
        Avance::create([
            'ot_id' => $otAtlantico->id,
            'user_id' => $eliseo->id,
            'descripcion' => 'Llegada a sitio EB Riomar Industrial. Inspección de riesgos y charla de seguridad SST de 5 minutos.',
            'porcentaje' => 20,
            'fecha_reporte' => '2026-08-10 09:40:00',
        ]);

        Avance::create([
            'ot_id' => $otAtlantico->id,
            'user_id' => $eliseo->id,
            'descripcion' => 'Ascenso seguro con arnés dieléctrico y doble eslinga. Retorque de pernería en tramos 1 a 3.',
            'porcentaje' => 60,
            'fecha_reporte' => '2026-08-10 13:00:00',
        ]);

        Avance::create([
            'ot_id' => $otAtlantico->id,
            'user_id' => $eliseo->id,
            'descripcion' => 'Medición de SPT con telurómetro (3.8 Ohms) y aplicación de pintura de balizamiento terminada.',
            'porcentaje' => 100,
            'fecha_reporte' => '2026-08-10 16:35:00',
        ]);

        Avance::create([
            'ot_id' => $otCordoba->id,
            'user_id' => $carlos->id,
            'descripcion' => 'Desplazamiento completado desde Montería hasta la EB Ronda del Sinú. Registro de llegada.',
            'porcentaje' => 25,
            'fecha_reporte' => '2026-08-14 14:20:00',
        ]);

        Avance::create([
            'ot_id' => $otCordoba->id,
            'user_id' => $carlos->id,
            'descripcion' => 'Medición de presiones manométricas, limpieza de serpentín condensador y reemplazo de filtro secador.',
            'porcentaje' => 65,
            'fecha_reporte' => '2026-08-14 16:10:00',
        ]);

        // 8. Sub-actividades de Checklist Operativo
        ActividadOt::create([
            'ot_id' => $otAntioquia->id,
            'nombre' => 'Inspección visual de cableado de fuerza y control en planta Cummins',
            'peso_porcentaje' => 25,
            'progreso' => 25,
            'estado' => 'completada',
        ]);

        ActividadOt::create([
            'ot_id' => $otAntioquia->id,
            'nombre' => 'Prueba de aislamiento con megóhmetro en bobinado de generador Stamford',
            'peso_porcentaje' => 35,
            'progreso' => 0,
            'estado' => 'pendiente',
        ]);

        ActividadOt::create([
            'ot_id' => $otAntioquia->id,
            'nombre' => 'Sustitución y calibración de tarjeta reguladora AVR',
            'peso_porcentaje' => 40,
            'progreso' => 0,
            'estado' => 'pendiente',
        ]);
    }
}

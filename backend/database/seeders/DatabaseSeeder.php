<?php

namespace Database\Seeders;

use App\Models\User;
use App\Models\Empleado;
use App\Models\Cuadrilla;
use App\Models\Ot;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        // 1. Crear usuarios por roles
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

        // 2. Crear Cuadrillas de Trabajo
        $cuadrillaVias = Cuadrilla::create([
            'nombre' => 'Cuadrilla Movimiento de Tierra',
            'especialidad' => 'Excavación y Pavimentación',
            'lider_id' => $luis->id,
        ]);

        $cuadrillaEstructuras = Cuadrilla::create([
            'nombre' => 'Cuadrilla Estructuras & Cimentación',
            'especialidad' => 'Fundición de Zapatas y Armado Metal',
            'lider_id' => $carlos->id,
        ]);

        // 3. Crear Empleados / Registro Maestro de Personal
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

        Empleado::create([
            'documento' => '1018445990',
            'nombre' => 'Ing. Carlos Pérez',
            'cargo' => 'Ingeniero Residente de Estructuras',
            'telefono' => '3157778899',
            'email' => 'carlos@doblex.com',
            'rol' => 'operativo',
            'cuadrilla_id' => $cuadrillaEstructuras->id,
            'user_id' => $carlos->id,
            'estado' => 'activo',
        ]);

        Empleado::create([
            'documento' => '1018445112',
            'nombre' => 'Ing. Luis Martínez',
            'cargo' => 'Ingeniero de Vías y Excavaciones',
            'telefono' => '3186665544',
            'email' => 'luis@doblex.com',
            'rol' => 'operativo',
            'cuadrilla_id' => $cuadrillaVias->id,
            'user_id' => $luis->id,
            'estado' => 'activo',
        ]);

        Empleado::create([
            'documento' => '1090554321',
            'nombre' => 'Jorge Ramírez',
            'cargo' => 'Maestro de Obra',
            'telefono' => '3201112233',
            'rol' => 'operativo',
            'cuadrilla_id' => $cuadrillaEstructuras->id,
            'estado' => 'activo',
        ]);

        Empleado::create([
            'documento' => '1090667890',
            'nombre' => 'Pedro Gómez',
            'cargo' => 'Operador de Maquinaria Pesada',
            'telefono' => '3124445566',
            'rol' => 'operativo',
            'cuadrilla_id' => $cuadrillaVias->id,
            'estado' => 'activo',
        ]);

        // 4. Crear Órdenes de Trabajo (OT)
        Ot::create([
            'codigo' => 'OT-2026-001',
            'descripcion' => 'Excavación y Movimiento de Tierra',
            'ubicacion' => 'Autopista Sur Km 5',
            'created_by' => $admin->id,
            'user_id' => $luis->id, // Asignado a Luis Martínez
            'cuadrilla_id' => $cuadrillaVias->id,
            'prioridad' => 'P1',
            'tipo_ubicacion' => 'urbana',
            'tipo_mantenimiento' => 'correctivo',
            'progreso' => 100,
            'estado' => 'solucionada',
            'fecha_inicio' => '2026-08-01 08:00:00',
            'fecha_limite_sla' => '2026-08-01 12:30:00',
        ]);

        Ot::create([
            'codigo' => 'OT-2026-002',
            'descripcion' => 'Cimentación y Fundición de Zapatas',
            'ubicacion' => 'Sede Principal Norte',
            'created_by' => $adminis->id,
            'user_id' => $carlos->id,
            'cuadrilla_id' => $cuadrillaEstructuras->id,
            'prioridad' => 'P2',
            'tipo_ubicacion' => 'rural',
            'tipo_mantenimiento' => 'preventivo',
            'progreso' => 45,
            'estado' => 'en_progreso',
            'fecha_inicio' => '2026-08-05 09:00:00',
            'fecha_limite_sla' => '2026-08-13 22:00:00',
        ]);

        Ot::create([
            'codigo' => 'OT-2026-003',
            'descripcion' => 'Armado de Estructuras Metálicas',
            'ubicacion' => 'Sede Principal Norte',
            'created_by' => $adminis->id,
            'user_id' => $carlos->id,
            'cuadrilla_id' => $cuadrillaEstructuras->id,
            'prioridad' => 'P1',
            'tipo_ubicacion' => 'rural',
            'tipo_mantenimiento' => 'emergencia',
            'progreso' => 0,
            'estado' => 'asignada',
            'fecha_inicio' => '2026-08-13 10:00:00',
            'fecha_limite_sla' => '2026-08-13 21:42:00',
        ]);
    }
}

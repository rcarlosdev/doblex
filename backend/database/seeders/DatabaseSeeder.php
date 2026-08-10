<?php

namespace Database\Seeders;

use App\Models\User;
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

        // 2. Crear Órdenes de Trabajo (OT)
        Ot::create([
            'codigo' => 'OT-2026-001',
            'descripcion' => 'Excavación y Movimiento de Tierra',
            'ubicacion' => 'Autopista Sur Km 5',
            'created_by' => $admin->id,
            'user_id' => $luis->id, // Asignado a Luis Martínez
            'progreso' => 100,
            'estado' => 'finalizado',
            'fecha_inicio' => '2026-08-01',
        ]);

        Ot::create([
            'codigo' => 'OT-2026-002',
            'descripcion' => 'Cimentación y Fundición de Zapatas',
            'ubicacion' => 'Sede Principal Norte',
            'created_by' => $adminis->id, // Creada por Administrativo (Auxiliar Técnico)
            'user_id' => $carlos->id, // Asignado a Carlos Pérez
            'progreso' => 45,
            'estado' => 'en_progreso',
            'fecha_inicio' => '2026-08-05',
        ]);

        Ot::create([
            'codigo' => 'OT-2026-003',
            'descripcion' => 'Armado de Estructuras Metálicas',
            'ubicacion' => 'Sede Principal Norte',
            'created_by' => $adminis->id, // Creada por Administrativo (Auxiliar Técnico)
            'user_id' => $carlos->id, // Asignado a Carlos Pérez
            'progreso' => 0,
            'estado' => 'pendiente',
            'fecha_inicio' => '2026-08-15',
        ]);
    }
}

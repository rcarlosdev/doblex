<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('empleados', function (Blueprint $table) {
            $table->id();
            $table->string('documento')->unique();
            $table->string('nombre');
            $table->string('cargo');
            $table->string('telefono')->nullable();
            $table->string('email')->nullable();
            $table->string('rol')->default('operativo'); // admin, administrativo, operativo
            $table->foreignId('cuadrilla_id')->nullable()->constrained('cuadrillas')->onDelete('set null');
            $table->foreignId('user_id')->nullable()->constrained('users')->onDelete('set null');
            $table->string('estado')->default('activo'); // activo, inactivo
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('empleados');
    }
};

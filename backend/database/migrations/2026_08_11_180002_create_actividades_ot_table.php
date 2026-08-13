<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('actividades_ot', function (Blueprint $table) {
            $table->id();
            $table->foreignId('ot_id')->constrained('ots')->onDelete('cascade');
            $table->string('nombre');
            $table->integer('peso_porcentaje')->default(100);
            $table->integer('progreso')->default(0);
            $table->string('estado')->default('pendiente'); // pendiente, en_progreso, finalizado
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('actividades_ot');
    }
};

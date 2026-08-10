<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('avances', function (Blueprint $table) {
            $table->id();
            $table->foreignId('ot_id')->constrained('ots')->onDelete('cascade');
            $table->foreignId('user_id')->constrained('users')->onDelete('cascade'); // Operativo que reporta
            $table->text('descripcion');
            $table->integer('porcentaje'); // Avance en porcentaje reportado hoy (ej: 15)
            $table->date('fecha_reporte');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('avances');
    }
};

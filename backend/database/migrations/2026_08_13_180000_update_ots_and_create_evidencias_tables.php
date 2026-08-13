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
        Schema::table('ots', function (Blueprint $table) {
            $table->string('sitio')->nullable()->after('descripcion');
            $table->string('prioridad')->default('P2')->after('sitio'); // P1, P2, P3
            $table->string('tipo_ubicacion')->default('urbana')->after('prioridad'); // urbana, rural
            $table->string('tipo_mantenimiento')->default('preventivo')->after('tipo_ubicacion'); // preventivo, correctivo, emergencia
            $table->string('subsistema')->default('sistema_electrico')->after('tipo_mantenimiento'); // aires_acondicionados, plantas_electricas, sistema_electrico, power, acceso_transmision, apoyo_integral, hibridos_sfv
            $table->string('tipo_gasto')->default('OPEX')->after('subsistema'); // OPEX, CAPEX
            $table->timestamp('fecha_limite_sla')->nullable()->after('fecha_inicio');
            $table->timestamp('fecha_llegada_sitio')->nullable()->after('fecha_limite_sla');
            $table->timestamp('fecha_solucion')->nullable()->after('fecha_llegada_sitio');
            $table->string('causa_falla')->nullable()->after('fecha_solucion'); // desgaste, vandalismo, factor_climatico
            $table->text('observaciones_cierre')->nullable()->after('causa_falla');
        });

        Schema::create('evidencias_fotograficas', function (Blueprint $table) {
            $table->id();
            $table->foreignId('ot_id')->constrained('ots')->onDelete('cascade');
            $table->string('tipo'); // antes, durante, despues
            $table->text('url_imagen');
            $table->decimal('latitud', 10, 8)->nullable();
            $table->decimal('longitud', 11, 8)->nullable();
            $table->timestamp('fecha_hora_captura');
            $table->timestamps();
        });

        Schema::create('repuestos_utilizados', function (Blueprint $table) {
            $table->id();
            $table->foreignId('ot_id')->constrained('ots')->onDelete('cascade');
            $table->string('nombre_item');
            $table->decimal('cantidad', 10, 2);
            $table->string('unidad_medida')->default('unidad');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('repuestos_utilizados');
        Schema::dropIfExists('evidencias_fotograficas');

        Schema::table('ots', function (Blueprint $table) {
            $table->dropColumn([
                'prioridad',
                'tipo_ubicacion',
                'tipo_mantenimiento',
                'fecha_limite_sla',
                'fecha_llegada_sitio',
                'fecha_solucion',
                'causa_falla',
                'observaciones_cierre',
            ]);
        });
    }
};

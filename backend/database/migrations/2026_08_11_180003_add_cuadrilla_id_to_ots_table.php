<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('ots', function (Blueprint $table) {
            $table->foreignId('cuadrilla_id')->nullable()->constrained('cuadrillas')->onDelete('set null');
        });
    }

    public function down(): void
    {
        Schema::table('ots', function (Blueprint $table) {
            $table->dropForeign(['cuadrilla_id']);
            $table->dropColumn('cuadrilla_id');
        });
    }
};

<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Attributes\Fillable;

#[Fillable(['ot_id', 'user_id', 'descripcion', 'porcentaje', 'fecha_reporte'])]
class Avance extends Model
{
    /**
     * Relación con la Orden de Trabajo.
     */
    public function ot(): BelongsTo
    {
        return $this->belongsTo(Ot::class);
    }

    /**
     * Relación con el Operativo que realiza el reporte.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}

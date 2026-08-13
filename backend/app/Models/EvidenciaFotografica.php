<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Attributes\Fillable;

#[Fillable(['ot_id', 'tipo', 'url_imagen', 'latitud', 'longitud', 'fecha_hora_captura'])]
class EvidenciaFotografica extends Model
{
    protected $table = 'evidencias_fotograficas';

    public function ot(): BelongsTo
    {
        return $this->belongsTo(Ot::class);
    }
}

<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Attributes\Fillable;

#[Fillable(['ot_id', 'nombre_item', 'cantidad', 'unidad_medida'])]
class RepuestoUtilizado extends Model
{
    protected $table = 'repuestos_utilizados';

    public function ot(): BelongsTo
    {
        return $this->belongsTo(Ot::class);
    }
}

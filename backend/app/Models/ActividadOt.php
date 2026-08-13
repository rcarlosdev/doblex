<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ActividadOt extends Model
{
    use HasFactory;

    protected $table = 'actividades_ot';

    protected $fillable = [
        'ot_id',
        'nombre',
        'peso_porcentaje',
        'progreso',
        'estado',
    ];

    public function ot()
    {
        return $this->belongsTo(Ot::class);
    }
}

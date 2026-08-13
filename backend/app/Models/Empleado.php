<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Empleado extends Model
{
    use HasFactory;

    protected $fillable = [
        'documento',
        'nombre',
        'cargo',
        'telefono',
        'email',
        'rol',
        'cuadrilla_id',
        'user_id',
        'estado',
    ];

    public function cuadrilla()
    {
        return $this->belongsTo(Cuadrilla::class);
    }

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}

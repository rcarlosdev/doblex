<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Cuadrilla extends Model
{
    use HasFactory;

    protected $fillable = [
        'nombre',
        'especialidad',
        'lider_id',
    ];

    public function lider()
    {
        return $this->belongsTo(User::class, 'lider_id');
    }

    public function empleados()
    {
        return $this->hasMany(Empleado::class);
    }

    public function ots()
    {
        return $this->hasMany(Ot::class);
    }
}

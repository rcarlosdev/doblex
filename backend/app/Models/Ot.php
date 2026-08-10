<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Attributes\Fillable;

#[Fillable(['codigo', 'descripcion', 'ubicacion', 'created_by', 'user_id', 'progreso', 'estado', 'fecha_inicio'])]
class Ot extends Model
{
    /**
     * Relación con el Operativo asignado.
     */
    public function assignedUser(): BelongsTo
    {
        return $this->belongsTo(User::class, 'user_id');
    }

    /**
     * Relación con el Administrador o Administrativo creador.
     */
    public function creator(): BelongsTo
    {
        return $this->belongsTo(User::class, 'created_by');
    }

    /**
     * Relación con el histórico de avances de obra.
     */
    public function avances(): HasMany
    {
        return $this->hasMany(Avance::class);
    }
}

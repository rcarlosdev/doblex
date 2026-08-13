<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Attributes\Fillable;

#[Fillable([
    'codigo', 
    'descripcion', 
    'sitio',
    'ubicacion', 
    'created_by', 
    'user_id', 
    'cuadrilla_id', 
    'progreso', 
    'estado', 
    'prioridad', 
    'tipo_ubicacion', 
    'tipo_mantenimiento', 
    'subsistema',
    'tipo_gasto',
    'fecha_inicio',
    'fecha_limite_sla',
    'fecha_llegada_sitio',
    'fecha_solucion',
    'causa_falla',
    'observaciones_cierre'
])]
class Ot extends Model
{
    /**
     * Relación con las evidencias fotográficas.
     */
    public function evidencias(): HasMany
    {
        return $this->hasMany(EvidenciaFotografica::class);
    }

    /**
     * Relación con repuestos utilizados.
     */
    public function repuestos(): HasMany
    {
        return $this->hasMany(RepuestoUtilizado::class);
    }

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
     * Relación con la cuadrilla asignada.
     */
    public function cuadrilla(): BelongsTo
    {
        return $this->belongsTo(Cuadrilla::class);
    }

    /**
     * Relación con las sub-actividades de la OT.
     */
    public function actividades(): HasMany
    {
        return $this->hasMany(ActividadOt::class);
    }

    /**
     * Relación con el histórico de avances de obra.
     */
    public function avances(): HasMany
    {
        return $this->hasMany(Avance::class);
    }
}

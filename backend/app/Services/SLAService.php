<?php

namespace App\Services;

use Carbon\Carbon;
use InvalidArgumentException;

class SLAService
{
    /**
     * Matriz de tiempos SLA en minutos basada en las reglas de negocio SMU.
     */
    private const SLA_MATRIX = [
        'P1' => [
            'urbana' => (4 * 60) + 30,  // 4h 30m = 270 min
            'rural'  => (11 * 60) + 42, // 11h 42m = 702 min
        ],
        'P2' => [
            'urbana' => 6 * 60,         // 6h 00m = 360 min
            'rural'  => 12 * 60,        // 12h 00m = 720 min
        ],
        'P3' => [
            'urbana' => 12 * 60,        // 12h 00m = 720 min
            'rural'  => 20 * 60,        // 20h 00m = 1200 min
        ],
    ];

    /**
     * Calcula la fecha limite de solucion para una Orden de Trabajo.
     *
     * @param string $prioridad 'P1', 'P2', 'P3'
     * @param string $tipoUbicacion 'urbana', 'rural'
     * @param Carbon|null $fechaApertura
     * @return Carbon
     */
    public function calcularFechaLimite(string $prioridad, string $tipoUbicacion, ?Carbon $fechaApertura = null): Carbon
    {
        $fechaInicio = $fechaApertura ? Carbon::parse($fechaApertura) : Carbon::now();
        $prioridadKey = strtoupper(trim($prioridad));
        $ubicacionKey = strtolower(trim($tipoUbicacion));

        if (!isset(self::SLA_MATRIX[$prioridadKey][$ubicacionKey])) {
            // Valor por defecto en caso de variaciones: 12 horas
            return $fechaInicio->copy()->addHours(12);
        }

        $minutos = self::SLA_MATRIX[$prioridadKey][$ubicacionKey];

        return $fechaInicio->copy()->addMinutes($minutos);
    }
}

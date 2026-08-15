<?php

namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use App\Models\Avance;
use App\Models\Ot;
use Illuminate\Http\Request;

class AvanceController extends Controller
{
    /**
     * Registrar un avance diario de obra civil en campo.
     */
    public function store(Request $request)
    {
        $user = $request->user();

        // Validar campos del reporte diario
        $request->validate([
            'ot_id' => 'required|exists:ots,id',
            'descripcion' => 'required|string|min:5',
            'porcentaje' => 'required|integer|min:1|max:100',
            'fecha_reporte' => 'required|date',
        ]);

        $ot = Ot::find($request->ot_id);

        // Validar permisos: el Operativo asignado, miembros de la cuadrilla asignada, o administradores
        $esAsignadoDirecto = ($ot->user_id === $user->id);
        $esDeCuadrilla = ($user->empleado && $user->empleado->cuadrilla_id && $ot->cuadrilla_id && $user->empleado->cuadrilla_id === $ot->cuadrilla_id);
        $esAdmin = in_array($user->role, ['admin', 'administrativo']);

        if (!$esAsignadoDirecto && !$esDeCuadrilla && !$esAdmin) {
            return response()->json([
                'status' => 'error',
                'message' => 'No estás autorizado para reportar avances en esta Orden de Trabajo.'
            ], 403);
        }

        // Validar que el nuevo progreso total no supere el 100%
        $nuevoProgreso = $ot->progreso + $request->porcentaje;
        if ($nuevoProgreso > 100) {
            return response()->json([
                'status' => 'error',
                'message' => "El avance diario reportado ({$request->porcentaje}%) hace que el progreso acumulado supere el 100% (Progreso actual: {$ot->progreso}%)."
            ], 422);
        }

        // Crear el avance en la base de datos
        $avance = Avance::create([
            'ot_id' => $request->ot_id,
            'user_id' => $user->id,
            'descripcion' => $request->descripcion,
            'porcentaje' => $request->porcentaje,
            'fecha_reporte' => $request->fecha_reporte,
        ]);

        // Actualizar el progreso acumulado y el estado de la OT correspondiente
        $ot->progreso = $nuevoProgreso;
        
        if ($ot->progreso >= 100) {
            $ot->estado = 'finalizado';
        } else {
            $ot->estado = 'en_progreso';
        }
        
        $ot->save();

        return response()->json([
            'status' => 'success',
            'message' => 'Avance reportado con éxito y progreso de la OT actualizado.',
            'data' => [
                'avance' => $avance,
                'ot' => $ot->load(['assignedUser', 'creator'])
            ]
        ], 211);
    }
}

<?php

namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use App\Models\Ot;
use App\Models\User;
use Illuminate\Http\Request;

class OtController extends Controller
{
    /**
     * Listar Órdenes de Trabajo (OT) según el rol y permisos de usuario.
     */
    public function index(Request $request)
    {
        $user = $request->user();

        if ($user->role === 'admin') {
            // Admin ve todo
            $ots = Ot::with(['assignedUser', 'creator', 'cuadrilla', 'actividades'])->orderBy('codigo', 'asc')->get();
        } elseif ($user->role === 'administrativo') {
            // Administrativo ve las creadas por él
            $ots = Ot::with(['assignedUser', 'creator', 'cuadrilla', 'actividades'])
                ->where('created_by', $user->id)
                ->orderBy('codigo', 'asc')
                ->get();
        } elseif ($user->role === 'operativo') {
            // Operativo ve las asignadas a él
            $ots = Ot::with(['assignedUser', 'creator', 'cuadrilla', 'actividades'])
                ->where('user_id', $user->id)
                ->orderBy('codigo', 'asc')
                ->get();
        } else {
            return response()->json([
                'status' => 'error',
                'message' => 'Rol de usuario no autorizado.'
            ], 403);
        }

        return response()->json([
            'status' => 'success',
            'data' => $ots
        ]);
    }

    /**
     * Registrar una nueva Orden de Trabajo (solo admin y administrativo).
     */
    public function store(Request $request)
    {
        $user = $request->user();

        if ($user->role !== 'admin' && $user->role !== 'administrativo') {
            return response()->json([
                'status' => 'error',
                'message' => 'No tienes permisos para registrar Órdenes de Trabajo.'
            ], 403);
        }

        $request->validate([
            'codigo' => 'required|string|unique:ots,codigo',
            'descripcion' => 'required|string',
            'ubicacion' => 'required|string',
            'user_id' => 'required|exists:users,id', // Operativo asignado
            'cuadrilla_id' => 'nullable|exists:cuadrillas,id',
            'fecha_inicio' => 'required|date',
        ]);

        // Validar que el usuario asignado sea operativo
        $assignedUser = User::find($request->user_id);
        if ($assignedUser->role !== 'operativo') {
            return response()->json([
                'status' => 'error',
                'message' => 'Solo se pueden asignar OTs a usuarios con perfil Operativo.'
            ], 422);
        }

        $ot = Ot::create([
            'codigo' => $request->codigo,
            'descripcion' => $request->descripcion,
            'ubicacion' => $request->ubicacion,
            'created_by' => $user->id,
            'user_id' => $request->user_id,
            'cuadrilla_id' => $request->cuadrilla_id,
            'fecha_inicio' => $request->fecha_inicio,
            'progreso' => 0,
            'estado' => 'pendiente',
        ]);

        return response()->json([
            'status' => 'success',
            'message' => 'Orden de Trabajo creada con éxito.',
            'data' => $ot->load(['assignedUser', 'creator', 'cuadrilla', 'actividades'])
        ], 201);
    }

    /**
     * Obtener el listado de usuarios con perfil Operativo (para el selector de asignación).
     */
    public function getOperativos(Request $request)
    {
        $user = $request->user();

        if ($user->role !== 'admin' && $user->role !== 'administrativo') {
            return response()->json([
                'status' => 'error',
                'message' => 'No tienes permisos para listar operadores.'
            ], 403);
        }

        $operativos = User::where('role', 'operativo')
            ->select('id', 'name', 'username')
            ->orderBy('name', 'asc')
            ->get();

        return response()->json([
            'status' => 'success',
            'data' => $operativos
        ]);
    }
}

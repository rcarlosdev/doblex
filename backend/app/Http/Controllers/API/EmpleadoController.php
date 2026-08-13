<?php

namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use App\Models\Empleado;
use Illuminate\Http\Request;

class EmpleadoController extends Controller
{
    /**
     * Listar todos los empleados con su cuadrilla y usuario asociado.
     */
    public function index(Request $request)
    {
        $empleados = Empleado::with(['cuadrilla', 'user'])
            ->orderBy('nombre', 'asc')
            ->get();

        return response()->json([
            'status' => 'success',
            'data' => $empleados
        ]);
    }

    /**
     * Crear un nuevo empleado.
     */
    public function store(Request $request)
    {
        $request->validate([
            'documento' => 'required|string|unique:empleados,documento',
            'nombre' => 'required|string|max:255',
            'cargo' => 'required|string|max:255',
            'telefono' => 'nullable|string|max:50',
            'email' => 'nullable|email|max:255',
            'rol' => 'required|in:admin,administrativo,operativo',
            'cuadrilla_id' => 'nullable|exists:cuadrillas,id',
            'user_id' => 'nullable|exists:users,id',
            'estado' => 'required|in:activo,inactivo',
        ]);

        $empleado = Empleado::create($request->all());

        return response()->json([
            'status' => 'success',
            'message' => 'Empleado creado exitosamente.',
            'data' => $empleado->load(['cuadrilla', 'user'])
        ], 201);
    }

    /**
     * Actualizar datos de un empleado.
     */
    public function update(Request $request, $id)
    {
        $empleado = Empleado::findOrFail($id);

        $request->validate([
            'documento' => 'required|string|unique:empleados,documento,' . $id,
            'nombre' => 'required|string|max:255',
            'cargo' => 'required|string|max:255',
            'telefono' => 'nullable|string|max:50',
            'email' => 'nullable|email|max:255',
            'rol' => 'required|in:admin,administrativo,operativo',
            'cuadrilla_id' => 'nullable|exists:cuadrillas,id',
            'user_id' => 'nullable|exists:users,id',
            'estado' => 'required|in:activo,inactivo',
        ]);

        $empleado->update($request->all());

        return response()->json([
            'status' => 'success',
            'message' => 'Empleado actualizado exitosamente.',
            'data' => $empleado->load(['cuadrilla', 'user'])
        ]);
    }

    /**
     * Eliminar o desactivar un empleado.
     */
    public function destroy($id)
    {
        $empleado = Empleado::findOrFail($id);
        $empleado->delete();

        return response()->json([
            'status' => 'success',
            'message' => 'Empleado eliminado exitosamente.'
        ]);
    }
}

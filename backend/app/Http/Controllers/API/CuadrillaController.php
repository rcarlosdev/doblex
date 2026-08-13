<?php

namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use App\Models\Cuadrilla;
use Illuminate\Http\Request;

class CuadrillaController extends Controller
{
    /**
     * Listar todas las cuadrillas con sus integrantes y líder.
     */
    public function index()
    {
        $cuadrillas = Cuadrilla::with(['lider', 'empleados'])
            ->orderBy('nombre', 'asc')
            ->get();

        return response()->json([
            'status' => 'success',
            'data' => $cuadrillas
        ]);
    }

    /**
     * Crear una nueva cuadrilla.
     */
    public function store(Request $request)
    {
        $request->validate([
            'nombre' => 'required|string|max:255',
            'especialidad' => 'nullable|string|max:255',
            'lider_id' => 'nullable|exists:users,id',
        ]);

        $cuadrilla = Cuadrilla::create($request->all());

        return response()->json([
            'status' => 'success',
            'message' => 'Cuadrilla creada exitosamente.',
            'data' => $cuadrilla->load(['lider', 'empleados'])
        ], 201);
    }

    /**
     * Actualizar una cuadrilla.
     */
    public function update(Request $request, $id)
    {
        $cuadrilla = Cuadrilla::findOrFail($id);

        $request->validate([
            'nombre' => 'required|string|max:255',
            'especialidad' => 'nullable|string|max:255',
            'lider_id' => 'nullable|exists:users,id',
        ]);

        $cuadrilla->update($request->all());

        return response()->json([
            'status' => 'success',
            'message' => 'Cuadrilla actualizada exitosamente.',
            'data' => $cuadrilla->load(['lider', 'empleados'])
        ]);
    }

    /**
     * Eliminar una cuadrilla.
     */
    public function destroy($id)
    {
        $cuadrilla = Cuadrilla::findOrFail($id);
        $cuadrilla->delete();

        return response()->json([
            'status' => 'success',
            'message' => 'Cuadrilla eliminada exitosamente.'
        ]);
    }
}

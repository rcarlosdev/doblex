<?php

namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use App\Models\Ot;
use App\Models\User;
use App\Models\EvidenciaFotografica;
use App\Models\RepuestoUtilizado;
use App\Services\SLAService;
use Illuminate\Http\Request;
use Carbon\Carbon;

class OtController extends Controller
{
    protected SLAService $slaService;

    public function __construct(SLAService $slaService)
    {
        $this->slaService = $slaService;
    }

    /**
     * Listar Órdenes de Trabajo (OT) según el rol y permisos de usuario.
     */
    public function index(Request $request)
    {
        $user = $request->user();

        $query = Ot::with(['assignedUser', 'creator', 'cuadrilla', 'actividades', 'evidencias', 'repuestos', 'avances'])
            ->orderBy('created_at', 'desc');

        if ($user->role === 'admin') {
            $ots = $query->get();
        } elseif ($user->role === 'administrativo') {
            $ots = $query->where('created_by', $user->id)->get();
        } elseif ($user->role === 'operativo') {
            $ots = $query->where(function ($q) use ($user) {
                $q->where('user_id', $user->id);
                if ($user->cuadrilla_id) {
                    $q->orWhere('cuadrilla_id', $user->cuadrilla_id);
                }
            })->get();
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
     * Obtener detalle de una OT específica.
     */
    public function show($id)
    {
        $ot = Ot::with(['assignedUser', 'creator', 'cuadrilla', 'actividades', 'evidencias', 'repuestos', 'avances'])->find($id);

        if (!$ot) {
            return response()->json([
                'status' => 'error',
                'message' => 'Orden de Trabajo no encontrada.'
            ], 404);
        }

        return response()->json([
            'status' => 'success',
            'data' => $ot
        ]);
    }

    /**
     * Registrar una nueva Orden de Trabajo con cálculo automático de SLA.
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
            'sitio' => 'nullable|string',
            'ubicacion' => 'required|string',
            'user_id' => 'required|exists:users,id',
            'cuadrilla_id' => 'nullable|exists:cuadrillas,id',
            'prioridad' => 'required|string|in:P1,P2,P3',
            'tipo_ubicacion' => 'required|string|in:urbana,rural',
            'tipo_mantenimiento' => 'required|string|in:preventivo,correctivo,emergencia',
            'subsistema' => 'nullable|string',
            'tipo_gasto' => 'nullable|string|in:OPEX,CAPEX',
            'fecha_inicio' => 'required|date',
        ]);

        $fechaInicio = Carbon::parse($request->fecha_inicio);
        
        // Calcular la fecha limite de SLA utilizando SLAService
        $fechaLimiteSla = $this->slaService->calcularFechaLimite(
            $request->prioridad,
            $request->tipo_ubicacion,
            $fechaInicio
        );

        $ot = Ot::create([
            'codigo' => $request->codigo,
            'descripcion' => $request->descripcion,
            'sitio' => $request->sitio,
            'ubicacion' => $request->ubicacion,
            'created_by' => $user->id,
            'user_id' => $request->user_id,
            'cuadrilla_id' => $request->cuadrilla_id,
            'prioridad' => $request->prioridad,
            'tipo_ubicacion' => $request->tipo_ubicacion,
            'tipo_mantenimiento' => $request->tipo_mantenimiento,
            'subsistema' => $request->subsistema ?? 'sistema_electrico',
            'tipo_gasto' => $request->tipo_gasto ?? 'OPEX',
            'fecha_inicio' => $request->fecha_inicio,
            'fecha_limite_sla' => $fechaLimiteSla,
            'progreso' => 0,
            'estado' => 'asignada',
        ]);

        return response()->json([
            'status' => 'success',
            'message' => 'Orden de Trabajo registrada con éxito y SLA calculado.',
            'data' => $ot->load(['assignedUser', 'creator', 'cuadrilla', 'actividades'])
        ], 201);
    }

    /**
     * Actualizar datos generales de una Orden de Trabajo (solo admin y administrativo).
     */
    public function update(Request $request, $id)
    {
        $user = $request->user();

        if ($user->role !== 'admin' && $user->role !== 'administrativo') {
            return response()->json([
                'status' => 'error',
                'message' => 'No tienes permisos para modificar Órdenes de Trabajo.'
            ], 403);
        }

        $ot = Ot::find($id);
        if (!$ot) {
            return response()->json([
                'status' => 'error',
                'message' => 'Orden de Trabajo no encontrada.'
            ], 404);
        }

        $request->validate([
            'codigo' => 'required|string|unique:ots,codigo,' . $id,
            'descripcion' => 'required|string',
            'sitio' => 'nullable|string',
            'ubicacion' => 'required|string',
            'user_id' => 'required|exists:users,id',
            'cuadrilla_id' => 'nullable|exists:cuadrillas,id',
            'prioridad' => 'required|string|in:P1,P2,P3',
            'tipo_ubicacion' => 'required|string|in:urbana,rural',
            'tipo_mantenimiento' => 'required|string|in:preventivo,correctivo,emergencia',
            'subsistema' => 'nullable|string',
            'tipo_gasto' => 'nullable|string|in:OPEX,CAPEX',
            'estado' => 'required|string',
            'fecha_inicio' => 'required|date',
        ]);

        $fechaInicio = Carbon::parse($request->fecha_inicio);
        
        // Recalcular SLA
        $fechaLimiteSla = $this->slaService->calcularFechaLimite(
            $request->prioridad,
            $request->tipo_ubicacion,
            $fechaInicio
        );

        $ot->update([
            'codigo' => $request->codigo,
            'descripcion' => $request->descripcion,
            'sitio' => $request->sitio,
            'ubicacion' => $request->ubicacion,
            'user_id' => $request->user_id,
            'cuadrilla_id' => $request->cuadrilla_id,
            'prioridad' => $request->prioridad,
            'tipo_ubicacion' => $request->tipo_ubicacion,
            'tipo_mantenimiento' => $request->tipo_mantenimiento,
            'subsistema' => $request->subsistema,
            'tipo_gasto' => $request->tipo_gasto,
            'estado' => $request->estado,
            'fecha_inicio' => $request->fecha_inicio,
            'fecha_limite_sla' => $fechaLimiteSla,
        ]);

        return response()->json([
            'status' => 'success',
            'message' => 'Orden de Trabajo actualizada con éxito.',
            'data' => $ot->load(['assignedUser', 'creator', 'cuadrilla', 'actividades', 'evidencias', 'repuestos'])
        ]);
    }

    /**
     * Actualizar el estado de la OT (Asignada, En Camino, En Sitio, En Progreso, Detenida por Materiales, Solucionada).
     */
    public function updateEstado(Request $request, $id)
    {
        $ot = Ot::find($id);

        if (!$ot) {
            return response()->json([
                'status' => 'error',
                'message' => 'OT no encontrada.'
            ], 404);
        }

        $request->validate([
            'estado' => 'required|string|in:asignada,en_camino,en_sitio,en_progreso,detenida_materiales,solucionada,finalizada',
            'progreso' => 'nullable|integer|min:0|max:100',
        ]);

        $data = ['estado' => $request->estado];

        if ($request->has('progreso')) {
            $data['progreso'] = $request->progreso;
        }

        if ($request->estado === 'en_sitio' && !$ot->fecha_llegada_sitio) {
            $data['fecha_llegada_sitio'] = Carbon::now();
        }

        if ($request->estado === 'solucionada') {
            $data['fecha_solucion'] = Carbon::now();
            $data['progreso'] = 100;
        }

        $ot->update($data);

        return response()->json([
            'status' => 'success',
            'message' => "Estado de la OT actualizado a '{$request->estado}'.",
            'data' => $ot
        ]);
    }

    /**
     * Cargar evidencia fotográfica (con metadatos de tipo, lat, lng).
     */
    public function uploadEvidencia(Request $request, $id)
    {
        $ot = Ot::find($id);

        if (!$ot) {
            return response()->json([
                'status' => 'error',
                'message' => 'OT no encontrada.'
            ], 404);
        }

        $request->validate([
            'tipo' => 'required|string|in:antes,durante,despues',
            'imagen_base64' => 'required_without:imagen_url|string',
            'latitud' => 'nullable|numeric',
            'longitud' => 'nullable|numeric',
        ]);

        $urlImagen = $request->imagen_url ?? $request->imagen_base64;

        $evidencia = EvidenciaFotografica::create([
            'ot_id' => $ot->id,
            'tipo' => $request->tipo,
            'url_imagen' => $urlImagen,
            'latitud' => $request->latitud,
            'longitud' => $request->longitud,
            'fecha_hora_captura' => Carbon::now(),
        ]);

        return response()->json([
            'status' => 'success',
            'message' => 'Evidencia fotográfica guardada.',
            'data' => $evidencia
        ], 201);
    }

    /**
     * Eliminar evidencia fotográfica.
     */
    public function deleteEvidencia(Request $request, $id)
    {
        $evidencia = EvidenciaFotografica::find($id);

        if (!$evidencia) {
            return response()->json([
                'status' => 'error',
                'message' => 'Evidencia fotográfica no encontrada.'
            ], 404);
        }

        // Si la OT ya fue solucionada/finalizada no permite borrado
        if (in_array($evidencia->ot->estado, ['solucionada', 'finalizada'])) {
            return response()->json([
                'status' => 'error',
                'message' => 'No se pueden eliminar evidencias de una Orden de Trabajo solucionada o finalizada.'
            ], 422);
        }

        $evidencia->delete();

        return response()->json([
            'status' => 'success',
            'message' => 'Evidencia fotográfica eliminada con éxito.'
        ]);
    }

    /**
     * Cerrar la OT registrando insumos/repuestos y causa raíz de la falla.
     */
    public function cerrarOt(Request $request, $id)
    {
        $ot = Ot::find($id);

        if (!$ot) {
            return response()->json([
                'status' => 'error',
                'message' => 'OT no encontrada.'
            ], 404);
        }

        $request->validate([
            'causa_falla' => 'required|string|in:desgaste,vandalismo,factor_climatico,desconocido',
            'observaciones_cierre' => 'nullable|string',
            'repuestos' => 'nullable|array',
            'repuestos.*.nombre_item' => 'required|string',
            'repuestos.*.cantidad' => 'required|numeric|min:0.01',
            'repuestos.*.unidad_medida' => 'nullable|string',
        ]);

        // Verificar que la OT tenga diligenciadas las 3 evidencias obligatorias
        $evidenciasTipos = $ot->evidencias()->pluck('tipo')->toArray();
        $faltantes = [];
        if (!in_array('antes', $evidenciasTipos)) $faltantes[] = 'Evidencia de ANTES';
        if (!in_array('durante', $evidenciasTipos)) $faltantes[] = 'Evidencia de DURANTE';
        if (!in_array('despues', $evidenciasTipos)) $faltantes[] = 'Evidencia de DESPUÉS';

        if (count($faltantes) > 0) {
            return response()->json([
                'status' => 'error',
                'message' => 'No se puede cerrar la OT sin diligenciar totalmente las evidencias obligatorias: ' . implode(', ', $faltantes)
            ], 422);
        }

        $ot->update([
            'estado' => 'solucionada',
            'progreso' => 100,
            'fecha_solucion' => Carbon::now(),
            'causa_falla' => $request->causa_falla,
            'observaciones_cierre' => $request->observaciones_cierre,
        ]);

        if ($request->has('repuestos')) {
            foreach ($request->repuestos as $item) {
                RepuestoUtilizado::create([
                    'ot_id' => $ot->id,
                    'nombre_item' => $item['nombre_item'],
                    'cantidad' => $item['cantidad'],
                    'unidad_medida' => $item['unidad_medida'] ?? 'unidad',
                ]);
            }
        }

        return response()->json([
            'status' => 'success',
            'message' => 'Orden de Trabajo cerrada y solucionada con éxito.',
            'data' => $ot->load(['evidencias', 'repuestos'])
        ]);
    }

    /**
     * Obtener el listado de usuarios con perfil Operativo.
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
            ->with('empleado:id,user_id,cuadrilla_id')
            ->select('id', 'name', 'username')
            ->orderBy('name', 'asc')
            ->get()
            ->map(function ($op) {
                return [
                    'id' => $op->id,
                    'name' => $op->name,
                    'username' => $op->username,
                    'cuadrilla_id' => $op->empleado ? $op->empleado->cuadrilla_id : null,
                ];
            });

        return response()->json([
            'status' => 'success',
            'data' => $operativos
        ]);
    }
}

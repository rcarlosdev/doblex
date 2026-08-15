<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\API\AuthController;
use App\Http\Controllers\API\OtController;
use App\Http\Controllers\API\AvanceController;
use App\Http\Controllers\API\EmpleadoController;
use App\Http\Controllers\API\CuadrillaController;

// Ruta pública de autenticación
Route::post('/login', [AuthController::class, 'login']);

// Rutas protegidas bajo autenticación de Laravel Sanctum
Route::middleware('auth:sanctum')->group(function () {
    
    // Obtener los datos del usuario en sesión
    Route::get('/user', function (Request $request) {
        return $request->user();
    });

    // Cerrar sesión
    Route::post('/logout', [AuthController::class, 'logout']);

    // Órdenes de Trabajo (OT)
    Route::get('/ots', [OtController::class, 'index']);
    Route::post('/ots', [OtController::class, 'store']);
    Route::get('/ots/{id}', [OtController::class, 'show']);
    Route::put('/ots/{id}', [OtController::class, 'update']);
    Route::put('/ots/{id}/estado', [OtController::class, 'updateEstado']);
    Route::post('/ots/{id}/evidencia', [OtController::class, 'uploadEvidencia']);
    Route::delete('/evidencias/{id}', [OtController::class, 'deleteEvidencia']);
    Route::post('/ots/{id}/cerrar', [OtController::class, 'cerrarOt']);
    Route::get('/operadores', [OtController::class, 'getOperativos']); // Listado de operadores para asignar


    // Módulo 7: Gestión Base de Empleados y Cuadrillas
    Route::get('/empleados', [EmpleadoController::class, 'index']);
    Route::post('/empleados', [EmpleadoController::class, 'store']);
    Route::put('/empleados/{id}', [EmpleadoController::class, 'update']);
    Route::delete('/empleados/{id}', [EmpleadoController::class, 'destroy']);

    Route::get('/cuadrillas', [CuadrillaController::class, 'index']);
    Route::post('/cuadrillas', [CuadrillaController::class, 'store']);
    Route::put('/cuadrillas/{id}', [CuadrillaController::class, 'update']);
    Route::delete('/cuadrillas/{id}', [CuadrillaController::class, 'destroy']);

    // Reportes de Avance en Campo
    Route::post('/avances', [AvanceController::class, 'store']);
});

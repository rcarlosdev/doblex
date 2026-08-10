<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\API\AuthController;
use App\Http\Controllers\API\OtController;
use App\Http\Controllers\API\AvanceController;

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
    Route::get('/operadores', [OtController::class, 'getOperativos']); // Listado de operadores para asignar

    // Reportes de Avance en Campo
    Route::post('/avances', [AvanceController::class, 'store']);
});

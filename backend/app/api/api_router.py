from fastapi import APIRouter
from app.api.endpoints import auth, ots, empleados, cuadrillas, avances, exports, sitios

api_router = APIRouter()

api_router.include_router(auth.router, tags=["Autenticación"])
api_router.include_router(ots.router, tags=["Órdenes de Trabajo"])
api_router.include_router(sitios.router, tags=["Sitios / Estaciones Base"])
api_router.include_router(empleados.router, tags=["Empleados"])
api_router.include_router(cuadrillas.router, tags=["Cuadrillas"])
api_router.include_router(avances.router, tags=["Avances en Campo"])
api_router.include_router(exports.router, tags=["Exportaciones e Importaciones"])

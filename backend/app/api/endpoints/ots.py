from typing import List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user, require_roles
from app.models.user import User
from app.schemas.ot import (
    OtCreate, OtUpdate, OtEstadoUpdate, OtCerrarRequest,
    EvidenciaCreate, RepuestoSyncRequest
)
from app.services.ot_service import ot_service

router = APIRouter()

# Compatibilidad con cualquier importación previa
serialize_ot = ot_service.serialize_ot
parse_datetime = ot_service.parse_datetime

@router.get("/ots")
def list_ots(
    response: Response,
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: Optional[int] = Query(None, ge=1, le=1000, description="Límite de registros por página"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    prioridad: Optional[str] = Query(None, description="Filtrar por prioridad (P1, P2, P3)"),
    tipo_mantenimiento: Optional[str] = Query(None, description="Filtrar por tipo de mantenimiento"),
    search: Optional[str] = Query(None, description="Búsqueda por código, sitio o descripción"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Listar Órdenes de Trabajo según el rol del usuario autenticado.
    Soporta filtros opcionales, paginación y expone cabecera X-Total-Count.
    """
    total = ot_service.count_ots(
        db=db,
        current_user=current_user,
        estado=estado,
        prioridad=prioridad,
        tipo_mantenimiento=tipo_mantenimiento,
        search=search
    )
    response.headers["X-Total-Count"] = str(total)

    data = ot_service.list_ots(
        db=db,
        current_user=current_user,
        skip=skip,
        limit=limit,
        estado=estado,
        prioridad=prioridad,
        tipo_mantenimiento=tipo_mantenimiento,
        search=search
    )
    return {
        "status": "success",
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": data
    }

@router.get("/ots/{ot_id}")
def get_ot_detail(ot_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Obtener detalle de una OT específica con todas sus relaciones.
    """
    data = ot_service.get_ot(db=db, ot_id=ot_id, current_user=current_user)
    return {
        "status": "success",
        "data": data
    }

@router.post("/ots", status_code=status.HTTP_201_CREATED)
def create_ot(
    payload: OtCreate,
    current_user: User = Depends(require_roles(["admin", "administrativo"])),
    db: Session = Depends(get_db)
):
    """
    Registrar una nueva Orden de Trabajo con cálculo automático de SLA.
    """
    data = ot_service.create_ot(db=db, payload=payload, current_user=current_user)
    return {
        "status": "success",
        "message": "Orden de Trabajo registrada con éxito y SLA calculado.",
        "data": data
    }

@router.put("/ots/{ot_id}")
def update_ot(
    ot_id: int,
    payload: OtUpdate,
    current_user: User = Depends(require_roles(["admin", "administrativo"])),
    db: Session = Depends(get_db)
):
    """
    Actualizar datos generales de una Orden de Trabajo.
    """
    data = ot_service.update_ot(db=db, ot_id=ot_id, payload=payload, current_user=current_user)
    return {
        "status": "success",
        "message": "Orden de Trabajo actualizada con éxito.",
        "data": data
    }

@router.put("/ots/{ot_id}/estado")
def update_ot_estado(
    ot_id: int,
    payload: OtEstadoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar el estado operativo de la OT.
    """
    data = ot_service.update_estado(db=db, ot_id=ot_id, payload=payload, current_user=current_user)
    return {
        "status": "success",
        "message": f"Estado de la OT actualizado a '{payload.estado}'.",
        "data": data
    }

@router.put("/ots/{ot_id}/formulario")
def update_formulario(
    ot_id: int,
    payload: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar las respuestas y parámetros del formato técnico de campo (WO / MP).
    Disponible para el personal operativo y administradores.
    """
    data = ot_service.update_formulario(db=db, ot_id=ot_id, payload=payload, current_user=current_user)
    return {
        "status": "success",
        "message": "Formato técnico de campo guardado con éxito.",
        "data": data
    }

@router.post("/ots/{ot_id}/evidencia", status_code=status.HTTP_201_CREATED)
def upload_evidencia(
    ot_id: int,
    payload: EvidenciaCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cargar evidencia fotográfica con validación estricta de seguridad.
    """
    data = ot_service.upload_evidencia(db=db, ot_id=ot_id, payload=payload, current_user=current_user)
    return {
        "status": "success",
        "message": "Evidencia fotográfica guardada con éxito.",
        "data": data
    }

@router.post("/evidencias", status_code=status.HTTP_201_CREATED)
def upload_evidencia_directa(
    payload: EvidenciaCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cargar evidencia fotográfica directamente en /api/evidencias especificando ot_id en el payload.
    """
    if not payload.ot_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Se requiere especificar el campo 'ot_id' en el cuerpo de la petición."
        )
    data = ot_service.upload_evidencia(db=db, ot_id=payload.ot_id, payload=payload, current_user=current_user)
    return {
        "status": "success",
        "message": "Evidencia fotográfica guardada con éxito.",
        "data": data
    }

@router.delete("/evidencias/{evidencia_id}")
def delete_evidencia(
    evidencia_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar evidencia fotográfica.
    """
    return ot_service.delete_evidencia(db=db, evidencia_id=evidencia_id, current_user=current_user)

@router.post("/ots/{ot_id}/repuestos")
def sync_repuestos(
    ot_id: int,
    payload: RepuestoSyncRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Sincronizar repuestos e insumos vinculados a la OT.
    """
    data = ot_service.sync_repuestos(db=db, ot_id=ot_id, payload=payload, current_user=current_user)
    return {
        "status": "success",
        "message": "Insumos y repuestos actualizados con éxito.",
        "data": data
    }

@router.post("/ots/{ot_id}/cerrar")
def cerrar_ot(
    ot_id: int,
    payload: OtCerrarRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cierre técnico de la OT validando evidencias obligatorias.
    """
    data = ot_service.cerrar_ot(db=db, ot_id=ot_id, payload=payload, current_user=current_user)
    return {
        "status": "success",
        "message": "Orden de Trabajo cerrada y solucionada con éxito.",
        "data": data
    }

@router.get("/operadores")
def get_operadores(
    current_user: User = Depends(require_roles(["admin", "administrativo"])),
    db: Session = Depends(get_db)
):
    """
    Listar usuarios con perfil Operativo con su respectiva cuadrilla asignada.
    """
    data = ot_service.get_operadores(db=db)
    return {
        "status": "success",
        "data": data
    }

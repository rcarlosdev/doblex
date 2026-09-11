from typing import List, Any
from fastapi import APIRouter, Depends, status
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
def list_ots(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Listar Órdenes de Trabajo según el rol del usuario autenticado.
    Arquitectura desacoplada delegando en OtService.
    """
    data = ot_service.list_ots(db=db, current_user=current_user)
    return {
        "status": "success",
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

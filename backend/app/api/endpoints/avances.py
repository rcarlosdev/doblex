from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.ot import Ot
from app.models.avance import Avance
from app.schemas.avance import AvanceCreate
from app.api.endpoints.ots import serialize_ot, parse_datetime

router = APIRouter()

@router.post("/avances", status_code=status.HTTP_201_CREATED)
def create_avance(
    payload: AvanceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Registrar un avance diario de obra civil en campo.
    """
    ot = db.query(Ot).filter(Ot.id == payload.ot_id).first()
    if not ot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden de Trabajo no encontrada.")

    # Validar permisos: Asignado directo, cuadrilla asignada, o administradores
    es_asignado_directo = (ot.user_id == current_user.id)
    es_de_cuadrilla = False
    if current_user.empleado and current_user.empleado.cuadrilla_id and ot.cuadrilla_id:
        es_de_cuadrilla = (current_user.empleado.cuadrilla_id == ot.cuadrilla_id)
    es_admin = current_user.role in ["admin", "administrativo"]

    if not es_asignado_directo and not es_de_cuadrilla and not es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No estás autorizado para reportar avances en esta Orden de Trabajo."
        )

    # Validar que no supere el 100%
    nuevo_progreso = ot.progreso + payload.porcentaje
    if nuevo_progreso > 100:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"El avance diario reportado ({payload.porcentaje}%) hace que el progreso acumulado supere el 100% (Progreso actual: {ot.progreso}%)."
        )

    fecha_rep = parse_datetime(payload.fecha_reporte)

    avance = Avance(
        ot_id=ot.id,
        user_id=current_user.id,
        descripcion=payload.descripcion,
        porcentaje=payload.porcentaje,
        fecha_reporte=fecha_rep
    )
    db.add(avance)

    ot.progreso = nuevo_progreso
    if ot.progreso >= 100:
        ot.estado = "finalizada"
    else:
        ot.estado = "en_progreso"

    db.commit()
    db.refresh(avance)
    db.refresh(ot)

    return {
        "status": "success",
        "message": "Avance reportado con éxito y progreso de la OT actualizado.",
        "data": {
            "avance": {
                "id": avance.id,
                "ot_id": avance.ot_id,
                "user_id": avance.user_id,
                "descripcion": avance.descripcion,
                "porcentaje": avance.porcentaje,
                "fecha_reporte": avance.fecha_reporte.isoformat() if avance.fecha_reporte else None,
                "created_at": avance.created_at.isoformat() if avance.created_at else None,
                "user": {
                    "id": current_user.id,
                    "name": current_user.name,
                    "username": current_user.username
                }
            },
            "ot": serialize_ot(ot)
        }
    }

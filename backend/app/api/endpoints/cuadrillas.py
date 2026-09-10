from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.api.deps import get_current_user, require_roles
from app.models.user import User
from app.models.cuadrilla import Cuadrilla
from app.schemas.cuadrilla import CuadrillaCreate, CuadrillaUpdate

router = APIRouter()

def serialize_cuadrilla(c: Cuadrilla) -> dict:
    return {
        "id": c.id,
        "nombre": c.nombre,
        "especialidad": c.especialidad,
        "lider_id": c.lider_id,
        "created_at": c.created_at.isoformat() if c.created_at else None,
        "updated_at": c.updated_at.isoformat() if c.updated_at else None,
        "lider": {
            "id": c.lider.id,
            "name": c.lider.name,
            "username": c.lider.username
        } if c.lider else None,
        "empleados": [
            {
                "id": emp.id,
                "documento": emp.documento,
                "nombre": emp.nombre,
                "cargo": emp.cargo,
                "telefono": emp.telefono,
                "email": emp.email,
                "rol": emp.rol,
                "estado": emp.estado
            }
            for emp in (c.empleados or [])
        ]
    }

@router.get("/cuadrillas")
def list_cuadrillas(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Listar todas las cuadrillas con sus integrantes y líder.
    """
    cuadrillas = db.query(Cuadrilla).options(
        joinedload(Cuadrilla.lider),
        joinedload(Cuadrilla.empleados)
    ).order_by(Cuadrilla.nombre.asc()).all()

    return {
        "status": "success",
        "data": [serialize_cuadrilla(c) for c in cuadrillas]
    }

@router.post("/cuadrillas", status_code=status.HTTP_201_CREATED)
def create_cuadrilla(
    payload: CuadrillaCreate,
    current_user: User = Depends(require_roles(["admin", "administrativo"])),
    db: Session = Depends(get_db)
):
    """
    Crear una nueva cuadrilla.
    """
    cuadrilla = Cuadrilla(
        nombre=payload.nombre,
        especialidad=payload.especialidad,
        lider_id=payload.lider_id
    )
    db.add(cuadrilla)
    db.commit()
    db.refresh(cuadrilla)

    return {
        "status": "success",
        "message": "Cuadrilla creada exitosamente.",
        "data": serialize_cuadrilla(cuadrilla)
    }

@router.put("/cuadrillas/{cuadrilla_id}")
def update_cuadrilla(
    cuadrilla_id: int,
    payload: CuadrillaUpdate,
    current_user: User = Depends(require_roles(["admin", "administrativo"])),
    db: Session = Depends(get_db)
):
    """
    Actualizar una cuadrilla.
    """
    cuadrilla = db.query(Cuadrilla).filter(Cuadrilla.id == cuadrilla_id).first()
    if not cuadrilla:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuadrilla no encontrada.")

    cuadrilla.nombre = payload.nombre
    cuadrilla.especialidad = payload.especialidad
    cuadrilla.lider_id = payload.lider_id

    db.commit()
    db.refresh(cuadrilla)

    return {
        "status": "success",
        "message": "Cuadrilla actualizada exitosamente.",
        "data": serialize_cuadrilla(cuadrilla)
    }

@router.delete("/cuadrillas/{cuadrilla_id}")
def delete_cuadrilla(
    cuadrilla_id: int,
    current_user: User = Depends(require_roles(["admin", "administrativo"])),
    db: Session = Depends(get_db)
):
    """
    Eliminar una cuadrilla.
    """
    cuadrilla = db.query(Cuadrilla).filter(Cuadrilla.id == cuadrilla_id).first()
    if not cuadrilla:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuadrilla no encontrada.")

    db.delete(cuadrilla)
    db.commit()

    return {
        "status": "success",
        "message": "Cuadrilla eliminada exitosamente."
    }

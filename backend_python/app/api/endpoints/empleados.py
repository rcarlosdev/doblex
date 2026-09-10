from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.api.deps import get_current_user, require_roles
from app.models.user import User
from app.models.empleado import Empleado
from app.schemas.empleado import EmpleadoCreate, EmpleadoUpdate

router = APIRouter()

def serialize_empleado(emp: Empleado) -> dict:
    return {
        "id": emp.id,
        "documento": emp.documento,
        "nombre": emp.nombre,
        "cargo": emp.cargo,
        "telefono": emp.telefono,
        "email": emp.email,
        "rol": emp.rol,
        "cuadrilla_id": emp.cuadrilla_id,
        "user_id": emp.user_id,
        "estado": emp.estado,
        "created_at": emp.created_at.isoformat() if emp.created_at else None,
        "updated_at": emp.updated_at.isoformat() if emp.updated_at else None,
        "cuadrilla": {
            "id": emp.cuadrilla.id,
            "nombre": emp.cuadrilla.nombre,
            "especialidad": emp.cuadrilla.especialidad
        } if emp.cuadrilla else None,
        "user": {
            "id": emp.user.id,
            "name": emp.user.name,
            "username": emp.user.username
        } if emp.user else None
    }

@router.get("/empleados")
def list_empleados(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Listar todos los empleados con su cuadrilla y usuario asociado.
    """
    empleados = db.query(Empleado).options(
        joinedload(Empleado.cuadrilla),
        joinedload(Empleado.user)
    ).order_by(Empleado.nombre.asc()).all()

    return {
        "status": "success",
        "data": [serialize_empleado(emp) for emp in empleados]
    }

@router.post("/empleados", status_code=status.HTTP_201_CREATED)
def create_empleado(
    payload: EmpleadoCreate,
    current_user: User = Depends(require_roles(["admin", "administrativo"])),
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo empleado.
    """
    existing = db.query(Empleado).filter(Empleado.documento == payload.documento).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"El documento '{payload.documento}' ya se encuentra registrado."
        )

    empleado = Empleado(
        documento=payload.documento,
        nombre=payload.nombre,
        cargo=payload.cargo,
        telefono=payload.telefono,
        email=payload.email,
        rol=payload.rol,
        cuadrilla_id=payload.cuadrilla_id,
        user_id=payload.user_id,
        estado=payload.estado
    )
    db.add(empleado)
    db.commit()
    db.refresh(empleado)

    return {
        "status": "success",
        "message": "Empleado creado exitosamente.",
        "data": serialize_empleado(empleado)
    }

@router.put("/empleados/{empleado_id}")
def update_empleado(
    empleado_id: int,
    payload: EmpleadoUpdate,
    current_user: User = Depends(require_roles(["admin", "administrativo"])),
    db: Session = Depends(get_db)
):
    """
    Actualizar datos de un empleado.
    """
    empleado = db.query(Empleado).filter(Empleado.id == empleado_id).first()
    if not empleado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado.")

    existing = db.query(Empleado).filter(Empleado.documento == payload.documento, Empleado.id != empleado_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"El documento '{payload.documento}' ya está asignado a otro empleado."
        )

    empleado.documento = payload.documento
    empleado.nombre = payload.nombre
    empleado.cargo = payload.cargo
    empleado.telefono = payload.telefono
    empleado.email = payload.email
    empleado.rol = payload.rol
    empleado.cuadrilla_id = payload.cuadrilla_id
    empleado.user_id = payload.user_id
    empleado.estado = payload.estado

    db.commit()
    db.refresh(empleado)

    return {
        "status": "success",
        "message": "Empleado actualizado exitosamente.",
        "data": serialize_empleado(empleado)
    }

@router.delete("/empleados/{empleado_id}")
def delete_empleado(
    empleado_id: int,
    current_user: User = Depends(require_roles(["admin", "administrativo"])),
    db: Session = Depends(get_db)
):
    """
    Eliminar un empleado.
    """
    empleado = db.query(Empleado).filter(Empleado.id == empleado_id).first()
    if not empleado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado.")

    db.delete(empleado)
    db.commit()

    return {
        "status": "success",
        "message": "Empleado eliminado exitosamente."
    }

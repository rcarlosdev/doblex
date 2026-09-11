from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.api.deps import get_current_user, require_roles
from app.core.security import get_password_hash, validate_password_strength
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
    Crear un nuevo empleado con soporte para habilitar acceso al sistema (crear cuenta de usuario).
    """
    # Seguridad de Roles: Solo un admin puede crear/asignar el rol admin
    if payload.rol == "admin" and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los usuarios con rol 'admin' pueden asignar el rol 'admin'."
        )

    existing = db.query(Empleado).filter(Empleado.documento == payload.documento).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"El documento '{payload.documento}' ya se encuentra registrado."
        )

    assigned_user_id = payload.user_id

    if payload.habilitar_acceso:
        # Validar o generar username
        username = (payload.username or "").strip().lower()
        if not username:
            clean_name = payload.nombre.strip().lower().replace(" ", ".")
            username = clean_name if clean_name else f"user_{payload.documento}"
        
        # Verificar unicidad del username
        user_exists = db.query(User).filter(User.username == username).first()
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"El nombre de usuario '{username}' ya se encuentra registrado. Por favor elija otro."
            )

        # Validar o asignar email
        user_email = (payload.email or "").strip().lower()
        if not user_email:
            user_email = f"{username}@doblex.local"
        else:
            email_exists = db.query(User).filter(User.email == user_email).first()
            if email_exists:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"El correo electrónico '{user_email}' ya está registrado en el sistema."
                )

        # Validar contraseña
        pwd = (payload.password or "").strip()
        if not pwd:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Debe ingresar una contraseña para habilitar el acceso al sistema."
            )
        
        is_valid_pwd, msg_pwd = validate_password_strength(pwd)
        if not is_valid_pwd:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=msg_pwd
            )

        new_user = User(
            name=payload.nombre.strip(),
            username=username,
            email=user_email,
            role=payload.rol,
            password=get_password_hash(pwd)
        )
        db.add(new_user)
        db.flush()
        assigned_user_id = new_user.id

    empleado = Empleado(
        documento=payload.documento.strip(),
        nombre=payload.nombre.strip(),
        cargo=payload.cargo.strip(),
        telefono=payload.telefono.strip() if payload.telefono else None,
        email=payload.email.strip() if payload.email else None,
        rol=payload.rol,
        cuadrilla_id=payload.cuadrilla_id,
        user_id=assigned_user_id,
        estado=payload.estado
    )
    db.add(empleado)
    db.commit()
    
    # Recargar con relaciones
    empleado = db.query(Empleado).options(
        joinedload(Empleado.cuadrilla),
        joinedload(Empleado.user)
    ).filter(Empleado.id == empleado.id).first()

    return {
        "status": "success",
        "message": "Empleado registrado exitosamente" + (" con credenciales de acceso creadas." if payload.habilitar_acceso else "."),
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
    Actualizar datos de un empleado y gestionar/sincronizar sus credenciales de acceso al sistema.
    """
    empleado = db.query(Empleado).filter(Empleado.id == empleado_id).first()
    if not empleado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado.")

    # Seguridad de Roles: Solo un admin puede asignar el rol admin o modificar a un admin existente
    if (payload.rol == "admin" or empleado.rol == "admin") and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los usuarios con rol 'admin' pueden asignar o modificar a un usuario con rol 'admin'."
        )

    existing = db.query(Empleado).filter(Empleado.documento == payload.documento, Empleado.id != empleado_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"El documento '{payload.documento}' ya está asignado a otro empleado."
        )

    if payload.habilitar_acceso:
        if empleado.user_id:
            user = db.query(User).filter(User.id == empleado.user_id).first()
            if user:
                user.name = payload.nombre.strip()
                user.role = payload.rol
                
                if payload.username and payload.username.strip().lower() != user.username:
                    new_uname = payload.username.strip().lower()
                    uname_exists = db.query(User).filter(User.username == new_uname, User.id != user.id).first()
                    if uname_exists:
                        raise HTTPException(
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"El nombre de usuario '{new_uname}' ya está en uso."
                        )
                    user.username = new_uname
                
                if payload.email and payload.email.strip().lower() != user.email:
                    new_email = payload.email.strip().lower()
                    email_exists = db.query(User).filter(User.email == new_email, User.id != user.id).first()
                    if email_exists:
                        raise HTTPException(
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"El correo '{new_email}' ya está registrado por otro usuario."
                        )
                    user.email = new_email
                
                if payload.password and payload.password.strip():
                    is_valid_pwd, msg_pwd = validate_password_strength(payload.password.strip())
                    if not is_valid_pwd:
                        raise HTTPException(
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=msg_pwd
                        )
                    user.password = get_password_hash(payload.password.strip())
        else:
            username = (payload.username or "").strip().lower()
            if not username:
                clean_name = payload.nombre.strip().lower().replace(" ", ".")
                username = clean_name if clean_name else f"user_{payload.documento}"
            
            uname_exists = db.query(User).filter(User.username == username).first()
            if uname_exists:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"El nombre de usuario '{username}' ya está registrado."
                )

            user_email = (payload.email or "").strip().lower()
            if not user_email:
                user_email = f"{username}@doblex.local"
            else:
                email_exists = db.query(User).filter(User.email == user_email).first()
                if email_exists:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail=f"El correo '{user_email}' ya está registrado en el sistema."
                    )

            pwd = (payload.password or "").strip()
            if not pwd:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Debe ingresar una contraseña para habilitar el acceso al sistema."
                )
            
            is_valid_pwd, msg_pwd = validate_password_strength(pwd)
            if not is_valid_pwd:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=msg_pwd
                )

            new_user = User(
                name=payload.nombre.strip(),
                username=username,
                email=user_email,
                role=payload.rol,
                password=get_password_hash(pwd)
            )
            db.add(new_user)
            db.flush()
            empleado.user_id = new_user.id
    elif payload.user_id is not None:
        empleado.user_id = payload.user_id

    empleado.documento = payload.documento.strip()
    empleado.nombre = payload.nombre.strip()
    empleado.cargo = payload.cargo.strip()
    empleado.telefono = payload.telefono.strip() if payload.telefono else None
    empleado.email = payload.email.strip() if payload.email else None
    empleado.rol = payload.rol
    empleado.cuadrilla_id = payload.cuadrilla_id
    empleado.estado = payload.estado

    db.commit()

    empleado = db.query(Empleado).options(
        joinedload(Empleado.cuadrilla),
        joinedload(Empleado.user)
    ).filter(Empleado.id == empleado.id).first()

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

    if empleado.rol == "admin" and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los usuarios con rol 'admin' pueden eliminar a un usuario con rol 'admin'."
        )

    db.delete(empleado)
    db.commit()

    return {
        "status": "success",
        "message": "Empleado eliminado exitosamente."
    }

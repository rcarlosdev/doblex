from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class EmpleadoBase(BaseModel):
    documento: str
    nombre: str
    cargo: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    rol: str = "operativo"  # admin, administrativo, operativo
    cuadrilla_id: Optional[int] = None
    user_id: Optional[int] = None
    estado: str = "activo"  # activo, inactivo

class EmpleadoCreate(EmpleadoBase):
    habilitar_acceso: Optional[bool] = False
    username: Optional[str] = None
    password: Optional[str] = None

class EmpleadoUpdate(EmpleadoBase):
    habilitar_acceso: Optional[bool] = False
    username: Optional[str] = None
    password: Optional[str] = None

class CuadrillaBrief(BaseModel):
    id: int
    nombre: str
    especialidad: Optional[str] = None

    class Config:
        from_attributes = True

class UserBrief(BaseModel):
    id: int
    name: str
    username: str

    class Config:
        from_attributes = True

class EmpleadoResponse(EmpleadoBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    cuadrilla: Optional[CuadrillaBrief] = None
    user: Optional[UserBrief] = None

    class Config:
        from_attributes = True

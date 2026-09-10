from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class CuadrillaBase(BaseModel):
    nombre: str
    especialidad: Optional[str] = None
    lider_id: Optional[int] = None

class CuadrillaCreate(CuadrillaBase):
    pass

class CuadrillaUpdate(CuadrillaBase):
    pass

class LiderBrief(BaseModel):
    id: int
    name: str
    username: str

    class Config:
        from_attributes = True

class EmpleadoInCuadrilla(BaseModel):
    id: int
    documento: str
    nombre: str
    cargo: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    rol: str
    estado: str

    class Config:
        from_attributes = True

class CuadrillaResponse(CuadrillaBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    lider: Optional[LiderBrief] = None
    empleados: List[EmpleadoInCuadrilla] = []

    class Config:
        from_attributes = True

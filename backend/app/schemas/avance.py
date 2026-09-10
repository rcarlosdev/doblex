from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field

class AvanceCreate(BaseModel):
    ot_id: int
    descripcion: str = Field(..., min_length=5)
    porcentaje: int = Field(..., ge=1, le=100)
    fecha_reporte: Any

class UserInAvance(BaseModel):
    id: int
    name: str
    username: str

    class Config:
        from_attributes = True

class AvanceResponse(BaseModel):
    id: int
    ot_id: int
    user_id: int
    descripcion: str
    porcentaje: int
    fecha_reporte: datetime
    created_at: Optional[datetime] = None
    user: Optional[UserInAvance] = None

    class Config:
        from_attributes = True

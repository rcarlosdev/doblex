from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel, Field

class RepuestoItem(BaseModel):
    nombre_item: str
    cantidad: float = Field(..., gt=0)
    unidad_medida: Optional[str] = "unidad"

class RepuestoSyncRequest(BaseModel):
    repuestos: List[RepuestoItem] = []

class RepuestoResponse(BaseModel):
    id: int
    ot_id: int
    nombre_item: str
    cantidad: float
    unidad_medida: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class EvidenciaCreate(BaseModel):
    tipo: str  # antes, durante, despues
    imagen_base64: Optional[str] = None
    imagen_url: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None

class EvidenciaResponse(BaseModel):
    id: int
    ot_id: int
    tipo: str
    url_imagen: str
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    fecha_hora_captura: Optional[datetime] = None

    class Config:
        from_attributes = True

class ActividadResponse(BaseModel):
    id: int
    ot_id: int
    nombre: str
    peso_porcentaje: int
    progreso: int
    estado: str

    class Config:
        from_attributes = True

class UserBrief(BaseModel):
    id: int
    name: str
    username: str

    class Config:
        from_attributes = True

class CuadrillaBrief(BaseModel):
    id: int
    nombre: str
    especialidad: Optional[str] = None

    class Config:
        from_attributes = True

class OtCreate(BaseModel):
    codigo: str
    descripcion: str
    sitio: Optional[str] = None
    ubicacion: str
    user_id: int
    cuadrilla_id: Optional[int] = None
    prioridad: str = "P2"  # P1, P2, P3
    tipo_ubicacion: str = "urbana"  # urbana, rural
    tipo_mantenimiento: str = "correctivo"  # preventivo, correctivo, emergencia
    subsistema: Optional[str] = "sistema_electrico"
    tipo_gasto: Optional[str] = "OPEX"
    fecha_inicio: Any

class OtUpdate(BaseModel):
    codigo: str
    descripcion: str
    sitio: Optional[str] = None
    ubicacion: str
    user_id: int
    cuadrilla_id: Optional[int] = None
    prioridad: str = "P2"
    tipo_ubicacion: str = "urbana"
    tipo_mantenimiento: str = "correctivo"
    subsistema: Optional[str] = "sistema_electrico"
    tipo_gasto: Optional[str] = "OPEX"
    estado: str
    fecha_inicio: Any

class OtEstadoUpdate(BaseModel):
    estado: str  # asignada, en_camino, en_sitio, en_progreso, detenida_materiales, solucionada, finalizada
    progreso: Optional[int] = None

class OtCerrarRequest(BaseModel):
    causa_falla: str  # desgaste, vandalismo, factor_climatico, desconocido
    observaciones_cierre: Optional[str] = None
    repuestos: Optional[List[RepuestoItem]] = []

class OperadorResponse(BaseModel):
    id: int
    name: str
    username: str
    cuadrilla_id: Optional[int] = None

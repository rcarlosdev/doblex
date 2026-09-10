from typing import Optional, List, Any, Dict
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
    tipo: str  # antes, durante, despues, transporte
    imagen_base64: Optional[str] = None
    imagen_url: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    fecha_hora_captura: Optional[Any] = None

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
    id_actividad: Optional[str] = None
    descripcion: str
    sitio: Optional[str] = None
    sitio_id: Optional[int] = None
    ubicacion: str
    user_id: int
    cuadrilla_id: Optional[int] = None
    coordinador: Optional[str] = None
    prioridad: str = "P2"  # P1, P2, P3
    tipo_ubicacion: str = "urbana"  # urbana, rural
    categoria: Optional[str] = "normal"  # normal, rural
    regional: Optional[str] = "R1"  # R1, R2
    departamento: Optional[str] = None
    tipo_estacion: Optional[str] = "MOVIL"
    site_owner: Optional[str] = None
    tipo_mantenimiento: str = "correctivo"  # preventivo, correctivo, emergencia
    tipo_actividad: Optional[str] = "correctivo"  # correctivo, emergencia, preventivo_planta, preventivo_aire
    subsistema: Optional[str] = "sistema_electrico"
    tipo_gasto: Optional[str] = None
    datos_formulario: Optional[Any] = None
    operadores_asignados: Optional[List[Any]] = None
    operadores_ids: Optional[List[int]] = None
    fecha_inicio: Any
    fecha_limite_sla: Optional[Any] = None
    actividades: Optional[List[Any]] = None

class OtUpdate(BaseModel):
    codigo: str
    id_actividad: Optional[str] = None
    descripcion: str
    sitio: Optional[str] = None
    sitio_id: Optional[int] = None
    ubicacion: str
    user_id: int
    cuadrilla_id: Optional[int] = None
    coordinador: Optional[str] = None
    prioridad: str = "P2"
    tipo_ubicacion: str = "urbana"
    categoria: Optional[str] = "normal"
    regional: Optional[str] = "R1"
    departamento: Optional[str] = None
    tipo_estacion: Optional[str] = "MOVIL"
    site_owner: Optional[str] = None
    tipo_mantenimiento: str = "correctivo"
    tipo_actividad: Optional[str] = "correctivo"
    subsistema: Optional[str] = "sistema_electrico"
    tipo_gasto: Optional[str] = None
    datos_formulario: Optional[Any] = None
    operadores_asignados: Optional[List[Any]] = None
    operadores_ids: Optional[List[int]] = None
    estado: str
    fecha_inicio: Any
    fecha_limite_sla: Optional[Any] = None

class OtEstadoUpdate(BaseModel):
    estado: str
    progreso: Optional[int] = None

class OtCerrarRequest(BaseModel):
    causa_falla: str
    observaciones_cierre: str
    repuestos: Optional[List[RepuestoItem]] = []
    datos_formulario: Optional[Any] = None

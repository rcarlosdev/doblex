from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class SitioBase(BaseModel):
    nombre: str
    zona: Optional[str] = None
    zona_tecnica: Optional[str] = None
    ciudad_base: Optional[str] = None
    municipio: Optional[str] = None
    ubicacion: Optional[str] = None
    codigo_transporte_lpu: Optional[str] = None
    km: Optional[float] = None
    km_texto: Optional[str] = None
    transporte_especial: Optional[str] = None
    estructura: Optional[str] = None
    altura_estructura: Optional[float] = None
    altura_estructura_texto: Optional[str] = None
    supervisor_operativo: Optional[str] = None
    correo_so: Optional[str] = None
    jefe_zona: Optional[str] = None
    correo_jefe_zona: Optional[str] = None
    ingeniero_soporte: Optional[str] = None
    correo_ing_soporte: Optional[str] = None
    facturadora: Optional[str] = None
    estado: Optional[str] = "activo"

class SitioCreate(SitioBase):
    pass

class SitioUpdate(BaseModel):
    nombre: Optional[str] = None
    zona: Optional[str] = None
    zona_tecnica: Optional[str] = None
    ciudad_base: Optional[str] = None
    municipio: Optional[str] = None
    ubicacion: Optional[str] = None
    codigo_transporte_lpu: Optional[str] = None
    km: Optional[float] = None
    km_texto: Optional[str] = None
    transporte_especial: Optional[str] = None
    estructura: Optional[str] = None
    altura_estructura: Optional[float] = None
    altura_estructura_texto: Optional[str] = None
    supervisor_operativo: Optional[str] = None
    correo_so: Optional[str] = None
    jefe_zona: Optional[str] = None
    correo_jefe_zona: Optional[str] = None
    ingeniero_soporte: Optional[str] = None
    correo_ing_soporte: Optional[str] = None
    facturadora: Optional[str] = None
    estado: Optional[str] = None

class SitioSummary(BaseModel):
    id: int
    nombre: str
    zona: Optional[str] = None
    zona_tecnica: Optional[str] = None
    municipio: Optional[str] = None
    ciudad_base: Optional[str] = None
    ubicacion: Optional[str] = None
    estructura: Optional[str] = None
    codigo_transporte_lpu: Optional[str] = None
    transporte_especial: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class SitioOut(SitioBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    total_ots: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)

class SitiosListResponse(BaseModel):
    items: List[SitioOut]
    total: int
    page: int
    limit: int
    pages: int

class SitioStatsResponse(BaseModel):
    total_sitios: int
    zonas: dict
    zonas_tecnicas: dict
    estructuras_principales: dict
    con_transporte_especial: int

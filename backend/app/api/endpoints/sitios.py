from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user, require_roles
from app.models.user import User
from app.schemas.sitio import (
    SitioCreate,
    SitioUpdate,
    SitioOut,
    SitioSummary,
    SitiosListResponse,
    SitioStatsResponse
)
from app.services.sitio_service import sitio_service

router = APIRouter()

@router.get("/sitios", response_model=SitiosListResponse)
def list_sitios(
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(25, ge=1, le=100, description="Registros por página"),
    search: Optional[str] = Query(None, description="Búsqueda por nombre, municipio, ubicación o código LPU"),
    zona: Optional[str] = Query(None, description="Filtrar por macro zona (NORTE, COSTA)"),
    zona_tecnica: Optional[str] = Query(None, description="Filtrar por zona técnica"),
    ciudad_base: Optional[str] = Query(None, description="Filtrar por ciudad base"),
    municipio: Optional[str] = Query(None, description="Filtrar por municipio"),
    estructura: Optional[str] = Query(None, description="Filtrar por estructura"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista paginada y filtrada de Sitios (Estaciones Base).
    Arquitectura desacoplada delegando en SitioService y SitioRepository.
    """
    return sitio_service.list_sitios(
        db=db,
        page=page,
        limit=limit,
        search=search,
        zona=zona,
        zona_tecnica=zona_tecnica,
        ciudad_base=ciudad_base,
        municipio=municipio,
        estructura=estructura,
        estado=estado
    )

@router.get("/sitios/select", response_model=List[SitioSummary])
def select_sitios(
    search: Optional[str] = Query(None, description="Término para autocompletar"),
    limit: int = Query(30, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint liviano para dropdowns y autocompletado en la creación/edición de OTs.
    """
    result = sitio_service.search_for_select(db=db, query=search, limit=limit)
    return result["data"]

@router.get("/sitios/stats/resumen", response_model=SitioStatsResponse)
def get_sitios_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Devuelve KPIs e información estadística del catálogo de sitios.
    """
    return sitio_service.get_stats(db=db)

@router.get("/sitios/filtros")
def get_filter_options(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna los valores únicos existentes para poblar los filtros dinámicos del frontend.
    """
    return sitio_service.get_filters(db=db)

@router.get("/sitios/{id}", response_model=SitioOut)
def get_sitio(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el detalle completo de un sitio específico por su ID.
    """
    res = sitio_service.get_sitio(db=db, sitio_id=id)
    return res["data"]

@router.post("/sitios", response_model=SitioOut, status_code=status.HTTP_201_CREATED)
def create_sitio(
    sitio_in: SitioCreate,
    current_user: User = Depends(require_roles(["admin", "administrativo"])),
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo sitio de forma manual (Requiere rol admin o administrativo).
    """
    res = sitio_service.create_sitio(db=db, payload=sitio_in)
    return res["data"]

@router.put("/sitios/{id}", response_model=SitioOut)
def update_sitio(
    id: int,
    sitio_in: SitioUpdate,
    current_user: User = Depends(require_roles(["admin", "administrativo"])),
    db: Session = Depends(get_db)
):
    """
    Actualiza los datos técnicos o de contacto de un sitio existente.
    """
    res = sitio_service.update_sitio(db=db, sitio_id=id, payload=sitio_in)
    return res["data"]

@router.delete("/sitios/{id}")
def delete_sitio(
    id: int,
    current_user: User = Depends(require_roles(["admin"])),
    db: Session = Depends(get_db)
):
    """
    Elimina o desactiva un sitio según si posee historial de OTs.
    """
    return sitio_service.delete_sitio(db=db, sitio_id=id)

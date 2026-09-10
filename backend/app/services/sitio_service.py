import math
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.sitio import Sitio
from app.repositories.sitio_repository import sitio_repository
from app.schemas.sitio import SitioCreate, SitioUpdate

class SitioService:
    @staticmethod
    def serialize_sitio(sitio: Sitio, total_ots: int = 0) -> dict:
        return {
            "id": sitio.id,
            "nombre": sitio.nombre,
            "zona": sitio.zona,
            "zona_tecnica": sitio.zona_tecnica,
            "ciudad_base": sitio.ciudad_base,
            "municipio": sitio.municipio,
            "ubicacion": sitio.ubicacion,
            "codigo_transporte_lpu": sitio.codigo_transporte_lpu,
            "km": sitio.km,
            "km_texto": sitio.km_texto,
            "transporte_especial": sitio.transporte_especial,
            "estructura": sitio.estructura,
            "altura_estructura": sitio.altura_estructura,
            "altura_estructura_texto": sitio.altura_estructura_texto,
            "supervisor_operativo": sitio.supervisor_operativo,
            "new_so": sitio.supervisor_operativo,
            "site_owner": sitio.supervisor_operativo,
            "correo_so": sitio.correo_so,
            "jefe_zona": sitio.jefe_zona,
            "correo_jefe_zona": sitio.correo_jefe_zona,
            "ingeniero_soporte": sitio.ingeniero_soporte,
            "correo_ing_soporte": sitio.correo_ing_soporte,
            "facturadora": sitio.facturadora,
            "estado": sitio.estado,
            "created_at": sitio.created_at.isoformat() if sitio.created_at else None,
            "updated_at": sitio.updated_at.isoformat() if sitio.updated_at else None,
            "total_ots": total_ots
        }

    def list_sitios(
        self,
        db: Session,
        page: int = 1,
        limit: int = 25,
        search: Optional[str] = None,
        zona: Optional[str] = None,
        zona_tecnica: Optional[str] = None,
        ciudad_base: Optional[str] = None,
        municipio: Optional[str] = None,
        estructura: Optional[str] = None,
        estado: Optional[str] = None
    ) -> Dict[str, Any]:
        sitios, total, ots_counts = sitio_repository.filter_and_paginate(
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
        pages = math.ceil(total / limit) if total > 0 else 1
        items = [self.serialize_sitio(s, ots_counts.get(s.id, 0)) for s in sitios]

        return {
            "status": "success",
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages,
            "items": items
        }

    def get_sitio(self, db: Session, sitio_id: int) -> Dict[str, Any]:
        sitio = sitio_repository.get_by_id(db, sitio_id)
        if not sitio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sitio con ID {sitio_id} no encontrado."
            )
        total_ots = sitio_repository.get_ots_count_for_sitio(db, sitio_id)
        return {
            "status": "success",
            "data": self.serialize_sitio(sitio, total_ots)
        }

    def get_stats(self, db: Session) -> Dict[str, Any]:
        return sitio_repository.get_statistics(db)

    def get_filters(self, db: Session) -> Dict[str, List[str]]:
        return sitio_repository.get_distinct_filter_options(db)

    def search_for_select(self, db: Session, query: Optional[str] = None, limit: int = 20) -> Dict[str, Any]:
        sitios = sitio_repository.search_for_select(db, query=query, limit=limit)
        return {
            "status": "success",
            "data": [
                {
                    "id": s.id,
                    "nombre": s.nombre,
                    "zona": s.zona,
                    "zona_tecnica": s.zona_tecnica,
                    "ciudad_base": s.ciudad_base,
                    "municipio": s.municipio,
                    "ubicacion": s.ubicacion,
                    "estructura": s.estructura,
                    "altura_estructura": s.altura_estructura,
                    "codigo_transporte_lpu": s.codigo_transporte_lpu,
                    "km": s.km,
                    "transporte_especial": s.transporte_especial,
                    "supervisor_operativo": s.supervisor_operativo,
                    "new_so": s.supervisor_operativo,
                    "site_owner": s.supervisor_operativo,
                    "jefe_zona": s.jefe_zona,
                    "ingeniero_soporte": s.ingeniero_soporte,
                    "facturadora": s.facturadora
                }
                for s in sitios
            ]
        }

    def create_sitio(self, db: Session, payload: SitioCreate) -> Dict[str, Any]:
        # Validar unicidad del nombre
        existing = sitio_repository.get_by_nombre(db, payload.nombre)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un sitio registrado con el nombre '{payload.nombre}'."
            )

        data = payload.model_dump()
        sitio = Sitio(**data)
        sitio_repository.create(db, sitio)

        return {
            "status": "success",
            "message": "Sitio creado correctamente.",
            "data": self.serialize_sitio(sitio, 0)
        }

    def update_sitio(self, db: Session, sitio_id: int, payload: SitioUpdate) -> Dict[str, Any]:
        sitio = sitio_repository.get_by_id(db, sitio_id)
        if not sitio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sitio con ID {sitio_id} no encontrado."
            )

        update_data = payload.model_dump(exclude_unset=True)
        if "nombre" in update_data and update_data["nombre"] != sitio.nombre:
            existing = sitio_repository.get_by_nombre(db, update_data["nombre"])
            if existing and existing.id != sitio_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe otro sitio con el nombre '{update_data['nombre']}'."
                )

        sitio_repository.update(db, sitio, update_data)
        total_ots = sitio_repository.get_ots_count_for_sitio(db, sitio_id)
        return {
            "status": "success",
            "message": "Sitio actualizado correctamente.",
            "data": self.serialize_sitio(sitio, total_ots)
        }

    def delete_sitio(self, db: Session, sitio_id: int) -> Dict[str, Any]:
        sitio = sitio_repository.get_by_id(db, sitio_id)
        if not sitio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sitio con ID {sitio_id} no encontrado."
            )

        ots_count = sitio_repository.get_ots_count_for_sitio(db, sitio_id)
        if ots_count > 0:
            # Desactivación lógica si tiene órdenes de trabajo asociadas
            sitio.estado = "inactivo"
            db.commit()
            return {
                "status": "success",
                "message": f"El sitio tiene {ots_count} OTs asociadas; se marcó como inactivo en lugar de eliminarse."
            }

        sitio_repository.delete(db, sitio_id)
        return {
            "status": "success",
            "message": f"Sitio con ID {sitio_id} eliminado exitosamente."
        }

sitio_service = SitioService()

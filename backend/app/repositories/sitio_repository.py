from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.models.sitio import Sitio
from app.models.ot import Ot
from app.repositories.base_repository import BaseRepository

class SitioRepository(BaseRepository[Sitio]):
    def __init__(self):
        super().__init__(Sitio)

    def get_by_nombre(self, db: Session, nombre: str) -> Optional[Sitio]:
        return db.query(Sitio).filter(func.lower(Sitio.nombre) == func.lower(nombre.strip())).first()

    def filter_and_paginate(
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
    ) -> Tuple[List[Sitio], int, Dict[int, int]]:
        query = db.query(Sitio)

        if search:
            search_term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Sitio.nombre.ilike(search_term),
                    Sitio.municipio.ilike(search_term),
                    Sitio.ubicacion.ilike(search_term),
                    Sitio.codigo_transporte_lpu.ilike(search_term),
                    Sitio.ciudad_base.ilike(search_term)
                )
            )

        if zona:
            query = query.filter(Sitio.zona == zona.strip())

        if zona_tecnica:
            query = query.filter(Sitio.zona_tecnica == zona_tecnica.strip())

        if ciudad_base:
            query = query.filter(Sitio.ciudad_base == ciudad_base.strip())

        if municipio:
            query = query.filter(Sitio.municipio == municipio.strip())

        if estructura:
            query = query.filter(Sitio.estructura == estructura.strip())

        if estado:
            query = query.filter(Sitio.estado == estado.strip())

        total = query.count()
        offset = (page - 1) * limit
        sitios = query.order_by(Sitio.nombre.asc()).offset(offset).limit(limit).all()

        # Recuento de OTs por sitio para los registros de la página actual
        sitio_ids = [s.id for s in sitios]
        ots_counts: Dict[int, int] = {}
        if sitio_ids:
            counts = (
                db.query(Ot.sitio_id, func.count(Ot.id))
                .filter(Ot.sitio_id.in_(sitio_ids))
                .group_by(Ot.sitio_id)
                .all()
            )
            ots_counts = {cid: cnt for cid, cnt in counts if cid is not None}

        return sitios, total, ots_counts

    def get_ots_count_for_sitio(self, db: Session, sitio_id: int) -> int:
        return db.query(func.count(Ot.id)).filter(Ot.sitio_id == sitio_id).scalar() or 0

    def get_statistics(self, db: Session) -> Dict[str, Any]:
        total_sitios = self.count(db)

        zonas_query = (
            db.query(Sitio.zona, func.count(Sitio.id))
            .filter(Sitio.zona.isnot(None))
            .group_by(Sitio.zona)
            .all()
        )
        zonas = {z: c for z, c in zonas_query if z}

        zt_query = (
            db.query(Sitio.zona_tecnica, func.count(Sitio.id))
            .filter(Sitio.zona_tecnica.isnot(None))
            .group_by(Sitio.zona_tecnica)
            .order_by(func.count(Sitio.id).desc())
            .limit(10)
            .all()
        )
        zonas_tecnicas = {zt: c for zt, c in zt_query if zt}

        est_query = (
            db.query(Sitio.estructura, func.count(Sitio.id))
            .filter(Sitio.estructura.isnot(None))
            .group_by(Sitio.estructura)
            .all()
        )
        estructuras = {e: c for e, c in est_query if e}

        con_transporte_especial = (
            db.query(func.count(Sitio.id))
            .filter(
                Sitio.transporte_especial.isnot(None),
                Sitio.transporte_especial != "",
                Sitio.transporte_especial != "NO",
                Sitio.transporte_especial != "None"
            )
            .scalar() or 0
        )

        return {
            "total_sitios": total_sitios,
            "zonas": zonas,
            "zonas_tecnicas": zonas_tecnicas,
            "estructuras_principales": estructuras,
            "con_transporte_especial": con_transporte_especial
        }

    def get_distinct_filter_options(self, db: Session) -> Dict[str, List[str]]:
        zonas = [r[0] for r in db.query(Sitio.zona).distinct().filter(Sitio.zona.isnot(None)).order_by(Sitio.zona).all() if r[0]]
        zonas_tecnicas = [r[0] for r in db.query(Sitio.zona_tecnica).distinct().filter(Sitio.zona_tecnica.isnot(None)).order_by(Sitio.zona_tecnica).all() if r[0]]
        ciudades = [r[0] for r in db.query(Sitio.ciudad_base).distinct().filter(Sitio.ciudad_base.isnot(None)).order_by(Sitio.ciudad_base).all() if r[0]]
        estructuras = [r[0] for r in db.query(Sitio.estructura).distinct().filter(Sitio.estructura.isnot(None)).order_by(Sitio.estructura).all() if r[0]]

        return {
            "zonas": zonas,
            "zonas_tecnicas": zonas_tecnicas,
            "ciudades_base": ciudades,
            "estructuras": estructuras
        }

    def search_for_select(self, db: Session, query: Optional[str] = None, limit: int = 20) -> List[Sitio]:
        q = db.query(Sitio).filter(Sitio.estado == "activo")
        if query and query.strip():
            term = f"%{query.strip()}%"
            q = q.filter(
                or_(
                    Sitio.nombre.ilike(term),
                    Sitio.municipio.ilike(term),
                    Sitio.ubicacion.ilike(term)
                )
            )
        return q.order_by(Sitio.nombre.asc()).limit(limit).all()

sitio_repository = SitioRepository()

from typing import Optional, List, Any
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import or_, func

from app.models.ot import Ot
from app.models.actividad_ot import ActividadOt
from app.models.evidencia import EvidenciaFotografica
from app.models.repuesto import RepuestoUtilizado
from app.models.avance import Avance
from app.models.user import User
from app.repositories.base_repository import BaseRepository

class OtRepository(BaseRepository[Ot]):
    def __init__(self):
        super().__init__(Ot)

    def get_by_codigo(self, db: Session, codigo: str) -> Optional[Ot]:
        return db.query(Ot).filter(func.lower(Ot.codigo) == func.lower(codigo.strip())).first()

    def get_with_relations(self, db: Session, ot_id: int) -> Optional[Ot]:
        return db.query(Ot).options(
            joinedload(Ot.assigned_user),
            joinedload(Ot.creator),
            joinedload(Ot.cuadrilla),
            selectinload(Ot.actividades),
            selectinload(Ot.evidencias),
            selectinload(Ot.repuestos),
            selectinload(Ot.avances)
        ).filter(Ot.id == ot_id).first()

    def _apply_role_and_filters(
        self,
        query,
        current_user: User,
        estado: Optional[str] = None,
        prioridad: Optional[str] = None,
        tipo_mantenimiento: Optional[str] = None,
        search: Optional[str] = None
    ):
        if current_user.role in ["admin", "administrativo"]:
            pass
        elif current_user.role == "operativo":
            user_cuadrilla_id = current_user.empleado.cuadrilla_id if current_user.empleado else None
            if user_cuadrilla_id:
                query = query.filter(
                    or_(Ot.user_id == current_user.id, Ot.cuadrilla_id == user_cuadrilla_id)
                )
            else:
                query = query.filter(Ot.user_id == current_user.id)
        else:
            return None

        if estado:
            query = query.filter(Ot.estado == estado.strip())

        if prioridad:
            query = query.filter(Ot.prioridad == prioridad.strip())

        if tipo_mantenimiento:
            query = query.filter(Ot.tipo_mantenimiento == tipo_mantenimiento.strip())

        if search:
            search_pattern = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Ot.codigo.ilike(search_pattern),
                    Ot.descripcion.ilike(search_pattern),
                    Ot.sitio.ilike(search_pattern),
                    Ot.ubicacion.ilike(search_pattern)
                )
            )

        return query

    def list_by_role(
        self,
        db: Session,
        current_user: User,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        estado: Optional[str] = None,
        prioridad: Optional[str] = None,
        tipo_mantenimiento: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Ot]:
        query = db.query(Ot).options(
            joinedload(Ot.assigned_user),
            joinedload(Ot.creator),
            joinedload(Ot.cuadrilla),
            selectinload(Ot.actividades),
            selectinload(Ot.evidencias),
            selectinload(Ot.repuestos),
            selectinload(Ot.avances)
        ).order_by(Ot.created_at.desc())

        filtered_query = self._apply_role_and_filters(
            query=query,
            current_user=current_user,
            estado=estado,
            prioridad=prioridad,
            tipo_mantenimiento=tipo_mantenimiento,
            search=search
        )

        if filtered_query is None:
            return []

        if skip is not None and skip > 0:
            filtered_query = filtered_query.offset(skip)

        if limit is not None and limit > 0:
            filtered_query = filtered_query.limit(limit)

        return filtered_query.all()

    def count_by_role(
        self,
        db: Session,
        current_user: User,
        estado: Optional[str] = None,
        prioridad: Optional[str] = None,
        tipo_mantenimiento: Optional[str] = None,
        search: Optional[str] = None
    ) -> int:
        query = db.query(func.count(Ot.id))
        filtered_query = self._apply_role_and_filters(
            query=query,
            current_user=current_user,
            estado=estado,
            prioridad=prioridad,
            tipo_mantenimiento=tipo_mantenimiento,
            search=search
        )

        if filtered_query is None:
            return 0

        return filtered_query.scalar() or 0

ot_repository = OtRepository()

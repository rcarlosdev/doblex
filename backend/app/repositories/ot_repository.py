from typing import Optional, List, Any
from sqlalchemy.orm import Session, joinedload
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
            joinedload(Ot.actividades),
            joinedload(Ot.evidencias),
            joinedload(Ot.repuestos),
            joinedload(Ot.avances)
        ).filter(Ot.id == ot_id).first()

    def list_by_role(
        self,
        db: Session,
        current_user: User,
        skip: Optional[int] = None,
        limit: Optional[int] = None
    ) -> List[Ot]:
        query = db.query(Ot).options(
            joinedload(Ot.assigned_user),
            joinedload(Ot.creator),
            joinedload(Ot.cuadrilla),
            joinedload(Ot.actividades),
            joinedload(Ot.evidencias),
            joinedload(Ot.repuestos),
            joinedload(Ot.avances)
        ).order_by(Ot.created_at.desc())

        if current_user.role == "admin":
            pass
        elif current_user.role == "administrativo":
            query = query.filter(Ot.created_by == current_user.id)
        elif current_user.role == "operativo":
            user_cuadrilla_id = current_user.empleado.cuadrilla_id if current_user.empleado else None
            if user_cuadrilla_id:
                query = query.filter(
                    or_(Ot.user_id == current_user.id, Ot.cuadrilla_id == user_cuadrilla_id)
                )
            else:
                query = query.filter(Ot.user_id == current_user.id)
        else:
            return []

        if skip is not None and limit is not None:
            query = query.offset(skip).limit(limit)

        return query.all()

    def count_by_role(self, db: Session, current_user: User) -> int:
        query = db.query(func.count(Ot.id))
        if current_user.role == "admin":
            pass
        elif current_user.role == "administrativo":
            query = query.filter(Ot.created_by == current_user.id)
        elif current_user.role == "operativo":
            user_cuadrilla_id = current_user.empleado.cuadrilla_id if current_user.empleado else None
            if user_cuadrilla_id:
                query = query.filter(
                    or_(Ot.user_id == current_user.id, Ot.cuadrilla_id == user_cuadrilla_id)
                )
            else:
                query = query.filter(Ot.user_id == current_user.id)
        else:
            return 0

        return query.scalar() or 0

ot_repository = OtRepository()

from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

ModelType = TypeVar("ModelType", bound=Any)

class BaseRepository(Generic[ModelType]):
    """
    Repositorio base genérico que encapsula operaciones CRUD comunes
    y patrones de consulta sobre modelos de SQLAlchemy 2.0.
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_by_id(self, db: Session, id: Any) -> Optional[ModelType]:
        id_col = getattr(self.model, "id")
        return db.query(self.model).filter(id_col == id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def count(self, db: Session) -> int:
        id_col = getattr(self.model, "id")
        return db.query(func.count(id_col)).scalar() or 0

    def create(self, db: Session, obj: ModelType) -> ModelType:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: ModelType, update_data: dict) -> ModelType:
        for field, value in update_data.items():
            if hasattr(db_obj, field) and value is not None:
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: Any) -> bool:
        obj = self.get_by_id(db, id)
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.core.utils import now_colombia

class Cuadrilla(Base):
    __tablename__ = "cuadrillas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    especialidad = Column(String(255), nullable=True)
    lider_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=now_colombia)
    updated_at = Column(DateTime, default=now_colombia, onupdate=now_colombia)

    # Relaciones
    lider = relationship("User", back_populates="cuadrillas_lideradas")
    empleados = relationship("Empleado", back_populates="cuadrilla")
    ots = relationship("Ot", back_populates="cuadrilla")

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Cuadrilla(Base):
    __tablename__ = "cuadrillas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    especialidad = Column(String(255), nullable=True)
    lider_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    lider = relationship("User", back_populates="cuadrillas_lideradas")
    empleados = relationship("Empleado", back_populates="cuadrilla")
    ots = relationship("Ot", back_populates="cuadrilla")

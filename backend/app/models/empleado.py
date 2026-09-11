from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.core.utils import now_colombia

class Empleado(Base):
    __tablename__ = "empleados"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    documento = Column(String(50), unique=True, index=True, nullable=False)
    nombre = Column(String(255), nullable=False)
    cargo = Column(String(255), nullable=False)
    telefono = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    rol = Column(String(50), nullable=False, default="operativo")  # admin, administrativo, operativo
    cuadrilla_id = Column(Integer, ForeignKey("cuadrillas.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    estado = Column(String(20), nullable=False, default="activo")  # activo, inactivo
    created_at = Column(DateTime, default=now_colombia)
    updated_at = Column(DateTime, default=now_colombia, onupdate=now_colombia)

    # Relaciones
    cuadrilla = relationship("Cuadrilla", back_populates="empleados")
    user = relationship("User", back_populates="empleado")

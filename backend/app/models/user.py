from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.core.utils import now_utc
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    role = Column(String(50), nullable=False, default="operativo")  # admin, administrativo, operativo
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=now_utc)
    updated_at = Column(DateTime, default=now_utc, onupdate=now_utc)

    # Relaciones
    empleado = relationship("Empleado", back_populates="user", uselist=False)
    ots_asignadas = relationship("Ot", back_populates="assigned_user", foreign_keys="Ot.user_id")
    ots_creadas = relationship("Ot", back_populates="creator", foreign_keys="Ot.created_by")
    cuadrillas_lideradas = relationship("Cuadrilla", back_populates="lider")
    avances = relationship("Avance", back_populates="user")

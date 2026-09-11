from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.core.utils import now_colombia

class RepuestoUtilizado(Base):
    __tablename__ = "repuestos_utilizados"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ot_id = Column(Integer, ForeignKey("ots.id", ondelete="CASCADE"), nullable=False)
    nombre_item = Column(String(255), nullable=False)
    cantidad = Column(Float, nullable=False, default=1.0)
    unidad_medida = Column(String(50), nullable=False, default="unidad")
    created_at = Column(DateTime, default=now_colombia)
    updated_at = Column(DateTime, default=now_colombia, onupdate=now_colombia)

    # Relaciones
    ot = relationship("Ot", back_populates="repuestos")

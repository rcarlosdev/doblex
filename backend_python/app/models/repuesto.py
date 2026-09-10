from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class RepuestoUtilizado(Base):
    __tablename__ = "repuestos_utilizados"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ot_id = Column(Integer, ForeignKey("ots.id", ondelete="CASCADE"), nullable=False)
    nombre_item = Column(String(255), nullable=False)
    cantidad = Column(Float, nullable=False, default=1.0)
    unidad_medida = Column(String(50), nullable=False, default="unidad")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    ot = relationship("Ot", back_populates="repuestos")

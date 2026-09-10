from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class ActividadOt(Base):
    __tablename__ = "actividades_ot"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ot_id = Column(Integer, ForeignKey("ots.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(255), nullable=False)
    peso_porcentaje = Column(Integer, default=0)
    progreso = Column(Integer, default=0)
    estado = Column(String(50), default="pendiente")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    ot = relationship("Ot", back_populates="actividades")

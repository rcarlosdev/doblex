from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.core.utils import now_colombia

class EvidenciaFotografica(Base):
    __tablename__ = "evidencias_fotograficas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ot_id = Column(Integer, ForeignKey("ots.id", ondelete="CASCADE"), nullable=False)
    tipo = Column(String(50), nullable=False)  # antes, durante, despues
    url_imagen = Column(Text, nullable=False)
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)
    fecha_hora_captura = Column(DateTime, default=now_colombia)
    created_at = Column(DateTime, default=now_colombia)
    updated_at = Column(DateTime, default=now_colombia, onupdate=now_colombia)

    # Relaciones
    ot = relationship("Ot", back_populates="evidencias")

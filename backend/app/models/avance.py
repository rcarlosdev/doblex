from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Avance(Base):
    __tablename__ = "avances"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ot_id = Column(Integer, ForeignKey("ots.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    descripcion = Column(Text, nullable=False)
    porcentaje = Column(Integer, nullable=False)
    fecha_reporte = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    ot = relationship("Ot", back_populates="avances")
    user = relationship("User", back_populates="avances")

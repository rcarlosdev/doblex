from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.utils import now_utc
from app.db.base import Base

class Ot(Base):
    __tablename__ = "ots"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo = Column(String(50), unique=True, index=True, nullable=False)
    descripcion = Column(Text, nullable=False)
    sitio = Column(String(255), nullable=True)
    sitio_id = Column(Integer, ForeignKey("sitios.id"), nullable=True, index=True)
    ubicacion = Column(String(255), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cuadrilla_id = Column(Integer, ForeignKey("cuadrillas.id"), nullable=True)
    progreso = Column(Integer, nullable=False, default=0)
    estado = Column(String(50), nullable=False, default="asignada")  # asignada, en_camino, en_sitio, en_progreso, detenida_materiales, solucionada, finalizada
    prioridad = Column(String(10), nullable=False, default="P2")     # P1, P2, P3
    tipo_ubicacion = Column(String(20), nullable=False, default="urbana")  # urbana, rural
    tipo_mantenimiento = Column(String(30), nullable=False, default="correctivo")  # preventivo, correctivo, emergencia
    subsistema = Column(String(100), nullable=True, default="sistema_electrico")
    tipo_gasto = Column(String(20), nullable=True, default="OPEX")  # OPEX, CAPEX
    fecha_inicio = Column(DateTime, nullable=False, default=now_utc)
    fecha_limite_sla = Column(DateTime, nullable=True)
    fecha_llegada_sitio = Column(DateTime, nullable=True)
    fecha_solucion = Column(DateTime, nullable=True)
    causa_falla = Column(String(100), nullable=True)
    observaciones_cierre = Column(Text, nullable=True)
    created_at = Column(DateTime, default=now_utc)
    updated_at = Column(DateTime, default=now_utc, onupdate=now_utc)

    # Relaciones
    sitio_rel = relationship("Sitio", back_populates="ots")
    assigned_user = relationship("User", foreign_keys=[user_id], back_populates="ots_asignadas")
    creator = relationship("User", foreign_keys=[created_by], back_populates="ots_creadas")
    cuadrilla = relationship("Cuadrilla", back_populates="ots")
    actividades = relationship("ActividadOt", back_populates="ot", cascade="all, delete-orphan")
    evidencias = relationship("EvidenciaFotografica", back_populates="ot", cascade="all, delete-orphan")
    repuestos = relationship("RepuestoUtilizado", back_populates="ot", cascade="all, delete-orphan")
    avances = relationship("Avance", back_populates="ot", cascade="all, delete-orphan")

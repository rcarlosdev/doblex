from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.orm import relationship
from app.core.utils import now_utc
from app.db.base import Base

class Sitio(Base):
    __tablename__ = "sitios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255), unique=True, index=True, nullable=False)
    zona = Column(String(50), index=True, nullable=True)                  # NORTE, COSTA
    zona_tecnica = Column(String(100), index=True, nullable=True)          # ANTIOQUIA, CHOCO Y ANTIOQUIA, CORDOBA-1, etc.
    ciudad_base = Column(String(100), index=True, nullable=True)           # RIONEGRO, MEDELLIN, FRONTINO, etc.
    municipio = Column(String(100), index=True, nullable=True)             # Abejorral, Apartado, Medellin, etc.
    ubicacion = Column(Text, nullable=True)                               # Dirección o referencia física
    codigo_transporte_lpu = Column(String(255), nullable=True)            # Código contractual LPU de transporte
    km = Column(Float, nullable=True)                                     # Distancia en Km calculada/limpia
    km_texto = Column(String(50), nullable=True)                          # Texto original si contiene notas
    transporte_especial = Column(String(255), nullable=True)              # MULAR X2, AYUDANTIA 60, etc.
    estructura = Column(String(100), nullable=True)                       # Poste, Torre, Indoor, C1, etc.
    altura_estructura = Column(Float, nullable=True)                      # Altura en metros para SST
    altura_estructura_texto = Column(String(50), nullable=True)           # Texto original
    supervisor_operativo = Column(String(255), nullable=True)             # New_SO Claro asignado
    correo_so = Column(String(255), nullable=True)
    jefe_zona = Column(String(255), nullable=True)                        # Jefe de Zona Claro
    correo_jefe_zona = Column(String(255), nullable=True)
    ingeniero_soporte = Column(String(255), nullable=True)                # Ing. Soporte Claro
    correo_ing_soporte = Column(String(255), nullable=True)
    facturadora = Column(String(100), nullable=True)                      # Responsable facturación
    estado = Column(String(50), default="activo", index=True, nullable=False) # activo, inactivo
    created_at = Column(DateTime, default=now_utc)
    updated_at = Column(DateTime, default=now_utc, onupdate=now_utc)

    # Relación con Órdenes de Trabajo (OTs)
    ots = relationship("Ot", back_populates="sitio_rel", cascade="all")

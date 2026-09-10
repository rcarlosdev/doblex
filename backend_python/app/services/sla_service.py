from datetime import datetime, timedelta
from typing import Optional
from app.core.utils import now_utc

class SLAService:
    """
    Servicio de cálculo de tiempos de SLA para Órdenes de Trabajo (SMU).
    """
    SLA_MATRIX = {
        "P1": {
            "urbana": 4 * 60 + 30,   # 4h 30m = 270 min
            "rural": 11 * 60 + 42,   # 11h 42m = 702 min
        },
        "P2": {
            "urbana": 6 * 60,        # 6h 00m = 360 min
            "rural": 12 * 60,        # 12h 00m = 720 min
        },
        "P3": {
            "urbana": 12 * 60,       # 12h 00m = 720 min
            "rural": 20 * 60,        # 20h 00m = 1200 min
        },
    }

    @classmethod
    def calcular_fecha_limite(cls, prioridad: str, tipo_ubicacion: str, fecha_apertura: Optional[datetime] = None) -> datetime:
        fecha_inicio = fecha_apertura if fecha_apertura else now_utc()
        prioridad_key = (prioridad or "P2").strip().upper()
        ubicacion_key = (tipo_ubicacion or "urbana").strip().lower()

        minutos = cls.SLA_MATRIX.get(prioridad_key, {}).get(ubicacion_key, 12 * 60)
        return fecha_inicio + timedelta(minutes=minutos)

sla_service = SLAService()

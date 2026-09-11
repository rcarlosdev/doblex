from datetime import datetime, timezone, timedelta
from typing import Optional
from zoneinfo import ZoneInfo
from app.core.config import settings

# Zona horaria oficial de Colombia (America/Bogota, UTC-5)
TIMEZONE_COLOMBIA_STR = getattr(settings, "TIMEZONE", "America/Bogota")
try:
    COLOMBIA_TZ = ZoneInfo(TIMEZONE_COLOMBIA_STR)
except Exception:
    COLOMBIA_TZ = timezone(timedelta(hours=-5), name="America/Bogota")

def now_colombia() -> datetime:
    """
    Retorna la fecha y hora actual en la zona horaria oficial de Colombia (America/Bogota, UTC-5).
    Se retorna naive (sin tzinfo) para compatibilidad nativa y consistente con SQLite y PostgreSQL.
    """
    return datetime.now(COLOMBIA_TZ).replace(tzinfo=None)

def now_colombia_tz() -> datetime:
    """
    Retorna la fecha y hora actual en Colombia conservando tzinfo (aware).
    """
    return datetime.now(COLOMBIA_TZ)

# Alias para compatibilidad con código existente
now_utc = now_colombia

def to_colombia_datetime(dt: Optional[datetime]) -> Optional[datetime]:
    """
    Convierte cualquier datetime a la hora local de Colombia en formato naive para la base de datos.
    """
    if not dt:
        return None
    if dt.tzinfo is not None:
        return dt.astimezone(COLOMBIA_TZ).replace(tzinfo=None)
    return dt

def to_iso_colombia(dt: Optional[datetime]) -> Optional[str]:
    """
    Serializa un datetime a formato ISO-8601 con el offset oficial de Colombia (-05:00).
    """
    if not dt:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=COLOMBIA_TZ)
    else:
        dt = dt.astimezone(COLOMBIA_TZ)
    return dt.isoformat()

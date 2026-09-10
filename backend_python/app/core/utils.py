from datetime import datetime, timezone

def now_utc() -> datetime:
    """
    Retorna la fecha y hora actual en UTC compatible con Python 3.13+.
    """
    return datetime.now(timezone.utc)

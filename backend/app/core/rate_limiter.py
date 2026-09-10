import time
import threading
from typing import Dict, List, Callable
from fastapi import Request, HTTPException, status
from app.core.config import settings

class SlidingWindowRateLimiter:
    """
    Limitador de tasa (Rate Limiter) en memoria de alto rendimiento y thread-safe.
    Implementa el algoritmo de ventana deslizante (Sliding Window Log).
    """
    def __init__(self):
        self._lock = threading.Lock()
        self._records: Dict[str, List[float]] = {}

    def is_allowed(self, key: str, max_requests: int, window_seconds: int) -> tuple[bool, int]:
        """
        Verifica si la petición actual está permitida para la clave dada.
        Retorna (permitido, segundos_para_reintentar).
        """
        if not getattr(settings, "SECURITY_RATE_LIMIT_ENABLED", True):
            return True, 0

        now = time.time()
        window_start = now - window_seconds

        with self._lock:
            timestamps = self._records.get(key, [])
            # Filtrar registros anteriores al inicio de la ventana
            timestamps = [t for t in timestamps if t > window_start]

            if len(timestamps) >= max_requests:
                # Calcular el tiempo de espera restante antes de que el intento más antiguo expire
                oldest_timestamp = timestamps[0]
                retry_after = max(1, int(oldest_timestamp + window_seconds - now))
                self._records[key] = timestamps
                return False, retry_after

            # Registrar la petición actual
            timestamps.append(now)
            self._records[key] = timestamps
            return True, 0

    def cleanup(self):
        """
        Limpia claves cuyos registros han expirado para evitar fugas de memoria.
        """
        now = time.time()
        with self._lock:
            keys_to_delete = []
            for key, timestamps in self._records.items():
                active = [t for t in timestamps if t > now - 3600]
                if not active:
                    keys_to_delete.append(key)
                else:
                    self._records[key] = active
            for k in keys_to_delete:
                del self._records[k]

# Instancia singleton del limitador
rate_limiter = SlidingWindowRateLimiter()

def get_client_ip(request: Request) -> str:
    """
    Obtiene la dirección IP real del cliente considerando cabeceras de proxy inverso.
    """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # Tomar la IP del cliente original (la primera de la lista separada por comas)
        client_ip = forwarded.split(",")[0].strip()
        if client_ip:
            return client_ip

    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()

    if request.client and request.client.host:
        return request.client.host

    return "127.0.0.1"

def rate_limit(max_requests: int = 60, window_seconds: int = 60) -> Callable:
    """
    Generador de dependencia FastAPI para aplicar rate limiting por IP y ruta.
    """
    async def dependency(request: Request):
        ip = get_client_ip(request)
        endpoint = request.url.path
        key = f"{endpoint}:{ip}"

        allowed, retry_after = rate_limiter.is_allowed(key, max_requests, window_seconds)
        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Demasiadas peticiones. Por favor espere {retry_after} segundos antes de intentar nuevamente.",
                headers={"Retry-After": str(retry_after)}
            )
        return True

    return dependency

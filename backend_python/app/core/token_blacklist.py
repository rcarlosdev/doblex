import time
import hashlib
import threading
from typing import Dict, Optional

class TokenBlacklist:
    """
    Lista negra de tokens JWT en memoria, thread-safe.
    Almacena hashes SHA-256 de los tokens revocados hasta su expiración natural.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self._revoked_tokens: Dict[str, float] = {}  # {token_hash: exp_timestamp}

    def _hash_token(self, token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def revoke_token(self, token: str, exp_timestamp: Optional[float] = None):
        """
        Revoca un token y lo añade a la lista negra.
        Si no se proporciona exp_timestamp, expira en 24 horas por defecto.
        """
        if not token:
            return

        token_hash = self._hash_token(token)
        now = time.time()
        expiry = exp_timestamp if exp_timestamp and exp_timestamp > now else now + 86400

        with self._lock:
            self._revoked_tokens[token_hash] = expiry

    def is_token_revoked(self, token: str) -> bool:
        """
        Comprueba si un token ha sido revocado.
        """
        if not token:
            return False

        token_hash = self._hash_token(token)
        now = time.time()

        with self._lock:
            expiry = self._revoked_tokens.get(token_hash)
            if expiry is None:
                return False

            if expiry < now:
                # El token ya expiró de forma natural, eliminar de la lista negra
                del self._revoked_tokens[token_hash]
                return False

            return True

    def cleanup(self):
        """
        Elimina entradas expiradas.
        """
        now = time.time()
        with self._lock:
            expired_keys = [k for k, exp in self._revoked_tokens.items() if exp < now]
            for k in expired_keys:
                del self._revoked_tokens[k]

# Instancia singleton de la lista negra
token_blacklist = TokenBlacklist()

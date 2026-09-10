from datetime import datetime, timedelta, timezone
from typing import Optional, Any
import bcrypt
import jwt
from app.core.config import settings

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica una contraseña en texto plano contra un hash bcrypt.
    Soporta los hashes de Laravel que inician con $2y$ convirtiéndolos a $2b$.
    """
    if not hashed_password or not plain_password:
        return False
    
    formatted_hash = hashed_password
    if formatted_hash.startswith("$2y$"):
        formatted_hash = "$2b$" + formatted_hash[4:]
    
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), formatted_hash.encode("utf-8"))
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """
    Genera un hash seguro usando bcrypt.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT firmado.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodifica y valida un token JWT con fijación estricta del algoritmo y verificación de expiración.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_signature": True, "verify_exp": True, "require": ["exp", "sub"]}
        )
        return payload
    except jwt.PyJWTError:
        return None

def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Valida que una contraseña cumpla con criterios mínimos de seguridad empresarial:
    - Mínimo 8 caracteres
    - Al menos una letra
    - Al menos un número
    """
    if not password or len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres."
    if not any(c.isalpha() for c in password):
        return False, "La contraseña debe contener al menos una letra."
    if not any(c.isdigit() for c in password):
        return False, "La contraseña debe contener al menos un número."
    return True, ""


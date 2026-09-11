from typing import List, Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_access_token
from app.core.token_blacklist import token_blacklist
from app.models.user import User

security_bearer = HTTPBearer(auto_error=False)

def extract_auth_token(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = None
) -> Optional[str]:
    """
    Estrategia de extracción de token multi-capa altamente resiliente ante proxies
    (Cloudflare, Google Cloud Load Balancer, PandaStack, Vercel, Nginx).
    """
    # 1. Credenciales estándar de FastAPI HTTPBearer
    if credentials and credentials.credentials:
        return credentials.credentials.strip()

    # 2. Header Authorization estándar o normalizado
    auth = request.headers.get("Authorization") or request.headers.get("authorization")
    if auth:
        if auth.lower().startswith("bearer "):
            return auth.split(" ", 1)[1].strip()
        return auth.strip()

    # 3. Header X-Authorization (evita filtros de proxies en cabeceras estándar)
    x_auth = request.headers.get("X-Authorization") or request.headers.get("x-authorization")
    if x_auth:
        if x_auth.lower().startswith("bearer "):
            return x_auth.split(" ", 1)[1].strip()
        return x_auth.strip()

    # 4. Headers X-Access-Token y X-Token
    for h in ["X-Access-Token", "x-access-token", "X-Token", "x-token"]:
        token_val = request.headers.get(h)
        if token_val:
            return token_val.strip()

    # 5. Cookies de sesión
    for c in ["smu_token", "access_token"]:
        cookie_val = request.cookies.get(c)
        if cookie_val:
            return cookie_val.strip()

    # 6. Parámetros de consulta (Query Params)
    for q in ["token", "access_token"]:
        query_val = request.query_params.get(q)
        if query_val:
            return query_val.strip()

    return None

def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer),
    db: Session = Depends(get_db)
) -> User:
    """
    Extrae y valida el token Bearer del header Authorization o cabeceras alternativas.
    Verifica firma criptográfica, expiración y estado de revocación en lista negra.
    """
    token = extract_auth_token(request, credentials)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se proporcionó token de autenticación.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Validar si el token fue revocado en /logout
    if token_blacklist.is_token_revoked(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token de sesión ha sido revocado. Inicie sesión nuevamente.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    
    username: Optional[str] = payload.get("username")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: falta información de usuario.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado en la base de datos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def require_roles(allowed_roles: List[str]):
    """
    Verifica que el usuario actual tenga al menos uno de los roles permitidos.
    """
    def role_checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos suficientes para realizar esta acción."
            )
        return user
    return role_checker

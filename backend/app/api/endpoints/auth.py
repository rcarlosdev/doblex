import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.config import settings
from app.core.security import verify_password, create_access_token, decode_access_token
from app.core.rate_limiter import rate_limit, get_client_ip
from app.core.token_blacklist import token_blacklist
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse, UserInfo
from app.api.deps import get_current_user, security_bearer

router = APIRouter()
logger = logging.getLogger("security.auth")

@router.post(
    "/login",
    response_model=LoginResponse,
    dependencies=[Depends(rate_limit(max_requests=settings.LOGIN_RATE_LIMIT_MAX, window_seconds=settings.LOGIN_RATE_LIMIT_WINDOW))]
)
def login(request_body: LoginRequest, request: Request, db: Session = Depends(get_db)):
    """
    Iniciar sesión con username y password.
    Protegido con limitación de tasa (Rate Limiting) anti-fuerza bruta y registro de auditoría.
    """
    client_ip = get_client_ip(request)
    user = db.query(User).filter(User.username == request_body.username).first()

    if not user or not verify_password(request_body.password, user.password):
        logger.warning(
            f"FALLO DE AUTENTICACION: Intento inválido para usuario='{request_body.username}' desde IP='{client_ip}'"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Las credenciales proporcionadas son incorrectas."
        )

    token = create_access_token(data={
        "sub": str(user.id),
        "username": user.username,
        "role": user.role
    })

    logger.info(
        f"AUTENTICACION EXITOSA: Usuario='{user.username}' rol='{user.role}' desde IP='{client_ip}'"
    )

    return {
        "status": "success",
        "token": token,
        "user": {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "role": user.role,
            "email": user.email
        }
    }

@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer)
):
    """
    Cerrar sesión e invalidar de forma inmediata el token JWT en la lista negra (Token Blacklist).
    """
    if credentials and credentials.credentials:
        token = credentials.credentials
        payload = decode_access_token(token)
        exp = payload.get("exp") if payload else None
        token_blacklist.revoke_token(token, exp)
        logger.info(f"LOGOUT: Token revocado para usuario='{current_user.username}'")

    return {
        "status": "success",
        "message": "Sesión cerrada correctamente y token revocado."
    }


@router.get("/user")
def get_user_profile(current_user: User = Depends(get_current_user)):
    """
    Obtener datos del usuario actualmente autenticado.
    """
    return {
        "id": current_user.id,
        "name": current_user.name,
        "username": current_user.username,
        "role": current_user.role,
        "email": current_user.email
    }

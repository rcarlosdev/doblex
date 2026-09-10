from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import verify_password, create_access_token
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse, UserInfo
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Iniciar sesión con username y password, compatible con el frontend de Vue.
    """
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Las credenciales proporcionadas son incorrectas."
        )
    
    token = create_access_token(data={
        "sub": str(user.id),
        "username": user.username,
        "role": user.role
    })

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
def logout(current_user: User = Depends(get_current_user)):
    """
    Cerrar sesión de usuario.
    """
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

import os
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.security_headers import SecurityHeadersMiddleware
from app.db.base import Base
from app.db.session import engine
from app.api.api_router import api_router
# Importar modelos para que Base los conozca
import app.models

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Asegurar directorio de subida de evidencias
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API REST en Python (FastAPI) para el Sistema de Gestión de Obra Civil (SMU) - Doblex S.A.S.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 1. Middleware de Cabeceras de Seguridad HTTP (HSTS, nosniff, frame-options, CSP, etc.)
app.add_middleware(SecurityHeadersMiddleware)

# 2. Configuración de CORS Profesional y Adaptable (Soporta localhost y cualquier dominio Vercel)
cors_origins = settings.cors_origins_list
if "*" in cors_origins:
    allowed_origins = ["*"]
else:
    allowed_origins = [o for o in cors_origins if o != "*"]
    if not allowed_origins:
        allowed_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"^https?:\/\/.*(vercel\.app|localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
    allow_headers=[
        "*",
        "Authorization",
        "X-Authorization",
        "X-Access-Token",
        "X-Token",
        "Content-Type",
        "Accept",
        "X-Requested-With",
        "Origin"
    ],
    expose_headers=["Content-Disposition", "Retry-After", "X-Total-Count"],
    max_age=3600,
)


# Custom Exception Handler para HTTPException (Formato compatible con frontend de Vue)
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "detail": exc.detail
        },
        headers=exc.headers
    )

# Custom Exception Handler para errores de validación 422 de Pydantic
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    # Construir mensaje amigable
    first_error = errors[0] if errors else {}
    field = ".".join(str(loc) for loc in first_error.get("loc", []) if loc != "body")
    msg = first_error.get("msg", "Datos inválidos")
    detail_msg = f"Error en campo '{field}': {msg}" if field else msg

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "message": detail_msg,
            "errors": errors
        }
    )

# Montar directorio estático para evidencias fotográficas
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Incluir rutas API bajo el prefijo /api
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "status": "success",
        "name": settings.PROJECT_NAME,
        "version": "2.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

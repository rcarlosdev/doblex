from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Doblex SMU API"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = "doblex_super_secret_jwt_key_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 horas

    DATABASE_URL: str = "sqlite:///./doblex.db"
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://localhost:8000"
    UPLOAD_DIR: str = "./uploads"

    # Parámetros de seguridad
    SECURITY_RATE_LIMIT_ENABLED: bool = True
    LOGIN_RATE_LIMIT_MAX: int = 5         # Máx 5 intentos
    LOGIN_RATE_LIMIT_WINDOW: int = 60      # por minuto
    API_RATE_LIMIT_MAX: int = 120          # Máx 120 peticiones
    API_RATE_LIMIT_WINDOW: int = 60        # por minuto
    MAX_UPLOAD_SIZE_MB: int = 10           # 10 MB para imágenes
    MAX_EXCEL_UPLOAD_SIZE_MB: int = 15     # 15 MB para planillas

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

settings = Settings()


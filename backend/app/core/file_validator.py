import base64
import re
import uuid
from typing import Tuple, Optional
from fastapi import HTTPException, status
from app.core.config import settings

# Firmas binarias de formatos permitidos
MAGIC_NUMBERS = {
    "jpeg": b"\xFF\xD8\xFF",
    "png": b"\x89PNG\r\n\x1a\n",
    "webp_riff": b"RIFF",
    "webp_tag": b"WEBP",
    "xlsx": b"PK\x03\x04",
    "xls": b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1"
}

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_EXCEL_EXTENSIONS = {".xlsx", ".xls"}

def is_valid_image_bytes(data: bytes) -> Tuple[bool, Optional[str]]:
    """
    Verifica los 'magic bytes' para confirmar que los datos corresponden a una imagen real.
    Retorna (es_valido, extension_sugerida).
    """
    if len(data) < 12:
        return False, None

    if data.startswith(MAGIC_NUMBERS["jpeg"]):
        return True, ".jpg"
    if data.startswith(MAGIC_NUMBERS["png"]):
        return True, ".png"
    if data.startswith(MAGIC_NUMBERS["webp_riff"]) and data[8:12] == MAGIC_NUMBERS["webp_tag"]:
        return True, ".webp"

    return False, None

def is_valid_excel_bytes(data: bytes) -> Tuple[bool, Optional[str]]:
    """
    Verifica que los bytes correspondan a una planilla Excel válida (.xlsx OpenXML o .xls BIFF8).
    """
    if len(data) < 8:
        return False, None

    if data.startswith(MAGIC_NUMBERS["xlsx"]):
        return True, ".xlsx"
    if data.startswith(MAGIC_NUMBERS["xls"]):
        return True, ".xls"

    return False, None

def validate_and_decode_base64_image(image_input: str, max_mb: Optional[int] = None) -> Tuple[bytes, str]:
    """
    Valida y decodifica una imagen en formato base64.
    Previene cargas maliciosas, verifica límite de tamaño y firmas binarias.
    Retorna (bytes_decodificados, extension).
    """
    if not image_input or not isinstance(image_input, str):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La imagen proporcionada no contiene datos válidos."
        )

    max_bytes = (max_mb or settings.MAX_UPLOAD_SIZE_MB) * 1024 * 1024

    # Extraer cabecera Data URL si existe: data:image/jpeg;base64,...
    raw_base64 = image_input
    if "," in image_input and image_input.startswith("data:"):
        header, raw_base64 = image_input.split(",", 1)
        if not re.match(r"^data:image/(jpeg|jpg|png|webp);base64$", header, re.IGNORECASE):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Formato de imagen en cabecera no permitido. Solo se aceptan JPEG, PNG y WebP."
            )

    # Validar tamaño preliminar del string base64 para evitar DoS en decode
    estimated_size = (len(raw_base64) * 3) / 4
    if estimated_size > max_bytes * 1.2:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"La imagen excede el tamaño máximo permitido de {settings.MAX_UPLOAD_SIZE_MB}MB."
        )

    try:
        decoded_bytes = base64.b64decode(raw_base64, validate=True)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La codificación base64 de la imagen es inválida o está corrupta."
        )

    if len(decoded_bytes) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"La imagen excede el límite máximo permitido de {settings.MAX_UPLOAD_SIZE_MB}MB."
        )

    is_valid, ext = is_valid_image_bytes(decoded_bytes)
    if not is_valid or not ext:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El archivo no corresponde a una imagen válida (JPEG, PNG o WebP según su firma binaria)."
        )

    return decoded_bytes, ext

def generate_secure_filename(extension: str) -> str:
    """
    Genera un nombre de archivo único, seguro y previene cualquier intento de Path Traversal.
    """
    clean_ext = extension.lower().strip()
    if not clean_ext.startswith("."):
        clean_ext = f".{clean_ext}"
    return f"{uuid.uuid4().hex}{clean_ext}"

def sanitize_text(text: Optional[str]) -> Optional[str]:
    """
    Sanitiza cadenas de texto libre para neutralizar inyecciones de scripts o HTML malicioso.
    """
    if not text:
        return text

    # Eliminar tags de script completos
    cleaned = re.sub(r"<\s*script[^>]*>.*?<\s*/\s*script\s*>", "", text, flags=re.DOTALL | re.IGNORECASE)
    # Neutralizar pseudo-protocolos javascript:
    cleaned = re.sub(r"javascript\s*:", "", cleaned, flags=re.IGNORECASE)
    # Reemplazar caracteres de etiquetas peligrosas < >
    cleaned = cleaned.replace("<", "&lt;").replace(">", "&gt;")
    return cleaned.strip()

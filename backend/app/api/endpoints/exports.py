from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, joinedload
from app.db.session import get_db
from app.api.deps import get_current_user, require_roles
from app.models.user import User
from app.models.ot import Ot
from app.core.config import settings
from app.core.file_validator import is_valid_excel_bytes
from app.services.excel_service import generate_ots_excel, parse_import_excel
from app.services.word_service import generate_ot_word
from app.services.pdf_service import generate_ot_pdf

router = APIRouter()


@router.get("/ots/export/excel")
def export_ots_to_excel(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Exportar listado de Órdenes de Trabajo en formato Microsoft Excel (.xlsx).
    """
    query = db.query(Ot).options(
        joinedload(Ot.assigned_user),
        joinedload(Ot.cuadrilla)
    ).order_by(Ot.created_at.desc())

    if current_user.role == "administrativo":
        query = query.filter(Ot.created_by == current_user.id)
    elif current_user.role == "operativo":
        query = query.filter(Ot.user_id == current_user.id)

    ots = query.all()
    buffer = generate_ots_excel(ots)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=reporte_ots_doblex.xlsx"}
    )

@router.get("/ots/{ot_id}/export/word")
def export_ot_to_word(
    ot_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Exportar informe técnico individual de una OT en formato Word (.docx).
    """
    ot = db.query(Ot).options(
        joinedload(Ot.assigned_user),
        joinedload(Ot.cuadrilla),
        joinedload(Ot.repuestos)
    ).filter(Ot.id == ot_id).first()

    if not ot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OT no encontrada.")

    buffer = generate_ot_word(ot)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=informe_ot_{ot.codigo}.docx"}
    )

@router.get("/ots/{ot_id}/export/pdf")
def export_ot_to_pdf(
    ot_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Exportar informe técnico individual de una OT en formato PDF (.pdf).
    """
    ot = db.query(Ot).options(
        joinedload(Ot.assigned_user),
        joinedload(Ot.cuadrilla),
        joinedload(Ot.repuestos)
    ).filter(Ot.id == ot_id).first()

    if not ot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OT no encontrada.")

    buffer = generate_ot_pdf(ot)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=informe_ot_{ot.codigo}.pdf"}
    )

@router.post("/ots/import/excel")
async def import_ots_from_excel(
    file: UploadFile = File(...),
    current_user: User = Depends(require_roles(["admin", "administrativo"])),
    db: Session = Depends(get_db)
):
    """
    Procesar e importar Órdenes de Trabajo o insumos masivamente desde un archivo Excel.
    Validado contra cargas maliciosas mediante comprobación de extensión, límite de tamaño y magic bytes.
    """
    clean_filename = (file.filename or "").lower()
    if not clean_filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Formato de archivo no válido. Se requiere un archivo con extensión .xlsx o .xls"
        )

    content = await file.read()

    # Validar tamaño máximo
    max_bytes = settings.MAX_EXCEL_UPLOAD_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"El archivo Excel excede el tamaño máximo permitido de {settings.MAX_EXCEL_UPLOAD_SIZE_MB}MB."
        )

    # Validar firma binaria (magic bytes)
    is_valid, _ = is_valid_excel_bytes(content)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El archivo no corresponde a una planilla Excel válida según su firma binaria."
        )

    try:
        records = parse_import_excel(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error al leer la planilla Excel: {str(e)}"
        )

    return {
        "status": "success",
        "message": f"Se procesaron {len(records)} filas del archivo Excel con éxito.",
        "total_filas": len(records),
        "preview": records[:5]
    }


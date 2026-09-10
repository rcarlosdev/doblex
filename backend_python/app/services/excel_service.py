import io
from typing import List
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from app.models.ot import Ot

def generate_ots_excel(ots: List[Ot]) -> io.BytesIO:
    """
    Genera un archivo Excel profesional con el listado de Órdenes de Trabajo.
    Retorna un buffer en memoria io.BytesIO listo para StreamingResponse.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Órdenes de Trabajo"

    # Estilos
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    thin_border = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )

    headers = [
        "Código", "Descripción", "Sitio / Ubicación", "Prioridad", 
        "Tipo Mantenimiento", "Estado", "Progreso (%)", "Técnico Asignado",
        "Cuadrilla", "Fecha Inicio", "Límite SLA"
    ]

    ws.append(headers)
    for col_num in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = thin_border

    # Filas de datos
    for row_idx, ot in enumerate(ots, start=2):
        assigned_name = ot.assigned_user.name if ot.assigned_user else "No Asignado"
        cuadrilla_name = ot.cuadrilla.nombre if ot.cuadrilla else "N/A"
        f_inicio = ot.fecha_inicio.strftime("%Y-%m-%d %H:%M") if ot.fecha_inicio else ""
        f_sla = ot.fecha_limite_sla.strftime("%Y-%m-%d %H:%M") if ot.fecha_limite_sla else ""

        row_data = [
            ot.codigo,
            ot.descripcion,
            f"{ot.sitio or ''} - {ot.ubicacion}".strip(" -"),
            ot.prioridad,
            ot.tipo_mantenimiento,
            ot.estado.upper(),
            f"{ot.progreso}%",
            assigned_name,
            cuadrilla_name,
            f_inicio,
            f_sla
        ]
        ws.append(row_data)

        for col_num in range(1, len(headers) + 1):
            cell = ws.cell(row=row_idx, column=col_num)
            cell.border = thin_border
            if col_num in [1, 4, 5, 6, 7, 10, 11]:
                cell.alignment = align_center
            else:
                cell.alignment = align_left

    # Autoajuste de columnas
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = col[0].column_letter
        ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output

def parse_import_excel(file_bytes: bytes) -> List[dict]:
    """
    Lee una planilla de Excel y retorna una lista de diccionarios validada con pandas.
    """
    df = pd.read_excel(io.BytesIO(file_bytes))
    df = df.fillna("")
    return df.to_dict(orient="records")

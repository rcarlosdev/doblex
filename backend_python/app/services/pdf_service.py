import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from app.models.ot import Ot

def generate_ot_pdf(ot: Ot) -> io.BytesIO:
    """
    Genera un informe técnico de Orden de Trabajo en formato PDF.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        alignment=1 # Center
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        textColor=colors.HexColor('#64748B'),
        alignment=1
    )
    section_style = ParagraphStyle(
        'DocSection',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=12,
        spaceAfter=6
    )
    normal_style = styles['Normal']

    story = []

    # Encabezado
    story.append(Paragraph(f"INFORME TÉCNICO DE OBRA CIVIL - {ot.codigo}", title_style))
    story.append(Paragraph("DOBLEX S.A.S. - Sistema de Mantenimiento y Obra (SMU)", subtitle_style))
    story.append(Spacer(1, 15))

    # Tabla de datos
    assigned_name = ot.assigned_user.name if ot.assigned_user else "Sin Asignar"
    cuadrilla_name = ot.cuadrilla.nombre if ot.cuadrilla else "N/A"

    data = [
        ["Código:", ot.codigo, "Estado:", ot.estado.upper()],
        ["Descripción:", ot.descripcion, "Progreso:", f"{ot.progreso}%"],
        ["Ubicación:", ot.ubicacion, "Sitio:", ot.sitio or "N/A"],
        ["Prioridad:", ot.prioridad, "Tipo:", ot.tipo_mantenimiento],
        ["Asignado a:", assigned_name, "Cuadrilla:", cuadrilla_name],
        ["Fecha Inicio:", str(ot.fecha_inicio or ""), "Límite SLA:", str(ot.fecha_limite_sla or "N/A")]
    ]

    t = Table(data, colWidths=[80, 180, 80, 180])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1E293B')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    # Cierre técnico si aplica
    if ot.estado in ["solucionada", "finalizada"]:
        story.append(Paragraph("Cierre Técnico y Diagnóstico", section_style))
        story.append(Paragraph(f"<b>Causa Falla:</b> {ot.causa_falla or 'No especificada'}", normal_style))
        if ot.observaciones_cierre:
            story.append(Paragraph(f"<b>Observaciones:</b> {ot.observaciones_cierre}", normal_style))
        story.append(Spacer(1, 10))

    # Insumos y Repuestos si existen
    if ot.repuestos:
        story.append(Paragraph("Insumos y Repuestos Utilizados", section_style))
        rep_data = [["Ítem", "Cantidad", "Unidad"]]
        for r in ot.repuestos:
            rep_data.append([r.nombre_item, str(r.cantidad), r.unidad_medida])
        
        rep_table = Table(rep_data, colWidths=[240, 140, 140])
        rep_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ]))
        story.append(rep_table)

    doc.build(story)
    buffer.seek(0)
    return buffer

import os
import json
from datetime import datetime
from typing import Optional, List, Any, Dict
from dateutil import parser as date_parser
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.ot import Ot
from app.models.actividad_ot import ActividadOt
from app.models.evidencia import EvidenciaFotografica
from app.models.repuesto import RepuestoUtilizado
from app.models.empleado import Empleado
from app.repositories.ot_repository import ot_repository
from app.core.config import settings
from app.core.utils import now_utc
from app.core.file_validator import (
    validate_and_decode_base64_image,
    generate_secure_filename,
    sanitize_text
)
from app.services.sla_service import sla_service
from app.schemas.ot import (
    OtCreate, OtUpdate, OtEstadoUpdate, OtCerrarRequest,
    EvidenciaCreate, RepuestoSyncRequest
)

class OtService:
    @staticmethod
    def parse_datetime(dt_input: Any) -> datetime:
        if isinstance(dt_input, datetime):
            return dt_input
        if isinstance(dt_input, str):
            return date_parser.parse(dt_input)
        return now_utc()

    @staticmethod
    def serialize_ot(ot: Ot) -> dict:
        assigned_user_dict = None
        if ot.assigned_user:
            assigned_user_dict = {
                "id": ot.assigned_user.id,
                "name": ot.assigned_user.name,
                "username": ot.assigned_user.username,
                "role": ot.assigned_user.role,
                "email": ot.assigned_user.email
            }
        
        creator_dict = None
        if ot.creator:
            creator_dict = {
                "id": ot.creator.id,
                "name": ot.creator.name,
                "username": ot.creator.username,
                "role": ot.creator.role
            }

        cuadrilla_dict = None
        if ot.cuadrilla:
            cuadrilla_dict = {
                "id": ot.cuadrilla.id,
                "nombre": ot.cuadrilla.nombre,
                "especialidad": ot.cuadrilla.especialidad,
                "lider_id": ot.cuadrilla.lider_id
            }

        actividades_list = [
            {
                "id": act.id,
                "ot_id": act.ot_id,
                "nombre": act.nombre,
                "peso_porcentaje": act.peso_porcentaje,
                "progreso": act.progreso,
                "estado": act.estado
            }
            for act in (ot.actividades or [])
        ]

        evidencias_list = [
            {
                "id": ev.id,
                "ot_id": ev.ot_id,
                "tipo": ev.tipo,
                "url_imagen": ev.url_imagen,
                "latitud": ev.latitud,
                "longitud": ev.longitud,
                "fecha_hora_captura": ev.fecha_hora_captura.isoformat() if ev.fecha_hora_captura else None
            }
            for ev in (ot.evidencias or [])
        ]

        repuestos_list = [
            {
                "id": rep.id,
                "ot_id": rep.ot_id,
                "nombre_item": rep.nombre_item,
                "cantidad": rep.cantidad,
                "unidad_medida": rep.unidad_medida,
                "created_at": rep.created_at.isoformat() if rep.created_at else None
            }
            for rep in (ot.repuestos or [])
        ]

        avances_list = [
            {
                "id": av.id,
                "ot_id": av.ot_id,
                "user_id": av.user_id,
                "descripcion": av.descripcion,
                "porcentaje": av.porcentaje,
                "fecha_reporte": av.fecha_reporte.isoformat() if av.fecha_reporte else None,
                "created_at": av.created_at.isoformat() if av.created_at else None,
                "user": {
                    "id": av.user.id,
                    "name": av.user.name,
                    "username": av.user.username
                } if av.user else None
            }
            for av in (ot.avances or [])
        ]

        # Manejo de datos_formulario
        datos_formulario_parsed = None
        if ot.datos_formulario:
            try:
                datos_formulario_parsed = json.loads(ot.datos_formulario)
            except Exception:
                datos_formulario_parsed = ot.datos_formulario

        return {
            "id": ot.id,
            "codigo": ot.codigo,
            "id_actividad": ot.id_actividad,
            "descripcion": ot.descripcion,
            "sitio": ot.sitio,
            "sitio_id": ot.sitio_id,
            "ubicacion": ot.ubicacion,
            "created_by": ot.created_by,
            "user_id": ot.user_id,
            "cuadrilla_id": ot.cuadrilla_id,
            "coordinador": ot.coordinador,
            "progreso": ot.progreso,
            "estado": ot.estado,
            "prioridad": ot.prioridad,
            "tipo_ubicacion": ot.tipo_ubicacion,
            "categoria": ot.categoria or ("rural" if ot.tipo_ubicacion == "rural" else "normal"),
            "regional": ot.regional or "R1",
            "departamento": ot.departamento,
            "tipo_estacion": ot.tipo_estacion or "MOVIL",
            "site_owner": ot.site_owner,
            "tipo_mantenimiento": ot.tipo_mantenimiento,
            "tipo_actividad": ot.tipo_actividad or ot.tipo_mantenimiento,
            "subsistema": ot.subsistema,
            "tipo_gasto": ot.tipo_gasto,
            "datos_formulario": datos_formulario_parsed,
            "operadores_asignados": datos_formulario_parsed.get("operadores_asignados", []) if isinstance(datos_formulario_parsed, dict) else [],
            "fecha_inicio": ot.fecha_inicio.isoformat() if ot.fecha_inicio else None,
            "fecha_limite_sla": ot.fecha_limite_sla.isoformat() if ot.fecha_limite_sla else None,
            "fecha_llegada_sitio": ot.fecha_llegada_sitio.isoformat() if ot.fecha_llegada_sitio else None,
            "fecha_solucion": ot.fecha_solucion.isoformat() if ot.fecha_solucion else None,
            "causa_falla": ot.causa_falla,
            "observaciones_cierre": ot.observaciones_cierre,
            "created_at": ot.created_at.isoformat() if ot.created_at else None,
            "updated_at": ot.updated_at.isoformat() if ot.updated_at else None,
            # Relaciones
            "assigned_user": assigned_user_dict,
            "assignedUser": assigned_user_dict,
            "creator": creator_dict,
            "cuadrilla": cuadrilla_dict,
            "actividades": actividades_list,
            "evidencias": evidencias_list,
            "repuestos": repuestos_list,
            "avances": avances_list
        }

    def list_ots(self, db: Session, current_user: User) -> List[dict]:
        if current_user.role not in ["admin", "administrativo", "operativo"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Rol de usuario no autorizado."
            )

        ots = ot_repository.list_by_role(db, current_user)
        return [self.serialize_ot(ot) for ot in ots]

    def get_ot(self, db: Session, ot_id: int, current_user: User) -> dict:
        ot = ot_repository.get_with_relations(db, ot_id)
        if not ot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Orden de Trabajo no encontrada."
            )

        if current_user.role == "operativo":
            user_cuadrilla_id = current_user.empleado.cuadrilla_id if current_user.empleado else None
            if ot.user_id != current_user.id and ot.cuadrilla_id != user_cuadrilla_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene autorización para visualizar esta Orden de Trabajo."
                )

        return self.serialize_ot(ot)

    def create_ot(self, db: Session, payload: OtCreate, current_user: User) -> dict:
        existing = ot_repository.get_by_codigo(db, payload.codigo)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"El código de OT '{payload.codigo}' ya se encuentra registrado."
            )

        fecha_inicio = self.parse_datetime(payload.fecha_inicio)
        fecha_limite_sla = payload.fecha_limite_sla
        if not fecha_limite_sla:
            fecha_limite_sla = sla_service.calcular_fecha_limite(
                payload.prioridad,
                payload.tipo_ubicacion,
                fecha_inicio
            )
        else:
            fecha_limite_sla = self.parse_datetime(fecha_limite_sla)

        id_actividad = payload.id_actividad
        if not id_actividad or not id_actividad.strip():
            clean_code = payload.codigo.replace("OT-", "").replace("WO", "").strip()
            id_actividad = f"ACT-{now_utc().strftime('%Y%m%d')}-{clean_code}"

        # Manejo de datos_formulario y asignación múltiple de operadores
        datos_form_dict: dict = {}
        if payload.datos_formulario:
            if isinstance(payload.datos_formulario, dict):
                datos_form_dict = dict(payload.datos_formulario)
            elif isinstance(payload.datos_formulario, str):
                try:
                    datos_form_dict = json.loads(payload.datos_formulario)
                except Exception:
                    datos_form_dict = {}

        if payload.operadores_asignados:
            datos_form_dict["operadores_asignados"] = payload.operadores_asignados

        datos_form_str = json.dumps(datos_form_dict) if datos_form_dict else None

        categoria = payload.categoria or ("rural" if payload.tipo_ubicacion == "rural" else "normal")

        new_ot = Ot(
            codigo=payload.codigo.strip(),
            id_actividad=id_actividad.strip(),
            descripcion=payload.descripcion.strip(),
            sitio=payload.sitio.strip() if payload.sitio else None,
            sitio_id=payload.sitio_id,
            ubicacion=payload.ubicacion.strip(),
            created_by=current_user.id,
            user_id=payload.user_id,
            cuadrilla_id=payload.cuadrilla_id,
            coordinador=payload.coordinador.strip() if payload.coordinador else None,
            prioridad=payload.prioridad,
            tipo_ubicacion=payload.tipo_ubicacion,
            categoria=categoria,
            regional=payload.regional or "R1",
            departamento=payload.departamento.strip() if payload.departamento else None,
            tipo_estacion=payload.tipo_estacion or "MOVIL",
            site_owner=payload.site_owner.strip() if payload.site_owner else None,
            tipo_mantenimiento=payload.tipo_mantenimiento,
            tipo_actividad=payload.tipo_actividad or payload.tipo_mantenimiento,
            subsistema=payload.subsistema or "sistema_electrico",
            tipo_gasto=payload.tipo_gasto,
            datos_formulario=datos_form_str,
            fecha_inicio=fecha_inicio,
            fecha_limite_sla=fecha_limite_sla,
            progreso=0,
            estado="asignada"
        )
        db.add(new_ot)
        db.commit()
        db.refresh(new_ot)

        return self.serialize_ot(new_ot)

    def update_ot(self, db: Session, ot_id: int, payload: OtUpdate, current_user: User) -> dict:
        ot = db.query(Ot).filter(Ot.id == ot_id).first()
        if not ot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Orden de Trabajo no encontrada."
            )

        existing = db.query(Ot).filter(Ot.codigo == payload.codigo, Ot.id != ot_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"El código '{payload.codigo}' ya está asignado a otra OT."
            )

        fecha_inicio = self.parse_datetime(payload.fecha_inicio)
        fecha_limite_sla = payload.fecha_limite_sla
        if not fecha_limite_sla:
            fecha_limite_sla = sla_service.calcular_fecha_limite(
                payload.prioridad,
                payload.tipo_ubicacion,
                fecha_inicio
            )
        else:
            fecha_limite_sla = self.parse_datetime(fecha_limite_sla)

        ot.codigo = payload.codigo
        if payload.id_actividad:
            ot.id_actividad = payload.id_actividad
        ot.descripcion = payload.descripcion
        ot.sitio = payload.sitio
        ot.sitio_id = payload.sitio_id
        ot.ubicacion = payload.ubicacion
        ot.user_id = payload.user_id
        ot.cuadrilla_id = payload.cuadrilla_id
        if payload.coordinador is not None:
            ot.coordinador = payload.coordinador
        ot.prioridad = payload.prioridad
        ot.tipo_ubicacion = payload.tipo_ubicacion
        if payload.categoria:
            ot.categoria = payload.categoria
        if payload.regional:
            ot.regional = payload.regional
        if payload.departamento is not None:
            ot.departamento = payload.departamento
        if payload.tipo_estacion:
            ot.tipo_estacion = payload.tipo_estacion
        if payload.site_owner is not None:
            ot.site_owner = payload.site_owner
        ot.tipo_mantenimiento = payload.tipo_mantenimiento
        if payload.tipo_actividad:
            ot.tipo_actividad = payload.tipo_actividad
        ot.subsistema = payload.subsistema
        if payload.tipo_gasto is not None:
            ot.tipo_gasto = payload.tipo_gasto
        if payload.datos_formulario is not None or payload.operadores_asignados is not None:
            curr_form: dict = {}
            if ot.datos_formulario:
                try:
                    curr_form = json.loads(ot.datos_formulario)
                except Exception:
                    curr_form = {}
            if payload.datos_formulario is not None:
                if isinstance(payload.datos_formulario, dict):
                    curr_form.update(payload.datos_formulario)
                elif isinstance(payload.datos_formulario, str):
                    try:
                        curr_form.update(json.loads(payload.datos_formulario))
                    except Exception:
                        pass
            if payload.operadores_asignados is not None:
                curr_form["operadores_asignados"] = payload.operadores_asignados
            ot.datos_formulario = json.dumps(curr_form) if curr_form else None
        ot.estado = payload.estado
        ot.fecha_inicio = fecha_inicio
        ot.fecha_limite_sla = fecha_limite_sla

        db.commit()
        db.refresh(ot)
        return self.serialize_ot(ot)

    def update_estado(self, db: Session, ot_id: int, payload: OtEstadoUpdate, current_user: User) -> dict:
        ot = db.query(Ot).filter(Ot.id == ot_id).first()
        if not ot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="OT no encontrada."
            )

        ot.estado = payload.estado
        if payload.progreso is not None:
            ot.progreso = payload.progreso

        now = now_utc()
        if payload.estado == "en_sitio" and not ot.fecha_llegada_sitio:
            ot.fecha_llegada_sitio = now

        if payload.estado == "solucionada":
            ot.fecha_solucion = now
            ot.progreso = 100

        db.commit()
        db.refresh(ot)
        return self.serialize_ot(ot)

    def update_formulario(self, db: Session, ot_id: int, payload: dict, current_user: User) -> dict:
        ot = db.query(Ot).filter(Ot.id == ot_id).first()
        if not ot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Orden de Trabajo no encontrada."
            )

        if current_user.role == "operativo":
            user_cuadrilla_id = current_user.empleado.cuadrilla_id if current_user.empleado else None
            if ot.user_id != current_user.id and ot.cuadrilla_id != user_cuadrilla_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene autorización para modificar esta Orden de Trabajo."
                )

        form_data = payload.get("datos_formulario", payload)
        if isinstance(form_data, dict):
            curr_form = {}
            if ot.datos_formulario:
                try:
                    curr_form = json.loads(ot.datos_formulario)
                except Exception:
                    curr_form = {}
            curr_form.update(form_data)
            ot.datos_formulario = json.dumps(curr_form, ensure_ascii=False)
        elif isinstance(form_data, str):
            ot.datos_formulario = form_data

        db.commit()
        db.refresh(ot)
        return self.serialize_ot(ot)

    def upload_evidencia(self, db: Session, ot_id: int, payload: EvidenciaCreate, current_user: User) -> dict:
        ot = db.query(Ot).filter(Ot.id == ot_id).first()
        if not ot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="OT no encontrada."
            )

        url_final = None
        if payload.imagen_base64:
            decoded_bytes, ext = validate_and_decode_base64_image(payload.imagen_base64)
            filename = generate_secure_filename(ext)
            filepath = os.path.join(settings.UPLOAD_DIR, filename)
            try:
                with open(filepath, "wb") as f:
                    f.write(decoded_bytes)
                url_final = f"/uploads/{filename}"
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error al almacenar evidencia en disco: {str(e)}"
                )
        elif payload.imagen_url:
            clean_url = payload.imagen_url.strip()
            if not (clean_url.startswith("http://") or clean_url.startswith("https://") or clean_url.startswith("/uploads/")):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="La URL de imagen no es válida. Debe iniciar con http://, https:// o /uploads/"
                )
            url_final = clean_url
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Se requiere imagen_base64 o imagen_url."
            )

        evidencia = EvidenciaFotografica(
            ot_id=ot.id,
            tipo=payload.tipo,
            url_imagen=url_final,
            latitud=payload.latitud,
            longitud=payload.longitud,
            fecha_hora_captura=now_utc()
        )
        db.add(evidencia)
        db.commit()
        db.refresh(evidencia)

        return {
            "id": evidencia.id,
            "ot_id": evidencia.ot_id,
            "tipo": evidencia.tipo,
            "url_imagen": evidencia.url_imagen,
            "latitud": evidencia.latitud,
            "longitud": evidencia.longitud,
            "fecha_hora_captura": evidencia.fecha_hora_captura.isoformat() if evidencia.fecha_hora_captura else None
        }

    def delete_evidencia(self, db: Session, evidencia_id: int, current_user: User) -> dict:
        evidencia = db.query(EvidenciaFotografica).filter(EvidenciaFotografica.id == evidencia_id).first()
        if not evidencia:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evidencia fotográfica no encontrada.")

        if evidencia.ot and evidencia.ot.estado in ["solucionada", "finalizada"]:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No se pueden eliminar evidencias de una Orden de Trabajo solucionada o finalizada."
            )

        db.delete(evidencia)
        db.commit()
        return {"status": "success", "message": "Evidencia fotográfica eliminada con éxito."}

    def sync_repuestos(self, db: Session, ot_id: int, payload: RepuestoSyncRequest, current_user: User) -> dict:
        ot = db.query(Ot).filter(Ot.id == ot_id).first()
        if not ot:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OT no encontrada.")

        if ot.estado in ["solucionada", "finalizada"]:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No se pueden modificar insumos de una Orden de Trabajo solucionada o finalizada."
            )

        db.query(RepuestoUtilizado).filter(RepuestoUtilizado.ot_id == ot.id).delete()

        for item in payload.repuestos:
            repuesto = RepuestoUtilizado(
                ot_id=ot.id,
                nombre_item=item.nombre_item,
                cantidad=item.cantidad,
                unidad_medida=item.unidad_medida or "unidad"
            )
            db.add(repuesto)

        db.commit()
        db.refresh(ot)
        return self.serialize_ot(ot)

    def cerrar_ot(self, db: Session, ot_id: int, payload: OtCerrarRequest, current_user: User) -> dict:
        ot = db.query(Ot).filter(Ot.id == ot_id).first()
        if not ot:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OT no encontrada.")

        tipos_existentes = [ev.tipo for ev in ot.evidencias]
        faltantes = []
        is_preventivo = (
            ot.tipo_mantenimiento == "preventivo" or 
            (ot.tipo_actividad and "preventivo" in ot.tipo_actividad.lower())
        )

        if is_preventivo:
            # Requisitos oficiales para formatos MP (Preventivo Planta / Aire)
            tiene_placas = any(t in tipos_existentes for t in ["placas", "antes", "inicial"])
            tiene_mantenimiento = any(t in tipos_existentes for t in ["mantenimiento", "filtracion", "durante"])
            tiene_pruebas = any(t in tipos_existentes for t in ["pruebas", "despues", "final"])

            if not tiene_placas:
                faltantes.append("Placas Técnicas / Estado Inicial")
            if not tiene_mantenimiento:
                faltantes.append("Servicio de Filtración / Mantenimiento")
            if not tiene_pruebas:
                faltantes.append("Pruebas Operativas / Mediciones Finales")
        else:
            # Requisitos oficiales para formatos WO (Correctivos y Emergencias)
            if "antes" not in tipos_existentes:
                faltantes.append("Evidencia de ANTES (Falla inicial)")
            if "durante" not in tipos_existentes:
                faltantes.append("Evidencia de DURANTE (Intervención técnica)")
            if "despues" not in tipos_existentes:
                faltantes.append("Evidencia de DESPUÉS (Equipo operativo)")

        if faltantes:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No se puede cerrar la OT sin diligenciar totalmente las evidencias obligatorias requeridas para este tipo de trabajo: " + ", ".join(faltantes)
            )

        now = now_utc()
        ot.estado = "solucionada"
        ot.progreso = 100
        ot.fecha_solucion = now
        ot.causa_falla = payload.causa_falla
        ot.observaciones_cierre = payload.observaciones_cierre

        if payload.datos_formulario is not None:
            ot.datos_formulario = json.dumps(payload.datos_formulario) if isinstance(payload.datos_formulario, (dict, list)) else str(payload.datos_formulario)

        if payload.repuestos:
            for item in payload.repuestos:
                rep = RepuestoUtilizado(
                    ot_id=ot.id,
                    nombre_item=item.nombre_item,
                    cantidad=item.cantidad,
                    unidad_medida=item.unidad_medida or "unidad"
                )
                db.add(rep)

        db.commit()
        db.refresh(ot)
        return self.serialize_ot(ot)

    def get_operadores(self, db: Session) -> List[dict]:
        operativos = db.query(User).filter(User.role == "operativo").order_by(User.name.asc()).all()
        return [
            {
                "id": op.id,
                "user_id": op.id,
                "name": op.name,
                "username": op.username,
                "documento": op.empleado.documento if op.empleado else "Sin documento",
                "cargo": op.empleado.cargo if op.empleado else "Técnico de Campo",
                "telefono": op.empleado.telefono if op.empleado else "",
                "cuadrilla_id": op.empleado.cuadrilla_id if op.empleado else None
            }
            for op in operativos
        ]

ot_service = OtService()

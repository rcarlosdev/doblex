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
from app.core.utils import now_utc, to_colombia_datetime
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
            return to_colombia_datetime(dt_input) or now_utc()
        if isinstance(dt_input, str):
            try:
                parsed = date_parser.parse(dt_input)
                return to_colombia_datetime(parsed) or now_utc()
            except Exception:
                return now_utc()
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
            if isinstance(ot.datos_formulario, dict):
                datos_formulario_parsed = ot.datos_formulario
            else:
                try:
                    datos_formulario_parsed = json.loads(str(ot.datos_formulario))
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
                    curr_form = json.loads(str(ot.datos_formulario))
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

    @staticmethod
    def _save_base64_to_disk(
        db: Session, 
        ot_id: int, 
        tipo: str, 
        base64_str: str,
        latitud: Optional[float] = None,
        longitud: Optional[float] = None
    ) -> Optional[str]:
        if not base64_str or not isinstance(base64_str, str):
            return None
        if base64_str.startswith("/uploads/") or base64_str.startswith("http://") or base64_str.startswith("https://"):
            return base64_str
        if "base64," in base64_str or len(base64_str) > 100:
            try:
                decoded_bytes, ext = validate_and_decode_base64_image(base64_str)
                filename = generate_secure_filename(ext)
                filepath = os.path.join(settings.UPLOAD_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(decoded_bytes)
                url_final = f"/uploads/{filename}"

                # Registrar evidencia en la base de datos si no existe con esa URL
                existente = db.query(EvidenciaFotografica).filter(
                    EvidenciaFotografica.ot_id == ot_id,
                    EvidenciaFotografica.url_imagen == url_final
                ).first()
                if not existente:
                    ev = EvidenciaFotografica(
                        ot_id=ot_id,
                        tipo=tipo,
                        url_imagen=url_final,
                        latitud=latitud,
                        longitud=longitud,
                        fecha_hora_captura=now_utc()
                    )
                    db.add(ev)
                return url_final
            except Exception as e:
                print(f"[WARN] No se pudo guardar imagen base64 de {tipo}: {e}")
                return base64_str
        return base64_str

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
                    curr_form = json.loads(str(ot.datos_formulario))
                except Exception:
                    curr_form = {}
            curr_form.update(form_data)

            # 1. Guardar a disco y registrar evidencia para llegada a sitio
            llegada_lat = curr_form.get("llegada_lat")
            llegada_lng = curr_form.get("llegada_lng")
            if curr_form.get("llegada_foto"):
                saved_url = self._save_base64_to_disk(
                    db, ot.id, "llegada_sitio", curr_form["llegada_foto"],
                    latitud=llegada_lat, longitud=llegada_lng
                )
                curr_form["llegada_foto"] = saved_url
                curr_form["llegada_sitio"] = saved_url
                curr_form["llegada_carnet"] = saved_url
                curr_form["llegada_estacion"] = saved_url
            elif curr_form.get("llegada_sitio"):
                saved_url = self._save_base64_to_disk(
                    db, ot.id, "llegada_sitio", curr_form["llegada_sitio"],
                    latitud=llegada_lat, longitud=llegada_lng
                )
                curr_form["llegada_sitio"] = saved_url
                curr_form["llegada_foto"] = saved_url

            # 2. Guardar fotos de transportes especiales a disco
            if isinstance(curr_form.get("transportes_especiales"), list):
                for t in curr_form["transportes_especiales"]:
                    if isinstance(t, dict) and t.get("foto"):
                        t["foto"] = self._save_base64_to_disk(db, ot.id, "transporte", t["foto"])

            # 3. Guardar fotos de repuestos cambiados a disco
            if isinstance(curr_form.get("repuestos_cambios"), list):
                for r in curr_form["repuestos_cambios"]:
                    if isinstance(r, dict):
                        if r.get("foto_retirado"):
                            r["foto_retirado"] = self._save_base64_to_disk(db, ot.id, "repuesto_retirado", r["foto_retirado"])
                        if r.get("foto_instalado"):
                            r["foto_instalado"] = self._save_base64_to_disk(db, ot.id, "repuesto_instalado", r["foto_instalado"])

            # 4. Guardar fotos de insumos menores (antes y después) a disco
            if isinstance(curr_form.get("insumos_menores"), list):
                for ins in curr_form["insumos_menores"]:
                    if isinstance(ins, dict):
                        if ins.get("foto_antes"):
                            ins["foto_antes"] = self._save_base64_to_disk(db, ot.id, "insumo_antes", ins["foto_antes"])
                        if ins.get("foto_despues"):
                            ins["foto_despues"] = self._save_base64_to_disk(db, ot.id, "insumo_despues", ins["foto_despues"])

            # 5. Guardar fotos de novedades y hallazgos a disco
            if isinstance(curr_form.get("hallazgos"), list):
                for h in curr_form["hallazgos"]:
                    if isinstance(h, dict) and h.get("foto"):
                        h["foto"] = self._save_base64_to_disk(db, ot.id, "hallazgo", h["foto"])

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
            (ot.tipo_actividad and any(k in ot.tipo_actividad.lower() for k in ["preventivo", "rutina", "7x24"]))
        )

        # Parsear datos_formulario
        form_data = payload.datos_formulario if payload.datos_formulario is not None else ot.datos_formulario
        if isinstance(form_data, str):
            try:
                form_data = json.loads(form_data)
            except Exception:
                form_data = {}
        elif not isinstance(form_data, dict):
            form_data = {}

        # -------------------------------------------------------------
        # REGLAS TRANSVERSALES OBLIGATORIAS (PARA TODOS LOS TIPOS DE TRABAJO)
        # -------------------------------------------------------------
        # 1. Foto cuando se llega a sitio (Una sola foto del técnico con el carnet y el sitio atrás, con localización y fecha)
        tiene_llegada_unica = bool(
            form_data.get("llegada_foto") or 
            form_data.get("llegada_sitio") or 
            form_data.get("llegada_tecnico_sitio") or 
            form_data.get("llegada_carnet_sitio")
        ) or any(t in tipos_existentes for t in ["llegada_sitio", "llegada_tecnico_sitio", "llegada_carnet_sitio", "llegada"])

        tiene_llegada_legada = (
            bool(form_data.get("llegada_carnet")) or "llegada_carnet" in tipos_existentes or "carnet" in tipos_existentes
        ) and (
            bool(form_data.get("llegada_estacion")) or "llegada_estacion" in tipos_existentes or "estacion" in tipos_existentes
        )

        if not (tiene_llegada_unica or tiene_llegada_legada):
            faltantes.append("Foto de llegada a sitio (Técnico con carnet y estación al fondo)")

        # 2. Registro de Transporte Especial (LPU) - OBLIGATORIO con soporte fotográfico
        transportes = form_data.get("transportes_especiales", [])
        tiene_transporte = (
            (isinstance(transportes, list) and len(transportes) > 0 and any(t.get("foto") for t in transportes if isinstance(t, dict))) or
            "transporte" in tipos_existentes
        )
        if not tiene_transporte:
            faltantes.append("Registro de Transporte Especial (LPU) con foto soporte obligatoria")

        # 3. Repuestos retirados e instalados (si se reportan cambios, verificar foto)
        repuestos_cambios = form_data.get("repuestos_cambios", [])
        if isinstance(repuestos_cambios, list) and repuestos_cambios:
            for idx, r in enumerate(repuestos_cambios, 1):
                if isinstance(r, dict) and (r.get("item_retirado") or r.get("item_instalado")):
                    if not r.get("foto_retirado") or not r.get("foto_instalado"):
                        faltantes.append(f"Fotos de repuesto retirado e instalado en ítem #{idx}")
                        break

        # 4. Materiales e insumos menores (si se reportan, foto antes y después)
        insumos_menores = form_data.get("insumos_menores", [])
        if isinstance(insumos_menores, list) and insumos_menores:
            for idx, ins in enumerate(insumos_menores, 1):
                if isinstance(ins, dict) and ins.get("nombre_item"):
                    if not ins.get("foto_antes") or not ins.get("foto_despues"):
                        faltantes.append(f"Foto antes y después de insumo menor en ítem #{idx}")
                        break

        # 5. Novedades y hallazgos en estación (si se reportan, foto obligatoria)
        hallazgos = form_data.get("hallazgos", [])
        if isinstance(hallazgos, list) and hallazgos:
            for idx, h in enumerate(hallazgos, 1):
                if isinstance(h, dict) and (h.get("descripcion") or h.get("sistema")):
                    if not h.get("foto"):
                        faltantes.append(f"Foto soporte para hallazgo #{idx}")
                        break

        # -------------------------------------------------------------
        # REQUISITOS ESPECÍFICOS SEGÚN TIPO DE TRABAJO
        # -------------------------------------------------------------
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

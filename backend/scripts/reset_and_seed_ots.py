import os
import sys
import json
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.core.config import settings
from app.core.utils import now_utc
from app.models.user import User
from app.models.cuadrilla import Cuadrilla
from app.models.empleado import Empleado
from app.models.sitio import Sitio
from app.models.ot import Ot
from app.models.actividad_ot import ActividadOt
from app.models.evidencia import EvidenciaFotografica
from app.models.repuesto import RepuestoUtilizado
from app.models.avance import Avance
from app.services.sla_service import sla_service

def format_empleado_operador(emp: Empleado):
    if not emp:
        return None
    return {
        "id": emp.id,
        "user_id": emp.user_id,
        "nombre": emp.nombre,
        "name": emp.nombre,
        "cargo": emp.cargo,
        "documento": emp.documento,
        "telefono": emp.telefono,
        "rol": emp.rol
    }

def seed_ots_for_session(db, db_name="SQLite"):
    print(f"\n[{db_name}] 1. Limpiando tablas de Órdenes de Trabajo y datos dependientes...")
    
    # 1. Eliminar datos existentes de OTs y sus tablas hijas en orden estricto de integridad referencial
    deleted_evidencias = db.query(EvidenciaFotografica).delete()
    deleted_repuestos = db.query(RepuestoUtilizado).delete()
    deleted_avances = db.query(Avance).delete()
    deleted_actividades = db.query(ActividadOt).delete()
    deleted_ots = db.query(Ot).delete()
    db.commit()
    
    print(f"[{db_name}] Tablas operativas limpiadas: {deleted_ots} OTs, {deleted_actividades} subactividades, {deleted_avances} avances PDT, {deleted_evidencias} evidencias, {deleted_repuestos} repuestos.")
    print(f"[{db_name}] Catálogos base preservados intactos: {db.query(User).count()} usuarios, {db.query(Cuadrilla).count()} cuadrillas, {db.query(Empleado).count()} empleados, {db.query(Sitio).count()} sitios.")

    # 2. Obtener usuarios y empleados para coordinaciones y multi-técnico
    admin = db.query(User).filter(User.username == "admin.doblex").first()
    adminis = db.query(User).filter(User.username == "adminis.doblex").first() or admin
    carlos = db.query(User).filter(User.username == "carlos.doblex").first() or admin
    luis = db.query(User).filter(User.username == "luis.doblex").first() or carlos
    jasmin = db.query(User).filter(User.username == "jasmin.doblex").first() or carlos
    eliseo = db.query(User).filter(User.username == "eliseo.doblex").first() or carlos

    # Directorio de Empleados
    emp_admin = db.query(Empleado).filter(Empleado.user_id == admin.id).first() if admin else None
    emp_adminis = db.query(Empleado).filter(Empleado.user_id == adminis.id).first() if adminis else None
    emp_carlos = db.query(Empleado).filter(Empleado.user_id == carlos.id).first() if carlos else None
    emp_luis = db.query(Empleado).filter(Empleado.user_id == luis.id).first() if luis else None
    emp_jasmin = db.query(Empleado).filter(Empleado.user_id == jasmin.id).first() if jasmin else None
    emp_eliseo = db.query(Empleado).filter(Empleado.user_id == eliseo.id).first() if eliseo else None
    
    emp_julian = db.query(Empleado).filter(Empleado.nombre.ilike("%Julián%Rivillas%")).first()
    emp_manuel = db.query(Empleado).filter(Empleado.nombre.ilike("%Manuel%Tapias%")).first()
    emp_lozano = db.query(Empleado).filter(Empleado.nombre.ilike("%Carlos%Lozano%")).first()
    emp_ancizar = db.query(Empleado).filter(Empleado.nombre.ilike("%Ancízar%Pérez%")).first()
    emp_ramon = db.query(Empleado).filter(Empleado.nombre.ilike("%Ramón%Yepes%")).first()

    # Cuadrillas
    cuadrilla_ant = db.query(Cuadrilla).filter(Cuadrilla.nombre.ilike("%Antioquia%")).first()
    cuadrilla_cho = db.query(Cuadrilla).filter(Cuadrilla.nombre.ilike("%Chocó%")).first() or cuadrilla_ant
    cuadrilla_cor = db.query(Cuadrilla).filter(Cuadrilla.nombre.ilike("%Córdoba%")).first() or cuadrilla_ant
    cuadrilla_atl = db.query(Cuadrilla).filter(Cuadrilla.nombre.ilike("%Atlántico%")).first() or cuadrilla_ant

    # 3. Buscar Sitios Reales en la base de datos de 1,821 estaciones
    sitio_ant = db.query(Sitio).filter(Sitio.nombre == "ANT.APARTADO").first() or db.query(Sitio).filter(Sitio.nombre.ilike("%APARTADO%")).first()
    sitio_cho = db.query(Sitio).filter(Sitio.nombre == "CHO.CANTON DE SAN PABLO").first() or db.query(Sitio).filter(Sitio.nombre.ilike("%CANTON%")).first()
    sitio_mon = db.query(Sitio).filter(Sitio.nombre == "MON.MONTERIA").first() or db.query(Sitio).filter(Sitio.nombre.ilike("%MONTERIA%")).first()
    sitio_bahia = db.query(Sitio).filter(Sitio.nombre.ilike("%BAHIA SOLANO%")).first() or sitio_cho
    sitio_titi = db.query(Sitio).filter(Sitio.nombre.ilike("%TITIRIBI%")).first() or sitio_ant
    sitio_pizarro = db.query(Sitio).filter(Sitio.nombre.ilike("%PIZARRO%")).first() or sitio_cho
    sitio_turbo = db.query(Sitio).filter(Sitio.nombre == "ANT.TURBO").first() or db.query(Sitio).filter(Sitio.nombre.ilike("%TURBO%")).first() or sitio_ant
    sitio_zungo = db.query(Sitio).filter(Sitio.nombre == "ANT.ZUNGO-2").first() or db.query(Sitio).filter(Sitio.nombre.ilike("%ZUNGO%")).first() or sitio_ant

    print(f"[{db_name}] 2. Sembrando exactamente 1 ejemplo oficial y completo para CADA TIPO DE TRABAJO (8 tipos)...")

    # =========================================================================
    # OT 1: Correctivo (WO) - Exacto a 'WO0000005558781 MC MON.CENTRO.xlsx'
    # =========================================================================
    ops_ot1 = [format_empleado_operador(emp_carlos), format_empleado_operador(emp_julian)]
    ops_ot1 = [op for op in ops_ot1 if op]
    ot1_so = (sitio_ant.supervisor_operativo or "CLEYVER ESPITIA") if sitio_ant else "CLEYVER ESPITIA"
    ot1_form = {
        "no_inc": "SMU008212",
        "tipo_actividad_label": "MANTENIMIENTO CORRECTIVO",
        "tipo_sitio": "Urbano",
        "subsistema": "PE - GRUPO ELECTROGENO",
        "presenta_afectacion": "No",
        "tipo_equipo_falla": "Planta eléctrica",
        "marca_equipo": "Selmec",
        "modelo_equipo": "Selmec 40SC",
        "reparacion": True,
        "reinstalacion": False,
        "cambio_equipo": False,
        "descripcion_falla": "Falla en sistema de enfriamiento del grupo electrógeno con fuga de refrigerante por bomba de agua y alarma de alta temperatura en tablero.",
        "descripcion_solucion": "Se realiza instalación de bomba de agua y se suministran 2 galones de refrigerante. Se realizan pruebas al grupo electrógeno en automático y con carga, el cual realiza el ciclo normalmente. Pruebas avaladas con SO Claro.",
        "repuesto_retirado": {
            "descripcion": "Bomba de agua Selmec 40SC averiada con sello desgastado",
            "marca": "Selmec / Perkins",
            "modelo": "40SC-WP",
            "serial": "SN-PUMP-40SC-092"
        },
        "repuesto_instalado": {
            "descripcion": "Bomba de agua original nueva con empaque perimetral",
            "marca": "Selmec / Perkins",
            "modelo": "40SC-WP-NEW",
            "serial": "SN-PUMP-40SC-991"
        },
        "repuestos_cambios": [
            {
                "item_retirado": "Bomba de agua Selmec 40SC (Sello desgastado)",
                "serial_retirado": "SN-PUMP-40SC-092",
                "item_instalado": "Bomba de agua original nueva Selmec Perkins",
                "serial_instalado": "SN-PUMP-40SC-991",
                "cantidad": 1,
                "motivo": "Fuga severa en sello mecánico y alarma de sobrecalentamiento",
                "foto_retirado": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800",
                "foto_instalado": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800"
            }
        ],
        "materiales": [
            {"codigo_sap": "5003210", "nombre_item": "Refrigerante Anticongelante 50/50 LPU Claro", "descripcion": "Refrigerante 50/50 LPU Claro", "alcance": "Suministro e inyección en radiador", "unidad": "Galón", "unidad_medida": "Galón", "cantidad": 2},
            {"codigo_sap": "5003211", "nombre_item": "Empaque sellador termostato alta temperatura", "descripcion": "Empaque sellador", "alcance": "Ajuste perimetral hermético", "unidad": "Unidad", "unidad_medida": "Unidad", "cantidad": 1}
        ],
        "desea_transporte_especial": "Si",
        "tipo_transporte": "Vehículo 4x4",
        "distancia_km": 42.5,
        "tiempo_desplazamiento": "1h 45min",
        "observacion_transporte": "Acceso por trocha terciaria no pavimentada.",
        "transportes_especiales": [
            {"tipo_transporte": "Vehículo 4x4", "distancia_km": 42.5, "tiempo_desplazamiento": "1h 45min", "observacion": "Acceso por trocha no pavimentada"}
        ],
        "se_encontraron_novedades": "Si",
        "sistema_novedad": "Cerramiento y Balizamiento",
        "prioridad_novedad": "Media",
        "descripcion_novedad": "Malla eslabonada perimetral presenta rotura en costado norte.",
        "resuelto_en_visita": "No",
        "falla_resuelta": "Si",
        "observaciones_actividad": "PE queda en modo automático y sin alarmas. Nivel de refrigerante óptimo.",
        "evidencias_actividad": [
            {
                "id": "ev_1",
                "foto_url": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800",
                "descripcion": "Desmonte de bomba de agua averiada con fuga de refrigerante y limpieza de base del motor PE"
            },
            {
                "id": "ev_2",
                "foto_url": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800",
                "descripcion": "Instalación de bomba de agua nueva Selmec Perkins y ajuste de empaque sellador de alta temperatura"
            },
            {
                "id": "ev_3",
                "foto_url": "https://images.unsplash.com/photo-1581092335397-9583fe92d232?w=800",
                "descripcion": "Suministro de refrigerante 50/50 LPU Claro y pruebas con carga en automático sin alarmas"
            }
        ],
        "medicion_telurometro_valor": 4.8,
        "nombre_supervisor": ot1_so,
        "operadores_asignados": ops_ot1,
        "empresa_ejecutora": "DOBLEX S.A.S.",
        "firma_tecnico_nombre": "Carlos Hinestroza",
        "firma_tecnico_cedula": "1098765432",
        "firma_tecnico_empresa": "DOBLEX S.A.S.",
        "firma_tecnico_lat": 10.33452,
        "firma_tecnico_lng": -74.88721,
        "firma_tecnico_confirmada": True
    }

    f_inicio_1 = now_utc() - timedelta(days=2)
    ot1 = Ot(
        codigo="WO0000005558781",
        id_actividad="ACT-2026-5558781",
        tipo_actividad="correctivo",
        tipo_mantenimiento="correctivo",
        descripcion="Mantenimiento Correctivo GE/ATS - Falla en Bomba de Agua y Calibración en Carga de Planta Selmec 40SC",
        sitio=sitio_ant.nombre if sitio_ant else "ANT.APARTADO",
        sitio_id=sitio_ant.id if sitio_ant else None,
        ubicacion=f"{sitio_ant.municipio or 'Apartadó'}, {sitio_ant.zona_tecnica or 'Antioquia'}" if sitio_ant else "Apartadó, Antioquia",
        departamento="Antioquia",
        regional="R1",
        categoria="normal",
        tipo_estacion="MOVIL",
        site_owner=ot1_so,
        coordinador=emp_admin.nombre if emp_admin else "Admin General",
        created_by=admin.id,
        user_id=carlos.id,
        cuadrilla_id=cuadrilla_ant.id if cuadrilla_ant else None,
        prioridad="P1",
        tipo_ubicacion="urbana",
        subsistema="PE - GRUPO ELECTROGENO",
        progreso=50,
        estado="en_progreso",
        fecha_inicio=f_inicio_1,
        fecha_limite_sla=sla_service.calcular_fecha_limite("P1", "urbana", f_inicio_1),
        fecha_llegada_sitio=f_inicio_1 + timedelta(hours=2),
        datos_formulario=json.dumps(ot1_form, ensure_ascii=False)
    )

    # =========================================================================
    # OT 2: Emergencia - Estructura WO de Emergencia Chocó (Fuerza DC / Power)
    # =========================================================================
    ops_ot2 = [format_empleado_operador(emp_jasmin), format_empleado_operador(emp_lozano)]
    ops_ot2 = [op for op in ops_ot2 if op]
    ot2_so = (sitio_cho.supervisor_operativo or "CARLOS HINESTROZA") if sitio_cho else "CARLOS HINESTROZA"
    ot2_form = {
        "no_inc": "INC-48190",
        "tipo_actividad_label": "EMERGENCIAS",
        "tipo_sitio": "Rural",
        "subsistema": "PW - POWER",
        "presenta_afectacion": "Si",
        "tipo_equipo_falla": "Banco de Baterías / Rectificador DC",
        "marca_equipo": "Narada / Huawei",
        "modelo_equipo": "48V 500Ah",
        "reparacion": False,
        "reinstalacion": False,
        "cambio_equipo": True,
        "descripcion_falla": "Descarga atmosférica severa averió módulo de protección SPD e incendió dos celdas del banco de baterías 48V de repetidora.",
        "descripcion_solucion": "Desconexión de celdas dañadas, instalación de celda de reemplazo y reactivación de rectificador de fuerza DC.",
        "repuesto_retirado": {
            "descripcion": "Celda de batería 2V 500Ah sulfatada y averiada",
            "marca": "Narada",
            "modelo": "2V-500AH",
            "serial": "SN-BAT-08812"
        },
        "repuesto_instalado": {
            "descripcion": "Celda de batería 2V 500Ah nueva de reemplazo",
            "marca": "Narada",
            "modelo": "2V-500AH",
            "serial": "SN-BAT-99411"
        },
        "repuestos_cambios": [
            {
                "item_retirado": "Celda de batería 2V 500Ah sulfatada",
                "serial_retirado": "SN-BAT-08812",
                "item_instalado": "Celda de batería Narada 2V 500Ah nueva",
                "serial_instalado": "SN-BAT-99411",
                "cantidad": 1,
                "motivo": "Impacto de rayo y perforación dieléctrica de celda",
                "foto_retirado": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800",
                "foto_instalado": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800"
            }
        ],
        "materiales": [
            {"codigo_sap": "5004101", "nombre_item": "Cable de fuerza 2 AWG flexible", "descripcion": "Cable de fuerza 2 AWG", "alcance": "Reemplazo de puentes entre celdas", "unidad": "Metro", "unidad_medida": "Metro", "cantidad": 6},
            {"codigo_sap": "5004102", "nombre_item": "Terminal de compresión 2 AWG 1/4", "descripcion": "Terminal de compresión", "alcance": "Ponchado y termoencogible", "unidad": "Unidad", "unidad_medida": "Unidad", "cantidad": 4}
        ],
        "desea_transporte_especial": "Si",
        "tipo_transporte": "Lancha Fluvial",
        "distancia_km": 68.0,
        "tiempo_desplazamiento": "3h 30min",
        "observacion_transporte": "Transporte fluvial por el Río San Juan.",
        "transportes_especiales": [
            {"tipo_transporte": "Lancha Fluvial", "distancia_km": 68.0, "tiempo_desplazamiento": "3h 30min", "observacion": "Ruta fluvial por el Río San Juan"}
        ],
        "se_encontraron_novedades": "No",
        "falla_resuelta": "Si",
        "observaciones_actividad": "Estación queda transmitiendo en 54.2 VDC sin caída de tráfico.",
        "evidencias_actividad": [
            {
                "id": "ev_1",
                "foto_url": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800",
                "descripcion": "Desconexión de celdas 2V sulfatadas y dañadas por descarga atmosférica en banco de baterías"
            },
            {
                "id": "ev_2",
                "foto_url": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800",
                "descripcion": "Instalación de celda nueva Narada 2V 500Ah, ponchado de terminales y torqueo de puentes 2 AWG"
            }
        ],
        "medicion_telurometro_valor": 2.3,
        "nombre_supervisor": ot2_so,
        "operadores_asignados": ops_ot2,
        "empresa_ejecutora": "DOBLEX S.A.S.",
        "firma_tecnico_nombre": "Jasmin Mosquera",
        "firma_tecnico_cedula": "1002345678",
        "firma_tecnico_empresa": "DOBLEX S.A.S.",
        "firma_tecnico_lat": 5.69472,
        "firma_tecnico_lng": -76.66111,
        "firma_tecnico_confirmada": True
    }

    f_inicio_2 = now_utc() - timedelta(hours=14)
    ot2 = Ot(
        codigo="WO0000005558782",
        id_actividad="ACT-2026-099014",
        tipo_actividad="emergencia",
        tipo_mantenimiento="emergencia",
        descripcion="Mantenimiento de Emergencia Híbrido SFV & Power DC - Falla en Inversor y Banco de Baterías de Repetidora ZNI",
        sitio=sitio_cho.nombre if sitio_cho else "CHO.CANTON DE SAN PABLO",
        sitio_id=sitio_cho.id if sitio_cho else None,
        ubicacion=f"{sitio_cho.municipio or 'Cantón de San Pablo'}, Chocó" if sitio_cho else "Cantón de San Pablo, Chocó",
        departamento="Chocó",
        regional="R2",
        categoria="rural",
        tipo_estacion="REPETIDORA",
        site_owner=ot2_so,
        coordinador=emp_adminis.nombre if emp_adminis else "Auxiliar Técnico",
        created_by=adminis.id,
        user_id=carlos.id,
        cuadrilla_id=cuadrilla_ant.id if cuadrilla_ant else None,
        prioridad="P1",
        tipo_ubicacion="rural",
        subsistema="PW - POWER",
        progreso=25,
        estado="en_camino",
        fecha_inicio=f_inicio_2,
        fecha_limite_sla=sla_service.calcular_fecha_limite("P1", "rural", f_inicio_2),
        datos_formulario=json.dumps(ot2_form, ensure_ascii=False)
    )

    # =========================================================================
    # OT 3: Preventivo Planta Eléctrica - Bahía Solano (Ref: OT5304019)
    # =========================================================================
    ops_ot3 = [format_empleado_operador(emp_eliseo), format_empleado_operador(emp_jasmin)]
    ops_ot3 = [op for op in ops_ot3 if op]
    ot3_so = (sitio_bahia.supervisor_operativo or "ALEXANDER GÓMEZ") if sitio_bahia else "ALEXANDER GÓMEZ"
    ot3_form = {
        # 1. Datos Principales de Planta (Hoja PROPUESTA ELECTROGENO)
        "marca_equipo": "AGG POWER SOLUTIONS",
        "modelo_equipo": "C27D6",
        "serial_equipo": "A1904183",
        "horometro_inicial": 3913.36,
        "frecuencia_hz": 60,
        "capacidad_kva": 24,
        "marca_motor": "CUMMINS",
        "modelo_motor": "4B3.9-G2",
        "serial_motor": "78934783",
        "marca_generador": "STAMFORD",
        "modelo_generador": "PI144D1",
        "serial_generador": "B18G294552",
        "marca_ats": "ABB",
        "modelo_ats": "OTM-70A",
        "capacidad_ats_amp": 70,
        # 2. Baterías
        "voltaje_bateria": 25.2,
        "capacidad_bateria": 1150,
        "tipo_bateria": "Celda Húmeda",
        "estado_bornes": "Limpios y Ajustados",
        # 3. Servicio de Filtración y Lubricación
        "filtro_aceite_cambiado": "Realizado",
        "filtro_combustible_cambiado": "Realizado",
        "filtro_aire_estado": "Cambiado Nuevo",
        "cambio_aceite_motor": "Realizado (15W40)",
        "cambio_aceite": "SI",
        "cambio_filtros_aire": "SI",
        "cambio_filtros_combustible": "SI",
        "cambio_refrigerante": "SI",
        "galones_aceite_suministrados": 3.5,
        "nivel_refrigerante": "Normal",
        "fugas_lubricacion": "Sin Fugas",
        "presion_aceite_bar": 4.2,
        "presion_aceite_psi": 52,
        "temperatura_refrigerante_c": 78,
        "temperatura_motor_c": 78,
        # 4. Combustible (Hoja Prueba de Planta)
        "tamano_tanque_galones": 48,
        "nivel_combustible_porcentaje": 90,
        "estado_alarma_nivel": "Normal",
        "trampa_agua_drenada": "Si",
        "lineas_combustible_estado": "Conforme Sin Fugas",
        # 5. Prueba de Encendido ATS con Carga 15 Minutos
        "prueba_ats_15min": "Exitosa con Carga",
        "horometro_final_prueba": 3913.65,
        "tiempo_transferencia_seg": 8,
        "voltaje_l1_l2": 221,
        "voltaje_l2_l3": 223,
        "voltaje_l1_l3": 222,
        "voltaje_l1_n": 127,
        "voltaje_l2_n": 128,
        "voltaje_l3_n": 127,
        "corriente_l1_amp": 5.6,
        "corriente_l2_amp": 5.8,
        "corriente_l3_amp": 5.5,
        "porcentaje_cargabilidad": 8.0,
        "frecuencia_operacion_hz": 60,
        "planta_en_automatico": "Si",
        "presenta_alarmas": "No",
        "planta_temporizada": "No",
        "alarma_externa_noc_ok": "Si",
        "requiere_cambio_cabina": "No",
        "responsable_tec_1": emp_eliseo.nombre if emp_eliseo else "Eliseo Smith Granados",
        "responsable_tec_2": emp_jasmin.nombre if emp_jasmin else "Jasmin Ariel Mosquera",
        "plan_de_mejora": "Durante la ejecución del mantenimiento preventivo se verificó el correcto funcionamiento del grupo electrógeno. La planta queda 100% operativa en modo automático.",
        "observaciones_preventivo": "Mantenimiento preventivo integral según formato RPT Bahía Solano. Prueba de encendido de planta durante 15 minutos soportando carga real sin novedades.",
        "operadores_asignados": ops_ot3
    }

    f_inicio_3 = now_utc() - timedelta(days=4)
    ot3 = Ot(
        codigo="OT5304019",
        id_actividad="ACT-2026-5304019",
        tipo_actividad="preventivo_planta",
        tipo_mantenimiento="preventivo",
        descripcion="Mantenimiento Preventivo Planta Eléctrica AGG Power - Inspección Operativa, Medición en Carga y Pruebas ATS (Ref. RPT Bahía Solano)",
        sitio=sitio_bahia.nombre if sitio_bahia else "CHO.RPT.BAHIA SOLANO",
        sitio_id=sitio_bahia.id if sitio_bahia else None,
        ubicacion=f"{sitio_bahia.municipio or 'Bahía Solano'}, Chocó" if sitio_bahia else "Bahía Solano, Chocó",
        departamento="Chocó",
        regional="R2",
        categoria="rural",
        tipo_estacion="REPETIDORA",
        site_owner=ot3_so,
        coordinador=emp_admin.nombre if emp_admin else "Admin General",
        created_by=admin.id,
        user_id=carlos.id,
        cuadrilla_id=cuadrilla_ant.id if cuadrilla_ant else None,
        prioridad="P2",
        tipo_ubicacion="rural",
        subsistema="Movil Plantas Eléctricas",
        progreso=60,
        estado="en_sitio",
        fecha_inicio=f_inicio_3,
        fecha_limite_sla=sla_service.calcular_fecha_limite("P2", "rural", f_inicio_3),
        fecha_llegada_sitio=f_inicio_3 + timedelta(hours=2),
        datos_formulario=json.dumps(ot3_form, ensure_ascii=False)
    )

    # =========================================================================
    # OT 4: Preventivo Aire Acondicionado - Montería (Ref: WO0000005520436)
    # =========================================================================
    ops_ot4 = [format_empleado_operador(emp_ancizar), format_empleado_operador(emp_ramon)]
    ops_ot4 = [op for op in ops_ot4 if op]
    ot4_so = (sitio_mon.supervisor_operativo or "SANDRA MORALES") if sitio_mon else "SANDRA MORALES"
    ot4_form = {
        "marca_aa": "ComfortStar",
        "marca_equipo": "ComfortStar",
        "modelo_equipo": "CP-24K-INV",
        "serial_equipo": "CS-98412-2024",
        "tipo_aire": "Mini Split Inverter",
        "capacidad_btu": 24000,
        "capacidad_btu_aa": 24,
        "estado_equipo_aa": "OPERATIVO",
        "tipo_refrigerante": "R410A",
        "compresor_refrigerante": "R410A",
        "presion_succion_psi": 120,
        "presion_baja_psi": 120,
        "presion_descarga_psi": 350,
        "presion_alta_psi": 350,
        "compresor_corriente": 9.8,
        "corriente_compresor_amp": 9.8,
        "voltaje_alimentacion_aa": 220,
        "compresor_voltaje": 220,
        "temperatura_cuarto_equipo": 30.0,
        "temperatura_aa_entrada": 28.0,
        "temperatura_aa_salida": 14.0,
        "temperatura_inyeccion_c": 14.0,
        "temperatura_retorno_c": 28.0,
        "ajuste_termostato": 22.0,
        "limpieza_evaporador": "Si",
        "limpieza_condensador": "Si",
        "cambio_lavado_filtros": "Si",
        "desague_drenaje_ok": "Si",
        "responsable_tec_1": emp_ancizar.nombre if emp_ancizar else "Ancízar Manuel Pérez",
        "responsable_tec_2": emp_ramon.nombre if emp_ramon else "Ramón Elías Yepes",
        "plan_de_mejora": "Durante la ejecución del mantenimiento preventivo de climatización se realizó limpieza profunda de serpentines y filtros. Las presiones frigoríficas y salto térmico quedaron en parámetros óptimos (14.0°C).",
        "observaciones_preventivo": "Mantenimiento preventivo general a equipo de climatización shelter. Serpentines desincrustados con hidrolavadora, presiones en rango óptimo.",
        "operadores_asignados": ops_ot4
    }

    f_inicio_4 = now_utc() - timedelta(days=1)
    ot4 = Ot(
        codigo="WO0000005520436",
        id_actividad="ACT-2026-030401",
        tipo_actividad="preventivo_aire",
        tipo_mantenimiento="preventivo",
        descripcion="Mantenimiento Preventivo & Climatización AA Móvil - Servicio a Compresores y Condensadoras de Shelter de Transmisión (Ref. Paseo Bolívar)",
        sitio=sitio_mon.nombre if sitio_mon else "MON.MONTERIA",
        sitio_id=sitio_mon.id if sitio_mon else None,
        ubicacion=f"{sitio_mon.municipio or 'Montería'}, Córdoba" if sitio_mon else "Montería, Córdoba",
        departamento="Córdoba",
        regional="R1",
        categoria="normal",
        tipo_estacion="MOVIL",
        site_owner=ot4_so,
        coordinador=emp_adminis.nombre if emp_adminis else "Auxiliar Técnico",
        created_by=adminis.id,
        user_id=carlos.id,
        cuadrilla_id=cuadrilla_cor.id if cuadrilla_cor else None,
        prioridad="P2",
        tipo_ubicacion="urbana",
        subsistema="AA - AIRES ACONDICIONADOS",
        progreso=65,
        estado="en_sitio",
        fecha_inicio=f_inicio_4,
        fecha_limite_sla=sla_service.calcular_fecha_limite("P2", "urbana", f_inicio_4),
        fecha_llegada_sitio=f_inicio_4 + timedelta(hours=3),
        datos_formulario=json.dumps(ot4_form, ensure_ascii=False)
    )

    # =========================================================================
    # OT 5: Rutina MP 7x24 - Planta Eléctrica (Rutina 1)
    # =========================================================================
    ops_ot5 = [format_empleado_operador(emp_jasmin), format_empleado_operador(emp_lozano)]
    ops_ot5 = [op for op in ops_ot5 if op]
    ot5_so = (sitio_pizarro.supervisor_operativo or "ALEXANDER GOMEZ") if sitio_pizarro else "ALEXANDER GOMEZ"
    ot5_form = {
        "numero_rutina_7x24": "Rutina 1",
        "marca_equipo": "Cummins Power",
        "modelo_equipo": "C33D5",
        "serial_equipo": "CP-449102",
        "horometro_inicial": 2150.4,
        "frecuencia_hz": 60,
        "capacidad_kva": 33,
        "voltaje_bateria": 25.8,
        "presion_aceite_bar": 4.2,
        "temperatura_refrigerante_c": 78,
        "nivel_combustible_porcentaje": 85,
        "filtro_aceite_cambiado": "Realizado",
        "filtro_combustible_cambiado": "Realizado",
        "cambio_aceite_motor": "Realizado (15W40)",
        "galones_aceite_suministrados": 3.8,
        "nivel_refrigerante": "Normal",
        "prueba_ats_15min": "Exitosa con Carga",
        "horometro_final_prueba": 2150.7,
        "voltaje_l1_l2": 220,
        "voltaje_l2_l3": 220,
        "voltaje_l1_l3": 220,
        "planta_en_automatico": "Si",
        "presenta_alarmas": "No",
        "responsable_tec_1": emp_jasmin.nombre if emp_jasmin else "Jasmin Ariel Mosquera",
        "responsable_tec_2": emp_lozano.nombre if emp_lozano else "Carlos Rafael Lozano",
        "plan_de_mejora": "Se cumplió con el protocolo de rutina decenal 1/3 para planta eléctrica, verificando encendido automático ante simulación de falla de red.",
        "observaciones_preventivo": "Rutina preventiva programada 7x24 completada sin observaciones. Tablero sin alarmas y transferencia automática en modo automático.",
        "operadores_asignados": ops_ot5
    }

    f_inicio_5 = now_utc() - timedelta(days=6)
    ot5 = Ot(
        codigo="OT5304021",
        id_actividad="ACT-2026-078192",
        tipo_actividad="rutina_7x24_planta",
        tipo_mantenimiento="preventivo",
        descripcion="Rutina Preventiva MP 7x24 Planta Eléctrica - Pruebas de Transferencia y Calidad de Red",
        sitio=sitio_pizarro.nombre if sitio_pizarro else "CHO.PIZARRO",
        sitio_id=sitio_pizarro.id if sitio_pizarro else None,
        ubicacion=f"{sitio_pizarro.municipio or 'Pizarro'}, Chocó" if sitio_pizarro else "Pizarro, Chocó",
        departamento="Chocó",
        regional="R2",
        categoria="rural",
        tipo_estacion="MOVIL",
        site_owner=ot5_so,
        coordinador=emp_adminis.nombre if emp_adminis else "Auxiliar Técnico",
        created_by=admin.id,
        user_id=carlos.id,
        cuadrilla_id=cuadrilla_ant.id if cuadrilla_ant else None,
        prioridad="P2",
        tipo_ubicacion="rural",
        subsistema="Movil Rutinas 7x24 - Planta Eléctrica",
        progreso=50,
        estado="en_sitio",
        fecha_inicio=f_inicio_5,
        fecha_limite_sla=sla_service.calcular_fecha_limite("P2", "rural", f_inicio_5),
        fecha_llegada_sitio=f_inicio_5 + timedelta(hours=2),
        observaciones_cierre="Rutina de inspección y mantenimiento preventivo ejecutada en su totalidad con pruebas ATS en carga.",
        datos_formulario=json.dumps(ot5_form, ensure_ascii=False)
    )

    # =========================================================================
    # OT 6: Rutina MP 7x24 - Aire Acondicionado (Rutina 2)
    # =========================================================================
    ops_ot6 = [format_empleado_operador(emp_carlos), format_empleado_operador(emp_julian)]
    ops_ot6 = [op for op in ops_ot6 if op]
    ot6_so = (sitio_turbo.supervisor_operativo or "CLEYVER ESPITIA") if sitio_turbo else "CLEYVER ESPITIA"
    ot6_form = {
        "numero_rutina_7x24": "Rutina 2",
        "marca_aa": "Carrier",
        "marca_equipo": "Carrier",
        "tipo_aire": "Mini Split Inverter",
        "capacidad_btu_aa": 24,
        "estado_equipo_aa": "OPERATIVO",
        "temperatura_cuarto_equipo": 23.5,
        "temperatura_aa_entrada": 24.0,
        "temperatura_aa_salida": 14.5,
        "ajuste_termostato": 22.0,
        "compresor_refrigerante": "R410A",
        "presion_succion_psi": 118,
        "presion_descarga_psi": 345,
        "compresor_corriente": 9.5,
        "compresor_voltaje": 220,
        "limpieza_evaporador": "Si",
        "limpieza_condensador": "Si",
        "cambio_lavado_filtros": "Si",
        "desague_drenaje_ok": "Si",
        "responsable_tec_1": emp_carlos.nombre if emp_carlos else "Ing. Carlos Pérez",
        "responsable_tec_2": emp_julian.nombre if emp_julian else "Julián Alexander Rivillas",
        "plan_de_mejora": "Rutina periódica decenal 2/3 de climatización ejecutada con balance térmico y alternancia de unidades AA1/AA2.",
        "observaciones_preventivo": "Mantenimiento decenal 7x24 ejecutado en sistema de aire acondicionado del shelter. Funcionamiento alternado y termostato calibrado a 22°C.",
        "operadores_asignados": ops_ot6
    }

    f_inicio_6 = now_utc() - timedelta(days=2)
    ot6 = Ot(
        codigo="OT5304022",
        id_actividad="ACT-2026-078193",
        tipo_actividad="rutina_7x24_aire",
        tipo_mantenimiento="preventivo",
        descripcion="Rutina Preventiva MP 7x24 Climatización AA - Inspección Operativa y Calibración de Termostato Shelter",
        sitio=sitio_turbo.nombre if sitio_turbo else "ANT.TURBO",
        sitio_id=sitio_turbo.id if sitio_turbo else None,
        ubicacion=f"{sitio_turbo.municipio or 'Turbo'}, Antioquia" if sitio_turbo else "Turbo, Antioquia",
        departamento="Antioquia",
        regional="R1",
        categoria="normal",
        tipo_estacion="MOVIL",
        site_owner=ot6_so,
        coordinador=emp_carlos.nombre if emp_carlos else "Ing. Carlos Pérez",
        created_by=admin.id,
        user_id=carlos.id,
        cuadrilla_id=cuadrilla_ant.id if cuadrilla_ant else None,
        prioridad="P2",
        tipo_ubicacion="urbana",
        subsistema="Movil Rutinas 7x24 - Aire Acondicionado",
        progreso=75,
        estado="en_sitio",
        fecha_inicio=f_inicio_6,
        fecha_limite_sla=sla_service.calcular_fecha_limite("P2", "urbana", f_inicio_6),
        fecha_llegada_sitio=f_inicio_6 + timedelta(hours=3),
        datos_formulario=json.dumps(ot6_form, ensure_ascii=False)
    )

    # =========================================================================
    # OT 7: Obra Civil e Infraestructura (Ref: PreLiquidación ANT.Zungo 2)
    # =========================================================================
    ops_ot7 = [format_empleado_operador(emp_carlos), format_empleado_operador(emp_manuel)]
    ops_ot7 = [op for op in ops_ot7 if op]
    ot7_so = (sitio_zungo.supervisor_operativo or "CLEYVER ESPITIA") if sitio_zungo else "CLEYVER ESPITIA"
    ot7_form = {
        "tipo_sitio": "Rural",
        "subsistema": "Infraestructura y Obra Civil",
        "descripcion_solucion": "Adecuación integral de infraestructura civil y cerramiento perimetral según especificaciones técnicas Claro Colombia.",
        "observaciones_obra": "Se realizó fundición de losa reforzada 3000 PSI para base del grupo electrógeno y reconstrucción de cerramiento perimetral en malla eslabonada calibre 10 con concertina.",
        "items_obra_civil": [
            {
                "codigo_sap": "5012301",
                "nombre_item": "Cerramiento en Malla Eslabonada Cal. 10 con Concertina",
                "alcance": "Suministro e instalación de cerramiento perimetral galvanizado con concertina helicoidal de seguridad",
                "unidad_medida": "ML",
                "cantidad": 18.5,
                "observaciones": "Costado norte y oriental de la estación base"
            },
            {
                "codigo_sap": "5012302",
                "nombre_item": "Losa de Concreto Reforzado 3000 PSI para GE",
                "alcance": "Excavación, formaleta, armadura en acero y fundición de losa impermeabilizada para motogenerador",
                "unidad_medida": "M3",
                "cantidad": 2.4,
                "observaciones": "Base de soporte con anclajes antivibración"
            },
            {
                "codigo_sap": "5012303",
                "nombre_item": "Pintura Epóxica / Balizamiento Anticorrosivo",
                "alcance": "Pintura anticorrosiva de portón metálico y señalización de seguridad perimetral",
                "unidad_medida": "M2",
                "cantidad": 45.0,
                "observaciones": "Portón vehicular y postes esquineros"
            },
            {
                "codigo_sap": "5012304",
                "nombre_item": "Bajante de Protección contra Rayos (LPS) en Cobre 2/0",
                "alcance": "Tendido de cable bajante de pararrayos y sujeción con grapas de bronce a torre",
                "unidad_medida": "ML",
                "cantidad": 32.0,
                "observaciones": "Conexión a electrodo de puesta a tierra con soldadura exotérmica"
            },
            {
                "codigo_sap": "5012305",
                "nombre_item": "Retiro y Disposición Final de Escombros",
                "alcance": "Limpieza general, cargue y transporte de material sobrante a botadero autorizado",
                "unidad_medida": "GL",
                "cantidad": 1.0,
                "observaciones": "Área técnica despejada y limpia"
            }
        ],
        "desea_transporte_especial": "Si",
        "tipo_transporte": "Camión de Carga 3.5 Ton",
        "distancia_km": 38.0,
        "tiempo_desplazamiento": "1h 30min",
        "observacion_transporte": "Transporte de agregados, cemento, malla galvanizada y herramienta pesada.",
        "transportes_especiales": [
            {"tipo_transporte": "Camión de Carga 3.5 Ton", "distancia_km": 38.0, "tiempo_desplazamiento": "1h 30min", "observacion": "Transporte de materiales pesados y cemento"}
        ],
        "nombre_supervisor": ot7_so,
        "operadores_asignados": ops_ot7
    }

    f_inicio_7 = now_utc() - timedelta(days=3)
    ot7 = Ot(
        codigo="OC2026-091101",
        id_actividad="ACT-2026-091101",
        tipo_actividad="obra_civil",
        tipo_mantenimiento="correctivo",
        descripcion="Liquidación de Obra Civil e Infraestructura - Cerramiento Perimetral en Malla, Losa de Motogenerador y Bajante LPS (Ref. ANT.Zungo 2)",
        sitio=sitio_zungo.nombre if sitio_zungo else "ANT.ZUNGO-2",
        sitio_id=sitio_zungo.id if sitio_zungo else None,
        ubicacion=f"{sitio_zungo.municipio or 'Carepa'}, Antioquia" if sitio_zungo else "Carepa, Antioquia",
        departamento="Antioquia",
        regional="R1",
        categoria="rural",
        tipo_estacion="MOVIL",
        site_owner=ot7_so,
        coordinador=emp_admin.nombre if emp_admin else "Admin General",
        created_by=admin.id,
        user_id=carlos.id,
        cuadrilla_id=cuadrilla_ant.id if cuadrilla_ant else None,
        prioridad="P2",
        tipo_ubicacion="rural",
        subsistema="Infraestructura y Obra Civil",
        progreso=70,
        estado="en_progreso",
        fecha_inicio=f_inicio_7,
        fecha_limite_sla=sla_service.calcular_fecha_limite("P2", "rural", f_inicio_7),
        fecha_llegada_sitio=f_inicio_7 + timedelta(hours=2),
        datos_formulario=json.dumps(ot7_form, ensure_ascii=False)
    )

    # =========================================================================
    # OT 8: Informe 360 - Relevamiento Técnico Integral Claro (Plantillas 360)
    # =========================================================================
    ops_ot8 = [format_empleado_operador(emp_carlos), format_empleado_operador(emp_julian)]
    ops_ot8 = [op for op in ops_ot8 if op]
    ot8_so = (sitio_titi.supervisor_operativo or "ROBERTO VELEZ") if sitio_titi else "ROBERTO VELEZ"
    ot8_form = {
        # 1. Datos Generales GE y Vida Útil
        "ge_estacion_base": sitio_titi.nombre if sitio_titi else "ANT.TITIRIBI",
        "ge_fecha_solicitud": (now_utc() - timedelta(days=3)).strftime("%Y-%m-%d"),
        "ge_horometro": 4120.5,
        "horometro_inicial": 4120.5,
        "ge_marca_planta": "CATERPILLAR OLYMPIAN",
        "marca_equipo": "CATERPILLAR OLYMPIAN",
        "ge_modelo_planta": "GEP33-3",
        "ge_estado_fisico": "BUENO",
        "ge_estado_operacional": "OPERATIVO",
        "ge_potencia_kw": 30,
        "ge_consumo_kva": 37.5,
        "capacidad_kva": 37.5,
        "voltaje_bateria": 25.6,
        "ge_marca_generador": "LEROY SOMER",
        "ge_modelo_generador": "LL1514P",
        "vida_util_calculada_pct": 85,
        # Matriz SMU de los 6 Subsistemas GE
        "diagnosticos_smu": {
            "devanado_generador": {
                "calificacion": "Bueno",
                "hallazgo": "Aislamiento conforme superior a 14 MΩ con devanados limpios",
                "accion": "Mantener protocolo de limpieza periódica"
            },
            "motor_diesel": {
                "calificacion": "Bueno",
                "hallazgo": "Presión de lubricación y compresión óptimas sin fugas",
                "accion": "Servicio de lubricación y filtros vigente"
            },
            "sistema_control": {
                "calificacion": "Bueno",
                "hallazgo": "Módulo ComAp operativo con parámetros digitales estables",
                "accion": "Inspección de cableado y terminales de control"
            },
            "sistema_refrigeracion": {
                "calificacion": "Bueno",
                "hallazgo": "Radiador sin obstrucciones y mangueras en buen estado",
                "accion": "Verificar nivel de refrigerante periódicamente"
            },
            "sistema_electrico": {
                "calificacion": "Regular",
                "hallazgo": "Leve sulfatación en borne positivo de batería de arranque",
                "accion": "Limpieza mecánica y aplicación de grasa dieléctrica"
            },
            "sistema_escape": {
                "calificacion": "Bueno",
                "hallazgo": "Silenciador y empaques sin fugas de gases de escape",
                "accion": "Revisión de mantas térmicas aislantes"
            }
        },
        # 2. Prueba Megger (Aislamiento Alternador IEEE 43)
        "megger_vdc_prueba": 1000,
        "megger_temp_c": 28,
        "megger_hr_porcentaje": 68,
        "megger_r_min_criterio": 5.0,
        "megger_pi_min_criterio": 2.0,
        "megger_cumple_global": True,
        "megger_mediciones": {
            "u_tierra": {"r1": 14.5, "r10": 32.0, "pi": 2.21, "cumple": True},
            "v_tierra": {"r1": 15.2, "r10": 33.5, "pi": 2.20, "cumple": True},
            "w_tierra": {"r1": 14.8, "r10": 32.8, "pi": 2.22, "cumple": True},
            "u_v": {"r1": 28.0, "r10": 60.0, "pi": 2.14, "cumple": True},
            "v_w": {"r1": 29.5, "r10": 62.0, "pi": 2.10, "cumple": True},
            "w_u": {"r1": 28.9, "r10": 61.2, "pi": 2.12, "cumple": True},
            "excitacion_tierra": {"r1": 45.0, "r10": 98.0, "pi": 2.18, "cumple": True}
        },
        "megger_diagnostico": "Aislamiento dieléctrico en devanados del generador conforme con norma IEEE 43 (> 5 MΩ e IP > 2.0).",
        "megger_plan_accion": "Mantener monitoreo anual durante mantenimiento preventivo 360.",
        # 3. Prueba Banco de Carga Resistivo 80% (60 Minutos)
        "banco_vnom_ll": 220,
        "banco_fnom_hz": 60,
        "banco_carga_objetivo_pct": 80,
        "banco_carga_lecturas": [
            {"tiempo": "00:05", "u_v": 220, "hz": 60.1, "i_u": 65.4, "kw": 24, "temp_c": 74, "presion_psi": "52 PSI", "notas": "Inicio de prueba. Curva de calentamiento normal."},
            {"tiempo": "00:15", "u_v": 220, "hz": 60.0, "i_u": 65.2, "kw": 24, "temp_c": 78, "presion_psi": "51 PSI", "notas": "Voltaje y frecuencia plenamente estables."},
            {"tiempo": "00:30", "u_v": 219, "hz": 60.0, "i_u": 65.5, "kw": 24, "temp_c": 80, "presion_psi": "50 PSI", "notas": "Temperatura estabilizada sin variaciones."},
            {"tiempo": "00:45", "u_v": 220, "hz": 60.0, "i_u": 65.3, "kw": 24, "temp_c": 81, "presion_psi": "50 PSI", "notas": "Operación silenciosa y sin vibración."},
            {"tiempo": "01:00", "u_v": 220, "hz": 60.0, "i_u": 65.4, "kw": 24, "temp_c": 81, "presion_psi": "50 PSI", "notas": "Prueba finalizada satisfactoriamente. Grupo Electrógeno APTO."}
        ],
        "banco_conclusion": "APTO",
        "banco_observaciones": "Comportamiento electromecánico sobresaliente. Frecuencia y voltaje dentro de la tolerancia de ±1.5%.",
        # 4. Inspección SPT Claro
        "spt_wenner_resistividad": 112.5,
        "spt_condicion_suelo": "Roca / Concreto",
        "spt_caida_potencial_r": 2.35,
        "spt_caida_observaciones": "Resistencia de puesta a tierra excelente cumpliendo RETIE/IEC (< 5.0 Ω).",
        "spt_puntos_equipotencial": [
            {"id": 1, "elemento": "Barra Equipotencial Principal (BEP) / Barraje de tierra", "r_medida": 0.03, "cumple": True},
            {"id": 2, "elemento": "Rack / gabinete de ACCESO RAN (BTS/BBU/DU) – chasis", "r_medida": 0.05, "cumple": True},
            {"id": 3, "elemento": "Rack / gabinete de TRANSMISIÓN (MW IDU / Router) – chasis", "r_medida": 0.06, "cumple": True},
            {"id": 4, "elemento": "Gabinete RECTIFICADOR / POWER DC (-48V) – chasis", "r_medida": 0.04, "cumple": True},
            {"id": 5, "elemento": "Banco de BATERÍAS (rack/caja y bandejas) – estructura", "r_medida": 0.05, "cumple": True},
            {"id": 6, "elemento": "Tablero de DISTRIBUCIÓN DC (PDB / fusiblera) – carcasa", "r_medida": 0.06, "cumple": True},
            {"id": 7, "elemento": "Tablero GENERAL AC / protecciones (TGP) – carcasa", "r_medida": 0.07, "cumple": True},
            {"id": 8, "elemento": "TRANSFERENCIA AUTOMÁTICA (ATS) – carcasa metálica", "r_medida": 0.09, "cumple": True},
            {"id": 9, "elemento": "GRUPO ELECTRÓGENO (chasis/bastidor + alternador)", "r_medida": 0.05, "cumple": True},
            {"id": 10, "elemento": "AIRES ACONDICIONADOS (AA-1 y AA-2) – chasis metálico", "r_medida": 0.08, "cumple": True},
            {"id": 11, "elemento": "Torre/estructura metálica + bajante LPS (pararrayos)", "r_medida": 0.11, "cumple": True}
        ],
        # 5. Instrumentos y Calibración
        "instrumentos_calibracion": [
            {"tipo": "Megóhmetro de Aislamiento", "marca": "Fluke", "modelo": "1587 FC", "serial": "FLK-1587-99214", "fecha_calibracion": "2026-02-15"},
            {"tipo": "Telurómetro / Medidor de Tierra", "marca": "AEMC", "modelo": "4630", "serial": "AEMC-4630-8812", "fecha_calibracion": "2026-01-20"},
            {"tipo": "Pinza Amperimétrica True RMS", "marca": "Fluke", "modelo": "376 FC", "serial": "FLK-376-77341", "fecha_calibracion": "2026-03-10"}
        ],
        "operadores_asignados": ops_ot8
    }

    f_inicio_8 = now_utc() - timedelta(days=3)
    ot8 = Ot(
        codigo="OT360000101",
        id_actividad="ACT-2026-3600101",
        tipo_actividad="informe_360",
        tipo_mantenimiento="preventivo",
        descripcion="Informe 360 Relevamiento Integral Claro - Megger Aislamiento, Banco Resistivo 80%, Inspección SPT y Diagnóstico SMU de 6 Subsistemas GE",
        sitio=sitio_titi.nombre if sitio_titi else "ANT.TITIRIBI",
        sitio_id=sitio_titi.id if sitio_titi else None,
        ubicacion=f"{sitio_titi.municipio or 'Titiribí'}, Antioquia" if sitio_titi else "Titiribí, Antioquia",
        departamento="Antioquia",
        regional="R1",
        categoria="rural",
        tipo_estacion="MOVIL",
        site_owner=ot8_so,
        coordinador=emp_carlos.nombre if emp_carlos else "Ing. Carlos Pérez",
        created_by=admin.id,
        user_id=carlos.id,
        cuadrilla_id=cuadrilla_ant.id if cuadrilla_ant else None,
        prioridad="P2",
        tipo_ubicacion="rural",
        subsistema="Inspección y Relevamiento 360",
        progreso=85,
        estado="en_progreso",
        fecha_inicio=f_inicio_8,
        fecha_limite_sla=sla_service.calcular_fecha_limite("P2", "rural", f_inicio_8),
        fecha_llegada_sitio=f_inicio_8 + timedelta(hours=2),
        datos_formulario=json.dumps(ot8_form, ensure_ascii=False)
    )

    db.add_all([ot1, ot2, ot3, ot4, ot5, ot6, ot7, ot8])
    db.commit()

    # 4. Evidencias Fotográficas Georreferenciadas (con foto obligatoria de llegada a sitio en todas)
    print(f"[{db_name}] 3. Creando evidencias fotográficas georreferenciadas (con foto de llegada obligatoria)...")
    evidencias = [
        # OT 1: Correctivo
        EvidenciaFotografica(ot_id=ot1.id, tipo="llegada_sitio", url_imagen="https://images.unsplash.com/photo-1541888946425-d0fbb186f5f8?w=800", latitud=7.8829, longitud=-76.6256, fecha_hora_captura=f_inicio_1 + timedelta(hours=1)),
        EvidenciaFotografica(ot_id=ot1.id, tipo="antes", url_imagen="https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800", latitud=7.8829, longitud=-76.6256, fecha_hora_captura=f_inicio_1 + timedelta(hours=2)),
        EvidenciaFotografica(ot_id=ot1.id, tipo="despues", url_imagen="https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800", latitud=7.8829, longitud=-76.6256, fecha_hora_captura=f_inicio_1 + timedelta(hours=4)),

        # OT 2: Emergencia
        EvidenciaFotografica(ot_id=ot2.id, tipo="llegada_sitio", url_imagen="https://images.unsplash.com/photo-1541888946425-d0fbb186f5f8?w=800", latitud=5.3120, longitud=-76.7820, fecha_hora_captura=f_inicio_2 + timedelta(hours=2)),
        EvidenciaFotografica(ot_id=ot2.id, tipo="antes", url_imagen="https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800", latitud=5.3120, longitud=-76.7820, fecha_hora_captura=f_inicio_2 + timedelta(hours=3)),

        # OT 3: Preventivo Planta
        EvidenciaFotografica(ot_id=ot3.id, tipo="llegada_sitio", url_imagen="https://images.unsplash.com/photo-1541888946425-d0fbb186f5f8?w=800", latitud=6.2269, longitud=-77.4044, fecha_hora_captura=f_inicio_3 + timedelta(hours=1)),
        EvidenciaFotografica(ot_id=ot3.id, tipo="antes", url_imagen="https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800", latitud=6.2269, longitud=-77.4044, fecha_hora_captura=f_inicio_3 + timedelta(hours=2)),
        EvidenciaFotografica(ot_id=ot3.id, tipo="durante", url_imagen="https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800", latitud=6.2270, longitud=-77.4045, fecha_hora_captura=f_inicio_3 + timedelta(hours=4)),
        EvidenciaFotografica(ot_id=ot3.id, tipo="despues", url_imagen="https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800", latitud=6.2269, longitud=-77.4044, fecha_hora_captura=f_inicio_3 + timedelta(hours=6)),

        # OT 4: Preventivo Aire
        EvidenciaFotografica(ot_id=ot4.id, tipo="llegada_sitio", url_imagen="https://images.unsplash.com/photo-1541888946425-d0fbb186f5f8?w=800", latitud=8.7500, longitud=-75.8833, fecha_hora_captura=f_inicio_4 + timedelta(hours=1)),
        EvidenciaFotografica(ot_id=ot4.id, tipo="durante", url_imagen="https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800", latitud=8.7500, longitud=-75.8833, fecha_hora_captura=f_inicio_4 + timedelta(hours=2)),
        EvidenciaFotografica(ot_id=ot4.id, tipo="despues", url_imagen="https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800", latitud=8.7500, longitud=-75.8833, fecha_hora_captura=f_inicio_4 + timedelta(hours=3)),

        # OT 5: Rutina 7x24 Planta
        EvidenciaFotografica(ot_id=ot5.id, tipo="llegada_sitio", url_imagen="https://images.unsplash.com/photo-1541888946425-d0fbb186f5f8?w=800", latitud=4.9500, longitud=-77.3667, fecha_hora_captura=f_inicio_5 + timedelta(hours=2)),
        EvidenciaFotografica(ot_id=ot5.id, tipo="despues", url_imagen="https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800", latitud=4.9500, longitud=-77.3667, fecha_hora_captura=f_inicio_5 + timedelta(hours=6)),

        # OT 6: Rutina 7x24 Aire
        EvidenciaFotografica(ot_id=ot6.id, tipo="llegada_sitio", url_imagen="https://images.unsplash.com/photo-1541888946425-d0fbb186f5f8?w=800", latitud=8.0927, longitud=-76.7283, fecha_hora_captura=f_inicio_6 + timedelta(hours=1)),
        EvidenciaFotografica(ot_id=ot6.id, tipo="durante", url_imagen="https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800", latitud=8.0927, longitud=-76.7283, fecha_hora_captura=f_inicio_6 + timedelta(hours=2)),

        # OT 7: Obra Civil
        EvidenciaFotografica(ot_id=ot7.id, tipo="llegada_sitio", url_imagen="https://images.unsplash.com/photo-1541888946425-d0fbb186f5f8?w=800", latitud=7.7564, longitud=-76.6578, fecha_hora_captura=f_inicio_7 + timedelta(hours=1)),
        EvidenciaFotografica(ot_id=ot7.id, tipo="obra_civil", url_imagen="https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800", latitud=7.7564, longitud=-76.6578, fecha_hora_captura=f_inicio_7 + timedelta(hours=2)),
        EvidenciaFotografica(ot_id=ot7.id, tipo="despues", url_imagen="https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800", latitud=7.7564, longitud=-76.6578, fecha_hora_captura=f_inicio_7 + timedelta(hours=5)),

        # OT 8: Relevamiento 360
        EvidenciaFotografica(ot_id=ot8.id, tipo="llegada_sitio", url_imagen="https://images.unsplash.com/photo-1541888946425-d0fbb186f5f8?w=800", latitud=6.0619, longitud=-75.7925, fecha_hora_captura=f_inicio_8 + timedelta(hours=1)),
        EvidenciaFotografica(ot_id=ot8.id, tipo="diagnostico_360", url_imagen="https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800", latitud=6.0619, longitud=-75.7925, fecha_hora_captura=f_inicio_8 + timedelta(hours=2)),
        EvidenciaFotografica(ot_id=ot8.id, tipo="pruebas", url_imagen="https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800", latitud=6.0619, longitud=-75.7925, fecha_hora_captura=f_inicio_8 + timedelta(hours=3)),
        EvidenciaFotografica(ot_id=ot8.id, tipo="spt", url_imagen="https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800", latitud=6.0619, longitud=-75.7925, fecha_hora_captura=f_inicio_8 + timedelta(hours=4))
    ]
    db.add_all(evidencias)

    # 5. Repuestos e Insumos LPU
    print(f"[{db_name}] 4. Creando insumos y repuestos LPU vinculados...")
    repuestos = [
        RepuestoUtilizado(ot_id=ot1.id, nombre_item="Bomba de agua Selmec Perkins 40SC", cantidad=1.0, unidad_medida="Unidad"),
        RepuestoUtilizado(ot_id=ot1.id, nombre_item="Refrigerante Anticongelante 50/50 LPU Claro", cantidad=2.0, unidad_medida="Galón"),
        RepuestoUtilizado(ot_id=ot2.id, nombre_item="Celda de Batería 2V 500Ah Narada", cantidad=1.0, unidad_medida="Unidad"),
        RepuestoUtilizado(ot_id=ot2.id, nombre_item="Cable de Fuerza 2 AWG flexible", cantidad=6.0, unidad_medida="Metro"),
        RepuestoUtilizado(ot_id=ot3.id, nombre_item="Filtro de Aceite LF16015 Fleetguard", cantidad=1.0, unidad_medida="Unidad"),
        RepuestoUtilizado(ot_id=ot3.id, nombre_item="Filtro Separador Combustible FS1242", cantidad=1.0, unidad_medida="Unidad"),
        RepuestoUtilizado(ot_id=ot3.id, nombre_item="Aceite Lubricante 15W40 CI-4", cantidad=3.5, unidad_medida="Galón"),
        RepuestoUtilizado(ot_id=ot4.id, nombre_item="Gas Refrigerante Ecológico R410A", cantidad=3.0, unidad_medida="Kg"),
        RepuestoUtilizado(ot_id=ot4.id, nombre_item="Filtro de Aire Lavable Tipo Panel", cantidad=2.0, unidad_medida="Unidad"),
        RepuestoUtilizado(ot_id=ot5.id, nombre_item="Kit Filtros y Lubricante 15W40 Cummins", cantidad=1.0, unidad_medida="Kit"),
        RepuestoUtilizado(ot_id=ot6.id, nombre_item="Gas Refrigerante R410A (Carga compensatoria)", cantidad=1.0, unidad_medida="Kg"),
        RepuestoUtilizado(ot_id=ot6.id, nombre_item="Filtro de aire sintético lavable AA", cantidad=2.0, unidad_medida="Unidad"),
        RepuestoUtilizado(ot_id=ot7.id, nombre_item="Malla eslabonada galvanizada Cal. 10", cantidad=18.5, unidad_medida="Metro"),
        RepuestoUtilizado(ot_id=ot7.id, nombre_item="Concreto premezclado 3000 PSI", cantidad=2.4, unidad_medida="M3"),
        RepuestoUtilizado(ot_id=ot7.id, nombre_item="Cable cobre desnudo 2/0 AWG para LPS", cantidad=32.0, unidad_medida="Metro"),
        RepuestoUtilizado(ot_id=ot8.id, nombre_item="Grasa dieléctrica sellante para bornes", cantidad=1.0, unidad_medida="Tubo")
    ]
    db.add_all(repuestos)

    # 6. Avances de Bitácora PDT
    print(f"[{db_name}] 5. Creando bitácora cronológica de avances en campo (PDT)...")
    avances = [
        # OT 1: Correctivo
        Avance(ot_id=ot1.id, user_id=carlos.id, descripcion="Llegada a estación base Apartadó. Inspección preoperacional y charla SST de 5 minutos.", porcentaje=10, fecha_reporte=f_inicio_1 + timedelta(hours=1)),
        Avance(ot_id=ot1.id, user_id=carlos.id, descripcion="Desmonte de bomba de agua averiada y limpieza de acople del motor.", porcentaje=30, fecha_reporte=f_inicio_1 + timedelta(hours=2)),
        Avance(ot_id=ot1.id, user_id=carlos.id, descripcion="Montaje de bomba nueva y pruebas con carga. Ciclo normal validado con SO Claro.", porcentaje=50, fecha_reporte=f_inicio_1 + timedelta(hours=3)),

        # OT 2: Emergencia
        Avance(ot_id=ot2.id, user_id=jasmin.id, descripcion="Activación de cuadrilla de emergencia y desplazamiento fluvial por Río San Juan.", porcentaje=15, fecha_reporte=f_inicio_2 + timedelta(hours=1)),
        Avance(ot_id=ot2.id, user_id=jasmin.id, descripcion="Llegada a Cantón de San Pablo y aislamiento preventivo del banco de baterías afectado.", porcentaje=25, fecha_reporte=f_inicio_2 + timedelta(hours=3)),

        # OT 3: Preventivo Planta
        Avance(ot_id=ot3.id, user_id=eliseo.id, descripcion="Llegada a RPT Bahía Solano tras desplazamiento fluvial. Apertura de caseta y toma de datos iniciales.", porcentaje=20, fecha_reporte=f_inicio_3 + timedelta(hours=1)),
        Avance(ot_id=ot3.id, user_id=eliseo.id, descripcion="Drenaje de aceite usado y sustitución de filtros de aceite y combustible.", porcentaje=60, fecha_reporte=f_inicio_3 + timedelta(hours=3)),
        Avance(ot_id=ot3.id, user_id=eliseo.id, descripcion="Prueba de encendido y simulación de corte de energía durante 15 minutos en carga con ATS. Parámetros conformes.", porcentaje=100, fecha_reporte=f_inicio_3 + timedelta(hours=6)),

        # OT 4: Preventivo Aire
        Avance(ot_id=ot4.id, user_id=carlos.id, descripcion="Llegada a estación base Montería. Inicio de lavado de condensadora exterior con hidrolavadora.", porcentaje=30, fecha_reporte=f_inicio_4 + timedelta(hours=1)),
        Avance(ot_id=ot4.id, user_id=carlos.id, descripcion="Limpieza de serpentín evaporador, lavado de filtros y medición de presiones R410A.", porcentaje=65, fecha_reporte=f_inicio_4 + timedelta(hours=2)),

        # OT 5: Rutina 7x24 Planta
        Avance(ot_id=ot5.id, user_id=luis.id, descripcion="Ejecución de rutina decenal 7x24 en planta eléctrica. Verificación de niveles y simulación de falla red.", porcentaje=60, fecha_reporte=f_inicio_5 + timedelta(hours=2)),
        Avance(ot_id=ot5.id, user_id=luis.id, descripcion="Cierre y confirmación de planta en modo automático sin alarmas ante el NOC.", porcentaje=100, fecha_reporte=f_inicio_5 + timedelta(hours=4)),

        # OT 6: Rutina 7x24 Aire
        Avance(ot_id=ot6.id, user_id=carlos.id, descripcion="Llegada a estación base Turbo. Verificación de consigna de termostato shelter y presiones.", porcentaje=40, fecha_reporte=f_inicio_6 + timedelta(hours=1)),
        Avance(ot_id=ot6.id, user_id=carlos.id, descripcion="Limpieza de filtros y verificación de alternancia automática entre unidades de climatización.", porcentaje=75, fecha_reporte=f_inicio_6 + timedelta(hours=2)),

        # OT 7: Obra Civil
        Avance(ot_id=ot7.id, user_id=carlos.id, descripcion="Llegada a ANT.Zungo-2 con camión de carga. Replanteo topográfico y excavación para losa de motogenerador.", porcentaje=30, fecha_reporte=f_inicio_7 + timedelta(hours=1)),
        Avance(ot_id=ot7.id, user_id=carlos.id, descripcion="Armado de formaleta, parrilla de acero e instalación de malla perimetral calibre 10.", porcentaje=70, fecha_reporte=f_inicio_7 + timedelta(hours=3)),

        # OT 8: Relevamiento 360
        Avance(ot_id=ot8.id, user_id=carlos.id, descripcion="Llegada a estación Titiribí. Inicio de relevamiento e inspección visual de los 6 subsistemas GE.", porcentaje=25, fecha_reporte=f_inicio_8 + timedelta(hours=1)),
        Avance(ot_id=ot8.id, user_id=carlos.id, descripcion="Pruebas de aislamiento Megger a 1000Vdc y mediciones de resistencia SPT con telurómetro.", porcentaje=60, fecha_reporte=f_inicio_8 + timedelta(hours=2)),
        Avance(ot_id=ot8.id, user_id=carlos.id, descripcion="Conexión de banco resistivo y prueba de carga al 80% durante 60 minutos con lecturas cada 15 min.", porcentaje=85, fecha_reporte=f_inicio_8 + timedelta(hours=4))
    ]
    db.add_all(avances)

    # 7. Sub-actividades de checklist
    print(f"[{db_name}] 6. Creando subactividades operativas del checklist...")
    actividades = [
        # OT 1: Correctivo
        ActividadOt(ot_id=ot1.id, nombre="Desmonte de bomba averiada y limpieza de acople", peso_porcentaje=30, progreso=30, estado="completada"),
        ActividadOt(ot_id=ot1.id, nombre="Instalación de nueva bomba y purga de refrigerante", peso_porcentaje=40, progreso=20, estado="pendiente"),
        ActividadOt(ot_id=ot1.id, nombre="Pruebas con carga y validación con supervisor Claro", peso_porcentaje=30, progreso=0, estado="pendiente"),

        # OT 2: Emergencia
        ActividadOt(ot_id=ot2.id, nombre="Desplazamiento y aislamiento del sistema en falla", peso_porcentaje=40, progreso=25, estado="pendiente"),
        ActividadOt(ot_id=ot2.id, nombre="Sustitución de celda sulfatada y ponchado de cables", peso_porcentaje=35, progreso=0, estado="pendiente"),
        ActividadOt(ot_id=ot2.id, nombre="Reactivación de rectificador DC y pruebas de carga", peso_porcentaje=25, progreso=0, estado="pendiente"),

        # OT 3: Preventivo Planta
        ActividadOt(ot_id=ot3.id, nombre="Inspección visual de planta y niveles de fluidos", peso_porcentaje=25, progreso=25, estado="completada"),
        ActividadOt(ot_id=ot3.id, nombre="Cambio de filtros y lubricante de motor 15W40", peso_porcentaje=35, progreso=35, estado="completada"),
        ActividadOt(ot_id=ot3.id, nombre="Prueba 15 min soportando carga simulando falla", peso_porcentaje=40, progreso=40, estado="completada"),

        # OT 4: Preventivo Aire
        ActividadOt(ot_id=ot4.id, nombre="Lavado profundo de serpentines y filtros de aire", peso_porcentaje=35, progreso=35, estado="completada"),
        ActividadOt(ot_id=ot4.id, nombre="Medición de presiones frigoríficas y corriente eléctrica", peso_porcentaje=35, progreso=30, estado="completada"),
        ActividadOt(ot_id=ot4.id, nombre="Prueba de salto térmico y drenajes de condensado", peso_porcentaje=30, progreso=0, estado="pendiente"),

        # OT 5: Rutina 7x24 Planta
        ActividadOt(ot_id=ot5.id, nombre="Revisión de parámetros estáticos de planta y batería", peso_porcentaje=40, progreso=40, estado="completada"),
        ActividadOt(ot_id=ot5.id, nombre="Prueba de transferencia automática ATS en carga", peso_porcentaje=60, progreso=60, estado="completada"),

        # OT 6: Rutina 7x24 Aire
        ActividadOt(ot_id=ot6.id, nombre="Verificación de temperatura ambiente y termostato", peso_porcentaje=40, progreso=40, estado="completada"),
        ActividadOt(ot_id=ot6.id, nombre="Inspección de alternancia automática de unidades AA", peso_porcentaje=60, progreso=35, estado="completada"),

        # OT 7: Obra Civil
        ActividadOt(ot_id=ot7.id, nombre="Excavación y armado de losa reforzada 3000 PSI", peso_porcentaje=40, progreso=40, estado="completada"),
        ActividadOt(ot_id=ot7.id, nombre="Instalación de cerramiento en malla eslabonada con concertina", peso_porcentaje=35, progreso=30, estado="completada"),
        ActividadOt(ot_id=ot7.id, nombre="Instalación de bajante LPS y retiro de escombros", peso_porcentaje=25, progreso=0, estado="pendiente"),

        # OT 8: Relevamiento 360
        ActividadOt(ot_id=ot8.id, nombre="Diagnóstico visual y funcional de los 6 subsistemas GE", peso_porcentaje=25, progreso=25, estado="completada"),
        ActividadOt(ot_id=ot8.id, nombre="Ensayo de aislamiento dieléctrico Megger 1000V", peso_porcentaje=25, progreso=25, estado="completada"),
        ActividadOt(ot_id=ot8.id, nombre="Prueba con Banco de Carga Resistivo al 80% (60 min)", peso_porcentaje=30, progreso=30, estado="completada"),
        ActividadOt(ot_id=ot8.id, nombre="Medición de resistividad y equipotencialidad SPT", peso_porcentaje=20, progreso=5, estado="pendiente")
    ]
    db.add_all(actividades)

    db.commit()
    print(f"[SUCCESS] {db_name}: 8 Órdenes de Trabajo tipificadas y sembradas con éxito (1 de cada tipo de trabajo).")

def main():
    print("=" * 80)
    print("  DOBLEX S.A.S. - LIMPIEZA DE BD Y GENERACIÓN DE EJEMPLO POR TIPO DE TRABAJO")
    print("=" * 80)

    # 1. Base de datos configurada (SQLite local)
    from app.db.session import SessionLocal as SQLiteSession
    sqlite_db = SQLiteSession()
    try:
        seed_ots_for_session(sqlite_db, "SQLite (doblex.db)")
    except Exception as e:
        print(f"[ERROR SQLite]: {e}")
        sqlite_db.rollback()
    finally:
        sqlite_db.close()

    # 2. Base de datos PostgreSQL en Docker si está disponible
    postgres_url = "postgresql://doblex_user:doblex_password@localhost:5432/doblex_smu"
    try:
        pg_engine = create_engine(postgres_url, echo=False)
        PgSession = sessionmaker(autocommit=False, autoflush=False, bind=pg_engine)
        pg_db = PgSession()
        seed_ots_for_session(pg_db, "PostgreSQL (doblex_postgres_db)")
        pg_db.close()
    except Exception as e:
        print(f"[INFO] PostgreSQL Docker no activo o no configurado ({e}). Se ha limpiado y sembrado SQLite local.")

    print("\n" + "=" * 80)
    print("  PROCESO DE LIMPIEZA Y RE-SEEDING FINALIZADO EXITOSAMENTE (8 TIPOS DE TRABAJO)")
    print("=" * 80)

if __name__ == "__main__":
    main()

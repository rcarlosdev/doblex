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

def seed_ots_for_session(db, db_name="SQLite"):
    print(f"\n[{db_name}] 1. Limpiando tablas de Órdenes de Trabajo...")
    
    # 1. Eliminar datos existentes de OTs y sus tablas hijas en orden de FK
    deleted_evidencias = db.query(EvidenciaFotografica).delete()
    deleted_repuestos = db.query(RepuestoUtilizado).delete()
    deleted_avances = db.query(Avance).delete()
    deleted_actividades = db.query(ActividadOt).delete()
    deleted_ots = db.query(Ot).delete()
    db.commit()
    
    print(f"[{db_name}] Tablas limpiadas: {deleted_ots} OTs, {deleted_actividades} actividades, {deleted_avances} avances, {deleted_evidencias} evidencias, {deleted_repuestos} repuestos eliminados.")
    print(f"[{db_name}] Preservados: {db.query(User).count()} usuarios, {db.query(Cuadrilla).count()} cuadrillas, {db.query(Empleado).count()} empleados, {db.query(Sitio).count()} sitios.")

    # 2. Obtener usuarios y cuadrillas
    admin = db.query(User).filter(User.username == "admin.doblex").first()
    adminis = db.query(User).filter(User.username == "auxiliar.doblex").first() or admin
    carlos = db.query(User).filter(User.username == "carlos.doblex").first() or admin
    jasmin = db.query(User).filter(User.username == "jasmin.doblex").first() or carlos
    eliseo = db.query(User).filter(User.username == "eliseo.doblex").first() or carlos
    luis = db.query(User).filter(User.username == "luis.doblex").first() or carlos

    cuadrilla_ant = db.query(Cuadrilla).filter(Cuadrilla.nombre.ilike("%Antioquia%")).first()
    cuadrilla_cho = db.query(Cuadrilla).filter(Cuadrilla.nombre.ilike("%Chocó%")).first() or cuadrilla_ant
    cuadrilla_cor = db.query(Cuadrilla).filter(Cuadrilla.nombre.ilike("%Córdoba%")).first() or cuadrilla_ant
    cuadrilla_atl = db.query(Cuadrilla).filter(Cuadrilla.nombre.ilike("%Atlántico%")).first() or cuadrilla_ant

    # 3. Buscar Sitios Reales en la base de datos
    sitio_ant = db.query(Sitio).filter(Sitio.nombre == "ANT.APARTADO").first() or db.query(Sitio).filter(Sitio.nombre.ilike("%APARTADO%")).first()
    sitio_cho = db.query(Sitio).filter(Sitio.nombre == "CHO.CANTON DE SAN PABLO").first() or db.query(Sitio).filter(Sitio.nombre.ilike("%CANTON%")).first()
    sitio_mon = db.query(Sitio).filter(Sitio.nombre == "MON.MONTERIA").first() or db.query(Sitio).filter(Sitio.nombre.ilike("%MONTERIA%")).first()
    sitio_bahia = db.query(Sitio).filter(Sitio.nombre.ilike("%BAHIA SOLANO%")).first()
    sitio_titi = db.query(Sitio).filter(Sitio.nombre == "ANT.TITIRIBI").first() or db.query(Sitio).filter(Sitio.nombre.ilike("%TITIRIBI%")).first()

    # 4. Crear las 5 OTs basadas en las plantillas oficiales WO y MP
    print(f"[{db_name}] 2. Sembrando OTs con estructura oficial de campo...")

    # OT 1: Correctivo - Exacto a 'WO0000005558781 MC MON.CENTRO.xlsx'
    ot1_form = {
        "presenta_afectacion": "No",
        "tipo_equipo_falla": "Planta eléctrica",
        "marca_equipo": "Selmec",
        "modelo_equipo": "Selmec 40SC",
        "reparacion": True,
        "reinstalacion": False,
        "cambio_equipo": False,
        "descripcion_falla": "Falla en sistema de enfriamiento del grupo electrógeno con fuga de refrigerante por bomba de agua y alarma de alta temperatura en tablero.",
        "descripcion_solucion": "Se realiza instalación de bomba de agua y se suministran 2 galones de refrigerante. Se realizan pruebas al grupo electrógeno en automático y con carga, el cual realiza el ciclo normalmente. Pruebas avaladas con SO Julio Ruiz.",
        "repuesto_retirado": {
            "descripcion": "Bomba de agua Selmec 40SC averiada",
            "marca": "Selmec / Perkins",
            "modelo": "40SC-WP",
            "serial": "SN-PUMP-40SC-092"
        },
        "repuesto_instalado": {
            "descripcion": "Bomba de agua original nueva",
            "marca": "Selmec / Perkins",
            "modelo": "40SC-WP-NEW",
            "serial": "SN-PUMP-40SC-991"
        },
        "materiales": [
            {"descripcion": "Refrigerante 50/50 LPU Claro", "unidad": "Galón", "cantidad": 2},
            {"descripcion": "Empaque sellador termostato", "unidad": "Unidad", "cantidad": 1}
        ],
        "desea_transporte_especial": "Si",
        "tipo_transporte": "Vehículo 4x4",
        "distancia_km": 42.5,
        "tiempo_desplazamiento": "1h 45min",
        "observacion_transporte": "Acceso por trocha terciaria no pavimentada.",
        "se_encontraron_novedades": "Si",
        "sistema_novedad": "Cerramiento y Balizamiento",
        "prioridad_novedad": "Media",
        "descripcion_novedad": "Malla eslabonada perimetral presenta rotura en costado norte.",
        "resuelto_en_visita": "No",
        "falla_resuelta": "Si",
        "observaciones_actividad": "PE queda en modo automático y sin alarmas. Nivel de refrigerante óptimo.",
        "nombre_supervisor": "Cleyver Espitia"
    }

    ot1 = Ot(
        codigo="OT-2026-101",
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
        site_owner="CLARO",
        coordinador="Ing. Carlos Pérez",
        created_by=admin.id,
        user_id=carlos.id,
        cuadrilla_id=cuadrilla_ant.id if cuadrilla_ant else None,
        prioridad="P1",
        tipo_ubicacion="urbana",
        subsistema="Planta eléctrica",
        progreso=25,
        estado="asignada",
        fecha_inicio=now_utc() - timedelta(days=2),
        fecha_limite_sla=now_utc() + timedelta(days=1),
        datos_formulario=json.dumps(ot1_form, ensure_ascii=False)
    )

    # OT 2: Emergencia - Estructura WO de Emergencia Chocó
    ot2_form = {
        "presenta_afectacion": "Si",
        "tipo_equipo_falla": "Banco de Baterías",
        "marca_equipo": "Narada / Huawei",
        "modelo_equipo": "48V 500Ah",
        "reparacion": False,
        "reinstalacion": False,
        "cambio_equipo": True,
        "descripcion_falla": "Descarga atmosférica severa averió módulo de protección SPD e incendió dos celdas del banco de baterías 48V de repetidora.",
        "descripcion_solucion": "Desconexión de celdas dañadas, instalación de banco temporal de respaldo y reactivación de rectificador de fuerza DC.",
        "repuesto_retirado": {
            "descripcion": "Celda de batería 2V 500Ah sulfatada",
            "marca": "Narada",
            "modelo": "2V-500AH",
            "serial": "SN-BAT-08812"
        },
        "repuesto_instalado": {
            "descripcion": "Celda de batería 2V 500Ah reemplazo",
            "marca": "Narada",
            "modelo": "2V-500AH",
            "serial": "SN-BAT-99411"
        },
        "materiales": [
            {"descripcion": "Cable de fuerza 2 AWG flexible", "unidad": "Metro", "cantidad": 6},
            {"descripcion": "Terminal de compresión 2 AWG 1/4", "unidad": "Unidad", "cantidad": 4}
        ],
        "desea_transporte_especial": "Si",
        "tipo_transporte": "Lancha Fluvial",
        "distancia_km": 68.0,
        "tiempo_desplazamiento": "3h 30min",
        "observacion_transporte": "Transporte fluvial por el Río San Juan.",
        "se_encontraron_novedades": "No",
        "falla_resuelta": "Si",
        "observaciones_actividad": "Estación queda transmitiendo en 54.2 VDC sin caída de tráfico.",
        "nombre_supervisor": "Ing. Carlos Hinestroza"
    }

    ot2 = Ot(
        codigo="OT-2026-102",
        id_actividad="ACT-2026-099014",
        tipo_actividad="emergencia",
        tipo_mantenimiento="emergencia",
        descripcion="Mantenimiento de Emergencia Híbrido SFV & Power DC - Falla en Inversor y Banco de Baterías de Repetidora ZNI",
        sitio=sitio_cho.nombre if sitio_cho else "CHO.CANTON DE SAN PABLO",
        sitio_id=sitio_cho.id if sitio_cho else None,
        ubicacion=f"{sitio_cho.municipio or 'Cantón de San Pablo'}, Chocó" if sitio_cho else "Sector Río San Juan, Cantón de San Pablo, Chocó",
        departamento="Chocó",
        regional="R2",
        categoria="rural",
        tipo_estacion="REPETIDORA",
        site_owner="CLARO",
        coordinador="Ing. Alexander Gómez",
        created_by=adminis.id,
        user_id=jasmin.id,
        cuadrilla_id=cuadrilla_cho.id if cuadrilla_cho else None,
        prioridad="P1",
        tipo_ubicacion="rural",
        subsistema="Móvil Híbridos SFV",
        progreso=35,
        estado="en_camino",
        fecha_inicio=now_utc() - timedelta(hours=14),
        fecha_limite_sla=now_utc() + timedelta(hours=10),
        datos_formulario=json.dumps(ot2_form, ensure_ascii=False)
    )

    # OT 3: Preventivo Aire Acondicionado - Montería
    ot3_form = {
        "marca_equipo": "ComfortStar",
        "modelo_equipo": "CP-24K-INV",
        "serial_equipo": "CS-98412-2024",
        "capacidad_btu": 24000,
        "tipo_refrigerante": "R410A",
        "presion_baja_psi": 120,
        "presion_alta_psi": 350,
        "corriente_compresor_amp": 9.8,
        "voltaje_alimentacion_aa": 220,
        "temperatura_inyeccion_c": 13.5,
        "temperatura_retorno_c": 23.0,
        "limpieza_evaporador": "Si",
        "limpieza_condensador": "Si",
        "cambio_lavado_filtros": "Si",
        "desague_drenaje_ok": "Si",
        "responsable_tec_1": "Carlos Rafael Lozano",
        "responsable_tec_2": "Ancízar Manuel Pérez",
        "observaciones_preventivo": "Mantenimiento preventivo general a equipo de climatización. Serpentines desincrustados con hidrolavadora, presiones en rango óptimo."
    }

    ot3 = Ot(
        codigo="OT-2026-103",
        id_actividad="ACT-2026-030401",
        tipo_actividad="preventivo_aire",
        tipo_mantenimiento="preventivo",
        descripcion="Mantenimiento Preventivo & Climatización AA Móvil - Servicio a Compresores y Condensadoras de Shelter de Transmisión",
        sitio=sitio_mon.nombre if sitio_mon else "MON.MONTERIA",
        sitio_id=sitio_mon.id if sitio_mon else None,
        ubicacion=f"{sitio_mon.municipio or 'Montería'}, Córdoba" if sitio_mon else "Calle 27 # 4-50, Centro, Montería, Córdoba",
        departamento="Córdoba",
        regional="R1",
        categoria="normal",
        tipo_estacion="MOVIL",
        site_owner="CLARO",
        coordinador="Ing. Sandra Morales",
        created_by=adminis.id,
        user_id=carlos.id,
        cuadrilla_id=cuadrilla_cor.id if cuadrilla_cor else None,
        prioridad="P2",
        tipo_ubicacion="urbana",
        subsistema="Movil Aires Acondicionados",
        progreso=65,
        estado="en_sitio",
        fecha_inicio=now_utc() - timedelta(days=1),
        fecha_limite_sla=now_utc() + timedelta(days=1),
        fecha_llegada_sitio=now_utc() - timedelta(hours=3),
        datos_formulario=json.dumps(ot3_form, ensure_ascii=False)
    )

    # OT 4: Preventivo Planta Eléctrica - Exacto a 'OT5304019_MP_CHO.RPT BAHIA SOLANO.xlsx'
    ot4_form = {
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
        "galones_aceite_suministrados": 3.5,
        "nivel_refrigerante": "Normal",
        "fugas_lubricacion": "Sin Fugas",
        "presion_aceite_psi": 52,
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
        # Responsables
        "responsable_tec_1": "Carlos Lozano",
        "responsable_tec_2": "Jasmin Ariel Mosquera",
        "observaciones_preventivo": "Mantenimiento preventivo integral según formato RPT Bahía Solano. Prueba de encendido de planta durante 15 minutos soportando carga real sin novedades."
    }

    ot4 = Ot(
        codigo="OT-2026-104",
        id_actividad="ACT-2026-5304019",
        tipo_actividad="preventivo_planta",
        tipo_mantenimiento="preventivo",
        descripcion="Mantenimiento Preventivo Planta Eléctrica AGG Power - Rutina de Encendido, Medición en Carga y Pruebas ATS (Ref. RPT Bahía Solano)",
        sitio=sitio_bahia.nombre if sitio_bahia else "CHO.RPT.BAHIA SOLANO",
        sitio_id=sitio_bahia.id if sitio_bahia else None,
        ubicacion=f"{sitio_bahia.municipio or 'Bahía Solano'}, Chocó" if sitio_bahia else "Bahía Solano, Chocó",
        departamento="Chocó",
        regional="R2",
        categoria="rural",
        tipo_estacion="REPETIDORA",
        site_owner="CLARO",
        coordinador="Ing. Alexander Gómez",
        created_by=admin.id,
        user_id=eliseo.id,
        cuadrilla_id=cuadrilla_atl.id if cuadrilla_atl else None,
        prioridad="P3",
        tipo_ubicacion="rural",
        subsistema="Movil Plantas Eléctricas",
        progreso=100,
        estado="solucionada",
        fecha_inicio=now_utc() - timedelta(days=4),
        fecha_limite_sla=now_utc() - timedelta(days=2),
        fecha_llegada_sitio=now_utc() - timedelta(days=4, hours=-2),
        fecha_solucion=now_utc() - timedelta(days=4, hours=-7),
        causa_falla="desgaste",
        observaciones_cierre="Rutina de mantenimiento preventivo de grupo electrógeno completada al 100%. Parámetros eléctricos en carga estables a 220V 60Hz. Planta queda en automático.",
        datos_formulario=json.dumps(ot4_form, ensure_ascii=False)
    )

    # OT 5: Preventivo Planta Eléctrica - Titiribí
    ot5_form = {
        "marca_equipo": "Caterpillar Olympian",
        "modelo_equipo": "GEP33-3",
        "serial_equipo": "OLY-88710",
        "horometro_inicial": 4120.5,
        "frecuencia_hz": 60,
        "capacidad_kva": 30,
        "marca_motor": "Perkins",
        "modelo_motor": "1104A-44G1",
        "serial_motor": "PK998124",
        "marca_generador": "Leroy Somer",
        "modelo_generador": "LL1514P",
        "serial_generador": "LS-55410",
        "voltaje_bateria": 26.0,
        "capacidad_bateria": 1200,
        "tipo_bateria": "Libre de Mantenimiento",
        "filtro_aceite_cambiado": "Realizado",
        "filtro_combustible_cambiado": "Realizado",
        "filtro_aire_estado": "Cambiado Nuevo",
        "cambio_aceite_motor": "Realizado (15W40)",
        "galones_aceite_suministrados": 4.0,
        "nivel_refrigerante": "Normal",
        "fugas_lubricacion": "Sin Fugas",
        "presion_aceite_psi": 55,
        "temperatura_motor_c": 76,
        "tamano_tanque_galones": 55,
        "nivel_combustible_porcentaje": 95,
        "estado_alarma_nivel": "Normal",
        "trampa_agua_drenada": "Si",
        "lineas_combustible_estado": "Conforme Sin Fugas",
        "prueba_ats_15min": "Exitosa con Carga",
        "horometro_final_prueba": 4120.8,
        "tiempo_transferencia_seg": 6,
        "voltaje_l1_l2": 220,
        "voltaje_l2_l3": 220,
        "voltaje_l1_l3": 220,
        "frecuencia_operacion_hz": 60,
        "planta_en_automatico": "Si",
        "presenta_alarmas": "No",
        "responsable_tec_1": "Julián Alexander Rivillas",
        "responsable_tec_2": "Manuel Francisco Tapias",
        "observaciones_preventivo": "Mantenimiento preventivo integral de planta eléctrica y transferencia ATS. Ajuste de pernería y limpieza de caseta."
    }

    ot5 = Ot(
        codigo="OT-2026-105",
        id_actividad="ACT-2026-078192",
        tipo_actividad="preventivo_planta",
        tipo_mantenimiento="preventivo",
        descripcion="Mantenimiento Preventivo Integral de Planta Eléctrica Caterpillar Olympian y Enlace de Transmisión",
        sitio=sitio_titi.nombre if sitio_titi else "ANT.TITIRIBI",
        sitio_id=sitio_titi.id if sitio_titi else None,
        ubicacion=f"{sitio_titi.municipio or 'Titiribí'}, Antioquia" if sitio_titi else "Vereda La Albania, Titiribí, Antioquia",
        departamento="Antioquia",
        regional="R1",
        categoria="rural",
        tipo_estacion="MOVIL",
        site_owner="CLARO",
        coordinador="Ing. Carlos Pérez",
        created_by=admin.id,
        user_id=luis.id,
        cuadrilla_id=cuadrilla_ant.id if cuadrilla_ant else None,
        prioridad="P2",
        tipo_ubicacion="rural",
        subsistema="Movil Plantas Eléctricas",
        progreso=100,
        estado="finalizada",
        fecha_inicio=now_utc() - timedelta(days=6),
        fecha_limite_sla=now_utc() - timedelta(days=4),
        fecha_llegada_sitio=now_utc() - timedelta(days=6, hours=-2),
        fecha_solucion=now_utc() - timedelta(days=6, hours=-8),
        causa_falla="desgaste",
        observaciones_cierre="Mantenimiento preventivo preventivo de grupo electrógeno con cambio de filtros, aceite y alineación de enlace.",
        datos_formulario=json.dumps(ot5_form, ensure_ascii=False)
    )

    db.add_all([ot1, ot2, ot3, ot4, ot5])
    db.commit()

    # 5. Evidencias Fotográficas
    print(f"[{db_name}] 3. Creando evidencias fotográficas georreferenciadas...")
    evidencias = [
        EvidenciaFotografica(
            ot_id=ot1.id,
            tipo="antes",
            url_imagen="https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800",
            latitud=7.8829,
            longitud=-76.6256,
            fecha_hora_captura=now_utc() - timedelta(days=2, hours=-1)
        ),
        EvidenciaFotografica(
            ot_id=ot4.id,
            tipo="antes",
            url_imagen="https://images.unsplash.com/photo-1541888946425-d0fbb186f5f8?w=800",
            latitud=6.2269,
            longitud=-77.4044,
            fecha_hora_captura=now_utc() - timedelta(days=4, hours=-1)
        ),
        EvidenciaFotografica(
            ot_id=ot4.id,
            tipo="durante",
            url_imagen="https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800",
            latitud=6.2270,
            longitud=-77.4045,
            fecha_hora_captura=now_utc() - timedelta(days=4, hours=-3)
        ),
        EvidenciaFotografica(
            ot_id=ot4.id,
            tipo="despues",
            url_imagen="https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800",
            latitud=6.2269,
            longitud=-77.4044,
            fecha_hora_captura=now_utc() - timedelta(days=4, hours=-6)
        ),
    ]
    db.add_all(evidencias)

    # 6. Repuestos e Insumos LPU
    print(f"[{db_name}] 4. Creando insumos y repuestos LPU vinculados...")
    repuestos = [
        RepuestoUtilizado(ot_id=ot1.id, nombre_item="Bomba de agua Selmec Perkins 40SC", cantidad=1.0, unidad_medida="Unidad"),
        RepuestoUtilizado(ot_id=ot1.id, nombre_item="Refrigerante Anticongelante 50/50", cantidad=2.0, unidad_medida="Galón"),
        RepuestoUtilizado(ot_id=ot4.id, nombre_item="Filtro de Aceite LF16015 Fleetguard", cantidad=1.0, unidad_medida="Unidad"),
        RepuestoUtilizado(ot_id=ot4.id, nombre_item="Filtro Separador Combustible FS1242", cantidad=1.0, unidad_medida="Unidad"),
        RepuestoUtilizado(ot_id=ot4.id, nombre_item="Aceite Lubricante 15W40 CI-4", cantidad=3.5, unidad_medida="Galón"),
        RepuestoUtilizado(ot_id=ot3.id, nombre_item="Gas Refrigerante Ecológico R410A", cantidad=3.0, unidad_medida="Kg"),
        RepuestoUtilizado(ot_id=ot3.id, nombre_item="Filtro de Aire Lavable Tipo Panel", cantidad=2.0, unidad_medida="Unidad"),
    ]
    db.add_all(repuestos)

    # 7. Avances de Bitácora PDT
    print(f"[{db_name}] 5. Creando bitácora de avances en campo (PDT)...")
    avances = [
        Avance(ot_id=ot1.id, user_id=carlos.id, descripcion="Llegada a estación base. Inspección preoperacional y charla SST de 5 minutos.", porcentaje=10, fecha_reporte=now_utc() - timedelta(days=2, hours=-1)),
        Avance(ot_id=ot1.id, user_id=carlos.id, descripcion="Desmonte de bomba de agua dañada con fuga en el sello mecánico.", porcentaje=25, fecha_reporte=now_utc() - timedelta(days=2, hours=-2)),
        Avance(ot_id=ot4.id, user_id=eliseo.id, descripcion="Llegada a RPT Bahía Solano tras desplazamiento en lancha. Apertura de caseta de planta eléctrica.", porcentaje=20, fecha_reporte=now_utc() - timedelta(days=4, hours=-1)),
        Avance(ot_id=ot4.id, user_id=eliseo.id, descripcion="Drenaje de aceite usado y sustitución de filtros de aceite y combustible.", porcentaje=60, fecha_reporte=now_utc() - timedelta(days=4, hours=-3)),
        Avance(ot_id=ot4.id, user_id=eliseo.id, descripcion="Prueba de encendido y simulación de corte de energía durante 15 minutos en carga con ATS. Parámetros conformes.", porcentaje=100, fecha_reporte=now_utc() - timedelta(days=4, hours=-6)),
        Avance(ot_id=ot3.id, user_id=carlos.id, descripcion="Llegada a estación base Montería. Inicio de lavado de condensadora exterior.", porcentaje=30, fecha_reporte=now_utc() - timedelta(hours=3)),
        Avance(ot_id=ot3.id, user_id=carlos.id, descripcion="Limpieza de serpentín evaporador y medición de presiones manométricas R410A.", porcentaje=65, fecha_reporte=now_utc() - timedelta(hours=1)),
    ]
    db.add_all(avances)

    # 8. Sub-actividades de checklist
    actividades = [
        ActividadOt(ot_id=ot1.id, nombre="Desmonte de bomba averiada y limpieza de acople", peso_porcentaje=30, progreso=30, estado="completada"),
        ActividadOt(ot_id=ot1.id, nombre="Instalación de nueva bomba y purga de refrigerante", peso_porcentaje=40, progreso=0, estado="pendiente"),
        ActividadOt(ot_id=ot1.id, nombre="Pruebas con carga y validación con SO Julio Ruiz", peso_porcentaje=30, progreso=0, estado="pendiente"),
        ActividadOt(ot_id=ot4.id, nombre="Inspección visual de planta y niveles de fluidos", peso_porcentaje=25, progreso=25, estado="completada"),
        ActividadOt(ot_id=ot4.id, nombre="Cambio de filtros y lubricante de motor", peso_porcentaje=35, progreso=35, estado="completada"),
        ActividadOt(ot_id=ot4.id, nombre="Prueba 15 min soportando carga simulando falla", peso_porcentaje=40, progreso=40, estado="completada"),
    ]
    db.add_all(actividades)

    db.commit()
    print(f"[SUCCESS] {db_name}: 5 Órdenes de Trabajo sincronizadas y sembradas con éxito.")

def main():
    print("=" * 70)
    print("  DOBLEX S.A.S. - LIMPIEZA Y RE-SIEMBRA OFICIAL DE OTs (WO & MP)")
    print("=" * 70)

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
        print("\nConexión a PostgreSQL en Docker exitosa...")
        seed_ots_for_session(pg_db, "PostgreSQL (doblex_postgres_db)")
        pg_db.close()
    except Exception as e:
        print(f"[INFO] PostgreSQL Docker no configurado o inaccesible: {e}")

    print("\n" + "=" * 70)
    print("  PROCESO DE LIMPIEZA Y RE-SEEDING DE OTS COMPLETADO")
    print("=" * 70)

if __name__ == "__main__":
    main()

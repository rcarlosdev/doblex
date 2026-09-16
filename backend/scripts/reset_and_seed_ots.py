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
    
    print(f"[{db_name}] Tablas limpiadas: {deleted_ots} OTs, {deleted_actividades} actividades, {deleted_avances} avances, {deleted_evidencias} evidencias, {deleted_repuestos} repuestos eliminados.")
    print(f"[{db_name}] Base preservada: {db.query(User).count()} usuarios, {db.query(Cuadrilla).count()} cuadrillas, {db.query(Empleado).count()} empleados, {db.query(Sitio).count()} sitios.")

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

    # 3. Buscar Sitios Reales en la base de datos de 1,819 estaciones
    sitio_ant = db.query(Sitio).filter(Sitio.nombre == "ANT.APARTADO").first() or db.query(Sitio).filter(Sitio.nombre.ilike("%APARTADO%")).first()
    sitio_cho = db.query(Sitio).filter(Sitio.nombre == "CHO.CANTON DE SAN PABLO").first() or db.query(Sitio).filter(Sitio.nombre.ilike("%CANTON%")).first()
    sitio_mon = db.query(Sitio).filter(Sitio.nombre == "MON.MONTERIA").first() or db.query(Sitio).filter(Sitio.nombre.ilike("%MONTERIA%")).first()
    sitio_bahia = db.query(Sitio).filter(Sitio.nombre.ilike("%BAHIA SOLANO%")).first()
    sitio_titi = db.query(Sitio).filter(Sitio.nombre.ilike("%TITIRIBI%")).first()
    sitio_pizarro = db.query(Sitio).filter(Sitio.nombre.ilike("%PIZARRO%")).first() or sitio_cho

    print(f"[{db_name}] 2. Sembrando OTs con estructura oficial de campo y formatos técnicos vigentes...")

    # =========================================================================
    # OT 1: Correctivo - Exacto a 'WO0000005558781 MC MON.CENTRO.xlsx'
    # =========================================================================
    ops_ot1 = [
        format_empleado_operador(emp_carlos),
        format_empleado_operador(emp_julian)
    ]
    ops_ot1 = [op for op in ops_ot1 if op]

    ot1_so = (sitio_ant.supervisor_operativo or sitio_ant.new_so or "CLEYVER ESPITIA") if sitio_ant else "CLEYVER ESPITIA"
    ot1_form = {
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
        "materiales": [
            {"descripcion": "Refrigerante 50/50 LPU Claro", "unidad": "Galón", "cantidad": 2},
            {"descripcion": "Empaque sellador termostato alta temperatura", "unidad": "Unidad", "cantidad": 1}
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
        "nombre_supervisor": ot1_so,
        "operadores_asignados": ops_ot1
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
        progreso=25,
        estado="asignada",
        fecha_inicio=f_inicio_1,
        fecha_limite_sla=sla_service.calcular_fecha_limite("P1", "urbana", f_inicio_1),
        datos_formulario=json.dumps(ot1_form, ensure_ascii=False)
    )

    # =========================================================================
    # OT 2: Emergencia - Estructura WO de Emergencia Chocó (Fuerza DC / Power)
    # =========================================================================
    ops_ot2 = [
        format_empleado_operador(emp_jasmin),
        format_empleado_operador(emp_lozano)
    ]
    ops_ot2 = [op for op in ops_ot2 if op]

    ot2_so = (sitio_cho.supervisor_operativo or sitio_cho.new_so or "CARLOS HINESTROZA") if sitio_cho else "CARLOS HINESTROZA"
    ot2_form = {
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
        "nombre_supervisor": ot2_so,
        "operadores_asignados": ops_ot2
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
        ubicacion=f"{sitio_cho.municipio or 'Cantón de San Pablo'}, Chocó" if sitio_cho else "Sector Río San Juan, Cantón de San Pablo, Chocó",
        departamento="Chocó",
        regional="R2",
        categoria="rural",
        tipo_estacion="REPETIDORA",
        site_owner=ot2_so,
        coordinador=emp_adminis.nombre if emp_adminis else "Auxiliar Técnico",
        created_by=adminis.id,
        user_id=jasmin.id,
        cuadrilla_id=cuadrilla_cho.id if cuadrilla_cho else None,
        prioridad="P1",
        tipo_ubicacion="rural",
        subsistema="PW - POWER",
        progreso=35,
        estado="en_camino",
        fecha_inicio=f_inicio_2,
        fecha_limite_sla=sla_service.calcular_fecha_limite("P1", "rural", f_inicio_2),
        datos_formulario=json.dumps(ot2_form, ensure_ascii=False)
    )

    # =========================================================================
    # OT 3: Preventivo Aire Acondicionado - Montería
    # =========================================================================
    ops_ot3 = [
        format_empleado_operador(emp_ancizar),
        format_empleado_operador(emp_ramon)
    ]
    ops_ot3 = [op for op in ops_ot3 if op]

    ot3_so = (sitio_mon.supervisor_operativo or sitio_mon.new_so or "SANDRA MORALES") if sitio_mon else "SANDRA MORALES"
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
        "responsable_tec_1": emp_ancizar.nombre if emp_ancizar else "Ancízar Manuel Pérez",
        "responsable_tec_2": emp_ramon.nombre if emp_ramon else "Ramón Elías Yepes",
        "observaciones_preventivo": "Mantenimiento preventivo general a equipo de climatización. Serpentines desincrustados con hidrolavadora, presiones en rango óptimo.",
        "operadores_asignados": ops_ot3
    }

    f_inicio_3 = now_utc() - timedelta(days=1)
    ot3 = Ot(
        codigo="OT5304020",
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
        site_owner=ot3_so,
        coordinador=emp_adminis.nombre if emp_adminis else "Auxiliar Técnico",
        created_by=adminis.id,
        user_id=carlos.id,
        cuadrilla_id=cuadrilla_cor.id if cuadrilla_cor else None,
        prioridad="P2",
        tipo_ubicacion="urbana",
        subsistema="AA - AIRES ACONDICIONADOS",
        progreso=65,
        estado="en_sitio",
        fecha_inicio=f_inicio_3,
        fecha_limite_sla=sla_service.calcular_fecha_limite("P2", "urbana", f_inicio_3),
        fecha_llegada_sitio=now_utc() - timedelta(hours=3),
        datos_formulario=json.dumps(ot3_form, ensure_ascii=False)
    )

    # =========================================================================
    # OT 4: Preventivo Planta Eléctrica - Bahía Solano (Ref: OT5304019)
    # =========================================================================
    ops_ot4 = [
        format_empleado_operador(emp_eliseo),
        format_empleado_operador(emp_jasmin)
    ]
    ops_ot4 = [op for op in ops_ot4 if op]

    ot4_so = (sitio_bahia.supervisor_operativo or sitio_bahia.new_so or "ALEXANDER GÓMEZ") if sitio_bahia else "ALEXANDER GÓMEZ"
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
        "responsable_tec_1": emp_eliseo.nombre if emp_eliseo else "Eliseo Smith Granados",
        "responsable_tec_2": emp_jasmin.nombre if emp_jasmin else "Jasmin Ariel Mosquera",
        "observaciones_preventivo": "Mantenimiento preventivo integral según formato RPT Bahía Solano. Prueba de encendido de planta durante 15 minutos soportando carga real sin novedades.",
        "operadores_asignados": ops_ot4
    }

    f_inicio_4 = now_utc() - timedelta(days=4)
    ot4 = Ot(
        codigo="OT5304019",
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
        site_owner=ot4_so,
        coordinador=emp_admin.nombre if emp_admin else "Admin General",
        created_by=admin.id,
        user_id=eliseo.id,
        cuadrilla_id=cuadrilla_atl.id if cuadrilla_atl else None,
        prioridad="P3",
        tipo_ubicacion="rural",
        subsistema="PE - GRUPO ELECTROGENO",
        progreso=100,
        estado="solucionada",
        fecha_inicio=f_inicio_4,
        fecha_limite_sla=sla_service.calcular_fecha_limite("P3", "rural", f_inicio_4),
        fecha_llegada_sitio=now_utc() - timedelta(days=4, hours=-2),
        fecha_solucion=now_utc() - timedelta(days=4, hours=-7),
        causa_falla="desgaste",
        observaciones_cierre="Rutina de mantenimiento preventivo de grupo electrógeno completada al 100%. Parámetros eléctricos en carga estables a 220V 60Hz. Planta queda en automático.",
        datos_formulario=json.dumps(ot4_form, ensure_ascii=False)
    )

    # =========================================================================
    # OT 5: Informe 360 - Relevamiento Técnico Integral Claro (Ref: Plantillas 360)
    # =========================================================================
    ops_ot5 = [
        format_empleado_operador(emp_carlos),
        format_empleado_operador(emp_julian)
    ]
    ops_ot5 = [op for op in ops_ot5 if op]

    ot5_so = (sitio_titi.supervisor_operativo or sitio_titi.new_so or "ROBERTO VELEZ") if sitio_titi else "ROBERTO VELEZ"
    ot5_form = {
        # 1. Datos Generales GE
        "ge_estacion_base": sitio_titi.nombre if sitio_titi else "ANT.TITIRIBI",
        "ge_fecha_solicitud": (now_utc() - timedelta(days=3)).strftime("%Y-%m-%d"),
        "ge_horometro": 4120.5,
        "ge_marca_planta": "CATERPILLAR OLYMPIAN",
        "ge_modelo_planta": "GEP33-3",
        "ge_estado_fisico": "BUENO",
        "ge_estado_operacional": "OPERATIVO",
        "ge_potencia_kw": 30,
        "ge_consumo_kva": 37.5,
        "ge_marca_generador": "LEROY SOMER",
        "ge_modelo_generador": "LL1514P",
        # 6 Subsistemas GE
        "ge_estado_devanado": "BUENO",
        "ge_estado_tarjeta_avr": "BUENO",
        "ge_estado_generador_general": "BUENO",
        "ge_estado_pistones": "BUENO",
        "ge_estado_bomba_inyeccion": "BUENO",
        "ge_estado_sistema_admision": "BUENO",
        "ge_estado_motor_general": "BUENO",
        "ge_tipo_control": "digital_comap",
        "ge_estado_tablero_control": "BUENO",
        "ge_estado_medidores_analogos": "BUENO",
        "ge_estado_cableado_control": "BUENO",
        "ge_estado_botones_paro": "BUENO",
        "ge_estado_control_general": "BUENO",
        "ge_estado_radiador": "BUENO",
        "ge_estado_ventilador": "BUENO",
        "ge_estado_bomba_agua": "BUENO",
        "ge_estado_termostato": "BUENO",
        "ge_estado_mangueras": "BUENO",
        "ge_estado_sensor_temperatura": "BUENO",
        "ge_estado_refrigerante": "BUENO",
        "ge_estado_alternador": "BUENO",
        "ge_estado_avr_electrico": "BUENO",
        "ge_estado_bateria_arranque": "BUENO",
        "ge_estado_cargador_bateria": "BUENO",
        "ge_estado_arranque_electrico": "BUENO",
        "ge_estado_breaker_principal": "BUENO",
        "ge_estado_spt_planta": "BUENO",
        "ge_estado_ats_planta": "BUENO",
        "ge_estado_multiple_escape": "BUENO",
        "ge_estado_tubo_escape": "BUENO",
        "ge_estado_silenciador": "BUENO",
        "ge_estado_aislantes_termicos": "BUENO",
        "hallazgos_diagnostico_ge": [
            {
                "sistema": "Sistema Eléctrico y Control",
                "componente": "Bornes de Batería de Arranque",
                "descripcion": "Leve sulfatación en borne positivo sin caída de tensión.",
                "criticidad": "Baja",
                "accion_recomendada": "Limpieza mecánica y aplicación de grasa dieléctrica.",
                "evento": "Mantenimiento preventivo rutinario",
                "sintoma": "Presencia de sales en borne",
                "causa_raiz": "Humedad ambiente en shelter",
                "acciones_correctivas": "Limpieza y torqueado de terminales."
            }
        ],
        # 2. Prueba Megger (Aislamiento Alternador)
        "megger_vdc_prueba": 1000,
        "megger_temp_c": 28,
        "megger_hr_porcentaje": 68,
        "megger_r_min_criterio": 5.0,
        "megger_pi_min_criterio": 2.0,
        "megger_puntos": [
            {"punto": "U – Tierra", "r1min": 14.5, "r10min": 32.0},
            {"punto": "V – Tierra", "r1min": 15.2, "r10min": 33.5},
            {"punto": "W – Tierra", "r1min": 14.8, "r10min": 32.8},
            {"punto": "U – V", "r1min": 28.0, "r10min": 60.0},
            {"punto": "V – W", "r1min": 29.5, "r10min": 62.0},
            {"punto": "W – U", "r1min": 28.9, "r10min": 61.2},
            {"punto": "Excitación – Tierra", "r1min": 45.0, "r10min": 98.0}
        ],
        "megger_diagnostico": "Aislamiento dieléctrico en devanados del generador conforme con norma IEEE 43 (> 5 MΩ e IP > 2.0).",
        "megger_plan_accion": "Mantener monitoreo anual durante mantenimiento preventivo 360.",
        # 3. Prueba Banco de Carga Resistivo 80%
        "banco_vnom_ll": 220,
        "banco_fnom_hz": 60,
        "banco_carga_objetivo_pct": 80,
        "banco_lecturas": [
            {"tiempo": "00:05", "carga_pct": 80, "v_ll": 220, "hz": 60.1, "i_prom": 65.4, "kw": 24, "temp_c": 74, "presion_bar": 3.8, "notas": "Inicio de prueba. Curva de calentamiento normal."},
            {"tiempo": "00:15", "carga_pct": 80, "v_ll": 220, "hz": 60.0, "i_prom": 65.2, "kw": 24, "temp_c": 78, "presion_bar": 3.7, "notas": "Voltaje y frecuencia plenamente estables."},
            {"tiempo": "00:30", "carga_pct": 80, "v_ll": 219, "hz": 60.0, "i_prom": 65.5, "kw": 24, "temp_c": 80, "presion_bar": 3.6, "notas": "Temperatura estabilizada sin variaciones."},
            {"tiempo": "00:45", "carga_pct": 80, "v_ll": 220, "hz": 60.0, "i_prom": 65.3, "kw": 24, "temp_c": 81, "presion_bar": 3.6, "notas": "Operación silenciosa y sin vibración."},
            {"tiempo": "01:00", "carga_pct": 80, "v_ll": 220, "hz": 60.0, "i_prom": 65.4, "kw": 24, "temp_c": 81, "presion_bar": 3.6, "notas": "Prueba finalizada satisfactoriamente. Grupo Electrógeno APTO."}
        ],
        "banco_conclusion": "APTO",
        "banco_observaciones": "Comportamiento electro-mecánico sobresaliente. Frecuencia y voltaje dentro de la tolerancia de ±1.5%.",
        # 4. Inspección SPT
        "spt_wenner_imposible": True,
        "spt_wenner_motivo_imposible": "Terreno rocoso con losa de concreto integral sin acceso directo a terreno abierto perimetral.",
        "spt_condicion_suelo": "Roca / Concreto",
        "spt_wenner_lecturas": [
            {"a": 1, "r": None}, {"a": 2, "r": None}, {"a": 4, "r": None},
            {"a": 8, "r": None}, {"a": 10, "r": None}, {"a": 12, "r": None}, {"a": 14, "r": None}
        ],
        "spt_caida_imposible": False,
        "spt_caida_criterio_max": 5.0,
        "spt_r_62_medida": 2.35,
        "spt_caida_observaciones": "Resistencia de puesta a tierra excelente cumpliendo RETIE/IEC (< 5.0 Ω).",
        "spt_umbral_continuidad_max": 1.0,
        "spt_equipotencialidad_puntos": [
            {"id": 1, "elemento": "Barra Equipotencial Principal (BEP) / Barraje de tierra", "r_ohm": 0.03},
            {"id": 2, "elemento": "Rack / gabinete de ACCESO RAN (BTS/BBU/DU) – chasis", "r_ohm": 0.05},
            {"id": 3, "elemento": "Rack / gabinete de TRANSMISIÓN (MW IDU / Router) – chasis", "r_ohm": 0.06},
            {"id": 4, "elemento": "Gabinete RECTIFICADOR / POWER DC (-48V) – chasis", "r_ohm": 0.04},
            {"id": 5, "elemento": "Banco de BATERÍAS (rack/caja y bandejas) – estructura", "r_ohm": 0.05},
            {"id": 6, "elemento": "Tablero de DISTRIBUCIÓN DC (PDB / fusiblera) – carcasa", "r_ohm": 0.06},
            {"id": 7, "elemento": "Tablero GENERAL AC / protecciones (TGP) – carcasa", "r_ohm": 0.07},
            {"id": 8, "elemento": "TRANSFERENCIA AUTOMÁTICA (ATS) – carcasa metálica", "r_ohm": 0.09},
            {"id": 9, "elemento": "GRUPO ELECTRÓGENO (chasis/bastidor + alternador)", "r_ohm": 0.05},
            {"id": 10, "elemento": "AIRES ACONDICIONADOS (AA-1 y AA-2) – chasis metálico", "r_ohm": 0.08},
            {"id": 11, "elemento": "Torre/estructura metálica + bajante LPS (pararrayos)", "r_ohm": 0.11}
        ],
        # 5. Instrumentos y Calibración
        "instrumentos": [
            {"tipo": "Megóhmetro de Aislamiento", "marca": "Fluke", "modelo": "1587 FC", "serial": "FLK-1587-99214", "fecha_calibracion": "2026-02-15", "vigente": "Si"},
            {"tipo": "Telurómetro / Medidor de Tierra", "marca": "AEMC", "modelo": "4630", "serial": "AEMC-4630-8812", "fecha_calibracion": "2026-01-20", "vigente": "Si"},
            {"tipo": "Pinza Amperimétrica True RMS", "marca": "Fluke", "modelo": "376 FC", "serial": "FLK-376-77341", "fecha_calibracion": "2026-03-10", "vigente": "Si"}
        ],
        "operadores_asignados": ops_ot5
    }

    f_inicio_5 = now_utc() - timedelta(days=3)
    ot5 = Ot(
        codigo="OT360000101",
        id_actividad="ACT-2026-3600101",
        tipo_actividad="informe_360",
        tipo_mantenimiento="preventivo",
        descripcion="Informe 360 Relevamiento Integral Claro - Megger Aislamiento, Banco Resistivo 80%, Inspección SPT y Diagnóstico SMU de 6 Subsistemas GE",
        sitio=sitio_titi.nombre if sitio_titi else "ANT.TITIRIBI",
        sitio_id=sitio_titi.id if sitio_titi else None,
        ubicacion=f"{sitio_titi.municipio or 'Titiribí'}, Antioquia" if sitio_titi else "Vereda La Albania, Titiribí, Antioquia",
        departamento="Antioquia",
        regional="R1",
        categoria="rural",
        tipo_estacion="MOVIL",
        site_owner=ot5_so,
        coordinador=emp_carlos.nombre if emp_carlos else "Ing. Carlos Pérez",
        created_by=admin.id,
        user_id=carlos.id,
        cuadrilla_id=cuadrilla_ant.id if cuadrilla_ant else None,
        prioridad="P2",
        tipo_ubicacion="rural",
        subsistema="PE - GRUPO ELECTROGENO",
        progreso=80,
        estado="en_progreso",
        fecha_inicio=f_inicio_5,
        fecha_limite_sla=sla_service.calcular_fecha_limite("P2", "rural", f_inicio_5),
        fecha_llegada_sitio=now_utc() - timedelta(days=2, hours=-3),
        datos_formulario=json.dumps(ot5_form, ensure_ascii=False)
    )

    # =========================================================================
    # OT 6: Rutina MP 7x24 - Planta Eléctrica (Ref: Rutinas Periódicas Claro)
    # =========================================================================
    ops_ot6 = [
        format_empleado_operador(emp_jasmin),
        format_empleado_operador(emp_lozano)
    ]
    ops_ot6 = [op for op in ops_ot6 if op]

    ot6_so = (sitio_pizarro.supervisor_operativo or sitio_pizarro.new_so or "ALEXANDER GOMEZ") if sitio_pizarro else "ALEXANDER GOMEZ"
    ot6_form = {
        "marca_equipo": "Cummins Power",
        "modelo_equipo": "C33D5",
        "serial_equipo": "CP-449102",
        "horometro_inicial": 2150.4,
        "frecuencia_hz": 60,
        "capacidad_kva": 33,
        "voltaje_bateria": 25.8,
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
        "observaciones_preventivo": "Rutina preventiva programada 7x24 completada sin observaciones. Tablero sin alarmas y transferencia automática en modo automático.",
        "operadores_asignados": ops_ot6
    }

    f_inicio_6 = now_utc() - timedelta(days=6)
    ot6 = Ot(
        codigo="OT5304021",
        id_actividad="ACT-2026-078192",
        tipo_actividad="rutina_7x24_planta",
        tipo_mantenimiento="preventivo",
        descripcion="Rutina Preventiva MP 7x24 Planta Eléctrica y Climatización - Pruebas de Transferencia y Calidad de Red",
        sitio=sitio_pizarro.nombre if sitio_pizarro else "CHO.PIZARRO",
        sitio_id=sitio_pizarro.id if sitio_pizarro else None,
        ubicacion=f"{sitio_pizarro.municipio or 'Pizarro'}, Chocó" if sitio_pizarro else "Pizarro, Chocó",
        departamento="Chocó",
        regional="R2",
        categoria="rural",
        tipo_estacion="MOVIL",
        site_owner=ot6_so,
        coordinador=emp_adminis.nombre if emp_adminis else "Auxiliar Técnico",
        created_by=admin.id,
        user_id=luis.id,
        cuadrilla_id=cuadrilla_cho.id if cuadrilla_cho else None,
        prioridad="P2",
        tipo_ubicacion="rural",
        subsistema="PE - GRUPO ELECTROGENO",
        progreso=100,
        estado="finalizada",
        fecha_inicio=f_inicio_6,
        fecha_limite_sla=sla_service.calcular_fecha_limite("P2", "rural", f_inicio_6),
        fecha_llegada_sitio=now_utc() - timedelta(days=6, hours=-2),
        fecha_solucion=now_utc() - timedelta(days=6, hours=-8),
        causa_falla="desgaste",
        observaciones_cierre="Rutina de inspección y mantenimiento preventivo ejecutada en su totalidad con pruebas ATS en carga.",
        datos_formulario=json.dumps(ot6_form, ensure_ascii=False)
    )

    db.add_all([ot1, ot2, ot3, ot4, ot5, ot6])
    db.commit()

    # 4. Evidencias Fotográficas Georreferenciadas con Foto Obligatoria de Llegada a Sitio
    print(f"[{db_name}] 3. Creando evidencias fotográficas georreferenciadas (con foto obligatoria de llegada a sitio)...")
    evidencias = [
        # OT 1: Correctivo
        EvidenciaFotografica(
            ot_id=ot1.id,
            tipo="llegada_sitio",
            url_imagen="https://images.unsplash.com/photo-1541888946425-d0fbb186f5f8?w=800",
            latitud=7.8829,
            longitud=-76.6256,
            fecha_hora_captura=now_utc() - timedelta(days=2, hours=-1)
        ),
        EvidenciaFotografica(
            ot_id=ot1.id,
            tipo="antes",
            url_imagen="https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800",
            latitud=7.8829,
            longitud=-76.6256,
            fecha_hora_captura=now_utc() - timedelta(days=2, hours=-2)
        ),
        # OT 2: Emergencia
        EvidenciaFotografica(
            ot_id=ot2.id,
            tipo="llegada_sitio",
            url_imagen="https://images.unsplash.com/photo-1541888946425-d0fbb186f5f8?w=800",
            latitud=5.3120,
            longitud=-76.7820,
            fecha_hora_captura=now_utc() - timedelta(hours=10)
        ),
        # OT 3: Preventivo Aire
        EvidenciaFotografica(
            ot_id=ot3.id,
            tipo="llegada_sitio",
            url_imagen="https://images.unsplash.com/photo-1541888946425-d0fbb186f5f8?w=800",
            latitud=8.7500,
            longitud=-75.8833,
            fecha_hora_captura=now_utc() - timedelta(hours=3)
        ),
        EvidenciaFotografica(
            ot_id=ot3.id,
            tipo="durante",
            url_imagen="https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800",
            latitud=8.7500,
            longitud=-75.8833,
            fecha_hora_captura=now_utc() - timedelta(hours=2)
        ),
        # OT 4: Preventivo Planta Bahía Solano
        EvidenciaFotografica(
            ot_id=ot4.id,
            tipo="llegada_sitio",
            url_imagen="https://images.unsplash.com/photo-1541888946425-d0fbb186f5f8?w=800",
            latitud=6.2269,
            longitud=-77.4044,
            fecha_hora_captura=now_utc() - timedelta(days=4, hours=-1)
        ),
        EvidenciaFotografica(
            ot_id=ot4.id,
            tipo="antes",
            url_imagen="https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800",
            latitud=6.2269,
            longitud=-77.4044,
            fecha_hora_captura=now_utc() - timedelta(days=4, hours=-2)
        ),
        EvidenciaFotografica(
            ot_id=ot4.id,
            tipo="durante",
            url_imagen="https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800",
            latitud=6.2270,
            longitud=-77.4045,
            fecha_hora_captura=now_utc() - timedelta(days=4, hours=-4)
        ),
        EvidenciaFotografica(
            ot_id=ot4.id,
            tipo="despues",
            url_imagen="https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800",
            latitud=6.2269,
            longitud=-77.4044,
            fecha_hora_captura=now_utc() - timedelta(days=4, hours=-6)
        ),
        # OT 5: Relevamiento 360
        EvidenciaFotografica(
            ot_id=ot5.id,
            tipo="llegada_sitio",
            url_imagen="https://images.unsplash.com/photo-1541888946425-d0fbb186f5f8?w=800",
            latitud=6.0619,
            longitud=-75.7925,
            fecha_hora_captura=now_utc() - timedelta(days=2, hours=-3)
        ),
        EvidenciaFotografica(
            ot_id=ot5.id,
            tipo="diagnostico_360",
            url_imagen="https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800",
            latitud=6.0619,
            longitud=-75.7925,
            fecha_hora_captura=now_utc() - timedelta(days=2, hours=-4)
        ),
        EvidenciaFotografica(
            ot_id=ot5.id,
            tipo="pruebas",
            url_imagen="https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800",
            latitud=6.0619,
            longitud=-75.7925,
            fecha_hora_captura=now_utc() - timedelta(days=2, hours=-5)
        ),
        EvidenciaFotografica(
            ot_id=ot5.id,
            tipo="spt",
            url_imagen="https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800",
            latitud=6.0619,
            longitud=-75.7925,
            fecha_hora_captura=now_utc() - timedelta(days=2, hours=-6)
        ),
        # OT 6: Rutina 7x24
        EvidenciaFotografica(
            ot_id=ot6.id,
            tipo="llegada_sitio",
            url_imagen="https://images.unsplash.com/photo-1541888946425-d0fbb186f5f8?w=800",
            latitud=4.9500,
            longitud=-77.3667,
            fecha_hora_captura=now_utc() - timedelta(days=6, hours=-2)
        ),
        EvidenciaFotografica(
            ot_id=ot6.id,
            tipo="despues",
            url_imagen="https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800",
            latitud=4.9500,
            longitud=-77.3667,
            fecha_hora_captura=now_utc() - timedelta(days=6, hours=-7)
        )
    ]
    db.add_all(evidencias)

    # 5. Repuestos e Insumos LPU
    print(f"[{db_name}] 4. Creando insumos y repuestos LPU vinculados...")
    repuestos = [
        RepuestoUtilizado(ot_id=ot1.id, nombre_item="Bomba de agua Selmec Perkins 40SC", cantidad=1.0, unidad_medida="Unidad"),
        RepuestoUtilizado(ot_id=ot1.id, nombre_item="Refrigerante Anticongelante 50/50 LPU Claro", cantidad=2.0, unidad_medida="Galón"),
        RepuestoUtilizado(ot_id=ot2.id, nombre_item="Celda de Batería 2V 500Ah Narada", cantidad=1.0, unidad_medida="Unidad"),
        RepuestoUtilizado(ot_id=ot2.id, nombre_item="Cable de Fuerza 2 AWG", cantidad=6.0, unidad_medida="Metro"),
        RepuestoUtilizado(ot_id=ot3.id, nombre_item="Gas Refrigerante Ecológico R410A", cantidad=3.0, unidad_medida="Kg"),
        RepuestoUtilizado(ot_id=ot3.id, nombre_item="Filtro de Aire Lavable Tipo Panel", cantidad=2.0, unidad_medida="Unidad"),
        RepuestoUtilizado(ot_id=ot4.id, nombre_item="Filtro de Aceite LF16015 Fleetguard", cantidad=1.0, unidad_medida="Unidad"),
        RepuestoUtilizado(ot_id=ot4.id, nombre_item="Filtro Separador Combustible FS1242", cantidad=1.0, unidad_medida="Unidad"),
        RepuestoUtilizado(ot_id=ot4.id, nombre_item="Aceite Lubricante 15W40 CI-4", cantidad=3.5, unidad_medida="Galón"),
        RepuestoUtilizado(ot_id=ot6.id, nombre_item="Kit Filtros y Lubricante 15W40 Cummins", cantidad=1.0, unidad_medida="Kit")
    ]
    db.add_all(repuestos)

    # 6. Avances de Bitácora PDT
    print(f"[{db_name}] 5. Creando bitácora cronológica de avances en campo (PDT)...")
    avances = [
        Avance(ot_id=ot1.id, user_id=carlos.id, descripcion="Llegada a estación base Apartadó. Inspección preoperacional y charla SST de 5 minutos.", porcentaje=10, fecha_reporte=now_utc() - timedelta(days=2, hours=-1)),
        Avance(ot_id=ot1.id, user_id=carlos.id, descripcion="Desmonte de bomba de agua dañada con fuga en el sello mecánico.", porcentaje=25, fecha_reporte=now_utc() - timedelta(days=2, hours=-2)),
        Avance(ot_id=ot3.id, user_id=carlos.id, descripcion="Llegada a estación base Montería. Inicio de lavado de condensadora exterior.", porcentaje=30, fecha_reporte=now_utc() - timedelta(hours=3)),
        Avance(ot_id=ot3.id, user_id=carlos.id, descripcion="Limpieza de serpentín evaporador y medición de presiones manométricas R410A.", porcentaje=65, fecha_reporte=now_utc() - timedelta(hours=1)),
        Avance(ot_id=ot4.id, user_id=eliseo.id, descripcion="Llegada a RPT Bahía Solano tras desplazamiento fluvial. Apertura de caseta de planta eléctrica.", porcentaje=20, fecha_reporte=now_utc() - timedelta(days=4, hours=-1)),
        Avance(ot_id=ot4.id, user_id=eliseo.id, descripcion="Drenaje de aceite usado y sustitución de filtros de aceite y combustible.", porcentaje=60, fecha_reporte=now_utc() - timedelta(days=4, hours=-3)),
        Avance(ot_id=ot4.id, user_id=eliseo.id, descripcion="Prueba de encendido y simulación de corte de energía durante 15 minutos en carga con ATS. Parámetros conformes.", porcentaje=100, fecha_reporte=now_utc() - timedelta(days=4, hours=-6)),
        Avance(ot_id=ot5.id, user_id=carlos.id, descripcion="Llegada a estación Titiribí. Inicio de relevamiento e inspección de los 6 subsistemas del GE.", porcentaje=25, fecha_reporte=now_utc() - timedelta(days=2, hours=-3)),
        Avance(ot_id=ot5.id, user_id=carlos.id, descripcion="Pruebas de aislamiento Megger a 1000Vdc y mediciones de resistencia de puesta a tierra SPT con telurómetro.", porcentaje=60, fecha_reporte=now_utc() - timedelta(days=2, hours=-4)),
        Avance(ot_id=ot5.id, user_id=carlos.id, descripcion="Conexión de banco resistivo y prueba de carga al 80% durante 60 minutos con lecturas cada 15 min.", porcentaje=80, fecha_reporte=now_utc() - timedelta(days=2, hours=-6)),
        Avance(ot_id=ot6.id, user_id=luis.id, descripcion="Ejecución y cierre de rutina preventiva 7x24 con pruebas de transferencia en automático.", porcentaje=100, fecha_reporte=now_utc() - timedelta(days=6, hours=-7))
    ]
    db.add_all(avances)

    # 7. Sub-actividades de checklist
    print(f"[{db_name}] 6. Creando subactividades operativas del checklist...")
    actividades = [
        ActividadOt(ot_id=ot1.id, nombre="Desmonte de bomba averiada y limpieza de acople", peso_porcentaje=30, progreso=30, estado="completada"),
        ActividadOt(ot_id=ot1.id, nombre="Instalación de nueva bomba y purga de refrigerante", peso_porcentaje=40, progreso=0, estado="pendiente"),
        ActividadOt(ot_id=ot1.id, nombre="Pruebas con carga y validación con supervisor Claro", peso_porcentaje=30, progreso=0, estado="pendiente"),
        ActividadOt(ot_id=ot4.id, nombre="Inspección visual de planta y niveles de fluidos", peso_porcentaje=25, progreso=25, estado="completada"),
        ActividadOt(ot_id=ot4.id, nombre="Cambio de filtros y lubricante de motor", peso_porcentaje=35, progreso=35, estado="completada"),
        ActividadOt(ot_id=ot4.id, nombre="Prueba 15 min soportando carga simulando falla", peso_porcentaje=40, progreso=40, estado="completada"),
        ActividadOt(ot_id=ot5.id, nombre="Diagnóstico visual y funcional de los 6 subsistemas GE", peso_porcentaje=25, progreso=25, estado="completada"),
        ActividadOt(ot_id=ot5.id, nombre="Ensayo de aislamiento dieléctrico Megger 1000V", peso_porcentaje=25, progreso=25, estado="completada"),
        ActividadOt(ot_id=ot5.id, nombre="Prueba con Banco de Carga Resistivo al 80%", peso_porcentaje=30, progreso=30, estado="completada"),
        ActividadOt(ot_id=ot5.id, nombre="Medición de resistividad y equipotencialidad SPT", peso_porcentaje=20, progreso=0, estado="pendiente")
    ]
    db.add_all(actividades)

    db.commit()
    print(f"[SUCCESS] {db_name}: 6 Órdenes de Trabajo tipificadas y sembradas con éxito (WO, MP Planta, MP Aire, Relevamiento 360 y Rutina 7x24).")

def main():
    print("=" * 75)
    print("  DOBLEX S.A.S. - LIMPIEZA Y RE-SIEMBRA INTEGRAL DE OTs (WO, MP & 360)")
    print("=" * 75)

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
        print(f"[INFO] PostgreSQL Docker no configurado o inactivo: {e}")

    print("\n" + "=" * 75)
    print("  PROCESO DE LIMPIEZA Y RE-SEEDING DE OTS FINALIZADO EXITOSAMENTE")
    print("=" * 75)

if __name__ == "__main__":
    main()

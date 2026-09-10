import json
from datetime import datetime, timedelta
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.core.security import get_password_hash
from app.core.utils import now_utc
from app.models.user import User
from app.models.empleado import Empleado
from app.models.cuadrilla import Cuadrilla
from app.models.ot import Ot
from app.models.actividad_ot import ActividadOt
from app.models.evidencia import EvidenciaFotografica
from app.models.repuesto import RepuestoUtilizado
from app.models.avance import Avance

def seed_database():
    """
    Puebla la base de datos con los perfiles operativos, cuadrillas, directorio de empleados
    y las 5 OTs tipificadas con sus evidencias fotográficas, repuestos y avances.
    """
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Verificar si ya existen usuarios y sincronizar OTs existentes con nuevos campos
        if db.query(User).count() > 0:
            print("[INFO] La base de datos ya contiene registros. Verificando y actualizando campos de OTs...")
            existing_ots = db.query(Ot).all()
            updated_count = 0
            for ot in existing_ots:
                needs_update = False
                if not ot.id_actividad:
                    ot.id_actividad = f"ACT-2026-{abs(hash(ot.codigo)) % 900000 + 100000}"
                    needs_update = True
                if not ot.tipo_actividad:
                    if ot.tipo_mantenimiento == "preventivo":
                        ot.tipo_actividad = "preventivo_aire" if "aire" in (ot.subsistema or "").lower() else "preventivo_planta"
                    else:
                        ot.tipo_actividad = ot.tipo_mantenimiento or "correctivo"
                    needs_update = True
                if not ot.coordinador:
                    ot.coordinador = "Ing. Mauricio Quintero" if "ANT" in (ot.sitio or "") else "Ing. Alexander Gómez"
                    needs_update = True
                if not ot.categoria:
                    ot.categoria = "rural" if ot.tipo_ubicacion == "rural" else "normal"
                    needs_update = True
                if not ot.regional:
                    ot.regional = "R2" if "Chocó" in (ot.ubicacion or "") else "R1"
                    needs_update = True
                if not ot.departamento:
                    if "Chocó" in (ot.ubicacion or ""):
                        ot.departamento = "Chocó"
                    elif "Córdoba" in (ot.ubicacion or ""):
                        ot.departamento = "Córdoba"
                    elif "Atlántico" in (ot.ubicacion or "") or "Barranquilla" in (ot.ubicacion or ""):
                        ot.departamento = "Atlántico"
                    else:
                        ot.departamento = "Antioquia"
                    needs_update = True
                if not ot.tipo_estacion:
                    ot.tipo_estacion = "REPETIDORA" if "repetidora" in (ot.descripcion or "").lower() else "MOVIL"
                    needs_update = True
                if not ot.site_owner:
                    ot.site_owner = "CLARO"
                    needs_update = True
                if not ot.datos_formulario:
                    if ot.tipo_actividad in ("correctivo", "emergencia"):
                        ot.datos_formulario = json.dumps({
                            "afectacion_servicio": "NO",
                            "equipo_en_falla": "Selmec 40SC" if "ANT" in (ot.sitio or "") else "Inversor y Banco Baterías",
                            "tipo_trabajo": "Reparación y calibración",
                            "repuesto_retirado": {
                                "nombre": "Tarjeta AVR SX460 con diodos quemados",
                                "serial": "SN-SX460-0988"
                            },
                            "repuesto_instalado": {
                                "nombre": "Tarjeta AVR SX460 original nueva",
                                "serial": "SN-SX460-7741"
                            },
                            "supervisor_claro": "Ing. Roberto Vélez",
                            "diagnostico_tecnico": "Falla en regulación de voltaje por sobrecalentamiento. Se reemplaza y calibra a 220V/127V a 60Hz."
                        })
                    elif ot.tipo_actividad == "preventivo_aire":
                        ot.datos_formulario = json.dumps({
                            "marca_equipo": "ComfortStar / York",
                            "capacidad_btu": 24000,
                            "refrigerante": "R410A",
                            "presion_baja_psi": 120,
                            "presion_alta_psi": 350,
                            "corriente_compresor_amp": 9.8,
                            "limpieza_evaporador": "OK - Con desincrustante",
                            "limpieza_condensador": "OK - Lavado a presión",
                            "cambio_filtros": "OK - Reemplazados"
                        })
                    else:
                        ot.datos_formulario = json.dumps({
                            "marca_planta": "AGG Power",
                            "kva": 24,
                            "marca_motor": "Cummins 4BTA3.9-G2",
                            "serial_motor": "46981245",
                            "marca_generador": "Stamford PI144E",
                            "serial_generador": "X19K458210",
                            "horometro": 3913.3,
                            "voltaje_bateria": 25.2,
                            "galones_combustible": 48,
                            "prueba_encendido": "Arranque automático ATS en 4.2s. Voltaje estable 220V a 60Hz."
                        })
                    needs_update = True

                if needs_update:
                    updated_count += 1

            if updated_count > 0:
                db.commit()
                print(f"[INFO] Se actualizaron {updated_count} OTs existentes con los nuevos campos y formularios técnicos.")
            return

        print("[SEED] Creando usuarios del sistema...")
        admin = User(
            name="Admin General",
            username="admin.doblex",
            email="admin@doblex.com",
            role="admin",
            password=get_password_hash("admin123")
        )
        adminis = User(
            name="Auxiliar Técnico",
            username="adminis.doblex",
            email="adminis@doblex.com",
            role="administrativo",
            password=get_password_hash("adminis123")
        )
        carlos = User(
            name="Ing. Carlos Pérez",
            username="carlos.doblex",
            email="carlos@doblex.com",
            role="operativo",
            password=get_password_hash("operador123")
        )
        luis = User(
            name="Ing. Luis Martínez",
            username="luis.doblex",
            email="luis@doblex.com",
            role="operativo",
            password=get_password_hash("operador123")
        )
        jasmin = User(
            name="Jasmin Ariel Mosquera",
            username="jasmin.doblex",
            email="jasmin@doblex.com",
            role="operativo",
            password=get_password_hash("operador123")
        )
        eliseo = User(
            name="Eliseo Smith Granados",
            username="eliseo.doblex",
            email="eliseo@doblex.com",
            role="operativo",
            password=get_password_hash("operador123")
        )
        db.add_all([admin, adminis, carlos, luis, jasmin, eliseo])
        db.commit()

        print("[SEED] Creando cuadrillas regionales...")
        cuadrilla_ant = Cuadrilla(
            nombre="Cuadrilla Regional Antioquia & Urabá",
            especialidad="Grupos Electrógenos GE/ATS & Mantenimiento Integral",
            lider_id=carlos.id
        )
        cuadrilla_cho = Cuadrilla(
            nombre="Cuadrilla Regional Chocó",
            especialidad="Sistemas Híbridos SFV & Redes Aisladas ZNI",
            lider_id=jasmin.id
        )
        cuadrilla_cor = Cuadrilla(
            nombre="Cuadrilla Regional Córdoba",
            especialidad="Climatización de Precisión & Fuerza DC",
            lider_id=carlos.id
        )
        cuadrilla_atl = Cuadrilla(
            nombre="Cuadrilla Regional Atlántico",
            especialidad="Media Tensión, Subestaciones & Balizamiento en Altura",
            lider_id=eliseo.id
        )
        db.add_all([cuadrilla_ant, cuadrilla_cho, cuadrilla_cor, cuadrilla_atl])
        db.commit()

        print("[SEED] Creando directorio completo de empleados (11)...")
        empleados = [
            Empleado(documento="1090887123", nombre="Admin General", cargo="Director General de Obra", telefono="3001234567", email="admin@doblex.com", rol="admin", user_id=admin.id, estado="activo"),
            Empleado(documento="1090887456", nombre="Auxiliar Técnico", cargo="Asistente Administrativo de Campo", telefono="3109876543", email="adminis@doblex.com", rol="administrativo", user_id=adminis.id, estado="activo"),
            # Antioquia
            Empleado(documento="1018445990", nombre="Ing. Carlos Pérez", cargo="Ingeniero Residente Electromecánico", telefono="3157778899", email="carlos@doblex.com", rol="operativo", cuadrilla_id=cuadrilla_ant.id, user_id=carlos.id, estado="activo"),
            Empleado(documento="71175427", nombre="Julián Alexander Rivillas Meneses", cargo="Técnico Integral (Medellín-Urabá)", telefono="3114567890", email="julian.rivillas@doblex.com", rol="operativo", cuadrilla_id=cuadrilla_ant.id, estado="activo"),
            Empleado(documento="8167017", nombre="Manuel Francisco Tapias Urango", cargo="Técnico Electromecánico (Urabá)", telefono="3145678901", email="manuel.tapias@doblex.com", rol="operativo", cuadrilla_id=cuadrilla_ant.id, estado="activo"),
            # Chocó
            Empleado(documento="8336030", nombre="Jasmin Ariel Mosquera Rosero", cargo="Técnico Electromecánico (Chocó)", telefono="3216549870", email="jasmin@doblex.com", rol="operativo", cuadrilla_id=cuadrilla_cho.id, user_id=jasmin.id, estado="activo"),
            Empleado(documento="1077173308", nombre="Carlos Rafael Lozano Hinestroza", cargo="Técnico Transmisión (Chocó)", telefono="3108765432", email="carlos.lozano@doblex.com", rol="operativo", cuadrilla_id=cuadrilla_cho.id, estado="activo"),
            # Córdoba
            Empleado(documento="78705371", nombre="Ancízar Manuel Pérez Ortiz", cargo="Técnico Electricista (Córdoba)", telefono="3137894561", email="ancizar.perez@doblex.com", rol="operativo", cuadrilla_id=cuadrilla_cor.id, estado="activo"),
            Empleado(documento="94466010", nombre="Ramón Elías Yepes Jaramillo", cargo="Técnico Electromecánico (Córdoba)", telefono="3123456789", email="ramon.yepes@doblex.com", rol="operativo", cuadrilla_id=cuadrilla_cor.id, estado="activo"),
            # Atlántico
            Empleado(documento="8567519", nombre="Eliseo Smith Granados Vanegas", cargo="Técnico Electricista (Barranquilla)", telefono="3012345678", email="eliseo@doblex.com", rol="operativo", cuadrilla_id=cuadrilla_atl.id, user_id=eliseo.id, estado="activo"),
            Empleado(documento="1018445112", nombre="Ing. Luis Martínez", cargo="Ingeniero de Energía y Climatización", telefono="3186665544", email="luis@doblex.com", rol="operativo", cuadrilla_id=cuadrilla_atl.id, user_id=luis.id, estado="activo"),
        ]
        db.add_all(empleados)
        db.commit()

        print("[SEED] Creando las 5 Órdenes de Trabajo (OTs) adaptadas a formatos de campo WO y MP...")
        # OT 1: Antioquia - Formato WO Correctivo Selmec 40SC
        ot1 = Ot(
            codigo="OT-2026-101",
            id_actividad="ACT-2026-5558781",
            tipo_actividad="correctivo",
            descripcion="Mantenimiento Correctivo GE/ATS - Diagnóstico de Tarjeta AVR y Reparación de Aislamientos en Bobinado de Generador Selmec / Stamford",
            sitio="ANT.APARTADO - EB Apartadó Centro (ANT-028)",
            ubicacion="Cra. 100 # 98-45, Apartadó, Antioquia",
            departamento="Antioquia",
            regional="R1",
            categoria="normal",
            tipo_estacion="MOVIL",
            site_owner="CLARO",
            coordinador="Ing. Mauricio Quintero",
            created_by=admin.id,
            user_id=carlos.id,
            cuadrilla_id=cuadrilla_ant.id,
            prioridad="P1",
            tipo_ubicacion="urbana",
            tipo_mantenimiento="correctivo",
            subsistema="Movil Plantas Eléctricas",
            progreso=15,
            estado="asignada",
            fecha_inicio=datetime(2026, 8, 14, 8, 0, 0),
            fecha_limite_sla=datetime(2026, 8, 15, 18, 0, 0),
            datos_formulario=json.dumps({
                "afectacion_servicio": "NO",
                "equipo_en_falla": "Selmec 40SC",
                "tipo_trabajo": "Reparación y calibración",
                "repuesto_retirado": {
                    "nombre": "Tarjeta AVR SX460 quemada",
                    "serial": "SN-SX460-0988"
                },
                "repuesto_instalado": {
                    "nombre": "Tarjeta AVR SX460 original nueva",
                    "serial": "SN-SX460-7741"
                },
                "transporte_especial": "Vehículo 4x4",
                "supervisor_claro": "Ing. Roberto Vélez",
                "diagnostico_tecnico": "Falla en regulación de voltaje por varistor quemado. Reemplazo y ajuste a 220V/127V 60Hz."
            })
        )

        # OT 2: Chocó - Formato WO Atención de Emergencia
        ot2 = Ot(
            codigo="OT-2026-102",
            id_actividad="ACT-2026-099014",
            tipo_actividad="emergencia",
            descripcion="Mantenimiento de Emergencia Híbrido SFV & Power DC - Falla en Inversor y Banco de Baterías de Repetidora ZNI",
            sitio="CHO.CANTON DE SAN PABLO - EB Managrú (CHO-014)",
            ubicacion="Sector Río Atrato, Cantón de San Pablo, Chocó",
            departamento="Chocó",
            regional="R2",
            categoria="rural",
            tipo_estacion="REPETIDORA",
            site_owner="CLARO",
            coordinador="Ing. Alexander Gómez",
            created_by=adminis.id,
            user_id=jasmin.id,
            cuadrilla_id=cuadrilla_cho.id,
            prioridad="P1",
            tipo_ubicacion="rural",
            tipo_mantenimiento="emergencia",
            subsistema="Móvil Híbridos SFV",
            progreso=35,
            estado="en_camino",
            fecha_inicio=datetime(2026, 8, 14, 10, 0, 0),
            fecha_limite_sla=datetime(2026, 8, 15, 6, 0, 0),
            datos_formulario=json.dumps({
                "afectacion_servicio": "SI",
                "equipo_en_falla": "Banco Baterías 48V / Inversor",
                "tipo_trabajo": "Reemplazo de emergencia",
                "transporte_especial": "Lancha fluvial Río Atrato",
                "supervisor_claro": "Ing. Carlos Hinestroza",
                "diagnostico_tecnico": "Descarga atmosférica averió módulo de protección y banco de baterías."
            })
        )

        # OT 3: Córdoba - Formato MP Aire Acondicionado
        ot3 = Ot(
            codigo="OT-2026-103",
            id_actividad="ACT-2026-030401",
            tipo_actividad="preventivo_aire",
            descripcion="Mantenimiento Preventivo & Climatización AA Móvil - Servicio a Compresores y Condensadoras de Precisión en Shelter de Transmisión",
            sitio="COR.MONTERIA - EB Ronda del Sinú (MON-019)",
            ubicacion="Calle 27 # 4-50, Centro, Montería, Córdoba",
            departamento="Córdoba",
            regional="R1",
            categoria="normal",
            tipo_estacion="MOVIL",
            site_owner="CLARO",
            coordinador="Ing. Sandra Morales",
            created_by=adminis.id,
            user_id=carlos.id,
            cuadrilla_id=cuadrilla_cor.id,
            prioridad="P2",
            tipo_ubicacion="urbana",
            tipo_mantenimiento="preventivo",
            subsistema="Movil Aires Acondicionados",
            progreso=65,
            estado="en_sitio",
            fecha_inicio=datetime(2026, 8, 14, 13, 0, 0),
            fecha_limite_sla=datetime(2026, 8, 15, 17, 0, 0),
            fecha_llegada_sitio=datetime(2026, 8, 14, 14, 15, 0),
            datos_formulario=json.dumps({
                "marca_equipo": "ComfortStar 24K BTU",
                "capacidad_btu": 24000,
                "refrigerante": "R410A",
                "presion_baja_psi": 120,
                "presion_alta_psi": 350,
                "corriente_compresor_amp": 9.8,
                "limpieza_evaporador": "Realizada",
                "limpieza_condensador": "Realizada con hidrolavadora",
                "cambio_filtros": "Filtros lavables reemplazados"
            })
        )

        # OT 4: Atlántico - Formato MP Planta Eléctrica AGG Power (Muestra Bahía Solano)
        ot4 = Ot(
            codigo="OT-2026-104",
            id_actividad="ACT-2026-5304019",
            tipo_actividad="preventivo_planta",
            descripcion="Mantenimiento Preventivo Planta Eléctrica AGG Power - Medición de Parámetros, Batería, Nivel de Combustible y Pruebas ATS",
            sitio="ATL.BARRANQUILLA - EB Riomar Industrial (BQ-042)",
            ubicacion="Vía 40 # 76-12, Barranquilla, Atlántico",
            departamento="Atlántico",
            regional="R1",
            categoria="normal",
            tipo_estacion="MOVIL",
            site_owner="CLARO",
            coordinador="Ing. Carlos Mendoza",
            created_by=admin.id,
            user_id=eliseo.id,
            cuadrilla_id=cuadrilla_atl.id,
            prioridad="P3",
            tipo_ubicacion="urbana",
            tipo_mantenimiento="preventivo",
            subsistema="Movil Plantas Eléctricas",
            progreso=100,
            estado="solucionada",
            fecha_inicio=datetime(2026, 8, 10, 8, 0, 0),
            fecha_limite_sla=datetime(2026, 8, 12, 18, 0, 0),
            fecha_llegada_sitio=datetime(2026, 8, 10, 9, 30, 0),
            fecha_solucion=datetime(2026, 8, 10, 16, 45, 0),
            causa_falla="desgaste",
            observaciones_cierre="Inspección de grupo electrógeno con prueba de arranque ATS. Parámetros eléctricos estables en 220V 60Hz.",
            datos_formulario=json.dumps({
                "marca_planta": "AGG Power",
                "kva": 24,
                "marca_motor": "Cummins 4BTA3.9-G2",
                "serial_motor": "46981245",
                "marca_generador": "Stamford PI144E",
                "serial_generador": "X19K458210",
                "horometro": 3913.3,
                "voltaje_bateria": 25.2,
                "galones_combustible": 48,
                "prueba_encendido": "Arranque automático ATS en 4.2 segundos. Voltaje estable 220V fase-fase, 60Hz.",
                "temperatura_operacion": "78 °C",
                "presion_aceite_psi": 52
            })
        )

        # OT 5: Titiribí - Formato MP Planta Eléctrica Rural
        ot5 = Ot(
            codigo="OT-2026-105",
            id_actividad="ACT-2026-078192",
            tipo_actividad="preventivo_planta",
            descripcion="Mantenimiento Preventivo Integral de Planta Eléctrica y Enlace de Transmisión",
            sitio="ANT.TITIRIBI LA ALBANIA - EB La Albania (ANT-072)",
            ubicacion="Vereda La Albania, Titiribí, Antioquia",
            departamento="Antioquia",
            regional="R1",
            categoria="rural",
            tipo_estacion="MOVIL",
            site_owner="CLARO",
            coordinador="Ing. Mauricio Quintero",
            created_by=admin.id,
            user_id=luis.id,
            cuadrilla_id=cuadrilla_ant.id,
            prioridad="P2",
            tipo_ubicacion="rural",
            tipo_mantenimiento="preventivo",
            subsistema="Movil Plantas Eléctricas",
            progreso=100,
            estado="finalizada",
            fecha_inicio=datetime(2026, 8, 8, 7, 0, 0),
            fecha_limite_sla=datetime(2026, 8, 9, 18, 0, 0),
            fecha_llegada_sitio=datetime(2026, 8, 8, 9, 0, 0),
            fecha_solucion=datetime(2026, 8, 8, 17, 0, 0),
            causa_falla="desgaste",
            observaciones_cierre="Mantenimiento preventivo de grupo electrógeno con cambio de filtros y alineación de microondas.",
            datos_formulario=json.dumps({
                "marca_planta": "Caterpillar Olympian",
                "kva": 30,
                "marca_motor": "Perkins 1104",
                "serial_motor": "PK998124",
                "marca_generador": "Leroy Somer",
                "serial_generador": "LS-55410",
                "horometro": 4120.5,
                "voltaje_bateria": 26.0,
                "galones_combustible": 55,
                "prueba_encendido": "Arranque correcto manual y automático en transferencia ATS."
            })
        )

        db.add_all([ot1, ot2, ot3, ot4, ot5])
        db.commit()

        # Evidencias Fotográficas para OT 4 (Barranquilla)
        print("[SEED] Creando evidencias fotográficas georreferenciadas...")
        ev1 = EvidenciaFotografica(
            ot_id=ot4.id,
            tipo="antes",
            url_imagen="https://images.unsplash.com/photo-1541888946425-d0fbb186f5f8?w=800",
            latitud=11.018254,
            longitud=-74.821420,
            fecha_hora_captura=datetime(2026, 8, 10, 9, 45, 0)
        )
        ev2 = EvidenciaFotografica(
            ot_id=ot4.id,
            tipo="durante",
            url_imagen="https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800",
            latitud=11.018270,
            longitud=-74.821415,
            fecha_hora_captura=datetime(2026, 8, 10, 13, 15, 0)
        )
        ev3 = EvidenciaFotografica(
            ot_id=ot4.id,
            tipo="despues",
            url_imagen="https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800",
            latitud=11.018260,
            longitud=-74.821410,
            fecha_hora_captura=datetime(2026, 8, 10, 16, 30, 0)
        )
        db.add_all([ev1, ev2, ev3])

        # Repuestos e Insumos
        print("[SEED] Creando insumos y repuestos utilizados...")
        reps = [
            RepuestoUtilizado(ot_id=ot4.id, nombre_item="Pintura Epóxica Balizamiento Naranja Aeronáutico", cantidad=2.0, unidad_medida="Galón"),
            RepuestoUtilizado(ot_id=ot4.id, nombre_item='Tornillería Galvanizada de Alta Resistencia A325 5/8" x 2"', cantidad=24.0, unidad_medida="Unidad"),
            RepuestoUtilizado(ot_id=ot4.id, nombre_item="Cartucho Soldadura Exotérmica Cadweld 90g", cantidad=4.0, unidad_medida="Unidad"),
            RepuestoUtilizado(ot_id=ot3.id, nombre_item="Gas Refrigerante Ecológico R410A", cantidad=3.5, unidad_medida="Kg"),
            RepuestoUtilizado(ot_id=ot3.id, nombre_item="Filtro Secador Deshidratador 3/8 Soldable", cantidad=2.0, unidad_medida="Unidad"),
        ]
        db.add_all(reps)

        # Bitácora de Avances
        print("[SEED] Creando bitácora de avances en campo...")
        avs = [
            Avance(ot_id=ot4.id, user_id=eliseo.id, descripcion="Llegada a sitio EB Riomar Industrial. Inspección de riesgos y charla de seguridad SST de 5 minutos.", porcentaje=20, fecha_reporte=datetime(2026, 8, 10, 9, 40, 0)),
            Avance(ot_id=ot4.id, user_id=eliseo.id, descripcion="Ascenso seguro con arnés dieléctrico y doble eslinga. Retorque de pernería en tramos 1 a 3.", porcentaje=60, fecha_reporte=datetime(2026, 8, 10, 13, 0, 0)),
            Avance(ot_id=ot4.id, user_id=eliseo.id, descripcion="Medición de SPT con telurómetro (3.8 Ohms) y aplicación de pintura de balizamiento terminada.", porcentaje=100, fecha_reporte=datetime(2026, 8, 10, 16, 35, 0)),
            Avance(ot_id=ot3.id, user_id=carlos.id, descripcion="Desplazamiento completado desde Montería hasta la EB Ronda del Sinú. Registro de llegada.", porcentaje=25, fecha_reporte=datetime(2026, 8, 14, 14, 20, 0)),
            Avance(ot_id=ot3.id, user_id=carlos.id, descripcion="Medición de presiones manométricas, limpieza de serpentín condensador y reemplazo de filtro secador.", porcentaje=65, fecha_reporte=datetime(2026, 8, 14, 16, 10, 0)),
        ]
        db.add_all(avs)

        # Sub-actividades de checklist
        print("[SEED] Creando sub-actividades de checklist...")
        acts = [
            ActividadOt(ot_id=ot1.id, nombre="Inspección visual de cableado de fuerza y control en planta Cummins", peso_porcentaje=25, progreso=25, estado="completada"),
            ActividadOt(ot_id=ot1.id, nombre="Prueba de aislamiento con megóhmetro en bobinado de generador Stamford", peso_porcentaje=35, progreso=0, estado="pendiente"),
            ActividadOt(ot_id=ot1.id, nombre="Sustitución y calibración de tarjeta reguladora AVR", peso_porcentaje=40, progreso=0, estado="pendiente"),
        ]
        db.add_all(acts)

        db.commit()
        print("[SUCCESS] Base de datos sembrada satisfactoriamente con todos los registros oficiales.")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error al sembrar base de datos: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

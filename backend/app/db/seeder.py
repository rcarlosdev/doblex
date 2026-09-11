import json
from datetime import datetime, timedelta
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.core.security import get_password_hash
from app.core.utils import now_utc
from app.models.user import User
from app.models.empleado import Empleado
from app.models.cuadrilla import Cuadrilla
from app.models.sitio import Sitio
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

        # 4. Sembrar las Órdenes de Trabajo adaptadas a formatos de campo WO y MP vinculadas a sitios reales
        from scripts.reset_and_seed_ots import seed_ots_for_session
        seed_ots_for_session(db, "Seeder Local")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error al sembrar base de datos: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

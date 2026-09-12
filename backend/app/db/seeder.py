import os
import sys
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

def seed_database(reset_ots: bool = True):
    """
    Puebla la base de datos con los perfiles operativos, cuadrillas, directorio de empleados
    y las 6 OTs tipificadas con sus evidencias fotográficas, repuestos, avances y formatos oficiales (WO, MP, 360).
    """
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Asegurar usuarios del sistema
        admin = db.query(User).filter(User.username == "admin.doblex").first()
        if not admin:
            print("[SEED] Creando usuarios principales del sistema...")
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
        else:
            adminis = db.query(User).filter(User.username == "adminis.doblex").first() or admin
            carlos = db.query(User).filter(User.username == "carlos.doblex").first() or admin
            luis = db.query(User).filter(User.username == "luis.doblex").first() or carlos
            jasmin = db.query(User).filter(User.username == "jasmin.doblex").first() or carlos
            eliseo = db.query(User).filter(User.username == "eliseo.doblex").first() or carlos

        # 2. Asegurar cuadrillas regionales
        cuadrilla_ant = db.query(Cuadrilla).filter(Cuadrilla.nombre.ilike("%Antioquia%")).first()
        if not cuadrilla_ant:
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
        else:
            cuadrilla_cho = db.query(Cuadrilla).filter(Cuadrilla.nombre.ilike("%Chocó%")).first() or cuadrilla_ant
            cuadrilla_cor = db.query(Cuadrilla).filter(Cuadrilla.nombre.ilike("%Córdoba%")).first() or cuadrilla_ant
            cuadrilla_atl = db.query(Cuadrilla).filter(Cuadrilla.nombre.ilike("%Atlántico%")).first() or cuadrilla_ant

        # 3. Asegurar directorio completo de empleados (11)
        if db.query(Empleado).count() < 6:
            print("[SEED] Creando directorio completo de empleados...")
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

        # 4. Sembrar las Órdenes de Trabajo adaptadas a formatos oficiales vigentes (WO, MP, 360)
        if reset_ots:
            from scripts.reset_and_seed_ots import seed_ots_for_session
            seed_ots_for_session(db, "Seeder Central")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error al sembrar base de datos: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database(reset_ots=True)

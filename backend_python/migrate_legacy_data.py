import sqlite3
import os
import sys
from datetime import datetime

# Rutas de las bases de datos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEGACY_DB_PATH = os.path.join(BASE_DIR, "backend", "database", "database.sqlite")
NEW_DB_PATH = os.path.join(BASE_DIR, "backend_python", "doblex.db")

def parse_dt(dt_str):
    if not dt_str:
        return None
    try:
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    except Exception:
        try:
            return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        except Exception:
            return None

def migrate_data():
    if not os.path.exists(LEGACY_DB_PATH):
        print(f"[ERROR] No se encontró la base de datos antigua en {LEGACY_DB_PATH}")
        sys.exit(1)

    print(f"[MIGRACIÓN] Conectando a BD antigua: {LEGACY_DB_PATH}")
    legacy_conn = sqlite3.connect(LEGACY_DB_PATH)
    legacy_conn.row_factory = sqlite3.Row
    legacy_cursor = legacy_conn.cursor()

    # Conectar con SQLAlchemy en el backend nuevo
    sys.path.insert(0, os.path.join(BASE_DIR, "backend_python"))
    from app.db.base import Base
    from app.db.session import engine, SessionLocal
    from app.models.user import User
    from app.models.cuadrilla import Cuadrilla
    from app.models.empleado import Empleado
    from app.models.ot import Ot
    from app.models.actividad_ot import ActividadOt
    from app.models.evidencia import EvidenciaFotografica
    from app.models.repuesto import RepuestoUtilizado
    from app.models.avance import Avance

    # Recrear tablas limpias en la base de datos nueva
    print("[MIGRACIÓN] Asegurando tablas en la base de datos nueva...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_db = SessionLocal()

    try:
        # 1. Migrar Usuarios
        print("\n[1/8] Migrando Usuarios...")
        users = legacy_cursor.execute("SELECT * FROM users").fetchall()
        for u in users:
            new_user = User(
                id=u["id"],
                name=u["name"],
                username=u["username"],
                email=u["email"],
                role=u["role"],
                password=u["password"],
                created_at=parse_dt(u["created_at"]),
                updated_at=parse_dt(u["updated_at"])
            )
            new_db.add(new_user)
        new_db.commit()
        print(f"  -> {len(users)} usuarios migrados.")

        # 2. Migrar Cuadrillas
        print("\n[2/8] Migrando Cuadrillas...")
        cuadrillas = legacy_cursor.execute("SELECT * FROM cuadrillas").fetchall()
        for c in cuadrillas:
            new_c = Cuadrilla(
                id=c["id"],
                nombre=c["nombre"],
                especialidad=c["especialidad"],
                lider_id=c["lider_id"],
                created_at=parse_dt(c["created_at"]),
                updated_at=parse_dt(c["updated_at"])
            )
            new_db.add(new_c)
        new_db.commit()
        print(f"  -> {len(cuadrillas)} cuadrillas migradas.")

        # 3. Migrar Empleados
        print("\n[3/8] Migrando Empleados...")
        empleados = legacy_cursor.execute("SELECT * FROM empleados").fetchall()
        for e in empleados:
            new_emp = Empleado(
                id=e["id"],
                documento=e["documento"],
                nombre=e["nombre"],
                cargo=e["cargo"],
                telefono=e["telefono"],
                email=e["email"],
                rol=e["rol"],
                cuadrilla_id=e["cuadrilla_id"],
                user_id=e["user_id"],
                estado=e["estado"],
                created_at=parse_dt(e["created_at"]),
                updated_at=parse_dt(e["updated_at"])
            )
            new_db.add(new_emp)
        new_db.commit()
        print(f"  -> {len(empleados)} empleados migrados.")

        # 4. Migrar Órdenes de Trabajo (OTs)
        print("\n[4/8] Migrando Órdenes de Trabajo (OTs)...")
        ots = legacy_cursor.execute("SELECT * FROM ots").fetchall()
        for ot in ots:
            new_ot = Ot(
                id=ot["id"],
                codigo=ot["codigo"],
                descripcion=ot["descripcion"],
                sitio=ot["sitio"],
                ubicacion=ot["ubicacion"],
                created_by=ot["created_by"],
                user_id=ot["user_id"],
                cuadrilla_id=ot["cuadrilla_id"],
                progreso=ot["progreso"],
                estado=ot["estado"],
                prioridad=ot["prioridad"],
                tipo_ubicacion=ot["tipo_ubicacion"],
                tipo_mantenimiento=ot["tipo_mantenimiento"],
                subsistema=ot["subsistema"],
                tipo_gasto=ot["tipo_gasto"],
                fecha_inicio=parse_dt(ot["fecha_inicio"]),
                fecha_limite_sla=parse_dt(ot["fecha_limite_sla"]),
                fecha_llegada_sitio=parse_dt(ot["fecha_llegada_sitio"]),
                fecha_solucion=parse_dt(ot["fecha_solucion"]),
                causa_falla=ot["causa_falla"],
                observaciones_cierre=ot["observaciones_cierre"],
                created_at=parse_dt(ot["created_at"]),
                updated_at=parse_dt(ot["updated_at"])
            )
            new_db.add(new_ot)
        new_db.commit()
        print(f"  -> {len(ots)} OTs migradas.")

        # 5. Migrar Evidencias Fotográficas
        print("\n[5/8] Migrando Evidencias Fotográficas...")
        evidencias = legacy_cursor.execute("SELECT * FROM evidencias_fotograficas").fetchall()
        for ev in evidencias:
            new_ev = EvidenciaFotografica(
                id=ev["id"],
                ot_id=ev["ot_id"],
                tipo=ev["tipo"],
                url_imagen=ev["url_imagen"],
                latitud=ev["latitud"],
                longitud=ev["longitud"],
                fecha_hora_captura=parse_dt(ev["fecha_hora_captura"]),
                created_at=parse_dt(ev["created_at"]),
                updated_at=parse_dt(ev["updated_at"])
            )
            new_db.add(new_ev)
        new_db.commit()
        print(f"  -> {len(evidencias)} evidencias fotográficas migradas con éxito.")

        # 6. Migrar Sub-actividades de OT
        print("\n[6/8] Migrando Sub-actividades de Checklist...")
        actividades = legacy_cursor.execute("SELECT * FROM actividades_ot").fetchall()
        for act in actividades:
            new_act = ActividadOt(
                id=act["id"],
                ot_id=act["ot_id"],
                nombre=act["nombre"],
                peso_porcentaje=act["peso_porcentaje"],
                progreso=act["progreso"],
                estado=act["estado"],
                created_at=parse_dt(act["created_at"]),
                updated_at=parse_dt(act["updated_at"])
            )
            new_db.add(new_act)
        new_db.commit()
        print(f"  -> {len(actividades)} sub-actividades migradas.")

        # 7. Migrar Repuestos / Insumos Utilizados
        print("\n[7/8] Migrando Insumos y Repuestos Utilizados...")
        repuestos = legacy_cursor.execute("SELECT * FROM repuestos_utilizados").fetchall()
        for rep in repuestos:
            new_rep = RepuestoUtilizado(
                id=rep["id"],
                ot_id=rep["ot_id"],
                nombre_item=rep["nombre_item"],
                cantidad=rep["cantidad"],
                unidad_medida=rep["unidad_medida"],
                created_at=parse_dt(rep["created_at"]),
                updated_at=parse_dt(rep["updated_at"])
            )
            new_db.add(new_rep)
        new_db.commit()
        print(f"  -> {len(repuestos)} repuestos/insumos migrados.")

        # 8. Migrar Historial de Avances en Campo
        print("\n[8/8] Migrando Historial de Avances de Campo (Bitácora)...")
        avances = legacy_cursor.execute("SELECT * FROM avances").fetchall()
        for av in avances:
            new_av = Avance(
                id=av["id"],
                ot_id=av["ot_id"],
                user_id=av["user_id"],
                descripcion=av["descripcion"],
                porcentaje=av["porcentaje"],
                fecha_reporte=parse_dt(av["fecha_reporte"]),
                created_at=parse_dt(av["created_at"]),
                updated_at=parse_dt(av["updated_at"])
            )
            new_db.add(new_av)
        new_db.commit()
        print(f"  -> {len(avances)} avances migrados.")

        print("\n=======================================================")
        print(" [SUCCESS] ¡Migración de datos antiguos completada al 100%!")
        print(f" Base de datos destino: {NEW_DB_PATH}")
        print("=======================================================\n")

    except Exception as e:
        new_db.rollback()
        print(f"\n[ERROR] Error durante la migración: {e}")
        raise
    finally:
        new_db.close()
        legacy_conn.close()

if __name__ == "__main__":
    migrate_data()

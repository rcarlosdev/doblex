"""
Script integral para:
1. Migrar la base de datos SQLite (doblex.db): agregar columnas faltantes en 'ots'.
2. Cargar los 1800+ sitios de 'docs/ARCHIVO FACTURACIÓN.xlsx' (primer pestaña 'Base de dato transporte').
3. Vincular OTs existentes con los sitios maestros correspondientes.
4. Sincronizar y aprovisionar la base de datos PostgreSQL en Docker (doblex_postgres_db) con el mismo esquema y datos.
"""
import os
import sys
import sqlite3
import openpyxl
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))

from app.db.base import Base
import app.models
from app.models.sitio import Sitio
from app.models.ot import Ot
from app.models.user import User
from app.models.cuadrilla import Cuadrilla
from app.models.empleado import Empleado

EXCEL_PATH = os.path.join(BASE_DIR, "docs", "ARCHIVO FACTURACIÓN.xlsx")
SQLITE_PATH = os.path.join(BASE_DIR, "backend", "doblex.db")
PG_URL = "postgresql+psycopg2://doblex_user:doblex_password@127.0.0.1:5432/doblex_smu"

def parse_float_safe(val):
    if val is None:
        return None, None
    if isinstance(val, (int, float)):
        return float(val), str(val)
    if isinstance(val, datetime):
        text_rep = f"{val.day}-{val.month}"
        return None, text_rep
    val_str = str(val).strip().replace(",", ".")
    if not val_str or val_str.lower() in ["#n/a", "#n/d", "nan", "null", "none", "0", "-", "--"]:
        if val_str == "0":
            return 0.0, "0"
        return None, None
    try:
        return float(val_str), str(val).strip()
    except (ValueError, TypeError):
        return None, str(val).strip()

def clean_str(val):
    if val is None:
        return None
    s = str(val).strip()
    if not s:
        return None
    s_lower = s.lower()
    if s_lower in ["#n/a", "#n/d", "#ref!", "#valor!", "#value!", "0", "-", "--", "none", "null", "n/a", "no aplica", "nan", "#div/0!", "#num!", "#name?"]:
        return None
    if "#n/a" in s_lower or "#n/d" in s_lower or "#ref!" in s_lower:
        return None
    return s

def clean_email(val):
    s = clean_str(val)
    if not s:
        return None
    s = s.lower().strip()
    if "@" not in s or "#" in s or " " in s:
        return None
    return s

def migrate_sqlite():
    print("\n--- [1/4] MIGRANDO ESQUEMA EN SQLITE (doblex.db) ---")
    conn = sqlite3.connect(SQLITE_PATH)
    cur = conn.cursor()

    cur.execute("PRAGMA table_info(ots)")
    existing_cols = {r[1] for r in cur.fetchall()}
    print(f"Columnas actuales en 'ots': {len(existing_cols)}")

    columns_to_add = [
        ("id_actividad", "VARCHAR(50)"),
        ("sitio_id", "INTEGER"),
        ("coordinador", "VARCHAR(150)"),
        ("categoria", "VARCHAR(50) DEFAULT 'normal'"),
        ("regional", "VARCHAR(50) DEFAULT 'R1'"),
        ("departamento", "VARCHAR(100)"),
        ("tipo_estacion", "VARCHAR(50) DEFAULT 'MOVIL'"),
        ("site_owner", "VARCHAR(150)"),
        ("tipo_actividad", "VARCHAR(50) DEFAULT 'correctivo'"),
        ("datos_formulario", "TEXT")
    ]

    added = 0
    for col_name, col_def in columns_to_add:
        if col_name not in existing_cols:
            print(f"  + Agregando columna faltante: ots.{col_name} ({col_def})")
            cur.execute(f"ALTER TABLE ots ADD COLUMN {col_name} {col_def}")
            added += 1

    # Actualizar valores por defecto si eran nulos
    cur.execute("""
        UPDATE ots 
        SET id_actividad = 'ACT-2026-' || (100000 + id) 
        WHERE id_actividad IS NULL OR id_actividad = ''
    """)
    cur.execute("""
        UPDATE ots 
        SET tipo_actividad = COALESCE(tipo_mantenimiento, 'correctivo') 
        WHERE tipo_actividad IS NULL OR tipo_actividad = ''
    """)
    cur.execute("""
        UPDATE ots 
        SET categoria = 'normal' 
        WHERE categoria IS NULL OR categoria = ''
    """)
    cur.execute("""
        UPDATE ots 
        SET regional = 'R1' 
        WHERE regional IS NULL OR regional = ''
    """)
    cur.execute("""
        UPDATE ots 
        SET tipo_estacion = 'MOVIL' 
        WHERE tipo_estacion IS NULL OR tipo_estacion = ''
    """)

    conn.commit()
    conn.close()
    print(f"  -> Migración SQLite completada. ({added} columnas agregadas)")

def load_sitios_to_db(db_session, db_name="SQLite"):
    print(f"\n--- [CARGA DE SITIOS EN {db_name.upper()}] ---")
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    sheet_name = wb.sheetnames[0]
    ws = wb[sheet_name]
    print(f"  Leyendo pestaña '{sheet_name}' (Total filas en hoja: {ws.max_row})")

    existing_sitios = {s.nombre: s for s in db_session.query(Sitio).all()}
    print(f"  Sitios pre-existentes en {db_name}: {len(existing_sitios)}")

    inserted = 0
    updated = 0
    batch_size = 300
    current_batch = 0

    for r in range(20, ws.max_row + 1):
        sitio_raw = ws.cell(r, 2).value
        if not sitio_raw or not str(sitio_raw).strip():
            continue

        nombre = str(sitio_raw).strip().upper()
        zona = clean_str(ws.cell(r, 1).value)
        if zona:
            zona = zona.upper()

        cod_transp = clean_str(ws.cell(r, 3).value)
        km_num, km_txt = parse_float_safe(ws.cell(r, 4).value)
        ciudad_base = clean_str(ws.cell(r, 5).value)
        if ciudad_base:
            ciudad_base = ciudad_base.upper()

        transp_esp = clean_str(ws.cell(r, 6).value)
        zona_tecnica = clean_str(ws.cell(r, 7).value)
        new_so = clean_str(ws.cell(r, 8).value)
        jefe_zona = clean_str(ws.cell(r, 9).value)
        ing_soporte = clean_str(ws.cell(r, 10).value)
        estructura = clean_str(ws.cell(r, 11).value)
        alt_num, alt_txt = parse_float_safe(ws.cell(r, 12).value)
        facturadora = clean_str(ws.cell(r, 13).value)
        municipio = clean_str(ws.cell(r, 14).value)
        ubicacion = clean_str(ws.cell(r, 15).value)

        correo_so = clean_email(ws.cell(r, 16).value)
        correo_jz = clean_email(ws.cell(r, 17).value)
        correo_ing = clean_email(ws.cell(r, 18).value)

        if nombre in existing_sitios:
            s = existing_sitios[nombre]
            s.zona = zona
            s.zona_tecnica = zona_tecnica
            s.ciudad_base = ciudad_base
            s.municipio = municipio
            s.ubicacion = ubicacion
            s.codigo_transporte_lpu = cod_transp
            s.km = km_num
            s.km_texto = km_txt
            s.transporte_especial = transp_esp
            s.estructura = estructura
            s.altura_estructura = alt_num
            s.altura_estructura_texto = alt_txt
            s.supervisor_operativo = new_so
            s.correo_so = correo_so
            s.jefe_zona = jefe_zona
            s.correo_jefe_zona = correo_jz
            s.ingeniero_soporte = ing_soporte
            s.correo_ing_soporte = correo_ing
            s.facturadora = facturadora
            updated += 1
        else:
            nuevo = Sitio(
                nombre=nombre,
                zona=zona,
                zona_tecnica=zona_tecnica,
                ciudad_base=ciudad_base,
                municipio=municipio,
                ubicacion=ubicacion,
                codigo_transporte_lpu=cod_transp,
                km=km_num,
                km_texto=km_txt,
                transporte_especial=transp_esp,
                estructura=estructura,
                altura_estructura=alt_num,
                altura_estructura_texto=alt_txt,
                supervisor_operativo=new_so,
                correo_so=correo_so,
                jefe_zona=jefe_zona,
                correo_jefe_zona=correo_jz,
                ingeniero_soporte=ing_soporte,
                correo_ing_soporte=correo_ing,
                facturadora=facturadora,
                estado="activo"
            )
            db_session.add(nuevo)
            existing_sitios[nombre] = nuevo
            inserted += 1

        current_batch += 1
        if current_batch >= batch_size:
            db_session.commit()
            current_batch = 0

    db_session.commit()
    print(f"  -> {inserted} sitios insertados nuevos en {db_name}.")
    print(f"  -> {updated} sitios actualizados en {db_name}.")
    total = db_session.query(Sitio).count()
    print(f"  -> Total de sitios en {db_name}: {total}")

    # Vincular OTs
    ots = db_session.query(Ot).all()
    vinculadas = 0
    for ot in ots:
        if not ot.sitio:
            continue
        ot_sitio_upper = ot.sitio.upper().strip()
        if ot_sitio_upper in existing_sitios:
            ot.sitio_id = existing_sitios[ot_sitio_upper].id
            vinculadas += 1
            continue
        parts = ot_sitio_upper.split(" - ")
        nombre_base = parts[0].strip()
        if nombre_base in existing_sitios:
            ot.sitio_id = existing_sitios[nombre_base].id
            vinculadas += 1
            continue
    db_session.commit()
    print(f"  -> {vinculadas} OTs vinculadas con su sitio en {db_name}.")

def sync_to_postgres():
    print("\n--- [3/4] MIGRANDO Y SINCRONIZANDO POSTGRESQL (DOCKER) ---")
    try:
        pg_engine = create_engine(PG_URL, echo=False)
        PgSession = sessionmaker(bind=pg_engine)

        # 1. Asegurar todas las tablas SQLAlchemy en Postgres
        print("  Recreando esquema limpio en PostgreSQL...")
        import psycopg2
        conn = psycopg2.connect("postgresql://doblex_user:doblex_password@127.0.0.1:5432/doblex_smu")
        cur = conn.cursor()
        cur.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
        conn.commit()
        conn.close()

        Base.metadata.create_all(bind=pg_engine)
        pg_db = PgSession()

        # 2. Sincronizar datos base de SQLite a Postgres (Usuarios, Cuadrillas, Empleados, OTs)
        sq_engine = create_engine(f"sqlite:///{SQLITE_PATH}")
        SqSession = sessionmaker(bind=sq_engine)
        sq_db = SqSession()

        # Sincronizar Usuarios
        if pg_db.query(User).count() == 0:
            print("  Copiando usuarios de SQLite a Postgres...")
            for u in sq_db.query(User).all():
                pg_db.merge(User(
                    id=u.id, name=u.name, username=u.username, email=u.email,
                    role=u.role, password=u.password, created_at=u.created_at, updated_at=u.updated_at
                ))
            pg_db.commit()

        # Sincronizar Cuadrillas
        if pg_db.query(Cuadrilla).count() == 0:
            print("  Copiando cuadrillas de SQLite a Postgres...")
            for c in sq_db.query(Cuadrilla).all():
                pg_db.merge(Cuadrilla(
                    id=c.id, nombre=c.nombre, especialidad=c.especialidad,
                    lider_id=c.lider_id, created_at=c.created_at, updated_at=c.updated_at
                ))
            pg_db.commit()

        # Sincronizar Empleados
        if pg_db.query(Empleado).count() == 0:
            print("  Copiando empleados de SQLite a Postgres...")
            for e in sq_db.query(Empleado).all():
                pg_db.merge(Empleado(
                    id=e.id, documento=e.documento, nombre=e.nombre, cargo=e.cargo,
                    telefono=e.telefono, email=e.email, rol=e.rol,
                    cuadrilla_id=e.cuadrilla_id, user_id=e.user_id,
                    created_at=e.created_at, updated_at=e.updated_at
                ))
            pg_db.commit()

        # 1. Cargar Sitios en Postgres primero (para que las FKs de OTs resuelvan correctamente)
        load_sitios_to_db(pg_db, "PostgreSQL")

        # 2. Sincronizar OTs de SQLite a Postgres
        if pg_db.query(Ot).count() == 0:
            print("  Copiando OTs de SQLite a Postgres...")
            for o in sq_db.query(Ot).all():
                pg_db.merge(Ot(
                    id=o.id, codigo=o.codigo, id_actividad=o.id_actividad, descripcion=o.descripcion,
                    sitio=o.sitio, sitio_id=o.sitio_id, ubicacion=o.ubicacion, created_by=o.created_by,
                    user_id=o.user_id, cuadrilla_id=o.cuadrilla_id, coordinador=o.coordinador,
                    progreso=o.progreso, estado=o.estado, prioridad=o.prioridad,
                    tipo_ubicacion=o.tipo_ubicacion, categoria=o.categoria, regional=o.regional,
                    departamento=o.departamento, tipo_estacion=o.tipo_estacion, site_owner=o.site_owner,
                    tipo_mantenimiento=o.tipo_mantenimiento, tipo_actividad=o.tipo_actividad,
                    subsistema=o.subsistema, tipo_gasto=o.tipo_gasto, datos_formulario=o.datos_formulario,
                    fecha_inicio=o.fecha_inicio, fecha_limite_sla=o.fecha_limite_sla,
                    fecha_llegada_sitio=o.fecha_llegada_sitio, fecha_solucion=o.fecha_solucion,
                    causa_falla=o.causa_falla, observaciones_cierre=o.observaciones_cierre,
                    created_at=o.created_at, updated_at=o.updated_at
                ))
            pg_db.commit()

        pg_db.close()
        sq_db.close()
        print("  -> PostgreSQL aprovisionado y sincronizado exitosamente.")

    except Exception as ex:
        print(f"  [AVISO] No se pudo sincronizar PostgreSQL: {ex}")

def main():
    print("==================================================================")
    print(" MIGRACIÓN Y CARGA DE BASE DE SITIOS (ARCHIVO FACTURACIÓN.xlsx)")
    print("==================================================================")

    # 1. Migrar esquema SQLite (doblex.db)
    migrate_sqlite()

    # 2. Cargar sitios en SQLite
    from app.db.session import SessionLocal
    sq_session = SessionLocal()
    try:
        load_sitios_to_db(sq_session, "SQLite (doblex.db)")
    finally:
        sq_session.close()

    # 3. Sincronizar Postgres en Docker
    sync_to_postgres()

    print("\n==================================================================")
    print(" ¡PROCESO FINALIZADO EXITOSAMENTE!")
    print("==================================================================")

if __name__ == "__main__":
    main()

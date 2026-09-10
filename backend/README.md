# Doblex SMU - Backend en Python (FastAPI)

Este backend sustituye la implementación previa en Laravel, implementando toda la lógica de negocio, autenticación, cálculo de SLA para OTs y gestión de cuadrillas/empleados, además de añadir capacidades avanzadas para **exportes (Excel, Word, PDF)** e **importes de datos**.

---

## 🚀 Requisitos Previos

- **Python 3.11+** (probado en Python 3.13)
- Gestor de paquetes `pip`

---

## 📦 Instalación y Configuración

1. **Crear y activar un entorno virtual (recomendado):**
   ```bash
   python -m venv .venv
   # En Windows:
   .venv\Scripts\activate
   # En Linux/Mac:
   source .venv/bin/activate
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuración de Variables de Entorno (`.env`):**
   Copia el archivo de ejemplo si no existe:
   ```bash
   copy .env.example .env
   ```
   *Por defecto, utiliza SQLite local (`sqlite:///./doblex.db`). Si deseas conectar con PostgreSQL, cambia `DATABASE_URL`.*

4. **Inicializar y Sembrar la Base de Datos:**
   Ejecuta el seeder para crear las tablas y los usuarios de prueba:
   ```bash
   python -m app.db.seeder
   ```

5. **Iniciar el Servidor de Desarrollo:**
   ```bash
   python run.py
   # O directamente con uvicorn:
   uvicorn app.main:app --reload --port 8000
   ```

---

## 🌐 Documentación Interactiva (Swagger / OpenAPI)

Una vez iniciado el servidor, accede a:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔐 Credenciales de Prueba

| Perfil | Username | Password | Rol |
| :--- | :--- | :--- | :--- |
| **Administrador** | `admin.doblex` | `admin123` | `admin` |
| **Administrativo** | `adminis.doblex` | `adminis123` | `administrativo` |
| **Operativo (Antioquia)** | `carlos.doblex` | `operador123` | `operativo` |
| **Operativo (Córdoba)** | `luis.doblex` | `operador123` | `operativo` |
| **Operativo (Chocó)** | `jasmin.doblex` | `operador123` | `operativo` |
| **Operativo (Atlántico)** | `eliseo.doblex` | `operador123` | `operativo` |

---

## 📄 Exportaciones e Importaciones

- `GET /api/ots/export/excel`: Descarga el listado consolidado de OTs en archivo Excel (`.xlsx`).
- `GET /api/ots/{id}/export/word`: Descarga informe técnico individual de la OT en Word (`.docx`).
- `GET /api/ots/{id}/export/pdf`: Descarga informe técnico de la OT en PDF (`.pdf`).
- `POST /api/ots/import/excel`: Importación y validación masiva de planillas Excel.

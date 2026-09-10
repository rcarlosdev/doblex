# SMU DOBLEX - Sistema de Gestión de Obra Civil

Este repositorio contiene la plataforma integral para el **Sistema de Gestión de Obra Civil y Mantenimiento de Infraestructura (SMU)** de Doblex S.A.S. Está estructurado bajo una arquitectura moderna y desacoplada con backend en **FastAPI (Python 3.13)**, frontend SPA en **Vue.js 3 (Vite)** y soporte para bases de datos relacionales (**SQLite** para desarrollo ágil y **PostgreSQL** para producción).

---

## Estructura del Proyecto

* `/backend` - API REST en FastAPI + SQLAlchemy + Pydantic V2 + JWT + Exportadores (Excel, Word, PDF).
* `/frontend` - Aplicación SPA reactiva en Vue 3 + Vite + Tailwind/CSS + Axios + Pinia.
* `docker-compose.yml` - Orquestación de Base de Datos PostgreSQL local.
* `DESARROLLO.md` - Guía técnica integral para desarrolladores.

---

## Requisitos Previos

Asegúrate de tener instalados los siguientes componentes:
1. **Python 3.11+** (recomendado Python 3.13).
2. **Node.js 20+** y **npm** (para el frontend).
3. **Docker Desktop** (opcional, si deseas ejecutar PostgreSQL local mediante contenedores).

---

## Paso a Paso: Inicio Rápido en Desarrollo

### Paso 1: Levantar el Backend (FastAPI en Python)

1. Dirígete a la carpeta del backend:
   ```bash
   cd backend
   ```

2. Activa el entorno virtual ya configurado:
   * **Windows (PowerShell):**
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   * **Linux / Mac:**
     ```bash
     source .venv/bin/activate
     ```

3. *(Opcional)* Si necesitas inicializar o sembrar la base de datos con los perfiles y OTs de prueba:
   ```bash
   python -m app.db.seeder
   ```

4. Inicia el servidor de desarrollo:
   ```bash
   python run.py
   # O directamente con Uvicorn:
   uvicorn app.main:app --reload --port 8000
   ```
   *El backend estará escuchando en `http://localhost:8000` con documentación interactiva en `http://localhost:8000/docs`.*

---

### Paso 2: Levantar el Frontend (Vue.js + Vite)

1. En una nueva terminal, ve al directorio del frontend:
   ```bash
   cd frontend
   ```

2. Instala dependencias si es la primera vez:
   ```bash
   npm install
   ```

3. Inicia el servidor de desarrollo de Vite:
   ```bash
   npm run dev
   ```
   *El frontend estará disponible en `http://localhost:5173`.*

---

## Credenciales de Acceso (Entorno Local)

Para acceder a la plataforma web (cargadas automáticamente mediante el seeder), puedes utilizar cualquiera de los siguientes perfiles:

| Perfil / Rol | Nombre / Empleado | Username | Contraseña | Cargo / Región |
| :--- | :--- | :--- | :--- | :--- |
| **Administrador** (`admin`) | Admin General | `admin.doblex` | `admin123` | Director General de Obra (Gestión total) |
| **Administrativo** (`administrativo`) | Auxiliar Técnico | `adminis.doblex` | `adminis123` | Asistente Administrativo de Campo |
| **Operativo** (`operativo`) | Ing. Carlos Pérez | `carlos.doblex` | `operador123` | Ingeniero Residente (Antioquia & Urabá) |
| **Operativo** (`operativo`) | Ing. Luis Martínez | `luis.doblex` | `operador123` | Ing. Energía y Climatización (Córdoba) |
| **Operativo** (`operativo`) | Jasmin Ariel Mosquera | `jasmin.doblex` | `operador123` | Técnico Electromecánico (Chocó) |
| **Operativo** (`operativo`) | Eliseo Smith Granados | `eliseo.doblex` | `operador123` | Técnico Electricista (Atlántico) |

---

## Funcionalidades Destacadas del Backend

* **Cálculo Automático de SLA:** Matriz paramétrica basada en prioridad (`P1`, `P2`, `P3`) y tipo de ubicación (`urbana`, `rural`).
* **Auditoría y Cierre Técnico:** Cierre estricto que exige las 3 evidencias fotográficas obligatorias (`antes`, `durante`, `despues`), causa de falla y registro de insumos/repuestos utilizados.
* **Control de Avance Acumulado:** Reportes diarios en campo con validación de límites (no permite superar el 100%).
* **Exportaciones al Vuelo:**
  * Consolidado de OTs en **Excel** (`GET /api/ots/export/excel`).
  * Informe técnico en **Word** (`GET /api/ots/{id}/export/word`).
  * Reporte formal en **PDF** (`GET /api/ots/{id}/export/pdf`).
* **Importación Masiva:** Validación y carga masiva de planillas Excel (`POST /api/ots/import/excel`).

---

## Pruebas Automatizadas

El backend incluye una suite completa de pruebas unitarias y de integración:

```bash
cd backend
.\.venv\Scripts\python tests_integration.py
.\.venv\Scripts\python tests_security.py
```
*(Valida autenticación, filtros por rol, SLA, estados, evidencias, avances y generación de reportes en menos de 1 segundo).*

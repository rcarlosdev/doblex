# Guía de Contribución y Configuración de Entorno - SMU DOBLEX

Esta guía detalla los requisitos tecnológicos, el proceso para ejecutar el proyecto de forma local y las directrices obligatorias para contribuir al desarrollo del **Sistema de Gestión de Obra Civil (SMU)**.

---

## 1. Tecnologías Requeridas y Entorno de Desarrollo

Para trabajar en este proyecto, tu máquina local debe contar con las siguientes tecnologías instaladas:

| Tecnología / Herramienta | Versión Requerida | Propósito en el Proyecto |
| :--- | :---: | :--- |
| **Python** | `v3.11` o superior (Recomendado `v3.13`) | Entorno del Backend FastAPI API |
| **Node.js** | `v20.0.0` o superior | Entorno de ejecución para la SPA de Frontend |
| **npm** | `v10.0.0` o superior | Gestor de paquetes de JavaScript |
| **Docker Desktop** | `v25.0` o superior (Opcional) | Contenedores locales (Base de Datos PostgreSQL) |
| **Git** | Cualquier versión estable | Control de versiones |

### Editor Recomendado
Se recomienda el uso de **Visual Studio Code** o **Antigravity IDE** con las siguientes extensiones:
* **Vue - Official (Volar):** Soporte de sintaxis y tipado para Vue 3.
* **Python (Microsoft):** Inteligencia de código, navegación y soporte para entornos virtuales.
* **Pylance / Pyrefly:** Análisis estático y autocompletado para Python y Pydantic.
* **EditorConfig para VS Code:** Consistencia en fin de línea y tabulación.

---

## 2. Configuración Inicial (Paso a Paso)

Sigue estos pasos para descargar, configurar y ejecutar el proyecto por primera vez:

### Paso 1: Obtener el Proyecto
Clona el repositorio en tu espacio de trabajo local:
```bash
git clone <URL_DEL_REPOSITORIO> DOBLEX
cd DOBLEX
```

### Paso 2: Aprovisionar Base de Datos
* **Opción A (SQLite - Por defecto para desarrollo ágil):** No requiere configuración previa; se autogenera en `backend_python/doblex.db`.
* **Opción B (PostgreSQL con Docker):**
  1. Asegúrate de tener Docker Desktop iniciado.
  2. Desde la raíz de la carpeta `DOBLEX`:
     ```bash
     docker-compose up -d
     ```
  3. Descomenta la línea de conexión PostgreSQL en `backend_python/.env`.

---

### Paso 3: Configurar y Correr el Backend (FastAPI en Python)

1. Navega a la carpeta del backend:
   ```bash
   cd backend_python
   ```

2. Activa el entorno virtual (`.venv`):
   * **Windows (PowerShell):**
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   * **Linux / Mac:**
     ```bash
     source .venv/bin/activate
     ```

3. Instala las dependencias (si configuras una máquina nueva):
   ```bash
   pip install -r requirements.txt
   ```

4. Asegúrate de tener el archivo `.env` configurado:
   ```bash
   # En Windows:
   copy .env.example .env
   # En Linux/Mac:
   cp .env.example .env
   ```

5. Inicializa y puebla la base de datos con los perfiles y OTs de prueba:
   ```bash
   python -m app.db.seeder
   ```

6. Inicia el servidor API local:
   ```bash
   python run.py
   # O directamente con Uvicorn:
   uvicorn app.main:app --reload --port 8000
   ```
   *El backend estará accesible en `http://localhost:8000` con documentación interactiva en `http://localhost:8000/docs`.*

---

### Paso 4: Configurar y Correr el Frontend (Vue.js + Vite)

1. Abre una nueva terminal y navega a la carpeta del frontend:
   ```bash
   cd frontend
   ```

2. Asegura el archivo de entorno `.env`:
   ```env
   VITE_API_URL=http://localhost:8000
   ```

3. Instala las dependencias de Node:
   ```bash
   npm install
   ```

4. Inicia el servidor de desarrollo de Vite:
   ```bash
   npm run dev
   ```
   *La aplicación frontend estará disponible en `http://localhost:5173`.*

---

## 3. Flujo de Trabajo y Git (Workflow de Contribución)

Para mantener la estabilidad de las ramas principales, aplicamos un flujo de trabajo estructurado:

```text
  main (Producción)
    ▲
    │ (Combinación tras validación final en UAT)
  staging (Pruebas / Pre-producción)
    ▲
    │ (Pull Requests aprobados)
  feature/mi-funcionalidad (Desarrollo de módulos)
```

### Reglas para Ramas:
* **`main`:** Contiene únicamente código estable desplegado en producción. Nadie hace commits directos aquí.
* **`staging`:** Entorno de pruebas de integración y aceptación del usuario (UAT).
* **`feature/*`:** Ramas de desarrollo para nuevos módulos o tareas (ej: `feature/exportacion-reportes-excel`, `feature/cierre-tecnico-ot`). Se crean a partir de `staging`.
* **`hotfix/*`:** Ramas para corregir fallos críticos directamente en producción. Se crean desde `main` y se combinan a `main` y `staging` de inmediato.

### Proceso de Contribución:
1. Crea tu rama de trabajo local desde `staging`:
   ```bash
   git checkout staging
   git pull origin staging
   git checkout -b feature/nueva-funcionalidad
   ```
2. Realiza los desarrollos correspondientes siguiendo las pautas de estilo.
3. **Validación Obligatoria antes de enviar PR:**
   * **Backend:** Ejecuta la suite de pruebas automatizadas y de seguridad:
     ```bash
     cd backend_python
     .\.venv\Scripts\python tests_integration.py
     .\.venv\Scripts\python tests_security.py
     ```
     *(Todas las pruebas deben finalizar con `OK`).*
   * **Frontend:** Ejecuta el build de Vite para descartar errores de sintaxis y tipos:
     ```bash
     cd frontend
     npm run build
     ```
4. Sube la rama y crea un Pull Request (PR) apuntando a `staging`.
5. El PR deberá ser revisado y aprobado por otro miembro del equipo antes de ser integrado.

---

## 4. Normas de Estilo y Buenas Prácticas (Obligatorias)

### 4.1. Idioma
* **Español Obligatorio:** Todo el desarrollo (nombres de tablas, columnas en base de datos, nombres de clases, funciones, variables, archivos, commits de Git y comentarios de código) debe realizarse en **español**.
  * *Bien:* `class Ot`, `def obtener_ordenes()`, `codigo_ot`
  * *Mal:* `class WorkOrder`, `def get_orders()`, `order_code`

### 4.2. Seguridad y Buenas Prácticas
* **SQLAlchemy ORM:** Prohibido realizar consultas crudas sin parametrizar. Usa siempre el ORM de SQLAlchemy para prevenir inyecciones SQL.
* **Esquemas Pydantic V2:** Todo endpoint que reciba o devuelva datos debe utilizar modelos Pydantic estrictos para tipado y validación de esquemas.
* **Manejo de Errores Estandarizado:** Toda respuesta de error debe formularse con `{ "status": "error", "message": "..." }` para mantener total compatibilidad con la interfaz de usuario.
* **Generación de Archivos en Memoria:** Los exportes de Excel, Word y PDF deben generarse utilizando buffers en memoria (`io.BytesIO`) y enviarse mediante `StreamingResponse` para optimizar el consumo de recursos en el servidor.

### 4.3. Estilo de Commits (Commit Semántico)
Utiliza mensajes descriptivos con el siguiente formato:
* `feat: ...` para nuevas funcionalidades (ej. `feat: agregar exporte en excel de ordenes de trabajo`).
* `fix: ...` para corrección de bugs (ej. `fix: corregir validacion de evidencias obligatorias en cierre de ot`).
* `docs: ...` para cambios puramente en documentación (ej. `docs: actualizar guia de contribucion`).
* `style: ...` para cambios de formato visual, CSS o linter (ej. `style: ajustar alineacion en modal de auditoria`).
* `test: ...` para agregar o actualizar pruebas unitarias/integración.

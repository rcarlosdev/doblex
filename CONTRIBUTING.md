# Guía de Contribución y Configuración de Entorno - SMU DOBLEX

Esta guía detalla los requisitos tecnológicos, el proceso para ejecutar el proyecto de forma local y las directrices obligatorias para contribuir al desarrollo del **Sistema de Gestión de Obra Civil (SMU)**.

---

## 1. Tecnologías Requeridas y Entorno de Desarrollo

Para trabajar en este proyecto, tu máquina local debe contar con las siguientes tecnologías instaladas:

| Tecnología / Herramienta | Versión Requerida | Propósito en el Proyecto |
| :--- | :---: | :--- |
| **Docker Desktop** | `v29.0` o superior | Contenedores locales (Base de Datos PostgreSQL) |
| **Node.js** | `v24.0.0` o superior | Entorno de ejecución para la SPA de Frontend |
| **npm** | `v11.0.0` o superior | Gestor de paquetes de JavaScript |
| **PHP** | `v8.3.0` o superior | Entorno del Backend Laravel API (incluido en Laragon) |
| **Composer** | `v2.9.0` o superior | Gestor de dependencias de PHP (incluido en Laragon) |
| **Git** | Cualquier versión estable | Control de versiones |

### Editor Recomendado
Se recomienda el uso de **Visual Studio Code** con las siguientes extensiones:
* **Volar** (Soporte oficial para Vue 3).
* **PHP Intelephense** (Autocompletado e inteligencia de código PHP).
* **EditorConfig para VS Code** (Para mantener la consistencia de fin de línea y tabuladores).

---

## 2. Configuración Inicial (Paso a Paso)

Sigue estos pasos para descargar, configurar y ejecutar el proyecto por primera vez:

### Paso 1: Obtener el Proyecto
Clona el repositorio en tu espacio de trabajo local (si estás en Laragon, se sugiere clonarlo dentro de la carpeta `C:/laragon/www/` o tu carpeta de desarrollo habitual):
```bash
git clone <URL_DEL_REPOSITORIO> DOBLEX
cd DOBLEX
```

### Paso 2: Aprovisionar Base de Datos (Docker)
1. Asegúrate de tener **Docker Desktop** abierto.
2. Desde la raíz de la carpeta `DOBLEX`, levanta el contenedor de PostgreSQL en segundo plano:
   ```bash
   docker-compose up -d
   ```
3. Verifica que esté corriendo en el puerto estándar `5432`:
   ```bash
   docker ps
   ```

### Paso 3: Configurar y Correr el Backend (Laravel)
1. Navega a la carpeta del backend:
   ```bash
   cd backend
   ```
2. Instala las dependencias de Composer. Si usas PHP y Composer de Laragon, ejecuta:
   ```bash
   & "C:\laragon\bin\php\php-8.3.30-Win32-vs16-x64\php.exe" "C:\laragon\bin\composer\composer.phar" install
   ```
3. Crea tu archivo de variables de entorno copiando el ejemplo:
   ```bash
   copy .env.example .env
   ```
4. Genera la llave de la aplicación:
   ```bash
   & "C:\laragon\bin\php\php-8.3.30-Win32-vs16-x64\php.exe" artisan key:generate
   ```
5. Asegura que la configuración de la base de datos en tu `.env` coincida con la de Docker:
   ```env
   DB_CONNECTION=pgsql
   DB_HOST=127.0.0.1
   DB_PORT=5432
   DB_DATABASE=doblex_smu
   DB_USERNAME=doblex_user
   DB_PASSWORD=doblex_password
   ```
6. Ejecuta las migraciones de la base de datos:
   ```bash
   & "C:\laragon\bin\php\php-8.3.30-Win32-vs16-x64\php.exe" artisan migrate
   ```
7. Enciende el servidor API local:
   ```bash
   & "C:\laragon\bin\php\php-8.3.30-Win32-vs16-x64\php.exe" artisan serve
   ```
   *El backend estará accesible en `http://localhost:8000`.*

### Paso 4: Configurar y Correr el Frontend (Vue.js)
1. Abre una nueva terminal y navega a la carpeta del frontend:
   ```bash
   cd frontend
   ```
2. Instala las dependencias de Node:
   ```bash
   npm install
   ```
3. Inicia el servidor de desarrollo de Vite:
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
* **`staging`:** Entorno de pruebas de aceptación del usuario (UAT).
* **`feature/*`:** Ramas de desarrollo para nuevos módulos o tareas (ej: `feature/crud-ordenes-trabajo`, `feature/configuracion-logistica`). Se crean a partir de `staging`.
* **`hotfix/*`:** Ramas para corregir fallos críticos directamente en producción. Se crean desde `main` y se combinan a `main` y `staging` de inmediato.

### Proceso de Contribución:
1. Crea tu rama de trabajo local desde `staging`:
   ```bash
   git checkout staging
   git pull origin staging
   git checkout -b feature/nueva-funcionalidad
   ```
2. Realiza los desarrollos correspondientes siguiendo las pautas de estilo.
3. Antes de subir tus cambios, verifica que todo compile y pase las validaciones:
   * **Backend:** Ejecuta `php artisan test` (si existen pruebas unitarias).
   * **Frontend:** Ejecuta `npm run build` para asegurar que el empaquetado de producción de Vite no arroje errores de sintaxis.
4. Sube la rama y crea un Pull Request (PR) apuntando a la rama `staging`.
5. El PR deberá ser revisado y aprobado por otro miembro del equipo antes de ser integrado.

---

## 4. Normas de Estilo y Buenas Prácticas (Obligatorias)

### 4.1. Idioma
* **Español Obligatorio:** Todo el desarrollo (nombres de tablas, columnas en base de datos, nombres de clases, funciones, variables, archivos, commits de Git y comentarios de código) debe realizarse en **español**.
  * *Bien:* `class OrdenTrabajoController`, `$idUsuario`, `public function obtenerOrdenes()`
  * *Mal:* `class WorkOrderController`, `$userId`, `public function getOrders()`

### 4.2. Seguridad
* **Consultas Parametrizadas:** Está prohibido concatenar variables del usuario directamente en sentencias SQL. Utiliza siempre el Query Builder o Eloquent de Laravel para prevenir inyección SQL.
* **Manejo de Excepciones:** Encapsula las operaciones sensibles (peticiones API, transacciones DB, operaciones de archivos) dentro de bloques `try/catch`. Registra los errores en los logs usando `Log::error(...)` sin exponer trazas técnicas al cliente.

### 4.3. Estilo de Commits (Commit Semántico)
Utiliza mensajes descriptivos con el siguiente formato:
* `feat: ...` para nuevas funcionalidades (ej. `feat: agregar formulario de creacion de OT`).
* `fix: ...` para corrección de bugs (ej. `fix: corregir redireccion despues de iniciar sesion`).
* `docs: ...` para cambios puramente en documentación (ej. `docs: actualizar guia de contribucion`).
* `style: ...` para cambios de formato visual, CSS o linter (ej. `style: ajustar padding en boton de login`).

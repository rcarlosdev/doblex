# SMU DOBLEX - Sistema de Gestión de Obra Civil

Este proyecto contiene la arquitectura base para el **Sistema de Gestión de Obra Civil (SMU)**. Está estructurado en un backend API desarrollado con Laravel, un frontend SPA reactivo desarrollado con Vue.js (Vite), y un entorno de base de datos relacional PostgreSQL levantado mediante Docker.

---

## Estructura del Proyecto

* `/backend` - API REST en Laravel 11 + Sanctum + PostgreSQL.
* `/frontend` - Aplicación SPA en Vue 3 + Vite + Axios + Pinia.
* `docker-compose.yml` - Orquestación de la Base de Datos PostgreSQL local.

---

## Requisitos Previos

Asegúrate de tener instalados los siguientes componentes:
1. **Docker Desktop** (para la base de datos).
2. **Node.js** v24+ y **npm** v11+ (para el frontend).
3. **Laragon** o PHP 8.2+ local y Composer (para el backend).

---

## Paso a Paso: Inicio Rápido en Desarrollo

Sigue estos 3 sencillos pasos para levantar todo el entorno localmente:

### Paso 1: Levantar la Base de Datos (Docker)
En la raíz del proyecto ejecuta:
```bash
docker-compose up -d
```
Esto iniciará una instancia de PostgreSQL en `localhost:5432` con las credenciales configuradas en tu docker-compose y sincronizadas con el `.env` del backend.

### Paso 2: Levantar el Backend (Laravel API)
1. Ve al directorio del backend:
   ```bash
   cd backend
   ```
2. Inicia el servidor de desarrollo de Laravel:
   ```bash
   php artisan serve
   ```
   El backend estará escuchando en `http://localhost:8000`.

### Paso 3: Levantar el Frontend (Vue.js + Vite)
1. Ve al directorio del frontend:
   ```bash
   cd ../frontend
   ```
2. Instala dependencias (si no lo has hecho aún):
   ```bash
   npm install
   ```
3. Inicia el servidor Vite:
   ```bash
   npm run dev
   ```
   El frontend estará escuchando en `http://localhost:5173`.

---

## Credenciales de Acceso (Entorno Local)

Para acceder a la plataforma web a través del Login maquetado en el entorno local (cargadas mediante `DatabaseSeeder`), puedes utilizar cualquiera de los siguientes perfiles de prueba:

| Perfil / Rol | Nombre / Empleado | Email / Username | Contraseña | Cargo / Descripción |
| :--- | :--- | :--- | :--- | :--- |
| **Administrador** (`admin`) | Admin General | `admin@doblex.com` / `admin.doblex` | `admin123` | Director General de Obra |
| **Administrativo** (`administrativo`) | Auxiliar Técnico | `adminis@doblex.com` / `adminis.doblex` | `adminis123` | Asistente Administrativo de Campo |
| **Operativo** (`operativo`) | Ing. Carlos Pérez | `carlos@doblex.com` / `carlos.doblex` | `operador123` | Ingeniero Residente de Estructuras |
| **Operativo** (`operativo`) | Ing. Luis Martínez | `luis@doblex.com` / `luis.doblex` | `operador123` | Ingeniero de Vías y Excavaciones |

---

## Configuración y Variables de Entorno

* **Backend (`backend/.env`):**
  * `DB_CONNECTION=pgsql`
  * `DB_HOST=127.0.0.1`
  * `DB_PORT=5432`
  * `DB_DATABASE=doblex_smu`
  * `DB_USERNAME=doblex_user`
  * `DB_PASSWORD=doblex_password`
  * `FRONTEND_URL=http://localhost:5173`
  
* **Frontend (`frontend/.env` - Opcional):**
  * `VITE_API_BASE_URL=http://localhost:8000/api`
  * `VITE_SANCTUM_CSRF_URL=http://localhost:8000/sanctum/csrf-cookie`

# Guía de Uso para el Desarrollo - DOBLEX SAS

Esta guía detalla la arquitectura de la aplicación, los flujos de comunicación y las pautas técnicas necesarias para extender y desarrollar nuevas funcionalidades dentro del **Sistema de Gestión de Obra Civil (SMU)**.

---

## 1. Arquitectura del Proyecto

El sistema está diseñado bajo una arquitectura desacoplada de alto rendimiento:

```mermaid
graph LR
  A[Vue.js SPA] -- HTTP / JSON (Axios + JWT) --> B[FastAPI Backend (Python 3.13)]
  B -- SQL (SQLAlchemy ORM) --> C[(SQLite / PostgreSQL)]
  B -- Generación en Memoria --> D[Reportes: Excel / Word / PDF]
```

* **Frontend (SPA):** Servido de manera independiente con Vue 3 + Vite. Se comunica con el backend mediante peticiones HTTP asíncronas con Axios inyectando el token Bearer JWT.
* **Backend (API REST):** FastAPI actúa como una API pura de alto rendimiento con validación estricta en Pydantic V2 y documentación OpenAPI/Swagger automática.
* **Base de Datos:** SQLite para desarrollo local ágil y PostgreSQL para entornos de despliegue o producción.

---

## 2. Flujo de Autenticación (JWT Bearer Token)

Para proteger las rutas y autenticar a los usuarios, utilizamos tokens **JSON Web Tokens (JWT)** con firma HMAC-SHA256 (`HS256`) y contraseñas hasheadas mediante **bcrypt**.

### Proceso de Autenticación

1. **Login:** El frontend envía las credenciales (`username` y `password`) mediante `POST` a `/api/login`.
2. **Validación:** FastAPI valida las credenciales y genera un token JWT firmado que incluye el `id`, `username`, `role` y fecha de expiración.
3. **Respuesta:** El servidor retorna:
   ```json
   {
     "status": "success",
     "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
     "user": {
       "id": 1,
       "name": "Admin General",
       "username": "admin.doblex",
       "role": "admin",
       "email": "admin@doblex.com"
     }
   }
   ```
4. **Almacenamiento Local:** El frontend almacena el token en `localStorage` (`smu_token`).
5. **Peticiones Autenticadas:** El interceptor de Axios en `client.js` inyecta automáticamente la cabecera:
   ```http
   Authorization: Bearer <smu_token>
   ```

### Credenciales de Perfiles de Desarrollo

Para probar los flujos y niveles de acceso de cada rol en el entorno local (generados en `app/db/seeder.py`), utiliza las siguientes credenciales:

| Perfil / Rol | Nombre / Empleado | Username | Contraseña | Cargo / Región |
| :--- | :--- | :--- | :--- | :--- |
| **Administrador** (`admin`) | Admin General | `admin.doblex` | `admin123` | Director General de Obra (Gestión total del sistema) |
| **Administrativo** (`administrativo`) | Auxiliar Técnico | `adminis.doblex` | `adminis123` | Asistente Administrativo de Campo (Gestión de OTs) |
| **Operativo** (`operativo`) | Ing. Carlos Pérez | `carlos.doblex` | `operador123` | Ingeniero Residente Electromecánico (Antioquia / Córdoba) |
| **Operativo** (`operativo`) | Ing. Luis Martínez | `luis.doblex` | `operador123` | Ingeniero de Energía y Climatización (Atlántico) |
| **Operativo** (`operativo`) | Jasmin Ariel Mosquera | `jasmin.doblex` | `operador123` | Técnico Electromecánico (Chocó / ZNI) |
| **Operativo** (`operativo`) | Eliseo Smith Granados | `eliseo.doblex` | `operador123` | Técnico Electricista (Atlántico / Barranquilla) |

---

## 3. Guía de Desarrollo Backend (FastAPI + Python)

### 3.1. Estructura de Carpetas

```text
backend/
├── app/
│   ├── api/
│   │   ├── endpoints/       # Controladores de rutas por módulo
│   │   │   ├── auth.py
│   │   │   ├── ots.py
│   │   │   ├── empleados.py
│   │   │   ├── cuadrillas.py
│   │   │   ├── avances.py
│   │   │   └── exports.py
│   │   ├── deps.py          # Inyección de dependencias (DB session, get_current_user, require_roles)
│   │   └── api_router.py    # Agrupador de enrutadores
│   ├── core/
│   │   ├── config.py        # Configuración centralizada (.env)
│   │   ├── security.py      # Lógica de JWT y bcrypt
│   │   └── utils.py         # Helpers de fecha UTC
│   ├── db/
│   │   ├── base.py          # Base declarativa de SQLAlchemy
│   │   ├── session.py       # Engine y generador get_db()
│   │   └── seeder.py        # Inicializador de datos de prueba
│   ├── models/              # Modelos de base de datos SQLAlchemy
│   ├── schemas/             # Esquemas de entrada/salida Pydantic V2
│   ├── services/            # Lógica de negocio, SLA, Excel, Word y PDF
│   └── main.py              # Aplicación FastAPI, CORS y Exception Handlers
├── tests_integration.py     # Suite de pruebas automatizadas
└── run.py                   # Script de arranque
```

### 3.2. Crear un Nuevo Modelo y Esquema

1. **Definir el Modelo en SQLAlchemy (`app/models/`):**
   ```python
   from sqlalchemy import Column, Integer, String, DateTime
   from app.db.base import Base
   from app.core.utils import now_utc

   class Material(Base):
       __tablename__ = "materiales"

       id = Column(Integer, primary_key=True, index=True)
       codigo = Column(String(50), unique=True, index=True, nullable=False)
       nombre = Column(String(255), nullable=False)
       stock = Column(Integer, default=0)
       created_at = Column(DateTime, default=now_utc)
   ```

2. **Definir el Esquema Pydantic (`app/schemas/`):**
   ```python
   from pydantic import BaseModel

   class MaterialCreate(BaseModel):
       codigo: str
       nombre: str
       stock: int = 0

   class MaterialResponse(MaterialCreate):
       id: int

       class Config:
           from_attributes = True
   ```

3. **Crear el Endpoint en `app/api/endpoints/`:**
   ```python
   from fastapi import APIRouter, Depends, HTTPException, status
   from sqlalchemy.orm import Session
   from app.db.session import get_db
   from app.api.deps import require_roles
   from app.models.material import Material
   from app.schemas.material import MaterialCreate

   router = APIRouter()

   @router.post("/materiales", status_code=status.HTTP_201_CREATED)
   def create_material(
       payload: MaterialCreate,
       current_user = Depends(require_roles(["admin", "administrativo"])),
       db: Session = Depends(get_db)
   ):
       material = Material(**payload.model_dump())
       db.add(material)
       db.commit()
       db.refresh(material)
       return {"status": "success", "data": material}
   ```

### 3.3. Servicios de Exportación (Excel, Word, PDF)

Toda exportación debe generarse **en memoria** usando buffers `io.BytesIO` para no almacenar archivos temporales en disco y retornarse mediante `StreamingResponse`:

```python
from fastapi.responses import StreamingResponse
from app.services.excel_service import generate_ots_excel

@router.get("/ots/export/excel")
def export_excel(db: Session = Depends(get_db)):
    ots = db.query(Ot).all()
    buffer = generate_ots_excel(ots)
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=reporte.xlsx"}
    )
```

---

## 4. Guía de Desarrollo Frontend (Vue.js)

### 4.1. Consumir Endpoints de la API

Utiliza el cliente Axios configurado en [`src/api/client.js`](file:///d:/DEV/CLIENTS/doblex/frontend/src/api/client.js). El cliente ya gestiona la inyección automática del token Bearer y el manejo de respuestas `401 Unauthorized` (redirección a login).

**Ejemplo de Servicio en Vue:**

```javascript
import client from '@/api/client';

export const OtsService = {
  // Obtener listado de OTs según rol
  async getAll() {
    const response = await client.get('/ots');
    return response.data.data;
  },

  // Crear una nueva OT con cálculo automático de SLA
  async create(payload) {
    const response = await client.post('/ots', payload);
    return response.data;
  },

  // Reportar avance diario de obra
  async reportarAvance(avanceData) {
    const response = await client.post('/avances', avanceData);
    return response.data;
  }
};
```

---

## 5. Reglas de Oro para el Desarrollo

1. **Idioma:** Todo el código fuente (nombres de variables, clases, métodos), la documentación y los comentarios deben escribirse en **Español**.
2. **Formato de Respuestas JSON:** Todo endpoint exitoso debe retornar `{ "status": "success", ... }` y cualquier excepción debe retornar `{ "status": "error", "message": "..." }` para garantizar consistencia con la UI.
3. **Manejo de Fechas:** Utilizar siempre zonas horarias consistentes (UTC) mediante el helper `now_utc()` de Python 3.13.
4. **Validación Obligatoria de Cierre:** Toda OT que cambie a estado `solucionada` debe exigir las 3 evidencias fotográficas (`antes`, `durante`, `despues`), causa de falla e insumos consumidos.
5. **Pruebas Automatizadas:** Todo nuevo endpoint debe incluir su correspondiente test en `tests_integration.py` y `tests_security.py` antes de ser integrado a producción.

---

## 6. Capa de Seguridad Profesional (Full-Stack)

El sistema incorpora una arquitectura de seguridad en profundidad (Defense-in-Depth):

### 6.1. Backend (FastAPI)
* **Cabeceras de Seguridad:** Inyección automática vía `SecurityHeadersMiddleware` de `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection`, `Referrer-Policy`, `Permissions-Policy`, `Content-Security-Policy` y `Strict-Transport-Security` (HSTS).
* **Protección Anti-Fuerza Bruta (Rate Limiting):** Algoritmo de ventana deslizante en memoria (`rate_limiter.py`) con detección de IP real tras proxies (`X-Forwarded-For`), bloqueando intentos excesivos en `/api/login` (HTTP 429 con `Retry-After`).
* **Revocación de Sesión (Token Blacklist):** `token_blacklist.py` almacena hashes criptográficos de tokens invalidados en `/logout`, denegando acceso inmediato antes de su fecha de expiración natural.
* **Validación Binaria de Archivos (*Magic Bytes*):** Inspección de firmas binarias reales (`file_validator.py`) en evidencias fotográficas (JPEG, PNG, WebP) y planillas Excel (XLSX, XLS), evitando cargas maliciosas o ejecutables encubiertos. Límite estricto de tamaño (HTTP 413) y generación de nombres seguros con UUID para mitigar *Path Traversal*.
* **CORS Endurecido:** Restricción a orígenes explícitos configurados, métodos HTTP específicos y cabeceras autorizadas.

### 6.2. Frontend (Vue 3 / Vite)
* **Metaetiquetas de Seguridad:** Inserción en `index.html` de directivas nosniff, frame-options y control de periféricos.
* **Integridad Criptográfica de Sesión:** `security.js` decodifica la carga útil del JWT y valida que el rol local en `localStorage` coincida con el firmado en el token. Ante cualquier manipulación en DevTools, destruye la sesión y redirige a login.
* **Verificación Previa de Expiración:** Interceptor de Axios que cancela proactivamente peticiones con tokens expirados, ahorrando llamadas innecesarias al backend.
* **Compilación Segura:** Vite configurado con esbuild para descartar sentencias `console.log` y `debugger` en builds de producción.

---

## 7. Estructura Oficial de OTs y Formularios de Campo (WO & MP)

### 7.1. Base de Sitios y Relación con OTs
* Se cargaron **1,819 estaciones base** oficiales desde `docs/ARCHIVO FACTURACIÓN.xlsx` en SQLite y PostgreSQL (`sitios`), incluyendo nemotécnicos, departamentos, municipios, transporte especial y supervisores operativos de Claro.
* Las órdenes de trabajo (`ots`) se vinculan a través de `sitio_id` (ForeignKey) y almacenan `id_actividad`, `coordinador`, `tipo_actividad` (`correctivo`, `emergencia`, `preventivo_planta`, `preventivo_aire`), `tipo_estacion` y `site_owner`.

### 7.2. Formato Correctivo & Emergencia (WO)
* **Plantilla de referencia:** `docs/WO0000005558781 MC MON.CENTRO.xlsx`.
* **Componente:** `FormularioTecnicoWO.vue` y endpoint dedicado `PUT /api/ots/{id}/formulario`.
* **Secciones:**
  1. *Información General & Afectación:* Tipo de sitio (Urbano/Rural), subsistema y afectación de servicio (Sí/No).
  2. *Diagnóstico de Falla & Equipo:* Tipo de equipo en falla, marca, modelo, intervención (Reparación, Reinstalación, Cambio), descripción de falla y solución técnica ejecutada.
  3. *Trazabilidad de Repuestos:* Datos de repuesto retirado (marca, modelo, serial) vs repuesto instalado nuevo.
  4. *Materiales LPU:* Tabla dinámica de materiales utilizados (descripción, unidad [Galón, Metro, UND, etc.], cantidad).
  5. *Transporte Especial:* Registro de medio (Vehículo 4x4, Lancha fluvial, Mula/Bestia, Caminata), distancia Km, tiempo y observaciones.
  6. *Novedades en Estación:* Hallazgos que comprometen el sitio (sistema, prioridad Alta/Media/Baja, descripción, resuelto en visita).
  7. *Cierre & Supervisión:* Falla resuelta a satisfacción (Sí/No), supervisor Claro notificado y observaciones finales de cierre.

### 7.3. Formato Preventivo Planta & Aire (MP)
* **Plantilla de referencia:** `docs/OT5304019_MP_CHO.RPT BAHIA SOLANO.xlsx`.
* **Componente:** `FormularioTecnicoMP.vue`.
* **Secciones (Preventivo Planta GE):**
  1. *Ficha Técnica / Placas:* Marca, modelo, serial y horómetro de planta, motor diesel, alternador Stamford y transferencia automática ATS con capacidad Amp.
  2. *Baterías de Arranque:* Voltaje VDC, capacidad Ah/CCA, tipo de batería y estado de bornes.
  3. *Rutina & Prueba de Encendido:* Horómetro final, prueba 15 min con carga simulando falla de energía, estado alarmas tablero, alarma externa NOC y temporización.
  4. *Parámetros Eléctricos en Carga:* Voltajes fase-fase (Vab, Vbc, Vca), voltajes fase-neutro (Van, Vbn, Vcn), corrientes L1/L2/L3, frecuencia Hz y % cargabilidad.
  5. *Checklist de Mantenimiento:* Filtración (aceite, combustible, aire), cambio aceite 15W40, galones, presión de aceite PSI, temperatura °C, nivel de tanque y trampa de agua.
* **Secciones (Preventivo Climatización AA):**
  1. *Ficha Técnica AA:* Marca, modelo, serial, capacidad BTU, refrigerante ecológico (R410A) y corriente compresor (Amp).
  2. *Parámetros Frigoríficos:* Presión de baja/alta PSI, temperaturas de inyección y retorno con cálculo automático de salto térmico (Delta T).
  3. *Checklist:* Lavado evaporador/condensador, filtros de aire y drenaje despejado.


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
backend_python/
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
5. **Pruebas Automatizadas:** Todo nuevo endpoint debe incluir su correspondiente test en `tests_integration.py` antes de ser integrado a producción.

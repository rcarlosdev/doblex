import unittest
import base64
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import validate_password_strength
from app.core.rate_limiter import rate_limiter

from app.core.token_blacklist import token_blacklist

class SecurityTestSuite(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Limpiar rate limiter y blacklist para aislamiento de pruebas unitarias
        rate_limiter._records.clear()
        token_blacklist._revoked_tokens.clear()


    def test_01_security_headers(self):
        """Verificar presencia obligatoria de cabeceras HTTP de seguridad profesionales."""
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)

        headers = res.headers
        self.assertEqual(headers.get("x-content-type-options"), "nosniff")
        self.assertEqual(headers.get("x-frame-options"), "DENY")
        self.assertEqual(headers.get("x-xss-protection"), "1; mode=block")
        self.assertEqual(headers.get("referrer-policy"), "strict-origin-when-cross-origin")
        self.assertIn("default-src", headers.get("content-security-policy", ""))
        self.assertIn("camera=(self)", headers.get("permissions-policy", ""))
        self.assertIn("max-age=31536000", headers.get("strict-transport-security", ""))
        self.assertIsNone(headers.get("server"))

    def test_02_rate_limiting_login_brute_force(self):
        """Verificar que el rate limiter bloquee intentos excesivos de login con HTTP 429."""
        # Limpiar registros para la clave de prueba
        key = "/api/login:testclient"
        if key in rate_limiter._records:
            del rate_limiter._records[key]

        # Enviar 5 intentos fallidos (límite configurado)
        for _ in range(5):
            res = self.client.post("/api/login", json={
                "username": "usuario_inexistente",
                "password": "wrongpassword"
            })
            self.assertEqual(res.status_code, 401)

        # El 6to intento debe ser bloqueado de inmediato con HTTP 429
        res_blocked = self.client.post("/api/login", json={
            "username": "usuario_inexistente",
            "password": "wrongpassword"
        })
        self.assertEqual(res_blocked.status_code, 429)
        self.assertIn("Demasiadas peticiones", res_blocked.json()["message"])
        self.assertTrue("Retry-After" in res_blocked.headers)

        # Limpiar para no afectar otras pruebas
        if key in rate_limiter._records:
            del rate_limiter._records[key]

    def test_03_token_blacklisting_on_logout(self):
        """Verificar que el token JWT quede inutilizado tras hacer logout."""
        # 1. Login exitoso como admin
        res_login = self.client.post("/api/login", json={
            "username": "admin.doblex",
            "password": "admin123"
        })
        self.assertEqual(res_login.status_code, 200)
        token = res_login.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Acceso inicial permitido a /api/user
        res_user_1 = self.client.get("/api/user", headers=headers)
        self.assertEqual(res_user_1.status_code, 200)

        # 3. Cerrar sesión
        res_logout = self.client.post("/api/logout", headers=headers)
        self.assertEqual(res_logout.status_code, 200)

        # 4. Reintentar acceso con el mismo token -> Debe ser rechazado con 401 por estar en lista negra
        res_user_2 = self.client.get("/api/user", headers=headers)
        self.assertEqual(res_user_2.status_code, 401)
        self.assertIn("revocado", res_user_2.json()["message"])

    def test_04_file_upload_security_magic_bytes(self):
        """Verificar rechazo de archivos que no cumplan la firma binaria real de imagen."""
        res_login = self.client.post("/api/login", json={
            "username": "admin.doblex",
            "password": "admin123"
        })
        token = res_login.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Intentar subir un payload falso que no es imagen
        fake_payload = base64.b64encode(b"<script>alert('malicious')</script>").decode("utf-8")
        res_fake = self.client.post("/api/ots/1/evidencia", json={
            "tipo": "antes",
            "imagen_base64": f"data:image/jpeg;base64,{fake_payload}",
            "latitud": 10.98,
            "longitud": -74.78
        }, headers=headers)
        self.assertEqual(res_fake.status_code, 422)
        self.assertIn("firma binaria", res_fake.json()["message"])

        # Subir imagen JPEG real mínima (FF D8 FF E0 00 10 4A 46 49 46 00 01)
        real_jpeg_bytes = b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xFF\xDB\x00C\x00\xFF\xD9"
        valid_b64 = base64.b64encode(real_jpeg_bytes).decode("utf-8")
        res_valid = self.client.post("/api/ots/1/evidencia", json={
            "tipo": "antes",
            "imagen_base64": f"data:image/jpeg;base64,{valid_b64}",
            "latitud": 10.98,
            "longitud": -74.78
        }, headers=headers)
        self.assertEqual(res_valid.status_code, 201)
        self.assertTrue(res_valid.json()["data"]["url_imagen"].startswith("/uploads/"))

    def test_05_excel_import_security_validation(self):
        """Verificar rechazo de archivos Excel falsos o corruptos."""
        res_login = self.client.post("/api/login", json={
            "username": "admin.doblex",
            "password": "admin123"
        })
        token = res_login.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Archivo con extensión .xlsx pero contenido malicioso de texto
        res_fake_excel = self.client.post(
            "/api/ots/import/excel",
            files={"file": ("malicious.xlsx", b"malicious executable content", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
            headers=headers
        )
        self.assertEqual(res_fake_excel.status_code, 422)
        self.assertIn("firma binaria", res_fake_excel.json()["message"])

    def test_06_password_complexity_validator(self):
        """Verificar reglas de contraseñas seguras."""
        ok1, _ = validate_password_strength("corta")
        self.assertFalse(ok1)

        ok2, _ = validate_password_strength("sololetrasmasdeochocaracteres")
        self.assertFalse(ok2)

        ok3, _ = validate_password_strength("1234567890")
        self.assertFalse(ok3)

        ok4, _ = validate_password_strength("Doblex2026*")
        self.assertTrue(ok4)

    def test_07_crear_empleado_con_acceso_y_login(self):
        """Verificar creación de empleado con usuario de inicio de sesión y autenticación posterior."""
        # 1. Autenticarse como admin
        res_admin = self.client.post("/api/login", json={
            "username": "admin.doblex",
            "password": "admin123"
        })
        self.assertEqual(res_admin.status_code, 200)
        token_admin = res_admin.json()["token"]
        headers = {"Authorization": f"Bearer {token_admin}"}

        # 2. Registrar empleado con acceso habilitado
        unique_doc = "9988776655"
        unique_user = "tecnico.prueba"
        unique_pwd = "Password2026*"

        # Limpiar por si existe previamente de una corrida previa
        from app.db.session import SessionLocal
        from app.models.empleado import Empleado
        from app.models.user import User
        db = SessionLocal()
        try:
            prev_emp = db.query(Empleado).filter(Empleado.documento == unique_doc).first()
            if prev_emp:
                db.delete(prev_emp)
            prev_u = db.query(User).filter(User.username == unique_user).first()
            if prev_u:
                db.delete(prev_u)
            db.commit()
        finally:
            db.close()

        payload = {
            "documento": unique_doc,
            "nombre": "Pedro Prueba Seguridad",
            "cargo": "Técnico Certificado",
            "telefono": "3009998877",
            "email": "pedro.prueba@doblex.com",
            "rol": "operativo",
            "estado": "activo",
            "habilitar_acceso": True,
            "username": unique_user,
            "password": unique_pwd
        }

        res_create = self.client.post("/api/empleados", json=payload, headers=headers)
        self.assertEqual(res_create.status_code, 201)
        data = res_create.json()["data"]
        self.assertIsNotNone(data.get("user"))
        self.assertEqual(data["user"]["username"], unique_user)

        # 3. Intentar iniciar sesión con las nuevas credenciales creadas
        res_login_nuevo = self.client.post("/api/login", json={
            "username": unique_user,
            "password": unique_pwd
        })
        self.assertEqual(res_login_nuevo.status_code, 200)
        self.assertEqual(res_login_nuevo.json()["status"], "success")
        self.assertEqual(res_login_nuevo.json()["user"]["username"], unique_user)
        self.assertEqual(res_login_nuevo.json()["user"]["role"], "operativo")

    def test_08_solo_admin_puede_asignar_rol_admin(self):
        """Verificar que un usuario no-admin (ej: administrativo) sea rechazado con 403 si intenta asignar rol admin."""
        # 1. Login como auxiliar técnico / administrativo
        res_adminis = self.client.post("/api/login", json={
            "username": "adminis.doblex",
            "password": "adminis123"
        })
        self.assertEqual(res_adminis.status_code, 200)
        token_adminis = res_adminis.json()["token"]
        headers_adminis = {"Authorization": f"Bearer {token_adminis}"}

        # 2. Intentar crear un nuevo empleado con rol 'admin'
        payload_create = {
            "documento": "8877665544",
            "nombre": "Intento Escalada",
            "cargo": "Técnico",
            "rol": "admin",
            "estado": "activo"
        }
        res_fail_create = self.client.post("/api/empleados", json=payload_create, headers=headers_adminis)
        self.assertEqual(res_fail_create.status_code, 403)
        self.assertIn("Solo los usuarios con rol 'admin'", res_fail_create.json()["detail"])

        # 3. Intentar modificar un empleado existente para asignarle rol 'admin'
        # Empleado Carlos Pérez (id 3 u otro existente)
        res_list = self.client.get("/api/empleados", headers=headers_adminis)
        empleados = res_list.json()["data"]
        operativo_emp = next((e for e in empleados if e["rol"] == "operativo"), None)
        self.assertIsNotNone(operativo_emp)

        payload_update = {
            "documento": operativo_emp["documento"],
            "nombre": operativo_emp["nombre"],
            "cargo": operativo_emp["cargo"],
            "rol": "admin",
            "estado": operativo_emp["estado"]
        }
        res_fail_update = self.client.put(f"/api/empleados/{operativo_emp['id']}", json=payload_update, headers=headers_adminis)
        self.assertEqual(res_fail_update.status_code, 403)
        self.assertIn("Solo los usuarios con rol 'admin'", res_fail_update.json()["detail"])

if __name__ == "__main__":
    unittest.main()

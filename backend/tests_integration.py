import os
import sys
import unittest
import uuid
from fastapi.testclient import TestClient

# Asegurar path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app

class TestDoblexAPI(unittest.TestCase):
    test_code = f"OT-TEST-{uuid.uuid4().hex[:6].upper()}"
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        
        # 1. Login Admin
        res_admin = cls.client.post("/api/login", json={
            "username": "admin.doblex",
            "password": "admin123"
        })
        assert res_admin.status_code == 200, f"Error en login admin: {res_admin.text}"
        data_admin = res_admin.json()
        cls.admin_token = data_admin["token"]
        cls.admin_headers = {"Authorization": f"Bearer {cls.admin_token}"}

        # 2. Login Operativo Carlos
        res_carlos = cls.client.post("/api/login", json={
            "username": "carlos.doblex",
            "password": "operador123"
        })
        assert res_carlos.status_code == 200, f"Error en login carlos: {res_carlos.text}"
        data_carlos = res_carlos.json()
        cls.carlos_token = data_carlos["token"]
        cls.carlos_headers = {"Authorization": f"Bearer {cls.carlos_token}"}

    def test_01_login_invalido(self):
        res = self.client.post("/api/login", json={
            "username": "admin.doblex",
            "password": "password_incorrecto"
        })
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json()["status"], "error")

    def test_02_get_user_profile(self):
        res = self.client.get("/api/user", headers=self.admin_headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["username"], "admin.doblex")
        self.assertEqual(data["role"], "admin")

    def test_03_list_ots_admin_vs_operativo(self):
        # Admin ve todas
        res_admin = self.client.get("/api/ots", headers=self.admin_headers)
        self.assertEqual(res_admin.status_code, 200)
        ots_admin = res_admin.json()["data"]
        self.assertGreaterEqual(len(ots_admin), 3)

        # Operativo Carlos ve sus asignadas o las de su cuadrilla
        res_carlos = self.client.get("/api/ots", headers=self.carlos_headers)
        self.assertEqual(res_carlos.status_code, 200)
        ots_carlos = res_carlos.json()["data"]
        for ot in ots_carlos:
            user_id = ot["user_id"]
            cuadrilla_id = ot["cuadrilla_id"]
            # Debe estar asignado directamente a Carlos o a su cuadrilla (Antioquia = 1)
            self.assertTrue(user_id == 3 or cuadrilla_id == 1)

    def test_04_create_ot_and_sla_calculation(self):
        payload = {
            "codigo": self.test_code,
            "descripcion": "Mantenimiento urgente en subestación",
            "sitio": "SE-Medellin-Sur",
            "ubicacion": "Medellín, Antioquia",
            "user_id": 3,
            "cuadrilla_id": 1,
            "prioridad": "P1",
            "tipo_ubicacion": "urbana",
            "tipo_mantenimiento": "emergencia",
            "subsistema": "sistema_electrico",
            "tipo_gasto": "OPEX",
            "fecha_inicio": "2026-09-10T08:00:00"
        }
        res = self.client.post("/api/ots", json=payload, headers=self.admin_headers)
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertEqual(data["status"], "success")
        ot = data["data"]
        self.assertEqual(ot["codigo"], self.test_code)
        self.assertIsNotNone(ot["fecha_limite_sla"])
        # Para P1 urbana son 270 minutos (4h 30m) -> 12:30:00
        self.assertTrue("12:30:00" in ot["fecha_limite_sla"])

    def test_05_update_ot_estado(self):
        # Obtener la OT creada
        res_get = self.client.get("/api/ots", headers=self.admin_headers)
        ot = [o for o in res_get.json()["data"] if o["codigo"] == self.test_code][0]

        res = self.client.put(f"/api/ots/{ot['id']}/estado", json={
            "estado": "en_progreso",
            "progreso": 30
        }, headers=self.admin_headers)
        self.assertEqual(res.status_code, 200)
        updated = res.json()["data"]
        self.assertEqual(updated["estado"], "en_progreso")
        self.assertEqual(updated["progreso"], 30)

    def test_06_reportar_avance(self):
        res_get = self.client.get("/api/ots", headers=self.admin_headers)
        ot = [o for o in res_get.json()["data"] if o["codigo"] == self.test_code][0]

        # Carlos reporta avance
        res = self.client.post("/api/avances", json={
            "ot_id": ot["id"],
            "descripcion": "Se realizó desmonte de tablero y pruebas de aislamiento.",
            "porcentaje": 20,
            "fecha_reporte": "2026-09-10T11:00:00"
        }, headers=self.carlos_headers)
        self.assertEqual(res.status_code, 201)
        data = res.json()["data"]
        self.assertEqual(data["ot"]["progreso"], 50)  # 30 + 20

    def test_07_validar_bloqueo_exceso_progreso(self):
        res_get = self.client.get("/api/ots", headers=self.admin_headers)
        ot = [o for o in res_get.json()["data"] if o["codigo"] == self.test_code][0]

        # Progreso actual 50%, si reporta 60% debe fallar con 422
        res = self.client.post("/api/avances", json={
            "ot_id": ot["id"],
            "descripcion": "Avance excesivo",
            "porcentaje": 60,
            "fecha_reporte": "2026-09-10T12:00:00"
        }, headers=self.carlos_headers)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.json()["status"], "error")

    def test_08_evidencias_y_cierre_tecnico(self):
        res_get = self.client.get("/api/ots", headers=self.admin_headers)
        ot = [o for o in res_get.json()["data"] if o["codigo"] == self.test_code][0]

        # Intentar cerrar sin evidencias -> 422
        res_cerrar_fail = self.client.post(f"/api/ots/{ot['id']}/cerrar", json={
            "causa_falla": "desgaste",
            "observaciones_cierre": "Cierre preventivo"
        }, headers=self.admin_headers)
        self.assertEqual(res_cerrar_fail.status_code, 422)
        self.assertIn("evidencias obligatorias", res_cerrar_fail.json()["message"])

        # Subir las 3 evidencias reales: antes, durante, después
        ev_urls = {
            "antes": "https://images.unsplash.com/photo-1541888946425-d0fbb186f5f8?w=800",
            "durante": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800",
            "despues": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800"
        }
        for tipo, url in ev_urls.items():
            res_ev = self.client.post(f"/api/ots/{ot['id']}/evidencia", json={
                "tipo": tipo,
                "imagen_url": url,
                "latitud": 6.2442,
                "longitud": -75.5812
            }, headers=self.carlos_headers)
            self.assertEqual(res_ev.status_code, 201)

        # Ahora cerrar satisfactoriamente con repuestos
        res_cerrar_ok = self.client.post(f"/api/ots/{ot['id']}/cerrar", json={
            "causa_falla": "desgaste",
            "observaciones_cierre": "Mantenimiento culminado con éxito.",
            "repuestos": [
                {"nombre_item": "Fusible 63A", "cantidad": 3.0, "unidad_medida": "unidad"}
            ]
        }, headers=self.admin_headers)
        self.assertEqual(res_cerrar_ok.status_code, 200)
        data_cerrada = res_cerrar_ok.json()["data"]
        self.assertEqual(data_cerrada["estado"], "solucionada")
        self.assertEqual(data_cerrada["progreso"], 100)

    def test_09_exportaciones(self):
        res_get = self.client.get("/api/ots", headers=self.admin_headers)
        ot = res_get.json()["data"][0]

        # 1. Excel
        res_excel = self.client.get("/api/ots/export/excel", headers=self.admin_headers)
        self.assertEqual(res_excel.status_code, 200)
        self.assertEqual(res_excel.headers["content-type"], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.assertGreater(len(res_excel.content), 1000)

        # 2. Word
        res_word = self.client.get(f"/api/ots/{ot['id']}/export/word", headers=self.admin_headers)
        self.assertEqual(res_word.status_code, 200)
        self.assertEqual(res_word.headers["content-type"], "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        self.assertGreater(len(res_word.content), 1000)

        # 3. PDF
        res_pdf = self.client.get(f"/api/ots/{ot['id']}/export/pdf", headers=self.admin_headers)
        self.assertEqual(res_pdf.status_code, 200)
        self.assertEqual(res_pdf.headers["content-type"], "application/pdf")
        self.assertGreater(len(res_pdf.content), 1000)

    def test_10_empleados_y_cuadrillas(self):
        res_emp = self.client.get("/api/empleados", headers=self.admin_headers)
        self.assertEqual(res_emp.status_code, 200)
        self.assertGreaterEqual(len(res_emp.json()["data"]), 4)

        res_cua = self.client.get("/api/cuadrillas", headers=self.admin_headers)
        self.assertEqual(res_cua.status_code, 200)
        self.assertGreaterEqual(len(res_cua.json()["data"]), 4)

        res_ops = self.client.get("/api/operadores", headers=self.admin_headers)
        self.assertEqual(res_ops.status_code, 200)
        self.assertGreaterEqual(len(res_ops.json()["data"]), 4)

if __name__ == "__main__":
    unittest.main()

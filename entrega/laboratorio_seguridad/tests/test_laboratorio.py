"""Casos de Wilberth (SeguridadWilberth) y de Jania (SeguridadJania)."""
import copy
import unittest

from src.lab import estado_inicial, leer_expediente, actualizar_nota, revocar_sesion


class SeguridadWilberth(unittest.TestCase):
    def setUp(self):
        self.estado = estado_inicial()
        self.expedientes_antes = copy.deepcopy(self.estado["expedientes"])

    def assertSinDatosProtegidos(self, datos):
        for campo in ("id", "estudiante", "sede", "nota"):
            with self.subTest(campo=campo):
                self.assertNotIn(campo, datos, f"La denegación filtra el campo {campo}")

    def assertExpedientesIntactos(self):
        self.assertEqual(
            self.expedientes_antes,
            self.estado["expedientes"],
            "La operación no debe modificar ningún expediente",
        )

    def assertLecturaAuditada(self, usuario, expediente_id):
        evento = self.estado["auditoria"][-1]
        self.assertEqual("lectura", evento.get("accion"))
        self.assertEqual(usuario, evento.get("usuario"), "La auditoría debe identificar al usuario")
        self.assertEqual(expediente_id, evento.get("id"))
        self.assertNotIn("token", evento, "La auditoría no debe almacenar credenciales")
        self.assertNotIn("lab-", repr(evento), "La auditoría contiene un token sintético")

    def test_tc01_sec01_estudiante_lee_su_expediente_sin_alterarlo(self):
        codigo, datos = leer_expediente(self.estado, "lab-ana", "101")
        self.assertEqual(200, codigo, "Ana debe poder consultar su expediente 101")
        self.assertEqual(self.expedientes_antes["101"], datos)
        self.assertExpedientesIntactos()
        self.assertEqual(1, len(self.estado["auditoria"]))
        self.assertLecturaAuditada("ana", "101")

    def test_tc03_sec01_administrador_lee_ambas_sedes_sin_alterarlas(self):
        for expediente_id in ("101", "202"):
            with self.subTest(expediente=expediente_id):
                codigo, datos = leer_expediente(self.estado, "lab-admin", expediente_id)
                self.assertEqual(200, codigo, f"El administrador debe poder consultar {expediente_id}")
                self.assertEqual(self.expedientes_antes[expediente_id], datos)
                self.assertExpedientesIntactos()
                self.assertLecturaAuditada("admin", expediente_id)
        self.assertEqual(2, len(self.estado["auditoria"]))

    def test_tc04_sec01_estudiante_no_lee_expediente_ajeno_ni_filtra_datos(self):
        codigo, datos = leer_expediente(self.estado, "lab-ana", "202")
        self.assertEqual(403, codigo, "Ana no debe consultar el expediente 202 de Luis")
        self.assertSinDatosProtegidos(datos)
        self.assertNotIn("luis", repr(datos).lower())
        self.assertExpedientesIntactos()

    def test_tc07_sec02_estudiante_y_admin_no_modifican_notas(self):
        for token in ("lab-ana", "lab-admin"):
            with self.subTest(rol=token.removeprefix("lab-")):
                self.estado = estado_inicial()
                self.expedientes_antes = copy.deepcopy(self.estado["expedientes"])
                codigo, datos = actualizar_nota(self.estado, token, "101", 70)
                self.assertEqual(403, codigo, f"{token} no tiene permiso para modificar notas")
                self.assertSinDatosProtegidos(datos)
                self.assertExpedientesIntactos()


class SeguridadExpedientes(unittest.TestCase):
    """Ejemplo original pendiente: Jania lo amplía como TC-02."""

    def setUp(self):
        self.estado = estado_inicial()

    def test_docente_actualiza_nota_en_su_sede(self):
        codigo, datos = actualizar_nota(self.estado, "lab-maria", "101", 85)
        self.assertEqual(200, codigo)
        self.assertEqual(85, datos.get("nota"))


class SeguridadJania(unittest.TestCase):
    """Casos del bloque de Jania: sesiones, escritura por sede y auditoría de escritura."""

    def setUp(self):
        self.estado = estado_inicial()
        self.expedientes_antes = copy.deepcopy(self.estado["expedientes"])

    def assertSinDatosProtegidos(self, datos):
        for campo in ("id", "estudiante", "sede", "nota"):
            with self.subTest(campo=campo):
                self.assertNotIn(campo, datos, f"La respuesta filtra el campo {campo}")

    def assertExpedientesIntactos(self):
        self.assertEqual(self.expedientes_antes, self.estado["expedientes"],
                         "La operación rechazada no debe modificar ningún expediente")

    def test_tc08_sec03_sesion_revocada_o_invalida_no_lee_ni_modifica(self):
        variantes = {
            "revocada": "lab-maria",
            "token_vacio": "",
            "token_inexistente": "lab-desconocido",
        }
        for nombre, token in variantes.items():
            with self.subTest(variante=nombre):
                self.estado = estado_inicial()
                self.expedientes_antes = copy.deepcopy(self.estado["expedientes"])
                if nombre == "revocada":
                    codigo, _ = revocar_sesion(self.estado, token)
                    self.assertEqual(200, codigo, "Precondición: la revocación debe aceptarse")
                codigo, datos = leer_expediente(self.estado, token, "101")
                self.assertEqual(401, codigo, f"Sesión {nombre}: la lectura debe rechazarse con 401")
                self.assertSinDatosProtegidos(datos)
                codigo, datos = actualizar_nota(self.estado, token, "101", 70)
                self.assertEqual(401, codigo, f"Sesión {nombre}: el cambio de nota debe rechazarse con 401")
                self.assertSinDatosProtegidos(datos)
                self.assertExpedientesIntactos()

if __name__ == "__main__":
    unittest.main()

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
        self.assertNotIn({"accion": "lectura", "usuario": "ana", "id": "202"}, self.estado["auditoria"],
                         "Una lectura denegada no debe registrarse como lectura exitosa")
        self.assertNotIn("lab-", repr(self.estado["auditoria"]), "La auditoría contiene un token sintético")

    def test_tc05_sec01_docente_no_lee_expediente_de_otra_sede(self):
        codigo, datos = leer_expediente(self.estado, "lab-maria", "202")
        self.assertEqual(403, codigo, "María (Central) no debe consultar el expediente 202 (Pacífico)")
        self.assertSinDatosProtegidos(datos)
        self.assertNotIn("luis", repr(datos).lower())
        self.assertExpedientesIntactos()
        self.assertEqual([], self.estado["auditoria"], "La lectura denegada no debe auditarse como exitosa")
        codigo, datos = leer_expediente(self.estado, "lab-pedro", "202")
        self.assertEqual(200, codigo, "Pedro (Pacífico) sí debe consultar el expediente 202 de su sede")
        self.assertEqual(self.expedientes_antes["202"], datos)

    def test_tc12_sec04_nota_fuera_de_rango_o_tipo_invalido_no_persiste(self):
        variantes = {"menor_que_0": -1, "mayor_que_100": 101, "texto": "ochenta",
                     "booleano": True, "entero_enorme": 10**400, "nulo": None}
        for nombre, nota in variantes.items():
            with self.subTest(variante=nombre):
                self.estado = estado_inicial()
                self.expedientes_antes = copy.deepcopy(self.estado["expedientes"])
                codigo, datos = actualizar_nota(self.estado, "lab-maria", "101", nota)
                self.assertEqual(400, codigo, f"La nota {nombre} debe rechazarse con 400")
                self.assertSinDatosProtegidos(datos)
                self.assertExpedientesIntactos()
                self.assertEqual([], self.estado["auditoria"], "Un cambio rechazado no debe auditarse")

    def test_tc07_sec02_estudiante_y_admin_no_modifican_notas(self):
        for token in ("lab-ana", "lab-admin"):
            with self.subTest(rol=token.removeprefix("lab-")):
                self.estado = estado_inicial()
                self.expedientes_antes = copy.deepcopy(self.estado["expedientes"])
                codigo, datos = actualizar_nota(self.estado, token, "101", 70)
                self.assertEqual(403, codigo, f"{token} no tiene permiso para modificar notas")
                self.assertSinDatosProtegidos(datos)
                self.assertExpedientesIntactos()


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

    def test_tc02_sec02_docente_modifica_nota_de_su_sede_y_queda_auditada(self):
        codigo, datos = actualizar_nota(self.estado, "lab-maria", "101", 85)
        self.assertEqual(200, codigo, "María debe poder cambiar la nota de un expediente de Central")
        self.assertEqual(85, datos.get("nota"))
        self.assertEqual(85, self.estado["expedientes"]["101"]["nota"], "El cambio debe persistir")
        self.assertEqual(self.expedientes_antes["202"], self.estado["expedientes"]["202"],
                         "El expediente de otra sede no debe cambiar")
        evento = self.estado["auditoria"][-1]
        self.assertEqual("actualizacion", evento.get("accion"))
        self.assertEqual("maria", evento.get("usuario"), "La auditoría debe identificar a la docente")
        self.assertEqual("101", evento.get("id"))
        self.assertNotIn("token", evento, "La auditoría no debe almacenar credenciales")
        self.assertNotIn("lab-", repr(evento), "La auditoría contiene un token sintético")

    def test_tc06_sec02_docente_no_modifica_nota_de_otra_sede(self):
        codigo, datos = actualizar_nota(self.estado, "lab-maria", "202", 70)
        self.assertEqual(403, codigo, "María (Central) no debe cambiar la nota del 202 (Pacífico)")
        self.assertSinDatosProtegidos(datos)
        self.assertEqual(91, self.estado["expedientes"]["202"]["nota"], "La nota original debe conservarse")
        self.assertExpedientesIntactos()
        self.assertEqual([], self.estado["auditoria"], "Un cambio denegado no debe auditarse como actualización")

    def test_tc06_sec02_otra_sede_con_nota_invalida_responde_403_antes_que_400(self):
        codigo, datos = actualizar_nota(self.estado, "lab-maria", "202", 150)
        self.assertEqual(403, codigo, "La autorización debe evaluarse antes que la validación de la nota")
        self.assertSinDatosProtegidos(datos)
        self.assertExpedientesIntactos()


if __name__ == "__main__":
    unittest.main()

"""Pruebas de ejemplo: algunas fallan INTENCIONALMENTE (fase roja de TDD)."""
import unittest
import copy
from src.lab import estado_inicial, leer_expediente, actualizar_nota, revocar_sesion


class SeguridadExpedientes(unittest.TestCase):
    def setUp(self):
        self.estado = estado_inicial()  # Un estado independiente por prueba.

    def test_estudiante_consulta_expediente_propio(self):
        codigo, datos = leer_expediente(self.estado, "lab-ana", "101")
        self.assertEqual(200, codigo)
        self.assertEqual("ana", datos.get("estudiante"))

    def test_docente_actualiza_nota_en_su_sede(self):
        codigo, datos = actualizar_nota(self.estado, "lab-maria", "101", 85)
        self.assertEqual(200, codigo)
        self.assertEqual(85, datos.get("nota"))

    def test_rojo_estudiante_no_consulta_expediente_ajeno(self):
        expedientes_antes = copy.deepcopy(self.estado["expedientes"])

        codigo, datos = leer_expediente(self.estado, "lab-ana", "202")

        self.assertEqual(
            403,
            codigo,
            "Ana no debe consultar el expediente 202 de Luis",
        )

        for campo in ("id", "estudiante", "sede", "nota"):
            with self.subTest(campo=campo):
                self.assertNotIn(
                    campo,
                    datos,
                    f"La respuesta denegada no debe incluir el campo {campo}",
                )

        self.assertEqual(
            expedientes_antes,
            self.estado["expedientes"],
            "La lectura denegada debe conservar los expedientes intactos",
        )

    def test_rojo_sesion_revocada_no_permita_lecturas(self):
        codigo, _ = revocar_sesion(self.estado, "lab-ana")
        self.assertEqual(200, codigo)
        codigo, datos = leer_expediente(self.estado, "lab-ana", "101")
        self.assertEqual(401, codigo)
        self.assertNotIn("nota", datos)


if __name__ == "__main__":
    unittest.main()

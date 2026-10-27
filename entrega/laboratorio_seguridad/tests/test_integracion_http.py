"""Pruebas de integración HTTP del bloque de Jania (TC-10, TC-11).

Levantan servidor.py en 127.0.0.1 con un puerto libre, envían solicitudes HTTP reales
y cierran el servidor al terminar. No requieren iniciar la API manualmente.
"""
import http.client
import json
import threading
import unittest
from http.server import ThreadingHTTPServer

import servidor
from src.lab import estado_inicial


class IntegracionHttpLimitesNota(unittest.TestCase):
    def setUp(self):
        servidor.ServidorLaboratorio.estado = estado_inicial()
        servidor.ServidorLaboratorio.log_message = lambda *args, **kwargs: None
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), servidor.ServidorLaboratorio)
        self.puerto = self.httpd.server_address[1]
        self.hilo = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.hilo.start()

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.hilo.join(timeout=5)

    def solicitar(self, metodo, ruta, token, cuerpo=None):
        conexion = http.client.HTTPConnection("127.0.0.1", self.puerto, timeout=5)
        encabezados = {"Authorization": f"Bearer {token}"}
        datos = None
        if cuerpo is not None:
            datos = json.dumps(cuerpo)
            encabezados["Content-Type"] = "application/json"
        try:
            conexion.request(metodo, ruta, body=datos, headers=encabezados)
            respuesta = conexion.getresponse()
            return respuesta.status, json.loads(respuesta.read().decode("utf-8"))
        finally:
            conexion.close()

    def verificar_limite(self, nota):
        estado = servidor.ServidorLaboratorio.estado
        nota_202_antes = estado["expedientes"]["202"]["nota"]
        codigo, datos = self.solicitar("POST", "/expedientes/101/nota", "lab-maria", {"nota": nota})
        self.assertEqual(200, codigo, f"La nota límite {nota} debe aceptarse por HTTP")
        self.assertEqual(nota, datos.get("nota"))
        codigo, datos = self.solicitar("GET", "/expedientes/101", "lab-maria")
        self.assertEqual(200, codigo)
        self.assertEqual(nota, datos.get("nota"), f"La nota {nota} debe persistir y leerse por HTTP")
        self.assertEqual(nota_202_antes, estado["expedientes"]["202"]["nota"], "El 202 no debe cambiar")
        eventos = [e for e in estado["auditoria"] if e.get("accion") == "actualizacion"]
        self.assertEqual(1, len(eventos), "Debe registrarse exactamente un cambio de nota")
        self.assertEqual("maria", eventos[0].get("usuario"))
        self.assertNotIn("lab-", repr(estado["auditoria"]), "La auditoría no debe contener tokens")

    def test_tc10_sec04_limite_inferior_0_se_acepta_por_http(self):
        self.verificar_limite(0)

    def test_tc11_sec04_limite_superior_100_se_acepta_por_http(self):
        self.verificar_limite(100)


if __name__ == "__main__":
    unittest.main()

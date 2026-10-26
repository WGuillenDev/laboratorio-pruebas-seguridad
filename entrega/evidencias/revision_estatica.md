# Revisión estática del código (SAST manual)

- **Fecha:** 25/10/2026
- **Versión revisada:** commit `8e98b14` (rama `wil`)
- **Archivos:** `src/lab.py` y `servidor.py`
- **Técnica:** lectura del código sin ejecutarlo, con lista de comprobación. No se utilizó un escáner SAST automatizado.

La revisión estática examina el código sin ejecutarlo. Las solicitudes HTTP (TC-05, TC-12) y `unittest` son pruebas dinámicas y se documentan por separado.

## Lista de comprobación

| Comprobación | Hallazgo en el código | Estado / acción |
| --- | --- | --- |
| Permisos de lectura | La versión base no aplicaba ninguna política después de autenticar. | Corregido: `_puede_leer` por rol, titular y sede (H-01, H-03). |
| Permisos de modificación | `actualizar_nota` solo verifica que el rol sea docente; no compara la sede del docente con la del expediente. | Abierto: H-06 (Jania). |
| Validez de sesión | `autenticar()` ignora los indicadores `revocada` y `expirada`. | Abierto: H-02 (Jania). |
| Validación de entrada | Se aceptaban `bool` y cualquier número sin rango. | Corregido: `_nota_valida` excluye `bool` y aplica [0, 100]; NaN e infinito quedan fuera del rango (H-04). |
| Manejo de errores | Mensajes genéricos 401/403/400; las respuestas no incluyen trazas internas. | Conforme. |
| Exposición de datos | Las denegaciones retornan antes de copiar el expediente. | Conforme; verificado en TC-04, TC-05 y TC-07. |
| Auditoría | Los eventos guardaban el token y no el usuario. | Lectura corregida; actualización abierta (H-05, Jania). |
| Orden de controles | Se responde 404 antes de autorizar: un estudiante distingue ids existentes (403) de inexistentes (404). | Observación O-06, baja. |
| Estado compartido | `ThreadingHTTPServer` comparte un diccionario sin bloqueo. | Observación O-08, baja (concurrencia fuera de alcance). |

## Confirmación de H-06 y de las observaciones

Para confirmar los puntos de la lista se ejecutó la lógica directamente (comprobación dinámica mínima, desde `entrega/laboratorio_seguridad`):

```text
leer_expediente(e, "lab-ana", "999")        -> (404, {'error': 'No existe'})          # O-06
leer_expediente(e, "lab-ana", "202")        -> (403, {'error': 'Operación denegada'})
actualizar_nota(e, "lab-maria", "202", 70)  -> (200, {... 'nota': 70})                # H-06
e["auditoria"]                              -> [{'accion': 'actualizacion', 'token': 'lab-maria', 'id': '202'}]   # H-05
revocar_sesion(e, "lab-vencida")            -> (200, {'mensaje': 'Sesión revocada'}) # O-07
actualizar_nota(e, "lab-maria", "101", nan) -> (400, ...)   ;   inf -> (400, ...)
```

## Observaciones para la inspección cruzada

| ID | Objeto | Observación | Severidad | Acción tomada / propuesta |
| --- | --- | --- | --- | --- |
| O-01 | Prueba de consulta propia | El oráculo original solo verificaba 200 e identidad; no detectaba fallos de auditoría. | Media | Ampliado: respuesta completa, estado intacto y auditoría sin token (TC-01). |
| O-02 | Prueba de acceso ajeno | `assertNotIn('nota')` no detectaba la filtración de otros campos. | Media | Ampliado: se comprueban id, estudiante, sede, nota y titular (TC-04). |
| O-03 | Política de lectura | Docentes podían leer otras sedes. | Alta | Corregido con `_puede_leer` (H-03). |
| O-04 | Sesiones | `autenticar()` no revisa revocada/expirada. | Alta | Abierto: H-02, TDD 2 de Jania. |
| O-05 | Auditoría de escritura | `actualizar_nota` guarda el token y no el usuario. | Alta | Abierto: H-05 (escritura), Jania. |
| O-06 | Orden de controles | 404 antes de autorizar permite enumerar ids existentes. | Baja | Propuesta: autorizar antes o responder 403/404 de forma uniforme. |
| O-07 | Revocación | `revocar_sesion` acepta una sesión expirada (200). | Baja | Propuesta: responder 401 si la sesión ya no es válida. |
| O-08 | Servidor | Estado compartido entre hilos sin bloqueo. | Baja | Se acepta como limitación del laboratorio. |

Jania debe confirmar o descartar estas observaciones en el acta de inspección cruzada (revisor, fecha, objetos, severidad y acción).

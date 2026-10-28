# Acta de inspección cruzada (§7.1) · política de escritura

| Campo | Registro |
| --- | --- |
| Revisor / autora | Wilberth Guillén Aguilar (revisor) / Jania Hernández Dormuz (autora) |
| Fecha | 27/10/2026 |
| Versión revisada | rama `wil`, commit `8b63a19` (integra todo el bloque de `jania`) |
| Objetos inspeccionados | Política de escritura `_puede_modificar` y orden de controles de `actualizar_nota` (src/lab.py) · TC-02 · TC-06 (tests/test_laboratorio.py) |
| Método | Lectura del código y de las pruebas; análisis de mutantes: se alteró cada regla de escritura en una copia y se ejecutó la suite real con el [script](inspeccion_wilberth_mutantes.py) ([salida](inspeccion_wilberth.txt)) |
| Preguntas guía | ¿La prueba comprueba el efecto sobre los datos? ¿Es independiente? ¿Puede fallar cuando el control falla? |

## Resultado del análisis de mutantes

| Mutante | Cambio aplicado | Suite `8b63a19` | Suite con acciones |
| --- | --- | --- | --- |
| M-E1 | Docente modifica cualquier sede | Detectado por TC-06 | Detectado por TC-06 (dos pruebas) |
| M-E2 | Cualquier rol de la sede modifica | Detectado por TC-07 | Detectado por TC-07 |
| M-E3 | Nadie puede modificar | Detectado por TC-02, TC-10, TC-11 | Detectado por TC-02, TC-10, TC-11, TC-12 |
| M-E4 | Se omite el rango 0–100 | **Sobrevive** | Detectado por TC-12 |
| M-E5 | La auditoría guarda el token | Detectado por TC-02, TC-10, TC-11 | Detectado por TC-02, TC-10, TC-11 |
| M-E6 | Se audita antes de autorizar | Detectado solo por TC-10, TC-11 | Detectado por TC-06, TC-10, TC-11, TC-12 |
| M-E7 | Se valida la nota antes de autorizar | **Sobrevive** | Detectado por TC-06 (variante 403 antes que 400) |
| M-L2 | Docente lee cualquier sede (J-01 de la revisora) | **Sobrevive** | Detectado por TC-05 |

## Respuestas a las preguntas guía

| Prueba | ¿Comprueba el efecto sobre los datos? | ¿Es independiente? | ¿Puede fallar si el control falla? |
| --- | --- | --- | --- |
| TC-02 | Sí: verifica la respuesta, la persistencia de 85 en el 101, que el 202 no cambia y el evento de auditoría con usuario y sin token | Sí: estado nuevo en `setUp`; no depende del orden ni de otras pruebas | Sí: falla con M-E3 y M-E5. Toma solo el último evento, por lo que no detectaría un evento duplicado (W-04) |
| TC-06 | Sí: copia profunda antes/después, nota 91 conservada y ausencia de id, estudiante, sede y nota | Sí: estado nuevo en `setUp` | Sí: falla con M-E1. En `8b63a19` no revisaba la bitácora (W-02) ni el orden de los controles (W-03) |

## Observaciones del revisor

| ID | Objeto | Observación | Severidad | Acción tomada | Estado |
| --- | --- | --- | --- | --- | --- |
| W-01 | `_nota_valida` / suite | Si se elimina el rango 0–100 (M-E4), ninguna prueba automatizada falla: TC-12 solo se ejecutaba por HTTP manual y TC-10/TC-11 prueban únicamente valores válidos. Una regresión de H-04 pasaría inadvertida. | Media | Se agregó `test_tc12_sec04_nota_fuera_de_rango_o_tipo_invalido_no_persiste` con −1, 101, texto, booleano, entero de 401 cifras y nulo; cada variante exige 400, expedientes intactos y bitácora vacía | Corregida y verificada |
| W-02 | TC-06 | La prueba no verificaba la bitácora. Si se registra el evento antes de autorizar (M-E6), el intento denegado queda como “actualizacion” de María y TC-06 sigue aprobando. | Baja | Se añadió la aserción de bitácora vacía tras la denegación | Corregida y verificada |
| W-03 | `actualizar_nota` / TC-06 | El orden autorizar → validar es correcto, pero ninguna prueba lo fijaba (M-E7). Invertido, un docente de otra sede recibiría 400 en lugar de 403 y sabría que su solicitud superó la autorización. | Baja | Se agregó `test_tc06_sec02_otra_sede_con_nota_invalida_responde_403_antes_que_400` | Corregida y verificada |
| W-04 | TC-02 / `SeguridadJania` | TC-02 inspecciona solo `auditoria[-1]`, y las clases `SeguridadWilberth` y `SeguridadJania` duplican `assertSinDatosProtegidos` y `assertExpedientesIntactos`. Afecta el mantenimiento, no el control. | Baja | Se recomienda una clase base común y comprobar la cantidad de eventos. No se aplicó para conservar las pruebas tal como aparecen en los registros TDD | Abierta (mejora) |

## Respuesta del autor a las observaciones de la revisora (J-01 a J-03)

| ID | Acción tomada por Wilberth | Estado |
| --- | --- | --- |
| J-01 | Se agregó `test_tc05_sec01_docente_no_lee_expediente_de_otra_sede`: María recibe 403 sin datos ni titular y Pedro recibe 200; el mutante M-L2 ya no sobrevive | Corregida y verificada |
| J-02 | No se modificó el servicio en este corte. Las lecturas denegadas siguen sin registrarse en la bitácora | Abierta; riesgo residual medio aceptado en el dictamen |
| J-03 | TC-04 comprueba ahora que la denegación no se registra como lectura exitosa y que la bitácora no contiene tokens | Corregida; ampliar cuando se resuelva J-02 |

**Conclusión del revisor:** la política de escritura es correcta en el código. Solo un docente de la misma sede modifica notas; el administrador, cuya sede es `None`, y cualquier rol desconocido quedan denegados por defecto. La autorización se evalúa antes que la validación y la auditoría solo registra cambios efectivos. TC-02 y TC-06 son independientes y comprueban el efecto sobre los datos. Las acciones W-01 a W-03 y J-01 cierran los tres huecos de detección encontrados: con la suite ampliada, los ocho mutantes son detectados. Quedan abiertas W-04 (mantenimiento) y J-02 (auditoría de intentos denegados), sin bloquear la liberación en el laboratorio.

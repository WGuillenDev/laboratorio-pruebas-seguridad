# Acta de inspección cruzada (§7.1)

| Campo | Registro |
| --- | --- |
| Revisora / autor | Jania Hernández Dormuz (revisora) / Wilberth Guillén Aguilar (autor) |
| Fecha | 27/10/2026 |
| Versión revisada | rama `jania`, commit `c3a90da` (incluye todo el código de `wil`) |
| Objetos inspeccionados | Política de lectura `_puede_leer` (src/lab.py) · TC-01 · TC-04 (tests/test_laboratorio.py) |
| Método | Lectura del código y de las pruebas; análisis de mutantes: se eliminó cada regla de `_puede_leer` en una copia y se ejecutó la suite real ([salida](inspeccion_jania.txt), [captura](inspeccion_jania.png)) |
| Preguntas guía | ¿La prueba comprueba el efecto sobre los datos? ¿Es independiente? ¿Puede fallar cuando el control falla? |

## Resultado del análisis de mutantes

```
M-L1  DETECTADO  Estudiante lee cualquier expediente    -> test_tc04_sec01_estudiante_no_lee_expediente_ajeno_ni_filtra_datos
M-L2  SOBREVIVE  Docente lee cualquier sede             -> ninguna prueba automatizada falla
M-L3  DETECTADO  Administrador no puede leer            -> test_tc03_sec01_administrador_lee_ambas_sedes_sin_alterarlas
```

## Respuestas a las preguntas guía

| Prueba | ¿Comprueba el efecto sobre los datos? | ¿Es independiente? | ¿Puede fallar si el control falla? |
| --- | --- | --- | --- |
| TC-01 | Sí: compara la respuesta completa, los expedientes antes/después y el evento de auditoría | Sí: estado nuevo en `setUp` | Sí: detecta la pérdida de la auditoría; la regla de titular la protege TC-04 |
| TC-04 | Sí: copia profunda antes/después y ausencia de id, estudiante, sede, nota y titular | Sí: estado nuevo en `setUp` | Sí: el mutante M-L1 hace fallar TC-04 |

## Observaciones preparadas por el autor (O-01 a O-08)

| ID | Decisión de la revisora | Estado al 27/10/2026 |
| --- | --- | --- |
| O-01 | Confirmada. TC-01 verifica respuesta, estado y auditoría sin token. | Corregida |
| O-02 | Confirmada. TC-04 revisa todos los campos protegidos y el titular. | Corregida |
| O-03 | Confirmada en el código: `_puede_leer` compara la sede del docente. Ver J-01: la regla no tiene prueba automatizada. | Corregida (verificada solo por HTTP manual, TC-05) |
| O-04 | Confirmada. | Corregida por Jania en el TDD 2 (`d3c21c3`, `5c7ea11`, `6d0eee5`) |
| O-05 | Confirmada. | Corregida por Jania en `f5fb01a` (evento con usuario, sin token) |
| O-06 | Confirmada: `leer_expediente` responde 404 antes de autorizar. | Abierta, severidad baja (riesgo residual) |
| O-07 | Confirmada: `revocar_sesion` no comprueba si la sesión ya expiró. | Abierta, severidad baja (riesgo residual) |
| O-08 | Confirmada: el estado del servidor se comparte entre hilos sin bloqueo. | Aceptada como limitación del laboratorio |

## Observaciones nuevas de la revisora

| ID | Objeto | Observación | Severidad | Acción propuesta |
| --- | --- | --- | --- | --- |
| J-01 | `_puede_leer` / suite | Si se elimina la regla de sede del docente (mutante M-L2), **ninguna prueba automatizada falla**: TC-05 solo se ejecuta a mano por HTTP. | Media | Agregar una prueba de unidad para TC-05 (María lee el 202 → 403 sin datos), para que la regresión sea automática |
| J-02 | `leer_expediente` | Las lecturas denegadas (403) no se registran en la bitácora; solo se auditan las permitidas. Un intento de acceso indebido no deja rastro (SEC-06). | Media | Registrar también los intentos denegados, con usuario, id y resultado, sin token |
| J-03 | TC-04 | La prueba no verifica qué ocurre con la bitácora ante la denegación, por lo que no detectaría J-02 ni un registro con token en ese camino. | Baja | Añadir una aserción sobre la bitácora cuando se resuelva J-02 |

**Conclusión de la revisora:** la política de lectura es correcta en el código y deniega por defecto los roles desconocidos. TC-01 y TC-04 son independientes, comprueban el efecto sobre los datos y fallan cuando su control falla. Quedan dos mejoras de severidad media (J-01, J-02) que no bloquean la liberación en el laboratorio, pero deben registrarse como riesgo residual o resolverse.

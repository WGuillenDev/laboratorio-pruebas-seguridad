# Ciclo TDD 1: autorización de lectura

Requisito: SEC-01. Caso planificado: TC-04. Hallazgo: H-01. Responsable: Wilberth.

Resumen visual de las tres fases con identificación RGB y enlaces a las evidencias originales: [tdd1_resumen_rgb.html](tdd1_resumen_rgb.html). El informe editable conserva el formato negro solicitado por el equipo.

## ROJO — ejecutado

- Fecha de la sesión: 25 de octubre de 2026, Costa Rica.
- Entorno: Windows, Python 3.14.7 y PowerShell; versión de PowerShell no registrada.
- Base del proyecto: `3a27a6f8aca674c3459b377e044e3dc30f405a4e`.
- Estado al ejecutar: prueba modificada por Wilberth en su copia de trabajo; `src/lab.py` sin cambios frente a la base.
- Cambio de la prueba: copia profunda de expedientes antes de solicitar el 202 con `lab-ana`; aserciones de 403, ausencia de campos protegidos y conservación de expedientes.
- Commit de la etapa roja: `4cf28d2`. El [tdd1_rojo_cambios.patch](tdd1_rojo_cambios.patch) conserva también el cambio de la prueba relativo a la base indicada.

Desde `entrega/laboratorio_seguridad`, Wilberth ejecutó:

```powershell
python -m unittest discover -s tests -k test_rojo_estudiante_no_consulta_expediente_ajeno -v 2>&1 | Tee-Object -FilePath ..\evidencias\tdd1_rojo.txt
```

Resultado real: una prueba ejecutada en 0.002 segundos; un fallo. La aserción esperaba `403` y recibió `200`, con el mensaje «Ana no debe consultar el expediente 202 de Luis». Es el fallo de autorización esperado, no un fallo de sintaxis, importación o instalación.

Las aserciones posteriores de ausencia de datos protegidos y conservación del estado aún no se ejecutan, porque la primera aserción falla. Su cumplimiento queda pendiente de verificar durante el verde.

Evidencias conservadas:

- [Salida original](tdd1_rojo.txt).
- [Captura aportada por Wilberth](tdd1_rojo.png).
- [Cambio de la prueba](tdd1_rojo_cambios.patch).

El encabezado `NativeCommandError` es el tratamiento de stderr por PowerShell durante la captura; la causa funcional se identifica en `AssertionError: 403 != 200`.

## VERDE — ejecutado

Wilberth añadió a `leer_expediente` una condición antes de registrar y devolver el expediente: si el usuario es estudiante y el titular del expediente no coincide con su identidad, devolver `403` con un mensaje genérico. Se corrigió la sangría de ese bloque con asistencia; no se cambió el oráculo de la prueba.

La base de esta etapa es el commit rojo `4cf28d2`; la modificación funcional aún estaba en la copia de trabajo al ejecutarse. El [diff del cambio mínimo](tdd1_verde_cambios.patch) identifica ese cambio, posteriormente guardado en el commit verde `e4cc9fc`.

Desde `entrega/laboratorio_seguridad`, Wilberth ejecutó:

```powershell
python -m unittest discover -s tests -k test_rojo_estudiante_no_consulta_expediente_ajeno -v 2>&1 | Tee-Object -FilePath ..\evidencias\tdd1_verde.txt
```

Resultado real: una prueba ejecutada en 0.000 segundos; `OK`. En esta ejecución pasan las aserciones de código `403`, ausencia de los campos `id`, `estudiante`, `sede` y `nota`, y conservación de los expedientes. La evidencia respalda el escenario de estudiante sobre expediente ajeno; no demuestra todavía la política completa de todos los roles ni constituye una ejecución de regresión.

Evidencias: [salida original](tdd1_verde.txt), [captura aportada por Wilberth](tdd1_verde.png) y [diff](tdd1_verde_cambios.patch). El encabezado `NativeCommandError` de PowerShell también aparece ante `ok`; el resultado de unittest es `OK`.

## REFACTOR — ejecutado

Wilberth extrajo la condición a `_estudiante_solicita_expediente_ajeno(usuario, expediente)` y reemplazó la expresión original por una llamada a esa función. Conservó la misma regla y la misma respuesta de denegación. La base es el commit verde `e4cc9fc`; el refactor estaba sin commit al ejecutar la regresión.

Desde `entrega/laboratorio_seguridad`, ejecutó:

```powershell
python -m unittest discover -s tests -k estudiante -k docente -v 2>&1 | Tee-Object -FilePath ..\evidencias\tdd1_refactor.txt
```

Resultado observado: tres pruebas ejecutadas en 0.000 segundos; `OK`. Pasan la consulta del expediente propio, la denegación de expediente ajeno y la modificación legítima de nota por el docente. Esta ejecución comprueba el caso objetivo y la regresión de los casos seleccionados; no es una ejecución de toda la suite.

Evidencias: [salida original](tdd1_refactor.txt), [captura aportada por Wilberth](tdd1_refactor.png) y [diff del refactor](tdd1_refactor_cambios.patch).

### Suite completa después del refactor

Wilberth ejecutó desde `entrega/laboratorio_seguridad`:

```powershell
python -m unittest discover -s tests -v 2>&1 | Tee-Object -FilePath ..\evidencias\tdd1_suite_completa.txt
```

Resultado real: cuatro pruebas ejecutadas en 0.029 segundos; tres aprobadas y una fallida. Aprueban la consulta propia, la modificación legítima del docente y el rechazo del expediente ajeno. Falla únicamente `test_rojo_sesion_revocada_no_permita_lecturas`, con `401 != 200`, correspondiente a H-02 y al bloque pendiente de Jania.

Evidencias: [salida original de toda la suite](tdd1_suite_completa.txt) y [captura aportada por Wilberth](tdd1_suite_completa.png).

### Balance del ciclo

Se conservaron las tres etapas del escenario TC-04: rojo por la causa esperada, verde con el cambio mínimo y refactor con el caso objetivo y dos casos relacionados aprobados. H-01 se clasifica como corregido y verificado para el acceso de estudiante a expediente ajeno. Esto no cierra la totalidad de SEC-01: aún corresponde ampliar y comprobar la política de lectura de los demás roles.

La suite completa todavía no está en verde por el defecto de sesión ya conocido. No se omite ni se altera esa prueba para aparentar aprobación total. Esta ejecución tampoco sustituye las dos ejecuciones finales en limpio después de integrar ambos bloques. El refactor quedó guardado en `9525e75`; el diff preservado identifica el cambio respecto de `e4cc9fc`.

## Evolución posterior de los nombres

Después del ciclo, durante la ampliación del bloque de Wilberth, la prueba histórica de acceso ajeno pasó a llamarse `test_tc04_sec01_estudiante_no_lee_expediente_ajeno_ni_filtra_datos`, en `SeguridadWilberth`. Los logs anteriores conservan los nombres que existían en cada commit. Para reproducir el escenario en la versión actual, usar `python -m unittest discover -s tests -k tc04 -v`; para repetir el estado histórico, consultar el commit correspondiente sin sobrescribir la copia de trabajo del equipo.

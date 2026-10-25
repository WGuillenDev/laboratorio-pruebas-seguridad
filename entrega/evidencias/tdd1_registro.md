# Ciclo TDD 1: autorización de lectura

Requisito: SEC-01. Caso planificado: TC-04. Hallazgo: H-01. Responsable: Wilberth.

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

La base de esta etapa es el commit rojo `4cf28d2`; la modificación funcional aún estaba en la copia de trabajo al ejecutarse. El [diff del cambio mínimo](tdd1_verde_cambios.patch) permite identificarla antes del commit verde.

Desde `entrega/laboratorio_seguridad`, Wilberth ejecutó:

```powershell
python -m unittest discover -s tests -k test_rojo_estudiante_no_consulta_expediente_ajeno -v 2>&1 | Tee-Object -FilePath ..\evidencias\tdd1_verde.txt
```

Resultado real: una prueba ejecutada en 0.000 segundos; `OK`. En esta ejecución pasan las aserciones de código `403`, ausencia de los campos `id`, `estudiante`, `sede` y `nota`, y conservación de los expedientes. La evidencia respalda el escenario de estudiante sobre expediente ajeno; no demuestra todavía la política completa de todos los roles ni constituye una ejecución de regresión.

Evidencias: [salida original](tdd1_verde.txt), [captura aportada por Wilberth](tdd1_verde.png) y [diff](tdd1_verde_cambios.patch). El encabezado `NativeCommandError` de PowerShell también aparece ante `ok`; el resultado de unittest es `OK`.

## REFACTOR — pendiente

Pendiente de mejora de estructura, repetición de la prueba y regresión de los casos relacionados. El defecto de sesiones corresponde al bloque de Jania y no se dará por corregido durante este ciclo.

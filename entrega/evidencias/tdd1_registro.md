# Ciclo TDD 1: autorización de lectura

Requisito: SEC-01. Caso planificado: TC-04. Hallazgo: H-01. Responsable: Wilberth.

## ROJO — ejecutado

- Fecha de la sesión: 25 de octubre de 2026, Costa Rica.
- Entorno: Windows, Python 3.14.7 y PowerShell; versión de PowerShell no registrada.
- Base del proyecto: `3a27a6f8aca674c3459b377e044e3dc30f405a4e`.
- Estado al ejecutar: prueba modificada por Wilberth en su copia de trabajo; `src/lab.py` sin cambios frente a la base.
- Cambio de la prueba: copia profunda de expedientes antes de solicitar el 202 con `lab-ana`; aserciones de 403, ausencia de campos protegidos y conservación de expedientes.
- Identificación del cambio previo al commit: [tdd1_rojo_cambios.patch](tdd1_rojo_cambios.patch), relativo a la base indicada. El commit de esta etapa se identificará en el historial una vez creado.

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

## VERDE — pendiente

Pendiente de cambio mínimo en la autorización de lectura y ejecución de la prueba por Wilberth.

## REFACTOR — pendiente

Pendiente de mejora de estructura, repetición de la prueba y regresión de los casos relacionados. El defecto de sesiones corresponde al bloque de Jania y no se dará por corregido durante este ciclo.

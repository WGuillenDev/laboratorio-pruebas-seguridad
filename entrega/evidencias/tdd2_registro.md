# Ciclo TDD 2: validez de sesión

Requisito: SEC-03. Caso planificado: TC-08. Hallazgo: H-02. Responsable: Jania.

Entorno: Windows, Python 3.13.14, ejecución desde `entrega/laboratorio_seguridad`. Fecha: 2026-10-26. Base: rama `wil` (commit `5a41a2c`).

## ROJO — commit `d3c21c3`

Se reemplazó el ejemplo original `test_rojo_sesion_revocada_no_permita_lecturas` por `test_tc08_sec03_sesion_revocada_o_invalida_no_lee_ni_modifica`, con tres variantes (sesión revocada de María, token vacío y token inexistente) que intentan leer el 101 y cambiar su nota. Oráculo: 401 en ambas operaciones, sin campos protegidos y expedientes intactos.

```powershell
py -m unittest discover -s tests -k test_tc08 -v
```

Resultado real: Ran 1 tests in 0.003s · FAILED failures=1. Falla la variante `revocada` con `AssertionError: 401 != 200`: la causa es el defecto H-02 (autenticar ignora el indicador de revocación), no un error de la prueba. Las variantes de token vacío e inexistente ya respondían 401.

Evidencias: [salida](tdd2_rojo.txt) y [captura](tdd2_rojo.png).

## VERDE — commit `5c7ea11`

Cambio mínimo en `autenticar()`: si la sesión está revocada o expirada, devolver `None`. No se modificó el oráculo de la prueba.

```powershell
py -m unittest discover -s tests -k test_tc08 -v
```

Resultado real: Ran 1 tests in 0.001s · OK. Evidencias: [salida](tdd2_verde.txt) y [captura](tdd2_verde.png).

## REFACTOR — commit `6d0eee5`

Se extrajo la regla a `_sesion_vigente(sesion)` sin cambiar el comportamiento, y se ejecutó la suite completa como regresión.

```powershell
py -m unittest discover -s tests -v
```

Resultado real: Ran 6 tests in 0.008s · OK. Evidencias: [salida](tdd2_refactor.txt) y [captura](tdd2_refactor.png).

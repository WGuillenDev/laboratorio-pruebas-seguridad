# Resultados del bloque de Jania

Entorno: Windows, Python 3.13.14, laboratorio local 127.0.0.1. Fecha: 2026-10-26.

| Etapa | Commit | Comando | Resultado | Evidencia |
| --- | --- | --- | --- | --- |
| HTTP antes de corregir | `5a41a2c` (base) | `manual_jania.ps1` | TC-06: Antes: cambio 200 y nota del 202 = 70 (persistió). TC-09: Antes: lectura 200 con datos y cambio 403 | [txt](jania_api_antes.txt), [png](jania_api_antes.png), [json](jania_api_antes.json) |
| TDD 2 rojo | `d3c21c3` | `-k test_tc08 -v` | Ran 1 tests in 0.003s · FAILED failures=1 | [tdd2_registro.md](tdd2_registro.md) |
| TDD 2 verde | `5c7ea11` | `-k test_tc08 -v` | Ran 1 tests in 0.001s · OK | [txt](tdd2_verde.txt) |
| TDD 2 refactor | `6d0eee5` | suite completa | Ran 6 tests in 0.008s · OK | [txt](tdd2_refactor.txt) |
| Escritura rojo (TC-02, TC-06) | `1789c6f` | `-k SeguridadJania -v` | Ran 3 tests in 0.005s · FAILED failures=2 | [txt](jania_escritura_rojo.txt), [png](jania_escritura_rojo.png) |
| Escritura verde (H-06, H-05) | `f5fb01a` | `-k SeguridadJania -v` | Ran 3 tests in 0.001s · OK | [txt](jania_escritura_verde.txt), [png](jania_escritura_verde.png) |
| Integración HTTP TC-10, TC-11 | `0d74bec` | `-p test_integracion_http.py -v` | Ran 2 tests in 1.055s · OK | [txt](jania_integracion.txt), [png](jania_integracion.png) |
| Suite completa, corrida limpia 1 | `0d74bec` | `discover -s tests -v` | Ran 9 tests in 1.063s · OK | [txt](jania_suite_corrida1.txt), [png](jania_suite_corrida1.png) |
| Suite completa, corrida limpia 2 | `0d74bec` | `discover -s tests -v` | Ran 9 tests in 1.038s · OK | [txt](jania_suite_corrida2.txt), [png](jania_suite_corrida2.png) |
| HTTP después de corregir | `0d74bec` | `manual_jania.ps1` | TC-06: después: 403 sin datos y nota del 202 = 91 (intacta). TC-09: después: lectura 401 y cambio 401 sin datos; nota del 101 = 82 (intacta) | [txt](jania_api_despues.txt), [png](jania_api_despues.png), [json](jania_api_despues.json) |

Las pruebas manuales reinician el servidor por caso y comparan el expediente con una lectura del administrador antes y después del intento.

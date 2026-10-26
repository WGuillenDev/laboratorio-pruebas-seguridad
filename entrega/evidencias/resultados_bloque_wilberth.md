# Resultados del bloque de Wilberth

- **Fecha:** 25/10/2026
- **Versión:** commit `8e98b14` (rama `wil`). Las corridas se registraron antes del commit; los hashes de `version_bloque_wilberth.json` coinciden con los archivos de `8e98b14`.
- **Entorno:** Windows 11, Python 3.14.7, `unittest`, `curl.exe`. Sin dependencias externas.
- **Casos del bloque:** TC-01, TC-03, TC-04, TC-05, TC-07 y TC-12.

## Ejecuciones

| Ejecución | Comando | Resultado | Evidencia |
| --- | --- | --- | --- |
| Antes de corregir la auditoría | `python -m unittest discover -s tests -k SeguridadWilberth -v` | TC-01 y TC-03 fallan: el evento no identifica al usuario (H-05) | `wilberth_unidad_antes.txt` |
| Corrida limpia 1 | mismo comando, proceso nuevo | 4/4 OK | `wilberth_unidad_corrida1.txt` |
| Corrida limpia 2 | mismo comando, proceso nuevo | 4/4 OK | `wilberth_unidad_corrida2.txt` |
| Suite completa del equipo | `python -m unittest discover -s tests -v` | 6 pruebas: 5 OK, 1 fallo esperado (H-02) | `suite_parcial_equipo.txt`, `verificacion_wilberth.png` |
| TC-05 por HTTP | `GET /expedientes/202` con `lab-maria` | Antes: 200 con datos de Luis. Después: 403 sin datos; Pedro 200; estado intacto | `wilberth_api_antes.txt`, `wilberth_api_despues.txt` |
| TC-12 por HTTP | `POST /expedientes/101/nota` con 5 variantes | Antes: -1, 101, true y el entero enorme persistían. Después: las 5 → 400; estado intacto | `wilberth_api_antes.txt`, `wilberth_api_despues.txt` |

Cada prueba unitaria crea su estado en `setUp()`; el servidor se reinició antes de cada escenario HTTP. Las corridas asistidas están identificadas en cada registro; Wilberth las repitió en su terminal (`verificacion_wilberth.png`, `verificacion_http_*.png`).

## Estado de los 12 casos en este corte

| Estado | Casos | Total |
| --- | --- | --- |
| Aprobado | TC-01, TC-03, TC-04, TC-05, TC-07, TC-12 | 6 |
| Fallido | TC-08 | 1 |
| Bloqueado | — | 0 |
| No ejecutado | TC-02, TC-06, TC-09, TC-10, TC-11 | 5 |

## Indicadores

- Tasa de aprobación = 6 / (6 + 1) × 100 = **85.71 %**
- Avance = (6 + 1) / 12 × 100 = **58.33 %**
- Cobertura de requisitos = 6 / 6 × 100 = **100 %** (cada SEC tiene al menos una prueba válida; SEC-03 cuenta la prueba de revocación que falla y detecta H-02).

## Hallazgos del bloque

| ID | Estado |
| --- | --- |
| H-01 Estudiante lee expediente ajeno | Corregido y verificado (TDD 1) |
| H-03 Docente lee otra sede | Corregido y verificado (TC-05) |
| H-04 Notas inválidas persistidas | Corregido y verificado (TC-12) |
| H-05 Auditoría con token | Lectura corregida; escritura abierta (Jania) |
| H-06 Docente cambia nota de otra sede | Confirmado en revisión estática; abierto (Jania) |

## Dictamen provisional

**NO LIBERAR.** H-02 (sesión revocada) y H-06 (escritura entre sedes) son defectos críticos abiertos; una tasa de aprobación alta no compensa un fallo de autorización. Responsable de la decisión hipotética: Wilberth Guillén Aguilar (responsable de calidad), con revisión de Jania Hernández.

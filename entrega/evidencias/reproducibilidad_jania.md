# Prueba de reproducibilidad con el README (§7.5)

| Campo | Registro |
| --- | --- |
| Ejecutora | Jania Hernández Dormuz (no es autora de la suite de Wilberth) |
| Fecha y entorno | 27/10/2026 · Windows · Python 3.13.14 · Git para Windows · clon nuevo en una carpeta vacía |
| Procedimiento | Clonar, seguir **solo** `entrega/laboratorio_seguridad/README.md` (rama `wil`), ejecutar la suite y el bloque de Wilberth, iniciar la API, consultarla y detenerla. Script: `reproducibilidad.py`; [salida](reproducibilidad_jania.txt), [captura](reproducibilidad_jania.png), [datos](reproducibilidad_jania.json) |
| ¿Los pasos del README fueron suficientes? | Sí: 9 de 9 pasos dieron el resultado indicado |

| Paso | Descripción | Comando | Resultado |
| --- | --- | --- | --- |
| 1 | Clonar el repositorio (README: Requisitos e instalación), intento 1 | `git clone https://github.com/WGuillenDev/laboratorio-pruebas-seguridad.git` | Sin problemas |
| 2 | Cambiar a la rama indicada | `git switch wil` | Sin problemas |
| 3 | Comprobar Python con el comando del README | `python --version` | Sin problemas |
| 4 | Comprobar Git | `git --version` | Sin problemas |
| 5 | Ejecutar la suite completa (README: 'Ran 6 tests' y 'FAILED (failures=1)') | `python -m unittest discover -s tests -v` | Sin problemas |
| 6 | Ejecutar el bloque de Wilberth (README: 'Ran 4 tests' y 'OK') | `python -m unittest discover -s tests -k SeguridadWilberth -v` | Sin problemas |
| 7a | GET /health | `curl.exe /health` | Sin problemas |
| 7b | Consulta del expediente propio (lab-ana) | `curl.exe /expedientes/101` | Sin problemas |
| 7c | Docente de Central consulta 202 (README: debe responder 403) | `curl.exe /expedientes/202` | Sin problemas |

## Dificultades encontradas

- **Primer intento (27/10/2026): fallo del entorno, no del README.** Al clonar, Windows no pudo resolver `github.com` (`Could not resolve host`) por una caída momentánea de internet, y los pasos siguientes no pudieron ejecutarse. Se conserva como [reproducibilidad_jania_intento1.txt](reproducibilidad_jania_intento1.txt) y se repitió la prueba con la red estable.

- El README indica `git switch wil`. Cuando `wil` y `jania` se integren en `main`, esa instrucción y los resultados esperados (6 pruebas, 1 fallo) tendrán que actualizarse.

## Cambios propuestos al README

- Tras integrar las ramas, cambiar `git switch wil` por `main` y actualizar el resultado esperado de la suite (9 pruebas, OK).

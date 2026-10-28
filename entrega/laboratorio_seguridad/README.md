# Laboratorio de Pruebas de Seguridad

Evaluación de seguridad de una API local de expedientes académicos mediante requisitos verificables, pruebas automatizadas y manuales, ciclos TDD y evidencias reproducibles.

## Objetivo

Verificar que la consulta de expedientes y la modificación de calificaciones respetan los permisos de cada rol y sede, la validez de las sesiones y las reglas de validación. Los resultados permitirán documentar defectos, comprobar sus correcciones y fundamentar una decisión de liberación considerando el riesgo residual.

## Estado final (versión `0b456db`)

- Corregidos y verificados: lectura por titular, rol y sede (H-01, H-03); validación de notas (H-04); auditoría de lecturas y escrituras sin token (H-05); sesión revocada/expirada (H-02, TDD 2); cambio de nota entre sedes (H-06).
- Revisiones: inspección cruzada en ambos sentidos ([Jania](../evidencias/inspeccion_cruzada_jania.md) y [Wilberth](../evidencias/inspeccion_cruzada_wilberth.md)) y [prueba de reproducibilidad](../evidencias/reproducibilidad_jania.md) siguiendo este README.
- Riesgo residual: las lecturas denegadas no se registran en la bitácora (J-02). Dictamen: liberar con condiciones (ver informe).

**Uso exclusivamente local:** ejecutar el servidor en `127.0.0.1` y utilizar únicamente las cuentas y los datos sintéticos proporcionados. La autenticación con tokens ficticios es didáctica y no es apta para producción. No exponer el servidor a Internet ni conectarlo a información real.

## Requisitos e instalación

- Python **3.10 o superior**, disponible mediante `python`.
- Git para obtener el proyecto y registrar cambios.
- PowerShell y `curl.exe` para los ejemplos HTTP en Windows.
- Puerto local **8765** disponible al iniciar la API.

El laboratorio utiliza la biblioteca estándar de Python: **no requiere instalar paquetes con `pip` ni configurar servicios externos**.

Desde la carpeta donde se almacenará el repositorio:

```powershell
git clone https://github.com/WGuillenDev/laboratorio-pruebas-seguridad.git
cd laboratorio-pruebas-seguridad
python --version
git --version
cd entrega/laboratorio_seguridad
```

La versión de entrega está en `main`. Si ya está clonado, ejecutar `git switch main` y `git pull` antes de abrir una terminal en `entrega/laboratorio_seguridad`. Los comandos de pruebas y servidor siguientes se ejecutan desde esa carpeta.

## Ejecutar las pruebas automatizadas

```powershell
python -m unittest discover -s tests -v
```

La suite tiene diez pruebas de unidad y dos de integración HTTP; las de integración levantan `servidor.py` solas en un puerto libre, así que **no hace falta iniciar el servidor**. Cada prueba crea un estado independiente mediante `estado_inicial()` en `setUp`.

Resultado esperado en esta versión: `Ran 12 tests` y `OK`.

Ejecutar solo un bloque:

```powershell
python -m unittest discover -s tests -k SeguridadWilberth -v
python -m unittest discover -s tests -k SeguridadJania -v
python -m unittest discover -s tests -p test_integracion_http.py -v
```

| Caso | Ejecución actual | Responsable |
| --- | --- | --- |
| TC-01, TC-03, TC-04 (TDD 1), TC-05, TC-07, TC-12 | Unidad automatizada, clase `SeguridadWilberth` | Wilberth |
| TC-05, TC-12 | HTTP manual con curl; ver "Solicitudes de referencia" | Wilberth |
| TC-02, TC-06, TC-08 | Unidad automatizada, clase `SeguridadJania` (TC-08 = TDD 2) | Jania |
| TC-06, TC-09 | HTTP manual; ver `evidencias/resultados_bloque_jania.md` | Jania |
| TC-10, TC-11 | Integración HTTP automatizada, `tests/test_integracion_http.py` | Jania |

Los diseños completos, estados y vínculos requisito-riesgo-caso están en [la matriz de trazabilidad](../matriz_trazabilidad.csv). Un método de ejemplo aprobado no acredita por sí solo todos los oráculos del caso planificado.

## Iniciar la API local

En una terminal ubicada en `entrega/laboratorio_seguridad`:

```powershell
python servidor.py
```

El servidor escucha en `http://127.0.0.1:8765`. Mantener esa terminal abierta y utilizar otra para las solicitudes HTTP. Para detenerlo, presionar **Ctrl+C** en la terminal del servidor.

Comprobar disponibilidad desde la segunda terminal:

```powershell
curl.exe -i http://127.0.0.1:8765/health
```

La respuesta esperada es `200` con `{"estado": "laboratorio"}`. El endpoint de salud comprueba disponibilidad; no demuestra que funcionen los controles de seguridad.

## Cuentas y política de acceso esperada

| Cuenta | Rol | Token sintético | Sede | Permisos |
| --- | --- | --- | --- | --- |
| Ana | Estudiante | `lab-ana` | Central | Consultar únicamente su expediente, 101 |
| Luis | Estudiante | `lab-luis` | Pacífico | Consultar únicamente su expediente, 202 |
| María | Docente | `lab-maria` | Central | Consultar expedientes y modificar notas de su sede |
| Pedro | Docente | `lab-pedro` | Pacífico | Consultar expedientes y modificar notas de su sede |
| Admin | Administrador | `lab-admin` | Global | Consultar ambas sedes; no modificar notas |
| Ana con sesión vencida | Estudiante | `lab-vencida` | Central | Sin acceso a operaciones protegidas |

Las sesiones ausentes, desconocidas, revocadas o vencidas deben impedir el acceso a información protegida. Las notas deben ser valores numéricos válidos entre **0 y 100**, incluidos ambos extremos.

| Resultado esperado | Código HTTP |
| --- | --- |
| Operación permitida | `200` |
| Sesión ausente o inválida | `401` |
| Permiso insuficiente | `403` |
| Entrada inválida | `400` |
| Recurso inexistente | `404` |

Esta política describe el comportamiento que se debe verificar. Las denegaciones no deben incluir notas ni información protegida; las operaciones rechazadas deben conservar los expedientes sin cambios. Comprobar únicamente el código HTTP no basta para validar una prueba.

## Solicitudes de referencia

Consulta del expediente propio:

```powershell
curl.exe -i -H "Authorization: Bearer lab-ana" http://127.0.0.1:8765/expedientes/101
```

Consulta de otra sede por una docente; según la política debe responder `403`:

```powershell
curl.exe -i -H "Authorization: Bearer lab-maria" http://127.0.0.1:8765/expedientes/202
```

Actualización por una docente de la misma sede:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8765/expedientes/101/nota" -Method Post -Headers @{ Authorization = "Bearer lab-maria" } -ContentType "application/json" -Body '{"nota":85}'
```

Revocación de una sesión sintética:

```powershell
curl.exe -i -X POST -H "Authorization: Bearer lab-ana" http://127.0.0.1:8765/sesiones/revocar
```

Las solicitudes de actualización y revocación modifican el estado en memoria. Estos ejemplos no sustituyen los casos documentados ni sus evidencias.

Para repetir TC-05, iniciar con datos limpios, consultar ambos expedientes como administrador antes y después de solicitar el 202 con `lab-maria`, y comprobar `403` sin campos protegidos ni cambios. La lectura del mismo recurso con `lab-pedro` debe devolver `200`.

Para repetir TC-12 en PowerShell, reiniciar el servidor por variante y cambiar el cuerpo entre `{"nota":-1}`, `{"nota":101}`, `{"nota":"ochenta"}`, `{"nota":true}` y un entero de 401 cifras (1 seguido de 400 ceros). El entero se envía como número JSON, no como expresión `10**400`. Guardar el cuerpo en un archivo ASCII temporal evita problemas de comillas con curl en PowerShell:

```powershell
'{"nota":101}' | Set-Content -LiteralPath "$env:TEMP\nota-invalida-lab.json" -Encoding ascii
curl.exe -i -H "Authorization: Bearer lab-maria" -H "Content-Type: application/json" --data-binary "@$env:TEMP\nota-invalida-lab.json" http://127.0.0.1:8765/expedientes/101/nota
```

Comparar ambos expedientes por GET autorizado antes y después de cada intento: se espera `400` y estado intacto. Los [registros antes](../evidencias/wilberth_api_antes.txt) y [después](../evidencias/wilberth_api_despues.txt) incluyen los comandos reales, los cuerpos exactos y los resultados, con reinicio por variante.

## Restablecer los datos sintéticos

1. Detener el servidor con **Ctrl+C**.
2. Desde `entrega/laboratorio_seguridad`, volver a ejecutar `python servidor.py`.

El reinicio restaura los expedientes, las sesiones y la auditoría en memoria. El expediente 101 comienza con nota **82** y el 202 con **91**. Las sesiones ordinarias vuelven a estar activas y `lab-vencida` permanece expirada. No hay base de datos ni archivos de persistencia que deban eliminarse.

Para repetir la suite unitaria en estado limpio, ejecutar de nuevo el comando de `unittest`: `setUp` restablece los datos antes de cada prueba. Las dos ejecuciones finales están registradas con versión, Python, comando y resultado en [corrida 1](../evidencias/suite_final_corrida1.txt) y [corrida 2](../evidencias/suite_final_corrida2.txt).

## Estructura de la entrega

```text
entrega/
├── informe_seguridad.pdf
├── laboratorio_seguridad/
│   ├── README.md
│   ├── servidor.py
│   ├── src/
│   │   ├── __init__.py
│   │   └── lab.py
│   └── tests/
│       ├── test_laboratorio.py
│       └── test_integracion_http.py
├── evidencias/
├── hallazgos.csv
└── matriz_trazabilidad.csv
```

| Elemento | Contenido |
| --- | --- |
| `src/lab.py` | Lógica de sesiones, permisos, notas y auditoría |
| `servidor.py` | API HTTP local |
| `tests/` | Pruebas automatizadas |
| `../evidencias/` | Registros reales de TDD, ejecuciones, pruebas manuales y revisiones |
| `../hallazgos.csv` | Defectos demostrados, tratamiento y verificación |
| `../matriz_trazabilidad.csv` | Vínculos entre requisitos, riesgos, casos y evidencia esperada |
| `../informe_seguridad.pdf` | Informe técnico, resultados, indicadores y dictamen |

La revisión estática examina el código sin ejecutarlo; las solicitudes HTTP evalúan el comportamiento dinámico. La [revisión estática](../evidencias/revision_estatica.md) identifica los controles que se corrigieron. Las tareas de Jania se gestionaron en el [issue de su bloque](https://github.com/WGuillenDev/laboratorio-pruebas-seguridad/issues/2).

La matriz distingue casos aprobados, fallidos, bloqueados y no ejecutados. Las dos ejecuciones finales completas se hicieron después de integrar ambos bloques.

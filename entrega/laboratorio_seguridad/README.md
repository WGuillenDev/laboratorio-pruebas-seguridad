# Laboratorio de Pruebas de Seguridad

Evaluación de seguridad de una API local de expedientes académicos mediante requisitos verificables, pruebas automatizadas y manuales, ciclos TDD y evidencias reproducibles.

## Objetivo

Verificar que la consulta de expedientes y la modificación de calificaciones respetan los permisos de cada rol y sede, la validez de las sesiones y las reglas de validación. Los resultados permitirán documentar defectos, comprobar sus correcciones y fundamentar una decisión de liberación considerando el riesgo residual.

## Estado actual

El bloque de Wilberth contiene cuatro casos unitarios aprobados y dos casos HTTP comprobados antes y después de corregir. Se completaron los permisos de lectura por propietario/rol/sede, la validación de notas y la auditoría de lecturas sin tokens.

La suite actual tiene seis métodos: cinco aprueban y uno falla por el defecto conocido de sesión revocada, pendiente del bloque de Jania. También están pendientes la autorización de modificación por sede, la auditoría de actualizaciones, la integración HTTP de los límites y el segundo ciclo TDD. El informe es un corte parcial; no representa una liberación del sistema.

La versión editable actual está en [informe_seguridad.docx](../informe_seguridad.docx), con Arial 12, texto negro y tablas simples. El PDF incluido refleja el mismo avance parcial; al completar y revisar ambos bloques se exportará de nuevo el Word al PDF final exigido en la entrega.

La campaña prevista comprende 12 casos distintos: 3 positivos, 6 negativos y 3 de frontera; al menos 8 automatizados, con pruebas unitarias y de integración, y 4 manuales por HTTP. Se documentarán dos ciclos TDD, revisión estática, inspección cruzada y dos ejecuciones finales en estado limpio.

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
git switch wil
python --version
git --version
cd entrega/laboratorio_seguridad
```

El avance de este corte se publica en `wil`; `main` solo lo incluirá después de aprobar el PR. Si ya está clonado, actualizar las referencias antes de seleccionar esa rama y abrir una terminal en `entrega/laboratorio_seguridad`. Los comandos de pruebas y servidor siguientes se ejecutan desde esa carpeta.

## Ejecutar las pruebas automatizadas

```powershell
python -m unittest discover -s tests -v
```

Las seis pruebas unitarias actuales no requieren iniciar el servidor. Cada prueba crea un estado independiente mediante `estado_inicial()` en `setUp`.

Resultado observado de este corte: `Ran 6 tests` y `FAILED (failures=1)`. El único fallo es `test_rojo_sesion_revocada_no_permita_lecturas` (`401 != 200`): el defecto no se ocultó ni se corrigió antes de que Jania documente su TDD.

Para ejecutar únicamente los cuatro casos automatizados de Wilberth:

```powershell
python -m unittest discover -s tests -k SeguridadWilberth -v
```

Resultado observado: `Ran 4 tests` y `OK`, en dos procesos independientes. La [verificación en la terminal de Wilberth](../evidencias/verificacion_wilberth.png) confirma tanto este bloque como el fallo pendiente de toda la suite.

Las pruebas de integración se incorporarán durante el desarrollo. Este apartado se actualizará con sus condiciones de ejecución cuando estén implementadas.

| Caso | Ejecución actual | Responsable |
| --- | --- | --- |
| TC-01, TC-03, TC-04, TC-07 | Unidad automatizada, clase `SeguridadWilberth` | Wilberth |
| TC-05, TC-12 | Solicitudes curl; comandos, cuerpos y respuestas en evidencias antes/después | Wilberth, con ejecución asistida identificada |
| TC-02, TC-08 | Ejemplos originales por completar; TC-08 ya demuestra un defecto | Jania |
| TC-06, TC-09 | HTTP manual pendiente | Jania |
| TC-10, TC-11 | Integración HTTP automatizada pendiente | Jania |

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

Esta política describe el comportamiento que se debe verificar. Existen controles pendientes indicados en el estado actual. Las denegaciones no deben incluir notas ni información protegida; las operaciones rechazadas deben conservar los expedientes sin cambios. Comprobar únicamente el código HTTP no basta para validar una prueba.

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

Para repetir la suite unitaria en estado limpio, ejecutar de nuevo el comando de `unittest`: `setUp` restablece los datos antes de cada prueba. Las dos ejecuciones finales deberán registrarse con la versión del proyecto, la versión de Python, el comando utilizado y el resultado real.

## Estructura de la entrega

```text
entrega/
├── informe_seguridad.pdf
├── informe_seguridad.docx
├── laboratorio_seguridad/
│   ├── README.md
│   ├── servidor.py
│   ├── src/
│   │   ├── __init__.py
│   │   └── lab.py
│   └── tests/
│       └── test_laboratorio.py
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
| `../informe_seguridad.docx` | Fuente editable actual para completar y revisar el informe |

La revisión estática examina el código sin ejecutarlo; las solicitudes HTTP evalúan el comportamiento dinámico. La [revisión estática](../evidencias/revision_estatica.md) identifica los controles pendientes. Las tareas de Jania, incluida la revisión y modificación del informe, se gestionan en el [issue de su bloque](https://github.com/WGuillenDev/laboratorio-pruebas-seguridad/issues/2).

La matriz distingue casos aprobados, fallidos, bloqueados y no ejecutados. Las dos corridas parciales de Wilberth no sustituyen las dos ejecuciones finales completas después de integrar ambos bloques.

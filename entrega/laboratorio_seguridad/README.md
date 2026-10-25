# Laboratorio de Pruebas de Seguridad

Evaluación de seguridad de una API local de expedientes académicos mediante requisitos verificables, pruebas automatizadas y manuales, ciclos TDD y evidencias reproducibles.

## Objetivo

Verificar que la consulta de expedientes y la modificación de calificaciones respetan los permisos de cada rol y sede, la validez de las sesiones y las reglas de validación. Los resultados permitirán documentar defectos, comprobar sus correcciones y fundamentar una decisión de liberación considerando el riesgo residual.

## Estado actual

El proyecto conserva el código base con defectos didácticos intencionales. La suite inicial contiene cuatro pruebas unitarias; dos están diseñadas para evidenciar fallos de autorización y revocación de sesiones. Las pruebas adicionales, correcciones y evidencias están pendientes de desarrollo y ejecución. El PDF está vacío, reservado para el informe, y los CSV contienen únicamente encabezados.

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
python --version
git --version
cd entrega/laboratorio_seguridad
```

Si ya está clonado, abrir una terminal en `entrega/laboratorio_seguridad` dentro del repositorio. Los comandos de pruebas y servidor siguientes se ejecutan desde esa carpeta.

## Ejecutar las pruebas automatizadas

```powershell
python -m unittest discover -s tests -v
```

Las cuatro pruebas unitarias actuales no requieren iniciar el servidor. Cada prueba crea un estado independiente mediante `estado_inicial()` en `setUp`.

En la base se esperan dos fallos intencionales: lectura de un expediente ajeno y lectura con una sesión revocada. Esta descripción corresponde al diseño de la suite y no constituye un registro de ejecución. Los fallos deben analizarse y registrarse antes de corregirlos; no implican necesariamente un problema de instalación.

Las pruebas de integración se incorporarán durante el desarrollo. Este apartado se actualizará con sus condiciones de ejecución cuando estén implementadas.

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

Esta política describe el comportamiento que se debe verificar. El código inicial contiene defectos y puede incumplirla. Las denegaciones no deben incluir notas ni información protegida; las operaciones rechazadas deben conservar los expedientes sin cambios. Comprobar únicamente el código HTTP no basta para validar una prueba.

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

## Restablecer los datos sintéticos

1. Detener el servidor con **Ctrl+C**.
2. Desde `entrega/laboratorio_seguridad`, volver a ejecutar `python servidor.py`.

El reinicio restaura los expedientes, las sesiones y la auditoría en memoria. El expediente 101 comienza con nota **82** y el 202 con **91**. Las sesiones ordinarias vuelven a estar activas y `lab-vencida` permanece expirada. No hay base de datos ni archivos de persistencia que deban eliminarse.

Para repetir la suite unitaria en estado limpio, ejecutar de nuevo el comando de `unittest`: `setUp` restablece los datos antes de cada prueba. Las dos ejecuciones finales deberán registrarse con la versión del proyecto, la versión de Python, el comando utilizado y el resultado real.

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

La revisión estática examina el código sin ejecutarlo; las solicitudes HTTP evalúan el comportamiento dinámico. El informe y las evidencias se completarán con los resultados observados, diferenciando casos aprobados, fallidos, bloqueados y no ejecutados.

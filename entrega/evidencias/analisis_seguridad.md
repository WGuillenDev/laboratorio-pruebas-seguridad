# Análisis de seguridad: activos, amenazas y requisitos

Documento de soporte de las secciones 2 y 3 de `informe_seguridad.pdf`. Versión del proyecto: `8e98b14`.

## Alcance

Dos expedientes sintéticos: 101 de Ana (Central, nota 82) y 202 de Luis (Pacífico, nota 91). Se evalúan lectura, cambio de notas, validez de sesiones, confidencialidad de las respuestas, validación de notas y auditoría. Quedan fuera sistemas reales, autenticación de producción, despliegue, carga, concurrencia y persistencia externa.

## Activos

| ID | Activo | Dónde reside | Propiedad a proteger |
| --- | --- | --- | --- |
| A-01 | Expediente académico (id, titular, sede) | `estado["expedientes"]` | Confidencialidad |
| A-02 | Nota académica (0–100) | campo `nota` del expediente | Integridad y confidencialidad |
| A-03 | Sesiones y tokens sintéticos (revocada / expirada) | `estado["sesiones"]` | Validez del acceso |
| A-04 | Política de permisos por rol, identidad y sede | `USUARIOS` y funciones de autorización | Autorización |
| A-05 | Bitácora de auditoría | `estado["auditoria"]` | Trazabilidad; no contener credenciales |
| A-06 | Respuestas de la API (cuerpo y código HTTP) | `servidor.py` → cliente | No divulgar información protegida |

## Flujo de datos

1. El cliente (curl, PowerShell o prueba automatizada) envía `Authorization: Bearer <token>`, la ruta `/expedientes/<id>` y, para cambios, `{"nota": n}`.
2. `servidor.py` extrae token, identificador y cuerpo; limita el tamaño a 1024 bytes y exige un objeto JSON.
3. `src/lab.py` autentica la sesión, busca el expediente, aplica la autorización y valida la nota.
4. Si se permite, lee o modifica el estado en memoria y registra un evento de auditoría.
5. El servidor responde con código HTTP y JSON (`Cache-Control: no-store`).

**Frontera de confianza:** token, identificador y nota provienen del cliente y no son confiables. Las decisiones de seguridad se toman en `src/lab.py`.

## Amenazas priorizadas

| ID | Actor y acción de abuso | Activo | Impacto | Prob. / Impacto | Prioridad razonada |
| --- | --- | --- | --- | --- | --- |
| R-01 | Estudiante cambia el id para leer otro expediente; docente lee otra sede | A-01, A-02, A-04 | Divulgación de notas de terceros | Alta / Alta | **Alta**: basta editar la URL con una sesión válida (IDOR) |
| R-02 | Docente modifica nota de otra sede; estudiante o administrador intenta cambiar notas | A-02, A-04 | Calificaciones alteradas | Media / Alta | **Alta**: rompe integridad y separación de funciones |
| R-03 | Portador reutiliza una sesión revocada o vencida, o usa un token inventado | A-03, A-01 | Acceso que debía terminar | Media / Alta | **Alta**: anula el cierre de sesión |
| R-04 | Docente autorizado envía nota fuera de 0–100, booleana o no numérica | A-02 | Datos inválidos persistidos | Media / Media | **Media**: requiere docente autorizado, pero corrompe el registro |
| R-05 | Persona con acceso a la bitácora extrae tokens o no puede atribuir una acción | A-05, A-03 | Reutilización de sesiones; sin no repudio | Baja / Alta | **Media**: requiere acceso a registros; el daño es amplio |

## Requisitos verificables

| ID | Categoría | Requisito observable (oráculo) |
| --- | --- | --- |
| SEC-01 | Autorización (lectura) | Con sesión válida, estudiante lee solo su expediente, docente solo su sede y administrador ambas sedes. Permitido → 200 con datos exactos; cualquier otra lectura → 403. |
| SEC-02 | Integridad | Solo un docente de la misma sede cambia la nota (200 y valor persistido). Estudiante, administrador y docente de otra sede → 403 con el expediente idéntico. |
| SEC-03 | Sesiones | Sesión ausente, desconocida, revocada o expirada → 401, sin datos protegidos ni cambios. |
| SEC-04 | Validación | Solo notas int/float (no bool) en [0, 100]. Fuera de rango, NaN, infinito u otro tipo → 400 sin persistir. |
| SEC-05 | Confidencialidad | Una denegación (401/403) omite id, estudiante, sede y nota, y no identifica al titular. Una operación rechazada no modifica expedientes. |
| SEC-06 | Trazabilidad | Cada lectura y cambio permitido registra acción, usuario e id, sin almacenar el token. |

## Criterios de aceptación

- **CA-01 (SEC-01, SEC-05).** **Dado** Ana con sesión válida y el expediente 202 de Luis, **cuando** solicita `GET /expedientes/202`, **entonces** recibe 403 sin id, estudiante, sede ni nota, y los expedientes quedan intactos.
- **CA-02 (SEC-02, SEC-05).** **Dado** María, docente de Central, y el 202 de Pacífico con nota 91, **cuando** envía `{"nota": 70}` a ese expediente, **entonces** recibe 403 y el 202 conserva la nota 91.
- **CA-03 (SEC-03).** **Dada** una sesión de Ana revocada, **cuando** solicita su expediente 101, **entonces** recibe 401 sin datos protegidos.
- **CA-04 (SEC-04).** **Dado** María con sesión válida y el 101 con nota 82, **cuando** envía -1, 101, "ochenta", true o un entero de 401 cifras, **entonces** recibe 400 y la nota sigue en 82; 0 y 100 se aceptan y persisten.

La matriz requisito–riesgo–caso está en `../matriz_trazabilidad.csv`.

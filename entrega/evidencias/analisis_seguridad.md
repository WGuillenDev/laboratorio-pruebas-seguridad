# Análisis de seguridad y alcance del equipo

Fecha de elaboración: 25 de octubre de 2026 (Costa Rica). Proyecto local de expedientes académicos, versión de trabajo posterior a `9525e75`. Este documento es contenido técnico de soporte del informe; no es una guía de aprendizaje ni evidencia de revisión cruzada realizada.

## Alcance y responsables

El sistema contiene dos expedientes sintéticos: 101 de Ana (Central, nota inicial 82) y 202 de Luis (Pacífico, nota inicial 91). Se evalúan lectura, actualización de notas, validez de sesiones, respuestas sin datos protegidos y auditoría. No se evalúan sistemas universitarios reales, autenticación de producción, despliegue, carga ni persistencia externa.

Wilberth: TC-01, TC-03, TC-04, TC-05, TC-07 y TC-12; autorización de lectura, validación de notas y auditoría de lecturas. Jania: TC-02, TC-06, TC-08, TC-09, TC-10 y TC-11; sesiones, autorización de escritura por sede, auditoría de actualizaciones e integración HTTP. La revisión cruzada y el cierre de la entrega requieren participación real de ambos.

La documentación y parte de la implementación y ejecución posterior al primer ciclo TDD se prepararon con asistencia de IA por autorización de Wilberth. Las evidencias identifican las ejecuciones manuales de Wilberth y las realizadas por el asistente; no se atribuye a una persona una revisión que no realizó. Ambos integrantes deben comprender y verificar sus aportes.

## Activos

| ID | Activo | Propiedad a proteger |
| --- | --- | --- |
| A-01 | Expedientes: identidad del titular, sede e identificador | Confidencialidad e integridad |
| A-02 | Notas académicas, entre 0 y 100 | Integridad y confidencialidad |
| A-03 | Sesiones y tokens sintéticos con indicadores de revocación/expiración | Validez del acceso y confidencialidad |
| A-04 | Permisos definidos por rol, identidad y sede | Integridad y autorización |
| A-05 | Bitácora de lecturas y actualizaciones | Trazabilidad, confidencialidad de credenciales |

## Flujo de datos

Cliente local (PowerShell, curl o prueba HTTP) → `servidor.py` (ruta, encabezado Bearer y JSON) → `src/lab.py` (sesión, existencia, permisos y validación) → estado en memoria (expedientes, sesiones y auditoría) → respuesta JSON y código HTTP → cliente.

El cliente controla token, identificador y datos: son entradas no confiables. El servidor debe aplicar los permisos; no basta con ocultar controles en un cliente. Las pruebas unitarias llaman directamente a la lógica; las de integración deben atravesar HTTP y el servidor real. Reiniciar el servidor restaura los datos sintéticos.

## Amenazas priorizadas

| ID | Actor y acción de abuso | Activo | Impacto | Prioridad y razón |
| --- | --- | --- | --- | --- |
| R-01 | Estudiante cambia el identificador para consultar otro expediente; docente consulta otra sede | A-01, A-02, A-04 | Divulgación de información académica | Alta: acceso directo a datos ajenos con una cuenta válida |
| R-02 | Docente modifica otra sede; estudiante o administrador intenta cambiar notas | A-02, A-04 | Calificaciones alteradas sin autorización | Alta: rompe integridad y separación de funciones |
| R-03 | Portador reutiliza una sesión revocada o vencida | A-03, A-01 | Acceso que debía haber terminado | Alta: la sesión inválida conserva acceso protegido |
| R-04 | Docente o cliente envía una nota fuera de rango o con tipo inválido | A-02 | Persistencia de datos académicos inválidos | Alta: compromete la integridad del expediente |
| R-05 | Persona con acceso a registros obtiene tokens o no puede atribuir una acción | A-05, A-03 | Reutilización de sesión y trazabilidad insuficiente | Alta: la bitácora no debe transformarse en un almacén de credenciales |

## Requisitos verificables

| ID | Requisito y oráculo | Responsable principal |
| --- | --- | --- |
| SEC-01 | Con sesión válida, estudiante lee solo su expediente, docente solo su sede y administrador ambas sedes. Lectura permitida: 200 y datos correctos. Otras lecturas: 403 sin datos protegidos y sin alterar expedientes. | Wilberth |
| SEC-02 | Solo un docente de la misma sede puede modificar notas. Permitir con 200 y persistencia del valor; denegar a estudiante, administrador y docente de otra sede con 403 y expedientes intactos. | Jania; Wilberth prueba denegaciones de estudiante/admin |
| SEC-03 | Lectura y modificación con sesión ausente, desconocida, revocada o expirada devuelven 401, sin datos protegidos ni cambios en expedientes. | Jania |
| SEC-04 | Aceptar únicamente int/float que no sean bool y estén entre 0 y 100 inclusive. Rechazar valores fuera de rango, no finitos y tipos inválidos con 400 sin persistir. Comparar el rango sin convertir enteros grandes a float. | Wilberth; Jania prueba los extremos válidos por HTTP |
| SEC-05 | Una respuesta denegada por sesión o permiso no incluye id, estudiante, sede ni nota, ni identifica al titular ajeno. Una operación rechazada conserva los expedientes. | Wilberth, con verificación de sesiones por Jania |
| SEC-06 | Cada lectura y actualización permitida registra acción, identidad del usuario e identificador del expediente, sin almacenar token ni su valor. | Compartido: Wilberth lectura; Jania actualización |

SEC-06 no exige incorporar en este laboratorio registro de todos los intentos denegados; no se añade esa funcionalidad al alcance. Las respuestas de error deben ser claras sin revelar información protegida.

## Criterios de aceptación

**CA-01 / SEC-01, SEC-05.** Dada Ana con sesión válida y el expediente 202 de Luis, cuando solicita ese expediente, entonces recibe 403 sin campos protegidos ni nombre de Luis y todos los expedientes permanecen intactos.

**CA-02 / SEC-02.** Dada María, docente de Central, y el expediente 202 de Pacífico con nota 91, cuando intenta cambiar su nota a 70, entonces recibe 403 sin datos protegidos y la nota y demás campos siguen iguales.

**CA-03 / SEC-03.** Dada una sesión revocada, cuando solicita una lectura o modificación protegida, entonces recibe 401 sin datos protegidos y los expedientes no cambian.

**CA-04 / SEC-04.** Dada María con sesión válida y la nota inicial 82 del expediente 101, cuando envía -1, 101, texto, true o un entero muy grande, entonces recibe 400 y el expediente conserva su estado. Los límites 0 y 100 se aceptan y persisten al verificarlos en el bloque de Jania.

## Casos y trazabilidad

Los diseños completos, sus estados y los vínculos requisito-riesgo-caso se consolidan en `../matriz_trazabilidad.csv`. Son 12 casos distintos: 3 positivos, 6 negativos y 3 de frontera. Cada variante dentro de un caso conserva el mismo ID; los métodos y las solicitudes no se suman para inflar el número de casos.

Los resultados del producto se registran únicamente cuando existe una ejecución. La revisión cruzada, el segundo ciclo TDD y la prueba de reproducibilidad por una persona diferente del autor no se consideran realizados por haber sido planificados aquí.

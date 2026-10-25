# Resultados del corte parcial de Wilberth

Fecha: 25 de octubre de 2026 (Costa Rica). Código: base `9525e75` más cambios identificados por `version_bloque_wilberth.json` y `wilberth_cambios.patch`. Los cambios autónomos todavía no tienen commit. Entorno de ejecución asistida: Windows, Python 3.14.7, biblioteca estándar y curl.exe. No se instaló SAST ni otra dependencia de ejecución.

## Ejecuciones reales

| Ejecución | Resultado | Evidencia |
| --- | --- | --- |
| Pruebas ampliadas antes de corregir auditoría | 4 métodos; TC-01 y TC-03 fallan por identidad ausente; 3 aserciones fallidas contando dos subcasos de TC-03 | wilberth_unidad_antes.txt |
| Bloque Wilberth, proceso limpio 1 | 4/4 métodos aprobados | wilberth_unidad_corrida1.txt |
| Bloque Wilberth, proceso limpio 2 | 4/4 métodos aprobados | wilberth_unidad_corrida2.txt |
| Suite parcial del equipo | 6 métodos: 5 aprobados, 1 fallido por sesión revocada | suite_parcial_equipo.txt |
| TC-05 HTTP antes/después | Antes: 200 con datos de otra sede. Después: 403 sin datos; ambos expedientes intactos y acceso legítimo de Pedro 200 | wilberth_api_antes.txt / wilberth_api_despues.txt |
| TC-12 HTTP antes/después | Antes: -1,101,true y entero grande persistían; texto ya se rechazaba. Después: las 5 variantes reciben 400, ambos expedientes intactos | wilberth_api_antes.txt / wilberth_api_despues.txt |

Las corridas asistidas identifican al ejecutor y guardan fecha UTC, comando, versión y código de salida. Cada proceso unitario crea estado por prueba; el servidor se detuvo y reinició por escenario/variante HTTP. Las solicitudes curl se realizaron contra `127.0.0.1:8765` y no están incluidas como métodos de una suite de integración. El equipo debe comprender y verificar los resultados; no se atribuyen estas ejecuciones a Wilberth como si hubiera escrito cada comando.

Wilberth ejecutó después en su terminal el bloque filtrado y la suite completa. La captura `verificacion_wilberth.png` muestra 4/4 OK y 6 métodos con un fallo de sesión revocada. Esa captura confirma la verificación humana de las pruebas. Las capturas `verificacion_http_servidor.png` y `verificacion_http_denegaciones.png` muestran además servidor local, lectura entre sedes 403 y nota 101 rechazada con 400. La captura posterior `verificacion_http_estado.png` acredita la consulta legítima 200 con nota 82 después del rechazo. La comparación completa antes/después de ambos expedientes y las otras variantes consta en los registros asistidos de curl.

## Estados de los casos planificados

- Aprobados: TC-01, TC-03, TC-04, TC-05, TC-07 y TC-12 (6).
- Fallido: TC-08 (1). El ejemplo original ya contradice la denegación obligatoria tras revocación; Jania debe ampliar el caso y completar su ciclo TDD.
- Bloqueados: ninguno (0).
- No ejecutados por completo: TC-02, TC-06, TC-09, TC-10 y TC-11 (5). El ejemplo original de TC-02 pasa, pero no acredita persistencia, aislamiento y auditoría del diseño completo; no se infla el número de aprobados.

Planificados: 12. Los 6 casos aprobados de Wilberth incluyen 4 unitarios y 2 HTTP. No confundir casos lógicos, métodos unittest, variantes de datos y solicitudes auxiliares.

## Indicadores parciales

- Tasa de aprobación: 6 / (6 + 1) × 100 = **85.71 %**.
- Avance: (6 + 1) / 12 × 100 = **58.33 %**.
- Cobertura de requisitos: 6 / 6 × 100 = **100 %**, usando la definición mínima de al menos una prueba válida vinculada por requisito. Para SEC-03 cuenta la prueba de revocación que falla correctamente; para SEC-06 cuentan las pruebas de auditoría de lectura. La cobertura no significa aprobación ni cobertura de todas las variantes: sesiones, escritura y auditoría de actualización siguen pendientes.
- Dentro del bloque de Wilberth: 6/6 casos aprobados. No es una tasa final del producto.

Los indicadores se calculan sobre casos planificados, no sobre los seis métodos que actualmente descubre unittest. Las cifras finales deben recalcularse después del bloque de Jania.

## Mantenimiento y usabilidad

Se mejoraron al menos dos pruebas: la consulta propia pasó a `test_tc01_sec01_estudiante_lee_su_expediente_sin_alterarlo`, con datos completos, estado y auditoría; la lectura ajena pasó a `test_tc04_sec01_estudiante_no_lee_expediente_ajeno_ni_filtra_datos`, con ID/requisito y mensajes diagnósticos. Los ayudantes centralizan ausencia de datos protegidos e invariancia. Cada variante de TC-07 crea estado nuevo.

Mensaje 403 actual: «Operación denegada». Es genérico y no divulga titular/sede/nota; su claridad es limitada porque no orienta a una acción. Mensaje 401 actual: «No autenticado». No divulga datos, pero no explica cómo recuperar una sesión; además el control de revocación todavía falla. Jania debe analizar ambos mensajes y verificar el comportamiento seguro tras su corrección. No se añade un portal de acceso ni autenticación real.

## Dictamen provisional y limitaciones

**NO LIBERAR el producto actual.** H-02 sigue abierto (revocación); H-05 sigue abierto en auditoría de actualizaciones; la autorización de escritura entre sedes está pendiente de implementar y comprobar. Una tasa alta de casos aprobados no compensa un fallo de sesión o autorización.

Este es un dictamen técnico provisional preparado con asistencia de IA para revisión del equipo. Responsable de la decisión hipotética final y fecha de aprobación: pendientes de designación por Wilberth y Jania. No se presenta una firma ficticia.

Limitaciones: dos expedientes y cinco usuarios sintéticos; sesiones simuladas sin tiempo real; datos en memoria; integración y segundo TDD pendientes; no se han probado carga ni concurrencia; no se ha completado inspección cruzada ni reproducibilidad humana usando solo README. Las dos corridas de este bloque no sustituyen las dos corridas finales completas.

## Aportes y calendario

Wilberth realizó el ciclo TDD 1 manualmente y sus commits `4cf28d2`, `e4cc9fc`, `9525e75`, además del README y la base. Después autorizó al asistente a completar implementación, pruebas, documentación y registros de su bloque; verificó las pruebas en su terminal. Las tareas pendientes de Jania se gestionan en el issue https://github.com/WGuillenDev/laboratorio-pruebas-seguridad/issues/2.

Todos los commits actuales de Wilberth son del 25/10/2026. Para cumplir el enunciado deberá hacer al menos otro aporte significativo en una fecha diferente antes de entregar. Abrir un PR o repetir un commit sin cambios no sustituye ese aporte. Las fechas y autorías se conservarán auténticas.

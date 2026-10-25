# Revisión estática del bloque de Wilberth

Fecha: 25/10/2026. Ejecución: asistente autorizado por Wilberth. Base: `9525e75` con los cambios de Wilberth todavía sin commit. Técnica: lectura del código sin ejecutarlo. Las peticiones curl y unittest se documentan por separado como pruebas dinámicas. No se instaló un escáner adicional.

Este registro no sustituye la inspección cruzada de una persona distinta del autor: Jania deberá revisar la política de lectura y dos casos; Wilberth deberá revisar el bloque de Jania después de su implementación.

| Comprobación | Resultado verificable | Acción / evidencia |
| --- | --- | --- |
| Permisos de lectura | `_puede_leer` aplica propietario al estudiante, sede al docente y acceso global solo al administrador; otros roles se deniegan | TC-01/03/04 y TC-05 por HTTP; `wilberth_api_despues.txt` |
| Permisos de modificación | Se deniega a estudiantes/admin; falta comprobar sede del docente | TC-07 aprobado; observación pendiente para Jania en `actualizar_nota` |
| Validación de notas | Se excluye bool; int/float debe estar dentro de [0,100]. El rango también excluye NaN e infinitos sin convertir enteros grandes a float | TC-12 antes/después por HTTP. Pruebas de aceptación de 0/100 pendientes de Jania |
| Manejo de errores | 403 genérico en lectura sin titular, sede ni nota; 400 genérico para nota inválida | TC-04 y TC-05; TC-12. Los mensajes 401 y la validez de sesiones aún corresponden a Jania |
| Exposición de datos | La denegación de lectura retorna antes de copiar el expediente; los tests comparan expedientes y campos protegidos | TC-04; lectura entre sedes TC-05 |
| Auditoría | Lecturas permitidas guardan usuario/acción/id y no token. Las actualizaciones aún guardan el token | TC-01/03; H-05 parcialmente tratado, pendiente Jania en actualización |
| Independencia | `setUp` crea estado por prueba; cada rol de TC-07 inicia estado nuevo. La repetición de ambos procesos unitarios usa datos nuevos | Corridas 1 y 2 del bloque Wilberth |

## Observaciones para la revisión cruzada humana

| ID | Objeto | Observación y severidad | Estado |
| --- | --- | --- | --- |
| O-01 | Prueba de consulta propia | La prueba base solo verificaba identidad y 200. Ahora comprueba respuesta completa, invariancia y auditoría sin token. Media: el oráculo anterior no detectaba defectos de trazabilidad | Implementado; pendiente confirmación por Jania |
| O-02 | Prueba de acceso ajeno | El test ahora usa copia profunda, ausencia de campos protegidos y mensaje diagnóstico con recurso concreto. Media: evitar que un 403 con datos filtrados se considere suficiente | Implementado; pendiente confirmación por Jania |
| O-03 | Política de lectura | El control inicial solo trataba estudiantes y permitía docentes de otra sede. Alta: lectura académica no autorizada | Corregido con política explícita; pendiente inspección por Jania |
| O-04 | Sesiones | `autenticar` todavía ignora revocada/expirada. Alta: sesión inválida conserva acceso | Abierto, Jania; H-02 demuestra revocación |
| O-05 | Auditoría de escritura | `actualizar_nota` conserva el campo token y carece de usuario explícito. Alta: expone credenciales sintéticas y no cumple SEC-06 | Abierto, Jania; no dar por corregida la auditoría completa |

Revisor humano, fecha y confirmación de acciones: pendientes. Estas observaciones se proponen para que el equipo las compruebe; no se presenta un acta firmada ficticia.

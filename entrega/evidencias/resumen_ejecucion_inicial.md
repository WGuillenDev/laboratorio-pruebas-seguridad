# Registro de ejecución inicial

- Ejecutor: Wilberth, mediante la terminal de PowerShell.
- Fecha: 25 de octubre de 2026, según el contexto de la sesión en Costa Rica.
- Versión del proyecto: `3a27a6f8aca674c3459b377e044e3dc30f405a4e`.
- Directorio de ejecución: `entrega/laboratorio_seguridad/`.
- Entorno: Windows y Python 3.14.7. La versión de Python se comprobó al revisar la evidencia; no aparece en la captura original. No se registró la versión de PowerShell.
- Evidencia original: [ejecucion_inicial.txt](ejecucion_inicial.txt), conservada sin modificaciones.

Comando ejecutado por Wilberth:

```powershell
python -m unittest discover -s tests -v 2>&1 | Tee-Object -FilePath ..\evidencias\ejecucion_inicial.txt
```

## Resultado observado

| Prueba original | Resultado | Observación |
| --- | --- | --- |
| `test_docente_actualiza_nota_en_su_sede` | Aprobado | Pasan las aserciones de código 200 y nota 85 devuelta. La prueba original no verifica por separado la persistencia. |
| `test_estudiante_consulta_expediente_propio` | Aprobado | Pasan las aserciones de código 200 e identidad de Ana en la respuesta. |
| `test_rojo_estudiante_no_consulta_expediente_ajeno` | Fallido | Esperado 403; observado 200. Hallazgo H-01. |
| `test_rojo_sesion_revocada_no_permita_lecturas` | Fallido | La revocación devuelve 200; la lectura posterior devuelve 200 en lugar de 401. Hallazgo H-02. |

Total: 4 pruebas ejecutadas, 2 aprobadas y 2 fallidas. Duración informada por unittest: 0.002 segundos. Esta ejecución corresponde a los ejemplos originales; no demuestra haber diseñado ni completado los 12 casos exigidos.

El encabezado `NativeCommandError` proviene del tratamiento de stderr por PowerShell al capturar la salida de unittest. Aparece incluso ante una línea con resultado `ok`; no es un tercer fallo del producto ni un error de instalación demostrado. La conclusión se basa en los detalles de las aserciones y en `FAILED (failures=2)`.

## Alcance de la evidencia

Ambos fallos ocurren por una discrepancia del código de respuesta esperado, coherente con los controles pendientes del código base. Las aserciones posteriores `assertNotIn("nota", datos)` no llegan a ejecutarse en esos dos métodos, porque la primera aserción detiene cada prueba. Esta salida, por sí sola, no prueba ausencia de filtración ni invariancia de los expedientes.

La ejecución constituye una referencia inicial y conserva evidencia roja de las pruebas originales. No se presenta como un ciclo TDD completo ni como una de las dos ejecuciones finales después de integrar el trabajo. No se ha aplicado ninguna corrección.

Los identificadores SEC-01/TC-04 y SEC-03/TC-08 utilizados en hallazgos.csv corresponden al reparto de trabajo acordado. Su especificación completa y su matriz se desarrollarán durante la fase de requisitos y diseño.

"""Inspección de la política de escritura: aplica un mutante por vez a una copia de lab.py
y ejecuta la suite real para ver qué prueba lo detecta."""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ORIGEN = Path(sys.argv[1])  # entrega/laboratorio_seguridad

MUTANTES = [
    ("M-L2", "Docente lee cualquier sede (J-01)",
     'return expediente["sede"] == usuario["sede"]\n    return usuario["rol"] == "administrador"',
     'return True\n    return usuario["rol"] == "administrador"'),
    ("M-E1", "Docente modifica cualquier sede",
     'return usuario["rol"] == "docente" and expediente["sede"] == usuario["sede"]',
     'return usuario["rol"] == "docente"'),
    ("M-E2", "Cualquier rol de la sede modifica",
     'return usuario["rol"] == "docente" and expediente["sede"] == usuario["sede"]',
     'return expediente["sede"] == usuario["sede"]'),
    ("M-E3", "Nadie puede modificar",
     'return usuario["rol"] == "docente" and expediente["sede"] == usuario["sede"]',
     'return False'),
    ("M-E4", "Se omite el rango 0-100",
     'and 0 <= nota <= 100',
     ''),
    ("M-E5", "La auditoría guarda el token",
     '"accion": "actualizacion",\n        "usuario": usuario["id"],',
     '"accion": "actualizacion",\n        "usuario": usuario["id"],\n        "token": token,'),
    ("M-E6", "Se audita antes de autorizar",
     '    if not _puede_modificar(usuario, expediente):\n        return 403',
     '    estado["auditoria"].append({"accion": "actualizacion", "usuario": usuario["id"], "id": expediente_id})\n'
     '    if not _puede_modificar(usuario, expediente):\n        return 403'),
    ("M-E7", "Se valida la nota antes de autorizar",
     '    if not _puede_modificar(usuario, expediente):\n        return 403, {"error": "Operación denegada"}\n'
     '    if not _nota_valida(nota):\n        return 400, {"error": "Nota inválida"}\n',
     '    if not _nota_valida(nota):\n        return 400, {"error": "Nota inválida"}\n'
     '    if not _puede_modificar(usuario, expediente):\n        return 403, {"error": "Operación denegada"}\n'),
]


def ejecutar(carpeta):
    resultado = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=carpeta, capture_output=True, text=True, encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )
    salida = resultado.stderr + resultado.stdout
    fallidas = sorted(set(re.findall(r"^(?:FAIL|ERROR): (test_\w+)", salida, re.M)))
    return resultado.returncode, fallidas


codigo_base, fallidas_base = ejecutar(ORIGEN)
print(f"Línea base (sin mutantes): {'OK' if codigo_base == 0 else 'FALLA'} {fallidas_base}")
print()
fuente = (ORIGEN / "src" / "lab.py").read_text(encoding="utf-8")
for ident, descripcion, buscar, reemplazo in MUTANTES:
    assert fuente.count(buscar) == 1, f"{ident}: patrón no encontrado"
    with tempfile.TemporaryDirectory() as tmp:
        copia = Path(tmp) / "lab"
        shutil.copytree(ORIGEN, copia, ignore=shutil.ignore_patterns("__pycache__"))
        (copia / "src" / "lab.py").write_text(fuente.replace(buscar, reemplazo), encoding="utf-8")
        _, fallidas = ejecutar(copia)
    estado = "DETECTADO" if fallidas else "SOBREVIVE"
    detalle = ", ".join(fallidas) if fallidas else "ninguna prueba automatizada falla"
    print(f"{ident}  {estado:<9}  {descripcion:<38} -> {detalle}")

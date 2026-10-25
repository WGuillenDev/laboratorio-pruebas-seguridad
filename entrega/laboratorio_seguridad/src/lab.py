"""Laboratorio didáctico: contiene fallas INTENCIONALES que deben identificarse.

No se debe reutilizar este código en producción. No realiza autenticación real.
"""

USUARIOS = {
    "ana": {"id": "ana", "rol": "estudiante", "sede": "Central"},
    "luis": {"id": "luis", "rol": "estudiante", "sede": "Pacifico"},
    "maria": {"id": "maria", "rol": "docente", "sede": "Central"},
    "pedro": {"id": "pedro", "rol": "docente", "sede": "Pacifico"},
    "admin": {"id": "admin", "rol": "administrador", "sede": None},
}


def estado_inicial():
    """Crea datos de laboratorio independientes para cada ejecución."""
    return {
        "expedientes": {
            "101": {"id": "101", "estudiante": "ana", "sede": "Central", "nota": 82},
            "202": {"id": "202", "estudiante": "luis", "sede": "Pacifico", "nota": 91},
        },
        "sesiones": {
            f"lab-{id_usuario}": {"usuario": id_usuario, "revocada": False, "expirada": False}
            for id_usuario in USUARIOS
        } | {"lab-vencida": {"usuario": "ana", "revocada": False, "expirada": True}},
        "auditoria": [],
    }


def autenticar(estado, token):
    """Recibe tokens SINTETICOS; no implementa autenticación de producción."""
    sesion = estado["sesiones"].get(token)
    if sesion is None:
        return None
    # TODO SEC-03: investigar el tratamiento de sesiones revocadas o expiradas.
    return USUARIOS[sesion["usuario"]]


def leer_expediente(estado, token, expediente_id):
    usuario = autenticar(estado, token)
    if usuario is None:
        return 401, {"error": "No autenticado"}
    expediente = estado["expedientes"].get(expediente_id)
    if expediente is None:
        return 404, {"error": "No existe"}
    # TODO SEC-01: identificar la política de autorización correcta.
    estado["auditoria"].append({"accion": "lectura", "token": token, "id": expediente_id})
    return 200, dict(expediente)


def actualizar_nota(estado, token, expediente_id, nota):
    usuario = autenticar(estado, token)
    if usuario is None:
        return 401, {"error": "No autenticado"}
    expediente = estado["expedientes"].get(expediente_id)
    if expediente is None:
        return 404, {"error": "No existe"}
    if usuario["rol"] != "docente":
        return 403, {"error": "Operación denegada"}
    if not isinstance(nota, (int, float)):
        return 400, {"error": "Nota inválida"}
    # TODO SEC-02/SEC-04: inspeccionar la sede y los valores de frontera.
    expediente["nota"] = nota
    estado["auditoria"].append({"accion": "actualizacion", "token": token, "id": expediente_id})
    return 200, dict(expediente)


def revocar_sesion(estado, token):
    sesion = estado["sesiones"].get(token)
    if sesion is None:
        return 401, {"error": "No autenticado"}
    sesion["revocada"] = True
    return 200, {"mensaje": "Sesión revocada"}

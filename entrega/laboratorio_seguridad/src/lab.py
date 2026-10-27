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


def _sesion_vigente(sesion):
    """SEC-03: la sesión existe y no fue revocada ni expiró."""
    return sesion is not None and not sesion["revocada"] and not sesion["expirada"]


def autenticar(estado, token):
    """Recibe tokens SINTETICOS; no implementa autenticación de producción."""
    sesion = estado["sesiones"].get(token)
    if not _sesion_vigente(sesion):
        return None
    return USUARIOS[sesion["usuario"]]


def _puede_leer(usuario, expediente):
    """Autoriza por propietario o sede; solo el administrador lee ambas sedes."""
    if usuario["rol"] == "estudiante":
        return expediente["estudiante"] == usuario["id"]
    if usuario["rol"] == "docente":
        return expediente["sede"] == usuario["sede"]
    return usuario["rol"] == "administrador"


def _puede_modificar(usuario, expediente):
    """SEC-02: solo un docente cambia notas, y únicamente de expedientes de su sede."""
    return usuario["rol"] == "docente" and expediente["sede"] == usuario["sede"]


def _nota_valida(nota):
    """Rechaza bool, tipos no numéricos y valores fuera de [0, 100]."""
    return (
        not isinstance(nota, bool)
        and isinstance(nota, (int, float))
        and 0 <= nota <= 100
    )


def leer_expediente(estado, token, expediente_id):
    usuario = autenticar(estado, token)
    if usuario is None:
        return 401, {"error": "No autenticado"}
    expediente = estado["expedientes"].get(expediente_id)
    if expediente is None:
        return 404, {"error": "No existe"}
    if not _puede_leer(usuario, expediente):
        return 403, {"error": "Operación denegada"}
    estado["auditoria"].append({
        "accion": "lectura",
        "usuario": usuario["id"],
        "id": expediente_id,
    })
    return 200, dict(expediente)


def actualizar_nota(estado, token, expediente_id, nota):
    usuario = autenticar(estado, token)
    if usuario is None:
        return 401, {"error": "No autenticado"}
    expediente = estado["expedientes"].get(expediente_id)
    if expediente is None:
        return 404, {"error": "No existe"}
    if not _puede_modificar(usuario, expediente):
        return 403, {"error": "Operación denegada"}
    if not _nota_valida(nota):
        return 400, {"error": "Nota inválida"}
    expediente["nota"] = nota
    estado["auditoria"].append({
        "accion": "actualizacion",
        "usuario": usuario["id"],
        "id": expediente_id,
    })
    return 200, dict(expediente)


def revocar_sesion(estado, token):
    sesion = estado["sesiones"].get(token)
    if sesion is None:
        return 401, {"error": "No autenticado"}
    sesion["revocada"] = True
    return 200, {"mensaje": "Sesión revocada"}

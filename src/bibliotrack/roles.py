"""Roles: reglas para cambiar el rol de un usuario (HU-04)."""

LECTOR = "lector"
BIBLIOTECARIO = "bibliotecario"
ADMINISTRADOR = "administrador"
ROLES = (LECTOR, BIBLIOTECARIO, ADMINISTRADOR)


class CambioDeRolNoPermitido(Exception):
    """El cambio de rol no cumple las reglas."""


def validar_cambio_de_rol(rol_actual, rol_nuevo, administradores):
    """Revisa si un usuario puede pasar de `rol_actual` a `rol_nuevo`.

    `administradores` es cuántos administradores hay ahora en el sistema.
    Siempre debe quedar al menos uno.
    """
    if rol_nuevo not in ROLES:
        raise CambioDeRolNoPermitido("Ese rol no existe")
    if rol_actual == ADMINISTRADOR and rol_nuevo != ADMINISTRADOR and administradores <= 1:
        raise CambioDeRolNoPermitido("Debe quedar al menos un administrador en el sistema")

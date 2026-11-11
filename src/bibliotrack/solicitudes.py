"""Solicitudes de préstamo en línea: reglas para que un lector pida un libro (HU-17)."""

from bibliotrack.prestamos import MAXIMO_PRESTAMOS_ACTIVOS


MENSAJE_YA_SOLICITADOS = "Los ejemplares disponibles ya están solicitados."


class SolicitudNoPermitida(Exception):
    """La solicitud no cumple las reglas de la biblioteca."""


def validar_solicitud(lector, libro):
    """Revisa si `lector` puede solicitar `libro`.

    `lector` es un diccionario con `prestamos_activos`, `solicitudes_pendientes`,
    `libros_prestados` y `libros_solicitados` (identificadores de libros).
    `libro` es un diccionario con `id`, `disponibles` y, opcional, `solicitudes_pendientes`
    (las solicitudes pendientes de todos los lectores para ese libro).
    Lanza SolicitudNoPermitida con el motivo si no se puede.
    """
    if libro["disponibles"] <= 0:
        raise SolicitudNoPermitida("No hay ejemplares disponibles")
    if libro["id"] in lector["libros_solicitados"]:
        raise SolicitudNoPermitida("Ya tienes una solicitud pendiente de este libro.")
    if libro["id"] in lector["libros_prestados"]:
        raise SolicitudNoPermitida("Ya tienes este libro prestado.")
    # BUG-07: una solicitud no descuenta el ejemplar, así que se cuentan las que están en espera.
    if libro.get("solicitudes_pendientes", 0) >= libro["disponibles"]:
        raise SolicitudNoPermitida(MENSAJE_YA_SOLICITADOS)
    if lector["prestamos_activos"] + lector["solicitudes_pendientes"] >= MAXIMO_PRESTAMOS_ACTIVOS:
        raise SolicitudNoPermitida(
            f"Ya tienes {MAXIMO_PRESTAMOS_ACTIVOS} préstamos activos o solicitudes pendientes; ese es el máximo."
        )

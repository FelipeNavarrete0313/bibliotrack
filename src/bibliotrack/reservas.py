"""Reservas: reglas para reservar un libro que no tiene ejemplares disponibles (HU-13)."""

from datetime import timedelta

MAXIMO_RESERVAS_ACTIVAS = 2
HORAS_DE_RESERVA = 48


class ReservaNoPermitida(Exception):
    """La reserva no cumple las reglas de la biblioteca."""


def validar_reserva(lector, libro):
    """Revisa si `lector` puede reservar `libro`.

    `lector` es un diccionario con `reservas_activas`, `libros_reservados` y
    `libros_prestados` (identificadores de libros).
    `libro` es un diccionario con `id` y `disponibles`.
    Lanza ReservaNoPermitida con el motivo si no se puede.
    """
    if libro["disponibles"] > 0:
        raise ReservaNoPermitida("Hay ejemplares disponibles: puedes pedirlo prestado ahora")
    if libro["id"] in lector["libros_reservados"]:
        raise ReservaNoPermitida("Ya tienes una reserva activa de este libro")
    if libro["id"] in lector["libros_prestados"]:
        raise ReservaNoPermitida("Ya tienes este libro prestado")
    if lector["reservas_activas"] >= MAXIMO_RESERVAS_ACTIVAS:
        raise ReservaNoPermitida(f"Ya tienes {MAXIMO_RESERVAS_ACTIVAS} reservas activas; ese es el máximo")


def guardar_hasta(ahora):
    """Hasta cuándo se guarda un ejemplar devuelto para quien lo reservó: 48 horas."""
    return ahora + timedelta(hours=HORAS_DE_RESERVA)


def reservas_por_guardar(cola, disponibles, guardados):
    """Reservas de la cola a las que se les guarda un ejemplar, en orden de llegada.

    `cola` son las reservas en espera, de la más antigua a la más nueva.
    `disponibles` son los ejemplares en la biblioteca y `guardados` los que ya
    están apartados para otra reserva.
    """
    libres = max(0, disponibles - guardados)
    return list(cola)[:libres]


def ejemplares_libres(disponibles, guardados_para_otros, solicitudes_pendientes=0):
    """Ejemplares que un lector puede pedir: ni guardados para otro ni ya solicitados."""
    return max(0, disponibles - guardados_para_otros - solicitudes_pendientes)

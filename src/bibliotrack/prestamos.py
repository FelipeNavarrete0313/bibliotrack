"""Préstamos: reglas para registrar un préstamo (HU-09)."""

from datetime import date, timedelta

DIAS_DE_PRESTAMO = 15
MAXIMO_PRESTAMOS_ACTIVOS = 3
DOMINGO = 6


class PrestamoNoPermitido(Exception):
    """El préstamo no cumple las reglas de la biblioteca."""


def fecha_de_devolucion(fecha_prestamo):
    """Calcula la fecha de devolución: 15 días calendario.

    Si cae domingo, se pasa al lunes siguiente.
    """
    fecha = fecha_prestamo + timedelta(days=DIAS_DE_PRESTAMO)
    if fecha.weekday() == DOMINGO:
        fecha += timedelta(days=1)
    return fecha


def registrar_prestamo(lector, libro, hoy=None):
    """Registra el préstamo de un ejemplar de `libro` a `lector`.

    `lector` es un diccionario con `documento` y `prestamos_activos`.
    `libro` es un diccionario con `isbn` y `disponibles`.
    Devuelve el préstamo creado y descuenta un ejemplar disponible.
    """
    hoy = hoy or date.today()
    if lector["prestamos_activos"] >= MAXIMO_PRESTAMOS_ACTIVOS:
        raise PrestamoNoPermitido(f"El lector ya tiene {MAXIMO_PRESTAMOS_ACTIVOS} préstamos activos")
    if libro["disponibles"] <= 0:
        raise PrestamoNoPermitido("No hay ejemplares disponibles")

    libro["disponibles"] -= 1
    lector["prestamos_activos"] += 1
    return {
        "documento": lector["documento"],
        "isbn": libro["isbn"],
        "fecha_prestamo": hoy,
        "fecha_devolucion": fecha_de_devolucion(hoy),
        "estado": "activo",
    }

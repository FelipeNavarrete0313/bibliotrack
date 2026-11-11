"""Renovaciones: reglas para que un lector renueve un préstamo (HU-12)."""

from datetime import timedelta

from bibliotrack.prestamos import DOMINGO, PrestamoNoPermitido

DIAS_DE_RENOVACION = 7


class RenovacionNoPermitida(PrestamoNoPermitido):
    """La renovación no cumple las reglas de la biblioteca."""


def renovar(prestamo, hoy, reservas_de_otros=0):
    """Devuelve la nueva fecha de devolución de `prestamo`: 7 días más.

    `prestamo` es un diccionario con `estado`, `fecha_devolucion` y `renovado`.
    `reservas_de_otros` es cuántas reservas activas de otros lectores tiene el libro.
    Lanza RenovacionNoPermitida con el motivo si no se puede renovar.
    Si la nueva fecha cae domingo, pasa al lunes (igual que en HU-09).
    """
    if prestamo["estado"] != "activo":
        raise RenovacionNoPermitida("El préstamo ya fue devuelto")
    if prestamo["fecha_devolucion"] < hoy:
        raise RenovacionNoPermitida("El préstamo está vencido; devuelve el libro en la biblioteca")
    if prestamo["renovado"]:
        raise RenovacionNoPermitida("Este préstamo ya se renovó una vez")
    if reservas_de_otros > 0:
        raise RenovacionNoPermitida("Otro lector tiene reservado este libro")
    fecha = prestamo["fecha_devolucion"] + timedelta(days=DIAS_DE_RENOVACION)
    if fecha.weekday() == DOMINGO:
        fecha += timedelta(days=1)
    return fecha

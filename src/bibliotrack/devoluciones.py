"""Devoluciones: reglas para registrar una devolución (HU-10, en progreso)."""


def dias_de_retraso(fecha_devolucion, fecha_entrega):
    """Días que pasaron desde la fecha de devolución hasta la entrega real.

    Si el libro se entrega a tiempo o antes, el retraso es 0.
    """
    return max(0, (fecha_entrega - fecha_devolucion).days)

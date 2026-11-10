"""Estado de un préstamo para resaltarlo en «Mis préstamos» (HU-11, en progreso)."""

VENCIDO = "vencido"
POR_VENCER = "por_vencer"
AL_DIA = "al_dia"
DIAS_DE_AVISO = 3


def estado_del_prestamo(fecha_devolucion, hoy):
    """vencido (rojo), por_vencer en 3 días o menos (amarillo) o al_dia."""
    dias = (fecha_devolucion - hoy).days
    if dias < 0:
        return VENCIDO
    if dias <= DIAS_DE_AVISO:
        return POR_VENCER
    return AL_DIA

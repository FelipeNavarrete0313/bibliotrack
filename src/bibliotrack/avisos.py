"""Avisos por correo de un préstamo (HU-14)."""

DIAS_DE_ANTICIPACION = 2
POR_VENCER = "por_vencer"
VENCIDO = "vencido"


def aviso_que_toca(fecha_devolucion, hoy, por_vencer_enviado=False, vencido_enviado=False):
    """Qué aviso hay que enviar hoy por un préstamo activo, o None.

    - `por_vencer`: desde 2 días antes de la fecha de devolución (una sola vez).
    - `vencido`: desde el día siguiente al vencimiento (una sola vez).
    Si un día no se ejecuta el envío, el aviso sale la siguiente vez.
    """
    dias = (fecha_devolucion - hoy).days
    if dias < 0:
        return None if vencido_enviado else VENCIDO
    if dias <= DIAS_DE_ANTICIPACION:
        return None if por_vencer_enviado else POR_VENCER
    return None

"""Correos que BiblioTrack envía a los lectores (HU-13 y HU-14).

En desarrollo los correos se imprimen en la terminal del servidor (ver settings).
"""

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from bibliotrack.avisos import POR_VENCER, VENCIDO, aviso_que_toca

from .models import Prestamo

ASUNTOS = {
    POR_VENCER: "BiblioTrack: tu préstamo de «{titulo}» vence pronto",
    VENCIDO: "BiblioTrack: tu préstamo de «{titulo}» está vencido",
    "reserva_lista": "BiblioTrack: tu reserva de «{titulo}» está lista",
}


def _enviar(perfil, tipo, libro, contexto, silencioso=False):
    """Envía el correo `tipo` al lector. Devuelve True si salió."""
    if not perfil.usuario.email:
        return False
    contexto = {
        "nombre": perfil.usuario.first_name or perfil.nombre, "libro": libro,
        "enlace": settings.SITIO_URL.rstrip("/") + reverse("mis_prestamos"), **contexto,
    }
    cuerpo = render_to_string(f"biblioteca/correos/{tipo}.txt", contexto)
    return bool(send_mail(ASUNTOS[tipo].format(titulo=libro.titulo), cuerpo, None, [perfil.usuario.email],
                          fail_silently=silencioso))


def avisar_reserva_lista(reserva):
    """HU-13: se guardó un ejemplar 48 horas para esta reserva. Un fallo del correo no detiene la devolución."""
    return _enviar(reserva.lector, "reserva_lista", reserva.libro, {"reserva": reserva}, silencioso=True)


def enviar_avisos(hoy=None):
    """HU-14: envía los avisos que tocan hoy por los préstamos activos.

    Devuelve cuántos avisos salieron de cada tipo. Cada aviso se envía una sola vez por préstamo.
    """
    hoy = hoy or timezone.localdate()
    enviados = {POR_VENCER: 0, VENCIDO: 0}
    activos = Prestamo.objects.filter(estado=Prestamo.ACTIVO).select_related("lector__usuario", "libro")
    for prestamo in activos:
        tipo = aviso_que_toca(prestamo.fecha_devolucion, hoy, bool(prestamo.aviso_por_vencer), bool(prestamo.aviso_vencido))
        if tipo is None:
            continue
        contexto = {"prestamo": prestamo, "puede_renovar": not prestamo.renovado,
                    "dias_vencido": (hoy - prestamo.fecha_devolucion).days}
        if _enviar(prestamo.lector, tipo, prestamo.libro, contexto):
            campo = "aviso_por_vencer" if tipo == POR_VENCER else "aviso_vencido"
            # Solo se marca si el préstamo sigue activo: si lo devolvieron mientras tanto, no importa.
            Prestamo.objects.filter(pk=prestamo.pk, estado=Prestamo.ACTIVO).update(**{campo: hoy})
            enviados[tipo] += 1
    return enviados

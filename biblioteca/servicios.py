"""Operaciones de préstamo que cambian la disponibilidad de los libros.

Las páginas de BiblioTrack y el panel Admin usan estas mismas funciones, para que
las reglas (HU-09, HU-10 y HU-17) se cumplan sin importar desde dónde se haga.
"""

from django.db import transaction
from django.utils import timezone

from bibliotrack.devoluciones import devolver_ejemplar, dias_de_retraso
from bibliotrack.prestamos import PrestamoNoPermitido, registrar_prestamo

from .models import Libro, Prestamo, Solicitud


def crear_prestamo(lector, libro):
    """HU-09: aplica las reglas, descuenta el ejemplar y guarda el préstamo.

    Lanza PrestamoNoPermitido si no se puede.
    """
    with transaction.atomic():
        libro = Libro.objects.select_for_update().get(pk=libro.pk)
        if not libro.activo:
            raise PrestamoNoPermitido("El libro fue dado de baja")
        datos_libro = libro.como_dict()
        prestamo = registrar_prestamo(
            {"documento": lector.documento, "prestamos_activos": lector.prestamos_activos}, datos_libro,
        )
        libro.disponibles = datos_libro["disponibles"]
        libro.save(update_fields=["disponibles"])
        return Prestamo.objects.create(
            lector=lector, libro=libro,
            fecha_prestamo=prestamo["fecha_prestamo"], fecha_devolucion=prestamo["fecha_devolucion"],
        )


def entregar_solicitud(solicitud):
    """HU-17: entrega una solicitud pendiente creando su préstamo."""
    if solicitud.estado != Solicitud.PENDIENTE:
        raise PrestamoNoPermitido("La solicitud ya no está pendiente")
    with transaction.atomic():
        prestamo = crear_prestamo(solicitud.lector, solicitud.libro)
        solicitud.estado = Solicitud.ENTREGADA
        solicitud.atendida = timezone.now()
        solicitud.prestamo = prestamo
        solicitud.save(update_fields=["estado", "atendida", "prestamo"])
    return prestamo


def cerrar_solicitud(solicitud, estado):
    """HU-17: rechaza o cancela una solicitud pendiente. No cambia ejemplares."""
    solicitud.estado = estado
    solicitud.atendida = timezone.now()
    solicitud.save(update_fields=["estado", "atendida"])


def registrar_devolucion(prestamo, hoy=None):
    """HU-10: cierra un préstamo activo y suma el ejemplar. Devuelve los días de retraso."""
    hoy = hoy or timezone.localdate()
    with transaction.atomic():
        libro = Libro.objects.select_for_update().get(pk=prestamo.libro_id)
        libro.disponibles = devolver_ejemplar(
            {"disponibles": libro.disponibles, "total_ejemplares": libro.total_ejemplares},
        )["disponibles"]
        libro.save(update_fields=["disponibles"])
        prestamo.estado = Prestamo.DEVUELTO
        prestamo.fecha_entrega = hoy
        prestamo.save(update_fields=["estado", "fecha_entrega"])
    return dias_de_retraso(prestamo.fecha_devolucion, hoy)


def borrar_prestamo(prestamo):
    """Si se borra un préstamo activo (solo desde el Admin), el ejemplar vuelve al catálogo."""
    with transaction.atomic():
        if prestamo.estado == Prestamo.ACTIVO:
            libro = Libro.objects.select_for_update().get(pk=prestamo.libro_id)
            libro.disponibles = min(libro.disponibles + 1, libro.total_ejemplares)
            libro.save(update_fields=["disponibles"])
        prestamo.delete()

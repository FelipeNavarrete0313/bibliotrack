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
    """HU-17: entrega una solicitud pendiente creando su préstamo.

    BUG-05: el estado se cambia con un UPDATE que solo afecta a la solicitud si
    sigue pendiente en la base de datos. Si otra petición ya la atendió, no se
    crea un segundo préstamo.
    """
    with transaction.atomic():
        ahora = timezone.now()
        _tomar(Solicitud, solicitud, Solicitud.PENDIENTE, "La solicitud ya no está pendiente",
               estado=Solicitud.ENTREGADA, atendida=ahora)
        prestamo = crear_prestamo(solicitud.lector, solicitud.libro)
        Solicitud.objects.filter(pk=solicitud.pk).update(prestamo=prestamo)
    solicitud.estado, solicitud.atendida, solicitud.prestamo = Solicitud.ENTREGADA, ahora, prestamo
    return prestamo


def cerrar_solicitud(solicitud, estado):
    """HU-17: rechaza o cancela una solicitud pendiente. No cambia ejemplares.

    BUG-05: si la solicitud ya no está pendiente, lanza PrestamoNoPermitido.
    """
    ahora = timezone.now()
    _tomar(Solicitud, solicitud, Solicitud.PENDIENTE, "La solicitud ya no está pendiente",
           estado=estado, atendida=ahora)
    solicitud.estado, solicitud.atendida = estado, ahora


def registrar_devolucion(prestamo, hoy=None):
    """HU-10: cierra un préstamo activo y suma el ejemplar. Devuelve los días de retraso.

    BUG-05: si el préstamo ya fue devuelto, lanza PrestamoNoPermitido y no suma nada.
    """
    hoy = hoy or timezone.localdate()
    with transaction.atomic():
        _tomar(Prestamo, prestamo, Prestamo.ACTIVO, "El préstamo ya fue devuelto",
               estado=Prestamo.DEVUELTO, fecha_entrega=hoy)
        libro = Libro.objects.select_for_update().get(pk=prestamo.libro_id)
        libro.disponibles = devolver_ejemplar(
            {"disponibles": libro.disponibles, "total_ejemplares": libro.total_ejemplares},
        )["disponibles"]
        libro.save(update_fields=["disponibles"])
    prestamo.estado, prestamo.fecha_entrega = Prestamo.DEVUELTO, hoy
    return dias_de_retraso(prestamo.fecha_devolucion, hoy)


def dar_de_baja(libro):
    """HU-08: saca el libro del catálogo y rechaza sus solicitudes pendientes.

    Devuelve cuántas solicitudes se rechazaron.
    """
    rechazadas = 0
    with transaction.atomic():
        Libro.objects.filter(pk=libro.pk).update(activo=False)
        for solicitud in libro.solicitudes.filter(estado=Solicitud.PENDIENTE):
            try:
                cerrar_solicitud(solicitud, Solicitud.RECHAZADA)
                rechazadas += 1
            except PrestamoNoPermitido:  # otra petición la atendió primero (BUG-05)
                pass
    libro.activo = False
    return rechazadas


def borrar_prestamo(prestamo):
    """Si se borra un préstamo activo (solo desde el Admin), el ejemplar vuelve al catálogo."""
    with transaction.atomic():
        if prestamo.estado == Prestamo.ACTIVO:
            libro = Libro.objects.select_for_update().get(pk=prestamo.libro_id)
            libro.disponibles = min(libro.disponibles + 1, libro.total_ejemplares)
            libro.save(update_fields=["disponibles"])
        prestamo.delete()


def _tomar(modelo, objeto, estado_esperado, mensaje, **cambios):
    """Cambia el registro solo si en la base de datos sigue en `estado_esperado` (BUG-05).

    Un objeto leído antes de otra petición puede tener un estado viejo; el UPDATE
    con el estado en el WHERE lo resuelve en un solo paso.
    """
    if not modelo.objects.filter(pk=objeto.pk, estado=estado_esperado).update(**cambios):
        raise PrestamoNoPermitido(mensaje)

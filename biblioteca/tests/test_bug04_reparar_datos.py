"""BUG-04 · La migración 0003 repara los datos que el panel Admin dejó mal (issue #47)."""

import importlib
from datetime import timedelta

from django.apps import apps
from django.utils import timezone

from biblioteca.models import Libro, Prestamo, Solicitud

from .conftest import crear_usuario

reparar = importlib.import_module("biblioteca.migrations.0003_reparar_prestamos_admin").reparar


def test_una_solicitud_entregada_sin_prestamo_recibe_su_prestamo(lector, libro):
    # Así quedó la solicitud del reporte: «Entregada» sin préstamo y sin descontar el ejemplar.
    solicitud = Solicitud.objects.create(lector=lector, libro=libro, estado=Solicitud.ENTREGADA, atendida=timezone.now())
    reparar(apps, None)
    solicitud.refresh_from_db()
    libro.refresh_from_db()
    assert solicitud.prestamo is not None and solicitud.prestamo.estado == Prestamo.ACTIVO
    assert libro.disponibles == 1


def test_si_ya_no_hay_ejemplares_la_solicitud_vuelve_a_pendiente(lector, libro):
    otra = crear_usuario("laura@bibliotrack.test", "1003", nombre="Laura")
    hoy = timezone.localdate()
    for _ in range(2):
        Prestamo.objects.create(lector=otra, libro=libro, fecha_prestamo=hoy, fecha_devolucion=hoy + timedelta(days=15))
    solicitud = Solicitud.objects.create(lector=lector, libro=libro, estado=Solicitud.ENTREGADA, atendida=timezone.now())
    reparar(apps, None)
    solicitud.refresh_from_db()
    assert solicitud.estado == Solicitud.PENDIENTE and solicitud.prestamo is None


def test_los_disponibles_se_recalculan_con_los_prestamos_activos(lector, libro):
    # Un préstamo que se marcó «devuelto» en el Admin sin sumar el ejemplar.
    hoy = timezone.localdate()
    Prestamo.objects.create(lector=lector, libro=libro, fecha_prestamo=hoy, fecha_devolucion=hoy, estado=Prestamo.DEVUELTO, fecha_entrega=hoy)
    Libro.objects.filter(pk=libro.pk).update(disponibles=1)
    reparar(apps, None)
    libro.refresh_from_db()
    assert libro.disponibles == 2

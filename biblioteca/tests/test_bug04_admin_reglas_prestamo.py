"""BUG-04 · El panel Admin no aplicaba las reglas de préstamo (issue #47).

Entregar una solicitud o devolver un préstamo desde el Admin debe hacer lo mismo
que los botones de BiblioTrack: crear el préstamo, descontar o sumar el ejemplar.
"""

from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from biblioteca.models import Prestamo, Solicitud


@pytest.fixture
def admin_client(client, db):
    admin = get_user_model().objects.create_superuser("admin", "admin@bibliotrack.test", "Admin2026!")
    client.force_login(admin)
    return client


def cambiar(cliente, objeto, datos):
    url = reverse(f"admin:biblioteca_{objeto._meta.model_name}_change", args=[objeto.pk])
    return cliente.post(url, datos, follow=True)


def accion(cliente, modelo, nombre, objetos):
    url = reverse(f"admin:biblioteca_{modelo._meta.model_name}_changelist")
    return cliente.post(url, {"action": nombre, "_selected_action": [o.pk for o in objetos]}, follow=True)


def test_pasos_del_reporte_entregar_desde_el_admin_crea_el_prestamo(admin_client, lector, libro):
    # Pasos del reporte: el lector solicita, el administrador cambia el estado a «Entregada» y graba.
    solicitud = Solicitud.objects.create(lector=lector, libro=libro)
    cambiar(admin_client, solicitud, {"lector": lector.pk, "libro": libro.pk, "estado": Solicitud.ENTREGADA})
    solicitud.refresh_from_db()
    libro.refresh_from_db()
    assert solicitud.estado == Solicitud.ENTREGADA
    assert solicitud.prestamo is not None, "debe crearse el préstamo"
    assert solicitud.prestamo.estado == Prestamo.ACTIVO
    assert libro.disponibles == 1, "debe descontarse un ejemplar"


def test_el_lector_ve_el_prestamo_entregado_desde_el_admin(admin_client, client, lector, libro):
    solicitud = Solicitud.objects.create(lector=lector, libro=libro)
    cambiar(admin_client, solicitud, {"lector": lector.pk, "libro": libro.pk, "estado": Solicitud.ENTREGADA})
    client.force_login(lector.usuario)
    contenido = client.get(reverse("mis_prestamos")).content.decode()
    assert "No tienes préstamos activos." not in contenido
    assert "Al día" in contenido


def test_entregar_desde_el_admin_respeta_las_reglas(admin_client, lector, libro):
    libro.disponibles = 0
    libro.save()
    solicitud = Solicitud.objects.create(lector=lector, libro=libro)
    respuesta = cambiar(admin_client, solicitud, {"lector": lector.pk, "libro": libro.pk, "estado": Solicitud.ENTREGADA})
    assert "No hay ejemplares disponibles" in respuesta.content.decode()
    solicitud.refresh_from_db()
    assert solicitud.estado == Solicitud.PENDIENTE and not Prestamo.objects.exists()


def test_accion_entregar_solicitudes_seleccionadas(admin_client, lector, libro):
    solicitud = Solicitud.objects.create(lector=lector, libro=libro)
    contenido = accion(admin_client, Solicitud, "entregar_solicitudes", [solicitud]).content.decode()
    assert "1 solicitud(es) entregada(s)" in contenido
    libro.refresh_from_db()
    assert libro.disponibles == 1 and Prestamo.objects.filter(lector=lector, estado=Prestamo.ACTIVO).count() == 1


def test_accion_rechazar_solicitudes_seleccionadas(admin_client, lector, libro):
    solicitud = Solicitud.objects.create(lector=lector, libro=libro)
    accion(admin_client, Solicitud, "rechazar_solicitudes", [solicitud])
    solicitud.refresh_from_db()
    libro.refresh_from_db()
    assert solicitud.estado == Solicitud.RECHAZADA and libro.disponibles == 2


def test_una_solicitud_entregada_no_vuelve_a_pendiente(admin_client, lector, libro):
    solicitud = Solicitud.objects.create(lector=lector, libro=libro)
    cambiar(admin_client, solicitud, {"lector": lector.pk, "libro": libro.pk, "estado": Solicitud.ENTREGADA})
    respuesta = cambiar(admin_client, solicitud, {"lector": lector.pk, "libro": libro.pk, "estado": Solicitud.PENDIENTE})
    assert "Una solicitud entregada, rechazada o cancelada ya no cambia de estado." in respuesta.content.decode()
    solicitud.refresh_from_db()
    assert solicitud.estado == Solicitud.ENTREGADA


def prestar(lector, libro, vence):
    libro.disponibles -= 1
    libro.save()
    return Prestamo.objects.create(lector=lector, libro=libro, fecha_prestamo=vence - timedelta(days=15), fecha_devolucion=vence)


def datos_prestamo(prestamo, estado):
    return {"lector": prestamo.lector_id, "libro": prestamo.libro_id, "estado": estado,
            "fecha_prestamo": prestamo.fecha_prestamo.isoformat(), "fecha_devolucion": prestamo.fecha_devolucion.isoformat()}


def test_devolver_desde_el_admin_suma_el_ejemplar(admin_client, lector, libro):
    prestamo = prestar(lector, libro, timezone.localdate() + timedelta(days=3))
    cambiar(admin_client, prestamo, datos_prestamo(prestamo, Prestamo.DEVUELTO))
    prestamo.refresh_from_db()
    libro.refresh_from_db()
    assert prestamo.estado == Prestamo.DEVUELTO and prestamo.fecha_entrega == timezone.localdate()
    assert libro.disponibles == 2


def test_accion_registrar_devolucion(admin_client, lector, libro):
    prestamo = prestar(lector, libro, timezone.localdate() - timedelta(days=2))
    contenido = accion(admin_client, Prestamo, "registrar_devoluciones", [prestamo]).content.decode()
    assert "1 devolución(es) registrada(s)" in contenido and "2 día(s) de retraso" in contenido
    libro.refresh_from_db()
    assert libro.disponibles == 2


def test_un_prestamo_devuelto_no_vuelve_a_activo(admin_client, lector, libro):
    prestamo = prestar(lector, libro, timezone.localdate())
    cambiar(admin_client, prestamo, datos_prestamo(prestamo, Prestamo.DEVUELTO))
    respuesta = cambiar(admin_client, prestamo, datos_prestamo(prestamo, Prestamo.ACTIVO))
    assert "Un préstamo devuelto no se puede volver a activar." in respuesta.content.decode()
    libro.refresh_from_db()
    assert libro.disponibles == 2


def test_crear_un_prestamo_en_el_admin_descuenta_el_ejemplar(admin_client, lector, libro):
    url = reverse("admin:biblioteca_prestamo_add")
    admin_client.post(url, {"lector": lector.pk, "libro": libro.pk}, follow=True)
    prestamo = Prestamo.objects.get()
    libro.refresh_from_db()
    assert prestamo.estado == Prestamo.ACTIVO and libro.disponibles == 1
    assert (prestamo.fecha_devolucion - prestamo.fecha_prestamo).days in (15, 16)


def test_borrar_un_prestamo_activo_en_el_admin_devuelve_el_ejemplar(admin_client, lector, libro):
    prestamo = prestar(lector, libro, timezone.localdate())
    url = reverse("admin:biblioteca_prestamo_delete", args=[prestamo.pk])
    admin_client.post(url, {"post": "yes"}, follow=True)
    libro.refresh_from_db()
    assert not Prestamo.objects.exists() and libro.disponibles == 2


def test_el_admin_no_edita_los_ejemplares_disponibles_a_mano(admin_client, libro):
    contenido = admin_client.get(reverse("admin:biblioteca_libro_change", args=[libro.pk])).content.decode()
    assert 'name="disponibles"' not in contenido

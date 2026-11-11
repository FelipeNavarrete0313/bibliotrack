"""BUG-06 · El panel Admin descuadraba la disponibilidad de los libros (issue #51).

Cambiar el número de ejemplares de un libro o borrar un préstamo desde el Admin
dejaba datos que no cuadran: un error 500, disponibles que no subían o una
solicitud «Entregada» sin préstamo.
"""

from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from biblioteca import servicios
from biblioteca.models import Libro, Prestamo, Solicitud
from biblioteca.tests.conftest import crear_usuario


@pytest.fixture
def admin_client(client, db):
    admin = get_user_model().objects.create_superuser("admin", "admin@bibliotrack.test", "Admin2026!")
    client.force_login(admin)
    return client


def editar_libro(cliente, libro, **cambios):
    datos = {"titulo": libro.titulo, "autor": libro.autor, "isbn": libro.isbn, "categoria": libro.categoria,
             "descripcion": libro.descripcion, "total_ejemplares": libro.total_ejemplares, "activo": "on"}
    datos.update(cambios)
    return cliente.post(reverse("admin:biblioteca_libro_change", args=[libro.pk]), datos, follow=True)


def test_escenario_bajar_el_total_no_da_error(admin_client, libro):
    # Pasos del reporte: un libro con todos sus ejemplares libres; se baja el total y se graba.
    libro.total_ejemplares = libro.disponibles = 3
    libro.save()
    respuesta = editar_libro(admin_client, libro, total_ejemplares=1)
    assert respuesta.status_code == 200
    libro.refresh_from_db()
    assert (libro.total_ejemplares, libro.disponibles) == (1, 1)


def test_escenario_subir_el_total_suma_disponibles(admin_client, lector, libro):
    servicios.crear_prestamo(lector, libro)  # 1 de 2 prestado
    editar_libro(admin_client, libro, total_ejemplares=5)
    libro.refresh_from_db()
    assert (libro.total_ejemplares, libro.disponibles) == (5, 4)


def test_escenario_total_menor_que_los_prestados(admin_client, lector, libro):
    otro = crear_usuario("carlos@bibliotrack.test", "1002", nombre="Carlos", apellido="Pérez")
    servicios.crear_prestamo(lector, libro)
    servicios.crear_prestamo(otro, libro)  # los 2 ejemplares están prestados
    respuesta = editar_libro(admin_client, libro, total_ejemplares=1)
    assert "Debe haber al menos 2 ejemplar(es)" in respuesta.content.decode()
    libro.refresh_from_db()
    assert (libro.total_ejemplares, libro.disponibles) == (2, 0)


def test_no_se_aceptan_cero_ejemplares_en_el_admin(admin_client, libro):
    respuesta = editar_libro(admin_client, libro, total_ejemplares=0)
    assert "Debe haber al menos 1 ejemplar(es)" in respuesta.content.decode()
    libro.refresh_from_db()
    assert libro.total_ejemplares == 2


def test_un_libro_nuevo_en_el_admin_empieza_con_todos_sus_ejemplares_disponibles(admin_client):
    admin_client.post(reverse("admin:biblioteca_libro_add"), {
        "titulo": "Rayuela", "autor": "Julio Cortázar", "isbn": "978-8437604572", "categoria": "Novela",
        "descripcion": "", "total_ejemplares": 3, "activo": "on",
    })
    nuevo = Libro.objects.get(isbn="978-8437604572")
    assert (nuevo.total_ejemplares, nuevo.disponibles) == (3, 3)


def test_escenario_borrar_el_prestamo_reabre_la_solicitud(admin_client, lector, libro):
    solicitud = Solicitud.objects.create(lector=lector, libro=libro)
    prestamo = servicios.entregar_solicitud(solicitud)
    admin_client.post(reverse("admin:biblioteca_prestamo_delete", args=[prestamo.pk]), {"post": "yes"})
    solicitud.refresh_from_db()
    libro.refresh_from_db()
    assert not Prestamo.objects.exists()
    assert solicitud.estado == Solicitud.PENDIENTE and solicitud.atendida is None
    assert libro.disponibles == 2


def test_la_fecha_de_devolucion_no_puede_ser_anterior_al_prestamo(admin_client, lector, libro):
    prestamo = servicios.crear_prestamo(lector, libro)
    ayer = prestamo.fecha_prestamo - timedelta(days=1)
    respuesta = admin_client.post(reverse("admin:biblioteca_prestamo_change", args=[prestamo.pk]), {
        "lector": lector.pk, "libro": libro.pk, "fecha_prestamo": prestamo.fecha_prestamo.isoformat(),
        "fecha_devolucion": ayer.isoformat(), "estado": Prestamo.ACTIVO,
    }, follow=True)
    assert "La fecha de devolución no puede ser anterior a la fecha de préstamo." in respuesta.content.decode()
    prestamo.refresh_from_db()
    assert prestamo.fecha_devolucion > timezone.localdate()

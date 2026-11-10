"""HU-07 · Ver el detalle y la disponibilidad de un libro (issue #9)."""

from datetime import date

from django.urls import reverse

from biblioteca.models import Prestamo


def test_escenario_ver_la_informacion_completa(client, libro):
    # Dado un libro del catálogo, cuando el lector abre su detalle,
    # entonces ve título, autor, ISBN, categoría y descripción.
    contenido = client.get(reverse("detalle_libro", args=[libro.pk])).content.decode()
    for dato in ("Clean Code", "Robert C. Martin", "978-0132350884", "Programación", "Buenas prácticas."):
        assert dato in contenido


def test_escenario_ver_cuantos_ejemplares_hay(client, libro):
    contenido = client.get(reverse("detalle_libro", args=[libro.pk])).content.decode()
    assert "2 de 2 ejemplares disponibles" in contenido


def test_escenario_libro_agotado_muestra_la_proxima_devolucion(client, libro, lector):
    # Dado un libro sin ejemplares disponibles con dos préstamos activos,
    # cuando el lector abre su detalle, entonces ve «Agotado» y la fecha más cercana de devolución.
    libro.disponibles = 0
    libro.save()
    Prestamo.objects.create(lector=lector, libro=libro, fecha_prestamo=date(2026, 11, 2), fecha_devolucion=date(2026, 11, 20))
    Prestamo.objects.create(lector=lector, libro=libro, fecha_prestamo=date(2026, 11, 1), fecha_devolucion=date(2026, 11, 17))
    contenido = client.get(reverse("detalle_libro", args=[libro.pk])).content.decode()
    assert "Agotado" in contenido
    assert "Próxima devolución: 17/11/2026" in contenido


def test_el_catalogo_enlaza_al_detalle(client, libro):
    assert reverse("detalle_libro", args=[libro.pk]) in client.get(reverse("catalogo")).content.decode()


def test_un_libro_dado_de_baja_no_tiene_detalle(client, libro):
    libro.activo = False
    libro.save()
    assert client.get(reverse("detalle_libro", args=[libro.pk])).status_code == 404

from datetime import date

import pytest
from django.urls import reverse

from biblioteca.models import Lector, Libro, Prestamo


@pytest.fixture
def libro(db):
    return Libro.objects.create(
        titulo="Clean Code", autor="Robert C. Martin", isbn="978-0132350884",
        categoria="Programación", total_ejemplares=2, disponibles=2,
    )


@pytest.fixture
def lector(db):
    return Lector.objects.create(nombre="Ana María Gómez", documento="1001", correo="ana@example.com")


def test_el_catalogo_muestra_los_libros(client, libro):
    respuesta = client.get(reverse("catalogo"))
    assert respuesta.status_code == 200
    assert "Clean Code" in respuesta.content.decode()


def test_el_catalogo_busca_por_autor(client, libro):
    Libro.objects.create(titulo="Cosmos", autor="Carl Sagan", isbn="1", categoria="Ciencia")
    contenido = client.get(reverse("catalogo"), {"q": "martin"}).content.decode()
    assert "Clean Code" in contenido
    assert "Cosmos" not in contenido


def test_el_detalle_muestra_la_disponibilidad(client, libro):
    contenido = client.get(reverse("detalle_libro", args=[libro.pk])).content.decode()
    assert "2 de 2 ejemplares disponibles" in contenido


def test_registrar_un_prestamo_desde_la_pagina(client, libro, lector):
    respuesta = client.post(reverse("prestamos"), {"documento": "1001", "libro": libro.pk}, follow=True)
    assert "Préstamo registrado" in respuesta.content.decode()
    prestamo = Prestamo.objects.get()
    assert prestamo.lector == lector
    assert prestamo.estado == Prestamo.ACTIVO
    assert (prestamo.fecha_devolucion - prestamo.fecha_prestamo).days in (15, 16)
    libro.refresh_from_db()
    assert libro.disponibles == 1


def test_no_presta_a_un_documento_que_no_existe(client, libro):
    respuesta = client.post(reverse("prestamos"), {"documento": "9999", "libro": libro.pk})
    assert "No hay ningún lector registrado" in respuesta.content.decode()
    assert Prestamo.objects.count() == 0


def test_no_presta_un_libro_agotado(client, libro, lector):
    libro.disponibles = 0
    libro.save()
    respuesta = client.post(reverse("prestamos"), {"documento": "1001", "libro": libro.pk}, follow=True)
    assert "No hay ejemplares disponibles" in respuesta.content.decode()
    assert Prestamo.objects.count() == 0


def test_no_presta_a_un_lector_con_3_prestamos_activos(client, libro, lector):
    for _ in range(3):
        Prestamo.objects.create(lector=lector, libro=libro, fecha_prestamo=date.today(), fecha_devolucion=date.today())
    respuesta = client.post(reverse("prestamos"), {"documento": "1001", "libro": libro.pk}, follow=True)
    assert "3 préstamos activos" in respuesta.content.decode()
    assert Prestamo.objects.count() == 3

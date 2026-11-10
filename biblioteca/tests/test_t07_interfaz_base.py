"""T-07 · Construir la interfaz web base con Django."""

from django.urls import reverse

from biblioteca.models import Libro


def test_el_catalogo_muestra_los_libros_activos(client, libro):
    Libro.objects.create(titulo="Libro dado de baja", autor="X", isbn="1", categoria="Novela", activo=False)
    contenido = client.get(reverse("catalogo")).content.decode()
    assert "Clean Code" in contenido
    assert "Libro dado de baja" not in contenido


def test_el_catalogo_busca_por_autor_y_filtra_por_categoria(client, libro):
    Libro.objects.create(titulo="Cosmos", autor="Carl Sagan", isbn="2", categoria="Ciencia")
    contenido = client.get(reverse("catalogo"), {"q": "martin"}).content.decode()
    assert "Clean Code" in contenido and "Cosmos" not in contenido
    contenido = client.get(reverse("catalogo"), {"categoria": "Ciencia"}).content.decode()
    assert "Cosmos" in contenido and "Clean Code" not in contenido


def test_la_busqueda_ignora_tildes_en_la_web(client, db):
    Libro.objects.create(titulo="Álgebra de Baldor", autor="Aurelio Baldor", isbn="3", categoria="Matemáticas")
    assert "Álgebra de Baldor" in client.get(reverse("catalogo"), {"q": "algebra"}).content.decode()


def test_sin_resultados_muestra_un_mensaje_claro(client, libro):
    assert "No encontramos libros con «zzz»" in client.get(reverse("catalogo"), {"q": "zzz"}).content.decode()


def test_ninguna_pagina_enlaza_al_panel_admin(client, libro):
    assert "/admin/" not in client.get(reverse("catalogo")).content.decode()

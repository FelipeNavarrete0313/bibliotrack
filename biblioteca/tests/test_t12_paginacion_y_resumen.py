"""T-12 · Paginación de las listas, filtro de vencidos y resumen del día para el personal."""

from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from biblioteca.models import Libro, Prestamo, Solicitud

CATALOGO = reverse("catalogo")
PRESTAMOS = reverse("prestamos")


def crear_libros(cantidad, categoria="Novela"):
    return [Libro.objects.create(titulo=f"Libro {n:02}", autor="Autora Prueba", isbn=f"isbn-{categoria}-{n}", categoria=categoria)
            for n in range(cantidad)]


def test_escenario_el_catalogo_muestra_20_por_pagina(client, db):
    crear_libros(45)
    primera = client.get(CATALOGO).content.decode()
    assert "Página 1 de 3" in primera and primera.count("/libros/") == 20
    tercera = client.get(CATALOGO, {"pagina": 3}).content.decode()
    assert "Página 3 de 3" in tercera and tercera.count("/libros/") == 5


def test_escenario_la_busqueda_se_conserva_al_paginar(client, db):
    crear_libros(25, "Novela")
    crear_libros(5, "Ciencia")
    contenido = client.get(CATALOGO, {"categoria": "Novela"}).content.decode()
    assert "Página 1 de 2" in contenido
    assert "categoria=Novela&amp;pagina=2" in contenido
    segunda = client.get(CATALOGO, {"categoria": "Novela", "pagina": 2}).content.decode()
    assert segunda.count("/libros/") == 5


def test_un_catalogo_pequeno_no_muestra_paginas(client, libro):
    assert "Página 1 de" not in client.get(CATALOGO).content.decode()


def test_una_pagina_que_no_existe_muestra_la_ultima(client, db):
    crear_libros(25)
    assert "Página 2 de 2" in client.get(CATALOGO, {"pagina": 99}).content.decode()


def test_el_personal_filtra_los_prestamos_vencidos(client, bibliotecario, lector):
    hoy = timezone.localdate()
    al_dia, vencido = crear_libros(2)
    Prestamo.objects.create(lector=lector, libro=al_dia, fecha_prestamo=hoy, fecha_devolucion=hoy + timedelta(days=5))
    Prestamo.objects.create(lector=lector, libro=vencido, fecha_prestamo=hoy - timedelta(days=20), fecha_devolucion=hoy - timedelta(days=5))
    client.force_login(bibliotecario.usuario)
    todos = client.get(PRESTAMOS).content.decode()
    assert "Solo vencidos (1)" in todos and "Libro 00" in todos
    solo = client.get(PRESTAMOS, {"vencidos": "1"}).content.decode()
    assert "Libro 01" in solo and "Libro 00<br>" not in solo


def test_el_inicio_del_personal_resume_lo_pendiente(client, bibliotecario, lector, libro):
    hoy = timezone.localdate()
    Solicitud.objects.create(lector=lector, libro=libro)
    Prestamo.objects.create(lector=lector, libro=libro, fecha_prestamo=hoy - timedelta(days=20), fecha_devolucion=hoy - timedelta(days=5))
    client.force_login(bibliotecario.usuario)
    contenido = client.get(reverse("inicio")).content.decode()
    assert "1 solicitud(es) pendiente(s)" in contenido and "1 préstamo(s) vencido(s)" in contenido
    client.force_login(lector.usuario)
    assert "vencido(s)" not in client.get(reverse("inicio")).content.decode()


def test_la_pagina_403_explica_el_motivo(client, lector, bibliotecario, libro):
    client.force_login(lector.usuario)
    assert "Solo el personal de la biblioteca puede entrar a esta página." in client.get(PRESTAMOS).content.decode()
    client.force_login(bibliotecario.usuario)
    contenido = client.post(reverse("solicitar_prestamo", args=[libro.pk])).content.decode()
    assert "Solo un lector puede solicitar préstamos." in contenido

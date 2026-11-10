"""HU-08 · Editar o dar de baja un libro (issue #14)."""

from datetime import date

from django.urls import reverse

from biblioteca.models import Libro, Prestamo


def editar(client, libro, **cambios):
    datos = {"titulo": libro.titulo, "autor": libro.autor, "categoria": libro.categoria,
             "descripcion": libro.descripcion, "total_ejemplares": libro.total_ejemplares}
    datos.update(cambios)
    return client.post(reverse("editar_libro", args=[libro.pk]), datos, follow=True)


def test_escenario_editar_los_datos_de_un_libro(client, bibliotecario, libro):
    # Dado un bibliotecario, cuando cambia el título y la categoría,
    # entonces el libro queda actualizado.
    client.force_login(bibliotecario.usuario)
    assert "Los cambios del libro quedaron guardados." in editar(client, libro, titulo="Código limpio", categoria="Software").content.decode()
    libro.refresh_from_db()
    assert (libro.titulo, libro.categoria) == ("Código limpio", "Software")


def test_escenario_el_isbn_no_se_puede_editar(client, bibliotecario, libro):
    client.force_login(bibliotecario.usuario)
    editar(client, libro, isbn="000-0000000000")
    libro.refresh_from_db()
    assert libro.isbn == "978-0132350884"


def test_al_sumar_ejemplares_suben_los_disponibles(client, bibliotecario, lector, libro):
    libro.disponibles = 1  # 1 de 2 está prestado
    libro.save()
    client.force_login(bibliotecario.usuario)
    editar(client, libro, total_ejemplares=4)
    libro.refresh_from_db()
    assert (libro.total_ejemplares, libro.disponibles) == (4, 3)


def test_escenario_se_pide_confirmacion_antes_de_dar_de_baja(client, bibliotecario, libro):
    client.force_login(bibliotecario.usuario)
    contenido = client.get(reverse("dar_de_baja", args=[libro.pk])).content.decode()
    assert "¿Seguro que quieres darlo de baja?" in contenido
    libro.refresh_from_db()
    assert libro.activo


def test_escenario_dar_de_baja_lo_saca_del_catalogo_y_conserva_el_historial(client, bibliotecario, lector, libro):
    Prestamo.objects.create(lector=lector, libro=libro, fecha_prestamo=date(2026, 10, 1),
                            fecha_devolucion=date(2026, 10, 16), estado=Prestamo.DEVUELTO)
    client.force_login(bibliotecario.usuario)
    respuesta = client.post(reverse("dar_de_baja", args=[libro.pk]), follow=True)
    assert "se dio de baja. Su historial de préstamos se conserva." in respuesta.content.decode()
    libro.refresh_from_db()
    assert not libro.activo
    assert "No encontramos libros con «clean»" in client.get(reverse("catalogo"), {"q": "clean"}).content.decode()
    assert Prestamo.objects.filter(libro=libro).count() == 1


def test_escenario_no_se_da_de_baja_con_prestamos_activos(client, bibliotecario, lector, libro):
    Prestamo.objects.create(lector=lector, libro=libro, fecha_prestamo=date.today(), fecha_devolucion=date.today())
    client.force_login(bibliotecario.usuario)
    contenido = client.post(reverse("dar_de_baja", args=[libro.pk]), follow=True).content.decode()
    assert "No se puede dar de baja: tiene 1 préstamo(s) activo(s)." in contenido
    libro.refresh_from_db()
    assert libro.activo


def test_un_lector_no_puede_editar_ni_dar_de_baja(client, lector, libro):
    client.force_login(lector.usuario)
    assert client.get(reverse("editar_libro", args=[libro.pk])).status_code == 403
    assert client.post(reverse("dar_de_baja", args=[libro.pk])).status_code == 403
    assert Libro.objects.get(pk=libro.pk).activo

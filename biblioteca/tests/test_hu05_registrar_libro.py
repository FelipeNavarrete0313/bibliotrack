"""HU-05 · Registrar un libro en el catálogo (issue #7)."""

from django.urls import reverse

from biblioteca.models import Libro

URL = reverse("registrar_libro")


def datos(**cambios):
    base = {"titulo": "Cosmos", "autor": "Carl Sagan", "isbn": "978-8408053224", "categoria": "Ciencia",
            "descripcion": "Un recorrido por el universo.", "total_ejemplares": 3}
    base.update(cambios)
    return base


def test_escenario_el_bibliotecario_registra_un_libro(client, bibliotecario):
    # Dado un bibliotecario con sesión iniciada, cuando registra un libro con datos completos,
    # entonces el libro queda guardado con todos sus ejemplares disponibles.
    client.force_login(bibliotecario.usuario)
    respuesta = client.post(URL, datos(), follow=True)
    libro = Libro.objects.get(isbn="978-8408053224")
    assert (libro.total_ejemplares, libro.disponibles) == (3, 3)
    assert "«Cosmos» quedó registrado en el catálogo." in respuesta.content.decode()


def test_escenario_el_libro_aparece_de_inmediato_en_el_catalogo(client, bibliotecario):
    client.force_login(bibliotecario.usuario)
    client.post(URL, datos())
    assert "Cosmos" in client.get(reverse("catalogo"), {"q": "cosmos"}).content.decode()


def test_escenario_campos_obligatorios(client, bibliotecario):
    # Cuando falta el título, el autor, el ISBN o los ejemplares, el libro no se guarda.
    client.force_login(bibliotecario.usuario)
    client.post(URL, datos(titulo="", autor="", isbn="", total_ejemplares=""))
    assert not Libro.objects.exists()


def test_escenario_isbn_repetido(client, bibliotecario, libro):
    client.force_login(bibliotecario.usuario)
    contenido = client.post(URL, datos(isbn=libro.isbn)).content.decode()
    assert "Ya existe un libro con este ISBN." in contenido
    assert Libro.objects.count() == 1


def test_escenario_un_lector_no_puede_registrar_libros(client, lector):
    # Dado un lector con sesión iniciada, cuando intenta abrir «Registrar libro»,
    # entonces recibe «sin permiso» y no ve la opción en la barra.
    client.force_login(lector.usuario)
    assert client.get(URL).status_code == 403
    assert URL not in client.get(reverse("catalogo")).content.decode()


def test_el_personal_ve_la_opcion_en_la_barra_y_en_su_inicio(client, bibliotecario):
    client.force_login(bibliotecario.usuario)
    assert URL in client.get(reverse("catalogo")).content.decode()
    assert "Registrar un libro" in client.get(reverse("inicio")).content.decode()


def test_un_visitante_debe_iniciar_sesion(client, db):
    respuesta = client.get(URL)
    assert respuesta.status_code == 302 and reverse("iniciar_sesion") in respuesta.url


def test_no_se_aceptan_cero_ejemplares(client, bibliotecario):
    client.force_login(bibliotecario.usuario)
    assert "al menos 1 ejemplar" in client.post(URL, datos(total_ejemplares=0)).content.decode()

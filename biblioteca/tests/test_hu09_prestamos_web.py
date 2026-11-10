"""HU-09 · Registrar un préstamo, página web (issue #11).

Las reglas (15 días, domingo → lunes, máximo 3) se prueban en tests/test_prestamos.py.
"""

from datetime import date

from django.urls import reverse

from biblioteca.models import Prestamo

URL = reverse("prestamos")


def test_escenario_registrar_un_prestamo(client, bibliotecario, lector, libro):
    # Dado un bibliotecario, un lector con documento 1001 y un libro con 2 ejemplares,
    # cuando registra el préstamo, entonces se crea activo y queda 1 ejemplar disponible.
    client.force_login(bibliotecario.usuario)
    respuesta = client.post(URL, {"documento": "1001", "libro": libro.pk}, follow=True)
    assert "Préstamo registrado: «Clean Code» para Ana María Gómez" in respuesta.content.decode()
    prestamo = Prestamo.objects.get()
    assert prestamo.lector == lector and prestamo.estado == Prestamo.ACTIVO
    assert (prestamo.fecha_devolucion - prestamo.fecha_prestamo).days in (15, 16)
    libro.refresh_from_db()
    assert libro.disponibles == 1


def test_escenario_documento_que_no_es_de_un_lector(client, bibliotecario, libro):
    client.force_login(bibliotecario.usuario)
    contenido = client.post(URL, {"documento": "9999", "libro": libro.pk}).content.decode()
    assert "No hay ningún lector registrado con ese documento." in contenido
    assert not Prestamo.objects.exists()


def test_escenario_libro_sin_ejemplares(client, bibliotecario, lector, libro):
    libro.disponibles = 0
    libro.save()
    client.force_login(bibliotecario.usuario)
    contenido = client.post(URL, {"documento": "1001", "libro": libro.pk}, follow=True).content.decode()
    assert "No hay ejemplares disponibles" in contenido
    assert not Prestamo.objects.exists()


def test_escenario_lector_con_3_prestamos_activos(client, bibliotecario, lector, libro):
    hoy = date.today()
    for _ in range(3):
        Prestamo.objects.create(lector=lector, libro=libro, fecha_prestamo=hoy, fecha_devolucion=hoy)
    client.force_login(bibliotecario.usuario)
    contenido = client.post(URL, {"documento": "1001", "libro": libro.pk}, follow=True).content.decode()
    assert "3 préstamos activos" in contenido
    assert Prestamo.objects.count() == 3


def test_los_prestamos_activos_se_listan(client, bibliotecario, lector, libro):
    Prestamo.objects.create(lector=lector, libro=libro, fecha_prestamo=date(2026, 11, 9), fecha_devolucion=date(2026, 11, 24))
    client.force_login(bibliotecario.usuario)
    contenido = client.get(URL).content.decode()
    assert "Ana María Gómez" in contenido and "24/11/2026" in contenido


def test_un_lector_no_puede_registrar_prestamos(client, lector):
    client.force_login(lector.usuario)
    assert client.get(URL).status_code == 403


def test_el_detalle_del_libro_ofrece_prestarlo_al_personal(client, bibliotecario, libro):
    client.force_login(bibliotecario.usuario)
    contenido = client.get(reverse("detalle_libro", args=[libro.pk])).content.decode()
    assert f"{URL}?libro={libro.pk}" in contenido

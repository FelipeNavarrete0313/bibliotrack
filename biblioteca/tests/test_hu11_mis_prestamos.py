"""HU-11 · Consultar mis préstamos y fechas de devolución (issue #13).

La regla de los colores (vencido, por vencer, al día) se prueba en tests/test_alertas.py.
"""

from datetime import date, timedelta

from django.urls import reverse
from django.utils import timezone

from biblioteca.models import Libro, Prestamo

from .conftest import crear_usuario

URL = reverse("mis_prestamos")


def prestamo(lector, libro, vence, **extra):
    return Prestamo.objects.create(lector=lector, libro=libro, fecha_prestamo=vence - timedelta(days=15), fecha_devolucion=vence, **extra)


def otro_libro(titulo, isbn):
    return Libro.objects.create(titulo=titulo, autor="Autor", isbn=isbn, categoria="Novela", total_ejemplares=1, disponibles=0)


def test_escenario_ver_mis_prestamos_activos(client, lector, libro):
    prestamo(lector, libro, date(2030, 11, 24))
    client.force_login(lector.usuario)
    contenido = client.get(URL).content.decode()
    assert "Clean Code" in contenido and "24/11/2030" in contenido and "Al día" in contenido


def test_escenario_prestamo_vencido_en_rojo(client, lector, libro):
    # Dado un préstamo que vencía ayer, cuando la lectora abre «Mis préstamos», entonces aparece en rojo.
    prestamo(lector, libro, timezone.localdate() - timedelta(days=1))
    client.force_login(lector.usuario)
    contenido = client.get(URL).content.decode()
    assert 'class="fila-vencido"' in contenido and "Vencido hace 1 día(s)" in contenido


def test_escenario_por_vencer_en_amarillo(client, lector, libro):
    # Dado un préstamo que vence en 3 días, cuando la lectora abre «Mis préstamos», entonces aparece en amarillo.
    prestamo(lector, libro, timezone.localdate() + timedelta(days=3))
    client.force_login(lector.usuario)
    contenido = client.get(URL).content.decode()
    assert 'class="fila-por-vencer"' in contenido and "Vence en 3 día(s)" in contenido


def test_escenario_historial_de_devueltos(client, lector, libro):
    # Dada una lectora con dos préstamos devueltos, cuando abre el historial, entonces ve ambos con su fecha de entrega.
    segundo = otro_libro("Cien años de soledad", "978-0307474728")
    prestamo(lector, libro, date(2026, 10, 20), estado=Prestamo.DEVUELTO, fecha_entrega=date(2026, 10, 18))
    prestamo(lector, segundo, date(2026, 10, 25), estado=Prestamo.DEVUELTO, fecha_entrega=date(2026, 10, 27))
    client.force_login(lector.usuario)
    contenido = client.get(URL).content.decode()
    historial = contenido[contenido.index("Historial de préstamos devueltos"):]
    assert "Clean Code" in historial and "18/10/2026" in historial
    assert "Cien años de soledad" in historial and "27/10/2026" in historial
    assert "No tienes préstamos activos." in contenido


def test_las_fechas_se_muestran_dia_mes_anio(client, lector, libro):
    prestamo(lector, libro, date(2030, 11, 15))
    client.force_login(lector.usuario)
    contenido = client.get(URL).content.decode()
    assert "15/11/2030" in contenido and "11/15/2030" not in contenido


def test_cada_lector_ve_solo_sus_prestamos(client, lector, libro):
    otra = crear_usuario("laura@bibliotrack.test", "1003", nombre="Laura")
    prestamo(otra, otro_libro("Rayuela", "978-8437604572"), date(2030, 11, 24))
    client.force_login(lector.usuario)
    assert "Rayuela" not in client.get(URL).content.decode()


def test_sin_sesion_pide_iniciar_sesion(client, db):
    respuesta = client.get(URL)
    assert respuesta.status_code == 302 and reverse("iniciar_sesion") in respuesta.url


def test_el_menu_del_lector_enlaza_mis_prestamos(client, lector, bibliotecario):
    client.force_login(lector.usuario)
    assert f'href="{URL}"' in client.get(reverse("inicio")).content.decode()
    client.force_login(bibliotecario.usuario)
    assert f'href="{URL}"' not in client.get(reverse("inicio")).content.decode()

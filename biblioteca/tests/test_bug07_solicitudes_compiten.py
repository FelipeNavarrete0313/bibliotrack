"""BUG-07 · Varias solicitudes pendientes competían por el mismo ejemplar (issue #52).

Una solicitud no descuenta el ejemplar (eso pasa al entregar), así que dos lectores
podían pedir el único ejemplar libre. El segundo quedaba «Pendiente» sin que la
biblioteca pudiera entregarle el libro.
"""

from django.urls import reverse

from biblioteca.models import Libro, Solicitud
from biblioteca.tests.conftest import crear_usuario

YA_SOLICITADOS = "Los ejemplares disponibles ya están solicitados."


def solicitar(client, libro):
    return client.post(reverse("solicitar_prestamo", args=[libro.pk]), follow=True).content.decode()


def un_ejemplar():
    return Libro.objects.create(titulo="Delirio", autor="Laura Restrepo", isbn="978-6070706813",
                                categoria="Novela", total_ejemplares=1, disponibles=1)


def test_escenario_no_se_acepta_una_solicitud_sin_ejemplar_libre(client, lector):
    # Pasos del reporte: Ana solicita «Delirio» (1 ejemplar) y después Carlos lo solicita también.
    carlos = crear_usuario("carlos@bibliotrack.test", "1002", nombre="Carlos", apellido="Pérez")
    delirio = un_ejemplar()
    Solicitud.objects.create(lector=lector, libro=delirio)
    client.force_login(carlos.usuario)
    contenido = solicitar(client, delirio)
    assert YA_SOLICITADOS in contenido
    assert not Solicitud.objects.filter(lector=carlos).exists()


def test_escenario_con_ejemplar_libre_se_acepta(client, lector, libro):
    carlos = crear_usuario("carlos@bibliotrack.test", "1002", nombre="Carlos", apellido="Pérez")
    Solicitud.objects.create(lector=lector, libro=libro)  # «Clean Code» tiene 2 ejemplares
    client.force_login(carlos.usuario)
    assert "Solicitud enviada: «Clean Code»." in solicitar(client, libro)
    assert Solicitud.objects.filter(libro=libro, estado=Solicitud.PENDIENTE).count() == 2


def test_escenario_el_detalle_muestra_las_solicitudes_en_espera(client, lector, libro):
    Solicitud.objects.create(lector=lector, libro=libro)
    contenido = client.get(reverse("detalle_libro", args=[libro.pk])).content.decode()
    assert "1 solicitud en espera" in contenido


def test_el_detalle_no_ofrece_solicitar_si_no_queda_ejemplar_libre(client, lector):
    carlos = crear_usuario("carlos@bibliotrack.test", "1002", nombre="Carlos", apellido="Pérez")
    delirio = un_ejemplar()
    Solicitud.objects.create(lector=lector, libro=delirio)
    client.force_login(carlos.usuario)
    contenido = client.get(reverse("detalle_libro", args=[delirio.pk])).content.decode()
    assert "Solicitar préstamo</button>" not in contenido
    assert YA_SOLICITADOS in contenido


def test_una_solicitud_cancelada_libera_el_ejemplar(client, lector):
    carlos = crear_usuario("carlos@bibliotrack.test", "1002", nombre="Carlos", apellido="Pérez")
    delirio = un_ejemplar()
    Solicitud.objects.create(lector=lector, libro=delirio, estado=Solicitud.CANCELADA)
    client.force_login(carlos.usuario)
    assert "Solicitud enviada: «Delirio»." in solicitar(client, delirio)

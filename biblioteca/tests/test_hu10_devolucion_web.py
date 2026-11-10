"""HU-10 · Registrar una devolución, página web (issue #12).

El cálculo de los días de retraso se prueba en tests/test_devoluciones.py.
"""

from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from biblioteca.models import Prestamo

PRESTAMOS = reverse("prestamos")


def prestar(lector, libro, vence):
    """Crea un préstamo activo y descuenta el ejemplar, como lo hace HU-09."""
    libro.disponibles -= 1
    libro.save()
    return Prestamo.objects.create(lector=lector, libro=libro, fecha_prestamo=vence - timedelta(days=15), fecha_devolucion=vence)


def devolver(client, prestamo):
    return client.post(reverse("registrar_devolucion", args=[prestamo.pk]), follow=True).content.decode()


def test_escenario_devolucion_a_tiempo(client, bibliotecario, lector, libro):
    # Dado un préstamo que vence hoy, cuando el libro se entrega hoy,
    # entonces no hay retraso y el libro recupera su ejemplar disponible.
    prestamo = prestar(lector, libro, timezone.localdate())
    client.force_login(bibliotecario.usuario)
    contenido = devolver(client, prestamo)
    assert "Devolución registrada: «Clean Code» de Ana María Gómez. Se entregó a tiempo." in contenido
    libro.refresh_from_db()
    assert libro.disponibles == 2


def test_escenario_devolucion_tardia(client, bibliotecario, lector, libro):
    # Dado un préstamo que venció hace 3 días, cuando se entrega hoy, entonces se muestran 3 días de retraso.
    prestamo = prestar(lector, libro, timezone.localdate() - timedelta(days=3))
    client.force_login(bibliotecario.usuario)
    assert "Se entregó con 3 día(s) de retraso." in devolver(client, prestamo)


def test_escenario_prestamo_cerrado(client, bibliotecario, lector, libro):
    # Dado un préstamo activo, cuando se registra su devolución,
    # entonces queda «devuelto», con la fecha real de entrega, y sale de la lista de activos.
    prestamo = prestar(lector, libro, timezone.localdate() + timedelta(days=5))
    client.force_login(bibliotecario.usuario)
    contenido = devolver(client, prestamo)
    prestamo.refresh_from_db()
    assert prestamo.estado == Prestamo.DEVUELTO
    assert prestamo.fecha_entrega == timezone.localdate()
    assert "Todavía no hay préstamos activos." in contenido


def test_escenario_buscar_el_prestamo_por_documento_o_isbn(client, bibliotecario, lector, libro):
    prestar(lector, libro, timezone.localdate() + timedelta(days=5))
    client.force_login(bibliotecario.usuario)
    assert "Ana María Gómez" in client.get(PRESTAMOS, {"buscar": "1001"}).content.decode()
    assert "Ana María Gómez" in client.get(PRESTAMOS, {"buscar": "978-0132350884"}).content.decode()
    contenido = client.get(PRESTAMOS, {"buscar": "5555"}).content.decode()
    assert "No hay préstamos activos con el documento o ISBN «5555»." in contenido


def test_un_prestamo_ya_devuelto_no_se_devuelve_dos_veces(client, bibliotecario, lector, libro):
    prestamo = prestar(lector, libro, timezone.localdate())
    client.force_login(bibliotecario.usuario)
    devolver(client, prestamo)
    respuesta = client.post(reverse("registrar_devolucion", args=[prestamo.pk]))
    assert respuesta.status_code == 404
    libro.refresh_from_db()
    assert libro.disponibles == 2


def test_un_lector_no_puede_registrar_devoluciones(client, lector, libro):
    prestamo = prestar(lector, libro, timezone.localdate())
    client.force_login(lector.usuario)
    assert client.post(reverse("registrar_devolucion", args=[prestamo.pk])).status_code == 403
    prestamo.refresh_from_db()
    assert prestamo.estado == Prestamo.ACTIVO


def test_la_devolucion_solo_se_registra_con_el_boton(client, bibliotecario, lector, libro):
    prestamo = prestar(lector, libro, timezone.localdate())
    client.force_login(bibliotecario.usuario)
    assert client.get(reverse("registrar_devolucion", args=[prestamo.pk])).status_code == 405

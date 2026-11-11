"""HU-12 · Renovar un préstamo (issue #19)."""

from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from biblioteca import servicios
from biblioteca.models import Prestamo, Reserva
from biblioteca.tests.conftest import crear_usuario
from bibliotrack.prestamos import PrestamoNoPermitido


def prestar(lector, libro, vence_en=5):
    """Préstamo activo que vence dentro de `vence_en` días (negativo: ya venció)."""
    hoy = timezone.localdate()
    libro.disponibles -= 1
    libro.save(update_fields=["disponibles"])
    return Prestamo.objects.create(
        lector=lector, libro=libro, fecha_prestamo=hoy - timedelta(days=10),
        fecha_devolucion=hoy + timedelta(days=vence_en),
    )


def renovar(client, prestamo):
    return client.post(reverse("renovar_prestamo", args=[prestamo.pk]), follow=True).content.decode()


def carlos():
    return crear_usuario("carlos@bibliotrack.test", "1002", nombre="Carlos", apellido="Pérez")


def test_escenario_renovacion_valida(client, lector, libro):
    # Dado un préstamo al día que nunca se ha renovado, cuando la lectora lo renueva,
    # entonces la fecha de devolución se corre 7 días y la ve de inmediato.
    prestamo = prestar(lector, libro)
    antes = prestamo.fecha_devolucion
    client.force_login(lector.usuario)
    assert "Renovar</button>" in client.get(reverse("mis_prestamos")).content.decode()
    contenido = renovar(client, prestamo)
    prestamo.refresh_from_db()
    assert prestamo.renovado
    assert prestamo.fecha_devolucion - antes in (timedelta(days=7), timedelta(days=8))  # 8 si cayó domingo
    assert f"Nueva fecha de devolución: {prestamo.fecha_devolucion:%d/%m/%Y}" in contenido
    assert "Renovar</button>" not in contenido
    assert "Ya renovado" in contenido


def test_escenario_prestamo_vencido(client, lector, libro):
    prestamo = prestar(lector, libro, vence_en=-2)
    antes = prestamo.fecha_devolucion
    client.force_login(lector.usuario)
    assert "Renovar</button>" not in client.get(reverse("mis_prestamos")).content.decode()
    contenido = renovar(client, prestamo)
    assert "El préstamo está vencido" in contenido
    prestamo.refresh_from_db()
    assert not prestamo.renovado and prestamo.fecha_devolucion == antes


def test_escenario_segunda_renovacion(client, lector, libro):
    prestamo = prestar(lector, libro)
    client.force_login(lector.usuario)
    renovar(client, prestamo)
    prestamo.refresh_from_db()
    primera = prestamo.fecha_devolucion
    contenido = renovar(client, prestamo)
    assert "Este préstamo ya se renovó una vez" in contenido
    prestamo.refresh_from_db()
    assert prestamo.fecha_devolucion == primera


def test_escenario_libro_reservado(client, lector, libro):
    prestamo = prestar(lector, libro)
    Reserva.objects.create(lector=carlos(), libro=libro)
    client.force_login(lector.usuario)
    assert "Renovar</button>" not in client.get(reverse("mis_prestamos")).content.decode()
    contenido = renovar(client, prestamo)
    assert "Otro lector tiene reservado este libro" in contenido
    prestamo.refresh_from_db()
    assert not prestamo.renovado


def test_una_reserva_cancelada_no_impide_renovar(client, lector, libro):
    prestamo = prestar(lector, libro)
    Reserva.objects.create(lector=carlos(), libro=libro, estado=Reserva.CANCELADA)
    client.force_login(lector.usuario)
    renovar(client, prestamo)
    prestamo.refresh_from_db()
    assert prestamo.renovado


def test_un_lector_no_renueva_el_prestamo_de_otro(client, lector, libro):
    prestamo = prestar(carlos(), libro)
    client.force_login(lector.usuario)
    assert client.post(reverse("renovar_prestamo", args=[prestamo.pk])).status_code == 404
    prestamo.refresh_from_db()
    assert not prestamo.renovado


def test_el_personal_y_los_visitantes_no_renuevan(client, bibliotecario, lector, libro):
    prestamo = prestar(lector, libro)
    url = reverse("renovar_prestamo", args=[prestamo.pk])
    assert client.post(url).status_code == 302  # visitante: va a «Iniciar sesión»
    client.force_login(bibliotecario.usuario)
    assert client.post(url).status_code == 403
    prestamo.refresh_from_db()
    assert not prestamo.renovado


def test_la_renovacion_solo_se_hace_con_el_boton(client, lector, libro):
    prestamo = prestar(lector, libro)
    client.force_login(lector.usuario)
    assert client.get(reverse("renovar_prestamo", args=[prestamo.pk])).status_code == 405


def test_doble_clic_en_renovar_solo_renueva_una_vez(lector, libro):
    # Igual que en BUG-05: la segunda petición trae el préstamo como estaba antes de la primera.
    prestamo = prestar(lector, libro)
    vieja = Prestamo.objects.get(pk=prestamo.pk)
    primera = servicios.renovar_prestamo(prestamo)
    try:
        servicios.renovar_prestamo(vieja)
    except PrestamoNoPermitido:
        pass
    prestamo.refresh_from_db()
    assert prestamo.fecha_devolucion == primera

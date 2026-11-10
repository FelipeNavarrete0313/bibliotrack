"""BUG-05 · Una solicitud o un préstamo se podía atender dos veces.

Con un doble clic, o con dos bibliotecarios a la vez, la segunda petición traía la
solicitud (o el préstamo) como estaba antes de la primera. Los servicios revisaban
ese estado viejo y volvían a crear el préstamo, a sumar el ejemplar o a rechazar
una solicitud que ya estaba entregada.

Cada prueba simula la segunda petición con un objeto leído antes de la primera.
"""

from django.conf import settings

from biblioteca import servicios
from biblioteca.models import Prestamo, Solicitud
from biblioteca.tests.conftest import crear_usuario
from bibliotrack.prestamos import PrestamoNoPermitido


def leer_dos_veces(modelo, pk):
    """Dos copias del mismo registro, como las que reciben dos peticiones al mismo tiempo."""
    return modelo.objects.get(pk=pk), modelo.objects.get(pk=pk)


def test_escenario_doble_clic_en_entregar(lector, libro):
    solicitud = Solicitud.objects.create(lector=lector, libro=libro)
    primera, segunda = leer_dos_veces(Solicitud, solicitud.pk)
    servicios.entregar_solicitud(primera)
    try:
        servicios.entregar_solicitud(segunda)
    except PrestamoNoPermitido:
        pass
    libro.refresh_from_db()
    assert Prestamo.objects.filter(lector=lector).count() == 1
    assert libro.disponibles == 1


def test_escenario_devolucion_repetida(lector, libro):
    otro = crear_usuario("carlos@bibliotrack.test", "1002", nombre="Carlos", apellido="Pérez")
    prestamo = servicios.crear_prestamo(lector, libro)
    servicios.crear_prestamo(otro, libro)
    primera, segunda = leer_dos_veces(Prestamo, prestamo.pk)
    servicios.registrar_devolucion(primera)
    try:
        servicios.registrar_devolucion(segunda)
    except PrestamoNoPermitido:
        pass
    libro.refresh_from_db()
    activos = Prestamo.objects.filter(libro=libro, estado=Prestamo.ACTIVO).count()
    assert activos == 1
    assert libro.disponibles + activos == libro.total_ejemplares


def test_escenario_rechazar_una_solicitud_ya_entregada(lector, libro):
    solicitud = Solicitud.objects.create(lector=lector, libro=libro)
    vieja = Solicitud.objects.get(pk=solicitud.pk)
    servicios.entregar_solicitud(solicitud)
    try:
        servicios.cerrar_solicitud(vieja, Solicitud.RECHAZADA)
    except PrestamoNoPermitido:
        pass
    solicitud.refresh_from_db()
    assert solicitud.estado == Solicitud.ENTREGADA
    assert solicitud.prestamo is not None


def test_la_segunda_peticion_recibe_un_mensaje_claro(lector, libro):
    solicitud = Solicitud.objects.create(lector=lector, libro=libro)
    vieja = Solicitud.objects.get(pk=solicitud.pk)
    servicios.entregar_solicitud(solicitud)
    try:
        servicios.entregar_solicitud(vieja)
    except PrestamoNoPermitido as error:
        assert "ya no está pendiente" in str(error)
    else:
        raise AssertionError("La segunda entrega debía rechazarse")


def test_sqlite_toma_el_bloqueo_al_iniciar_la_transaccion():
    # SQLite ignora select_for_update; IMMEDIATE hace que las escrituras vayan una por una.
    assert settings.DATABASES["default"]["OPTIONS"]["transaction_mode"] == "IMMEDIATE"


def test_la_pagina_avisa_si_la_devolucion_ya_estaba_registrada(client, bibliotecario, lector, libro, monkeypatch):
    prestamo = servicios.crear_prestamo(lector, libro)
    client.force_login(bibliotecario.usuario)
    # La segunda petición encontró el préstamo activo, pero la primera lo devolvió justo antes.
    original = servicios.registrar_devolucion

    def devolver_dos_veces(p, hoy=None):
        original(Prestamo.objects.get(pk=p.pk))
        return original(p, hoy)

    monkeypatch.setattr(servicios, "registrar_devolucion", devolver_dos_veces)
    respuesta = client.post(f"/prestamos/{prestamo.pk}/devolver/", follow=True)
    assert respuesta.status_code == 200
    assert "El préstamo ya fue devuelto" in respuesta.content.decode()

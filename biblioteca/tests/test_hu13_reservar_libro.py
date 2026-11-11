"""HU-13 · Reservar un libro que no está disponible (issue #20)."""

from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from biblioteca import servicios
from biblioteca.models import Libro, Perfil, Prestamo, Reserva, Solicitud
from biblioteca.tests.conftest import crear_usuario
from bibliotrack.prestamos import PrestamoNoPermitido


@pytest.fixture
def carlos(db):
    return crear_usuario("carlos@bibliotrack.test", "1002", nombre="Carlos", apellido="Pérez")


@pytest.fixture
def laura(db):
    return crear_usuario("laura@bibliotrack.test", "1003", nombre="Laura", apellido="Rodríguez")


@pytest.fixture
def agotado(db, laura):
    """«El amor en los tiempos del cólera»: 1 ejemplar, prestado a Laura."""
    libro = Libro.objects.create(titulo="El amor en los tiempos del cólera", autor="Gabriel García Márquez",
                                 isbn="978-0307387264", categoria="Novela", total_ejemplares=1, disponibles=1)
    servicios.crear_prestamo(laura, libro)
    libro.refresh_from_db()
    return libro


def otro_agotado(n):
    return Libro.objects.create(titulo=f"Agotado {n}", autor="Autor", isbn=f"isbn-agotado-{n}", categoria="Novela",
                                total_ejemplares=1, disponibles=0)


def reservar(client, libro):
    return client.post(reverse("reservar_libro", args=[libro.pk]), follow=True).content.decode()


def devolver(libro):
    servicios.registrar_devolucion(Prestamo.objects.get(libro=libro, estado=Prestamo.ACTIVO))


# ------------------------------------------------------------ Escenarios del issue

def test_escenario_reservar_un_libro_agotado(client, lector, agotado):
    # Dado «El amor en los tiempos del cólera» sin ejemplares, cuando la lectora lo reserva,
    # entonces queda en la cola de reservas.
    client.force_login(lector.usuario)
    assert "Reservar</button>" in client.get(reverse("detalle_libro", args=[agotado.pk])).content.decode()
    contenido = reservar(client, agotado)
    assert "Reservaste «El amor en los tiempos del cólera»: quedaste en el puesto 1 de la cola." in contenido
    reserva = Reserva.objects.get()
    assert (reserva.lector, reserva.estado, reserva.guardada_hasta) == (lector, Reserva.ACTIVA, None)
    assert "puesto 1 de la cola" in contenido and "1 reserva en cola" in contenido
    assert "En cola · puesto 1" in client.get(reverse("mis_prestamos")).content.decode()


def test_escenario_libro_disponible(client, lector, libro):
    # Dado un libro con ejemplares disponibles, cuando la lectora intenta reservarlo,
    # entonces el sistema le indica que puede pedirlo prestado.
    client.force_login(lector.usuario)
    assert "Reservar</button>" not in client.get(reverse("detalle_libro", args=[libro.pk])).content.decode()
    contenido = reservar(client, libro)
    assert "Hay ejemplares disponibles: puedes pedirlo prestado ahora." in contenido
    assert not Reserva.objects.exists()


def test_escenario_orden_de_llegada(lector, carlos, agotado):
    # Dadas dos reservas del mismo libro, cuando se devuelve un ejemplar,
    # entonces se guarda 48 horas para quien reservó primero.
    primera = servicios.crear_reserva(lector, agotado)
    segunda = servicios.crear_reserva(carlos, agotado)
    antes = timezone.now()
    devolver(agotado)
    primera.refresh_from_db()
    segunda.refresh_from_db()
    assert primera.lista_para_recoger and not segunda.lista_para_recoger
    assert timedelta(hours=47, minutes=59) < primera.guardada_hasta - antes < timedelta(hours=48, minutes=1)
    assert (primera.puesto, segunda.puesto) == (1, 2)


def test_escenario_limite_de_reservas(client, lector, agotado):
    # Dada una lectora con 2 reservas activas, cuando intenta hacer una tercera, el sistema no lo permite.
    servicios.crear_reserva(lector, otro_agotado(1))
    servicios.crear_reserva(lector, otro_agotado(2))
    client.force_login(lector.usuario)
    assert "Ya tienes 2 reservas activas; ese es el máximo." in reservar(client, agotado)
    assert Reserva.objects.filter(lector=lector, estado=Reserva.ACTIVA).count() == 2


def test_escenario_cancelar_mi_reserva(client, lector, agotado):
    reserva = servicios.crear_reserva(lector, agotado)
    client.force_login(lector.usuario)
    contenido = client.post(reverse("cancelar_reserva", args=[reserva.pk]), follow=True).content.decode()
    assert "Cancelaste la reserva de «El amor en los tiempos del cólera»." in contenido
    reserva.refresh_from_db()
    assert reserva.estado == Reserva.CANCELADA


# ------------------------------------------------------------ El ejemplar guardado

def test_el_ejemplar_guardado_no_se_presta_ni_se_solicita_por_otro_lector(client, lector, carlos, agotado):
    servicios.crear_reserva(lector, agotado)
    devolver(agotado)  # queda 1 disponible, guardado para la lectora
    with pytest.raises(PrestamoNoPermitido, match="guardados para una reserva"):
        servicios.crear_prestamo(carlos, agotado)
    client.force_login(carlos.usuario)
    detalle = client.get(reverse("detalle_libro", args=[agotado.pk])).content.decode()
    assert "Solicitar préstamo</button>" not in detalle
    assert "Los ejemplares disponibles están guardados para una reserva." in detalle
    client.post(reverse("solicitar_prestamo", args=[agotado.pk]))
    assert not Solicitud.objects.exists()
    # Pero sí puede entrar a la cola detrás de ella.
    assert "quedaste en el puesto 2 de la cola" in reservar(client, agotado)


def test_la_bibliotecaria_entrega_la_reserva_guardada(client, bibliotecario, lector, agotado):
    reserva = servicios.crear_reserva(lector, agotado)
    devolver(agotado)
    client.force_login(bibliotecario.usuario)
    assert "Reservas listas para entregar (1)" in client.get(reverse("prestamos")).content.decode()
    contenido = client.post(reverse("entregar_reserva", args=[reserva.pk]), follow=True).content.decode()
    assert "Entregado: «El amor en los tiempos del cólera» a Ana María Gómez." in contenido
    reserva.refresh_from_db()
    agotado.refresh_from_db()
    assert reserva.estado == Reserva.ATENDIDA
    assert Prestamo.objects.filter(lector=lector, libro=agotado, estado=Prestamo.ACTIVO).count() == 1
    assert agotado.disponibles == 0


def test_quien_tiene_el_ejemplar_guardado_puede_solicitarlo_en_linea(client, lector, agotado):
    reserva = servicios.crear_reserva(lector, agotado)
    devolver(agotado)
    client.force_login(lector.usuario)
    detalle = client.get(reverse("detalle_libro", args=[agotado.pk])).content.decode()
    assert "Tu reserva está lista." in detalle and "Solicitar préstamo</button>" in detalle
    assert "Lista para recoger" in client.get(reverse("mis_prestamos")).content.decode()
    client.post(reverse("solicitar_prestamo", args=[agotado.pk]))
    servicios.entregar_solicitud(Solicitud.objects.get(lector=lector))
    reserva.refresh_from_db()
    assert reserva.estado == Reserva.ATENDIDA


def test_a_las_48_horas_la_reserva_vence_y_pasa_a_la_siguiente(lector, carlos, agotado):
    primera = servicios.crear_reserva(lector, agotado)
    segunda = servicios.crear_reserva(carlos, agotado)
    devolver(agotado)
    servicios.actualizar_reservas(ahora=timezone.now() + timedelta(hours=47))
    primera.refresh_from_db()
    assert primera.lista_para_recoger, "a las 47 horas sigue guardada"
    despues = timezone.now() + timedelta(hours=49)
    servicios.actualizar_reservas(ahora=despues)
    primera.refresh_from_db()
    segunda.refresh_from_db()
    assert primera.estado == Reserva.VENCIDA
    assert segunda.lista_para_recoger and segunda.guardada_hasta > despues + timedelta(hours=47)


def test_si_nadie_mas_espera_el_ejemplar_vuelve_a_estar_libre(client, lector, carlos, agotado):
    servicios.crear_reserva(lector, agotado)
    devolver(agotado)
    Reserva.objects.update(guardada_hasta=timezone.now() - timedelta(minutes=1))  # ya pasaron las 48 horas
    client.force_login(carlos.usuario)
    assert "Solicitar préstamo</button>" in client.get(reverse("detalle_libro", args=[agotado.pk])).content.decode()
    assert Reserva.objects.get().estado == Reserva.VENCIDA


def test_cancelar_una_reserva_guardada_la_pasa_a_la_siguiente(lector, carlos, agotado):
    primera = servicios.crear_reserva(lector, agotado)
    segunda = servicios.crear_reserva(carlos, agotado)
    devolver(agotado)
    servicios.cancelar_reserva(primera)
    segunda.refresh_from_db()
    assert segunda.lista_para_recoger


def test_se_puede_reservar_si_el_unico_ejemplar_ya_lo_solicito_otro(client, lector, carlos):
    # BUG-07: el ejemplar está disponible, pero otro lector ya lo solicitó.
    libro = Libro.objects.create(titulo="Delirio", autor="Laura Restrepo", isbn="978-6070706813",
                                 categoria="Novela", total_ejemplares=1, disponibles=1)
    solicitud = Solicitud.objects.create(lector=lector, libro=libro)
    client.force_login(carlos.usuario)
    assert "quedaste en el puesto 1 de la cola" in reservar(client, libro)
    # Si la solicitud se rechaza, el ejemplar se guarda para quien reservó.
    servicios.cerrar_solicitud(solicitud, Solicitud.RECHAZADA)
    assert Reserva.objects.get(lector=carlos).lista_para_recoger


# ------------------------------------------------------------ Otras reglas y permisos

def test_no_se_reserva_dos_veces_ni_un_libro_que_ya_tengo(client, lector, laura, agotado):
    client.force_login(lector.usuario)
    reservar(client, agotado)
    assert "Ya tienes una reserva activa de este libro." in reservar(client, agotado)
    client.force_login(laura.usuario)  # Laura tiene el libro prestado
    assert "Ya tienes este libro prestado." in reservar(client, agotado)
    assert Reserva.objects.count() == 1


def test_una_reserva_impide_renovar_el_prestamo_de_otro(client, lector, laura, agotado):
    # HU-12: Laura no puede renovar si la lectora reservó el libro.
    servicios.crear_reserva(lector, agotado)
    with pytest.raises(PrestamoNoPermitido, match="reservado"):
        servicios.renovar_prestamo(Prestamo.objects.get(lector=laura))


def test_un_lector_no_cancela_la_reserva_de_otro(client, lector, carlos, agotado):
    reserva = servicios.crear_reserva(carlos, agotado)
    client.force_login(lector.usuario)
    assert client.post(reverse("cancelar_reserva", args=[reserva.pk])).status_code == 404
    reserva.refresh_from_db()
    assert reserva.estado == Reserva.ACTIVA


def test_el_personal_no_reserva_y_un_lector_no_entrega(client, bibliotecario, lector, agotado):
    reserva = servicios.crear_reserva(lector, agotado)
    devolver(agotado)
    client.force_login(lector.usuario)
    assert client.post(reverse("entregar_reserva", args=[reserva.pk])).status_code == 403
    client.force_login(bibliotecario.usuario)
    assert client.post(reverse("reservar_libro", args=[agotado.pk])).status_code == 403
    assert bibliotecario.rol == Perfil.BIBLIOTECARIO and Reserva.objects.count() == 1


def test_un_visitante_debe_iniciar_sesion_para_reservar(client, agotado):
    respuesta = client.post(reverse("reservar_libro", args=[agotado.pk]))
    assert respuesta.status_code == 302 and reverse("iniciar_sesion") in respuesta.url
    assert client.get(reverse("reservar_libro", args=[agotado.pk])).status_code == 302

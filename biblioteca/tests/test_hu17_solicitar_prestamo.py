"""HU-17 · Solicitar un préstamo en línea (issue #44).

Las reglas de la solicitud se prueban también en tests/test_solicitudes.py.
"""

from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from biblioteca.models import Libro, Prestamo, Solicitud

from .conftest import crear_usuario


def solicitar(client, libro):
    return client.post(reverse("solicitar_prestamo", args=[libro.pk]), follow=True).content.decode()


def otro_libro(titulo, isbn, disponibles=1):
    return Libro.objects.create(titulo=titulo, autor="Autor", isbn=isbn, categoria="Novela",
                                total_ejemplares=max(disponibles, 1), disponibles=disponibles)


def test_escenario_solicitar_un_libro(client, lector, libro):
    # Dada la lectora en el detalle de «Clean Code» con 2 ejemplares, cuando pulsa «Solicitar préstamo»,
    # entonces la solicitud queda pendiente.
    client.force_login(lector.usuario)
    detalle = client.get(reverse("detalle_libro", args=[libro.pk])).content.decode()
    assert "Solicitar préstamo" in detalle
    contenido = solicitar(client, libro)
    assert "Solicitud enviada: «Clean Code»." in contenido
    solicitud = Solicitud.objects.get()
    assert solicitud.lector == lector and solicitud.estado == Solicitud.PENDIENTE
    assert "Estado: pendiente" in contenido
    libro.refresh_from_db()
    assert libro.disponibles == 2, "solicitar no descuenta ejemplares: eso pasa al entregar"


def test_escenario_solicitud_repetida(client, lector, libro):
    client.force_login(lector.usuario)
    solicitar(client, libro)
    contenido = solicitar(client, libro)
    assert "Ya tienes una solicitud pendiente de este libro." in contenido
    assert Solicitud.objects.count() == 1


def test_no_se_solicita_un_libro_que_ya_tengo_prestado(client, lector, libro):
    hoy = timezone.localdate()
    Prestamo.objects.create(lector=lector, libro=libro, fecha_prestamo=hoy, fecha_devolucion=hoy + timedelta(days=15))
    client.force_login(lector.usuario)
    assert "Tienes este libro prestado." in client.get(reverse("detalle_libro", args=[libro.pk])).content.decode()
    assert "Ya tienes este libro prestado." in solicitar(client, libro)
    assert not Solicitud.objects.exists()


def test_escenario_limite_de_3_entre_prestamos_y_solicitudes(client, lector, libro):
    # Dada una lectora con 2 préstamos activos y 1 solicitud pendiente, cuando solicita otro libro, entonces no puede.
    hoy = timezone.localdate()
    for n in range(2):
        Prestamo.objects.create(lector=lector, libro=otro_libro(f"Libro {n}", f"isbn-{n}"), fecha_prestamo=hoy, fecha_devolucion=hoy)
    Solicitud.objects.create(lector=lector, libro=otro_libro("Pendiente", "isbn-p"))
    client.force_login(lector.usuario)
    contenido = solicitar(client, libro)
    assert "Ya tienes 3 préstamos activos o solicitudes pendientes; ese es el máximo." in contenido
    assert not Solicitud.objects.filter(libro=libro).exists()


def test_no_se_solicita_un_libro_agotado(client, lector, libro):
    libro.disponibles = 0
    libro.save()
    client.force_login(lector.usuario)
    assert "Solicitar préstamo" not in client.get(reverse("detalle_libro", args=[libro.pk])).content.decode()
    assert "No hay ejemplares disponibles" in solicitar(client, libro)
    assert not Solicitud.objects.exists()


def test_escenario_entregar_crea_el_prestamo(client, lector, bibliotecario, libro):
    # Dada una solicitud pendiente, cuando la bibliotecaria pulsa «Entregar»,
    # entonces se crea el préstamo a 15 días, baja un ejemplar y la solicitud queda «Entregada».
    solicitud = Solicitud.objects.create(lector=lector, libro=libro)
    client.force_login(bibliotecario.usuario)
    pagina = client.get(reverse("prestamos")).content.decode()
    assert "Solicitudes pendientes (1)" in pagina and "Ana María Gómez" in pagina
    contenido = client.post(reverse("entregar_solicitud", args=[solicitud.pk]), follow=True).content.decode()
    assert "Entregado: «Clean Code» a Ana María Gómez." in contenido
    solicitud.refresh_from_db()
    prestamo = Prestamo.objects.get()
    assert solicitud.estado == Solicitud.ENTREGADA and solicitud.prestamo == prestamo
    assert prestamo.lector == lector and prestamo.estado == Prestamo.ACTIVO
    assert (prestamo.fecha_devolucion - prestamo.fecha_prestamo).days in (15, 16)
    libro.refresh_from_db()
    assert libro.disponibles == 1
    client.force_login(lector.usuario)
    mis = client.get(reverse("mis_prestamos")).content.decode()
    assert "Entregada" in mis and prestamo.fecha_devolucion.strftime("%d/%m/%Y") in mis


def test_escenario_entregar_un_libro_agotado(client, lector, bibliotecario, libro):
    solicitud = Solicitud.objects.create(lector=lector, libro=libro)
    libro.disponibles = 0
    libro.save()
    client.force_login(bibliotecario.usuario)
    contenido = client.post(reverse("entregar_solicitud", args=[solicitud.pk]), follow=True).content.decode()
    assert "No se pudo entregar «Clean Code»: No hay ejemplares disponibles." in contenido
    solicitud.refresh_from_db()
    assert solicitud.estado == Solicitud.PENDIENTE and not Prestamo.objects.exists()


def test_entregar_respeta_el_maximo_de_3_prestamos(client, lector, bibliotecario, libro):
    hoy = timezone.localdate()
    solicitud = Solicitud.objects.create(lector=lector, libro=libro)
    for n in range(3):
        Prestamo.objects.create(lector=lector, libro=otro_libro(f"Libro {n}", f"isbn-{n}"), fecha_prestamo=hoy, fecha_devolucion=hoy)
    client.force_login(bibliotecario.usuario)
    contenido = client.post(reverse("entregar_solicitud", args=[solicitud.pk]), follow=True).content.decode()
    assert "El lector ya tiene 3 préstamos activos" in contenido
    solicitud.refresh_from_db()
    assert solicitud.estado == Solicitud.PENDIENTE


def test_escenario_rechazar(client, lector, bibliotecario, libro):
    solicitud = Solicitud.objects.create(lector=lector, libro=libro)
    client.force_login(bibliotecario.usuario)
    contenido = client.post(reverse("rechazar_solicitud", args=[solicitud.pk]), follow=True).content.decode()
    assert "Rechazaste la solicitud de «Clean Code» de Ana María Gómez." in contenido
    assert "No hay solicitudes pendientes." in contenido
    solicitud.refresh_from_db()
    assert solicitud.estado == Solicitud.RECHAZADA and not Prestamo.objects.exists()
    client.force_login(lector.usuario)
    assert "Rechazada" in client.get(reverse("mis_prestamos")).content.decode()


def test_escenario_cancelar_mi_solicitud(client, lector, libro):
    solicitud = Solicitud.objects.create(lector=lector, libro=libro)
    client.force_login(lector.usuario)
    assert "Cancelar solicitud" in client.get(reverse("mis_prestamos")).content.decode()
    contenido = client.post(reverse("cancelar_solicitud", args=[solicitud.pk]), follow=True).content.decode()
    assert "Cancelaste la solicitud de «Clean Code»." in contenido
    solicitud.refresh_from_db()
    assert solicitud.estado == Solicitud.CANCELADA


def test_un_lector_no_cancela_la_solicitud_de_otro(client, lector, libro):
    otra = crear_usuario("laura@bibliotrack.test", "1003", nombre="Laura")
    solicitud = Solicitud.objects.create(lector=otra, libro=libro)
    client.force_login(lector.usuario)
    assert client.post(reverse("cancelar_solicitud", args=[solicitud.pk])).status_code == 404
    solicitud.refresh_from_db()
    assert solicitud.estado == Solicitud.PENDIENTE


def test_un_lector_no_puede_entregar_ni_rechazar(client, lector, libro):
    solicitud = Solicitud.objects.create(lector=lector, libro=libro)
    client.force_login(lector.usuario)
    assert client.post(reverse("entregar_solicitud", args=[solicitud.pk])).status_code == 403
    assert client.post(reverse("rechazar_solicitud", args=[solicitud.pk])).status_code == 403


def test_el_personal_no_solicita_prestamos(client, bibliotecario, libro):
    client.force_login(bibliotecario.usuario)
    assert client.post(reverse("solicitar_prestamo", args=[libro.pk])).status_code == 403


def test_un_visitante_debe_iniciar_sesion_para_solicitar(client, libro):
    detalle = client.get(reverse("detalle_libro", args=[libro.pk])).content.decode()
    assert "Inicia sesión para solicitar este libro" in detalle
    respuesta = client.post(reverse("solicitar_prestamo", args=[libro.pk]))
    assert respuesta.status_code == 302 and reverse("iniciar_sesion") in respuesta.url


def test_el_inicio_del_personal_avisa_las_solicitudes_pendientes(client, lector, bibliotecario, libro):
    Solicitud.objects.create(lector=lector, libro=libro)
    client.force_login(bibliotecario.usuario)
    assert "1 solicitud(es) pendiente(s)" in client.get(reverse("inicio")).content.decode()

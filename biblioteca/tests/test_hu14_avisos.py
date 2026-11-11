"""HU-14 · Recibir un aviso por correo antes del vencimiento (issue #21)."""

from datetime import timedelta
from io import StringIO

from django.core import mail
from django.core.management import call_command
from django.utils import timezone

from biblioteca import notificaciones, servicios
from biblioteca.models import Prestamo, Reserva
from biblioteca.tests.conftest import crear_usuario
from bibliotrack.avisos import POR_VENCER, VENCIDO


def prestar(lector, libro, vence_en):
    """Préstamo activo que vence dentro de `vence_en` días (negativo: ya venció)."""
    hoy = timezone.localdate()
    libro.disponibles -= 1
    libro.save(update_fields=["disponibles"])
    return Prestamo.objects.create(lector=lector, libro=libro, fecha_prestamo=hoy - timedelta(days=13),
                                   fecha_devolucion=hoy + timedelta(days=vence_en))


def test_escenario_aviso_dos_dias_antes(lector, libro):
    # Dado un préstamo que vence en 2 días, cuando corre el envío diario,
    # entonces la lectora recibe un correo con el título, la fecha y el enlace para renovar.
    prestamo = prestar(lector, libro, vence_en=2)
    assert notificaciones.enviar_avisos() == {POR_VENCER: 1, VENCIDO: 0}
    correo = mail.outbox[0]
    assert correo.to == ["ana@bibliotrack.test"]
    assert "Clean Code" in correo.subject and "vence pronto" in correo.subject
    assert f"vence el {prestamo.fecha_devolucion:%d/%m/%Y}" in correo.body
    assert "puedes renovarlo una vez" in correo.body and "/mis-prestamos/" in correo.body
    prestamo.refresh_from_db()
    assert prestamo.aviso_por_vencer == timezone.localdate()


def test_el_aviso_no_se_repite(lector, libro):
    prestar(lector, libro, vence_en=2)
    notificaciones.enviar_avisos()
    assert notificaciones.enviar_avisos() == {POR_VENCER: 0, VENCIDO: 0}
    assert len(mail.outbox) == 1


def test_tres_dias_antes_no_se_envia(lector, libro):
    prestar(lector, libro, vence_en=3)
    notificaciones.enviar_avisos()
    assert not mail.outbox


def test_escenario_prestamo_devuelto_no_recibe_aviso(lector, libro):
    prestamo = prestar(lector, libro, vence_en=1)
    servicios.registrar_devolucion(prestamo)
    notificaciones.enviar_avisos()
    assert not mail.outbox


def test_escenario_segundo_aviso_al_dia_siguiente_del_vencimiento(lector, libro):
    prestamo = prestar(lector, libro, vence_en=-1)
    assert notificaciones.enviar_avisos() == {POR_VENCER: 0, VENCIDO: 1}
    assert "está vencido" in mail.outbox[0].subject
    assert f"venció el {prestamo.fecha_devolucion:%d/%m/%Y} (hace 1 día)" in mail.outbox[0].body
    notificaciones.enviar_avisos()
    assert len(mail.outbox) == 1, "el aviso de vencido también sale una sola vez"


def test_un_prestamo_renovado_avisa_otra_vez_con_la_fecha_nueva(lector, libro):
    prestamo = prestar(lector, libro, vence_en=2)
    notificaciones.enviar_avisos()
    nueva = servicios.renovar_prestamo(prestamo)
    notificaciones.enviar_avisos()
    assert len(mail.outbox) == 1, "con la fecha nueva faltan más de 2 días"
    notificaciones.enviar_avisos(hoy=nueva - timedelta(days=2))
    assert len(mail.outbox) == 2
    assert "ya se renovó una vez" in mail.outbox[1].body


def test_el_comando_diario_envia_los_avisos(lector, bibliotecario, libro):
    prestar(lector, libro, vence_en=1)
    salida = StringIO()
    call_command("enviar_avisos", stdout=salida)
    assert "Avisos enviados: 1 por vencer y 0 vencidos." in salida.getvalue()
    assert len(mail.outbox) == 1


def test_el_comando_acepta_una_fecha(lector, libro):
    prestamo = prestar(lector, libro, vence_en=10)
    salida = StringIO()
    call_command("enviar_avisos", fecha=(prestamo.fecha_devolucion + timedelta(days=1)).isoformat(), stdout=salida)
    assert "0 por vencer y 1 vencidos" in salida.getvalue()


def test_cuando_una_reserva_queda_lista_se_avisa_por_correo(lector, libro):
    # HU-13: al devolver el libro, quien lo reservó recibe un correo con la hora límite.
    carlos = crear_usuario("carlos@bibliotrack.test", "1002", nombre="Carlos", apellido="Pérez")
    libro.total_ejemplares = libro.disponibles = 1
    libro.save()
    prestamo = servicios.crear_prestamo(carlos, libro)
    reserva = servicios.crear_reserva(lector, libro)
    servicios.registrar_devolucion(prestamo)
    reserva.refresh_from_db()
    assert reserva.estado == Reserva.ACTIVA and reserva.guardada_hasta
    assert len(mail.outbox) == 1 and mail.outbox[0].to == ["ana@bibliotrack.test"]
    assert "tu reserva de «Clean Code» está lista" in mail.outbox[0].subject

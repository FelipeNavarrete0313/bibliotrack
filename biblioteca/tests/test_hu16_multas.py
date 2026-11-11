"""HU-16 · Calcular la multa por devolución tardía (issue #25)."""

from datetime import date, timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from biblioteca import servicios
from biblioteca.models import Libro, Multa, Prestamo, Solicitud
from biblioteca.tests.conftest import crear_usuario
from bibliotrack.multas import dias_de_multa
from bibliotrack.prestamos import PrestamoNoPermitido

MULTAS = reverse("multas")


def prestar(lector, libro, vence):
    libro.disponibles -= 1
    libro.save(update_fields=["disponibles"])
    return Prestamo.objects.create(lector=lector, libro=libro, fecha_prestamo=vence - timedelta(days=15), fecha_devolucion=vence)


def con_multa(lector, libro):
    """Devuelve el martes 10 un préstamo que vencía el viernes 6 de noviembre de 2026: 3 días (sin el domingo)."""
    prestamo = prestar(lector, libro, date(2026, 11, 6))
    servicios.registrar_devolucion(prestamo, hoy=date(2026, 11, 10))
    return Multa.objects.get(prestamo=prestamo)


def test_escenario_la_multa_se_calcula_por_dia_de_retraso(lector, libro, settings):
    # Dado un préstamo que vencía el viernes 6, cuando se devuelve el martes 10,
    # entonces la multa es de 3 días (sábado, lunes y martes) por el valor configurado.
    settings.MULTA_POR_DIA = 1500
    multa = con_multa(lector, libro)
    assert (multa.dias, multa.valor, multa.estado, multa.lector) == (3, 4500, Multa.PENDIENTE, lector)
    assert multa.en_pesos == "$4.500"


def test_escenario_domingos_y_festivos_no_cuentan(lector, libro):
    # Vencía el sábado 14 y se devuelve el lunes 16 de noviembre (festivo): domingo y festivo no se cobran.
    prestamo = prestar(lector, libro, date(2026, 11, 14))
    assert servicios.registrar_devolucion(prestamo, hoy=date(2026, 11, 16)) == 2, "son 2 días de retraso en el calendario"
    assert not Multa.objects.exists()


def test_devolver_a_tiempo_no_genera_multa(lector, libro):
    servicios.registrar_devolucion(servicios.crear_prestamo(lector, libro))
    assert not Multa.objects.exists()


def test_la_pagina_de_devolucion_muestra_la_multa(client, bibliotecario, lector, libro):
    hoy = timezone.localdate()
    prestamo = prestar(lector, libro, hoy - timedelta(days=10))
    client.force_login(bibliotecario.usuario)
    contenido = client.post(reverse("registrar_devolucion", args=[prestamo.pk]), follow=True).content.decode()
    dias = dias_de_multa(prestamo.fecha_devolucion, hoy)
    assert "Se entregó con 10 día(s) de retraso." in contenido
    assert f"Multa: ${dias}.000 por {dias} día(s) hábil(es)." in contenido


def test_escenario_con_multas_pendientes_no_hay_nuevos_prestamos(client, lector, libro):
    con_multa(lector, libro)
    otro = Libro.objects.create(titulo="Cosmos", autor="Carl Sagan", isbn="978-8408053224", categoria="Ciencia")
    with pytest.raises(PrestamoNoPermitido, match="multas pendientes"):
        servicios.crear_prestamo(lector, otro)
    client.force_login(lector.usuario)
    contenido = client.post(reverse("solicitar_prestamo", args=[otro.pk]), follow=True).content.decode()
    assert "Tienes una multa pendiente." in contenido and not Solicitud.objects.exists()
    mis = client.get(reverse("mis_prestamos")).content.decode()
    assert "Tienes 1 multa pendiente" in mis and "$3.000" in mis


def test_escenario_el_bibliotecario_registra_el_pago(client, bibliotecario, lector, libro):
    multa = con_multa(lector, libro)
    client.force_login(bibliotecario.usuario)
    lista = client.get(MULTAS).content.decode()
    assert "Ana María Gómez" in lista and "$3.000" in lista
    contenido = client.post(reverse("pagar_multa", args=[multa.pk]), follow=True).content.decode()
    assert "Pago registrado: $3.000 de Ana María Gómez por «Clean Code»." in contenido
    assert "No hay multas pendientes." in contenido
    multa.refresh_from_db()
    assert multa.estado == Multa.PAGADA and multa.pagada == timezone.localdate()
    servicios.crear_prestamo(lector, libro)  # ya puede pedir préstamos otra vez


def test_una_multa_no_se_paga_dos_veces(client, bibliotecario, lector, libro):
    multa = con_multa(lector, libro)
    client.force_login(bibliotecario.usuario)
    client.post(reverse("pagar_multa", args=[multa.pk]))
    assert "La multa ya estaba pagada." in client.post(reverse("pagar_multa", args=[multa.pk]), follow=True).content.decode()


def test_buscar_multas_por_documento(client, bibliotecario, lector, libro):
    con_multa(lector, libro)
    carlos = crear_usuario("carlos@bibliotrack.test", "1002", nombre="Carlos", apellido="Pérez")
    client.force_login(bibliotecario.usuario)
    assert "Ana María Gómez" in client.get(MULTAS, {"documento": "1001"}).content.decode()
    vacio = client.get(MULTAS, {"documento": carlos.documento}).content.decode()
    assert "no tiene multas pendientes" in vacio and "Ana María Gómez" not in vacio


def test_solo_el_personal_gestiona_las_multas(client, lector, libro):
    multa = con_multa(lector, libro)
    assert client.get(MULTAS).status_code == 302
    client.force_login(lector.usuario)
    assert client.get(MULTAS).status_code == 403
    assert client.post(reverse("pagar_multa", args=[multa.pk])).status_code == 403
    multa.refresh_from_db()
    assert multa.estado == Multa.PENDIENTE

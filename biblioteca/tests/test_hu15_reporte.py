"""HU-15 · Reporte de los libros más prestados (issue #24)."""

from datetime import date, timedelta
from io import BytesIO

from django.urls import reverse
from django.utils import timezone
from openpyxl import load_workbook

from biblioteca.models import Libro, Prestamo

REPORTE = reverse("reporte_mas_prestados")


def prestar(lector, libro, dia, veces=1):
    for _ in range(veces):
        Prestamo.objects.create(lector=lector, libro=libro, fecha_prestamo=dia, fecha_devolucion=dia + timedelta(days=15),
                                estado=Prestamo.DEVUELTO, fecha_entrega=dia + timedelta(days=10))


def cosmos():
    return Libro.objects.create(titulo="Cosmos", autor="Carl Sagan", isbn="978-8408053224", categoria="Ciencia")


def test_escenario_los_mas_prestados_del_periodo(client, administrador, lector, libro):
    # Dado que en el mes «Clean Code» se prestó 3 veces y «Cosmos» 1, cuando el administrador abre el reporte,
    # entonces los ve en ese orden.
    hoy = timezone.localdate()
    prestar(lector, libro, hoy, veces=3)
    prestar(lector, cosmos(), hoy)
    client.force_login(administrador.usuario)
    contenido = client.get(REPORTE).content.decode()
    assert contenido.index("Clean Code") < contenido.index("Cosmos")
    assert "<td><b>3</b></td>" in contenido and "suman 4 préstamos" in contenido


def test_escenario_filtrar_por_fechas_y_categoria(client, administrador, lector, libro):
    prestar(lector, libro, date(2026, 9, 10))
    prestar(lector, cosmos(), date(2026, 10, 5))
    client.force_login(administrador.usuario)
    octubre = client.get(REPORTE, {"desde": "2026-10-01", "hasta": "2026-10-31"}).content.decode()
    assert "<td>Cosmos</td>" in octubre and "<td>Clean Code</td>" not in octubre
    ciencia = client.get(REPORTE, {"desde": "2026-09-01", "hasta": "2026-10-31", "categoria": "Ciencia"}).content.decode()
    assert "<td>Cosmos</td>" in ciencia and "<td>Clean Code</td>" not in ciencia
    vacio = client.get(REPORTE, {"desde": "2026-01-01", "hasta": "2026-01-31"}).content.decode()
    assert "No hubo préstamos en ese período." in vacio


def test_escenario_descargar_en_excel(client, administrador, lector, libro):
    prestar(lector, libro, date(2026, 10, 5), veces=2)
    client.force_login(administrador.usuario)
    respuesta = client.get(REPORTE, {"desde": "2026-10-01", "hasta": "2026-10-31", "formato": "xlsx"})
    assert respuesta["Content-Type"].endswith("spreadsheetml.sheet")
    assert "mas-prestados-20261001-20261031.xlsx" in respuesta["Content-Disposition"]
    filas = list(load_workbook(BytesIO(respuesta.content)).active.values)
    assert filas[3] == ("Puesto", "Título", "Autor", "Categoría", "ISBN", "Préstamos")
    assert filas[4] == (1, "Clean Code", "Robert C. Martin", "Programación", "978-0132350884", 2)


def test_fechas_mal_escritas_usan_el_mes_actual(client, administrador):
    client.force_login(administrador.usuario)
    assert client.get(REPORTE, {"desde": "ayer", "hasta": "32/13/2026"}).status_code == 200


def test_solo_el_administrador_ve_los_reportes(client, bibliotecario, lector):
    assert client.get(REPORTE).status_code == 302
    for perfil in (lector, bibliotecario):
        client.force_login(perfil.usuario)
        assert client.get(REPORTE).status_code == 403

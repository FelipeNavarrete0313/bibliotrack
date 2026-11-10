from datetime import date

import pytest

from bibliotrack.prestamos import PrestamoNoPermitido, fecha_de_devolucion, registrar_prestamo


def lector(activos=0):
    return {"documento": "1001", "prestamos_activos": activos}


def libro(disponibles=2):
    return {"isbn": "978-0132350884", "disponibles": disponibles}


def test_fecha_de_devolucion_es_15_dias_despues():
    # lunes 2 de noviembre de 2026 + 15 días = martes 17 de noviembre
    assert fecha_de_devolucion(date(2026, 11, 2)) == date(2026, 11, 17)


def test_si_la_devolucion_cae_domingo_pasa_al_lunes():
    # sábado 7 de noviembre + 15 días = domingo 22, se pasa al lunes 23
    assert fecha_de_devolucion(date(2026, 11, 7)) == date(2026, 11, 23)


def test_registrar_prestamo_descuenta_un_ejemplar():
    el_libro = libro(disponibles=2)
    prestamo = registrar_prestamo(lector(), el_libro, hoy=date(2026, 11, 2))
    assert el_libro["disponibles"] == 1
    assert prestamo["estado"] == "activo"
    assert prestamo["fecha_devolucion"] == date(2026, 11, 17)


def test_no_se_presta_a_un_lector_con_3_prestamos_activos():
    with pytest.raises(PrestamoNoPermitido):
        registrar_prestamo(lector(activos=3), libro())


def test_no_se_presta_un_libro_sin_ejemplares():
    with pytest.raises(PrestamoNoPermitido):
        registrar_prestamo(lector(), libro(disponibles=0))

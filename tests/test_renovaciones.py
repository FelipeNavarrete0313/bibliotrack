from datetime import date

import pytest

from bibliotrack.renovaciones import RenovacionNoPermitida, renovar

HOY = date(2026, 11, 10)  # martes


def prestamo(vence=date(2026, 11, 20), renovado=False, estado="activo"):
    return {"estado": estado, "fecha_devolucion": vence, "renovado": renovado}


def test_renovar_corre_la_fecha_7_dias():
    assert renovar(prestamo(), HOY) == date(2026, 11, 27)


def test_se_puede_renovar_el_dia_que_vence():
    assert renovar(prestamo(vence=HOY), HOY) == date(2026, 11, 17)


def test_no_se_renueva_un_prestamo_vencido():
    with pytest.raises(RenovacionNoPermitida, match="vencido"):
        renovar(prestamo(vence=date(2026, 11, 9)), HOY)


def test_no_se_renueva_dos_veces():
    with pytest.raises(RenovacionNoPermitida, match="ya se renovó"):
        renovar(prestamo(renovado=True), HOY)


def test_no_se_renueva_si_otro_lector_reservo_el_libro():
    with pytest.raises(RenovacionNoPermitida, match="reservado"):
        renovar(prestamo(), HOY, reservas_de_otros=1)


def test_no_se_renueva_un_prestamo_devuelto():
    with pytest.raises(RenovacionNoPermitida, match="devuelto"):
        renovar(prestamo(estado="devuelto"), HOY)


def test_si_la_nueva_fecha_cae_domingo_pasa_al_lunes():
    assert renovar(prestamo(vence=date(2026, 11, 15)), HOY) == date(2026, 11, 23)

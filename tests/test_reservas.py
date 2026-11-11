from datetime import datetime

import pytest

from bibliotrack.reservas import (
    ReservaNoPermitida,
    ejemplares_libres,
    guardar_hasta,
    reservas_por_guardar,
    validar_reserva,
)

AGOTADO = {"id": 7, "disponibles": 0}


def lector(reservas=0, reservados=(), prestados=()):
    return {"reservas_activas": reservas, "libros_reservados": set(reservados), "libros_prestados": set(prestados)}


def test_se_puede_reservar_un_libro_agotado():
    validar_reserva(lector(), AGOTADO)


def test_no_se_reserva_un_libro_con_ejemplares():
    with pytest.raises(ReservaNoPermitida, match="puedes pedirlo prestado"):
        validar_reserva(lector(), {"id": 7, "disponibles": 1})


def test_no_se_reserva_dos_veces_el_mismo_libro():
    with pytest.raises(ReservaNoPermitida, match="reserva activa de este libro"):
        validar_reserva(lector(reservas=1, reservados=[7]), AGOTADO)


def test_no_se_reserva_un_libro_que_ya_se_tiene_prestado():
    with pytest.raises(ReservaNoPermitida, match="prestado"):
        validar_reserva(lector(prestados=[7]), AGOTADO)


def test_maximo_2_reservas_activas():
    validar_reserva(lector(reservas=1, reservados=[3]), AGOTADO)
    with pytest.raises(ReservaNoPermitida, match="2 reservas activas"):
        validar_reserva(lector(reservas=2, reservados=[3, 4]), AGOTADO)


def test_el_ejemplar_se_guarda_48_horas():
    assert guardar_hasta(datetime(2026, 11, 10, 9, 30)) == datetime(2026, 11, 12, 9, 30)


def test_se_guarda_para_quien_reservo_primero():
    assert reservas_por_guardar(["ana", "carlos"], disponibles=1, guardados=0) == ["ana"]
    assert reservas_por_guardar(["ana", "carlos"], disponibles=2, guardados=0) == ["ana", "carlos"]


def test_no_se_guarda_mas_de_lo_que_hay():
    assert reservas_por_guardar(["carlos"], disponibles=1, guardados=1) == []
    assert reservas_por_guardar(["carlos"], disponibles=0, guardados=0) == []


def test_ejemplares_libres_descuenta_guardados_y_solicitados():
    assert ejemplares_libres(3, 1, 1) == 1
    assert ejemplares_libres(1, 1) == 0
    assert ejemplares_libres(0, 1) == 0

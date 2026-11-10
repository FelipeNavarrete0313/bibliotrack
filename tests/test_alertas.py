from datetime import date

from bibliotrack.alertas import AL_DIA, POR_VENCER, VENCIDO, estado_del_prestamo

HOY = date(2026, 11, 10)


def test_un_prestamo_con_fecha_pasada_esta_vencido():
    assert estado_del_prestamo(date(2026, 11, 9), HOY) == VENCIDO


def test_vence_en_3_dias_o_menos_esta_por_vencer():
    assert estado_del_prestamo(date(2026, 11, 13), HOY) == POR_VENCER
    assert estado_del_prestamo(HOY, HOY) == POR_VENCER


def test_vence_en_mas_de_3_dias_esta_al_dia():
    assert estado_del_prestamo(date(2026, 11, 14), HOY) == AL_DIA

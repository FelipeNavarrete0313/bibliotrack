from datetime import date

from bibliotrack.avisos import POR_VENCER, VENCIDO, aviso_que_toca

VENCE = date(2026, 11, 20)


def test_dos_dias_antes_toca_el_aviso_por_vencer():
    assert aviso_que_toca(VENCE, date(2026, 11, 18)) == POR_VENCER


def test_tres_dias_antes_todavia_no_se_avisa():
    assert aviso_que_toca(VENCE, date(2026, 11, 17)) is None


def test_el_aviso_por_vencer_sale_una_sola_vez():
    assert aviso_que_toca(VENCE, date(2026, 11, 19), por_vencer_enviado=True) is None


def test_si_un_dia_no_se_envio_sale_al_siguiente():
    assert aviso_que_toca(VENCE, date(2026, 11, 19)) == POR_VENCER
    assert aviso_que_toca(VENCE, VENCE) == POR_VENCER


def test_el_dia_siguiente_al_vencimiento_toca_el_segundo_aviso():
    assert aviso_que_toca(VENCE, date(2026, 11, 21), por_vencer_enviado=True) == VENCIDO


def test_el_aviso_de_vencido_sale_una_sola_vez():
    assert aviso_que_toca(VENCE, date(2026, 11, 25), por_vencer_enviado=True, vencido_enviado=True) is None

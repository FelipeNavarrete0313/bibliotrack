from datetime import date

from bibliotrack.devoluciones import dias_de_retraso


def test_entrega_a_tiempo_no_tiene_retraso():
    assert dias_de_retraso(date(2026, 11, 17), date(2026, 11, 17)) == 0


def test_entrega_anticipada_no_tiene_retraso():
    assert dias_de_retraso(date(2026, 11, 17), date(2026, 11, 10)) == 0


def test_entrega_tardia_cuenta_los_dias_de_retraso():
    assert dias_de_retraso(date(2026, 11, 17), date(2026, 11, 20)) == 3

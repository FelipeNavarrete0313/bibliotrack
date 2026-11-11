from datetime import date

from bibliotrack.multas import dias_de_multa, domingo_de_pascua, festivos_de_colombia, valor_de_la_multa


def test_domingo_de_pascua():
    assert domingo_de_pascua(2026) == date(2026, 4, 5)
    assert domingo_de_pascua(2027) == date(2027, 3, 28)


def test_festivos_de_colombia_en_2026():
    esperados = {
        date(2026, 1, 1), date(2026, 1, 12), date(2026, 3, 23), date(2026, 4, 2), date(2026, 4, 3), date(2026, 5, 1),
        date(2026, 5, 18), date(2026, 6, 8), date(2026, 6, 15), date(2026, 6, 29), date(2026, 7, 20), date(2026, 8, 7),
        date(2026, 8, 17), date(2026, 10, 12), date(2026, 11, 2), date(2026, 11, 16), date(2026, 12, 8), date(2026, 12, 25),
    }
    assert festivos_de_colombia(2026) == esperados


def test_entrega_a_tiempo_no_tiene_multa():
    assert dias_de_multa(date(2026, 11, 20), date(2026, 11, 20)) == 0
    assert dias_de_multa(date(2026, 11, 20), date(2026, 11, 18)) == 0


def test_cada_dia_de_retraso_cuenta():
    # Vence el martes 3 de noviembre y se entrega el viernes 6: miércoles, jueves y viernes.
    assert dias_de_multa(date(2026, 11, 3), date(2026, 11, 6)) == 3


def test_el_domingo_no_cuenta():
    # Vence el viernes 20 y se entrega el lunes 23: cuentan sábado y lunes.
    assert dias_de_multa(date(2026, 11, 20), date(2026, 11, 23)) == 2


def test_los_festivos_no_cuentan():
    # Vence el viernes 13 de noviembre y se entrega el martes 17: el lunes 16 es festivo.
    assert dias_de_multa(date(2026, 11, 13), date(2026, 11, 17)) == 2


def test_el_valor_es_por_dia():
    assert valor_de_la_multa(3, 1000) == 3000

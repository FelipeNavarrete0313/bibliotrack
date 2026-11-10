from datetime import date

from bibliotrack.devoluciones import devolver_ejemplar, dias_de_retraso


def test_entrega_a_tiempo_no_tiene_retraso():
    assert dias_de_retraso(date(2026, 11, 17), date(2026, 11, 17)) == 0


def test_entrega_anticipada_no_tiene_retraso():
    assert dias_de_retraso(date(2026, 11, 17), date(2026, 11, 10)) == 0


def test_entrega_tardia_cuenta_los_dias_de_retraso():
    assert dias_de_retraso(date(2026, 11, 17), date(2026, 11, 20)) == 3


def test_devolver_suma_un_ejemplar_disponible():
    assert devolver_ejemplar({"disponibles": 1, "total_ejemplares": 2})["disponibles"] == 2


def test_devolver_no_supera_el_total_de_ejemplares():
    assert devolver_ejemplar({"disponibles": 2, "total_ejemplares": 2})["disponibles"] == 2

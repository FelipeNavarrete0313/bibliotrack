from datetime import date

from bibliotrack.reportes import mas_prestados

DESDE, HASTA = date(2026, 11, 1), date(2026, 11, 30)


def prestamo(titulo, dia, categoria="Novela", mes=11):
    return {"isbn": f"isbn-{titulo}", "titulo": titulo, "autor": "Autora", "categoria": categoria,
            "fecha_prestamo": date(2026, mes, dia)}


def test_ordena_de_mas_a_menos_prestado():
    datos = [prestamo("Delirio", 3), prestamo("María", 4), prestamo("Delirio", 9)]
    assert [(f["titulo"], f["prestamos"]) for f in mas_prestados(datos, DESDE, HASTA)] == [("Delirio", 2), ("María", 1)]


def test_solo_cuenta_el_periodo_elegido():
    datos = [prestamo("Delirio", 31, mes=10), prestamo("Delirio", 1), prestamo("Delirio", 30), prestamo("Delirio", 1, mes=12)]
    assert mas_prestados(datos, DESDE, HASTA)[0]["prestamos"] == 2


def test_filtra_por_categoria():
    datos = [prestamo("Delirio", 3), prestamo("Cosmos", 4, "Ciencia")]
    assert [f["titulo"] for f in mas_prestados(datos, DESDE, HASTA, categoria="Ciencia")] == ["Cosmos"]


def test_muestra_maximo_10_libros():
    datos = [prestamo(f"Libro {n:02}", 5) for n in range(15)]
    assert len(mas_prestados(datos, DESDE, HASTA)) == 10


def test_el_empate_se_ordena_por_titulo():
    datos = [prestamo("Zama", 3), prestamo("Aura", 4)]
    assert [f["titulo"] for f in mas_prestados(datos, DESDE, HASTA)] == ["Aura", "Zama"]


def test_sin_prestamos_devuelve_lista_vacia():
    assert mas_prestados([], DESDE, HASTA) == []

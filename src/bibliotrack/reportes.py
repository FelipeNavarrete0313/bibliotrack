"""Reportes: los libros más prestados en un período (HU-15)."""

LIMITE = 10


def mas_prestados(prestamos, desde, hasta, categoria=None, limite=LIMITE):
    """Los `limite` libros con más préstamos entre `desde` y `hasta` (incluidos).

    `prestamos` es una lista de diccionarios con `isbn`, `titulo`, `autor`,
    `categoria` y `fecha_prestamo`. Devuelve una lista de diccionarios con esos
    datos del libro y `prestamos` (la cantidad), de mayor a menor. Si hay empate,
    se ordena por título.
    """
    conteo = {}
    for prestamo in prestamos:
        if not desde <= prestamo["fecha_prestamo"] <= hasta:
            continue
        if categoria and prestamo["categoria"] != categoria:
            continue
        fila = conteo.setdefault(prestamo["isbn"], {
            "isbn": prestamo["isbn"], "titulo": prestamo["titulo"], "autor": prestamo["autor"],
            "categoria": prestamo["categoria"], "prestamos": 0,
        })
        fila["prestamos"] += 1
    return sorted(conteo.values(), key=lambda fila: (-fila["prestamos"], fila["titulo"]))[:limite]

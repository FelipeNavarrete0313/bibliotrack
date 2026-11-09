"""Catálogo de libros: búsqueda por título, autor o categoría (HU-06)."""

import unicodedata


def normalizar(texto):
    """Pasa a minúsculas y quita las tildes para comparar textos (BUG-01)."""
    sin_tildes = unicodedata.normalize("NFD", texto)
    sin_tildes = "".join(c for c in sin_tildes if unicodedata.category(c) != "Mn")
    return sin_tildes.strip().lower()


def buscar(libros, texto="", categoria=None):
    """Devuelve los libros cuyo título o autor contiene `texto`.

    `libros` es una lista de diccionarios con las llaves
    `titulo`, `autor` y `categoria`. Si se indica `categoria`,
    solo se devuelven los libros de esa categoría.
    La búsqueda ignora mayúsculas y tildes.
    """
    texto = normalizar(texto)
    resultado = []
    for libro in libros:
        if categoria and normalizar(libro["categoria"]) != normalizar(categoria):
            continue
        if texto in normalizar(libro["titulo"]) or texto in normalizar(libro["autor"]):
            resultado.append(libro)
    return resultado

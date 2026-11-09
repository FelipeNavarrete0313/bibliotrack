"""Catálogo de libros: búsqueda por título, autor o categoría (HU-06)."""


def buscar(libros, texto="", categoria=None):
    """Devuelve los libros cuyo título o autor contiene `texto`.

    `libros` es una lista de diccionarios con las llaves
    `titulo`, `autor` y `categoria`. Si se indica `categoria`,
    solo se devuelven los libros de esa categoría.
    """
    texto = texto.strip().lower()
    resultado = []
    for libro in libros:
        if categoria and libro["categoria"].lower() != categoria.lower():
            continue
        if texto in libro["titulo"].lower() or texto in libro["autor"].lower():
            resultado.append(libro)
    return resultado

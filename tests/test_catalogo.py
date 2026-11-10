from bibliotrack.catalogo import buscar

LIBROS = [
    {"titulo": "Cien años de soledad", "autor": "Gabriel García Márquez", "categoria": "Novela"},
    {"titulo": "Álgebra de Baldor", "autor": "Aurelio Baldor", "categoria": "Matemáticas"},
    {"titulo": "Clean Code", "autor": "Robert C. Martin", "categoria": "Programación"},
]


def test_busca_por_parte_del_titulo():
    assert [l["titulo"] for l in buscar(LIBROS, "soledad")] == ["Cien años de soledad"]


def test_busca_por_autor_sin_importar_mayusculas():
    assert [l["titulo"] for l in buscar(LIBROS, "MARTIN")] == ["Clean Code"]


def test_filtra_por_categoria():
    assert [l["titulo"] for l in buscar(LIBROS, "", categoria="Matemáticas")] == ["Álgebra de Baldor"]


def test_sin_resultados_devuelve_lista_vacia():
    assert buscar(LIBROS, "inexistente") == []


def test_busqueda_ignora_tildes():
    # BUG-01: buscar "algebra" debe encontrar "Álgebra de Baldor"
    assert [l["titulo"] for l in buscar(LIBROS, "algebra")] == ["Álgebra de Baldor"]


def test_busqueda_ignora_tildes_en_el_autor():
    assert [l["titulo"] for l in buscar(LIBROS, "garcia marquez")] == ["Cien años de soledad"]

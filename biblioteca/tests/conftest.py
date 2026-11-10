import pytest
from django.contrib.auth import get_user_model
from django.core.cache import cache

from biblioteca.models import Libro, Perfil


@pytest.fixture(autouse=True)
def limpiar_cache():
    """Los intentos fallidos de inicio de sesión se guardan en la caché."""
    cache.clear()
    yield
    cache.clear()


def crear_usuario(correo, documento, rol=Perfil.LECTOR, contrasena="Biblio2026", nombre="Ana María", apellido="Gómez"):
    usuario = get_user_model().objects.create_user(
        username=correo, email=correo, password=contrasena, first_name=nombre, last_name=apellido,
    )
    return Perfil.objects.create(usuario=usuario, documento=documento, rol=rol)


@pytest.fixture
def lector(db):
    return crear_usuario("ana@bibliotrack.test", "1001")


@pytest.fixture
def bibliotecario(db):
    return crear_usuario("sofia@bibliotrack.test", "2001", Perfil.BIBLIOTECARIO, nombre="Sofía", apellido="Martínez")


@pytest.fixture
def libro(db):
    return Libro.objects.create(
        titulo="Clean Code", autor="Robert C. Martin", isbn="978-0132350884",
        categoria="Programación", descripcion="Buenas prácticas.", total_ejemplares=2, disponibles=2,
    )

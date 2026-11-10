"""T-02 · Diseñar el modelo de base de datos."""

from datetime import date

import pytest
from django.core.management import call_command
from django.db import IntegrityError

from biblioteca.models import Libro, Perfil, Prestamo, Reserva


def test_un_libro_no_puede_tener_mas_disponibles_que_ejemplares(db):
    with pytest.raises(IntegrityError):
        Libro.objects.create(titulo="X", autor="Y", isbn="1", categoria="Z", total_ejemplares=1, disponibles=2)


def test_el_isbn_es_unico(libro):
    with pytest.raises(IntegrityError):
        Libro.objects.create(titulo="Otro", autor="Otro", isbn=libro.isbn, categoria="Z")


def test_el_perfil_cuenta_sus_prestamos_activos(lector, libro):
    hoy = date.today()
    Prestamo.objects.create(lector=lector, libro=libro, fecha_prestamo=hoy, fecha_devolucion=hoy)
    Prestamo.objects.create(lector=lector, libro=libro, fecha_prestamo=hoy, fecha_devolucion=hoy, estado=Prestamo.DEVUELTO)
    assert lector.prestamos_activos == 1


def test_una_reserva_empieza_activa(lector, libro):
    assert Reserva.objects.create(lector=lector, libro=libro).estado == Reserva.ACTIVA


def test_los_datos_de_prueba_tienen_20_libros_y_5_usuarios(db):
    call_command("cargar_datos")
    assert Libro.objects.count() == 20
    assert Perfil.objects.count() == 5
    assert Perfil.objects.filter(rol=Perfil.BIBLIOTECARIO).count() == 1


def test_cargar_datos_dos_veces_no_duplica(db):
    call_command("cargar_datos")
    call_command("cargar_datos")
    assert Libro.objects.count() == 20
    assert Perfil.objects.count() == 5

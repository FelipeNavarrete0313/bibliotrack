"""Carga datos de prueba (T-02): 20 libros y 5 usuarios.

Uso: py manage.py cargar_datos
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from biblioteca.models import Libro, Perfil

CONTRASENA_DE_PRUEBA = "Biblio2026"

LIBROS = [
    ("Cien años de soledad", "Gabriel García Márquez", "978-0307474728", "Novela", 3, "La historia de la familia Buendía en Macondo."),
    ("El amor en los tiempos del cólera", "Gabriel García Márquez", "978-0307387264", "Novela", 1, "Florentino Ariza espera más de cincuenta años por Fermina Daza."),
    ("Crónica de una muerte anunciada", "Gabriel García Márquez", "978-1400034710", "Novela", 2, "Un crimen que todo el pueblo sabía que iba a ocurrir."),
    ("La vorágine", "José Eustasio Rivera", "978-8437611891", "Novela", 2, "Novela clásica colombiana ambientada en la selva."),
    ("María", "Jorge Isaacs", "978-8437604510", "Novela", 2, "Novela romántica ambientada en el Valle del Cauca."),
    ("Delirio", "Laura Restrepo", "978-6070706813", "Novela", 1, "Una mujer pierde la razón en la Bogotá de los años ochenta."),
    ("Álgebra de Baldor", "Aurelio Baldor", "978-6075502083", "Matemáticas", 4, "Texto clásico de álgebra con miles de ejercicios."),
    ("Cálculo de una variable", "James Stewart", "978-6075266527", "Matemáticas", 2, "Límites, derivadas e integrales con aplicaciones."),
    ("Estadística para principiantes", "Ana López", "978-8441530012", "Matemáticas", 1, "Conceptos básicos de estadística con ejemplos."),
    ("Clean Code", "Robert C. Martin", "978-0132350884", "Programación", 2, "Buenas prácticas para escribir código legible."),
    ("Aprende Python en un fin de semana", "Alfredo Moreno", "978-8409025534", "Programación", 3, "Introducción práctica al lenguaje Python."),
    ("Diseño de bases de datos", "Adoración de Miguel", "978-8478977659", "Programación", 1, "Modelo entidad-relación, normalización y SQL."),
    ("Django para principiantes", "William S. Vincent", "978-1735467207", "Programación", 2, "Construcción de aplicaciones web con Django."),
    ("Scrum: el arte de hacer el doble de trabajo", "Jeff Sutherland", "978-6070726729", "Gestión", 2, "El origen de Scrum contado por uno de sus creadores."),
    ("Ingeniería de software", "Ian Sommerville", "978-6073206037", "Gestión", 1, "Procesos, requisitos, diseño y pruebas de software."),
    ("Breve historia del tiempo", "Stephen Hawking", "978-8498892685", "Ciencia", 2, "Del Big Bang a los agujeros negros."),
    ("Cosmos", "Carl Sagan", "978-8408053224", "Ciencia", 1, "Un recorrido por el universo y la historia de la ciencia."),
    ("El gen egoísta", "Richard Dawkins", "978-8434510050", "Ciencia", 1, "La evolución vista desde los genes."),
    ("Sapiens", "Yuval Noah Harari", "978-8499926223", "Historia", 3, "Breve historia de la humanidad."),
    ("Historia mínima de Colombia", "Jorge Orlando Melo", "978-8415863707", "Historia", 2, "La historia del país en un solo volumen."),
]

# (nombre, apellido, correo, documento, rol)
USUARIOS = [
    ("Ana María", "Gómez", "ana@bibliotrack.test", "1001", Perfil.LECTOR),
    ("Carlos", "Pérez", "carlos@bibliotrack.test", "1002", Perfil.LECTOR),
    ("Laura", "Rodríguez", "laura@bibliotrack.test", "1003", Perfil.LECTOR),
    ("Sofía", "Martínez", "sofia@bibliotrack.test", "2001", Perfil.BIBLIOTECARIO),
    ("Diego", "Ramírez", "diego@bibliotrack.test", "3001", Perfil.ADMINISTRADOR),
]


class Command(BaseCommand):
    help = "Carga 20 libros y 5 usuarios de prueba."

    def handle(self, *args, **options):
        Usuario = get_user_model()
        libros = 0
        for titulo, autor, isbn, categoria, ejemplares, descripcion in LIBROS:
            _, creado = Libro.objects.get_or_create(
                isbn=isbn,
                defaults={
                    "titulo": titulo, "autor": autor, "categoria": categoria, "descripcion": descripcion,
                    "total_ejemplares": ejemplares, "disponibles": ejemplares,
                },
            )
            libros += creado
        usuarios = 0
        for nombre, apellido, correo, documento, rol in USUARIOS:
            if Usuario.objects.filter(username=correo).exists():
                continue
            usuario = Usuario.objects.create_user(
                username=correo, email=correo, password=CONTRASENA_DE_PRUEBA,
                first_name=nombre, last_name=apellido,
            )
            Perfil.objects.create(usuario=usuario, documento=documento, rol=rol)
            usuarios += 1
        self.stdout.write(self.style.SUCCESS(
            f"Listo: {libros} libros y {usuarios} usuarios nuevos. "
            f"Todos los usuarios de prueba usan la contraseña {CONTRASENA_DE_PRUEBA}."
        ))

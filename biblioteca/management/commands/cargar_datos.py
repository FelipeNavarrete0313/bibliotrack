"""Carga libros y lectores de ejemplo: py manage.py cargar_datos"""

from django.core.management.base import BaseCommand

from biblioteca.models import Lector, Libro

LIBROS = [
    ("Cien años de soledad", "Gabriel García Márquez", "978-0307474728", "Novela", 3,
     "La historia de la familia Buendía en el pueblo de Macondo."),
    ("El amor en los tiempos del cólera", "Gabriel García Márquez", "978-0307387264", "Novela", 1,
     "Florentino Ariza espera más de cincuenta años por Fermina Daza."),
    ("La vorágine", "José Eustasio Rivera", "978-8437611891", "Novela", 2,
     "Novela clásica colombiana ambientada en la selva amazónica."),
    ("Álgebra de Baldor", "Aurelio Baldor", "978-6075502083", "Matemáticas", 4,
     "Texto clásico de álgebra con miles de ejercicios resueltos."),
    ("Cálculo de una variable", "James Stewart", "978-6075266527", "Matemáticas", 2,
     "Límites, derivadas e integrales con aplicaciones."),
    ("Clean Code", "Robert C. Martin", "978-0132350884", "Programación", 2,
     "Buenas prácticas para escribir código legible y fácil de mantener."),
    ("Aprende Python en un fin de semana", "Alfredo Moreno", "978-8409025534", "Programación", 3,
     "Introducción práctica al lenguaje Python."),
    ("Diseño de bases de datos", "Adoración de Miguel", "978-8478977659", "Programación", 1,
     "Modelo entidad-relación, normalización y SQL."),
    ("Breve historia del tiempo", "Stephen Hawking", "978-8498892685", "Ciencia", 2,
     "Del Big Bang a los agujeros negros, explicado para todos."),
    ("Cosmos", "Carl Sagan", "978-8408053224", "Ciencia", 1,
     "Un recorrido por el universo y la historia de la ciencia."),
]

LECTORES = [
    ("Ana María Gómez", "1001", "ana.gomez@example.com"),
    ("Carlos Pérez", "1002", "carlos.perez@example.com"),
    ("Laura Rodríguez", "1003", "laura.rodriguez@example.com"),
    ("Andrés Torres", "1004", "andres.torres@example.com"),
    ("Valentina Ruiz", "1005", "valentina.ruiz@example.com"),
]


class Command(BaseCommand):
    help = "Carga libros y lectores de ejemplo en la base de datos."

    def handle(self, *args, **options):
        nuevos_libros = 0
        for titulo, autor, isbn, categoria, ejemplares, descripcion in LIBROS:
            _, creado = Libro.objects.get_or_create(
                isbn=isbn,
                defaults={
                    "titulo": titulo, "autor": autor, "categoria": categoria, "descripcion": descripcion,
                    "total_ejemplares": ejemplares, "disponibles": ejemplares,
                },
            )
            nuevos_libros += creado
        nuevos_lectores = 0
        for nombre, documento, correo in LECTORES:
            _, creado = Lector.objects.get_or_create(documento=documento, defaults={"nombre": nombre, "correo": correo})
            nuevos_lectores += creado
        self.stdout.write(self.style.SUCCESS(
            f"Listo: {nuevos_libros} libros y {nuevos_lectores} lectores nuevos. "
            f"Lectores de prueba: documentos 1001 a 1005."
        ))

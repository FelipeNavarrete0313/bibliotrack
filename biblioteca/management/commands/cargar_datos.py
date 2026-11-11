"""Carga datos de prueba (T-02): 20 libros y 5 usuarios.

Uso: py manage.py cargar_datos
     py manage.py cargar_datos --demo    (además crea préstamos, una reserva, una multa y una solicitud)
"""

from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from biblioteca.models import Libro, Multa, Perfil, Prestamo, Reserva, Solicitud
from bibliotrack.multas import dias_de_multa, valor_de_la_multa
from bibliotrack.prestamos import fecha_de_devolucion

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

    def add_arguments(self, parser):
        parser.add_argument("--demo", action="store_true",
                            help="Crea también actividad de ejemplo: préstamos, un vencido, una multa, una reserva y una solicitud.")

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
        if options["demo"]:
            self.cargar_actividad()

    def cargar_actividad(self):
        """Actividad de ejemplo para ver todas las páginas con datos. Solo se carga si no hay préstamos."""
        if Prestamo.objects.exists():
            self.stdout.write("Ya hay préstamos registrados: no se cargó la actividad de ejemplo.")
            return
        hoy = timezone.localdate()
        ana, carlos, laura = (Perfil.objects.get(documento=d) for d in ("1001", "1002", "1003"))
        libro = {titulo: Libro.objects.get(titulo=titulo) for titulo, *_ in LIBROS}

        def devuelto(lector, titulo, hace, tardo=10):
            """Préstamo de hace `hace` días, devuelto a los `tardo` días."""
            inicio = hoy - timedelta(days=hace)
            return Prestamo.objects.create(
                lector=lector, libro=libro[titulo], fecha_prestamo=inicio, fecha_devolucion=fecha_de_devolucion(inicio),
                fecha_entrega=inicio + timedelta(days=tardo), estado=Prestamo.DEVUELTO,
            )

        def activo(lector, titulo, vence_en):
            """Préstamo activo que vence dentro de `vence_en` días (negativo: vencido). Descuenta el ejemplar."""
            vence = hoy + timedelta(days=vence_en)
            Libro.objects.filter(pk=libro[titulo].pk).update(disponibles=libro[titulo].disponibles - 1)
            libro[titulo].refresh_from_db()
            return Prestamo.objects.create(lector=lector, libro=libro[titulo], fecha_prestamo=vence - timedelta(days=15), fecha_devolucion=vence)

        # Historial para el reporte de los más prestados
        for lector, titulo, hace in [
            (ana, "Cien años de soledad", 50), (carlos, "Cien años de soledad", 34), (laura, "Cien años de soledad", 18),
            (ana, "Clean Code", 45), (carlos, "Clean Code", 22), (laura, "Sapiens", 40), (ana, "Sapiens", 20),
            (carlos, "Álgebra de Baldor", 30), (laura, "Django para principiantes", 25), (ana, "Cosmos", 28),
        ]:
            devuelto(lector, titulo, hace)
        # Laura devolvió tarde: multa pendiente
        tarde = devuelto(laura, "María", hace=24, tardo=20)
        dias = dias_de_multa(tarde.fecha_devolucion, tarde.fecha_entrega)
        if dias:
            Multa.objects.create(prestamo=tarde, lector=laura, dias=dias, creada=tarde.fecha_entrega,
                                 valor=valor_de_la_multa(dias, settings.MULTA_POR_DIA))
        # Préstamos activos: uno al día, uno por vencer y uno vencido
        activo(ana, "Aprende Python en un fin de semana", vence_en=9)
        activo(ana, "Breve historia del tiempo", vence_en=2)
        activo(carlos, "La vorágine", vence_en=-4)
        # «Delirio» tiene 1 ejemplar: lo tiene Carlos y Ana lo reservó
        activo(carlos, "Delirio", vence_en=6)
        Reserva.objects.create(lector=ana, libro=libro["Delirio"])
        # Una solicitud pendiente para la bibliotecaria
        Solicitud.objects.create(lector=carlos, libro=libro["Scrum: el arte de hacer el doble de trabajo"])
        self.stdout.write(self.style.SUCCESS(
            "Actividad de ejemplo: 11 préstamos devueltos, 4 activos (1 vencido), 1 multa, 1 reserva y 1 solicitud."
        ))

from django.contrib import admin

from .models import Lector, Libro, Prestamo


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "categoria", "isbn", "disponibles", "total_ejemplares")
    list_filter = ("categoria",)
    search_fields = ("titulo", "autor", "isbn")


@admin.register(Lector)
class LectorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "documento", "correo", "prestamos_activos")
    search_fields = ("nombre", "documento", "correo")


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ("libro", "lector", "fecha_prestamo", "fecha_devolucion", "estado")
    list_filter = ("estado",)

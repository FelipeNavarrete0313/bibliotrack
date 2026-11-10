"""Registro en el panel interno de Django, solo para desarrollo.

Ninguna pantalla de BiblioTrack enlaza al panel. Los usuarios trabajan con las
páginas propias de la aplicación.
"""

from django.contrib import admin

from .models import Libro, Perfil, Prestamo, Reserva

admin.site.register([Perfil, Libro, Prestamo, Reserva])

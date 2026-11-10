"""Registro en el panel interno de Django, solo para desarrollo.

Ninguna pantalla de BiblioTrack enlaza al panel. Los usuarios trabajan con las
páginas propias de la aplicación.

BUG-04: el panel no guarda cambios de estado sueltos. Entregar una solicitud,
registrar o devolver un préstamo pasa por biblioteca/servicios.py, igual que en
las páginas, para que la disponibilidad de los libros siempre cuadre.
"""

from django import forms
from django.contrib import admin, messages

from bibliotrack.prestamos import PrestamoNoPermitido

from . import servicios
from .models import Libro, Perfil, Prestamo, Reserva, Solicitud

admin.site.register([Perfil, Reserva])


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ["titulo", "autor", "isbn", "categoria", "disponibles", "total_ejemplares", "activo"]
    list_filter = ["categoria", "activo"]
    search_fields = ["titulo", "autor", "isbn"]

    def get_readonly_fields(self, request, obj=None):
        # Los disponibles solo cambian con préstamos y devoluciones.
        return ["disponibles"] if obj else []


# ---------------------------------------------------------------- Solicitudes

class SolicitudAdminForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ["lector", "libro", "estado"]

    def clean(self):
        datos = super().clean()
        anterior = self.instance.estado if self.instance.pk else Solicitud.PENDIENTE
        nuevo = datos.get("estado")
        if anterior != Solicitud.PENDIENTE and nuevo != anterior:
            raise forms.ValidationError("Una solicitud entregada, rechazada o cancelada ya no cambia de estado.")
        if self.instance.pk and anterior != Solicitud.PENDIENTE and (
            datos.get("lector") != self.instance.lector or datos.get("libro") != self.instance.libro
        ):
            raise forms.ValidationError("No se puede cambiar el lector ni el libro de una solicitud ya atendida.")
        if nuevo == Solicitud.ENTREGADA and anterior == Solicitud.PENDIENTE:
            lector, libro = datos.get("lector"), datos.get("libro")
            if libro and not libro.activo:
                raise forms.ValidationError("No se puede entregar: el libro fue dado de baja.")
            if libro and libro.disponibles <= 0:
                raise forms.ValidationError("No se puede entregar: No hay ejemplares disponibles.")
            if lector and lector.prestamos_activos >= 3:
                raise forms.ValidationError("No se puede entregar: El lector ya tiene 3 préstamos activos.")
        return datos


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    form = SolicitudAdminForm
    list_display = ["libro", "lector", "estado", "creada", "atendida", "prestamo"]
    list_filter = ["estado"]
    readonly_fields = ["creada", "atendida", "prestamo"]
    actions = ["entregar_solicitudes", "rechazar_solicitudes"]

    def save_model(self, request, obj, form, change):
        nuevo = obj.estado
        if nuevo == Solicitud.PENDIENTE or (change and form.initial.get("estado") != Solicitud.PENDIENTE):
            super().save_model(request, obj, form, change)
            return
        # Se guarda como pendiente y se atiende con las mismas reglas de las páginas.
        obj.estado = Solicitud.PENDIENTE
        super().save_model(request, obj, form, change)
        if nuevo == Solicitud.ENTREGADA:
            try:
                prestamo = servicios.entregar_solicitud(obj)
            except PrestamoNoPermitido as error:
                self.message_user(request, f"No se pudo entregar: {error}. La solicitud sigue pendiente.", messages.ERROR)
            else:
                self.message_user(request, f"Préstamo creado: devolver el {prestamo.fecha_devolucion:%d/%m/%Y}. "
                                           f"Quedan {prestamo.libro.disponibles} ejemplar(es) disponible(s).")
        else:
            servicios.cerrar_solicitud(obj, nuevo)

    @admin.action(description="Entregar las solicitudes seleccionadas (crea el préstamo)")
    def entregar_solicitudes(self, request, queryset):
        entregadas, errores = 0, []
        for solicitud in queryset.filter(estado=Solicitud.PENDIENTE).select_related("libro", "lector__usuario"):
            try:
                servicios.entregar_solicitud(solicitud)
                entregadas += 1
            except PrestamoNoPermitido as error:
                errores.append(f"«{solicitud.libro.titulo}» para {solicitud.lector.nombre}: {error}")
        self.message_user(request, f"{entregadas} solicitud(es) entregada(s).")
        for error in errores:
            self.message_user(request, f"No se pudo entregar {error}.", messages.ERROR)

    @admin.action(description="Rechazar las solicitudes seleccionadas")
    def rechazar_solicitudes(self, request, queryset):
        pendientes = list(queryset.filter(estado=Solicitud.PENDIENTE))
        for solicitud in pendientes:
            servicios.cerrar_solicitud(solicitud, Solicitud.RECHAZADA)
        self.message_user(request, f"{len(pendientes)} solicitud(es) rechazada(s).")


# ---------------------------------------------------------------- Préstamos

class PrestamoAdminForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ["lector", "libro", "fecha_prestamo", "fecha_devolucion", "renovado", "estado"]

    def clean(self):
        datos = super().clean()
        if self.instance.pk:
            if self.instance.estado == Prestamo.DEVUELTO and datos.get("estado") == Prestamo.ACTIVO:
                raise forms.ValidationError("Un préstamo devuelto no se puede volver a activar.")
            if datos.get("libro") != self.instance.libro or datos.get("lector") != self.instance.lector:
                raise forms.ValidationError("No se puede cambiar el lector ni el libro de un préstamo; devuélvelo y registra uno nuevo.")
        return datos


class NuevoPrestamoAdminForm(forms.ModelForm):
    """Al crear un préstamo en el Admin solo se elige lector y libro: las fechas salen de las reglas."""

    class Meta:
        model = Prestamo
        fields = ["lector", "libro"]

    def clean(self):
        datos = super().clean()
        lector, libro = datos.get("lector"), datos.get("libro")
        if libro and not libro.activo:
            raise forms.ValidationError("El libro fue dado de baja.")
        if libro and libro.disponibles <= 0:
            raise forms.ValidationError("No hay ejemplares disponibles.")
        if lector and lector.prestamos_activos >= 3:
            raise forms.ValidationError("El lector ya tiene 3 préstamos activos.")
        return datos


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ["libro", "lector", "fecha_prestamo", "fecha_devolucion", "fecha_entrega", "estado"]
    list_filter = ["estado"]
    search_fields = ["libro__titulo", "libro__isbn", "lector__documento"]
    actions = ["registrar_devoluciones"]

    def get_form(self, request, obj=None, **kwargs):
        kwargs["form"] = PrestamoAdminForm if obj else NuevoPrestamoAdminForm
        return super().get_form(request, obj, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        return ["fecha_entrega"] if obj else []

    def save_model(self, request, obj, form, change):
        if not change:
            try:
                creado = servicios.crear_prestamo(obj.lector, obj.libro)
            except PrestamoNoPermitido as error:
                self.message_user(request, f"No se pudo prestar: {error}.", messages.ERROR)
                return
            obj.pk = creado.pk
            obj.refresh_from_db()
            return
        devolver = form.initial.get("estado") == Prestamo.ACTIVO and obj.estado == Prestamo.DEVUELTO
        if devolver:
            obj.estado = Prestamo.ACTIVO
        super().save_model(request, obj, form, change)
        if devolver:
            retraso = servicios.registrar_devolucion(obj)
            self.message_user(request, f"Devolución registrada{f' con {retraso} día(s) de retraso' if retraso else ' a tiempo'}. "
                                       f"El libro tiene ahora {obj.libro.disponibles} ejemplar(es) disponible(s).")

    def delete_model(self, request, obj):
        servicios.borrar_prestamo(obj)

    def delete_queryset(self, request, queryset):
        for prestamo in queryset:
            servicios.borrar_prestamo(prestamo)

    @admin.action(description="Registrar la devolución de los préstamos seleccionados")
    def registrar_devoluciones(self, request, queryset):
        activos = list(queryset.filter(estado=Prestamo.ACTIVO).select_related("libro"))
        detalle = []
        for prestamo in activos:
            retraso = servicios.registrar_devolucion(prestamo)
            if retraso:
                detalle.append(f"«{prestamo.libro.titulo}» con {retraso} día(s) de retraso")
        texto = f"{len(activos)} devolución(es) registrada(s)."
        if detalle:
            texto += " Tardías: " + "; ".join(detalle) + "."
        self.message_user(request, texto)

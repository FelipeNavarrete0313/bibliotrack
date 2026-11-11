from django.urls import path

from . import views

urlpatterns = [
    path("", views.catalogo, name="catalogo"),
    path("libros/nuevo/", views.registrar_libro, name="registrar_libro"),
    path("libros/<int:pk>/", views.detalle_libro, name="detalle_libro"),
    path("prestamos/", views.prestamos, name="prestamos"),
    path("prestamos/<int:pk>/devolver/", views.registrar_devolucion, name="registrar_devolucion"),
    path("iniciar-sesion/", views.iniciar_sesion, name="iniciar_sesion"),
    path("registro/", views.registro, name="registro"),
    path("recuperar-contrasena/", views.RecuperarContrasena.as_view(), name="recuperar_contrasena"),
    path("recuperar-contrasena/enviado/", views.vistas_auth.PasswordResetDoneView.as_view(
        template_name="biblioteca/recuperar_contrasena_enviado.html"), name="recuperar_contrasena_enviado"),
    path("restablecer/<uidb64>/<token>/", views.RestablecerContrasena.as_view(), name="restablecer_contrasena"),
    path("mi-cuenta/contrasena/", views.CambiarContrasena.as_view(), name="cambiar_contrasena"),
    path("cerrar-sesion/", views.cerrar_sesion, name="cerrar_sesion"),
    path("inicio/", views.inicio, name="inicio"),
    path("multas/", views.multas, name="multas"),
    path("multas/<int:pk>/pagar/", views.pagar_multa, name="pagar_multa"),
    path("reportes/mas-prestados/", views.reporte_mas_prestados, name="reporte_mas_prestados"),
    path("usuarios/", views.usuarios, name="usuarios"),
    path("usuarios/<int:pk>/rol/", views.cambiar_rol, name="cambiar_rol"),
    path("mis-prestamos/", views.mis_prestamos, name="mis_prestamos"),
    path("mis-prestamos/<int:pk>/renovar/", views.renovar_prestamo, name="renovar_prestamo"),
    path("libros/<int:pk>/solicitar/", views.solicitar_prestamo, name="solicitar_prestamo"),
    path("libros/<int:pk>/reservar/", views.reservar_libro, name="reservar_libro"),
    path("reservas/<int:pk>/cancelar/", views.cancelar_reserva, name="cancelar_reserva"),
    path("reservas/<int:pk>/entregar/", views.entregar_reserva, name="entregar_reserva"),
    path("solicitudes/<int:pk>/cancelar/", views.cancelar_solicitud, name="cancelar_solicitud"),
    path("solicitudes/<int:pk>/entregar/", views.entregar_solicitud, name="entregar_solicitud"),
    path("solicitudes/<int:pk>/rechazar/", views.rechazar_solicitud, name="rechazar_solicitud"),
]

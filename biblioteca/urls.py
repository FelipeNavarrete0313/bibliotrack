from django.urls import path

from . import views

urlpatterns = [
    path("", views.catalogo, name="catalogo"),
    path("iniciar-sesion/", views.iniciar_sesion, name="iniciar_sesion"),
    path("registro/", views.registro, name="registro"),
    path("cerrar-sesion/", views.cerrar_sesion, name="cerrar_sesion"),
    path("inicio/", views.inicio, name="inicio"),
]

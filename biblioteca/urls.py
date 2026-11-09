from django.urls import path

from . import views

urlpatterns = [
    path("", views.catalogo, name="catalogo"),
    path("libros/<int:pk>/", views.detalle_libro, name="detalle_libro"),
    path("prestamos/", views.prestamos, name="prestamos"),
]

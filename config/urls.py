from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Panel interno de Django para desarrollo. Ninguna pantalla de BiblioTrack enlaza aquí.
    path("admin/", admin.site.urls),
    path("", include("biblioteca.urls")),
]

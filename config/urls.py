from django.contrib import admin
from django.urls import path

urlpatterns = [
    # Panel interno de Django para desarrollo. Ninguna pantalla de BiblioTrack enlaza aquí.
    path("admin/", admin.site.urls),
]

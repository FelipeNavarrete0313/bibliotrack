from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "BiblioTrack · Administración"
admin.site.site_title = "BiblioTrack"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("biblioteca.urls")),
]

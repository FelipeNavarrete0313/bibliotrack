"""BUG-04: repara los datos que quedaron mal por cambios hechos en el panel Admin.

1. Cada solicitud «entregada» sin préstamo recibe su préstamo (15 días desde que se
   atendió, domingo → lunes). Si ya no hay ejemplares o el lector tiene 3 préstamos
   activos, la solicitud vuelve a «pendiente» para que la biblioteca decida.
2. Los ejemplares disponibles de cada libro se recalculan: total menos préstamos activos.
"""

from django.db import migrations
from django.utils import timezone

from bibliotrack.prestamos import MAXIMO_PRESTAMOS_ACTIVOS, fecha_de_devolucion


def reparar(apps, schema_editor):
    Libro = apps.get_model("biblioteca", "Libro")
    Prestamo = apps.get_model("biblioteca", "Prestamo")
    Solicitud = apps.get_model("biblioteca", "Solicitud")

    def disponibles(libro):
        return libro.total_ejemplares - Prestamo.objects.filter(libro=libro, estado="activo").count()

    for solicitud in Solicitud.objects.filter(estado="entregada", prestamo__isnull=True).order_by("atendida", "creada"):
        libro, lector = solicitud.libro, solicitud.lector
        activos = Prestamo.objects.filter(lector=lector, estado="activo").count()
        if libro.activo and disponibles(libro) > 0 and activos < MAXIMO_PRESTAMOS_ACTIVOS:
            dia = timezone.localdate(solicitud.atendida) if solicitud.atendida else timezone.localdate()
            solicitud.prestamo = Prestamo.objects.create(
                lector=lector, libro=libro, fecha_prestamo=dia, fecha_devolucion=fecha_de_devolucion(dia),
            )
        else:
            solicitud.estado = "pendiente"
            solicitud.atendida = None
        solicitud.save()

    for libro in Libro.objects.all():
        correcto = max(0, min(libro.total_ejemplares, disponibles(libro)))
        if libro.disponibles != correcto:
            libro.disponibles = correcto
            libro.save(update_fields=["disponibles"])


class Migration(migrations.Migration):
    dependencies = [("biblioteca", "0002_solicitud")]
    operations = [migrations.RunPython(reparar, migrations.RunPython.noop)]

"""Envía los avisos por correo de los préstamos (HU-14) y vence las reservas guardadas (HU-13).

Uso: py manage.py enviar_avisos

Debe ejecutarse una vez al día. En Windows se programa con el Programador de tareas;
en Linux, con cron:  0 7 * * *  python manage.py enviar_avisos
"""

from datetime import date

from django.core.management.base import BaseCommand

from biblioteca import notificaciones, servicios
from bibliotrack.avisos import POR_VENCER, VENCIDO


class Command(BaseCommand):
    help = "Envía los avisos de préstamos por vencer y vencidos, y vence las reservas guardadas hace más de 48 horas."

    def add_arguments(self, parser):
        parser.add_argument("--fecha", help="Fecha a usar como «hoy», en formato AAAA-MM-DD (para pruebas).")

    def handle(self, *args, **options):
        hoy = date.fromisoformat(options["fecha"]) if options["fecha"] else None
        servicios.actualizar_reservas()
        enviados = notificaciones.enviar_avisos(hoy)
        self.stdout.write(self.style.SUCCESS(
            f"Avisos enviados: {enviados[POR_VENCER]} por vencer y {enviados[VENCIDO]} vencidos."
        ))

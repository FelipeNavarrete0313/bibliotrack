"""Multas por devolución tardía (HU-16).

La multa se cobra por cada día de retraso en que la biblioteca abre: no cuentan
los domingos ni los festivos de Colombia.
"""

from datetime import date, timedelta

DOMINGO = 6
LUNES = 0


def domingo_de_pascua(anio):
    """Fecha del Domingo de Pascua (algoritmo de Butcher para el calendario gregoriano)."""
    a, b, c = anio % 19, anio // 100, anio % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    m = (32 + 2 * e + 2 * i - h - k) % 7
    n = (a + 11 * h + 22 * m) // 451
    mes = (h + m - 7 * n + 114) // 31
    dia = (h + m - 7 * n + 114) % 31 + 1
    return date(anio, mes, dia)


def _al_lunes(fecha):
    """Ley Emiliani: si el festivo no cae lunes, se pasa al lunes siguiente."""
    return fecha + timedelta(days=(LUNES - fecha.weekday()) % 7)


def festivos_de_colombia(anio):
    """Los 18 festivos de Colombia en `anio`."""
    pascua = domingo_de_pascua(anio)
    fijos = [(1, 1), (5, 1), (7, 20), (8, 7), (12, 8), (12, 25)]
    trasladables = [(1, 6), (3, 19), (6, 29), (8, 15), (10, 12), (11, 1), (11, 11)]
    festivos = {date(anio, mes, dia) for mes, dia in fijos}
    festivos |= {_al_lunes(date(anio, mes, dia)) for mes, dia in trasladables}
    festivos |= {pascua - timedelta(days=3), pascua - timedelta(days=2)}  # Jueves y Viernes Santo
    festivos |= {pascua + timedelta(days=dias) for dias in (43, 64, 71)}  # Ascensión, Corpus Christi, Sagrado Corazón
    return festivos


def dias_de_multa(fecha_devolucion, fecha_entrega):
    """Días de retraso que se cobran: no cuentan los domingos ni los festivos."""
    dias = 0
    dia = fecha_devolucion + timedelta(days=1)
    while dia <= fecha_entrega:
        if dia.weekday() != DOMINGO and dia not in festivos_de_colombia(dia.year):
            dias += 1
        dia += timedelta(days=1)
    return dias


def valor_de_la_multa(dias, valor_por_dia):
    return dias * valor_por_dia

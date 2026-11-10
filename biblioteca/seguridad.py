"""Bloqueo por intentos fallidos de inicio de sesión (HU-02).

Después de 5 intentos fallidos con el mismo correo, la cuenta se bloquea 15 minutos.
Los contadores viven en la caché de Django.
"""

from django.core.cache import cache

MAXIMO_INTENTOS = 5
MINUTOS_DE_BLOQUEO = 15


def _clave(correo, tipo):
    return f"inicio_sesion:{tipo}:{correo.strip().lower()}"


def esta_bloqueado(correo):
    return cache.get(_clave(correo, "bloqueo")) is not None


def registrar_fallo(correo):
    """Suma un intento fallido; al llegar al máximo bloquea la cuenta."""
    clave = _clave(correo, "intentos")
    intentos = cache.get(clave, 0) + 1
    cache.set(clave, intentos, MINUTOS_DE_BLOQUEO * 60)
    if intentos >= MAXIMO_INTENTOS:
        cache.set(_clave(correo, "bloqueo"), True, MINUTOS_DE_BLOQUEO * 60)
        cache.delete(clave)
    return intentos


def limpiar_fallos(correo):
    cache.delete(_clave(correo, "intentos"))

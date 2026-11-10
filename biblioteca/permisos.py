"""Permisos por rol (HU-05 y siguientes)."""

from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def solo_personal(vista):
    """Solo el bibliotecario y el administrador pueden entrar.

    Un visitante va a «Iniciar sesión»; un lector recibe 403 (prohibido).
    """
    @login_required
    @wraps(vista)
    def envoltura(request, *args, **kwargs):
        perfil = getattr(request.user, "perfil", None)
        if not (perfil and perfil.es_personal):
            raise PermissionDenied("Solo el personal de la biblioteca puede entrar a esta página.")
        return vista(request, *args, **kwargs)
    return envoltura

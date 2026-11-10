from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from bibliotrack.catalogo import buscar

from . import seguridad
from .forms import InicioSesionForm
from .models import Libro

MENSAJE_CREDENCIALES = "Correo o contraseña incorrectos."
MENSAJE_BLOQUEO = (
    f"La cuenta está bloqueada por {seguridad.MINUTOS_DE_BLOQUEO} minutos "
    f"después de {seguridad.MAXIMO_INTENTOS} intentos fallidos."
)


def catalogo(request):
    """Catálogo web con buscador (T-07), con la búsqueda de HU-06."""
    texto = request.GET.get("q", "")
    categoria = request.GET.get("categoria", "")
    activos = Libro.objects.filter(activo=True)
    resultados = buscar([libro.como_dict() for libro in activos], texto, categoria or None)
    categorias = activos.order_by("categoria").values_list("categoria", flat=True).distinct()
    return render(request, "biblioteca/catalogo.html", {
        "resultados": resultados,
        "texto": texto,
        "categoria": categoria,
        "categorias": categorias,
        "hubo_busqueda": bool(texto or categoria),
    })


def iniciar_sesion(request):
    """HU-02: inicio de sesión con correo, error genérico y bloqueo por intentos fallidos."""
    if request.user.is_authenticated:
        return redirect("inicio")
    form = InicioSesionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        correo = form.cleaned_data["correo"].strip()
        if seguridad.esta_bloqueado(correo):
            messages.error(request, MENSAJE_BLOQUEO)
        else:
            cuenta = get_user_model().objects.filter(email__iexact=correo).first()
            usuario = None
            if cuenta:
                usuario = authenticate(request, username=cuenta.username, password=form.cleaned_data["contrasena"])
            if usuario:
                seguridad.limpiar_fallos(correo)
                login(request, usuario)
                return redirect("inicio")
            seguridad.registrar_fallo(correo)
            messages.error(request, MENSAJE_BLOQUEO if seguridad.esta_bloqueado(correo) else MENSAJE_CREDENCIALES)
    return render(request, "biblioteca/iniciar_sesion.html", {"form": form})


@require_POST
def cerrar_sesion(request):
    logout(request)
    messages.info(request, "Cerraste sesión.")
    return redirect("catalogo")


@login_required
def inicio(request):
    """HU-02: página de inicio según el rol del usuario."""
    perfil = getattr(request.user, "perfil", None)
    return render(request, "biblioteca/inicio.html", {"perfil": perfil})

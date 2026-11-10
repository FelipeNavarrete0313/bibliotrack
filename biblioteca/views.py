from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from bibliotrack.catalogo import buscar
from bibliotrack.prestamos import PrestamoNoPermitido, registrar_prestamo

from . import seguridad
from .forms import EditarLibroForm, InicioSesionForm, LibroForm, PrestamoForm, RegistroForm
from .models import Libro, Prestamo
from .permisos import solo_personal

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


def detalle_libro(request, pk):
    """HU-07: detalle y disponibilidad de un libro."""
    libro = get_object_or_404(Libro, pk=pk, activo=True)
    proxima = None
    if libro.disponibles == 0:
        proxima = libro.prestamos.filter(estado=Prestamo.ACTIVO).order_by("fecha_devolucion").first()
    return render(request, "biblioteca/detalle_libro.html", {"libro": libro, "proxima": proxima})


@solo_personal
def registrar_libro(request):
    """HU-05: registrar un libro en el catálogo (solo personal)."""
    form = LibroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        libro = form.save()
        messages.success(request, f"«{libro.titulo}» quedó registrado en el catálogo.")
        return redirect("detalle_libro", pk=libro.pk)
    return render(request, "biblioteca/registrar_libro.html", {"form": form})


@solo_personal
def editar_libro(request, pk):
    """HU-08: editar los datos de un libro, excepto el ISBN."""
    libro = get_object_or_404(Libro, pk=pk, activo=True)
    form = EditarLibroForm(request.POST or None, instance=libro)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Los cambios del libro quedaron guardados.")
        return redirect("detalle_libro", pk=libro.pk)
    return render(request, "biblioteca/editar_libro.html", {"form": form, "libro": libro})


@solo_personal
def dar_de_baja(request, pk):
    """HU-08: dar de baja un libro, con confirmación y sin préstamos activos."""
    libro = get_object_or_404(Libro, pk=pk, activo=True)
    activos = libro.prestamos.filter(estado=Prestamo.ACTIVO).count()
    if request.method == "POST":
        if activos:
            messages.error(request, f"No se puede dar de baja: tiene {activos} préstamo(s) activo(s).")
            return redirect("detalle_libro", pk=libro.pk)
        libro.activo = False
        libro.save(update_fields=["activo"])
        messages.success(request, f"«{libro.titulo}» se dio de baja. Su historial de préstamos se conserva.")
        return redirect("catalogo")
    return render(request, "biblioteca/dar_de_baja.html", {"libro": libro, "activos": activos})


@solo_personal
def prestamos(request):
    """HU-09: registrar un préstamo (solo personal) y ver los préstamos activos."""
    form = PrestamoForm(request.POST or None, initial={"libro": request.GET.get("libro")})
    if request.method == "POST" and form.is_valid():
        lector, libro = form.lector, form.cleaned_data["libro"]
        datos_libro = libro.como_dict()
        try:
            prestamo = registrar_prestamo(
                {"documento": lector.documento, "prestamos_activos": lector.prestamos_activos}, datos_libro,
            )
        except PrestamoNoPermitido as error:
            messages.error(request, str(error))
        else:
            with transaction.atomic():
                libro.disponibles = datos_libro["disponibles"]
                libro.save(update_fields=["disponibles"])
                Prestamo.objects.create(
                    lector=lector, libro=libro,
                    fecha_prestamo=prestamo["fecha_prestamo"], fecha_devolucion=prestamo["fecha_devolucion"],
                )
            messages.success(
                request,
                f"Préstamo registrado: «{libro.titulo}» para {lector.nombre}. "
                f"Debe devolverlo el {prestamo['fecha_devolucion']:%d/%m/%Y}.",
            )
            return redirect("prestamos")
    activos = Prestamo.objects.filter(estado=Prestamo.ACTIVO).select_related("lector__usuario", "libro")
    return render(request, "biblioteca/prestamos.html", {"form": form, "activos": activos})


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


def registro(request):
    """HU-01: registro de lector."""
    if request.user.is_authenticated:
        return redirect("inicio")
    form = RegistroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.guardar()
        messages.success(request, "Tu cuenta fue creada. Ya puedes iniciar sesión.")
        return redirect("iniciar_sesion")
    return render(request, "biblioteca/registro.html", {"form": form})


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

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from bibliotrack.alertas import POR_VENCER, VENCIDO, estado_del_prestamo
from bibliotrack.catalogo import buscar
from bibliotrack.prestamos import PrestamoNoPermitido
from bibliotrack.solicitudes import SolicitudNoPermitida, validar_solicitud

from . import seguridad, servicios
from .forms import InicioSesionForm, LibroForm, PrestamoForm, RegistroForm
from .models import Libro, Perfil, Prestamo, Solicitud
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
    perfil = getattr(request.user, "perfil", None)
    solicitud = None
    prestado = False
    if perfil and perfil.rol == Perfil.LECTOR:
        solicitud = perfil.solicitudes.filter(libro=libro, estado=Solicitud.PENDIENTE).first()
        prestado = perfil.prestamos.filter(libro=libro, estado=Prestamo.ACTIVO).exists()
    return render(request, "biblioteca/detalle_libro.html", {
        "libro": libro, "proxima": proxima, "solicitud": solicitud, "prestado": prestado,
    })


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
def prestamos(request):
    """HU-09: registrar un préstamo (solo personal) y ver los préstamos activos.

    También muestra las solicitudes pendientes de HU-17 para entregarlas o rechazarlas.
    """
    form = PrestamoForm(request.POST or None, initial={"libro": request.GET.get("libro")})
    if request.method == "POST" and form.is_valid():
        lector, libro = form.lector, form.cleaned_data["libro"]
        try:
            prestamo = servicios.crear_prestamo(lector, libro)
        except PrestamoNoPermitido as error:
            messages.error(request, str(error))
        else:
            messages.success(
                request,
                f"Préstamo registrado: «{libro.titulo}» para {lector.nombre}. "
                f"Debe devolverlo el {prestamo.fecha_devolucion:%d/%m/%Y}.",
            )
            return redirect("prestamos")
    buscar_prestamo = request.GET.get("buscar", "").strip()
    activos = Prestamo.objects.filter(estado=Prestamo.ACTIVO).select_related("lector__usuario", "libro")
    if buscar_prestamo:
        activos = activos.filter(Q(lector__documento=buscar_prestamo) | Q(libro__isbn=buscar_prestamo))
    pendientes = Solicitud.objects.filter(estado=Solicitud.PENDIENTE).select_related("lector__usuario", "libro")
    return render(request, "biblioteca/prestamos.html", {
        "form": form, "activos": activos, "buscar_prestamo": buscar_prestamo, "hoy": timezone.localdate(),
        "pendientes": pendientes,
    })


@solo_personal
@require_POST
def registrar_devolucion(request, pk):
    """HU-10: registrar la devolución de un préstamo activo (solo personal)."""
    prestamo = get_object_or_404(Prestamo.objects.select_related("libro", "lector__usuario"), pk=pk, estado=Prestamo.ACTIVO)
    libro = prestamo.libro
    retraso = servicios.registrar_devolucion(prestamo)
    texto = f"Devolución registrada: «{libro.titulo}» de {prestamo.lector.nombre}."
    if retraso:
        messages.warning(request, f"{texto} Se entregó con {retraso} día(s) de retraso.")
    else:
        messages.success(request, f"{texto} Se entregó a tiempo.")
    return redirect("prestamos")


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
    pendientes = Solicitud.objects.filter(estado=Solicitud.PENDIENTE).count() if perfil and perfil.es_personal else 0
    return render(request, "biblioteca/inicio.html", {"perfil": perfil, "pendientes": pendientes})


@login_required
def mis_prestamos(request):
    """HU-11: el lector consulta sus préstamos activos, con alertas, y su historial."""
    perfil = getattr(request.user, "perfil", None)
    if perfil is None:
        return render(request, "biblioteca/mis_prestamos.html", {"sin_perfil": True})
    hoy = timezone.localdate()
    activos = []
    for prestamo in perfil.prestamos.filter(estado=Prestamo.ACTIVO).select_related("libro"):
        estado = estado_del_prestamo(prestamo.fecha_devolucion, hoy)
        dias = (prestamo.fecha_devolucion - hoy).days
        if estado == VENCIDO:
            aviso = f"Vencido hace {-dias} día(s)"
        elif estado == POR_VENCER:
            aviso = "Vence hoy" if dias == 0 else f"Vence en {dias} día(s)"
        else:
            aviso = "Al día"
        activos.append({"prestamo": prestamo, "estado": estado, "aviso": aviso})
    historial = perfil.prestamos.filter(estado=Prestamo.DEVUELTO).select_related("libro").order_by("-fecha_entrega")
    solicitudes = perfil.solicitudes.select_related("libro").order_by("-creada")[:10]
    return render(request, "biblioteca/mis_prestamos.html", {
        "activos": activos, "historial": historial, "solicitudes": solicitudes,
    })


def perfil_de_lector(request):
    """Perfil del usuario si es lector; si no, 403 (prohibido)."""
    perfil = getattr(request.user, "perfil", None)
    if not (perfil and perfil.rol == Perfil.LECTOR):
        raise PermissionDenied("Solo un lector puede solicitar préstamos.")
    return perfil


@login_required
@require_POST
def solicitar_prestamo(request, pk):
    """HU-17: el lector solicita en línea el préstamo de un libro disponible."""
    perfil = perfil_de_lector(request)
    libro = get_object_or_404(Libro, pk=pk, activo=True)
    activos = perfil.prestamos.filter(estado=Prestamo.ACTIVO)
    pendientes = perfil.solicitudes.filter(estado=Solicitud.PENDIENTE)
    try:
        validar_solicitud(
            {
                "prestamos_activos": activos.count(),
                "solicitudes_pendientes": pendientes.count(),
                "libros_prestados": set(activos.values_list("libro_id", flat=True)),
                "libros_solicitados": set(pendientes.values_list("libro_id", flat=True)),
            },
            {"id": libro.pk, "disponibles": libro.disponibles},
        )
    except SolicitudNoPermitida as error:
        messages.error(request, str(error))
    else:
        Solicitud.objects.create(lector=perfil, libro=libro)
        messages.success(
            request,
            f"Solicitud enviada: «{libro.titulo}». Cuando la biblioteca la entregue, "
            "el préstamo aparecerá en «Mis préstamos».",
        )
    return redirect("detalle_libro", pk=libro.pk)


@login_required
@require_POST
def cancelar_solicitud(request, pk):
    """HU-17: el lector cancela una solicitud suya que sigue pendiente."""
    perfil = perfil_de_lector(request)
    solicitud = get_object_or_404(Solicitud, pk=pk, lector=perfil, estado=Solicitud.PENDIENTE)
    servicios.cerrar_solicitud(solicitud, Solicitud.CANCELADA)
    messages.info(request, f"Cancelaste la solicitud de «{solicitud.libro.titulo}».")
    return redirect("mis_prestamos")


@solo_personal
@require_POST
def entregar_solicitud(request, pk):
    """HU-17: el bibliotecario entrega el libro; se crea el préstamo con las reglas de HU-09."""
    solicitud = get_object_or_404(
        Solicitud.objects.select_related("libro", "lector__usuario"), pk=pk, estado=Solicitud.PENDIENTE,
    )
    try:
        prestamo = servicios.entregar_solicitud(solicitud)
    except PrestamoNoPermitido as error:
        messages.error(request, f"No se pudo entregar «{solicitud.libro.titulo}»: {error}.")
    else:
        messages.success(
            request,
            f"Entregado: «{solicitud.libro.titulo}» a {solicitud.lector.nombre}. "
            f"Debe devolverlo el {prestamo.fecha_devolucion:%d/%m/%Y}.",
        )
    return redirect("prestamos")


@solo_personal
@require_POST
def rechazar_solicitud(request, pk):
    """HU-17: el bibliotecario rechaza una solicitud pendiente."""
    solicitud = get_object_or_404(Solicitud.objects.select_related("libro", "lector__usuario"), pk=pk, estado=Solicitud.PENDIENTE)
    servicios.cerrar_solicitud(solicitud, Solicitud.RECHAZADA)
    messages.info(request, f"Rechazaste la solicitud de «{solicitud.libro.titulo}» de {solicitud.lector.nombre}.")
    return redirect("prestamos")

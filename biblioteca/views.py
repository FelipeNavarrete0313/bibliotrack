from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from bibliotrack.catalogo import buscar
from bibliotrack.prestamos import PrestamoNoPermitido, registrar_prestamo

from .forms import PrestamoForm
from .models import Libro, Prestamo


def catalogo(request):
    """HU-06: buscar libros por título, autor o categoría."""
    texto = request.GET.get("q", "")
    categoria = request.GET.get("categoria", "")
    libros = [libro.como_dict() for libro in Libro.objects.all()]
    resultados = buscar(libros, texto, categoria or None)
    categorias = Libro.objects.order_by("categoria").values_list("categoria", flat=True).distinct()
    return render(request, "biblioteca/catalogo.html", {
        "resultados": resultados,
        "texto": texto,
        "categoria": categoria,
        "categorias": categorias,
        "hubo_busqueda": bool(texto or categoria),
    })


def detalle_libro(request, pk):
    """HU-07: ver el detalle y la disponibilidad de un libro."""
    libro = get_object_or_404(Libro, pk=pk)
    proxima = None
    if libro.disponibles == 0:
        proxima = libro.prestamos.filter(estado=Prestamo.ACTIVO).order_by("fecha_devolucion").first()
    return render(request, "biblioteca/detalle_libro.html", {"libro": libro, "proxima": proxima})


def prestamos(request):
    """HU-09: registrar un préstamo, y lista de préstamos activos."""
    form = PrestamoForm(request.POST or None, initial={"libro": request.GET.get("libro")})
    if request.method == "POST" and form.is_valid():
        lector = form.lector
        libro = form.cleaned_data["libro"]
        datos_lector = {"documento": lector.documento, "prestamos_activos": lector.prestamos_activos}
        datos_libro = libro.como_dict()
        try:
            prestamo = registrar_prestamo(datos_lector, datos_libro)
        except PrestamoNoPermitido as error:
            messages.error(request, str(error))
        else:
            with transaction.atomic():
                libro.disponibles = datos_libro["disponibles"]
                libro.save(update_fields=["disponibles"])
                Prestamo.objects.create(
                    lector=lector,
                    libro=libro,
                    fecha_prestamo=prestamo["fecha_prestamo"],
                    fecha_devolucion=prestamo["fecha_devolucion"],
                )
            messages.success(
                request,
                f"Préstamo registrado: «{libro.titulo}» para {lector.nombre}. "
                f"Devolver el {prestamo['fecha_devolucion']:%d/%m/%Y}.",
            )
            return redirect("prestamos")
    activos = Prestamo.objects.filter(estado=Prestamo.ACTIVO).select_related("lector", "libro")
    return render(request, "biblioteca/prestamos.html", {"form": form, "activos": activos})

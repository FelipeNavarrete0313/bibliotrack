"""Modelo de datos de BiblioTrack (T-02).

El diagrama entidad-relación está en docs/modelo-datos.md.
"""

from django.conf import settings
from django.db import models


class Perfil(models.Model):
    """Datos de BiblioTrack de cada usuario: documento y rol."""

    LECTOR = "lector"
    BIBLIOTECARIO = "bibliotecario"
    ADMINISTRADOR = "administrador"
    ROLES = [(LECTOR, "Lector"), (BIBLIOTECARIO, "Bibliotecario"), (ADMINISTRADOR, "Administrador")]

    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil")
    documento = models.CharField(max_length=20, unique=True)
    rol = models.CharField(max_length=15, choices=ROLES, default=LECTOR)

    class Meta:
        verbose_name_plural = "perfiles"

    def __str__(self):
        return f"{self.nombre} ({self.documento})"

    @property
    def nombre(self):
        return self.usuario.get_full_name() or self.usuario.email

    @property
    def es_personal(self):
        """El bibliotecario y el administrador gestionan el catálogo y los préstamos."""
        return self.rol in (self.BIBLIOTECARIO, self.ADMINISTRADOR)

    @property
    def prestamos_activos(self):
        return self.prestamos.filter(estado=Prestamo.ACTIVO).count()


class Libro(models.Model):
    titulo = models.CharField("título", max_length=200)
    autor = models.CharField(max_length=150)
    isbn = models.CharField("ISBN", max_length=20, unique=True)
    categoria = models.CharField("categoría", max_length=80)
    descripcion = models.TextField("descripción", blank=True)
    total_ejemplares = models.PositiveIntegerField("número de ejemplares", default=1)
    disponibles = models.PositiveIntegerField("ejemplares disponibles", default=1)
    activo = models.BooleanField(default=True, help_text="Un libro dado de baja deja de aparecer en el catálogo.")

    class Meta:
        ordering = ["titulo"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(disponibles__lte=models.F("total_ejemplares")),
                name="disponibles_no_supera_total",
            ),
        ]

    def __str__(self):
        return f"{self.titulo} · {self.autor}"

    def como_dict(self):
        """Formato que usan las funciones de src/bibliotrack."""
        return {
            "id": self.pk,
            "titulo": self.titulo,
            "autor": self.autor,
            "categoria": self.categoria,
            "isbn": self.isbn,
            "disponibles": self.disponibles,
        }


class Prestamo(models.Model):
    ACTIVO = "activo"
    DEVUELTO = "devuelto"
    ESTADOS = [(ACTIVO, "Activo"), (DEVUELTO, "Devuelto")]

    lector = models.ForeignKey(Perfil, on_delete=models.PROTECT, related_name="prestamos")
    libro = models.ForeignKey(Libro, on_delete=models.PROTECT, related_name="prestamos")
    fecha_prestamo = models.DateField("fecha de préstamo")
    fecha_devolucion = models.DateField("fecha de devolución")
    fecha_entrega = models.DateField("fecha real de entrega", null=True, blank=True)
    renovado = models.BooleanField(default=False)
    estado = models.CharField(max_length=10, choices=ESTADOS, default=ACTIVO)

    class Meta:
        ordering = ["fecha_devolucion"]
        verbose_name = "préstamo"

    def __str__(self):
        return f"{self.libro.titulo} → {self.lector.nombre}"


class Reserva(models.Model):
    ACTIVA = "activa"
    ATENDIDA = "atendida"
    CANCELADA = "cancelada"
    ESTADOS = [(ACTIVA, "Activa"), (ATENDIDA, "Atendida"), (CANCELADA, "Cancelada")]

    lector = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="reservas")
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name="reservas")
    creada = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default=ACTIVA)

    class Meta:
        ordering = ["creada"]

    def __str__(self):
        return f"Reserva de {self.libro.titulo} para {self.lector.nombre}"

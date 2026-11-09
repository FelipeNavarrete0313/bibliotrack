from django.db import models


class Libro(models.Model):
    titulo = models.CharField("título", max_length=200)
    autor = models.CharField(max_length=150)
    isbn = models.CharField("ISBN", max_length=20, unique=True)
    categoria = models.CharField("categoría", max_length=80)
    descripcion = models.TextField("descripción", blank=True)
    total_ejemplares = models.PositiveIntegerField("total de ejemplares", default=1)
    disponibles = models.PositiveIntegerField("ejemplares disponibles", default=1)

    class Meta:
        ordering = ["titulo"]

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


class Lector(models.Model):
    nombre = models.CharField(max_length=150)
    documento = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(unique=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "lectores"

    def __str__(self):
        return f"{self.nombre} ({self.documento})"

    @property
    def prestamos_activos(self):
        return self.prestamos.filter(estado=Prestamo.ACTIVO).count()


class Prestamo(models.Model):
    ACTIVO = "activo"
    DEVUELTO = "devuelto"
    ESTADOS = [(ACTIVO, "Activo"), (DEVUELTO, "Devuelto")]

    lector = models.ForeignKey(Lector, on_delete=models.PROTECT, related_name="prestamos")
    libro = models.ForeignKey(Libro, on_delete=models.PROTECT, related_name="prestamos")
    fecha_prestamo = models.DateField("fecha de préstamo")
    fecha_devolucion = models.DateField("fecha de devolución")
    estado = models.CharField(max_length=10, choices=ESTADOS, default=ACTIVO)

    class Meta:
        ordering = ["fecha_devolucion"]
        verbose_name = "préstamo"

    def __str__(self):
        return f"{self.libro.titulo} → {self.lector.nombre}"

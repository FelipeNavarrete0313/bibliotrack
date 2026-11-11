from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import Libro, Perfil


class InicioSesionForm(forms.Form):
    """HU-02: iniciar sesión con correo y contraseña."""

    correo = forms.CharField(label="Correo", max_length=254, widget=forms.EmailInput(attrs={"autofocus": True, "autocomplete": "email"}))
    contrasena = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}))


class RegistroForm(forms.Form):
    """HU-01: registro de lector."""

    nombre = forms.CharField(label="Nombre", max_length=150)
    apellido = forms.CharField(label="Apellido", max_length=150)
    documento = forms.CharField(label="Documento", max_length=20)
    # BUG-02: el formato del correo se valida en el servidor, no solo en el navegador.
    correo = forms.EmailField(label="Correo", max_length=254, widget=forms.EmailInput(attrs={"autocomplete": "email"}),
                              error_messages={"invalid": "Escribe un correo válido, por ejemplo nombre@dominio.com."})
    contrasena = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
                                 help_text="Mínimo 8 caracteres. No puede ser solo números ni una contraseña muy común.")
    confirmacion = forms.CharField(label="Confirma la contraseña", widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))

    def clean_documento(self):
        documento = self.cleaned_data["documento"].strip()
        if not (documento.isdigit() and 4 <= len(documento) <= 12):
            raise forms.ValidationError("El documento solo puede tener números (de 4 a 12 dígitos).")
        if Perfil.objects.filter(documento=documento).exists():
            raise forms.ValidationError("Ya existe una cuenta con este documento.")
        return documento

    def clean_correo(self):
        correo = self.cleaned_data["correo"].strip()
        if get_user_model().objects.filter(email__iexact=correo).exists():
            raise forms.ValidationError("Ya existe una cuenta con este correo.")
        return correo

    def clean(self):
        datos = super().clean()
        contrasena, confirmacion = datos.get("contrasena"), datos.get("confirmacion")
        if contrasena:
            try:
                validate_password(contrasena)
            except forms.ValidationError as error:
                for detalle in error.error_list:
                    if detalle.code == "password_too_short":
                        self.add_error("contrasena", "La contraseña debe tener mínimo 8 caracteres.")
                    else:  # demasiado común o solo números
                        self.add_error("contrasena", detalle)
        if contrasena and confirmacion and contrasena != confirmacion:
            self.add_error("confirmacion", "Las contraseñas no coinciden.")
        return datos

    def guardar(self):
        datos = self.cleaned_data
        usuario = get_user_model().objects.create_user(
            username=datos["correo"].lower(), email=datos["correo"].lower(), password=datos["contrasena"],
            first_name=datos["nombre"], last_name=datos["apellido"],
        )
        return Perfil.objects.create(usuario=usuario, documento=datos["documento"], rol=Perfil.LECTOR)


class LibroForm(forms.ModelForm):
    """HU-05: registrar un libro."""

    class Meta:
        model = Libro
        fields = ["titulo", "autor", "isbn", "categoria", "descripcion", "total_ejemplares"]
        widgets = {"descripcion": forms.Textarea(attrs={"rows": 3})}
        error_messages = {"isbn": {"unique": "Ya existe un libro con este ISBN."}}

    def clean_total_ejemplares(self):
        total = self.cleaned_data["total_ejemplares"]
        if total < 1:
            raise forms.ValidationError("Debe haber al menos 1 ejemplar.")
        return total

    def save(self, commit=True):
        libro = super().save(commit=False)
        if libro.pk is None:
            libro.disponibles = libro.total_ejemplares
        if commit:
            libro.save()
        return libro


class PrestamoForm(forms.Form):
    """HU-09: registrar un préstamo."""

    documento = forms.CharField(label="Documento del lector", max_length=20)
    libro = forms.ModelChoiceField(label="Libro", queryset=Libro.objects.filter(activo=True), empty_label="Elige un libro")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["libro"].label_from_instance = lambda libro: f"{libro.titulo} · ISBN {libro.isbn}"

    def clean_documento(self):
        documento = self.cleaned_data["documento"].strip()
        self.lector = Perfil.objects.filter(documento=documento, rol=Perfil.LECTOR).select_related("usuario").first()
        if self.lector is None:
            raise forms.ValidationError("No hay ningún lector registrado con ese documento.")
        return documento

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import Perfil


class InicioSesionForm(forms.Form):
    """HU-02: iniciar sesión con correo y contraseña."""

    correo = forms.CharField(label="Correo", max_length=254, widget=forms.EmailInput(attrs={"autofocus": True, "autocomplete": "email"}))
    contrasena = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}))


class RegistroForm(forms.Form):
    """HU-01: registro de lector."""

    nombre = forms.CharField(label="Nombre", max_length=150)
    apellido = forms.CharField(label="Apellido", max_length=150)
    documento = forms.CharField(label="Documento", max_length=20)
    correo = forms.CharField(label="Correo", max_length=254, widget=forms.EmailInput(attrs={"autocomplete": "email"}))
    contrasena = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
                                 help_text="Mínimo 8 caracteres.")
    confirmacion = forms.CharField(label="Confirma la contraseña", widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))

    def clean_documento(self):
        documento = self.cleaned_data["documento"].strip()
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
            except forms.ValidationError:
                self.add_error("contrasena", "La contraseña debe tener mínimo 8 caracteres.")
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

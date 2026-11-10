from django import forms


class InicioSesionForm(forms.Form):
    """HU-02: iniciar sesión con correo y contraseña."""

    correo = forms.CharField(label="Correo", max_length=254, widget=forms.EmailInput(attrs={"autofocus": True, "autocomplete": "email"}))
    contrasena = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}))

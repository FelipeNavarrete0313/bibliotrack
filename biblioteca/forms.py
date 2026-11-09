from django import forms

from .models import Lector, Libro


class PrestamoForm(forms.Form):
    documento = forms.CharField(label="Documento del lector", max_length=20)
    libro = forms.ModelChoiceField(label="Libro", queryset=Libro.objects.all(), empty_label="Elige un libro")

    def clean_documento(self):
        documento = self.cleaned_data["documento"].strip()
        try:
            self.lector = Lector.objects.get(documento=documento)
        except Lector.DoesNotExist:
            raise forms.ValidationError("No hay ningún lector registrado con ese documento.")
        return documento

"""BUG-02 · El formulario de registro acepta correos sin formato válido (issue #10)."""

import pytest
from django.urls import reverse

from biblioteca.models import Perfil


def registrar(client, correo):
    return client.post(reverse("registro"), {
        "nombre": "Pipe", "apellido": "Navarrete", "documento": "1088",
        "correo": correo, "contrasena": "Biblio2026", "confirmacion": "Biblio2026",
    })


def test_pasos_del_reporte_pipe_arroba_correo_sin_dominio(client, db):
    # Pasos para reproducir: escribir «pipe@correo» (sin dominio) y enviar.
    # Resultado esperado: el formulario rechaza el correo y la cuenta no se crea.
    contenido = registrar(client, "pipe@correo").content.decode()
    assert "Escribe un correo válido" in contenido
    assert not Perfil.objects.exists()


@pytest.mark.parametrize("correo", ["pipe", "@bibliotrack.test", "pipe@", "pipe @bibliotrack.test"])
def test_otros_correos_sin_formato_valido(client, db, correo):
    assert "Escribe un correo válido" in registrar(client, correo).content.decode()
    assert not Perfil.objects.exists()


def test_un_correo_valido_se_sigue_aceptando(client, db):
    assert registrar(client, "pipe@bibliotrack.test").status_code == 302
    assert Perfil.objects.filter(documento="1088").exists()

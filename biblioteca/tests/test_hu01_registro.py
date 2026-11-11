"""HU-01 · Registro de lector.

Cada prueba sigue uno de los escenarios (Dado / Cuando / Entonces) del issue #5.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse

from biblioteca.models import Perfil

URL = reverse("registro")


def datos(**cambios):
    base = {
        "nombre": "Pipe", "apellido": "Navarrete", "documento": "1088",
        "correo": "pipe@bibliotrack.test", "contrasena": "Biblio2026", "confirmacion": "Biblio2026",
    }
    base.update(cambios)
    return base


def test_escenario_registro_exitoso(client, db):
    # Dado un visitante, cuando llena el formulario con datos válidos,
    # entonces se crea su cuenta de lector y ve un mensaje de confirmación.
    respuesta = client.post(URL, datos(), follow=True)
    assert "Tu cuenta fue creada. Ya puedes iniciar sesión." in respuesta.content.decode()
    perfil = Perfil.objects.get(documento="1088")
    assert perfil.rol == Perfil.LECTOR
    assert perfil.usuario.email == "pipe@bibliotrack.test"


def test_escenario_despues_de_registrarse_puede_iniciar_sesion(client, db):
    client.post(URL, datos())
    respuesta = client.post(reverse("iniciar_sesion"), {"correo": "pipe@bibliotrack.test", "contrasena": "Biblio2026"}, follow=True)
    assert "Hola, Pipe" in respuesta.content.decode()


def test_escenario_correo_repetido(client, lector):
    # Dado que ya existe una cuenta con ana@bibliotrack.test,
    # cuando alguien intenta registrarse con ese correo, entonces ve un error y no se crea otra cuenta.
    contenido = client.post(URL, datos(correo="ANA@bibliotrack.test")).content.decode()
    assert "Ya existe una cuenta con este correo." in contenido
    assert get_user_model().objects.count() == 1


def test_escenario_documento_repetido(client, lector):
    contenido = client.post(URL, datos(documento="1001")).content.decode()
    assert "Ya existe una cuenta con este documento." in contenido
    assert Perfil.objects.count() == 1


def test_escenario_contrasena_de_menos_de_8_caracteres(client, db):
    contenido = client.post(URL, datos(contrasena="corta1", confirmacion="corta1")).content.decode()
    assert "mínimo 8 caracteres" in contenido
    assert not Perfil.objects.exists()


def test_las_contrasenas_deben_coincidir(client, db):
    contenido = client.post(URL, datos(confirmacion="Otra2026")).content.decode()
    assert "Las contraseñas no coinciden." in contenido


def test_el_inicio_de_sesion_ofrece_registrarse(client, db):
    assert reverse("registro") in client.get(reverse("iniciar_sesion")).content.decode()


def test_el_documento_solo_acepta_numeros(client, db):
    contenido = client.post(URL, datos(documento="<x>")).content.decode()
    assert "El documento solo puede tener números (de 4 a 12 dígitos)." in contenido
    assert not Perfil.objects.exists()


def test_no_se_acepta_una_contrasena_solo_de_numeros(client, db):
    respuesta = client.post(URL, datos(contrasena="12345678", confirmacion="12345678"))
    assert respuesta.status_code == 200 and not Perfil.objects.exists()

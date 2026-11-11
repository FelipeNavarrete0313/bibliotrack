"""HU-03 · Recuperar la contraseña (issue #17), cambiarla con sesión y volver a la página pedida."""

import re
from datetime import datetime, timedelta

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import mail
from django.urls import reverse

from biblioteca import seguridad

RECUPERAR = reverse("recuperar_contrasena")
ENTRAR = reverse("iniciar_sesion")
NUEVA = "Lectura-2026"


def pedir_enlace(client, correo="ana@bibliotrack.test"):
    respuesta = client.post(RECUPERAR, {"email": correo}, follow=True)
    enlaces = re.findall(r"http://testserver(/restablecer/\S+)", mail.outbox[-1].body) if mail.outbox else []
    return respuesta.content.decode(), (enlaces[0] if enlaces else None)


def abrir(client, enlace):
    """Django redirige el enlace del correo a una dirección sin el token; devuelve esa dirección."""
    return client.get(enlace, follow=True).redirect_chain[-1][0]


def entrar(client, contrasena, correo="ana@bibliotrack.test"):
    return client.post(ENTRAR, {"correo": correo, "contrasena": contrasena})


def test_escenario_recuperar_con_el_enlace_del_correo(client, lector):
    # Dado un usuario registrado, cuando pide recuperar su contraseña,
    # entonces recibe un enlace y con él crea una contraseña nueva.
    contenido, enlace = pedir_enlace(client)
    assert "Si hay una cuenta con ese correo, te enviamos un enlace" in contenido
    assert len(mail.outbox) == 1 and mail.outbox[0].to == ["ana@bibliotrack.test"]
    assert "vence a los 30 minutos" in mail.outbox[0].body
    formulario = abrir(client, enlace)
    respuesta = client.post(formulario, {"new_password1": NUEVA, "new_password2": NUEVA}, follow=True)
    assert "Tu contraseña fue cambiada. Ya puedes iniciar sesión." in respuesta.content.decode()
    assert entrar(client, NUEVA).status_code == 302
    client.post(reverse("cerrar_sesion"))
    assert "Correo o contraseña incorrectos." in entrar(client, "Biblio2026").content.decode()


def test_escenario_el_mensaje_es_el_mismo_si_el_correo_no_existe(client, lector):
    contenido, enlace = pedir_enlace(client, "nadie@bibliotrack.test")
    assert "Si hay una cuenta con ese correo, te enviamos un enlace" in contenido
    assert enlace is None and not mail.outbox


def test_escenario_el_enlace_solo_sirve_una_vez(client, lector):
    _, enlace = pedir_enlace(client)
    client.post(abrir(client, enlace), {"new_password1": NUEVA, "new_password2": NUEVA})
    client.cookies.clear()
    assert "Este enlace ya no sirve" in client.get(enlace, follow=True).content.decode()


def test_escenario_el_enlace_vence_a_los_30_minutos(client, lector, monkeypatch):
    _, enlace = pedir_enlace(client)
    monkeypatch.setattr(PasswordResetTokenGenerator, "_now", lambda self: datetime.now() + timedelta(minutes=31))
    assert "Este enlace ya no sirve" in client.get(enlace, follow=True).content.decode()


def test_escenario_la_nueva_contrasena_cumple_las_reglas_del_registro(client, lector):
    _, enlace = pedir_enlace(client)
    formulario = abrir(client, enlace)
    for mala in ["corta1", "12345678"]:
        respuesta = client.post(formulario, {"new_password1": mala, "new_password2": mala})
        assert respuesta.status_code == 200 and "errorlist" in respuesta.content.decode()
    assert entrar(client, "Biblio2026").status_code == 302, "la contraseña anterior sigue igual"


def test_recuperar_la_contrasena_quita_el_bloqueo_por_intentos(client, lector):
    for _ in range(seguridad.MAXIMO_INTENTOS):
        entrar(client, "mala")
    assert seguridad.esta_bloqueado("ana@bibliotrack.test")
    _, enlace = pedir_enlace(client)
    client.post(abrir(client, enlace), {"new_password1": NUEVA, "new_password2": NUEVA})
    assert not seguridad.esta_bloqueado("ana@bibliotrack.test")
    assert entrar(client, NUEVA).status_code == 302


def test_el_inicio_de_sesion_ofrece_recuperar_la_contrasena(client, db):
    assert RECUPERAR in client.get(ENTRAR).content.decode()


# ------------------------------------------------------------ Cambiar la contraseña con sesión

def test_cambiar_mi_contrasena(client, lector):
    cambiar = reverse("cambiar_contrasena")
    assert client.get(cambiar).status_code == 302, "sin sesión va a «Iniciar sesión»"
    client.force_login(lector.usuario)
    datos = {"old_password": "otra", "new_password1": NUEVA, "new_password2": NUEVA}
    assert "errorlist" in client.post(cambiar, datos).content.decode(), "la contraseña actual no coincide"
    datos["old_password"] = "Biblio2026"
    assert "Tu contraseña fue cambiada." in client.post(cambiar, datos, follow=True).content.decode()
    client.post(reverse("cerrar_sesion"))
    assert entrar(client, NUEVA).status_code == 302


# ------------------------------------------------------------ Volver a la página pedida

def test_despues_de_entrar_vuelve_a_la_pagina_que_pidio(client, lector):
    destino = reverse("mis_prestamos")
    respuesta = client.get(destino)
    assert respuesta.url == f"{ENTRAR}?next={destino}"
    assert f'name="next" value="{destino}"' in client.get(respuesta.url).content.decode()
    respuesta = client.post(ENTRAR, {"correo": "ana@bibliotrack.test", "contrasena": "Biblio2026", "next": destino})
    assert respuesta.url == destino


def test_no_redirige_a_otro_sitio_despues_de_entrar(client, lector):
    respuesta = client.post(ENTRAR, {"correo": "ana@bibliotrack.test", "contrasena": "Biblio2026",
                                     "next": "https://sitio-malo.example/robar"})
    assert respuesta.url == reverse("inicio")

"""HU-02 · Inicio de sesión.

Cada prueba sigue uno de los escenarios (Dado / Cuando / Entonces) del issue #6.
"""

from django.urls import reverse

URL = reverse("iniciar_sesion")


def entrar(client, correo, contrasena, seguir=True):
    return client.post(URL, {"correo": correo, "contrasena": contrasena}, follow=seguir)


def test_escenario_credenciales_correctas_del_lector(client, lector):
    # Dado un lector registrado, cuando entra con su correo y contraseña,
    # entonces llega a su página de inicio de lector.
    respuesta = entrar(client, "ana@bibliotrack.test", "Biblio2026")
    contenido = respuesta.content.decode()
    assert respuesta.redirect_chain[-1][0] == reverse("inicio")
    assert "Hola, Ana María" in contenido
    assert "Rol: Lector" in contenido


def test_escenario_el_correo_no_distingue_mayusculas(client, lector):
    respuesta = entrar(client, "ANA@BiblioTrack.test", "Biblio2026")
    assert respuesta.redirect_chain[-1][0] == reverse("inicio")


def test_escenario_la_pagina_de_inicio_depende_del_rol(client, bibliotecario):
    contenido = entrar(client, "sofia@bibliotrack.test", "Biblio2026").content.decode()
    assert "Rol: Bibliotecario" in contenido


def test_escenario_contrasena_incorrecta_no_dice_que_dato_fallo(client, lector):
    # Dado un lector registrado, cuando escribe mal la contraseña,
    # entonces ve un mensaje genérico y sigue sin sesión.
    contenido = entrar(client, "ana@bibliotrack.test", "otra-clave").content.decode()
    assert "Correo o contraseña incorrectos." in contenido
    assert "_auth_user_id" not in client.session


def test_escenario_correo_inexistente_muestra_el_mismo_mensaje(client, db):
    contenido = entrar(client, "nadie@bibliotrack.test", "Biblio2026").content.decode()
    assert "Correo o contraseña incorrectos." in contenido


def test_escenario_cinco_intentos_fallidos_bloquean_la_cuenta(client, lector):
    # Dado un lector, cuando falla 5 veces seguidas,
    # entonces la cuenta queda bloqueada aunque después escriba la contraseña correcta.
    for _ in range(4):
        entrar(client, "ana@bibliotrack.test", "mala")
    contenido = entrar(client, "ana@bibliotrack.test", "mala").content.decode()
    assert "bloqueada por 15 minutos" in contenido
    contenido = entrar(client, "ana@bibliotrack.test", "Biblio2026").content.decode()
    assert "bloqueada por 15 minutos" in contenido
    assert "_auth_user_id" not in client.session


def test_escenario_cerrar_sesion_desde_cualquier_pantalla(client, lector):
    # Dado un lector con sesión iniciada, cuando está en el catálogo
    # y pulsa «Cerrar sesión», entonces queda sin sesión.
    client.force_login(lector.usuario)
    assert "Cerrar sesión" in client.get(reverse("catalogo")).content.decode()
    respuesta = client.post(reverse("cerrar_sesion"), follow=True)
    assert "Cerraste sesión." in respuesta.content.decode()
    assert "_auth_user_id" not in client.session


def test_mi_inicio_exige_sesion(client, db):
    respuesta = client.get(reverse("inicio"))
    assert respuesta.status_code == 302
    assert reverse("iniciar_sesion") in respuesta.url

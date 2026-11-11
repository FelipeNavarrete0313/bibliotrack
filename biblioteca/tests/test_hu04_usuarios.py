"""HU-04 · Administrar los roles de los usuarios (issue #18)."""

from django.urls import reverse

from biblioteca.models import Perfil
from biblioteca.tests.conftest import crear_usuario

USUARIOS = reverse("usuarios")


def cambiar_rol(client, perfil, rol):
    return client.post(reverse("cambiar_rol", args=[perfil.pk]), {"rol": rol}, follow=True).content.decode()


def test_escenario_solo_el_administrador_ve_la_gestion_de_usuarios(client, administrador, bibliotecario, lector):
    assert client.get(USUARIOS).status_code == 302  # visitante: va a «Iniciar sesión»
    for perfil in (lector, bibliotecario):
        client.force_login(perfil.usuario)
        assert client.get(USUARIOS).status_code == 403
        assert client.post(reverse("cambiar_rol", args=[lector.pk]), {"rol": "administrador"}).status_code == 403
        assert USUARIOS not in client.get(reverse("inicio")).content.decode()
    client.force_login(administrador.usuario)
    contenido = client.get(USUARIOS).content.decode()
    assert "Ana María Gómez" in contenido and "Sofía Martínez" in contenido
    assert USUARIOS in client.get(reverse("inicio")).content.decode()
    lector.refresh_from_db()
    assert lector.rol == Perfil.LECTOR


def test_escenario_buscar_por_nombre_o_documento(client, administrador, bibliotecario, lector):
    client.force_login(administrador.usuario)
    por_nombre = client.get(USUARIOS, {"q": "sofia"}).content.decode()  # sin tilde
    assert "Sofía Martínez" in por_nombre and "Ana María Gómez" not in por_nombre
    por_documento = client.get(USUARIOS, {"q": "1001"}).content.decode()
    assert "Ana María Gómez" in por_documento and "Sofía Martínez" not in por_documento
    assert "No hay usuarios con «zzz»." in client.get(USUARIOS, {"q": "zzz"}).content.decode()


def test_escenario_cambiar_el_rol_de_un_usuario(client, administrador, lector):
    client.force_login(administrador.usuario)
    assert "Ana María Gómez ahora es bibliotecario." in cambiar_rol(client, lector, "bibliotecario")
    lector.refresh_from_db()
    assert lector.rol == Perfil.BIBLIOTECARIO
    # El cambio aplica cuando esa persona vuelve a entrar: ya ve las páginas del personal.
    client.force_login(lector.usuario)
    assert client.get(reverse("prestamos")).status_code == 200


def test_escenario_siempre_queda_un_administrador(client, administrador):
    client.force_login(administrador.usuario)
    contenido = cambiar_rol(client, administrador, "lector")
    assert "Debe quedar al menos un administrador en el sistema." in contenido
    administrador.refresh_from_db()
    assert administrador.rol == Perfil.ADMINISTRADOR


def test_con_dos_administradores_uno_puede_dejar_de_serlo(client, administrador):
    otro = crear_usuario("otro@bibliotrack.test", "3002", Perfil.ADMINISTRADOR, nombre="Otro", apellido="Admin")
    client.force_login(administrador.usuario)
    cambiar_rol(client, otro, "lector")
    otro.refresh_from_db()
    assert otro.rol == Perfil.LECTOR


def test_no_se_acepta_un_rol_inventado(client, administrador, lector):
    client.force_login(administrador.usuario)
    assert "Ese rol no existe." in cambiar_rol(client, lector, "jefe")
    lector.refresh_from_db()
    assert lector.rol == Perfil.LECTOR


def test_la_lista_de_usuarios_se_pagina(client, administrador):
    for n in range(25):
        crear_usuario(f"lector{n}@bibliotrack.test", str(5000 + n), nombre=f"Lector {n:02}", apellido="Prueba")
    client.force_login(administrador.usuario)
    contenido = client.get(USUARIOS).content.decode()
    assert "Página 1 de 2" in contenido and contenido.count("Guardar</button>") == 20
    assert "Página 2 de 2" in client.get(USUARIOS, {"pagina": 2}).content.decode()

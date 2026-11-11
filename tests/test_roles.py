import pytest

from bibliotrack.roles import CambioDeRolNoPermitido, validar_cambio_de_rol


def test_un_lector_puede_pasar_a_bibliotecario_o_administrador():
    validar_cambio_de_rol("lector", "bibliotecario", administradores=1)
    validar_cambio_de_rol("lector", "administrador", administradores=1)


def test_no_se_quita_el_ultimo_administrador():
    with pytest.raises(CambioDeRolNoPermitido, match="al menos un administrador"):
        validar_cambio_de_rol("administrador", "lector", administradores=1)


def test_si_hay_dos_administradores_uno_puede_dejar_de_serlo():
    validar_cambio_de_rol("administrador", "bibliotecario", administradores=2)


def test_no_se_acepta_un_rol_que_no_existe():
    with pytest.raises(CambioDeRolNoPermitido, match="no existe"):
        validar_cambio_de_rol("lector", "jefe", administradores=1)

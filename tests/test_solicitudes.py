import pytest

from bibliotrack.solicitudes import SolicitudNoPermitida, validar_solicitud


def lector(activos=0, pendientes=0, prestados=(), solicitados=()):
    return {"prestamos_activos": activos, "solicitudes_pendientes": pendientes,
            "libros_prestados": set(prestados), "libros_solicitados": set(solicitados)}


LIBRO = {"id": 7, "disponibles": 2}


def test_un_lector_sin_prestamos_puede_solicitar():
    validar_solicitud(lector(), LIBRO)


def test_no_se_solicita_sin_ejemplares():
    with pytest.raises(SolicitudNoPermitida, match="No hay ejemplares disponibles"):
        validar_solicitud(lector(), {"id": 7, "disponibles": 0})


def test_no_se_repite_una_solicitud_pendiente():
    with pytest.raises(SolicitudNoPermitida, match="solicitud pendiente"):
        validar_solicitud(lector(pendientes=1, solicitados=[7]), LIBRO)


def test_no_se_solicita_un_libro_ya_prestado():
    with pytest.raises(SolicitudNoPermitida, match="prestado"):
        validar_solicitud(lector(activos=1, prestados=[7]), LIBRO)


def test_prestamos_mas_solicitudes_no_pasan_de_3():
    validar_solicitud(lector(activos=1, pendientes=1), LIBRO)
    with pytest.raises(SolicitudNoPermitida, match="3 préstamos activos o solicitudes pendientes"):
        validar_solicitud(lector(activos=2, pendientes=1), LIBRO)


def test_no_se_solicita_si_los_ejemplares_ya_estan_solicitados():
    # BUG-07: 2 disponibles y 2 solicitudes pendientes de otros lectores.
    with pytest.raises(SolicitudNoPermitida, match="ya están solicitados"):
        validar_solicitud(lector(), {"id": 7, "disponibles": 2, "solicitudes_pendientes": 2})


def test_se_solicita_si_queda_un_ejemplar_sin_solicitar():
    validar_solicitud(lector(), {"id": 7, "disponibles": 2, "solicitudes_pendientes": 1})

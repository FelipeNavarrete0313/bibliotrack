"""Configuración de Django para BiblioTrack (ambiente de desarrollo)."""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Las reglas del negocio viven en src/bibliotrack
if str(BASE_DIR / "src") not in sys.path:
    sys.path.insert(0, str(BASE_DIR / "src"))

# Cada valor se puede cambiar con una variable de entorno; sin ella, queda el de desarrollo.
# En un servidor real define BIBLIOTRACK_SECRET_KEY y BIBLIOTRACK_DEBUG=0.
SECRET_KEY = os.environ.get("BIBLIOTRACK_SECRET_KEY", "django-insecure-solo-para-desarrollo-bibliotrack")
DEBUG = os.environ.get("BIBLIOTRACK_DEBUG", "1") == "1"
ALLOWED_HOSTS = os.environ.get("BIBLIOTRACK_ALLOWED_HOSTS", "localhost,127.0.0.1,testserver").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "biblioteca",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        # BUG-05: SQLite ignora select_for_update. Con IMMEDIATE cada transacción toma
        # el bloqueo de escritura al empezar, así dos peticiones no cambian lo mismo a la vez.
        "OPTIONS": {"transaction_mode": "IMMEDIATE"},
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

LOGIN_URL = "iniciar_sesion"

# Correo (HU-03 y HU-14). En desarrollo los correos se imprimen en la terminal del servidor.
# Para enviarlos de verdad: BIBLIOTRACK_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# y los datos del servidor de correo en las variables BIBLIOTRACK_EMAIL_*.
EMAIL_BACKEND = os.environ.get("BIBLIOTRACK_EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.environ.get("BIBLIOTRACK_EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.environ.get("BIBLIOTRACK_EMAIL_PORT", "25"))
EMAIL_HOST_USER = os.environ.get("BIBLIOTRACK_EMAIL_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("BIBLIOTRACK_EMAIL_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("BIBLIOTRACK_EMAIL_TLS", "0") == "1"
DEFAULT_FROM_EMAIL = os.environ.get("BIBLIOTRACK_EMAIL_FROM", "BiblioTrack <biblioteca@bibliotrack.test>")
# Dirección pública de la aplicación, para los enlaces de los correos.
SITIO_URL = os.environ.get("BIBLIOTRACK_URL", "http://127.0.0.1:8000")

# HU-03: el enlace para recuperar la contraseña vence a los 30 minutos.
PASSWORD_RESET_TIMEOUT = 30 * 60

# El bloqueo por intentos fallidos (HU-02) vive en la caché. En archivos, no se pierde
# al reiniciar el servidor y lo comparten todos los procesos.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": BASE_DIR / ".cache",
    }
}

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

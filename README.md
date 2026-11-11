# BiblioTrack

[![CI](https://github.com/FelipeNavarrete0313/bibliotrack/actions/workflows/ci.yml/badge.svg)](https://github.com/FelipeNavarrete0313/bibliotrack/actions/workflows/ci.yml)

Sistema web de préstamos de biblioteca para un centro de formación.

> **Proyecto académico de ejemplo.** BiblioTrack es un proyecto inventado para demostrar cómo se administra y gestiona un proyecto de software con **GitHub Projects** y **Scrum**. El foco está en la gestión (backlog, estimación, issues, sprints, tablero, pull requests y trazabilidad). El código es una aplicación Django pequeña: cada historia terminada tiene su rama, su pull request y sus pruebas.

## Tablero del proyecto

**[Abrir el GitHub Project](https://github.com/users/FelipeNavarrete0313/projects/2)**

| Vista | Para qué sirve |
| --- | --- |
| Backlog | Tabla con todo el Product Backlog agrupado por sprint, con prioridad, puntos y horas |
| Board | Tablero Kanban: Todo → In progress → In review → Done |
| Current iteration | Solo el sprint en curso |
| Roadmap | Línea de tiempo con los tres sprints |

## Product Goal

Que la biblioteca gestione su catálogo, sus usuarios y sus préstamos en línea, para que un lector encuentre y pida un libro en minutos y el bibliotecario deje de llevar el control en planillas de papel.

## Cómo está organizado el trabajo

| Elemento | En GitHub | Cantidad |
| --- | --- | --- |
| Historias de usuario | Issues con la etiqueta `tipo: historia de usuario` | 17 |
| Tareas técnicas y documentación | Issues con `tipo: tarea` o `tipo: documentación` | 12 |
| Bugs | Issues con `tipo: bug` | 8 |
| Épicas | Etiquetas `épica: …` | 5 |
| Sprints | Hitos (milestones) e iteraciones del Project | 3 |
| Estimación | Campos **Estimate** (puntos) y **Horas** del Project | 112 puntos · 448 horas |

## Documentación

- [Product Backlog](docs/product-backlog.md)
- [Estimación: Planning Poker, puntos y horas](docs/estimacion.md)
- [Trazabilidad: de la historia al código](docs/trazabilidad.md)
- [Modelo de datos](docs/modelo-datos.md)
- [Prototipos de interfaz](docs/wireframes.md)
- [Cómo trabajamos: Scrum en GitHub](docs/scrum.md)
- [Definición de terminado](docs/definicion-de-terminado.md)
- [Sprint 1: review y retrospectiva](docs/sprints/sprint-1.md)
- [Cómo contribuir](CONTRIBUTING.md)

## Preparar la base de datos

```bash
py -m pip install -r requirements-dev.txt
py manage.py migrate         # crea la base de datos (db.sqlite3)
py manage.py cargar_datos    # 20 libros y 5 usuarios de prueba
```

Para ver todas las páginas con datos (préstamos, un vencido, una multa, una reserva y una solicitud), usa `py manage.py cargar_datos --demo`. Solo carga esa actividad si todavía no hay préstamos.

Si ya tenías una base de datos, basta con `py manage.py migrate`: las migraciones nuevas solo agregan campos y tablas.

En Mac o Linux usa `python3` en lugar de `py`.

## Ejecutar la aplicación

Después de preparar la base de datos:

```bash
py manage.py runserver
```

Abre **http://127.0.0.1:8000** en el navegador. Para detener el servidor, presiona `Ctrl + C` en la terminal.

### Páginas

| Página | Dirección | Quién la ve | Historia |
| --- | --- | --- | --- |
| Catálogo con buscador | `/` | Todos | HU-06, T-07 |
| Detalle de un libro (con «Solicitar préstamo» o «Reservar» para lectores) | `/libros/<id>/` | Todos | HU-07, HU-13, HU-17 |
| Iniciar sesión | `/iniciar-sesion/` | Visitantes | HU-02 |
| Crear una cuenta | `/registro/` | Visitantes | HU-01 |
| Recuperar la contraseña | `/recuperar-contrasena/` | Visitantes | HU-03 |
| Cambiar mi contraseña (clic en tu nombre) | `/mi-cuenta/contrasena/` | Con sesión | HU-03 |
| Mi inicio, con el resumen del día para el personal | `/inicio/` | Con sesión | HU-02 |
| Registrar un libro | `/libros/nuevo/` | Bibliotecario y administrador | HU-05 |
| Editar o dar de baja un libro | `/libros/<id>/editar/` y `/libros/<id>/baja/` | Bibliotecario y administrador | HU-08 |
| Mis préstamos: solicitudes, reservas, préstamos activos (con «Renovar») e historial | `/mis-prestamos/` | Lectores | HU-11, HU-12, HU-13, HU-17 |
| Préstamos: solicitudes pendientes, reservas listas, préstamos, vencidos y devoluciones | `/prestamos/` | Bibliotecario y administrador | HU-09, HU-10, HU-13, HU-17 |
| Multas pendientes y registro del pago | `/multas/` | Bibliotecario y administrador | HU-16 |
| Libros más prestados, con descarga en Excel | `/reportes/mas-prestados/` | Administrador | HU-15 |
| Usuarios y roles | `/usuarios/` | Administrador | HU-04 |

Ninguna pantalla enlaza al panel Admin de Django: todo se hace desde las páginas de BiblioTrack.

### Cómo se presta un libro

1. El **lector** inicia sesión, abre un libro disponible y pulsa **«Solicitar préstamo»** (HU-17). Si los ejemplares libres ya están solicitados por otros lectores, el botón no aparece (BUG-07).
2. La **bibliotecaria** entra a **Préstamos**, ve la solicitud pendiente y pulsa **«Entregar»**. Se crea el préstamo a 15 días con las reglas de HU-09. También puede **«Rechazar»**.
3. El lector ve su préstamo y la fecha de devolución en **Mis préstamos** (HU-11). Puede cancelar una solicitud mientras siga pendiente, y **renovar** un préstamo una vez, por 7 días, si no está vencido ni reservado por otro lector (HU-12).
4. Cuando devuelve el libro, la bibliotecaria pulsa **«Registrar devolución»** en Préstamos (HU-10). Si hay retraso, se muestran los días y la multa.

La bibliotecaria también puede prestar directamente, sin solicitud, con el documento del lector.

Si dos personas atienden la misma solicitud o el mismo préstamo al mismo tiempo (por ejemplo, con un doble clic), solo cuenta la primera; la segunda ve un aviso (BUG-05).

### Cómo se reserva un libro agotado

1. Si un libro no tiene ejemplares libres, el **lector** pulsa **«Reservar»** en su página y entra a una cola por orden de llegada (HU-13). Puede tener máximo 2 reservas activas.
2. Cuando alguien devuelve un ejemplar, se **guarda 48 horas** para la primera reserva de la cola. Nadie más puede solicitarlo ni recibirlo en ese tiempo.
3. El lector lo ve como **«Lista para recoger»** en Mis préstamos. La **bibliotecaria** lo ve en «Reservas listas para entregar» y pulsa **«Entregar»**.
4. Si pasan las 48 horas, la reserva queda «Vencida» y el ejemplar pasa a la siguiente reserva o vuelve al catálogo.

### Multas por devolución tardía

- Al registrar una devolución tardía se crea una multa: un valor por cada día de retraso, **sin contar domingos ni festivos de Colombia** (HU-16). El valor por día es de $1.000 y se cambia con la variable de entorno `BIBLIOTRACK_MULTA_POR_DIA`.
- Un lector con multas pendientes **no puede pedir nuevos préstamos**. Las ve en «Mis préstamos».
- La bibliotecaria registra el pago en **Multas**.

### Avisos por correo

BiblioTrack envía estos correos:

| Correo | Cuándo |
| --- | --- |
| Tu préstamo vence pronto (con el enlace para renovar) | 2 días antes de la fecha de devolución (HU-14) |
| Tu préstamo está vencido | El día siguiente al vencimiento (HU-14) |
| Tu reserva está lista | Cuando se guarda un ejemplar para tu reserva (HU-13) |
| Crea una contraseña nueva | Cuando pides recuperar la contraseña (HU-03); el enlace dura 30 minutos |

Los dos primeros salen con este comando, que debe ejecutarse **una vez al día** (con el Programador de tareas de Windows o con `cron` en Linux):

```bash
py manage.py enviar_avisos
```

En desarrollo los correos **no se envían de verdad**: se imprimen en la terminal donde corre `runserver`. Para enviarlos, configura el servidor de correo con variables de entorno (ver «Configuración»).

### Usuarios y roles

Las cuentas nuevas se crean en «Registrarse» y empiezan como lector. El **administrador** entra a **Usuarios**, busca a la persona por nombre, documento o correo y le cambia el rol (HU-04). Siempre debe quedar al menos un administrador.

### Panel interno de Django (opcional)

Para revisar la base de datos crea un superusuario con `py manage.py createsuperuser` (escribe también el correo) y entra a `http://127.0.0.1:8000/admin/` escribiendo la dirección. El superusuario no tiene rol en BiblioTrack; para usarlo en las páginas de la aplicación, créale un Perfil desde el panel.

El panel aplica las mismas reglas que las páginas (BUG-04):

- En **Solicitudes**, grabar una solicitud como «Entregada» crea el préstamo y descuenta el ejemplar. También hay acciones para entregar o rechazar varias a la vez.
- En **Préstamos**, grabar un préstamo como «Devuelto» (o usar la acción «Registrar la devolución») suma el ejemplar.
- «Ejemplares disponibles» no se edita a mano: cambia con préstamos y devoluciones, y se recalcula al cambiar el «número de ejemplares» (BUG-06).
- Borrar un préstamo activo que vino de una solicitud devuelve el ejemplar y deja la solicitud otra vez «Pendiente» (BUG-06).

### Usuarios de prueba

Todos usan la contraseña `Biblio2026`. También puedes crear tu propia cuenta de lector en «Registrarse».

| Correo | Rol |
| --- | --- |
| ana@bibliotrack.test, carlos@bibliotrack.test y laura@bibliotrack.test | Lector |
| sofia@bibliotrack.test | Bibliotecario |
| diego@bibliotrack.test | Administrador |

## Configuración

Sin configurar nada, la aplicación corre en modo de desarrollo. Cada valor se cambia con una variable de entorno:

| Variable | Para qué sirve | Valor por defecto |
| --- | --- | --- |
| `BIBLIOTRACK_SECRET_KEY` | Clave secreta de Django. **Cámbiala en un servidor real** | Una clave solo para desarrollo |
| `BIBLIOTRACK_DEBUG` | `1` muestra errores detallados; en un servidor real usa `0` | `1` |
| `BIBLIOTRACK_ALLOWED_HOSTS` | Dominios permitidos, separados por comas | `localhost,127.0.0.1,testserver` |
| `BIBLIOTRACK_URL` | Dirección pública, para los enlaces de los correos | `http://127.0.0.1:8000` |
| `BIBLIOTRACK_MULTA_POR_DIA` | Valor de la multa por día de retraso, en pesos | `1000` |
| `BIBLIOTRACK_EMAIL_BACKEND` | Cómo se envían los correos. Para enviarlos de verdad: `django.core.mail.backends.smtp.EmailBackend` | Se imprimen en la terminal |
| `BIBLIOTRACK_EMAIL_HOST`, `_PORT`, `_USER`, `_PASSWORD`, `_TLS`, `_FROM` | Datos del servidor de correo | — |

El bloqueo por intentos fallidos de inicio de sesión se guarda en la carpeta `.cache/`, así que no se pierde al reiniciar el servidor.

## Ejecutar las pruebas

```bash
py -m pytest -v
```

Para revisar el estilo del código:

```bash
py -m ruff check .
```

## Estructura

```
manage.py          punto de entrada de Django
config/            configuración de Django
biblioteca/        app de Django: modelos, vistas, plantillas, datos de prueba y sus pruebas
src/bibliotrack/   reglas del negocio (búsqueda, préstamos, renovaciones, reservas, multas, avisos, roles y reportes), sin Django
tests/             pruebas de las reglas del negocio
docs/              backlog, Scrum y sprints
.github/           plantillas de issues y PR, y el workflow de CI
```

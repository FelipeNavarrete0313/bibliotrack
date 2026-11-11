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
| Detalle de un libro (y «Solicitar préstamo» para lectores) | `/libros/<id>/` | Todos | HU-07, HU-17 |
| Iniciar sesión | `/iniciar-sesion/` | Visitantes | HU-02 |
| Crear una cuenta | `/registro/` | Visitantes | HU-01 |
| Mi inicio | `/inicio/` | Con sesión | HU-02 |
| Registrar un libro | `/libros/nuevo/` | Bibliotecario y administrador | HU-05 |
| Mis préstamos: solicitudes, préstamos activos (con «Renovar») e historial | `/mis-prestamos/` | Lectores | HU-11, HU-12, HU-17 |
| Préstamos: solicitudes pendientes, préstamos y devoluciones | `/prestamos/` | Bibliotecario y administrador | HU-09, HU-10, HU-17 |

Ninguna pantalla enlaza al panel Admin de Django: todo se hace desde las páginas de BiblioTrack.

### Cómo se presta un libro

1. El **lector** inicia sesión, abre un libro disponible y pulsa **«Solicitar préstamo»** (HU-17). Si los ejemplares libres ya están solicitados por otros lectores, el botón no aparece (BUG-07).
2. La **bibliotecaria** entra a **Préstamos**, ve la solicitud pendiente y pulsa **«Entregar»**. Se crea el préstamo a 15 días con las reglas de HU-09. También puede **«Rechazar»**.
3. El lector ve su préstamo y la fecha de devolución en **Mis préstamos** (HU-11). Puede cancelar una solicitud mientras siga pendiente, y **renovar** un préstamo una vez, por 7 días, si no está vencido ni reservado por otro lector (HU-12).
4. Cuando devuelve el libro, la bibliotecaria pulsa **«Registrar devolución»** en Préstamos (HU-10). Si hay retraso, se muestran los días.

La bibliotecaria también puede prestar directamente, sin solicitud, con el documento del lector.

Si dos personas atienden la misma solicitud o el mismo préstamo al mismo tiempo (por ejemplo, con un doble clic), solo cuenta la primera; la segunda ve un aviso (BUG-05).

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
| ana@bibliotrack.test | Lector |
| sofia@bibliotrack.test | Bibliotecario |
| diego@bibliotrack.test | Administrador |

## Ejecutar las pruebas

```bash
py -m pytest -v
```

## Estructura

```
manage.py          punto de entrada de Django
config/            configuración de Django
biblioteca/        app de Django: modelos, vistas, plantillas, datos de prueba y sus pruebas
src/bibliotrack/   reglas del negocio (búsqueda y préstamos), sin Django
tests/             pruebas de las reglas del negocio
docs/              backlog, Scrum y sprints
.github/           plantillas de issues y PR, y el workflow de CI
```

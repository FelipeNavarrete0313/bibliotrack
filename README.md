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
| Historias de usuario | Issues con la etiqueta `tipo: historia de usuario` | 16 |
| Tareas técnicas y documentación | Issues con `tipo: tarea` o `tipo: documentación` | 8 |
| Bugs | Issues con `tipo: bug` | 3 |
| Épicas | Etiquetas `épica: …` | 5 |
| Sprints | Hitos (milestones) e iteraciones del Project | 3 |
| Estimación | Campos **Estimate** (puntos) y **Horas** del Project | 88 puntos · 352 horas |

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
| Detalle de un libro | `/libros/<id>/` | Todos | HU-07 |
| Iniciar sesión | `/iniciar-sesion/` | Visitantes | HU-02 |
| Crear una cuenta | `/registro/` | Visitantes | HU-01 |
| Mi inicio | `/inicio/` | Con sesión | HU-02 |
| Registrar un libro | `/libros/nuevo/` | Bibliotecario y administrador | HU-05 |
| Préstamos | `/prestamos/` | Bibliotecario y administrador | HU-09 |

Ninguna pantalla enlaza al panel Admin de Django: todo se hace desde las páginas de BiblioTrack.

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

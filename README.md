# BiblioTrack

[![CI](https://github.com/FelipeNavarrete0313/bibliotrack/actions/workflows/ci.yml/badge.svg)](https://github.com/FelipeNavarrete0313/bibliotrack/actions/workflows/ci.yml)

Sistema web de préstamos de biblioteca para un centro de formación.

> **Proyecto académico de ejemplo.** BiblioTrack es un proyecto inventado para demostrar cómo se administra y gestiona un proyecto de software con **GitHub Projects** y **Scrum**. El foco está en la gestión (backlog, issues, sprints, tablero y pull requests); el código es una aplicación Django pequeña y los issues cerrados del Sprint 1 simulan trabajo ya terminado.

## Tablero del proyecto

**[Abrir el GitHub Project](https://github.com/users/FelipeNavarrete0313/projects/2)**

| Vista | Para qué sirve |
| --- | --- |
| Backlog | Tabla con todo el Product Backlog agrupado por sprint, con prioridad y estimación |
| Board | Tablero Kanban: Todo → In progress → In review → Done |
| Current iteration | Solo el sprint en curso |
| Roadmap | Línea de tiempo con los tres sprints |

## Product Goal

Que la biblioteca gestione su catálogo, sus usuarios y sus préstamos en línea, para que un lector encuentre y pida un libro en minutos y el bibliotecario deje de llevar el control en planillas de papel.

## Cómo está organizado el trabajo

| Elemento | En GitHub | Cantidad |
| --- | --- | --- |
| Historias de usuario | Issues con la etiqueta `tipo: historia de usuario` | 16 |
| Tareas técnicas y documentación | Issues con `tipo: tarea` o `tipo: documentación` | 7 |
| Bugs | Issues con `tipo: bug` | 3 |
| Épicas | Etiquetas `épica: …` | 5 |
| Sprints | Hitos (milestones) e iteraciones del Project | 3 |

## Documentación

- [Product Backlog](docs/product-backlog.md)
- [Cómo trabajamos: Scrum en GitHub](docs/scrum.md)
- [Definición de terminado](docs/definicion-de-terminado.md)
- [Sprint 1: review y retrospectiva](docs/sprints/sprint-1.md)
- [Cómo contribuir](CONTRIBUTING.md)

## Ejecutar la aplicación (Django)

Necesitas [Python 3.10 o superior](https://www.python.org/downloads/) y [Git](https://git-scm.com/downloads).
En Windows, al instalar Python marca la casilla **«Add python.exe to PATH»**.

```bash
git clone https://github.com/FelipeNavarrete0313/bibliotrack.git
cd bibliotrack
py -m pip install -r requirements-dev.txt     # en Mac o Linux: python3 -m pip ...
py manage.py migrate                          # crea la base de datos (db.sqlite3)
py manage.py cargar_datos                     # 10 libros y 5 lectores de ejemplo
py manage.py runserver
```

Abre **http://127.0.0.1:8000** en el navegador. Para detener el servidor, presiona `Ctrl + C` en la terminal.

| Página | Dirección | Historia |
| --- | --- | --- |
| Catálogo con buscador | `/` | HU-06 |
| Detalle de un libro | `/libros/<id>/` | HU-07 |
| Registrar préstamo y préstamos activos | `/prestamos/` | HU-09 |
| Administración (libros, lectores, préstamos) | `/admin/` | HU-05 |

Los lectores de prueba tienen los documentos **1001** a **1005**.
Para entrar a `/admin/`, crea primero un usuario con `py manage.py createsuperuser`.

## Ejecutar las pruebas

```bash
py -m pytest -v
```

## Estructura

```
manage.py          punto de entrada de Django
config/            configuración de Django (settings, urls)
biblioteca/        app web: modelos, vistas, plantillas, admin y pruebas
src/bibliotrack/   reglas del negocio (búsqueda y préstamos), sin Django
tests/             pruebas de las reglas del negocio
docs/              backlog, Scrum y sprints
.github/           plantillas de issues y PR, y el workflow de CI
```

Las vistas de Django no repiten las reglas: llaman a `src/bibliotrack/catalogo.py` y `src/bibliotrack/prestamos.py`.

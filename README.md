# BiblioTrack

[![CI](https://github.com/FelipeNavarrete0313/bibliotrack/actions/workflows/ci.yml/badge.svg)](https://github.com/FelipeNavarrete0313/bibliotrack/actions/workflows/ci.yml)

Sistema web de préstamos de biblioteca para un centro de formación.

> **Proyecto académico de ejemplo.** BiblioTrack es un proyecto inventado para demostrar cómo se administra y gestiona un proyecto de software con **GitHub Projects** y **Scrum**. El foco está en la gestión (backlog, issues, sprints, tablero y pull requests); el código es un esqueleto mínimo y los issues cerrados del Sprint 1 simulan trabajo ya terminado.

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
| Tareas técnicas y documentación | Issues con `tipo: tarea` o `tipo: documentación` | 6 |
| Bugs | Issues con `tipo: bug` | 3 |
| Épicas | Etiquetas `épica: …` | 5 |
| Sprints | Hitos (milestones) e iteraciones del Project | 3 |

## Documentación

- [Product Backlog](docs/product-backlog.md)
- [Cómo trabajamos: Scrum en GitHub](docs/scrum.md)
- [Definición de terminado](docs/definicion-de-terminado.md)
- [Sprint 1: review y retrospectiva](docs/sprints/sprint-1.md)
- [Cómo contribuir](CONTRIBUTING.md)

## Ejecutar las pruebas

```bash
pip install -r requirements-dev.txt
pytest
```

## Estructura

```
src/bibliotrack/   código de la aplicación
tests/             pruebas automáticas
docs/              backlog, Scrum y sprints
.github/           plantillas de issues y PR, y el workflow de CI
```

# Cómo trabajamos: Scrum en GitHub

## Roles

| Rol | Responsabilidad en este proyecto |
| --- | --- |
| Product Owner | Ordena el Product Backlog, define prioridades y acepta las historias en la Sprint Review |
| Scrum Master | Facilita las ceremonias, mantiene el tablero al día y quita impedimentos |
| Developers | Estiman, toman issues, programan en ramas y revisan los pull requests de los compañeros |

## Artefactos y dónde viven en GitHub

| Artefacto Scrum | En GitHub |
| --- | --- |
| Product Backlog | Vista **Backlog** del [GitHub Project](https://github.com/users/FelipeNavarrete0313/projects/2) y [`product-backlog.md`](product-backlog.md) |
| Historia de usuario | Un **issue** con la etiqueta `tipo: historia de usuario` |
| Sprint Backlog | Los issues del **hito** del sprint y la vista **Current iteration** del Project |
| Incremento | Lo que está fusionado en la rama `main` |
| Definición de terminado | [`definicion-de-terminado.md`](definicion-de-terminado.md) y la lista al final de cada historia |

## Ceremonias

| Ceremonia | Cuándo | Qué se hace en GitHub |
| --- | --- | --- |
| Sprint Planning | Primer lunes del sprint | Se eligen issues del backlog, se les asigna el hito y la iteración del sprint, y quedan en **Todo** |
| Daily | Todos los días, 15 minutos | Se revisa la vista **Board**; cada persona mueve sus tarjetas |
| Sprint Review | Último viernes del sprint | Se muestran los issues en **Done** y el Product Owner los acepta |
| Retrospectiva | Después de la Review | Se registra en `docs/sprints/` qué salió bien, qué mejorar y las acciones |

## Flujo de un issue

1. **Todo**: el issue tiene criterios de aceptación, estimación y sprint, pero nadie lo ha empezado.
2. **In progress**: alguien lo tomó y creó una rama (`feature/HU-09-registrar-prestamo`).
3. **In review**: hay un pull request abierto que dice `Closes #11`. El Project cambia el estado solo.
4. **Done**: el pull request se fusionó. GitHub cierra el issue y el Project lo mueve a Done automáticamente.

La columna **In progress** tiene un límite de 5 tarjetas (límite WIP) para no empezar más trabajo del que se puede terminar.

## Estimación

Se usan puntos de historia con la escala 1, 2, 3, 5, 8. Una historia de más de 8 puntos se divide.

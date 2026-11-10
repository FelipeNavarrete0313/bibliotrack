# Product Backlog

## Product Goal

Que la biblioteca de un centro de formación gestione su catálogo, sus usuarios y sus préstamos en línea, para que un lector encuentre y pida un libro en minutos y el bibliotecario deje de llevar el control en planillas de papel.

## Épicas

| Épica | Nombre | Qué cubre |
| --- | --- | --- |
| E1 | Autenticación y usuarios | Registro, inicio de sesión, recuperación de contraseña y roles |
| E2 | Catálogo de libros | Registro, búsqueda, detalle y mantenimiento de libros |
| E3 | Préstamos y devoluciones | Préstamo, devolución, consulta y renovación |
| E4 | Reservas y notificaciones | Reservas de libros agotados y avisos por correo |
| E5 | Reportes y administración | Reportes, multas y documentación |

## Backlog ordenado

Cada fila es un issue del repositorio. El detalle (historia, criterios, escenarios, estimación, trazabilidad y definición de terminado) está dentro del issue.

| ID | Título | Tipo | Épica | Prioridad | Puntos | Horas | Sprint | Estado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T-01 | [Configurar el repositorio, las ramas y la estructura del proyecto](https://github.com/FelipeNavarrete0313/bibliotrack/issues/1) | Tarea técnica | E1 | Alta | 1 | 4 | Sprint 1 | Done |
| T-02 | [Diseñar el modelo de base de datos](https://github.com/FelipeNavarrete0313/bibliotrack/issues/2) | Tarea técnica | E2 | Alta | 3 | 12 | Sprint 1 | Done |
| T-03 | [Configurar integración continua con GitHub Actions](https://github.com/FelipeNavarrete0313/bibliotrack/issues/3) | Tarea técnica | E1 | Media | 2 | 8 | Sprint 1 | Done |
| T-04 | [Diseñar los prototipos de interfaz (wireframes)](https://github.com/FelipeNavarrete0313/bibliotrack/issues/4) | Tarea técnica | E2 | Media | 3 | 12 | Sprint 1 | Done |
| T-07 | [Construir la interfaz web base con Django](https://github.com/FelipeNavarrete0313/bibliotrack/issues/29) | Tarea técnica | E2 | Alta | 5 | 20 | Sprint 1 | Done |
| HU-01 | [Registro de lector](https://github.com/FelipeNavarrete0313/bibliotrack/issues/5) | Historia de usuario | E1 | Alta | 3 | 12 | Sprint 1 | Done |
| HU-02 | [Inicio de sesión](https://github.com/FelipeNavarrete0313/bibliotrack/issues/6) | Historia de usuario | E1 | Alta | 2 | 8 | Sprint 1 | Done |
| HU-05 | [Registrar un libro en el catálogo](https://github.com/FelipeNavarrete0313/bibliotrack/issues/7) | Historia de usuario | E2 | Alta | 3 | 12 | Sprint 1 | Done |
| HU-06 | [Buscar libros por título, autor o categoría](https://github.com/FelipeNavarrete0313/bibliotrack/issues/8) | Historia de usuario | E2 | Alta | 5 | 20 | Sprint 1 | Done |
| HU-07 | [Ver el detalle y la disponibilidad de un libro](https://github.com/FelipeNavarrete0313/bibliotrack/issues/9) | Historia de usuario | E2 | Alta | 2 | 8 | Sprint 1 | Done |
| BUG-02 | [El formulario de registro acepta correos sin formato válido](https://github.com/FelipeNavarrete0313/bibliotrack/issues/10) | Bug | E1 | Alta | 1 | 4 | Sprint 1 | Done |
| HU-09 | [Registrar un préstamo](https://github.com/FelipeNavarrete0313/bibliotrack/issues/11) | Historia de usuario | E3 | Alta | 5 | 20 | Sprint 2 | Done |
| HU-10 | [Registrar una devolución](https://github.com/FelipeNavarrete0313/bibliotrack/issues/12) | Historia de usuario | E3 | Alta | 3 | 12 | Sprint 2 | Done |
| HU-11 | [Consultar mis préstamos y fechas de devolución](https://github.com/FelipeNavarrete0313/bibliotrack/issues/13) | Historia de usuario | E3 | Alta | 3 | 12 | Sprint 2 | Done |
| HU-17 | [Solicitar un préstamo en línea](https://github.com/FelipeNavarrete0313/bibliotrack/issues/44) | Historia de usuario | E3 | Alta | 5 | 20 | Sprint 2 | Done |
| BUG-04 | [Al entregar una solicitud desde el panel Admin no se crea el préstamo ni se descuenta el ejemplar](https://github.com/FelipeNavarrete0313/bibliotrack/issues/47) | Bug | E3 | Alta | 2 | 8 | Sprint 2 | Done |
| BUG-05 | [Una solicitud o un préstamo se puede atender dos veces con un doble clic](https://github.com/FelipeNavarrete0313/bibliotrack/issues/50) | Bug | E3 | Alta | 3 | 12 | Sprint 2 | Done |
| HU-08 | [Editar o dar de baja un libro](https://github.com/FelipeNavarrete0313/bibliotrack/issues/14) | Historia de usuario | E2 | Media | 3 | 12 | Sprint 2 | In review |
| T-05 | [Desplegar la aplicación en un ambiente de pruebas](https://github.com/FelipeNavarrete0313/bibliotrack/issues/15) | Tarea técnica | E3 | Media | 3 | 12 | Sprint 2 | Todo |
| BUG-01 | [La búsqueda no encuentra libros cuando el título tiene tilde](https://github.com/FelipeNavarrete0313/bibliotrack/issues/16) | Bug | E2 | Alta | 2 | 8 | Sprint 2 | Done |
| T-08 | [Documentar la estimación y la trazabilidad del proyecto](https://github.com/FelipeNavarrete0313/bibliotrack/issues/40) | Documentación | E5 | Alta | 3 | 12 | Sprint 2 | Done |
| HU-03 | [Recuperar la contraseña](https://github.com/FelipeNavarrete0313/bibliotrack/issues/17) | Historia de usuario | E1 | Media | 3 | 12 | Sprint 3 | Todo |
| HU-04 | [Administrar los roles de los usuarios](https://github.com/FelipeNavarrete0313/bibliotrack/issues/18) | Historia de usuario | E1 | Media | 5 | 20 | Sprint 3 | Todo |
| HU-12 | [Renovar un préstamo](https://github.com/FelipeNavarrete0313/bibliotrack/issues/19) | Historia de usuario | E3 | Media | 3 | 12 | Sprint 3 | Todo |
| HU-13 | [Reservar un libro que no está disponible](https://github.com/FelipeNavarrete0313/bibliotrack/issues/20) | Historia de usuario | E4 | Media | 5 | 20 | Sprint 3 | Todo |
| HU-14 | [Recibir un aviso por correo antes del vencimiento](https://github.com/FelipeNavarrete0313/bibliotrack/issues/21) | Historia de usuario | E4 | Media | 5 | 20 | Sprint 3 | Todo |
| T-06 | [Escribir el manual de usuario y la documentación técnica](https://github.com/FelipeNavarrete0313/bibliotrack/issues/22) | Documentación | E5 | Media | 3 | 12 | Sprint 3 | Todo |
| BUG-03 | [El historial de préstamos muestra las fechas en formato mes/día/año](https://github.com/FelipeNavarrete0313/bibliotrack/issues/23) | Bug | E3 | Baja | 2 | 8 | Sprint 3 | Todo |
| BUG-06 | [Editar los ejemplares o borrar un préstamo en el panel Admin descuadra la disponibilidad](https://github.com/FelipeNavarrete0313/bibliotrack/issues/51) | Bug | E3 | Alta | 3 | 12 | Sprint 3 | Todo |
| BUG-07 | [Varias solicitudes pendientes compiten por el mismo ejemplar](https://github.com/FelipeNavarrete0313/bibliotrack/issues/52) | Bug | E3 | Media | 2 | 8 | Sprint 3 | Todo |
| HU-15 | [Reporte de los libros más prestados](https://github.com/FelipeNavarrete0313/bibliotrack/issues/24) | Historia de usuario | E5 | Baja | 5 | 20 | — | Todo |
| HU-16 | [Calcular la multa por devolución tardía](https://github.com/FelipeNavarrete0313/bibliotrack/issues/25) | Historia de usuario | E5 | Baja | 5 | 20 | — | Todo |
| T-09 | [Unificar las reglas de préstamo que el panel Admin repite](https://github.com/FelipeNavarrete0313/bibliotrack/issues/53) | Tarea técnica | E3 | Media | 2 | 8 | — | Todo |
| T-10 | [Agregar linter y medición de cobertura al CI](https://github.com/FelipeNavarrete0313/bibliotrack/issues/54) | Tarea técnica | E5 | Media | 2 | 8 | — | Todo |
| T-11 | [Mejorar la accesibilidad y los mensajes de las páginas](https://github.com/FelipeNavarrete0313/bibliotrack/issues/55) | Tarea técnica | E3 | Baja | 2 | 8 | — | Todo |
| T-12 | [Paginar el catálogo, los préstamos activos y el historial](https://github.com/FelipeNavarrete0313/bibliotrack/issues/56) | Tarea técnica | E2 | Baja | 2 | 8 | — | Todo |
| BUG-08 | [El registro acepta documentos con símbolos y contraseñas muy comunes](https://github.com/FelipeNavarrete0313/bibliotrack/issues/57) | Bug | E1 | Baja | 1 | 4 | — | Todo |

## Resumen por sprint

| Sprint | Fechas | Puntos | Horas | Objetivo |
| --- | --- | --- | --- | --- |
| Sprint 1 | 19 oct – 1 nov | 30 | 120 | Un lector puede registrarse, iniciar sesión y consultar el catálogo |
| Sprint 2 | 2 nov – 15 nov | 32 | 128 | El lector solicita libros en línea, el bibliotecario registra préstamos y devoluciones, y el lector consulta los suyos |
| Sprint 3 | 16 nov – 29 nov | 31 | 124 | Reservas, renovaciones, notificaciones y administración de roles, más dos bugs de la revisión de código (BUG-06 y BUG-07) |
| Sin asignar | — | 19 | 76 | Reportes y multas, y las mejoras técnicas de la revisión de código, si queda capacidad |

La estimación se explica en [`estimacion.md`](estimacion.md) y la relación entre issues, ramas y pull requests en [`trazabilidad.md`](trazabilidad.md).

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

Cada fila es un issue del repositorio. El detalle (historia, criterios de aceptación y definición de terminado) está dentro del issue.

| ID | Título | Tipo | Épica | Prioridad | Puntos | Sprint |
| --- | --- | --- | --- | --- | --- | --- |
| T-01 | [Configurar el repositorio, las ramas y la estructura del proyecto](https://github.com/FelipeNavarrete0313/bibliotrack/issues/1) | Tarea técnica | E1 | Alta | 1 | Sprint 1 |
| T-02 | [Diseñar el modelo de base de datos](https://github.com/FelipeNavarrete0313/bibliotrack/issues/2) | Tarea técnica | E2 | Alta | 3 | Sprint 1 |
| T-03 | [Configurar integración continua con GitHub Actions](https://github.com/FelipeNavarrete0313/bibliotrack/issues/3) | Tarea técnica | E1 | Media | 2 | Sprint 1 |
| T-04 | [Diseñar los prototipos de interfaz (wireframes)](https://github.com/FelipeNavarrete0313/bibliotrack/issues/4) | Tarea técnica | E2 | Media | 3 | Sprint 1 |
| HU-01 | [Registro de lector](https://github.com/FelipeNavarrete0313/bibliotrack/issues/5) | Historia de usuario | E1 | Alta | 3 | Sprint 1 |
| HU-02 | [Inicio de sesión](https://github.com/FelipeNavarrete0313/bibliotrack/issues/6) | Historia de usuario | E1 | Alta | 2 | Sprint 1 |
| HU-05 | [Registrar un libro en el catálogo](https://github.com/FelipeNavarrete0313/bibliotrack/issues/7) | Historia de usuario | E2 | Alta | 3 | Sprint 1 |
| HU-06 | [Buscar libros por título, autor o categoría](https://github.com/FelipeNavarrete0313/bibliotrack/issues/8) | Historia de usuario | E2 | Alta | 5 | Sprint 1 |
| HU-07 | [Ver el detalle y la disponibilidad de un libro](https://github.com/FelipeNavarrete0313/bibliotrack/issues/9) | Historia de usuario | E2 | Alta | 2 | Sprint 1 |
| BUG-02 | [El formulario de registro acepta correos sin formato válido](https://github.com/FelipeNavarrete0313/bibliotrack/issues/10) | Bug | E1 | Alta | 1 | Sprint 1 |
| HU-09 | [Registrar un préstamo](https://github.com/FelipeNavarrete0313/bibliotrack/issues/11) | Historia de usuario | E3 | Alta | 5 | Sprint 2 |
| HU-10 | [Registrar una devolución](https://github.com/FelipeNavarrete0313/bibliotrack/issues/12) | Historia de usuario | E3 | Alta | 3 | Sprint 2 |
| HU-11 | [Consultar mis préstamos y fechas de devolución](https://github.com/FelipeNavarrete0313/bibliotrack/issues/13) | Historia de usuario | E3 | Alta | 3 | Sprint 2 |
| HU-08 | [Editar o dar de baja un libro](https://github.com/FelipeNavarrete0313/bibliotrack/issues/14) | Historia de usuario | E2 | Media | 3 | Sprint 2 |
| T-05 | [Desplegar la aplicación en un ambiente de pruebas](https://github.com/FelipeNavarrete0313/bibliotrack/issues/15) | Tarea técnica | E3 | Media | 3 | Sprint 2 |
| T-07 | [Construir la interfaz web con Django](https://github.com/FelipeNavarrete0313/bibliotrack/issues/29) | Tarea técnica | E2 | Alta | 5 | Sprint 2 |
| BUG-01 | [La búsqueda no encuentra libros cuando el título tiene tilde](https://github.com/FelipeNavarrete0313/bibliotrack/issues/16) | Bug | E2 | Alta | 2 | Sprint 2 |
| HU-03 | [Recuperar la contraseña](https://github.com/FelipeNavarrete0313/bibliotrack/issues/17) | Historia de usuario | E1 | Media | 3 | Sprint 3 |
| HU-04 | [Administrar los roles de los usuarios](https://github.com/FelipeNavarrete0313/bibliotrack/issues/18) | Historia de usuario | E1 | Media | 5 | Sprint 3 |
| HU-12 | [Renovar un préstamo](https://github.com/FelipeNavarrete0313/bibliotrack/issues/19) | Historia de usuario | E3 | Media | 3 | Sprint 3 |
| HU-13 | [Reservar un libro que no está disponible](https://github.com/FelipeNavarrete0313/bibliotrack/issues/20) | Historia de usuario | E4 | Media | 5 | Sprint 3 |
| HU-14 | [Recibir un aviso por correo antes del vencimiento](https://github.com/FelipeNavarrete0313/bibliotrack/issues/21) | Historia de usuario | E4 | Media | 5 | Sprint 3 |
| T-06 | [Escribir el manual de usuario y la documentación técnica](https://github.com/FelipeNavarrete0313/bibliotrack/issues/22) | Documentación | E5 | Media | 3 | Sprint 3 |
| BUG-03 | [El historial de préstamos muestra las fechas en formato mes/día/año](https://github.com/FelipeNavarrete0313/bibliotrack/issues/23) | Bug | E3 | Baja | 2 | Sprint 3 |
| HU-15 | [Reporte de los libros más prestados](https://github.com/FelipeNavarrete0313/bibliotrack/issues/24) | Historia de usuario | E5 | Baja | 5 | — |
| HU-16 | [Calcular la multa por devolución tardía](https://github.com/FelipeNavarrete0313/bibliotrack/issues/25) | Historia de usuario | E5 | Baja | 5 | — |

## Resumen por sprint

| Sprint | Fechas | Puntos planeados | Objetivo |
| --- | --- | --- | --- |
| Sprint 1 | 19 oct – 1 nov | 25 | Un lector puede registrarse, iniciar sesión y consultar el catálogo |
| Sprint 2 | 2 nov – 15 nov | 24 | El bibliotecario registra préstamos y devoluciones, y el lector consulta los suyos |
| Sprint 3 | 16 nov – 29 nov | 26 | Reservas, renovaciones, notificaciones y administración de roles |
| Sin asignar | — | 10 | Reportes y multas, si queda capacidad |

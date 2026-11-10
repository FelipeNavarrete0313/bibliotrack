# Sprint 1 · 19 oct – 1 nov

**Objetivo del sprint:** un lector puede registrarse, iniciar sesión y consultar el catálogo.

## Sprint Review

| ID | Título | Puntos | Pull request | Resultado |
| --- | --- | --- | --- | --- |
| T-01 | Configurar el repositorio, las ramas y la estructura del proyecto | 1 | [#26](https://github.com/FelipeNavarrete0313/bibliotrack/pull/26) | Terminado |
| T-02 | Diseñar el modelo de base de datos | 3 | [#31](https://github.com/FelipeNavarrete0313/bibliotrack/pull/31) | Terminado |
| T-03 | Configurar integración continua con GitHub Actions | 2 | [#26](https://github.com/FelipeNavarrete0313/bibliotrack/pull/26) | Terminado |
| T-04 | Diseñar los prototipos de interfaz (wireframes) | 3 | [#32](https://github.com/FelipeNavarrete0313/bibliotrack/pull/32) | Terminado |
| T-07 | Construir la interfaz web base con Django | 5 | [#33](https://github.com/FelipeNavarrete0313/bibliotrack/pull/33) | Terminado |
| HU-01 | Registro de lector | 3 | [#35](https://github.com/FelipeNavarrete0313/bibliotrack/pull/35) | Terminado |
| HU-02 | Inicio de sesión | 2 | [#34](https://github.com/FelipeNavarrete0313/bibliotrack/pull/34) | Terminado |
| HU-05 | Registrar un libro en el catálogo | 3 | [#38](https://github.com/FelipeNavarrete0313/bibliotrack/pull/38) | Terminado |
| HU-06 | Buscar libros por título, autor o categoría | 5 | [#26](https://github.com/FelipeNavarrete0313/bibliotrack/pull/26) | Terminado |
| HU-07 | Ver el detalle y la disponibilidad de un libro | 2 | [#37](https://github.com/FelipeNavarrete0313/bibliotrack/pull/37) | Terminado |
| BUG-02 | El formulario de registro acepta correos sin formato válido | 1 | [#36](https://github.com/FelipeNavarrete0313/bibliotrack/pull/36) | Terminado |

- Puntos planeados: 30 (incluye T-07, que se agregó al ver que las pantallas lo necesitaban)
- Puntos terminados: 30
- Velocidad del equipo: 30 puntos (120 horas)

## Retrospectiva

**Qué salió bien**
- Las plantillas de issues hicieron que todas las historias quedaran con criterios de aceptación.
- Cada pull request pasó las pruebas automáticas antes de fusionarse.

**Qué mejorar**
- Algunos issues se cerraron sin un pull request que los respaldara, y se perdió la trazabilidad. Se reabrieron y se cerraron con su PR.
- La interfaz base (T-07) no estaba en el backlog y era requisito de varias historias.
- Apareció un bug (BUG-02) porque el correo solo se validaba en el navegador.

**Acciones para el Sprint 2**
- Ningún issue se cierra a mano: se cierra con el `Closes #n` de su pull request.
- Escribir escenarios Dado / Cuando / Entonces antes de programar, y una prueba por escenario.
- Revisar las dependencias técnicas en la Sprint Planning.

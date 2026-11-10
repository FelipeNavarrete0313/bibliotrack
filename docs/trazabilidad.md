# Trazabilidad

Issue: [#40](https://github.com/FelipeNavarrete0313/bibliotrack/issues/40) · T-08 Documentar la estimación y la trazabilidad del proyecto

Trazabilidad significa poder seguir cualquier cambio en las dos direcciones: **de la historia de usuario al código** que la cumple, y **del código a la historia** que lo pidió.

## La convención

Todo lleva el **identificador del backlog** (HU-01, T-02, BUG-02…) y el **número del issue** (#5):

| Pieza | Formato | Ejemplo |
| --- | --- | --- |
| Issue | `[ID] Título` | `[HU-01] Registro de lector` (#5) |
| Rama | `tipo/ID-descripcion-corta` | `feature/HU-01-registro-lector` |
| Commit | `tipo: descripción (ID)` y en el cuerpo `Refs #n` | `feat: registro de lector con documento y correo únicos (HU-01)` |
| Pull request | `tipo: descripción (ID)` y en la descripción `Closes #n` | `feat: registro de lector (HU-01)` · `Closes #5` |
| Prueba | Un archivo por historia y una prueba por escenario | `biblioteca/tests/test_hu01_registro.py::test_escenario_correo_repetido` |
| Merge | Commit de merge que nombra el PR y la rama | `Merge pull request #35 from …/feature/HU-01-registro-lector` |

Prefijos de rama: `feature/` para historias y tareas, `fix/` para bugs y `docs/` para documentación.

## Ejemplo de punta a punta: HU-01 · Registro de lector

1. **Historia.** El issue [#5](https://github.com/FelipeNavarrete0313/bibliotrack/issues/5) tiene la historia, los criterios de aceptación, 4 escenarios Dado / Cuando / Entonces y la estimación (3 puntos, 12 horas).
2. **Rama.** Se crea `feature/HU-01-registro-lector` desde `main`.
3. **Commit.** [`52c5722`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/52c5722) · `feat: registro de lector con documento y correo únicos (HU-01)`, con `Refs #5` en el cuerpo. GitHub muestra ese commit en el historial del issue.
4. **Pull request.** [#35](https://github.com/FelipeNavarrete0313/bibliotrack/pull/35) con `Closes #5`. La automatización del Project mueve la tarjeta a **In review**.
5. **Pruebas.** GitHub Actions ejecuta las pruebas ([ejecución](https://github.com/FelipeNavarrete0313/bibliotrack/actions/runs/42869510851)). Cada escenario del issue tiene su prueba con el mismo nombre (`test_escenario_…`).
6. **Merge.** [`b68d1b5`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/b68d1b5) · `Merge pull request #35 …`. GitHub cierra el issue #5 y el Project mueve la tarjeta a **Done**.
7. **Bug y regreso.** Después del merge apareció el [#10](https://github.com/FelipeNavarrete0313/bibliotrack/issues/10): el registro aceptaba `pipe@correo`. Se reprodujo, se comentó en el issue y se corrigió en `fix/BUG-02-validar-correo` → [#36](https://github.com/FelipeNavarrete0313/bibliotrack/pull/36). Primero va un commit con la prueba que reproduce el bug y después el arreglo.

**De vuelta, del código a la historia:** en `main`, `git log --grep "(HU-01)"` muestra los commits de la historia; el commit de merge dice qué PR los trajo, y el PR dice qué issue cerró.

## Cómo rastrear en GitHub

| Pregunta | Dónde se ve |
| --- | --- |
| ¿Qué código cumple esta historia? | En el issue, panel **Development** (PR enlazado) y el historial de commits que la mencionan |
| ¿Por qué existe este cambio? | En el PR, la línea `Closes #n`; en el commit, el `(ID)` del mensaje |
| ¿Qué pruebas la cubren? | En el issue, cada escenario nombra su prueba |
| ¿En qué estado está? | En el Project, columna **Status**; en el issue, abierto o cerrado |
| ¿Cuánto se estimó? | En el Project, campos **Estimate** y **Horas**; en el issue, sección «Estimación» |

## Matriz de trazabilidad

| ID | Issue | Estado | Rama | Pull request | Merge en `main` | Pruebas |
| --- | --- | --- | --- | --- | --- | --- |
| T-01 | [#1](https://github.com/FelipeNavarrete0313/bibliotrack/issues/1) | Done | [`feature/T-01-estructura-inicial`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/feature/T-01-estructura-inicial) | [#26](https://github.com/FelipeNavarrete0313/bibliotrack/pull/26) | [`de05e2b`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/de05e2b) | CI (`.github/workflows/ci.yml`) |
| T-02 | [#2](https://github.com/FelipeNavarrete0313/bibliotrack/issues/2) | Done | [`feature/T-02-modelo-datos`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/feature/T-02-modelo-datos) | [#31](https://github.com/FelipeNavarrete0313/bibliotrack/pull/31) | [`4f3fd48`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/4f3fd48) | `biblioteca/tests/test_t02_modelo_datos.py` |
| T-03 | [#3](https://github.com/FelipeNavarrete0313/bibliotrack/issues/3) | Done | [`feature/T-01-estructura-inicial`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/feature/T-01-estructura-inicial) | [#26](https://github.com/FelipeNavarrete0313/bibliotrack/pull/26) | [`de05e2b`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/de05e2b) | CI (`.github/workflows/ci.yml`) |
| T-04 | [#4](https://github.com/FelipeNavarrete0313/bibliotrack/issues/4) | Done | [`docs/T-04-wireframes`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/docs/T-04-wireframes) | [#32](https://github.com/FelipeNavarrete0313/bibliotrack/pull/32) | [`063c8e1`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/063c8e1) | No aplica |
| T-07 | [#29](https://github.com/FelipeNavarrete0313/bibliotrack/issues/29) | Done | [`feature/T-07-interfaz-base`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/feature/T-07-interfaz-base) | [#33](https://github.com/FelipeNavarrete0313/bibliotrack/pull/33) | [`f3d13be`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/f3d13be) | `biblioteca/tests/test_t07_interfaz_base.py` |
| HU-01 | [#5](https://github.com/FelipeNavarrete0313/bibliotrack/issues/5) | Done | [`feature/HU-01-registro-lector`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/feature/HU-01-registro-lector) | [#35](https://github.com/FelipeNavarrete0313/bibliotrack/pull/35) | [`b68d1b5`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/b68d1b5) | `biblioteca/tests/test_hu01_registro.py` |
| HU-02 | [#6](https://github.com/FelipeNavarrete0313/bibliotrack/issues/6) | Done | [`feature/HU-02-inicio-sesion`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/feature/HU-02-inicio-sesion) | [#34](https://github.com/FelipeNavarrete0313/bibliotrack/pull/34) | [`91c54de`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/91c54de) | `biblioteca/tests/test_hu02_inicio_sesion.py` |
| HU-05 | [#7](https://github.com/FelipeNavarrete0313/bibliotrack/issues/7) | Done | [`feature/HU-05-registrar-libro`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/feature/HU-05-registrar-libro) | [#38](https://github.com/FelipeNavarrete0313/bibliotrack/pull/38) | [`17b6115`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/17b6115) | `biblioteca/tests/test_hu05_registrar_libro.py` |
| HU-06 | [#8](https://github.com/FelipeNavarrete0313/bibliotrack/issues/8) | Done | [`feature/T-01-estructura-inicial`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/feature/T-01-estructura-inicial) | [#26](https://github.com/FelipeNavarrete0313/bibliotrack/pull/26) | [`de05e2b`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/de05e2b) | `tests/test_catalogo.py`, `biblioteca/tests/test_t07_interfaz_base.py` |
| HU-07 | [#9](https://github.com/FelipeNavarrete0313/bibliotrack/issues/9) | Done | [`feature/HU-07-detalle-libro`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/feature/HU-07-detalle-libro) | [#37](https://github.com/FelipeNavarrete0313/bibliotrack/pull/37) | [`bc329a3`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/bc329a3) | `biblioteca/tests/test_hu07_detalle_libro.py` |
| BUG-02 | [#10](https://github.com/FelipeNavarrete0313/bibliotrack/issues/10) | Done | [`fix/BUG-02-validar-correo`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/fix/BUG-02-validar-correo) | [#36](https://github.com/FelipeNavarrete0313/bibliotrack/pull/36) | [`359006d`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/359006d) | `biblioteca/tests/test_bug02_validar_correo.py` |
| HU-09 | [#11](https://github.com/FelipeNavarrete0313/bibliotrack/issues/11) | Done | [`feature/HU-09-registrar-prestamo`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/feature/HU-09-registrar-prestamo) | [#28](https://github.com/FelipeNavarrete0313/bibliotrack/pull/28) | [`270df42`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/270df42) | `biblioteca/tests/test_hu09_prestamos_web.py`, `tests/test_prestamos.py` |
| HU-10 | [#12](https://github.com/FelipeNavarrete0313/bibliotrack/issues/12) | In progress | [`feature/HU-10-registrar-devolucion`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/feature/HU-10-registrar-devolucion) | — | — | `tests/test_devoluciones.py` |
| HU-11 | [#13](https://github.com/FelipeNavarrete0313/bibliotrack/issues/13) | In progress | [`feature/HU-11-mis-prestamos`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/feature/HU-11-mis-prestamos) | — | — | `tests/test_alertas.py` |
| HU-08 | [#14](https://github.com/FelipeNavarrete0313/bibliotrack/issues/14) | In review | [`feature/HU-08-editar-libro`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/feature/HU-08-editar-libro) | [#39](https://github.com/FelipeNavarrete0313/bibliotrack/pull/39) | PR abierto | `biblioteca/tests/test_hu08_editar_libro.py` |
| T-05 | [#15](https://github.com/FelipeNavarrete0313/bibliotrack/issues/15) | Todo | — | — | — | Pendiente |
| BUG-01 | [#16](https://github.com/FelipeNavarrete0313/bibliotrack/issues/16) | Done | [`fix/BUG-01-busqueda-tildes`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/fix/BUG-01-busqueda-tildes) | [#27](https://github.com/FelipeNavarrete0313/bibliotrack/pull/27) | [`53dd440`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/53dd440) | `tests/test_catalogo.py` |
| T-08 | [#40](https://github.com/FelipeNavarrete0313/bibliotrack/issues/40) | Done | [`docs/T-08-estimacion-trazabilidad`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/docs/T-08-estimacion-trazabilidad) | [#41](https://github.com/FelipeNavarrete0313/bibliotrack/pull/41) | Pendiente | No aplica |
| HU-03 | [#17](https://github.com/FelipeNavarrete0313/bibliotrack/issues/17) | Todo | — | — | — | Pendiente |
| HU-04 | [#18](https://github.com/FelipeNavarrete0313/bibliotrack/issues/18) | Todo | — | — | — | Pendiente |
| HU-12 | [#19](https://github.com/FelipeNavarrete0313/bibliotrack/issues/19) | Todo | — | — | — | Pendiente |
| HU-13 | [#20](https://github.com/FelipeNavarrete0313/bibliotrack/issues/20) | Todo | — | — | — | Pendiente |
| HU-14 | [#21](https://github.com/FelipeNavarrete0313/bibliotrack/issues/21) | Todo | — | — | — | Pendiente |
| T-06 | [#22](https://github.com/FelipeNavarrete0313/bibliotrack/issues/22) | Todo | — | — | — | No aplica |
| BUG-03 | [#23](https://github.com/FelipeNavarrete0313/bibliotrack/issues/23) | Todo | — | — | — | Pendiente |
| HU-15 | [#24](https://github.com/FelipeNavarrete0313/bibliotrack/issues/24) | Todo | — | — | — | Pendiente |
| HU-16 | [#25](https://github.com/FelipeNavarrete0313/bibliotrack/issues/25) | Todo | — | — | — | Pendiente |

## Notas

- **PR #26** fue el primero del proyecto y cerró tres issues a la vez (T-01, T-03 y HU-06). Desde entonces, la regla es **un pull request por issue**.
- **PR #30** se cerró sin fusionar porque mezclaba varios issues. Su contenido se rehízo en un PR por issue (#31, #33, #37 y #28).
- Los issues del Sprint 1 que se habían cerrado sin código se **reabrieron** y se cerraron con su pull request. Cada uno tiene un comentario que lo explica.
- HU-10 y HU-11 están **In progress**: ya tienen su rama con un primer avance y todavía no tienen pull request.
- HU-08 está **In review**: su PR [#39](https://github.com/FelipeNavarrete0313/bibliotrack/pull/39) está abierto y se fusiona en la Sprint Review.

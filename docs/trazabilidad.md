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
| HU-10 | [#12](https://github.com/FelipeNavarrete0313/bibliotrack/issues/12) | Done | [`feature/HU-10-registrar-devolucion`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/feature/HU-10-registrar-devolucion) | [#42](https://github.com/FelipeNavarrete0313/bibliotrack/pull/42) | [`5cd25a7`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/5cd25a7) | `biblioteca/tests/test_hu10_devolucion_web.py` |
| HU-11 | [#13](https://github.com/FelipeNavarrete0313/bibliotrack/issues/13) | Done | [`feature/HU-11-mis-prestamos`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/feature/HU-11-mis-prestamos) | [#43](https://github.com/FelipeNavarrete0313/bibliotrack/pull/43) | [`57158f7`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/57158f7) | `biblioteca/tests/test_hu11_mis_prestamos.py` |
| HU-17 | [#44](https://github.com/FelipeNavarrete0313/bibliotrack/issues/44) | Done | [`feature/HU-17-solicitar-prestamo`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/feature/HU-17-solicitar-prestamo) | [#45](https://github.com/FelipeNavarrete0313/bibliotrack/pull/45) | [`9c9d800`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/9c9d800) | `biblioteca/tests/test_hu17_solicitar_prestamo.py` |
| BUG-04 | [#47](https://github.com/FelipeNavarrete0313/bibliotrack/issues/47) | Done | [`fix/BUG-04-admin-reglas-prestamo`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/fix/BUG-04-admin-reglas-prestamo) | [#48](https://github.com/FelipeNavarrete0313/bibliotrack/pull/48) | [`d9644de`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/d9644de) | `biblioteca/tests/test_bug04_admin_reglas_prestamo.py` |
| BUG-05 | [#50](https://github.com/FelipeNavarrete0313/bibliotrack/issues/50) | Done | [`fix/BUG-05-estado-desactualizado`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/fix/BUG-05-estado-desactualizado) | [#58](https://github.com/FelipeNavarrete0313/bibliotrack/pull/58) | [`ab2b764`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/ab2b764) | `biblioteca/tests/test_bug05_estado_desactualizado.py` |
| HU-08 | [#14](https://github.com/FelipeNavarrete0313/bibliotrack/issues/14) | In review | [`feature/HU-08-editar-libro`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/feature/HU-08-editar-libro) | [#39](https://github.com/FelipeNavarrete0313/bibliotrack/pull/39) | PR abierto | `biblioteca/tests/test_hu08_editar_libro.py` |
| T-05 | [#15](https://github.com/FelipeNavarrete0313/bibliotrack/issues/15) | Todo | — | — | — | Pendiente |
| BUG-01 | [#16](https://github.com/FelipeNavarrete0313/bibliotrack/issues/16) | Done | [`fix/BUG-01-busqueda-tildes`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/fix/BUG-01-busqueda-tildes) | [#27](https://github.com/FelipeNavarrete0313/bibliotrack/pull/27) | [`53dd440`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/53dd440) | `tests/test_catalogo.py` |
| T-08 | [#40](https://github.com/FelipeNavarrete0313/bibliotrack/issues/40) | Done | [`docs/T-08-estimacion-trazabilidad`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/docs/T-08-estimacion-trazabilidad) | [#41](https://github.com/FelipeNavarrete0313/bibliotrack/pull/41) | [`92d8820`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/92d8820) | No aplica |
| HU-03 | [#17](https://github.com/FelipeNavarrete0313/bibliotrack/issues/17) | Todo | — | — | — | Pendiente |
| HU-04 | [#18](https://github.com/FelipeNavarrete0313/bibliotrack/issues/18) | Todo | — | — | — | Pendiente |
| HU-12 | [#19](https://github.com/FelipeNavarrete0313/bibliotrack/issues/19) | Done | [`feature/HU-12-renovar-prestamo`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/feature/HU-12-renovar-prestamo) | [#63](https://github.com/FelipeNavarrete0313/bibliotrack/pull/63) | [`954cd35`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/954cd35) | `biblioteca/tests/test_hu12_renovar_prestamo.py`, `tests/test_renovaciones.py` |
| HU-13 | [#20](https://github.com/FelipeNavarrete0313/bibliotrack/issues/20) | Done | [`feature/HU-13-reservar-libro`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/feature/HU-13-reservar-libro) | [#65](https://github.com/FelipeNavarrete0313/bibliotrack/pull/65) | [`4e9f7c2`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/4e9f7c2) | `biblioteca/tests/test_hu13_reservar_libro.py`, `tests/test_reservas.py` |
| HU-14 | [#21](https://github.com/FelipeNavarrete0313/bibliotrack/issues/21) | Todo | — | — | — | Pendiente |
| T-06 | [#22](https://github.com/FelipeNavarrete0313/bibliotrack/issues/22) | Todo | — | — | — | No aplica |
| BUG-03 | [#23](https://github.com/FelipeNavarrete0313/bibliotrack/issues/23) | Todo | — | — | — | Pendiente |
| BUG-06 | [#51](https://github.com/FelipeNavarrete0313/bibliotrack/issues/51) | Done | [`fix/BUG-06-admin-ejemplares`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/fix/BUG-06-admin-ejemplares) | [#60](https://github.com/FelipeNavarrete0313/bibliotrack/pull/60) | [`88ff139`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/88ff139) | `biblioteca/tests/test_bug06_admin_ejemplares.py` |
| BUG-07 | [#52](https://github.com/FelipeNavarrete0313/bibliotrack/issues/52) | Done | [`fix/BUG-07-solicitudes-compiten`](https://github.com/FelipeNavarrete0313/bibliotrack/tree/fix/BUG-07-solicitudes-compiten) | [#61](https://github.com/FelipeNavarrete0313/bibliotrack/pull/61) | [`a0ebd6b`](https://github.com/FelipeNavarrete0313/bibliotrack/commit/a0ebd6b) | `biblioteca/tests/test_bug07_solicitudes_compiten.py`, `tests/test_solicitudes.py` |
| HU-15 | [#24](https://github.com/FelipeNavarrete0313/bibliotrack/issues/24) | Todo | — | — | — | Pendiente |
| HU-16 | [#25](https://github.com/FelipeNavarrete0313/bibliotrack/issues/25) | Todo | — | — | — | Pendiente |
| T-09 | [#53](https://github.com/FelipeNavarrete0313/bibliotrack/issues/53) | Todo | — | — | — | Pendiente |
| T-10 | [#54](https://github.com/FelipeNavarrete0313/bibliotrack/issues/54) | Todo | — | — | — | Pendiente |
| T-11 | [#55](https://github.com/FelipeNavarrete0313/bibliotrack/issues/55) | Todo | — | — | — | Pendiente |
| T-12 | [#56](https://github.com/FelipeNavarrete0313/bibliotrack/issues/56) | Todo | — | — | — | Pendiente |
| BUG-08 | [#57](https://github.com/FelipeNavarrete0313/bibliotrack/issues/57) | Todo | — | — | — | Pendiente |

## Notas

- **PR #26** fue el primero del proyecto y cerró tres issues a la vez (T-01, T-03 y HU-06). Desde entonces, la regla es **un pull request por issue**.
- **PR #30** se cerró sin fusionar porque mezclaba varios issues. Su contenido se rehízo en un PR por issue (#31, #33, #37 y #28).
- Los issues del Sprint 1 que se habían cerrado sin código se **reabrieron** y se cerraron con su pull request. Cada uno tiene un comentario que lo explica.
- HU-10 y HU-11 empezaron en su rama con las reglas (sin Django) y se terminaron con las páginas en [#42](https://github.com/FelipeNavarrete0313/bibliotrack/pull/42) y [#43](https://github.com/FelipeNavarrete0313/bibliotrack/pull/43).
- **HU-17 se agregó durante el Sprint 2.** Al probar la aplicación se vio que un lector no tenía cómo pedir un libro: solo el bibliotecario podía registrar préstamos. El Product Owner la priorizó como Alta, se estimó en 5 puntos y entró al sprint en curso ([#44](https://github.com/FelipeNavarrete0313/bibliotrack/issues/44) → [#45](https://github.com/FelipeNavarrete0313/bibliotrack/pull/45)). Esta actualización de la documentación va aparte, en `docs/HU-17-trazabilidad`, con `Refs #44`.
- **BUG-04** salió al probar HU-17: entregar una solicitud desde el panel Admin de Django cambiaba el estado sin crear el préstamo ni descontar el ejemplar. Se reprodujo con 12 pruebas que fallaban, se movieron las reglas a `biblioteca/servicios.py` (las usan las páginas y el Admin) y la migración `0003` reparó los datos que habían quedado mal ([#47](https://github.com/FelipeNavarrete0313/bibliotrack/issues/47) → [#48](https://github.com/FelipeNavarrete0313/bibliotrack/pull/48)).
- **BUG-05** salió de una revisión de código: con un doble clic en «Entregar» se creaban dos préstamos para una sola solicitud, porque el servicio revisaba un estado leído antes de la transacción (y SQLite ignora `select_for_update`). Primero se subió el commit con las 6 pruebas que fallaban y después el arreglo: el estado se cambia con un `UPDATE` que incluye el estado esperado ([#50](https://github.com/FelipeNavarrete0313/bibliotrack/issues/50) → [#58](https://github.com/FelipeNavarrete0313/bibliotrack/pull/58)). Esta documentación va aparte, en `docs/BUG-05-trazabilidad`, con `Refs #50`.
- La misma revisión creó **BUG-06, BUG-07, T-09, T-10, T-11, T-12 y BUG-08** ([#51](https://github.com/FelipeNavarrete0313/bibliotrack/issues/51) a [#57](https://github.com/FelipeNavarrete0313/bibliotrack/issues/57)). También agregó a HU-08 un criterio (al dar de baja un libro, sus solicitudes pendientes se rechazan; commit en la rama del PR #39) y a T-05 dos puntos de configuración para el despliegue.
- **BUG-06 y BUG-07** se arreglaron al empezar el Sprint 3, cada uno con su commit de pruebas que fallan antes del arreglo. BUG-06: el Admin recalcula los disponibles al cambiar el número de ejemplares y, al borrar un préstamo activo, su solicitud vuelve a «Pendiente» ([#51](https://github.com/FelipeNavarrete0313/bibliotrack/issues/51) → [#60](https://github.com/FelipeNavarrete0313/bibliotrack/pull/60)). BUG-07: no se acepta una solicitud si las pendientes ya cubren los ejemplares disponibles, y el detalle muestra cuántas hay en espera ([#52](https://github.com/FelipeNavarrete0313/bibliotrack/issues/52) → [#61](https://github.com/FelipeNavarrete0313/bibliotrack/pull/61)). Esta documentación va en `docs/BUG-07-trazabilidad`, con `Refs #51` y `Refs #52`.
- **HU-12** se hizo antes que HU-13 aunque una de sus reglas depende de las reservas: el modelo `Reserva` existe desde T-02, así que la regla «no renovar si otro lector reservó el libro» ya se cumple y se prueba; la página para reservar llega con HU-13 ([#19](https://github.com/FelipeNavarrete0313/bibliotrack/issues/19) → [#63](https://github.com/FelipeNavarrete0313/bibliotrack/pull/63)).
- **HU-13** agregó la migración `0004` (un campo opcional en `Reserva`). El criterio «solo se puede reservar si no hay ejemplares disponibles» se tomó como «libres para ese lector»: un ejemplar ya solicitado por otro lector (BUG-07) o guardado para otra reserva no cuenta como disponible. La decisión quedó escrita en el PR para el Product Owner ([#20](https://github.com/FelipeNavarrete0313/bibliotrack/issues/20) → [#65](https://github.com/FelipeNavarrete0313/bibliotrack/pull/65)).
- HU-08 está **In review**: su PR [#39](https://github.com/FelipeNavarrete0313/bibliotrack/pull/39) está abierto y se fusiona en la Sprint Review.

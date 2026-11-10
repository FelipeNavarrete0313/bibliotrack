# Estimación del Product Backlog

Issue: [#40](https://github.com/FelipeNavarrete0313/bibliotrack/issues/40) · T-08 Documentar la estimación y la trazabilidad del proyecto

## Método: Planning Poker con puntos de historia

1. El Product Owner lee la historia y sus criterios de aceptación.
2. Cada integrante elige una carta en secreto con la escala **1, 2, 3, 5, 8**. Una historia de más de 8 puntos se divide.
3. Todos muestran su carta al mismo tiempo.
4. Si los votos coinciden, ese es el valor. Si no, explican su voto **el más alto y el más bajo**, el Product Owner resuelve las dudas y se vota otra vez.
5. El valor acordado se escribe en el campo **Estimate** del GitHub Project y en la sección «Estimación» del issue.

Un punto no es una hora: mide **tamaño relativo**, es decir, esfuerzo, complejidad e incertidumbre juntos. Para comparar se usan historias de referencia ya conocidas.

## Historias de referencia

| Puntos | Historia | Por qué sirve de referencia |
| --- | --- | --- |
| 2 | HU-07 · Ver el detalle de un libro | Solo muestra datos que ya existen |
| 3 | HU-05 · Registrar un libro | Un formulario con validaciones y un permiso por rol |
| 5 | HU-09 · Registrar un préstamo | Varias reglas de negocio con fechas y límites |

## De puntos a horas

Las horas se usan **solo como referencia de capacidad**, no para controlar a nadie.

- Capacidad del equipo: 4 integrantes × 15 horas por semana × 2 semanas = **120 horas por sprint**.
- Velocidad del Sprint 1: **30 puntos** terminados.
- Entonces, **1 punto ≈ 4 horas** (120 ÷ 30).

| Puntos | 1 | 2 | 3 | 5 | 8 |
| --- | --- | --- | --- | --- | --- |
| Horas aproximadas | 4 | 8 | 12 | 20 | 32 |

En el GitHub Project, cada ítem tiene los campos **Estimate** (puntos) y **Horas**.

## Ejemplos de Planning Poker

Los votos son de un equipo de ejemplo de cuatro desarrolladores (Dev A a Dev D).

### HU-07 · Ver el detalle y la disponibilidad de un libro

| Ronda | Dev A | Dev B | Dev C | Dev D | Qué pasó |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 3 | 2 | Casi todos votan 2: solo se leen datos que ya existen. Quien votó 3 pregunta por la «próxima devolución»; el Product Owner aclara que es la fecha más cercana de los préstamos activos. Se acepta 2. |

**Estimación acordada: 2 puntos (8 horas).**

### HU-06 · Buscar libros por título, autor o categoría

| Ronda | Dev A | Dev B | Dev C | Dev D | Qué pasó |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 5 | 8 | 5 | Votos muy separados (3 y 8). Quien votó 8 explica que la búsqueda debe ignorar tildes y responder en menos de 2 segundos con 1.000 libros. Quien votó 3 pensaba solo en un filtro simple. El Product Owner confirma los dos requisitos. |
| 2 | 5 | 5 | 5 | 5 | Con la duda resuelta, todos votan 5. |

**Estimación acordada: 5 puntos (20 horas).**

### HU-09 · Registrar un préstamo

| Ronda | Dev A | Dev B | Dev C | Dev D | Qué pasó |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 5 | 5 | 8 | Quien votó 8 cuenta cinco reglas: 15 días, domingo → lunes, máximo 3 préstamos, sin ejemplares y descontar el disponible. Quien votó 3 no había visto la regla del domingo. |
| 2 | 5 | 5 | 5 | 5 | Se acuerda separar las reglas (sin Django) de la página, y todos votan 5. |

**Estimación acordada: 5 puntos (20 horas).**

## Estimación de todo el backlog

| ID | Título | Sprint | Puntos | Horas | Justificación |
| --- | --- | --- | --- | --- | --- |
| T-01 | Configurar el repositorio, las ramas y la estructura del proyecto | S1 | 1 | 4 | Tarea de configuración conocida: carpetas, plantillas y reglas. Sin incertidumbre. |
| T-02 | Diseñar el modelo de base de datos | S1 | 3 | 12 | Cuatro tablas con relaciones simples, más el diagrama, el SQL y los datos de prueba. |
| T-03 | Configurar integración continua con GitHub Actions | S1 | 2 | 8 | Un workflow estándar de GitHub Actions; el equipo ya lo había hecho antes. |
| T-04 | Diseñar los prototipos de interfaz (wireframes) | S1 | 3 | 12 | Siete pantallas en baja fidelidad y una revisión; poco riesgo pero varias piezas. |
| T-07 | Construir la interfaz web base con Django | S1 | 5 | 20 | Base de Django, plantillas, estilos y catálogo web: mucho código nuevo para el equipo. |
| HU-01 | Registro de lector | S1 | 3 | 12 | Formulario con tres validaciones y creación de usuario y perfil. Similar a HU-05. |
| HU-02 | Inicio de sesión | S1 | 2 | 8 | Django resuelve la sesión; lo nuevo es el bloqueo por intentos y el inicio según el rol. |
| HU-05 | Registrar un libro en el catálogo | S1 | 3 | 12 | Un formulario de modelo con validaciones y permiso por rol. Historia de referencia de 3. |
| HU-06 | Buscar libros por título, autor o categoría | S1 | 5 | 20 | Búsqueda parcial, filtro y requisito de rendimiento; dudas sobre tildes y mayúsculas. |
| HU-07 | Ver el detalle y la disponibilidad de un libro | S1 | 2 | 8 | Solo lectura de datos que ya existen. Historia de referencia de 2. |
| BUG-02 | El formulario de registro acepta correos sin formato válido | S1 | 1 | 4 | Causa conocida (validación en el servidor) y una prueba de regresión. |
| HU-09 | Registrar un préstamo | S2 | 5 | 20 | Cinco reglas de negocio con fechas y límites, más la página. Historia de referencia de 5. |
| HU-10 | Registrar una devolución | S2 | 3 | 12 | Inverso del préstamo con cálculo de retraso; reutiliza lo aprendido en HU-09. |
| HU-11 | Consultar mis préstamos y fechas de devolución | S2 | 3 | 12 | Consulta con dos reglas de color y un historial. Sin escritura de datos. |
| HU-17 | Solicitar un préstamo en línea | S2 | 5 | 20 | Nuevo modelo con migración, dos actores (lector y bibliotecario) y reutiliza las reglas de HU-09. Tamaño parecido a HU-09. |
| HU-08 | Editar o dar de baja un libro | S2 | 3 | 12 | Edición con una regla (ISBN fijo) y baja lógica con confirmación y una restricción. |
| T-05 | Desplegar la aplicación en un ambiente de pruebas | S2 | 3 | 12 | Servicio de hosting nuevo para el equipo: incertidumbre en la configuración. |
| BUG-01 | La búsqueda no encuentra libros cuando el título tiene tilde | S2 | 2 | 8 | Causa clara (comparación sin normalizar) y arreglo localizado en una función. |
| T-08 | Documentar la estimación y la trazabilidad del proyecto | S2 | 3 | 12 | Dos documentos y la actualización de 27 issues; trabajo conocido pero extenso. |
| HU-03 | Recuperar la contraseña | S3 | 3 | 12 | Envío de correo y enlace con vencimiento: integración nueva, pero Django la facilita. |
| HU-04 | Administrar los roles de los usuarios | S3 | 5 | 20 | Pantalla de gestión con búsqueda y la regla del último administrador. |
| HU-12 | Renovar un préstamo | S3 | 3 | 12 | Tres reglas sobre un préstamo existente; depende de reservas (HU-13). |
| HU-13 | Reservar un libro que no está disponible | S3 | 5 | 20 | Cola por orden de llegada y reserva que vence a las 48 horas: lógica con tiempo. |
| HU-14 | Recibir un aviso por correo antes del vencimiento | S3 | 5 | 20 | Tarea programada y envío de correos: infraestructura nueva para el equipo. |
| T-06 | Escribir el manual de usuario y la documentación técnica | S3 | 3 | 12 | Documentación con capturas; trabajo conocido. |
| BUG-03 | El historial de préstamos muestra las fechas en formato mes/día/año | S3 | 2 | 8 | Cambio de formato de fecha en una plantilla, más su prueba. |
| HU-15 | Reporte de los libros más prestados | — | 5 | 20 | Consulta agregada con filtros y exportación a PDF y Excel: dos librerías nuevas. |
| HU-16 | Calcular la multa por devolución tardía | — | 5 | 20 | Cálculo con días hábiles y un bloqueo sobre los préstamos; reglas que tocan HU-09. |

| Sprint | Puntos | Horas |
| --- | --- | --- |
| Sprint 1 | 30 | 120 |
| Sprint 2 | 27 | 108 |
| Sprint 3 | 26 | 104 |
| Sin sprint | 10 | 40 |
| **Total** | **93** | **372** |

# Cómo contribuir

Cada cambio sigue el mismo camino, y así cualquiera puede ir de una historia de usuario al código que la cumple y volver. El detalle y la matriz completa están en [`docs/trazabilidad.md`](docs/trazabilidad.md).

```
Issue [HU-01] (#5) → rama feature/HU-01-… → commits «… (HU-01)» → PR «Closes #5» → CI → merge → Done
```

## 1. Toma un issue

- Elige un issue en **Todo** del sprint actual en el tablero del Project.
- Revisa que tenga criterios de aceptación, escenarios y estimación (puntos y horas). Si no los tiene, todavía no está listo.
- Asígnatelo y muévelo a **In progress**.

## 2. Crea una rama con el identificador del issue

```bash
git checkout main
git pull
git checkout -b feature/HU-01-registro-lector
```

| Tipo de issue | Prefijo de rama | Ejemplo |
| --- | --- | --- |
| Historia de usuario o tarea | `feature/` | `feature/HU-01-registro-lector` |
| Bug | `fix/` | `fix/BUG-02-validar-correo` |
| Documentación | `docs/` | `docs/T-04-wireframes` |

## 3. Escribe primero las pruebas de los escenarios

Cada escenario Dado / Cuando / Entonces del issue se vuelve una prueba con el mismo nombre:

```python
# biblioteca/tests/test_hu01_registro.py
def test_escenario_correo_repetido(client, lector):
    ...
```

En un bug, el primer commit es la prueba que reproduce el error, y el segundo es el arreglo.

## 4. Haz commits pequeños con el identificador

Formato: `tipo: descripción corta (ID)`, con `Refs #n` en el cuerpo.

```
feat: registro de lector con documento y correo únicos (HU-01)

Refs #5
```

Tipos: `feat` (funcionalidad), `fix` (arreglo), `test` (pruebas), `docs` (documentación), `ci` (integración continua).

## 5. Abre un pull request

- Título igual al del commit principal: `feat: registro de lector (HU-01)`.
- En la descripción, usa la plantilla y escribe **`Closes #5`**. Esto enlaza el PR con el issue y hace que el Project mueva la tarjeta a **In review**.
- Llena la tabla de trazabilidad: issue, rama y archivo de pruebas, y qué prueba cubre cada criterio de aceptación.
- El CI debe pasar.

## 6. Fusiona

- Usa **Merge pull request**: el commit de merge guarda el número del PR y el nombre de la rama.
- Al fusionar, GitHub cierra el issue y el Project lo pasa a **Done**.
- **Ningún issue se cierra a mano**: siempre se cierra con su pull request.

## Pruebas

```bash
py -m pip install -r requirements-dev.txt
py -m pytest -v
```

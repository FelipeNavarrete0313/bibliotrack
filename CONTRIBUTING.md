# Cómo contribuir

## 1. Toma un issue

- Elige un issue en **Ready** del sprint actual en el tablero del Project.
- Asígnatelo y muévelo a **In progress**.

## 2. Crea una rama

Desde `main`, con el tipo y el identificador del issue:

```bash
git checkout main
git pull
git checkout -b feature/HU-09-registrar-prestamo
```

| Tipo de issue | Prefijo de rama |
| --- | --- |
| Historia de usuario o tarea | `feature/` |
| Bug | `fix/` |
| Documentación | `docs/` |

## 3. Haz commits pequeños y claros

Formato: `tipo: descripción corta (ID)`

```
feat: calcular fecha de devolución del préstamo (HU-09)
fix: ignorar tildes en la búsqueda (BUG-01)
docs: actualizar el backlog
```

## 4. Abre un pull request

- Usa la plantilla y escribe `Closes #<número del issue>` para enlazarlo.
- Mueve el issue a **In review**.
- El CI debe pasar y un compañero debe aprobar.

## 5. Fusiona

Al fusionar, GitHub cierra el issue y el Project lo pasa a **Done**.

## Pruebas

```bash
pip install -r requirements-dev.txt
pytest
```

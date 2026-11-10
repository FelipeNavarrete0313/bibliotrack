# Definición de terminado (DoD)

Una historia de usuario está terminada cuando:

- El código está en una rama propia y entró a `main` por pull request
- El pull request enlaza su issue con `Closes #n` y explica cómo se probó
- Las pruebas automáticas (CI) pasan
- Se cumplen todos los criterios de aceptación
- La documentación está actualizada si aplica

En un equipo real, además, **un compañero aprueba el pull request** antes de fusionarlo. En este proyecto de ejemplo todo el trabajo se hizo desde una sola cuenta de GitHub, y GitHub no deja que el autor apruebe su propio PR; por eso esa aprobación no aparece en los PR.

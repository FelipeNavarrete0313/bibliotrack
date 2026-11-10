# Modelo de datos (T-02)

Issue: [#2 · T-02 Diseñar el modelo de base de datos](https://github.com/FelipeNavarrete0313/bibliotrack/issues/2)

## Diagrama entidad-relación

```mermaid
erDiagram
    USUARIO ||--|| PERFIL : "tiene"
    PERFIL ||--o{ PRESTAMO : "pide"
    PERFIL ||--o{ RESERVA : "hace"
    LIBRO ||--o{ PRESTAMO : "se presta en"
    LIBRO ||--o{ RESERVA : "se reserva en"
    PERFIL ||--o{ SOLICITUD : "solicita"
    LIBRO ||--o{ SOLICITUD : "se solicita en"
    SOLICITUD |o--o| PRESTAMO : "al entregarse crea"

    USUARIO {
        int id PK
        string username "igual al correo"
        string email
        string first_name
        string last_name
        string password "cifrada por Django"
    }
    PERFIL {
        int id PK
        int usuario_id FK
        string documento UK
        string rol "lector, bibliotecario o administrador"
    }
    LIBRO {
        int id PK
        string titulo
        string autor
        string isbn UK
        string categoria
        text descripcion
        int total_ejemplares
        int disponibles "nunca mayor que total_ejemplares"
        bool activo "false = dado de baja"
    }
    PRESTAMO {
        int id PK
        int lector_id FK
        int libro_id FK
        date fecha_prestamo
        date fecha_devolucion
        date fecha_entrega "null mientras esté activo"
        bool renovado
        string estado "activo o devuelto"
    }
    RESERVA {
        int id PK
        int lector_id FK
        int libro_id FK
        datetime creada
        string estado "activa, atendida o cancelada"
    }
    SOLICITUD {
        int id PK
        int lector_id FK
        int libro_id FK
        datetime creada
        string estado "pendiente, entregada, rechazada o cancelada"
        datetime atendida "null mientras esté pendiente"
        int prestamo_id FK "el préstamo creado al entregarla"
    }
```

## Decisiones de diseño

| Decisión | Por qué |
| --- | --- |
| Se usa el usuario de Django y un `Perfil` aparte | Django ya resuelve contraseñas cifradas y sesiones; el perfil guarda lo propio de BiblioTrack (documento y rol). |
| El correo es el nombre de usuario | La historia HU-02 pide iniciar sesión con correo y contraseña. |
| Los ejemplares son una cantidad en `Libro` (`total_ejemplares` y `disponibles`) | Ninguna historia necesita distinguir un ejemplar físico de otro. Si eso cambia, se crea una tabla `Ejemplar`. |
| `disponibles <= total_ejemplares` es una restricción de la base de datos | El error se detecta aunque alguien se salte la aplicación. |
| Un libro dado de baja no se borra (`activo = false`) | HU-08 pide conservar su historial de préstamos. |
| El préstamo guarda `fecha_devolucion` y `fecha_entrega` por separado | HU-10 necesita calcular los días de retraso. |
| La `Solicitud` (HU-17) es una tabla aparte y no descuenta ejemplares | El lector pide el libro en línea, pero el ejemplar solo sale al entregarlo; ahí se crea el `Prestamo` con las reglas de HU-09. Se agregó en la migración `0002_solicitud`. |

## Script SQL

Django crea las tablas con migraciones (`biblioteca/migrations/`). El SQL equivalente está en [`sql/esquema.sql`](sql/esquema.sql) y se generó con:

```bash
py manage.py sqlmigrate biblioteca 0001
py manage.py sqlmigrate biblioteca 0002
```

## Datos de prueba

`py manage.py cargar_datos` crea 20 libros en 7 categorías y 5 usuarios. Todos usan la contraseña `Biblio2026`.

| Correo | Documento | Rol |
| --- | --- | --- |
| ana@bibliotrack.test | 1001 | Lector |
| carlos@bibliotrack.test | 1002 | Lector |
| laura@bibliotrack.test | 1003 | Lector |
| sofia@bibliotrack.test | 2001 | Bibliotecario |
| diego@bibliotrack.test | 3001 | Administrador |

Son datos inventados para el ambiente de desarrollo.

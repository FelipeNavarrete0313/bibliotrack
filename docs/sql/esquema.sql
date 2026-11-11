BEGIN;
--
-- Create model Libro
--
CREATE TABLE "biblioteca_libro" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "titulo" varchar(200) NOT NULL, "autor" varchar(150) NOT NULL, "isbn" varchar(20) NOT NULL UNIQUE, "categoria" varchar(80) NOT NULL, "descripcion" text NOT NULL, "total_ejemplares" integer unsigned NOT NULL CHECK ("total_ejemplares" >= 0), "disponibles" integer unsigned NOT NULL CHECK ("disponibles" >= 0), "activo" bool NOT NULL, CONSTRAINT "disponibles_no_supera_total" CHECK ("disponibles" <= ("total_ejemplares")));
--
-- Create model Perfil
--
CREATE TABLE "biblioteca_perfil" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "documento" varchar(20) NOT NULL UNIQUE, "rol" varchar(15) NOT NULL, "usuario_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Prestamo
--
CREATE TABLE "biblioteca_prestamo" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "fecha_prestamo" date NOT NULL, "fecha_devolucion" date NOT NULL, "fecha_entrega" date NULL, "renovado" bool NOT NULL, "estado" varchar(10) NOT NULL, "lector_id" bigint NOT NULL REFERENCES "biblioteca_perfil" ("id") DEFERRABLE INITIALLY DEFERRED, "libro_id" bigint NOT NULL REFERENCES "biblioteca_libro" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Reserva
--
CREATE TABLE "biblioteca_reserva" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "creada" datetime NOT NULL, "estado" varchar(10) NOT NULL, "lector_id" bigint NOT NULL REFERENCES "biblioteca_perfil" ("id") DEFERRABLE INITIALLY DEFERRED, "libro_id" bigint NOT NULL REFERENCES "biblioteca_libro" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "biblioteca_prestamo_lector_id_c48c43e7" ON "biblioteca_prestamo" ("lector_id");
CREATE INDEX "biblioteca_prestamo_libro_id_c71c231b" ON "biblioteca_prestamo" ("libro_id");
CREATE INDEX "biblioteca_reserva_lector_id_054f8144" ON "biblioteca_reserva" ("lector_id");
CREATE INDEX "biblioteca_reserva_libro_id_b356f2b1" ON "biblioteca_reserva" ("libro_id");
COMMIT;

-- HU-17 · migración 0002 (py manage.py sqlmigrate biblioteca 0002)
BEGIN;
--
-- Create model Solicitud
--
CREATE TABLE "biblioteca_solicitud" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "creada" datetime NOT NULL, "estado" varchar(10) NOT NULL, "atendida" datetime NULL, "lector_id" bigint NOT NULL REFERENCES "biblioteca_perfil" ("id") DEFERRABLE INITIALLY DEFERRED, "libro_id" bigint NOT NULL REFERENCES "biblioteca_libro" ("id") DEFERRABLE INITIALLY DEFERRED, "prestamo_id" bigint NULL UNIQUE REFERENCES "biblioteca_prestamo" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "biblioteca_solicitud_lector_id_2a1a6344" ON "biblioteca_solicitud" ("lector_id");
CREATE INDEX "biblioteca_solicitud_libro_id_b990b808" ON "biblioteca_solicitud" ("libro_id");
COMMIT;

-- HU-13 · migración 0004 (py manage.py sqlmigrate biblioteca 0004)
BEGIN;
--
-- Add field guardada_hasta to reserva
--
ALTER TABLE "biblioteca_reserva" ADD COLUMN "guardada_hasta" datetime NULL;
--
-- Alter field estado on reserva
--
-- (no-op)
COMMIT;

-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler version: 0.9.4
-- PostgreSQL version: 13.0
-- Project Site: pgmodeler.io
-- Model Author: Lucas Felix

-- Database creation must be performed outside a multi lined SQL file. 
-- These commands were put in this file only as a convenience.
-- 
-- object: a3data | type: DATABASE --
-- DROP DATABASE IF EXISTS a3data;
-- CREATE DATABASE a3data;
-- ddl-end --


-- object: public."user" | type: TABLE --
-- DROP TABLE IF EXISTS public."user" CASCADE;
CREATE TABLE public."user" (
	id bigserial NOT NULL,
	name text NOT NULL,
	email varchar(50) NOT NULL,
	password text NOT NULL,
	CONSTRAINT user_pk PRIMARY KEY (id)
);
-- ddl-end --

INSERT INTO public."user" (id, name, email, password) VALUES (E'1', E'Administrador', E'admin@email.com', E'123456');
-- ddl-end --

-- object: public.session | type: TABLE --
-- DROP TABLE IF EXISTS public.session CASCADE;
CREATE TABLE public.session (
	id serial NOT NULL,
	token varchar(50) NOT NULL,
	expiration timestamp NOT NULL,
	id_user bigint NOT NULL,
	CONSTRAINT authentication_pk PRIMARY KEY (id)
);
-- ddl-end --

-- object: public.patient | type: TABLE --
-- DROP TABLE IF EXISTS public.patient CASCADE;
CREATE TABLE public.patient (
	id varchar(36) NOT NULL,
	birthplace text NOT NULL,
	ssn varchar(11) NOT NULL,
	first_name text NOT NULL,
	last_name text NOT NULL,
	CONSTRAINT ssn_uq UNIQUE (ssn),
	CONSTRAINT patient_pk PRIMARY KEY (id)
);
-- ddl-end --

-- object: user_fk | type: CONSTRAINT --
-- ALTER TABLE public.session DROP CONSTRAINT IF EXISTS user_fk CASCADE;
ALTER TABLE public.session ADD CONSTRAINT user_fk FOREIGN KEY (id_user)
REFERENCES public."user" (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: session_id_user_unique | type: CONSTRAINT --
-- ALTER TABLE public.session DROP CONSTRAINT IF EXISTS session_id_user_unique CASCADE;
ALTER TABLE public.session ADD CONSTRAINT session_id_user_unique UNIQUE (id_user);
-- ddl-end --

-- object: authentication_token_index | type: INDEX --
-- DROP INDEX IF EXISTS public.authentication_token_index CASCADE;
CREATE INDEX authentication_token_index ON public.session
USING btree
(
	token
);
-- ddl-end --

-- object: authentication_id_user_index | type: INDEX --
-- DROP INDEX IF EXISTS public.authentication_id_user_index CASCADE;
CREATE INDEX authentication_id_user_index ON public.session
USING btree
(
	id_user
);
-- ddl-end --


-- Appended SQL commands --
CREATE EXTENSION pgcrypto
WITH SCHEMA public;

DO $$ 
 --Substitua SECRET_KEY na próxima linha pela chave de criptografia utilizada no ambiente, em seguida descomente-a.
 DECLARE secret text := '123456';
 begin
 update public."user" set "password" = public.PGP_SYM_ENCRYPT(public."user".password, secret);
END $$;
-- ddl-end --
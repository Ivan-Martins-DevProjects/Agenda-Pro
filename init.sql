--
-- PostgreSQL database dump
--

\restrict BEIY4Hb1LN6mdkGL2Lm9wevd18FB8H0EqXoa7vNSMQEgTVfZvHIJbXWb6inJJxi

-- Dumped from database version 15.14 (Debian 15.14-1.pgdg13+1)
-- Dumped by pg_dump version 15.14 (Debian 15.14-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: bussines; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bussines (
    id character varying(255) NOT NULL,
    nome character varying(60),
    email character varying(60),
    telefone character varying(15)
);

ALTER TABLE public.bussines OWNER TO postgres;

--
-- Name: contacts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contacts (
    userid character varying(250),
    clientid character varying(250),
    nome character varying(50),
    email character varying(100),
    last_contact timestamp without time zone DEFAULT now(),
    status character varying(255) DEFAULT true,
    telefone character varying(20),
    visitas integer DEFAULT 0,
    gasto integer DEFAULT 0,
    obs character varying(1000),
    resp_name character varying(255),
    bussines_id character varying(255),
    search text,
    cpf character varying(20)
);

ALTER TABLE public.contacts OWNER TO postgres;

--
-- Name: contacts_address; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contacts_address (
    clientid character varying(255),
    rua character varying(100),
    bairro character varying(50),
    cidade character varying(50),
    numero integer
);

ALTER TABLE public.contacts_address OWNER TO postgres;

--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    user_id character varying(255) NOT NULL,
    read_contacts boolean,
    write_contacts boolean,
    read_appointments boolean,
    write_appointments boolean,
    delete_contact boolean
);

ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    role character varying(10),
    instance character varying(255),
    isconnected boolean,
    nome character varying(50),
    bussiness character varying(255)
);

ALTER TABLE public.users OWNER TO postgres;

--
-- Name: bussines bussines_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bussines
    ADD CONSTRAINT bussines_pkey PRIMARY KEY (id);

--
-- Name: roles role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT role_pkey PRIMARY KEY (user_id);

--
-- Name: contacts unique_clientid; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts
    ADD CONSTRAINT unique_clientid UNIQUE (clientid);

--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);

--
-- Name: users fk_bussiness_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_bussiness_id FOREIGN KEY (id) REFERENCES public.bussines(id);

--
-- Name: contacts_address fk_contacts_info; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts_address
    ADD CONSTRAINT fk_contacts_info FOREIGN KEY (clientid) REFERENCES public.contacts(clientid);

--
-- Name: roles roles_pkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey FOREIGN KEY (user_id) REFERENCES public.users(id);

--
-- INSERT Statements
--

INSERT INTO public.bussines (
    id,
    nome,
    email,
    telefone
)
VALUES (
    '1',
    'Agenda PRO',
    'Agendpro@email.com',
    '1234567890'
);

INSERT INTO public.users (
    id,
    email,
    password,
    created_at,
    role,
    instance,
    isconnected,
    nome,
    bussiness
)
VALUES (
    '1',
    'admin@email.com',
    'admin',
    CURRENT_TIMESTAMP,
    'admin',
    'default',
    true,
    'Administrador',
    'Agenda PRO'
);

--
-- PostgreSQL database dump complete
--

\unrestrict BEIY4Hb1LN6mdkGL2Lm9wevd18FB8H0EqXoa7vNSMQEgTVfZvHIJbXWb6inJJxi


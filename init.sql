--
-- PostgreSQL database dump
--

\restrict bYQAF4yKEHA6s6SGxo3nEeEhdBaTD1A4bbxDLxskJKfjfLdtWRn4CBKyHGUyzIl

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
-- Name: appointments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.appointments (
    id character varying(255) NOT NULL,
    user_id character varying(255),
    service_id character varying(255),
    client_id character varying(255),
    date date,
    time_begin time without time zone,
    status character varying(20) DEFAULT 'pendente'::character varying,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    bussines_id character varying(255),
    client_name character varying(100),
    user_name character varying(255),
    service_name character varying(255),
    price integer,
    obs text,
    duration integer
);


ALTER TABLE public.appointments OWNER TO postgres;

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
    delete_contact boolean,
    read_services boolean,
    write_services boolean,
    delete_services boolean
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: services; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.services (
    id character varying(255) NOT NULL,
    user_id character varying(255),
    bussines_id character varying(255),
    title character varying(50),
    description text,
    price numeric,
    duration numeric,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    resp_name character varying(100)
);


ALTER TABLE public.services OWNER TO postgres;

--
-- Name: services_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.services_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.services_id_seq OWNER TO postgres;

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
-- Data for Name: appointments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.appointments (id, user_id, service_id, client_id, date, time_begin, status, created_at, updated_at, bussines_id, client_name, user_name, service_name, price, obs, duration) FROM stdin;
01744f09-ebde-49c4-977c-74a266e0f0c4	usr_2	srv_2	cli_2	2025-12-30	10:45:00	pendente	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Daniela Lima	Julia (Manicure)	Limpeza de Pele Profunda	9000	Cliente frequente	120
27ac227a-eb18-4d46-9f2f-db13963157b1	usr_3	srv_3	cli_3	2025-12-16	19:15:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	\N	Roberto (Estilista)	Selagem	18000	Cansaço muscular nos ombros	120
79a1e808-cb6d-44ad-a0a0-431fba4da014	usr_4	srv_4	cli_4	2026-01-18	11:30:00	pendente	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Fernanda Oliveira	Roberto (Estilista)	Manicure Completa	4500	Resenha de casamento	120
7a9c920b-16e8-4027-abeb-21d2f2a0fa02	usr_5	srv_5	cli_5	2025-12-25	11:45:00	pendente	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Maria Clara Gomes	Patricia (Colorista)	Coloração	15000	Cliente tem alergia a amônia	120
f00858b6-6ba2-45a2-abdf-9b77430656f0	usr_1	srv_6	cli_6	2025-12-20	10:45:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Juliana Santos	Fernanda (Esteticista)	Hidratação Capilar	8000	Pacote de 5 sessões (2/5)	120
f9813d7b-30a3-4981-8adf-8bda800448a1	usr_2	srv_7	cli_7	2025-12-29	12:45:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Ana Silva	Marcos (Barbeiro)	Progressiva	20000	Primeira vez no salão	120
01fb459f-ef33-4310-bcd6-62f3115f23b1	usr_3	srv_8	cli_8	2025-12-20	14:30:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Tatiane Mendes	Roberto (Estilista)	Corte de Cabelo Masculino	5000	Traçado degradê	120
6f02323c-ed6c-46c8-b537-9b666fea9583	usr_4	srv_9	cli_9	2026-02-03	09:15:00	cancelado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Maria Clara Gomes	Fernanda (Esteticista)	Limpeza de Pele Profunda	9000	Traçado degradê	120
660b8eba-29a5-413f-84c4-534eda263c67	usr_5	srv_10	cli_10	2026-01-06	10:15:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Lucas Ferreira	Roberto (Estilista)	Hidratação Capilar	8000	Cuidado com a região da nuca	120
a4b2cf16-994b-4f31-8864-48eb680c74fd	usr_1	srv_11	cli_11	2026-02-03	13:30:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Victor Hugo	Marcos (Barbeiro)	Corte de Cabelo Masculino	5000	Cliente tem alergia a amônia	120
9a31fb65-e57a-4832-9c27-c009f2be30bf	usr_2	srv_12	cli_12	2026-02-01	12:30:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Beatriz Rodrigues	Patricia (Colorista)	Progressiva	20000	Chegar 10 minutos antes	120
09704717-04e1-4296-b25e-56d64e9b4b4f	usr_2	srv_1	cli_17	2025-12-22	09:15:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Juliana Santos	Julia (Manicure)	Pedicure Spa	6000	Pacote de 5 sessões (2/5)	120
f2adab23-246e-4c1b-b287-917817158753	usr_3	srv_2	cli_18	2026-01-10	16:45:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Pedro Henrique	Roberto (Estilista)	Progressiva	20000	Primeira vez no salão	120
1d0284cc-4b87-4301-9ea3-4dcdf275d2aa	usr_4	srv_3	cli_19	2026-01-23	09:15:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Eduardo Pereira	Roberto (Estilista)	Corte Feminino	6500	Cliente frequente	120
5592f071-5360-4071-afe7-f65d11434e26	usr_5	srv_4	cli_20	2026-01-02	12:15:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Lucas Ferreira	Fernanda (Esteticista)	Barba Modelada	3500	Cuidado com a região da nuca	120
2b5cd6f6-89c6-4da7-8bcb-c613cf3f70b0	usr_1	srv_5	cli_1	2026-01-20	09:00:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Pedro Henrique	Roberto (Estilista)	Selagem	18000	Primeira vez no salão	120
363cc69f-f4c2-4b51-a114-a16762ec34d2	usr_5	srv_1	cli_5	2026-01-20	18:30:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Fernanda Oliveira	Fernanda (Esteticista)	Coloração	15000	Cliente tem alergia a amônia	120
5559d923-596c-49ef-bd0e-e632d0df40f7	usr_1	srv_2	cli_6	2026-01-27	18:00:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Helena Martins	Fernanda (Esteticista)	Barba Modelada	3500	Prefere tons mais claros	120
fe9e1ddb-fcfa-4eab-94e9-35f712d1abfc	usr_2	srv_3	cli_7	2026-01-27	12:15:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Helena Martins	Roberto (Estilista)	Massagem Relaxante	12000	Pacote de 5 sessões (2/5)	120
ae35b9d0-a45f-4a23-ab75-49da1f28e222	usr_3	srv_4	cli_8	2025-12-19	15:00:00	cancelado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Carlos Souza	Roberto (Estilista)	Corte de Cabelo Masculino	5000	Resenha de casamento	120
87b851a9-aa22-44e7-b8d1-5fd504e22209	usr_4	srv_5	cli_9	2025-12-31	10:30:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Eduardo Pereira	Lucas (Massagista)	Massagem Relaxante	12000	Cuidado com a região da nuca	120
530f5076-ef39-4bf8-b546-f0980be22cc6	usr_5	srv_6	cli_10	2026-01-20	17:00:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Lucas Ferreira	Lucas (Massagista)	Pezinho e Acabamento	2500	Resenha de casamento	120
3c6b4b31-f082-48fd-a551-f8b4e29c1249	usr_1	srv_7	cli_11	2026-01-24	18:00:00	pendente	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Raquel Moreira	Fernanda (Esteticista)	Massagem Relaxante	12000	Cliente tem alergia a amônia	120
2dacd6ce-7dbf-4d6f-be8f-6f738a3cfd47	usr_2	srv_8	cli_12	2025-12-20	10:15:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Igor Almeida	\N	Selagem	18000	Cliente tem alergia a amônia	120
4b8e19c6-3a02-4883-9c79-581750e0f17c	usr_3	srv_9	cli_13	2026-01-12	12:15:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Lucas Ferreira	Julia (Manicure)	Barba Modelada	3500	Cansaço muscular nos ombros	120
358a19b9-2a86-4879-ad95-4439de8ec083	usr_3	srv_1	cli_13	2026-01-02	09:30:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	\N	Roberto (Estilista)	Corte de Cabelo Masculino	5000	Traçado degradê	120
fff492a7-1cba-4aff-9bcb-62df40ef2cd7	usr_4	srv_2	cli_14	2026-01-26	17:45:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Pedro Henrique	Lucas (Massagista)	Progressiva	20000	\N	120
b65a8a61-1423-42ee-980c-1c7469726fca	usr_5	srv_3	cli_15	2026-01-03	11:15:00	pendente	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Gabriel Rocha	Lucas (Massagista)	Progressiva	20000	Pacote de 5 sessões (2/5)	120
d89b3aa7-6373-494b-86c5-3891d25d283b	usr_1	srv_4	cli_16	2026-01-07	10:00:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Igor Almeida	\N	Barba Modelada	3500	Resenha de casamento	120
2e77ebfe-7961-4f2a-bdb5-11e5248fa2b1	usr_2	srv_5	cli_17	2025-12-18	11:00:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Olivia Dias	Julia (Manicure)	Selagem	18000	Cliente frequente	120
1f09ba6c-80d4-41dc-8d03-cdf26a3868b5	usr_3	srv_6	cli_18	2026-01-30	17:45:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Carlos Souza	Fernanda (Esteticista)	Barba Modelada	3500	Cansaço muscular nos ombros	120
73772985-9be6-47e2-aa1c-64e05d4f6048	usr_4	srv_7	cli_19	2025-12-30	13:45:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Carlos Souza	Julia (Manicure)	Selagem	18000	Cliente frequente	120
166a295a-d120-4a10-92cc-447b379bb513	usr_5	srv_8	cli_20	2026-01-20	11:00:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Bruno Costa	Roberto (Estilista)	Coloração	15000	Prefere tons mais claros	120
6ca7fda2-5414-4568-ae50-4509c9cc49a1	usr_1	srv_9	cli_1	2026-01-28	12:45:00	pendente	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Helena Martins	Roberto (Estilista)	Massagem Relaxante	12000	Prefere tons mais claros	120
c92238c0-0b30-4e42-855a-cc21bb3440c2	usr_2	srv_10	cli_2	2026-01-19	15:45:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Raquel Moreira	Roberto (Estilista)	Pedicure Spa	6000	Cuidado com a região da nuca	120
04ee7837-c7a5-4070-8075-b67f6ef4b90a	usr_3	srv_11	cli_3	2025-12-28	11:15:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Lucas Ferreira	Lucas (Massagista)	Pezinho e Acabamento	2500	\N	120
61ba5aef-dc0a-4677-b569-9ad6534ec0fa	usr_4	srv_12	cli_4	2026-01-19	08:30:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Helena Martins	Roberto (Estilista)	Manicure Completa	4500	Cliente frequente	120
c46e591e-25f7-4017-be66-5627dc3466b1	usr_4	srv_10	cli_14	2026-01-02	13:45:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Carlos Souza	Roberto (Estilista)	Coloração	15000	\N	120
3db5a718-c34c-4f07-952a-c0f5d2fb67dd	usr_5	srv_11	cli_15	2026-01-08	09:00:00	pendente	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Pedro Henrique	Roberto (Estilista)	Manicure Completa	4500	Primeira vez no salão	120
ba094060-5def-410e-ba11-532fe2c59efd	usr_1	srv_12	cli_16	2026-01-16	09:15:00	confirmado	2026-01-14 20:49:19.055542	2026-01-14 20:49:19.055542	Agenda PRO	Gabriel Rocha	Patricia (Colorista)	Progressiva	20000	Cliente tem alergia a amônia	120
\.


--
-- Data for Name: bussines; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bussines (id, nome, email, telefone) FROM stdin;
1	Agenda PRO	Agendpro@email.com	1234567890
\.


--
-- Data for Name: contacts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contacts (userid, clientid, nome, email, last_contact, status, telefone, visitas, gasto, obs, resp_name, bussines_id, search, cpf) FROM stdin;
1	86844956-f366-433a-bb39-9bdd76558b04	Ivan Martins	Ivan_g.Martins@outlook.com	2025-12-13 01:55:08.693604	ativo	11952923369	0	0		Administrador	Agenda PRO	\N	
1	client_26	Cliente 26	cliente26@email.com	2025-12-13 13:32:03.33706	ativo	11990000026	3	1055	Observação do cliente 26	Responsável 26	Agenda PRO	cliente 26	00000000026
1	client_28	Cliente 28	cliente28@email.com	2025-12-13 13:32:03.33706	ativo	11990000028	4	3524	Observação do cliente 28	Responsável 28	Agenda PRO	cliente 28	00000000028
1	client_29	Cliente 29	cliente29@email.com	2025-12-13 13:32:03.33706	ativo	11990000029	3	1475	Observação do cliente 29	Responsável 29	Agenda PRO	cliente 29	00000000029
1	client_30	Cliente 30	cliente30@email.com	2025-12-13 13:32:03.33706	ativo	11990000030	5	4384	Observação do cliente 30	Responsável 30	Agenda PRO	cliente 30	00000000030
1	client_31	Cliente 31	cliente31@email.com	2025-12-13 13:32:03.33706	ativo	11990000031	6	717	Observação do cliente 31	Responsável 31	Agenda PRO	cliente 31	00000000031
1	client_32	Cliente 32	cliente32@email.com	2025-12-13 13:32:03.33706	ativo	11990000032	8	4668	Observação do cliente 32	Responsável 32	Agenda PRO	cliente 32	00000000032
1	client_7	Cliente 7	cliente7@email.com	2025-12-13 13:32:03.33706	ativo	11990000007	4	1056	Observação do cliente 7	Responsável 7	Agenda PRO	cliente 7	00000000007
1	client_8	Cliente 8	cliente8@email.com	2025-12-13 13:32:03.33706	ativo	11990000008	8	273	Observação do cliente 8	Responsável 8	Agenda PRO	cliente 8	00000000008
1	client_9	Cliente 9	cliente9@email.com	2025-12-13 13:32:03.33706	ativo	11990000009	9	134	Observação do cliente 9	Responsável 9	Agenda PRO	cliente 9	00000000009
1	client_10	Cliente 10	cliente10@email.com	2025-12-13 13:32:03.33706	ativo	11990000010	10	4491	Observação do cliente 10	Responsável 10	Agenda PRO	cliente 10	00000000010
1	client_11	Cliente 11	cliente11@email.com	2025-12-13 13:32:03.33706	ativo	11990000011	5	3915	Observação do cliente 11	Responsável 11	Agenda PRO	cliente 11	00000000011
1	client_12	Cliente 12	cliente12@email.com	2025-12-13 13:32:03.33706	ativo	11990000012	2	4206	Observação do cliente 12	Responsável 12	Agenda PRO	cliente 12	00000000012
1	client_13	Cliente 13	cliente13@email.com	2025-12-13 13:32:03.33706	ativo	11990000013	10	3586	Observação do cliente 13	Responsável 13	Agenda PRO	cliente 13	00000000013
1	client_14	Cliente 14	cliente14@email.com	2025-12-13 13:32:03.33706	ativo	11990000014	9	433	Observação do cliente 14	Responsável 14	Agenda PRO	cliente 14	00000000014
1	client_15	Cliente 15	cliente15@email.com	2025-12-13 13:32:03.33706	ativo	11990000015	6	2386	Observação do cliente 15	Responsável 15	Agenda PRO	cliente 15	00000000015
1	client_16	Cliente 16	cliente16@email.com	2025-12-13 13:32:03.33706	ativo	11990000016	3	659	Observação do cliente 16	Responsável 16	Agenda PRO	cliente 16	00000000016
1	client_17	Cliente 17	cliente17@email.com	2025-12-13 13:32:03.33706	ativo	11990000017	6	3141	Observação do cliente 17	Responsável 17	Agenda PRO	cliente 17	00000000017
1	client_18	Cliente 18	cliente18@email.com	2025-12-13 13:32:03.33706	ativo	11990000018	4	820	Observação do cliente 18	Responsável 18	Agenda PRO	cliente 18	00000000018
1	client_19	Cliente 19	cliente19@email.com	2025-12-13 13:32:03.33706	ativo	11990000019	4	3274	Observação do cliente 19	Responsável 19	Agenda PRO	cliente 19	00000000019
1	client_20	Cliente 20	cliente20@email.com	2025-12-13 13:32:03.33706	ativo	11990000020	9	1729	Observação do cliente 20	Responsável 20	Agenda PRO	cliente 20	00000000020
1	client_22	Cliente 22	cliente22@email.com	2025-12-13 13:32:03.33706	ativo	11990000022	1	1274	Observação do cliente 22	Responsável 22	Agenda PRO	cliente 22	00000000022
1	client_23	Cliente 23	cliente23@email.com	2025-12-13 13:32:03.33706	ativo	11990000023	5	922	Observação do cliente 23	Responsável 23	Agenda PRO	cliente 23	00000000023
1	client_24	Cliente 24	cliente24@email.com	2025-12-13 13:32:03.33706	ativo	11990000024	9	3842	Observação do cliente 24	Responsável 24	Agenda PRO	cliente 24	00000000024
1	client_25	Cliente 25	cliente25@email.com	2025-12-13 13:32:03.33706	ativo	11990000025	0	4307	Observação do cliente 25	Responsável 25	Agenda PRO	cliente 25	00000000025
1	client_5	Cliente 5	cliente5@email.com	2025-12-13 13:32:03.33706	ativo	11990000005	0	3995	Observação do cliente 5	Responsável 5	Agenda PRO	cliente 5	00000000005
\.


--
-- Data for Name: contacts_address; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contacts_address (clientid, rua, bairro, cidade, numero) FROM stdin;
86844956-f366-433a-bb39-9bdd76558b04				0
client_5	Rua Exemplo 5	Bairro 5	Cidade Exemplo	304
client_7	Rua Exemplo 7	Bairro 7	Cidade Exemplo	986
client_8	Rua Exemplo 8	Bairro 8	Cidade Exemplo	743
client_9	Rua Exemplo 9	Bairro 9	Cidade Exemplo	217
client_10	Rua Exemplo 10	Bairro 10	Cidade Exemplo	40
client_11	Rua Exemplo 11	Bairro 11	Cidade Exemplo	659
client_12	Rua Exemplo 12	Bairro 12	Cidade Exemplo	0
client_13	Rua Exemplo 13	Bairro 13	Cidade Exemplo	770
client_14	Rua Exemplo 14	Bairro 14	Cidade Exemplo	709
client_15	Rua Exemplo 15	Bairro 15	Cidade Exemplo	199
client_16	Rua Exemplo 16	Bairro 16	Cidade Exemplo	562
client_17	Rua Exemplo 17	Bairro 17	Cidade Exemplo	827
client_18	Rua Exemplo 18	Bairro 18	Cidade Exemplo	432
client_19	Rua Exemplo 19	Bairro 19	Cidade Exemplo	665
client_20	Rua Exemplo 20	Bairro 20	Cidade Exemplo	26
client_22	Rua Exemplo 22	Bairro 22	Cidade Exemplo	408
client_23	Rua Exemplo 23	Bairro 23	Cidade Exemplo	567
client_24	Rua Exemplo 24	Bairro 24	Cidade Exemplo	987
client_25	Rua Exemplo 25	Bairro 25	Cidade Exemplo	726
client_26	Rua Exemplo 26	Bairro 26	Cidade Exemplo	998
client_28	Rua Exemplo 28	Bairro 28	Cidade Exemplo	182
client_29	Rua Exemplo 29	Bairro 29	Cidade Exemplo	596
client_30	Rua Exemplo 30	Bairro 30	Cidade Exemplo	190
client_31	Rua Exemplo 31	Bairro 31	Cidade Exemplo	720
client_32	Rua Exemplo 32	Bairro 32	Cidade Exemplo	100
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (user_id, read_contacts, write_contacts, read_appointments, write_appointments, delete_contact, read_services, write_services, delete_services) FROM stdin;
1	t	t	t	t	t	t	t	t
\.


--
-- Data for Name: services; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services (id, user_id, bussines_id, title, description, price, duration, created_at, resp_name) FROM stdin;
10	1	Agenda PRO	Luzes	Mechas naturais	20000	120	2025-12-29 17:56:40.13281	\N
11	1	Agenda PRO	Tintura	Coloração completa	12000	90	2025-12-29 17:56:40.13281	\N
12	1	Agenda PRO	Progressiva	Alisamento temporário	25000	150	2025-12-29 17:56:40.13281	\N
13	1	Agenda PRO	Botox Capilar	Preenchimento de fios	18000	60	2025-12-29 17:56:40.13281	\N
14	1	Agenda PRO	Corte Social	Corte rápido sem lavagem	3500	20	2025-12-29 17:56:40.13281	\N
15	1	Agenda PRO	Massagem Capilar	Relaxamento e hidratação	5000	30	2025-12-29 17:56:40.13281	\N
16	1	Agenda PRO	Manutenção Dread	Manutenção de dreads	10000	60	2025-12-29 17:56:40.13281	\N
18	1	Agenda PRO	Mechas Loiras	Descoloração e tonalização	28000	150	2025-12-29 17:56:40.13281	\N
20	1	Agenda PRO	Selagem	Tratamento anti-frizz	22000	120	2025-12-29 17:56:40.13281	\N
21	1	Agenda PRO	Corte de Pontas	Apenas remoção das pontas duplas	3000	20	2025-12-29 17:56:40.13281	\N
22	1	Agenda PRO	Coloração Preto	Tintura preta básica	8000	60	2025-12-29 17:56:40.13281	\N
23	1	Agenda PRO	Coloração Ruivo	Tintura vermelha intensa	9000	60	2025-12-29 17:56:40.13281	\N
24	1	Agenda PRO	Coloração Castanho	Tintura marrom chocolate	8500	60	2025-12-29 17:56:40.13281	\N
25	1	Agenda PRO	Henna de Sobrancelha	Tintagem natural com henna	3000	20	2025-12-29 17:56:40.13281	\N
26	1	Agenda PRO	Limpeza de Pele	Procedimento estético facial	12000	60	2025-12-29 17:56:40.13281	\N
27	1	Agenda PRO	Design de Sobrancelha	Correção e design de formato	3500	30	2025-12-29 17:56:40.13281	\N
28	1	Agenda PRO	Penteado Festa	Pentear para ocasiões especiais	15000	60	2025-12-29 17:56:40.13281	\N
30	1	Agenda PRO	Coque Afro	Penteados específicos para fios crespos	8000	45	2025-12-29 17:56:40.13281	\N
31	1	Agenda PRO	Finalização Gloss	Brilho intenso para o cabelo	9000	30	2025-12-29 17:56:40.13281	\N
2	1	Agenda PRO	Corte de Cabelo Masculino	Corte tradicional com tesoura e máquina	5000	30	2025-12-29 17:56:40.13281	\N
5	1	Agenda PRO	Hidratação	Máscara capilar profunda	6000	40	2025-12-29 17:56:40.13281	\N
3	1	Agenda PRO	Barba Completa	Toalha quente, navalha e finalização	4000	30	2025-12-29 17:56:40.13281	\N
6	1	Agenda PRO	Corte Infantil	Corte para crianças até 12 anos	4000	30	2025-12-29 17:56:40.13281	\N
4	1	Agenda PRO	Pezinho	Acabamento na nuca e laterais	2000	15	2025-12-29 17:56:40.13281	\N
9	1	Agenda PRO	Platinado	Clareamento total dos fios	300	180	2025-12-29 17:56:40.13281	\N
736f7437-f74c-4181-9572-1c9bc4da2c11	1	Agenda PRO	Corte de Cabelo Masculina	Corte tradicional com tesoura e máquina	500	30	2026-01-19 18:28:16.430954	Administrador
8	1	Agenda PRO	Sobrancelham	Design e pinça	25	15	2025-12-29 17:56:40.13281	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, email, password, created_at, role, instance, isconnected, nome, bussiness) FROM stdin;
1	admin@email.com	admin	2025-12-12 19:05:07.506279	admin	default	t	Administrador	Agenda PRO
\.


--
-- Name: services_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.services_id_seq', 36, true);


--
-- Name: appointments appointments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_pkey PRIMARY KEY (id);


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
-- Name: services services_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_pkey PRIMARY KEY (id);


--
-- Name: services services_title_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_title_unique UNIQUE (title);


--
-- Name: contacts unique_clientid; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts
    ADD CONSTRAINT unique_clientid UNIQUE (clientid);


--
-- Name: contacts unique_telefone; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts
    ADD CONSTRAINT unique_telefone UNIQUE (telefone);


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
-- PostgreSQL database dump complete
--

\unrestrict bYQAF4yKEHA6s6SGxo3nEeEhdBaTD1A4bbxDLxskJKfjfLdtWRn4CBKyHGUyzIl


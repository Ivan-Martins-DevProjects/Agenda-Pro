--
-- PostgreSQL database dump
--

\restrict VE9K4oJ7qpdudNdYTCAzTRW6cRo9nbZlL8tMCQ37TLnLkevT2i15QgWucVNAnkG

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
    delete_contact boolean,
    read_services boolean
);


ALTER TABLE public.roles OWNER TO postgres;

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
-- Name: services; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.services (
    id character varying(255) DEFAULT nextval('public.services_id_seq'::regclass) NOT NULL,
    user_id character varying(255),
    bussines_id character varying(255),
    name character varying(50),
    description text,
    price integer,
    duration integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.services OWNER TO postgres;

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
-- Data for Name: bussines; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bussines (id, nome, email, telefone) FROM stdin;
1	Agenda PRO	Agendpro@email.com	1234567890
\.


--
-- Data for Name: contacts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contacts (userid, clientid, nome, email, last_contact, status, telefone, visitas, gasto, obs, resp_name, bussines_id, search, cpf) FROM stdin;
1	client_3	Cliente 3	cliente3@email.com	2025-12-13 13:32:03.33706	ativo	11990000003	0	3452	Observação do cliente 3	Responsável 3	Agenda PRO	cliente 3	00000000003
1	client_5	Cliente 5	cliente5@email.com	2025-12-13 13:32:03.33706	ativo	11990000005	0	3995	Observação do cliente 5	Responsável 5	Agenda PRO	cliente 5	00000000005
1	client_6	Cliente 6	cliente6@email.com	2025-12-13 13:32:03.33706	ativo	11990000006	1	123	Observação do cliente 6	Responsável 6	Agenda PRO	cliente 6	00000000006
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
\.


--
-- Data for Name: contacts_address; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contacts_address (clientid, rua, bairro, cidade, numero) FROM stdin;
86844956-f366-433a-bb39-9bdd76558b04				0
client_3	Rua Exemplo 3	Bairro 3	Cidade Exemplo	758
client_5	Rua Exemplo 5	Bairro 5	Cidade Exemplo	304
client_6	Rua Exemplo 6	Bairro 6	Cidade Exemplo	507
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

COPY public.roles (user_id, read_contacts, write_contacts, read_appointments, write_appointments, delete_contact, read_services) FROM stdin;
1	t	t	t	t	t	t
\.


--
-- Data for Name: services; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services (id, user_id, bussines_id, name, description, price, duration, created_at) FROM stdin;
2	1	Agenda PRO	Corte de Cabelo Masculino	Corte tradicional com tesoura e máquina	50	30	2025-12-29 17:56:40.13281
3	1	Agenda PRO	Barba Completa	Toalha quente, navalha e finalização	40	30	2025-12-29 17:56:40.13281
4	1	Agenda PRO	Pezinho	Acabamento na nuca e laterais	20	15	2025-12-29 17:56:40.13281
5	1	Agenda PRO	Hidratação	Máscara capilar profunda	60	40	2025-12-29 17:56:40.13281
6	1	Agenda PRO	Corte Infantil	Corte para crianças até 12 anos	40	30	2025-12-29 17:56:40.13281
7	1	Agenda PRO	Pigmentação de Barba	Design e pigmentação para barba	150	60	2025-12-29 17:56:40.13281
8	1	Agenda PRO	Sobrancelha	Design e pinça	25	15	2025-12-29 17:56:40.13281
9	1	Agenda PRO	Platinado	Clareamento total dos fios	300	180	2025-12-29 17:56:40.13281
10	1	Agenda PRO	Luzes	Mechas naturais	200	120	2025-12-29 17:56:40.13281
11	1	Agenda PRO	Tintura	Coloração completa	120	90	2025-12-29 17:56:40.13281
12	1	Agenda PRO	Progressiva	Alisamento temporário	250	150	2025-12-29 17:56:40.13281
13	1	Agenda PRO	Botox Capilar	Preenchimento de fios	180	60	2025-12-29 17:56:40.13281
14	1	Agenda PRO	Corte Social	Corte rápido sem lavagem	35	20	2025-12-29 17:56:40.13281
15	1	Agenda PRO	Massagem Capilar	Relaxamento e hidratação	50	30	2025-12-29 17:56:40.13281
16	1	Agenda PRO	Manutenção Dread	Manutenção de dreads	100	60	2025-12-29 17:56:40.13281
17	1	Agenda PRO	Alisamento Japonês	Química para alisar fios cacheados	350	180	2025-12-29 17:56:40.13281
18	1	Agenda PRO	Mechas Loiras	Descoloração e tonalização	280	150	2025-12-29 17:56:40.13281
19	1	Agenda PRO	Corte Degradê	Degradê nas laterais e nuca	45	30	2025-12-29 17:56:40.13281
20	1	Agenda PRO	Selagem	Tratamento anti-frizz	220	120	2025-12-29 17:56:40.13281
21	1	Agenda PRO	Corte de Pontas	Apenas remoção das pontas duplas	30	20	2025-12-29 17:56:40.13281
22	1	Agenda PRO	Coloração Preto	Tintura preta básica	80	60	2025-12-29 17:56:40.13281
23	1	Agenda PRO	Coloração Ruivo	Tintura vermelha intensa	90	60	2025-12-29 17:56:40.13281
24	1	Agenda PRO	Coloração Castanho	Tintura marrom chocolate	85	60	2025-12-29 17:56:40.13281
25	1	Agenda PRO	Henna de Sobrancelha	Tintagem natural com henna	30	20	2025-12-29 17:56:40.13281
26	1	Agenda PRO	Limpeza de Pele	Procedimento estético facial	120	60	2025-12-29 17:56:40.13281
27	1	Agenda PRO	Design de Sobrancelha	Correção e design de formato	35	30	2025-12-29 17:56:40.13281
28	1	Agenda PRO	Penteado Festa	Pentear para ocasiões especiais	150	60	2025-12-29 17:56:40.13281
29	1	Agenda PRO	Tranças	Fazer tranças no cabelo inteiro	200	120	2025-12-29 17:56:40.13281
30	1	Agenda PRO	Coque Afro	Penteados específicos para fios crespos	80	45	2025-12-29 17:56:40.13281
31	1	Agenda PRO	Finalização Gloss	Brilho intenso para o cabelo	90	30	2025-12-29 17:56:40.13281
32	1	Agenda PRO	Corte Teste	Corte experimental para novos alunos	0	15	2025-12-29 17:56:40.13281
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

SELECT pg_catalog.setval('public.services_id_seq', 32, true);


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

\unrestrict VE9K4oJ7qpdudNdYTCAzTRW6cRo9nbZlL8tMCQ37TLnLkevT2i15QgWucVNAnkG


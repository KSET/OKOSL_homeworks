--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.18
-- Dumped by pg_dump version 9.5.18

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: okosl
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO okosl;

--
-- Name: homeworks; Type: TABLE; Schema: public; Owner: okosl
--

CREATE TABLE public.homeworks (
    id integer NOT NULL,
    ordinal_number integer NOT NULL,
    name character varying(255),
    year integer NOT NULL
);


ALTER TABLE public.homeworks OWNER TO okosl;

--
-- Name: homeworks_id_seq; Type: SEQUENCE; Schema: public; Owner: okosl
--

CREATE SEQUENCE public.homeworks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.homeworks_id_seq OWNER TO okosl;

--
-- Name: homeworks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: okosl
--

ALTER SEQUENCE public.homeworks_id_seq OWNED BY public.homeworks.id;


--
-- Name: remarks; Type: TABLE; Schema: public; Owner: okosl
--

CREATE TABLE public.remarks (
    id integer NOT NULL,
    text text NOT NULL,
    score_penalty double precision NOT NULL,
    author_id integer NOT NULL,
    date timestamp without time zone NOT NULL,
    solution_group_id integer NOT NULL
);


ALTER TABLE public.remarks OWNER TO okosl;

--
-- Name: remarks_id_seq; Type: SEQUENCE; Schema: public; Owner: okosl
--

CREATE SEQUENCE public.remarks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.remarks_id_seq OWNER TO okosl;

--
-- Name: remarks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: okosl
--

ALTER SEQUENCE public.remarks_id_seq OWNED BY public.remarks.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: okosl
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying(50)
);


ALTER TABLE public.roles OWNER TO okosl;

--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: okosl
--

CREATE SEQUENCE public.roles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.roles_id_seq OWNER TO okosl;

--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: okosl
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: solution_groups; Type: TABLE; Schema: public; Owner: okosl
--

CREATE TABLE public.solution_groups (
    id integer NOT NULL,
    task_id integer NOT NULL,
    final_remark text,
    final_score_penalty integer
);


ALTER TABLE public.solution_groups OWNER TO okosl;

--
-- Name: solution_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: okosl
--

CREATE SEQUENCE public.solution_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.solution_groups_id_seq OWNER TO okosl;

--
-- Name: solution_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: okosl
--

ALTER SEQUENCE public.solution_groups_id_seq OWNED BY public.solution_groups.id;


--
-- Name: solutions; Type: TABLE; Schema: public; Owner: okosl
--

CREATE TABLE public.solutions (
    id integer NOT NULL,
    solution_text text NOT NULL,
    solution_group_id integer NOT NULL
);


ALTER TABLE public.solutions OWNER TO okosl;

--
-- Name: solutions_id_seq; Type: SEQUENCE; Schema: public; Owner: okosl
--

CREATE SEQUENCE public.solutions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.solutions_id_seq OWNER TO okosl;

--
-- Name: solutions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: okosl
--

ALTER SEQUENCE public.solutions_id_seq OWNED BY public.solutions.id;


--
-- Name: tasks; Type: TABLE; Schema: public; Owner: okosl
--

CREATE TABLE public.tasks (
    id integer NOT NULL,
    task_number integer NOT NULL,
    task_text text NOT NULL,
    homework_id integer NOT NULL
);


ALTER TABLE public.tasks OWNER TO okosl;

--
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: okosl
--

CREATE SEQUENCE public.tasks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tasks_id_seq OWNER TO okosl;

--
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: okosl
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- Name: user_roles; Type: TABLE; Schema: public; Owner: okosl
--

CREATE TABLE public.user_roles (
    id integer NOT NULL,
    user_id integer,
    role_id integer
);


ALTER TABLE public.user_roles OWNER TO okosl;

--
-- Name: user_roles_id_seq; Type: SEQUENCE; Schema: public; Owner: okosl
--

CREATE SEQUENCE public.user_roles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_roles_id_seq OWNER TO okosl;

--
-- Name: user_roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: okosl
--

ALTER SEQUENCE public.user_roles_id_seq OWNED BY public.user_roles.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: okosl
--

CREATE TABLE public.users (
    id integer NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    username character varying(100) NOT NULL,
    password character varying(255) DEFAULT ''::character varying NOT NULL,
    first_name character varying(100) DEFAULT ''::character varying NOT NULL,
    last_name character varying(100) DEFAULT ''::character varying NOT NULL,
    added_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO okosl;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: okosl
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO okosl;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: okosl
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.homeworks ALTER COLUMN id SET DEFAULT nextval('public.homeworks_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.remarks ALTER COLUMN id SET DEFAULT nextval('public.remarks_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.solution_groups ALTER COLUMN id SET DEFAULT nextval('public.solution_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.solutions ALTER COLUMN id SET DEFAULT nextval('public.solutions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.user_roles ALTER COLUMN id SET DEFAULT nextval('public.user_roles_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: okosl
--

COPY public.alembic_version (version_num) FROM stdin;
4d49d2a77c15
\.


--
-- Data for Name: homeworks; Type: TABLE DATA; Schema: public; Owner: okosl
--

COPY public.homeworks (id, ordinal_number, name, year) FROM stdin;
4	1	DZ01-2018	2018
5	2	DZ02-2018	2018
6	3	DZ03-2018	2018
7	1	DZ01-2017	2017
8	2	DZ02-2017	2017
9	3	DZ03-2017	2017
1	1	DZ01-2016	2016
2	2	DZ02-2016	2016
3	3	DZ03-2016	2016
\.


--
-- Name: homeworks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: okosl
--

SELECT pg_catalog.setval('public.homeworks_id_seq', 9, true);


--
-- Data for Name: remarks; Type: TABLE DATA; Schema: public; Owner: okosl
--

COPY public.remarks (id, text, score_penalty, author_id, date, solution_group_id) FROM stdin;
\.


--
-- Name: remarks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: okosl
--

SELECT pg_catalog.setval('public.remarks_id_seq', 1, false);


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: okosl
--

COPY public.roles (id, name) FROM stdin;
1	Admin
\.


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: okosl
--

SELECT pg_catalog.setval('public.roles_id_seq', 1, true);


--
-- Data for Name: solution_groups; Type: TABLE DATA; Schema: public; Owner: okosl
--

COPY public.solution_groups (id, task_id, final_remark, final_score_penalty) FROM stdin;
1	4		\N
2	4		\N
3	4		\N
4	5		\N
5	6		\N
6	6		\N
7	1		\N
8	3		\N
9	3		\N
10	2		\N
11	2		\N
\.


--
-- Name: solution_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: okosl
--

SELECT pg_catalog.setval('public.solution_groups_id_seq', 11, true);


--
-- Data for Name: solutions; Type: TABLE DATA; Schema: public; Owner: okosl
--

COPY public.solutions (id, solution_text, solution_group_id) FROM stdin;
1	mali pimpeki	1
2	veliki pimpeki	1
3	ls -la	2
4	ls -al	2
5	ls -a -l	2
6	ls -a	3
7	ls --all	3
8	bilo bi dosta	4
9	dosta bi bilo	4
10	ovo je tocno	5
11	ovo je isto tocno	5
12	ovo ne valja	6
13	ne valja ovo	6
14	ovo je za kurac	6
15	jedino moguce	7
16	isto jedino moguce jer mi se vise ne da	8
17	cat fajl | grep pimpek	9
18	grep pimpek fajl	10
19	grep -ic pat fajl	11
20	grep -ci pat fajl	11
\.


--
-- Name: solutions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: okosl
--

SELECT pg_catalog.setval('public.solutions_id_seq', 20, true);


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: okosl
--

COPY public.tasks (id, task_number, task_text, homework_id) FROM stdin;
4	1	stvorite symlink na /etc/hosts u ~	2
5	2	odredite tip datoteke koristenjem naredbe file	2
6	3	naredbom wc doynajte ukupan broj korisnika na sustavu	2
1	1	Stvorite datoteku koja u prvom retku sadrzi jmbag > personal_info.dat	3
3	3	sortirajte datoteku po broju retka	3
2	2	pomoću naredbe cat i here dokumenta dodajte ime i prezime	3
7	1	odi u home	1
8	2	ispisi .bashrc	1
9	3	kreiraj DZ1 u /tmp	1
10	1	Ispišite sadržaj \\shell{.bash\\_logout} datoteke u vašem matičnom direktoriju.	7
11	2	Ispišite sadržaj svog \\shell{/home} direktorija sortiran po veličini uzlazno.	7
12	3	Pokretanjem iz matičnog direktorija, unutar direktorija \\shell{/tmp} napravite direktorij \\shell{OKOSL tjedan} koji će sadržavati direktorije \\shell{ponedjeljak}, \\shell{utorak}, \\shell{srijeda}, \\shell{cetvrtak}, \\shell{petak} i \\shell{subota}, gdje će subota biti skriveni direktorij	7
13	1	Stvorite datoteku koja u prvom redu sadrži vaš JMBAG koristeći naredbu \\texttt{echo} i preusmjeravanje. Datoteku nazovite \\texttt{personal\\_info.dat}	8
14	2	Pomoću naredbe \\texttt{cat} i here dokumenta dodajte vaše ime i prezime u redak ispod JMBAG-a.	8
15	3	Pomoću naredbe \\shell{tee} dodajte "okosl" u redak ispod imena i prezimena.	8
16	1	Ispišite sve direktorije u \\shell{/usr/share} čiji naziv započinje s \\shell{gtk}	9
17	2	Ispišite sve direktorije u \\shell{/usr/share} koji u nazivu sadrže barem dvije znamenke	9
18	3	Pronađite riječi koje sadrže znamenke (ako ih ima)	9
19	1	2018 prva zadaca prvi zadatak	4
20	2	2018 prva zadaca drugi zadatak	4
21	3	2018 prva zadaca treci	4
22	1	2018 druga zadaca prvi zadatak	5
23	2	2018 2 2	5
24	3	2018 2 3	5
25	1	2018 3 1	6
26	2	2018 3 2	6
27	3	2018 3 3	6
\.


--
-- Name: tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: okosl
--

SELECT pg_catalog.setval('public.tasks_id_seq', 27, true);


--
-- Data for Name: user_roles; Type: TABLE DATA; Schema: public; Owner: okosl
--

COPY public.user_roles (id, user_id, role_id) FROM stdin;
1	1	1
\.


--
-- Name: user_roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: okosl
--

SELECT pg_catalog.setval('public.user_roles_id_seq', 1, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: okosl
--

COPY public.users (id, is_active, username, password, first_name, last_name, added_at) FROM stdin;
1	t	rincewind	$2b$12$jx.90IrKv4s8vmz05L3.aeN41kg7lmy5EFidk.A7qBnYVd7dJmm.i			2019-08-07 15:30:37.89849
2	t	okosl	$2b$12$2cPWhYrgxwuPGss5wzeWeuNsZykDVl6KbmosIwjTZkwuVKONmvKo6			2019-08-07 15:31:06.003478
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: okosl
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: homeworks_pkey; Type: CONSTRAINT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.homeworks
    ADD CONSTRAINT homeworks_pkey PRIMARY KEY (id);


--
-- Name: remarks_pkey; Type: CONSTRAINT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.remarks
    ADD CONSTRAINT remarks_pkey PRIMARY KEY (id);


--
-- Name: roles_name_key; Type: CONSTRAINT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- Name: roles_pkey; Type: CONSTRAINT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: solution_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.solution_groups
    ADD CONSTRAINT solution_groups_pkey PRIMARY KEY (id);


--
-- Name: solutions_pkey; Type: CONSTRAINT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.solutions
    ADD CONSTRAINT solutions_pkey PRIMARY KEY (id);


--
-- Name: tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: unique_homework_year; Type: CONSTRAINT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.homeworks
    ADD CONSTRAINT unique_homework_year UNIQUE (ordinal_number, year);


--
-- Name: user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_username_key; Type: CONSTRAINT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: remarks_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.remarks
    ADD CONSTRAINT remarks_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id);


--
-- Name: remarks_solution_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.remarks
    ADD CONSTRAINT remarks_solution_group_id_fkey FOREIGN KEY (solution_group_id) REFERENCES public.solution_groups(id);


--
-- Name: solution_groups_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.solution_groups
    ADD CONSTRAINT solution_groups_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);


--
-- Name: solutions_solution_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.solutions
    ADD CONSTRAINT solutions_solution_group_id_fkey FOREIGN KEY (solution_group_id) REFERENCES public.solution_groups(id);


--
-- Name: tasks_homework_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_homework_id_fkey FOREIGN KEY (homework_id) REFERENCES public.homeworks(id);


--
-- Name: user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id) ON DELETE CASCADE;


--
-- Name: user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: okosl
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--


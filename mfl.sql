--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO mfl;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO mfl;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO mfl;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO mfl;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO mfl;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO mfl;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: common_constituency; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE common_constituency (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    name character varying(100) NOT NULL,
    code character varying(100) NOT NULL,
    county_id integer NOT NULL,
    created_by_id integer NOT NULL,
    updated_by_id integer NOT NULL
);


ALTER TABLE public.common_constituency OWNER TO mfl;

--
-- Name: common_constituency_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE common_constituency_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_constituency_id_seq OWNER TO mfl;

--
-- Name: common_constituency_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE common_constituency_id_seq OWNED BY common_constituency.id;


--
-- Name: common_contact; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE common_contact (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    email character varying(254),
    town character varying(100) NOT NULL,
    postal_code character varying(100) NOT NULL,
    address character varying(100) NOT NULL,
    nearest_town character varying(100) NOT NULL,
    landline character varying(100) NOT NULL,
    mobile character varying(10) NOT NULL,
    created_by_id integer NOT NULL,
    updated_by_id integer NOT NULL
);


ALTER TABLE public.common_contact OWNER TO mfl;

--
-- Name: common_contact_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE common_contact_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_contact_id_seq OWNER TO mfl;

--
-- Name: common_contact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE common_contact_id_seq OWNED BY common_contact.id;


--
-- Name: common_county; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE common_county (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    name character varying(100) NOT NULL,
    code character varying(100) NOT NULL,
    "Province_id" integer,
    created_by_id integer NOT NULL,
    updated_by_id integer NOT NULL
);


ALTER TABLE public.common_county OWNER TO mfl;

--
-- Name: common_county_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE common_county_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_county_id_seq OWNER TO mfl;

--
-- Name: common_county_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE common_county_id_seq OWNED BY common_county.id;


--
-- Name: common_district; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE common_district (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    name character varying(100) NOT NULL,
    code character varying(100) NOT NULL,
    county_id integer NOT NULL,
    created_by_id integer NOT NULL,
    province_id integer,
    updated_by_id integer NOT NULL
);


ALTER TABLE public.common_district OWNER TO mfl;

--
-- Name: common_district_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE common_district_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_district_id_seq OWNER TO mfl;

--
-- Name: common_district_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE common_district_id_seq OWNED BY common_district.id;


--
-- Name: common_division; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE common_division (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    name character varying(100) NOT NULL,
    code character varying(100) NOT NULL,
    constituency_id integer,
    created_by_id integer NOT NULL,
    district_id integer NOT NULL,
    updated_by_id integer NOT NULL
);


ALTER TABLE public.common_division OWNER TO mfl;

--
-- Name: common_division_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE common_division_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_division_id_seq OWNER TO mfl;

--
-- Name: common_division_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE common_division_id_seq OWNED BY common_division.id;


--
-- Name: common_feedback; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE common_feedback (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    job character varying(255) NOT NULL,
    email character varying(254) NOT NULL,
    subjet character varying(255) NOT NULL,
    comment text NOT NULL
);


ALTER TABLE public.common_feedback OWNER TO mfl;

--
-- Name: common_feedback_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE common_feedback_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_feedback_id_seq OWNER TO mfl;

--
-- Name: common_feedback_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE common_feedback_id_seq OWNED BY common_feedback.id;


--
-- Name: common_location; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE common_location (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    name character varying(100) NOT NULL,
    code character varying(100) NOT NULL,
    created_by_id integer NOT NULL,
    division_id integer NOT NULL,
    updated_by_id integer NOT NULL
);


ALTER TABLE public.common_location OWNER TO mfl;

--
-- Name: common_location_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE common_location_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_location_id_seq OWNER TO mfl;

--
-- Name: common_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE common_location_id_seq OWNED BY common_location.id;


--
-- Name: common_province; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE common_province (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    name character varying(100) NOT NULL,
    code character varying(100) NOT NULL,
    created_by_id integer NOT NULL,
    updated_by_id integer NOT NULL
);


ALTER TABLE public.common_province OWNER TO mfl;

--
-- Name: common_province_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE common_province_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_province_id_seq OWNER TO mfl;

--
-- Name: common_province_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE common_province_id_seq OWNED BY common_province.id;


--
-- Name: common_sublocation; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE common_sublocation (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    name character varying(100) NOT NULL,
    code character varying(100) NOT NULL,
    created_by_id integer NOT NULL,
    location_id integer NOT NULL,
    updated_by_id integer NOT NULL
);


ALTER TABLE public.common_sublocation OWNER TO mfl;

--
-- Name: common_sublocation_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE common_sublocation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_sublocation_id_seq OWNER TO mfl;

--
-- Name: common_sublocation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE common_sublocation_id_seq OWNED BY common_sublocation.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO mfl;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO mfl;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO mfl;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO mfl;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO mfl;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO mfl;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO mfl;

--
-- Name: facilities_facility; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE facilities_facility (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    name character varying(100) NOT NULL,
    code character varying(100) NOT NULL,
    latitude character varying(255) NOT NULL,
    longitude character varying(255) NOT NULL,
    is_classified boolean NOT NULL,
    description text NOT NULL,
    facility_type character varying(100) NOT NULL,
    number_of_beds integer NOT NULL,
    number_of_cots integer NOT NULL,
    open_whole_day boolean NOT NULL,
    open_whole_week boolean NOT NULL,
    status character varying(50) NOT NULL,
    created_by_id integer NOT NULL,
    owner_id integer NOT NULL,
    sub_location_id integer NOT NULL,
    updated_by_id integer NOT NULL,
    CONSTRAINT facilities_facility_number_of_beds_check CHECK ((number_of_beds >= 0)),
    CONSTRAINT facilities_facility_number_of_cots_check CHECK ((number_of_cots >= 0))
);


ALTER TABLE public.facilities_facility OWNER TO mfl;

--
-- Name: facilities_facility_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE facilities_facility_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.facilities_facility_id_seq OWNER TO mfl;

--
-- Name: facilities_facility_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE facilities_facility_id_seq OWNED BY facilities_facility.id;


--
-- Name: facilities_facility_services; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE facilities_facility_services (
    id integer NOT NULL,
    facility_id integer NOT NULL,
    service_id integer NOT NULL
);


ALTER TABLE public.facilities_facility_services OWNER TO mfl;

--
-- Name: facilities_facility_services_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE facilities_facility_services_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.facilities_facility_services_id_seq OWNER TO mfl;

--
-- Name: facilities_facility_services_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE facilities_facility_services_id_seq OWNED BY facilities_facility_services.id;


--
-- Name: facilities_owner; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE facilities_owner (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    code character varying(100) NOT NULL,
    created_by_id integer NOT NULL,
    updated_by_id integer NOT NULL
);


ALTER TABLE public.facilities_owner OWNER TO mfl;

--
-- Name: facilities_owner_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE facilities_owner_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.facilities_owner_id_seq OWNER TO mfl;

--
-- Name: facilities_owner_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE facilities_owner_id_seq OWNED BY facilities_owner.id;


--
-- Name: facilities_service; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE facilities_service (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    code character varying(100),
    created_by_id integer NOT NULL,
    updated_by_id integer NOT NULL
);


ALTER TABLE public.facilities_service OWNER TO mfl;

--
-- Name: facilities_service_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE facilities_service_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.facilities_service_id_seq OWNER TO mfl;

--
-- Name: facilities_service_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE facilities_service_id_seq OWNED BY facilities_service.id;


--
-- Name: roles_permission; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE roles_permission (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    name character varying(100) NOT NULL,
    description text NOT NULL,
    created_by_id integer NOT NULL,
    updated_by_id integer NOT NULL
);


ALTER TABLE public.roles_permission OWNER TO mfl;

--
-- Name: roles_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE roles_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.roles_permission_id_seq OWNER TO mfl;

--
-- Name: roles_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE roles_permission_id_seq OWNED BY roles_permission.id;


--
-- Name: roles_role; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE roles_role (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    name character varying(100) NOT NULL,
    description text NOT NULL,
    code character varying(100),
    created_by_id integer NOT NULL,
    updated_by_id integer NOT NULL
);


ALTER TABLE public.roles_role OWNER TO mfl;

--
-- Name: roles_role_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE roles_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.roles_role_id_seq OWNER TO mfl;

--
-- Name: roles_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE roles_role_id_seq OWNED BY roles_role.id;


--
-- Name: roles_rolepermissions; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE roles_rolepermissions (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    created_by_id integer NOT NULL,
    permission_id integer NOT NULL,
    role_id integer NOT NULL,
    updated_by_id integer NOT NULL
);


ALTER TABLE public.roles_rolepermissions OWNER TO mfl;

--
-- Name: roles_rolepermissions_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE roles_rolepermissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.roles_rolepermissions_id_seq OWNER TO mfl;

--
-- Name: roles_rolepermissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE roles_rolepermissions_id_seq OWNED BY roles_rolepermissions.id;


--
-- Name: roles_userroles; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE roles_userroles (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    created_by_id integer NOT NULL,
    role_id integer NOT NULL,
    updated_by_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.roles_userroles OWNER TO mfl;

--
-- Name: roles_userroles_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE roles_userroles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.roles_userroles_id_seq OWNER TO mfl;

--
-- Name: roles_userroles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE roles_userroles_id_seq OWNED BY roles_userroles.id;


--
-- Name: users_inchargecounties; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE users_inchargecounties (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    county_id integer NOT NULL,
    created_by_id integer NOT NULL,
    updated_by_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.users_inchargecounties OWNER TO mfl;

--
-- Name: users_inchargecounties_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE users_inchargecounties_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_inchargecounties_id_seq OWNER TO mfl;

--
-- Name: users_inchargecounties_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE users_inchargecounties_id_seq OWNED BY users_inchargecounties.id;


--
-- Name: users_mfluser; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE users_mfluser (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    email character varying(254) NOT NULL,
    first_name character varying(60) NOT NULL,
    last_name character varying(60) NOT NULL,
    other_names character varying(80) NOT NULL,
    username character varying(60) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    is_incharge boolean NOT NULL,
    contact_id integer,
    county_id integer,
    is_national boolean NOT NULL
);


ALTER TABLE public.users_mfluser OWNER TO mfl;

--
-- Name: users_mfluser_groups; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE users_mfluser_groups (
    id integer NOT NULL,
    mfluser_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.users_mfluser_groups OWNER TO mfl;

--
-- Name: users_mfluser_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE users_mfluser_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_mfluser_groups_id_seq OWNER TO mfl;

--
-- Name: users_mfluser_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE users_mfluser_groups_id_seq OWNED BY users_mfluser_groups.id;


--
-- Name: users_mfluser_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE users_mfluser_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_mfluser_id_seq OWNER TO mfl;

--
-- Name: users_mfluser_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE users_mfluser_id_seq OWNED BY users_mfluser.id;


--
-- Name: users_mfluser_user_permissions; Type: TABLE; Schema: public; Owner: mfl; Tablespace: 
--

CREATE TABLE users_mfluser_user_permissions (
    id integer NOT NULL,
    mfluser_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.users_mfluser_user_permissions OWNER TO mfl;

--
-- Name: users_mfluser_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: mfl
--

CREATE SEQUENCE users_mfluser_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_mfluser_user_permissions_id_seq OWNER TO mfl;

--
-- Name: users_mfluser_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mfl
--

ALTER SEQUENCE users_mfluser_user_permissions_id_seq OWNED BY users_mfluser_user_permissions.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_constituency ALTER COLUMN id SET DEFAULT nextval('common_constituency_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_contact ALTER COLUMN id SET DEFAULT nextval('common_contact_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_county ALTER COLUMN id SET DEFAULT nextval('common_county_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_district ALTER COLUMN id SET DEFAULT nextval('common_district_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_division ALTER COLUMN id SET DEFAULT nextval('common_division_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_feedback ALTER COLUMN id SET DEFAULT nextval('common_feedback_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_location ALTER COLUMN id SET DEFAULT nextval('common_location_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_province ALTER COLUMN id SET DEFAULT nextval('common_province_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_sublocation ALTER COLUMN id SET DEFAULT nextval('common_sublocation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY facilities_facility ALTER COLUMN id SET DEFAULT nextval('facilities_facility_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY facilities_facility_services ALTER COLUMN id SET DEFAULT nextval('facilities_facility_services_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY facilities_owner ALTER COLUMN id SET DEFAULT nextval('facilities_owner_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY facilities_service ALTER COLUMN id SET DEFAULT nextval('facilities_service_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY roles_permission ALTER COLUMN id SET DEFAULT nextval('roles_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY roles_role ALTER COLUMN id SET DEFAULT nextval('roles_role_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY roles_rolepermissions ALTER COLUMN id SET DEFAULT nextval('roles_rolepermissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY roles_userroles ALTER COLUMN id SET DEFAULT nextval('roles_userroles_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY users_inchargecounties ALTER COLUMN id SET DEFAULT nextval('users_inchargecounties_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY users_mfluser ALTER COLUMN id SET DEFAULT nextval('users_mfluser_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY users_mfluser_groups ALTER COLUMN id SET DEFAULT nextval('users_mfluser_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY users_mfluser_user_permissions ALTER COLUMN id SET DEFAULT nextval('users_mfluser_user_permissions_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add mfl user	2	add_mfluser
5	Can change mfl user	2	change_mfluser
6	Can delete mfl user	2	delete_mfluser
7	Can add permission	3	add_permission
8	Can change permission	3	change_permission
9	Can delete permission	3	delete_permission
10	Can add group	4	add_group
11	Can change group	4	change_group
12	Can delete group	4	delete_group
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add owner	7	add_owner
20	Can change owner	7	change_owner
21	Can delete owner	7	delete_owner
22	Can add service	8	add_service
23	Can change service	8	change_service
24	Can delete service	8	delete_service
25	Can add facility	9	add_facility
26	Can change facility	9	change_facility
27	Can delete facility	9	delete_facility
31	Can add contact	11	add_contact
32	Can change contact	11	change_contact
33	Can delete contact	11	delete_contact
34	Can add province	12	add_province
35	Can change province	12	change_province
36	Can delete province	12	delete_province
37	Can add county	13	add_county
38	Can change county	13	change_county
39	Can delete county	13	delete_county
40	Can add constituency	14	add_constituency
41	Can change constituency	14	change_constituency
42	Can delete constituency	14	delete_constituency
43	Can add district	15	add_district
44	Can change district	15	change_district
45	Can delete district	15	delete_district
46	Can add division	16	add_division
47	Can change division	16	change_division
48	Can delete division	16	delete_division
49	Can add location	17	add_location
50	Can change location	17	change_location
51	Can delete location	17	delete_location
52	Can add sub location	18	add_sublocation
53	Can change sub location	18	change_sublocation
54	Can delete sub location	18	delete_sublocation
55	Can add Feedback from users	19	add_feedback
56	Can change Feedback from users	19	change_feedback
57	Can delete Feedback from users	19	delete_feedback
58	Can add role	20	add_role
59	Can change role	20	change_role
60	Can delete role	20	delete_role
61	Can add user roles	21	add_userroles
62	Can change user roles	21	change_userroles
63	Can delete user roles	21	delete_userroles
64	Can add permission	22	add_permission
65	Can change permission	22	change_permission
66	Can delete permission	22	delete_permission
67	Can add role permissions	23	add_rolepermissions
68	Can change role permissions	23	change_rolepermissions
69	Can delete role permissions	23	delete_rolepermissions
73	Can add incharge counties	25	add_inchargecounties
74	Can change incharge counties	25	change_inchargecounties
75	Can delete incharge counties	25	delete_inchargecounties
\.


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('auth_permission_id_seq', 75, true);


--
-- Data for Name: common_constituency; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY common_constituency (id, created, updated, name, code, county_id, created_by_id, updated_by_id) FROM stdin;
1	2015-04-01 17:59:36+03	2015-04-01 17:59:36+03	Limuru	4	2	5	5
\.


--
-- Name: common_constituency_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('common_constituency_id_seq', 1, true);


--
-- Data for Name: common_contact; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY common_contact (id, created, updated, email, town, postal_code, address, nearest_town, landline, mobile, created_by_id, updated_by_id) FROM stdin;
1	2015-04-02 15:00:38.501834+03	2015-04-02 15:00:38.501849+03	tom@jelly.com	Kaimu	900	679	Old town	083259	0716458286	1	1
\.


--
-- Name: common_contact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('common_contact_id_seq', 1, true);


--
-- Data for Name: common_county; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY common_county (id, created, updated, name, code, "Province_id", created_by_id, updated_by_id) FROM stdin;
1	2015-04-01 17:56:50+03	2015-04-01 17:56:50+03	Nairobi	2	\N	5	5
2	2015-04-01 17:57:10+03	2015-04-01 17:57:10+03	Kiambu	7	\N	5	5
\.


--
-- Name: common_county_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('common_county_id_seq', 2, true);


--
-- Data for Name: common_district; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY common_district (id, created, updated, name, code, county_id, created_by_id, province_id, updated_by_id) FROM stdin;
1	2015-04-01 17:59:02+03	2015-04-01 17:59:02+03	Kiambu East	2	2	5	\N	5
\.


--
-- Name: common_district_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('common_district_id_seq', 1, true);


--
-- Data for Name: common_division; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY common_division (id, created, updated, name, code, constituency_id, created_by_id, district_id, updated_by_id) FROM stdin;
1	2015-04-01 17:58:43+03	2015-04-01 17:58:43+03	Kiambu East	2	1	5	1	5
\.


--
-- Name: common_division_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('common_division_id_seq', 1, true);


--
-- Data for Name: common_feedback; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY common_feedback (id, name, job, email, subjet, comment) FROM stdin;
\.


--
-- Name: common_feedback_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('common_feedback_id_seq', 1, false);


--
-- Data for Name: common_location; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY common_location (id, created, updated, name, code, created_by_id, division_id, updated_by_id) FROM stdin;
1	2015-04-01 18:00:04+03	2015-04-01 18:00:04+03	Nyanza	2	5	1	5
\.


--
-- Name: common_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('common_location_id_seq', 1, true);


--
-- Data for Name: common_province; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY common_province (id, created, updated, name, code, created_by_id, updated_by_id) FROM stdin;
1	2015-04-01 17:55:09+03	2015-04-01 17:55:09+03	Coast	2	5	5
2	2015-04-01 17:55:34+03	2015-04-01 17:55:34+03	Nairobi	3	5	5
3	2015-04-01 17:55:42+03	2015-04-01 17:55:42+03	Nyanza	4	5	5
4	2015-04-01 17:55:51+03	2015-04-01 17:55:51+03	Western	5	5	5
\.


--
-- Name: common_province_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('common_province_id_seq', 4, true);


--
-- Data for Name: common_sublocation; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY common_sublocation (id, created, updated, name, code, created_by_id, location_id, updated_by_id) FROM stdin;
2	2015-04-02 13:13:00.717386+03	2015-04-02 13:13:00.717402+03	asf	asf	1	1	1
3	2015-04-02 13:13:38.108154+03	2015-04-02 13:13:38.10817+03	afsf	asff	1	1	1
5	2015-04-02 13:14:37.270626+03	2015-04-02 13:14:37.270639+03	afesf	aswegff	1	1	1
6	2015-04-02 13:27:57.936421+03	2015-04-02 13:27:57.936435+03	444	5444	1	1	1
7	2015-04-02 13:28:08.171611+03	2015-04-02 13:28:08.171622+03	4f44	54f44	1	1	1
1	2015-04-01 18:00:30+03	2015-04-01 18:00:30+03	Teikun Royal	4	5	1	5
\.


--
-- Name: common_sublocation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('common_sublocation_id_seq', 7, true);


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2015-04-01 17:55:34.563084+03	1	Coast	1		12	5
2	2015-04-01 17:55:42.599172+03	2	Nairobi	1		12	5
3	2015-04-01 17:55:51.355227+03	3	Nyanza	1		12	5
4	2015-04-01 17:56:11.365793+03	4	Western	1		12	5
5	2015-04-01 17:57:10.162514+03	1	Nairobi	1		13	5
6	2015-04-01 17:57:25.190291+03	2	Kiambu	1		13	5
7	2015-04-01 17:59:28.347706+03	1	Kiambu East	1		15	5
8	2015-04-01 17:59:54.82974+03	1	Limuru	1		14	5
9	2015-04-01 17:59:57.141001+03	1	Kiambu East	1		16	5
10	2015-04-01 18:00:24.788802+03	1	Nyanza	1		17	5
11	2015-04-01 18:00:44.571794+03	1	Teikun	1		18	5
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 11, true);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	users	mfluser
3	auth	permission
4	auth	group
5	contenttypes	contenttype
6	sessions	session
7	facilities	owner
8	facilities	service
9	facilities	facility
11	common	contact
12	common	province
13	common	county
14	common	constituency
15	common	district
16	common	division
17	common	location
18	common	sublocation
19	common	feedback
20	roles	role
21	roles	userroles
22	roles	permission
23	roles	rolepermissions
25	users	inchargecounties
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('django_content_type_id_seq', 25, true);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2015-04-01 17:50:21.781104+03
2	contenttypes	0002_remove_content_type_name	2015-04-01 17:50:21.813741+03
3	auth	0001_initial	2015-04-01 17:50:22.402921+03
4	auth	0002_alter_permission_name_max_length	2015-04-01 17:50:22.437523+03
5	auth	0003_alter_user_email_max_length	2015-04-01 17:50:22.464995+03
6	auth	0004_alter_user_username_opts	2015-04-01 17:50:22.488245+03
7	auth	0005_alter_user_last_login_null	2015-04-01 17:50:22.509395+03
8	auth	0006_require_contenttypes_0002	2015-04-01 17:50:22.514471+03
9	users	0001_initial	2015-04-01 17:50:23.370593+03
10	admin	0001_initial	2015-04-01 17:50:24.960494+03
11	common	0001_initial	2015-04-01 17:50:28.988339+03
12	facilities	0001_initial	2015-04-01 17:50:30.656626+03
13	roles	0001_initial	2015-04-01 17:50:31.246489+03
14	sessions	0001_initial	2015-04-01 17:50:31.503414+03
15	roles	0002_permission_rolepermissions	2015-04-02 11:48:42.714456+03
16	users	0002_auto_20150402_1135	2015-04-02 14:35:28.583207+03
17	users	0003_auto_20150402_1159	2015-04-02 14:59:31.892063+03
18	roles	0003_auto_20150402_1252	2015-04-02 15:52:46.492715+03
19	users	0004_auto_20150402_1252	2015-04-02 15:52:47.098998+03
20	roles	0004_auto_20150402_1256	2015-04-02 15:57:11.433037+03
21	roles	0005_auto_20150402_1318	2015-04-02 16:19:41.156451+03
22	users	0005_mfluser_is_national	2015-04-02 16:21:59.017408+03
23	facilities	0002_auto_20150402_1400	2015-04-02 17:00:35.977778+03
\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('django_migrations_id_seq', 23, true);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
vmre9h2ysfog9f8yf5q1ftehhct8wbdp	NzJmNTk0NmQzNzMzOTFmNmVhZTIzZjc4ZWNhZDNiOTI5NDllYTFiNDp7Il9hdXRoX3VzZXJfaGFzaCI6IjllNGE3OTkwMDYyY2VlYjRmYWU0YzMxZTVmZjc4YTA1NjNmNmFiZWUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI1In0=	2015-04-15 17:54:56.190218+03
i7ee0zaugvhp35glfks88chk298aha6s	NTYzMzMwNTkxOGVlYWRhYmQ4NTNhNDkwZjg0NWNkOTA2MTFiZjhjNzp7Il9hdXRoX3VzZXJfaGFzaCI6ImZlYjJlMzhlNmM2MjY5OTNlNDEyYzU5YjUzZTFlNzBiNWM0ZTdjNjQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=	2015-04-16 16:53:10.247574+03
\.


--
-- Data for Name: facilities_facility; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY facilities_facility (id, created, updated, name, code, latitude, longitude, is_classified, description, facility_type, number_of_beds, number_of_cots, open_whole_day, open_whole_week, status, created_by_id, owner_id, sub_location_id, updated_by_id) FROM stdin;
1	2015-04-02 17:00:37.971271+03	2015-04-02 17:00:37.971293+03	nairobi womens hosp	aslfjk	ajal	afj	t	sdfak	DISPENSARY	10	10	f	f	OPERATIONAL	1	1	1	1
2	2015-04-02 17:15:47.043323+03	2015-04-02 17:15:47.043335+03	asfas	aslfjkc	ajal	afj	t	sdfak	DISPENSARY	10	10	f	f	OPERATIONAL	1	1	1	1
3	2015-04-02 17:20:37.756409+03	2015-04-02 17:20:37.756421+03	nairobi womevns hosp	aslvfjk	ajal	afj	t	sdfak	DISPENSARY	10	10	f	f	OPERATIONAL	1	1	1	1
4	2015-04-02 17:25:22.184046+03	2015-04-02 17:25:22.184057+03	nairffobi womevns hosp	ffff	ajal	afj	t	sdfak	DISPENSARY	10	10	f	f	OPERATIONAL	1	1	1	1
5	2015-04-02 17:27:18.088921+03	2015-04-02 17:27:18.08893+03	naddrobi womevns hosp	aslvddfjk	ajal	afj	t	sdfak	DISPENSARY	10	10	f	f	OPERATIONAL	1	1	1	1
6	2015-04-02 17:28:45.67482+03	2015-04-02 17:28:45.674834+03	naddrobi womevns hdbosp	aslvdsdfdfjk	ajal	afj	t	sdfak	DISPENSARY	10	10	f	f	OPERATIONAL	1	1	1	1
7	2015-04-02 17:31:22.511365+03	2015-04-02 17:31:22.511388+03	naddrobi womevns hdcbosp	aslvdscdfdfjk	ajal	afj	t	sdfak	DISPENSARY	10	10	f	f	OPERATIONAL	1	1	1	1
8	2015-04-02 17:31:59.432324+03	2015-04-02 17:31:59.432336+03	naddrobi womevns hdcbospvv	aslvdsvvcdfdfjk	ajal	afj	t	sdfak	DISPENSARY	10	10	f	f	OPERATIONAL	1	1	1	1
\.


--
-- Name: facilities_facility_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('facilities_facility_id_seq', 8, true);


--
-- Data for Name: facilities_facility_services; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY facilities_facility_services (id, facility_id, service_id) FROM stdin;
1	3	1
2	6	2
3	7	3
4	8	4
\.


--
-- Name: facilities_facility_services_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('facilities_facility_services_id_seq', 4, true);


--
-- Data for Name: facilities_owner; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY facilities_owner (id, created, updated, name, description, code, created_by_id, updated_by_id) FROM stdin;
1	2015-04-02 16:55:13.410039+03	2015-04-02 16:55:13.410055+03	MOH	MOH	MOH	1	1
\.


--
-- Name: facilities_owner_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('facilities_owner_id_seq', 1, true);


--
-- Data for Name: facilities_service; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY facilities_service (id, created, updated, name, description, code, created_by_id, updated_by_id) FROM stdin;
1	2015-04-02 16:56:30.48247+03	2015-04-02 16:56:30.482494+03	Diabetes	Diabetes	DIA	1	1
2	2015-04-02 17:28:45.67482+03	2015-04-02 17:28:45.674834+03	Diabetes	Diabetes	DIA	1	1
3	2015-04-02 17:31:22.511365+03	2015-04-02 17:31:22.511388+03	Diabetes	Diabetes	DIA	1	1
4	2015-04-02 17:31:59.432324+03	2015-04-02 17:31:59.432336+03	Diabetes	Diabetes	DIA	1	1
\.


--
-- Name: facilities_service_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('facilities_service_id_seq', 4, true);


--
-- Data for Name: roles_permission; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY roles_permission (id, created, updated, name, description, created_by_id, updated_by_id) FROM stdin;
1	2015-04-02 15:46:59.080047+03	2015-04-02 15:46:59.080065+03	adfha	asfajk	1	1
\.


--
-- Name: roles_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('roles_permission_id_seq', 1, true);


--
-- Data for Name: roles_role; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY roles_role (id, created, updated, name, description, code, created_by_id, updated_by_id) FROM stdin;
1	2015-04-02 15:45:55.771578+03	2015-04-02 15:45:55.771593+03	sub county list	asfjk	ff	1	1
\.


--
-- Name: roles_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('roles_role_id_seq', 1, true);


--
-- Data for Name: roles_rolepermissions; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY roles_rolepermissions (id, created, updated, created_by_id, permission_id, role_id, updated_by_id) FROM stdin;
1	2015-04-02 15:47:36.859199+03	2015-04-02 15:47:36.859209+03	1	1	1	1
\.


--
-- Name: roles_rolepermissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('roles_rolepermissions_id_seq', 2, true);


--
-- Data for Name: roles_userroles; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY roles_userroles (id, created, updated, created_by_id, role_id, updated_by_id, user_id) FROM stdin;
1	2015-04-02 15:48:21.347839+03	2015-04-02 15:48:21.347856+03	1	1	1	1
\.


--
-- Name: roles_userroles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('roles_userroles_id_seq', 1, true);


--
-- Data for Name: users_inchargecounties; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY users_inchargecounties (id, created, updated, is_active, county_id, created_by_id, updated_by_id, user_id) FROM stdin;
1	2015-04-02 14:56:40.805426+03	2015-04-02 14:56:40.805446+03	t	1	1	1	5
\.


--
-- Name: users_inchargecounties_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('users_inchargecounties_id_seq', 1, true);


--
-- Data for Name: users_mfluser; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY users_mfluser (id, password, last_login, is_superuser, email, first_name, last_name, other_names, username, is_staff, is_active, date_joined, is_incharge, contact_id, county_id, is_national) FROM stdin;
4	pbkdf2_sha256$20000$GJGLqAv49tKl$jRXQvKjdIVGUhkEMrEZaHJbD6bI3ykgRowL8hHjlyro=	2015-04-01 17:54:09.5344+03	f	marika2@gmail.com	marikas			marikas	f	t	2015-04-01 17:54:09.5344+03	f	\N	\N	f
5	pbkdf2_sha256$20000$Wiei9F0mhoKQ$H53/1smlTEfXV0y6nljwcfufBCDhIlNyZLzxgjn+b1E=	2015-04-01 17:54:56.176038+03	t	marika1@gmail.com	marika1			marika1	t	t	2015-04-01 17:54:28.264403+03	f	\N	\N	f
6	brian	\N	f	brianmarika@gmail.com	marikas	mwaura	bm	brianmarika	f	t	2015-04-02 14:44:26.563977+03	f	\N	\N	f
1	pbkdf2_sha256$20000$Ze8KX0ZDBuLV$QvgwyJ51/wCuUTShnGN07GaqRu7wGCdQsgYA8NcJ0qo=	2015-04-02 16:53:10.235542+03	f	marika.rian@gmail.com	marika			marika	f	t	2015-04-01 17:52:05.834859+03	f	1	1	t
\.


--
-- Data for Name: users_mfluser_groups; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY users_mfluser_groups (id, mfluser_id, group_id) FROM stdin;
\.


--
-- Name: users_mfluser_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('users_mfluser_groups_id_seq', 1, false);


--
-- Name: users_mfluser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('users_mfluser_id_seq', 6, true);


--
-- Data for Name: users_mfluser_user_permissions; Type: TABLE DATA; Schema: public; Owner: mfl
--

COPY users_mfluser_user_permissions (id, mfluser_id, permission_id) FROM stdin;
\.


--
-- Name: users_mfluser_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mfl
--

SELECT pg_catalog.setval('users_mfluser_user_permissions_id_seq', 1, false);


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: common_constituency_code_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_constituency
    ADD CONSTRAINT common_constituency_code_key UNIQUE (code);


--
-- Name: common_constituency_name_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_constituency
    ADD CONSTRAINT common_constituency_name_key UNIQUE (name);


--
-- Name: common_constituency_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_constituency
    ADD CONSTRAINT common_constituency_pkey PRIMARY KEY (id);


--
-- Name: common_contact_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_contact
    ADD CONSTRAINT common_contact_pkey PRIMARY KEY (id);


--
-- Name: common_county_code_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_county
    ADD CONSTRAINT common_county_code_key UNIQUE (code);


--
-- Name: common_county_name_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_county
    ADD CONSTRAINT common_county_name_key UNIQUE (name);


--
-- Name: common_county_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_county
    ADD CONSTRAINT common_county_pkey PRIMARY KEY (id);


--
-- Name: common_district_code_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_district
    ADD CONSTRAINT common_district_code_key UNIQUE (code);


--
-- Name: common_district_name_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_district
    ADD CONSTRAINT common_district_name_key UNIQUE (name);


--
-- Name: common_district_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_district
    ADD CONSTRAINT common_district_pkey PRIMARY KEY (id);


--
-- Name: common_division_code_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_division
    ADD CONSTRAINT common_division_code_key UNIQUE (code);


--
-- Name: common_division_name_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_division
    ADD CONSTRAINT common_division_name_key UNIQUE (name);


--
-- Name: common_division_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_division
    ADD CONSTRAINT common_division_pkey PRIMARY KEY (id);


--
-- Name: common_feedback_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_feedback
    ADD CONSTRAINT common_feedback_pkey PRIMARY KEY (id);


--
-- Name: common_location_code_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_location
    ADD CONSTRAINT common_location_code_key UNIQUE (code);


--
-- Name: common_location_name_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_location
    ADD CONSTRAINT common_location_name_key UNIQUE (name);


--
-- Name: common_location_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_location
    ADD CONSTRAINT common_location_pkey PRIMARY KEY (id);


--
-- Name: common_province_code_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_province
    ADD CONSTRAINT common_province_code_key UNIQUE (code);


--
-- Name: common_province_name_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_province
    ADD CONSTRAINT common_province_name_key UNIQUE (name);


--
-- Name: common_province_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_province
    ADD CONSTRAINT common_province_pkey PRIMARY KEY (id);


--
-- Name: common_sublocation_code_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_sublocation
    ADD CONSTRAINT common_sublocation_code_key UNIQUE (code);


--
-- Name: common_sublocation_name_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_sublocation
    ADD CONSTRAINT common_sublocation_name_key UNIQUE (name);


--
-- Name: common_sublocation_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY common_sublocation
    ADD CONSTRAINT common_sublocation_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_45f3b1d93ec8c61c_uniq; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_45f3b1d93ec8c61c_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: facilities_facility_code_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY facilities_facility
    ADD CONSTRAINT facilities_facility_code_key UNIQUE (code);


--
-- Name: facilities_facility_name_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY facilities_facility
    ADD CONSTRAINT facilities_facility_name_key UNIQUE (name);


--
-- Name: facilities_facility_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY facilities_facility
    ADD CONSTRAINT facilities_facility_pkey PRIMARY KEY (id);


--
-- Name: facilities_facility_services_facility_id_service_id_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY facilities_facility_services
    ADD CONSTRAINT facilities_facility_services_facility_id_service_id_key UNIQUE (facility_id, service_id);


--
-- Name: facilities_facility_services_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY facilities_facility_services
    ADD CONSTRAINT facilities_facility_services_pkey PRIMARY KEY (id);


--
-- Name: facilities_owner_name_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY facilities_owner
    ADD CONSTRAINT facilities_owner_name_key UNIQUE (name);


--
-- Name: facilities_owner_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY facilities_owner
    ADD CONSTRAINT facilities_owner_pkey PRIMARY KEY (id);


--
-- Name: facilities_service_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY facilities_service
    ADD CONSTRAINT facilities_service_pkey PRIMARY KEY (id);


--
-- Name: roles_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY roles_permission
    ADD CONSTRAINT roles_permission_pkey PRIMARY KEY (id);


--
-- Name: roles_role_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY roles_role
    ADD CONSTRAINT roles_role_pkey PRIMARY KEY (id);


--
-- Name: roles_rolepermissions_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY roles_rolepermissions
    ADD CONSTRAINT roles_rolepermissions_pkey PRIMARY KEY (id);


--
-- Name: roles_rolepermissions_role_id_4183d7cfcfaf066_uniq; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY roles_rolepermissions
    ADD CONSTRAINT roles_rolepermissions_role_id_4183d7cfcfaf066_uniq UNIQUE (role_id, permission_id);


--
-- Name: roles_userroles_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY roles_userroles
    ADD CONSTRAINT roles_userroles_pkey PRIMARY KEY (id);


--
-- Name: users_inchargecounties_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY users_inchargecounties
    ADD CONSTRAINT users_inchargecounties_pkey PRIMARY KEY (id);


--
-- Name: users_mfluser_email_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY users_mfluser
    ADD CONSTRAINT users_mfluser_email_key UNIQUE (email);


--
-- Name: users_mfluser_groups_mfluser_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY users_mfluser_groups
    ADD CONSTRAINT users_mfluser_groups_mfluser_id_group_id_key UNIQUE (mfluser_id, group_id);


--
-- Name: users_mfluser_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY users_mfluser_groups
    ADD CONSTRAINT users_mfluser_groups_pkey PRIMARY KEY (id);


--
-- Name: users_mfluser_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY users_mfluser
    ADD CONSTRAINT users_mfluser_pkey PRIMARY KEY (id);


--
-- Name: users_mfluser_user_permissions_mfluser_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY users_mfluser_user_permissions
    ADD CONSTRAINT users_mfluser_user_permissions_mfluser_id_permission_id_key UNIQUE (mfluser_id, permission_id);


--
-- Name: users_mfluser_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY users_mfluser_user_permissions
    ADD CONSTRAINT users_mfluser_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: users_mfluser_username_key; Type: CONSTRAINT; Schema: public; Owner: mfl; Tablespace: 
--

ALTER TABLE ONLY users_mfluser
    ADD CONSTRAINT users_mfluser_username_key UNIQUE (username);


--
-- Name: auth_group_name_253ae2a6331666e8_like; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX auth_group_name_253ae2a6331666e8_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- Name: common_constituency_9ccf0ba6; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_constituency_9ccf0ba6 ON common_constituency USING btree (updated_by_id);


--
-- Name: common_constituency_code_1f10603c4f66d571_like; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_constituency_code_1f10603c4f66d571_like ON common_constituency USING btree (code varchar_pattern_ops);


--
-- Name: common_constituency_d19428be; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_constituency_d19428be ON common_constituency USING btree (county_id);


--
-- Name: common_constituency_e93cb7eb; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_constituency_e93cb7eb ON common_constituency USING btree (created_by_id);


--
-- Name: common_constituency_name_aa922c28156171d_like; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_constituency_name_aa922c28156171d_like ON common_constituency USING btree (name varchar_pattern_ops);


--
-- Name: common_contact_9ccf0ba6; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_contact_9ccf0ba6 ON common_contact USING btree (updated_by_id);


--
-- Name: common_contact_e93cb7eb; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_contact_e93cb7eb ON common_contact USING btree (created_by_id);


--
-- Name: common_county_9ccf0ba6; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_county_9ccf0ba6 ON common_county USING btree (updated_by_id);


--
-- Name: common_county_a9309f29; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_county_a9309f29 ON common_county USING btree ("Province_id");


--
-- Name: common_county_code_7cad7422992f0379_like; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_county_code_7cad7422992f0379_like ON common_county USING btree (code varchar_pattern_ops);


--
-- Name: common_county_e93cb7eb; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_county_e93cb7eb ON common_county USING btree (created_by_id);


--
-- Name: common_county_name_28ac62bb869ec26d_like; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_county_name_28ac62bb869ec26d_like ON common_county USING btree (name varchar_pattern_ops);


--
-- Name: common_district_4a5754ed; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_district_4a5754ed ON common_district USING btree (province_id);


--
-- Name: common_district_9ccf0ba6; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_district_9ccf0ba6 ON common_district USING btree (updated_by_id);


--
-- Name: common_district_code_4dc201546e9a3977_like; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_district_code_4dc201546e9a3977_like ON common_district USING btree (code varchar_pattern_ops);


--
-- Name: common_district_d19428be; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_district_d19428be ON common_district USING btree (county_id);


--
-- Name: common_district_e93cb7eb; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_district_e93cb7eb ON common_district USING btree (created_by_id);


--
-- Name: common_district_name_4920e97771165fb_like; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_district_name_4920e97771165fb_like ON common_district USING btree (name varchar_pattern_ops);


--
-- Name: common_division_721b30ed; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_division_721b30ed ON common_division USING btree (constituency_id);


--
-- Name: common_division_9ccf0ba6; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_division_9ccf0ba6 ON common_division USING btree (updated_by_id);


--
-- Name: common_division_a34a99d3; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_division_a34a99d3 ON common_division USING btree (district_id);


--
-- Name: common_division_code_501976dd18a9c41a_like; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_division_code_501976dd18a9c41a_like ON common_division USING btree (code varchar_pattern_ops);


--
-- Name: common_division_e93cb7eb; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_division_e93cb7eb ON common_division USING btree (created_by_id);


--
-- Name: common_division_name_1379e8dbb09e778c_like; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_division_name_1379e8dbb09e778c_like ON common_division USING btree (name varchar_pattern_ops);


--
-- Name: common_location_9ccf0ba6; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_location_9ccf0ba6 ON common_location USING btree (updated_by_id);


--
-- Name: common_location_9ff3405c; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_location_9ff3405c ON common_location USING btree (division_id);


--
-- Name: common_location_code_2641e4badc54b216_like; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_location_code_2641e4badc54b216_like ON common_location USING btree (code varchar_pattern_ops);


--
-- Name: common_location_e93cb7eb; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_location_e93cb7eb ON common_location USING btree (created_by_id);


--
-- Name: common_location_name_1cd5ded0b6c5b8b8_like; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_location_name_1cd5ded0b6c5b8b8_like ON common_location USING btree (name varchar_pattern_ops);


--
-- Name: common_province_9ccf0ba6; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_province_9ccf0ba6 ON common_province USING btree (updated_by_id);


--
-- Name: common_province_code_68a90fedf5b5edff_like; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_province_code_68a90fedf5b5edff_like ON common_province USING btree (code varchar_pattern_ops);


--
-- Name: common_province_e93cb7eb; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_province_e93cb7eb ON common_province USING btree (created_by_id);


--
-- Name: common_province_name_a501345c2b18725_like; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_province_name_a501345c2b18725_like ON common_province USING btree (name varchar_pattern_ops);


--
-- Name: common_sublocation_9ccf0ba6; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_sublocation_9ccf0ba6 ON common_sublocation USING btree (updated_by_id);


--
-- Name: common_sublocation_code_138eeb11d23141c9_like; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_sublocation_code_138eeb11d23141c9_like ON common_sublocation USING btree (code varchar_pattern_ops);


--
-- Name: common_sublocation_e274a5da; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_sublocation_e274a5da ON common_sublocation USING btree (location_id);


--
-- Name: common_sublocation_e93cb7eb; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_sublocation_e93cb7eb ON common_sublocation USING btree (created_by_id);


--
-- Name: common_sublocation_name_5f6de9fc0d8bcfbb_like; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX common_sublocation_name_5f6de9fc0d8bcfbb_like ON common_sublocation USING btree (name varchar_pattern_ops);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX django_session_de54fa62 ON django_session USING btree (expire_date);


--
-- Name: django_session_session_key_461cfeaa630ca218_like; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX django_session_session_key_461cfeaa630ca218_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: facilities_facility_5e7b1936; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX facilities_facility_5e7b1936 ON facilities_facility USING btree (owner_id);


--
-- Name: facilities_facility_9ccf0ba6; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX facilities_facility_9ccf0ba6 ON facilities_facility USING btree (updated_by_id);


--
-- Name: facilities_facility_badcf0a1; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX facilities_facility_badcf0a1 ON facilities_facility USING btree (sub_location_id);


--
-- Name: facilities_facility_code_3c3b33344edb02b8_like; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX facilities_facility_code_3c3b33344edb02b8_like ON facilities_facility USING btree (code varchar_pattern_ops);


--
-- Name: facilities_facility_e93cb7eb; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX facilities_facility_e93cb7eb ON facilities_facility USING btree (created_by_id);


--
-- Name: facilities_facility_name_28415b4ba13317fa_like; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX facilities_facility_name_28415b4ba13317fa_like ON facilities_facility USING btree (name varchar_pattern_ops);


--
-- Name: facilities_facility_services_b0dc1e29; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX facilities_facility_services_b0dc1e29 ON facilities_facility_services USING btree (service_id);


--
-- Name: facilities_facility_services_e32a5395; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX facilities_facility_services_e32a5395 ON facilities_facility_services USING btree (facility_id);


--
-- Name: facilities_owner_9ccf0ba6; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX facilities_owner_9ccf0ba6 ON facilities_owner USING btree (updated_by_id);


--
-- Name: facilities_owner_e93cb7eb; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX facilities_owner_e93cb7eb ON facilities_owner USING btree (created_by_id);


--
-- Name: facilities_owner_name_1c780feb471e7173_like; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX facilities_owner_name_1c780feb471e7173_like ON facilities_owner USING btree (name varchar_pattern_ops);


--
-- Name: facilities_service_9ccf0ba6; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX facilities_service_9ccf0ba6 ON facilities_service USING btree (updated_by_id);


--
-- Name: facilities_service_e93cb7eb; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX facilities_service_e93cb7eb ON facilities_service USING btree (created_by_id);


--
-- Name: roles_permission_9ccf0ba6; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX roles_permission_9ccf0ba6 ON roles_permission USING btree (updated_by_id);


--
-- Name: roles_permission_e93cb7eb; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX roles_permission_e93cb7eb ON roles_permission USING btree (created_by_id);


--
-- Name: roles_role_9ccf0ba6; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX roles_role_9ccf0ba6 ON roles_role USING btree (updated_by_id);


--
-- Name: roles_role_e93cb7eb; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX roles_role_e93cb7eb ON roles_role USING btree (created_by_id);


--
-- Name: roles_rolepermissions_8373b171; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX roles_rolepermissions_8373b171 ON roles_rolepermissions USING btree (permission_id);


--
-- Name: roles_rolepermissions_84566833; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX roles_rolepermissions_84566833 ON roles_rolepermissions USING btree (role_id);


--
-- Name: roles_rolepermissions_9ccf0ba6; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX roles_rolepermissions_9ccf0ba6 ON roles_rolepermissions USING btree (updated_by_id);


--
-- Name: roles_rolepermissions_e93cb7eb; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX roles_rolepermissions_e93cb7eb ON roles_rolepermissions USING btree (created_by_id);


--
-- Name: roles_userroles_84566833; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX roles_userroles_84566833 ON roles_userroles USING btree (role_id);


--
-- Name: roles_userroles_9ccf0ba6; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX roles_userroles_9ccf0ba6 ON roles_userroles USING btree (updated_by_id);


--
-- Name: roles_userroles_e8701ad4; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX roles_userroles_e8701ad4 ON roles_userroles USING btree (user_id);


--
-- Name: roles_userroles_e93cb7eb; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX roles_userroles_e93cb7eb ON roles_userroles USING btree (created_by_id);


--
-- Name: users_inchargecounties_9ccf0ba6; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX users_inchargecounties_9ccf0ba6 ON users_inchargecounties USING btree (updated_by_id);


--
-- Name: users_inchargecounties_d19428be; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX users_inchargecounties_d19428be ON users_inchargecounties USING btree (county_id);


--
-- Name: users_inchargecounties_e8701ad4; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX users_inchargecounties_e8701ad4 ON users_inchargecounties USING btree (user_id);


--
-- Name: users_inchargecounties_e93cb7eb; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX users_inchargecounties_e93cb7eb ON users_inchargecounties USING btree (created_by_id);


--
-- Name: users_mfluser_6d82f13d; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX users_mfluser_6d82f13d ON users_mfluser USING btree (contact_id);


--
-- Name: users_mfluser_d19428be; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX users_mfluser_d19428be ON users_mfluser USING btree (county_id);


--
-- Name: users_mfluser_email_315db9f556d7d6b2_like; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX users_mfluser_email_315db9f556d7d6b2_like ON users_mfluser USING btree (email varchar_pattern_ops);


--
-- Name: users_mfluser_groups_0e939a4f; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX users_mfluser_groups_0e939a4f ON users_mfluser_groups USING btree (group_id);


--
-- Name: users_mfluser_groups_23e3a42e; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX users_mfluser_groups_23e3a42e ON users_mfluser_groups USING btree (mfluser_id);


--
-- Name: users_mfluser_user_permissions_23e3a42e; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX users_mfluser_user_permissions_23e3a42e ON users_mfluser_user_permissions USING btree (mfluser_id);


--
-- Name: users_mfluser_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX users_mfluser_user_permissions_8373b171 ON users_mfluser_user_permissions USING btree (permission_id);


--
-- Name: users_mfluser_username_27fdd41e42f169e1_like; Type: INDEX; Schema: public; Owner: mfl; Tablespace: 
--

CREATE INDEX users_mfluser_username_27fdd41e42f169e1_like ON users_mfluser USING btree (username varchar_pattern_ops);


--
-- Name: auth_content_type_id_508cf46651277a81_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_content_type_id_508cf46651277a81_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissio_group_id_689710a9a73b7457_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_group_id_689710a9a73b7457_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: comm_constituency_id_795a4922d5904e70_fk_common_constituency_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_division
    ADD CONSTRAINT comm_constituency_id_795a4922d5904e70_fk_common_constituency_id FOREIGN KEY (constituency_id) REFERENCES common_constituency(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_const_created_by_id_2f92de12c6cd0abf_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_constituency
    ADD CONSTRAINT common_const_created_by_id_2f92de12c6cd0abf_fk_users_mfluser_id FOREIGN KEY (created_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_const_updated_by_id_5e21fab60bf7a930_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_constituency
    ADD CONSTRAINT common_const_updated_by_id_5e21fab60bf7a930_fk_users_mfluser_id FOREIGN KEY (updated_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_constitue_county_id_59bee06356043e4d_fk_common_county_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_constituency
    ADD CONSTRAINT common_constitue_county_id_59bee06356043e4d_fk_common_county_id FOREIGN KEY (county_id) REFERENCES common_county(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_conta_created_by_id_4742f420ccde64e8_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_contact
    ADD CONSTRAINT common_conta_created_by_id_4742f420ccde64e8_fk_users_mfluser_id FOREIGN KEY (created_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_conta_updated_by_id_6487ab3d15911ac9_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_contact
    ADD CONSTRAINT common_conta_updated_by_id_6487ab3d15911ac9_fk_users_mfluser_id FOREIGN KEY (updated_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_count_Province_id_55978edf1b36f711_fk_common_province_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_county
    ADD CONSTRAINT "common_count_Province_id_55978edf1b36f711_fk_common_province_id" FOREIGN KEY ("Province_id") REFERENCES common_province(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_count_created_by_id_33d5ce969b039c57_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_county
    ADD CONSTRAINT common_count_created_by_id_33d5ce969b039c57_fk_users_mfluser_id FOREIGN KEY (created_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_count_updated_by_id_7defde02d36b2f1a_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_county
    ADD CONSTRAINT common_count_updated_by_id_7defde02d36b2f1a_fk_users_mfluser_id FOREIGN KEY (updated_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_distr_created_by_id_12d3cfb2f0b619a7_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_district
    ADD CONSTRAINT common_distr_created_by_id_12d3cfb2f0b619a7_fk_users_mfluser_id FOREIGN KEY (created_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_distr_province_id_1ada859471465701_fk_common_province_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_district
    ADD CONSTRAINT common_distr_province_id_1ada859471465701_fk_common_province_id FOREIGN KEY (province_id) REFERENCES common_province(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_distr_updated_by_id_4a144765d15c3e48_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_district
    ADD CONSTRAINT common_distr_updated_by_id_4a144765d15c3e48_fk_users_mfluser_id FOREIGN KEY (updated_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_district_county_id_264c81c5f8a02f65_fk_common_county_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_district
    ADD CONSTRAINT common_district_county_id_264c81c5f8a02f65_fk_common_county_id FOREIGN KEY (county_id) REFERENCES common_county(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_divis_created_by_id_78368ea69148ff98_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_division
    ADD CONSTRAINT common_divis_created_by_id_78368ea69148ff98_fk_users_mfluser_id FOREIGN KEY (created_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_divis_updated_by_id_63dde2ec04a35787_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_division
    ADD CONSTRAINT common_divis_updated_by_id_63dde2ec04a35787_fk_users_mfluser_id FOREIGN KEY (updated_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_divisi_district_id_37f77493cb8100c_fk_common_district_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_division
    ADD CONSTRAINT common_divisi_district_id_37f77493cb8100c_fk_common_district_id FOREIGN KEY (district_id) REFERENCES common_district(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_locat_created_by_id_3e5e6f894e41b754_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_location
    ADD CONSTRAINT common_locat_created_by_id_3e5e6f894e41b754_fk_users_mfluser_id FOREIGN KEY (created_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_locat_division_id_2625839fcfdff27f_fk_common_division_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_location
    ADD CONSTRAINT common_locat_division_id_2625839fcfdff27f_fk_common_division_id FOREIGN KEY (division_id) REFERENCES common_division(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_locat_updated_by_id_3b52ae4823080cfb_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_location
    ADD CONSTRAINT common_locat_updated_by_id_3b52ae4823080cfb_fk_users_mfluser_id FOREIGN KEY (updated_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_provi_created_by_id_2d08fed6d0c5f231_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_province
    ADD CONSTRAINT common_provi_created_by_id_2d08fed6d0c5f231_fk_users_mfluser_id FOREIGN KEY (created_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_provi_updated_by_id_1ac164aa4222cc92_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_province
    ADD CONSTRAINT common_provi_updated_by_id_1ac164aa4222cc92_fk_users_mfluser_id FOREIGN KEY (updated_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_sublo_created_by_id_788a318de1041e67_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_sublocation
    ADD CONSTRAINT common_sublo_created_by_id_788a318de1041e67_fk_users_mfluser_id FOREIGN KEY (created_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_sublo_location_id_3d16522281f6f3f0_fk_common_location_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_sublocation
    ADD CONSTRAINT common_sublo_location_id_3d16522281f6f3f0_fk_common_location_id FOREIGN KEY (location_id) REFERENCES common_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_subloc_updated_by_id_7a1ae4b3a0a8188_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY common_sublocation
    ADD CONSTRAINT common_subloc_updated_by_id_7a1ae4b3a0a8188_fk_users_mfluser_id FOREIGN KEY (updated_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djan_content_type_id_697914295151027a_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT djan_content_type_id_697914295151027a_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_52fdd58701c5f563_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_52fdd58701c5f563_fk_users_mfluser_id FOREIGN KEY (user_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: facil_sub_location_id_503f17b983a7ed64_fk_common_sublocation_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY facilities_facility
    ADD CONSTRAINT facil_sub_location_id_503f17b983a7ed64_fk_common_sublocation_id FOREIGN KEY (sub_location_id) REFERENCES common_sublocation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: faciliti_facility_id_3d4d7aade261a067_fk_facilities_facility_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY facilities_facility_services
    ADD CONSTRAINT faciliti_facility_id_3d4d7aade261a067_fk_facilities_facility_id FOREIGN KEY (facility_id) REFERENCES facilities_facility(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: facilities_f_created_by_id_4a654b445dba3e36_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY facilities_facility
    ADD CONSTRAINT facilities_f_created_by_id_4a654b445dba3e36_fk_users_mfluser_id FOREIGN KEY (created_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: facilities_f_updated_by_id_7a8303fbec1e9099_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY facilities_facility
    ADD CONSTRAINT facilities_f_updated_by_id_7a8303fbec1e9099_fk_users_mfluser_id FOREIGN KEY (updated_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: facilities_faci_owner_id_e79db9206af15c4_fk_facilities_owner_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY facilities_facility
    ADD CONSTRAINT facilities_faci_owner_id_e79db9206af15c4_fk_facilities_owner_id FOREIGN KEY (owner_id) REFERENCES facilities_owner(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: facilities_o_created_by_id_5e62318aece21d51_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY facilities_owner
    ADD CONSTRAINT facilities_o_created_by_id_5e62318aece21d51_fk_users_mfluser_id FOREIGN KEY (created_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: facilities_o_updated_by_id_1a1e44b9f443c9a0_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY facilities_owner
    ADD CONSTRAINT facilities_o_updated_by_id_1a1e44b9f443c9a0_fk_users_mfluser_id FOREIGN KEY (updated_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: facilities_s_created_by_id_7e8fcd913cc3cced_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY facilities_service
    ADD CONSTRAINT facilities_s_created_by_id_7e8fcd913cc3cced_fk_users_mfluser_id FOREIGN KEY (created_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: facilities_s_updated_by_id_696a3d7c6b7f628a_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY facilities_service
    ADD CONSTRAINT facilities_s_updated_by_id_696a3d7c6b7f628a_fk_users_mfluser_id FOREIGN KEY (updated_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: facilities_service_id_458a8a3c829f933c_fk_facilities_service_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY facilities_facility_services
    ADD CONSTRAINT facilities_service_id_458a8a3c829f933c_fk_facilities_service_id FOREIGN KEY (service_id) REFERENCES facilities_service(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: roles_permis_created_by_id_642f810c31c23d61_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY roles_permission
    ADD CONSTRAINT roles_permis_created_by_id_642f810c31c23d61_fk_users_mfluser_id FOREIGN KEY (created_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: roles_permiss_updated_by_id_3ae93a6fa1c0ab0_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY roles_permission
    ADD CONSTRAINT roles_permiss_updated_by_id_3ae93a6fa1c0ab0_fk_users_mfluser_id FOREIGN KEY (updated_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: roles_rol_permission_id_22e9b8dac20f8106_fk_roles_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY roles_rolepermissions
    ADD CONSTRAINT roles_rol_permission_id_22e9b8dac20f8106_fk_roles_permission_id FOREIGN KEY (permission_id) REFERENCES roles_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: roles_role_created_by_id_5af6ba1bea0ddd44_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY roles_role
    ADD CONSTRAINT roles_role_created_by_id_5af6ba1bea0ddd44_fk_users_mfluser_id FOREIGN KEY (created_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: roles_role_updated_by_id_228bca41137a56cd_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY roles_role
    ADD CONSTRAINT roles_role_updated_by_id_228bca41137a56cd_fk_users_mfluser_id FOREIGN KEY (updated_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: roles_rolepe_created_by_id_442edf68265a0533_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY roles_rolepermissions
    ADD CONSTRAINT roles_rolepe_created_by_id_442edf68265a0533_fk_users_mfluser_id FOREIGN KEY (created_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: roles_rolepe_updated_by_id_230fb2c22bb3f144_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY roles_rolepermissions
    ADD CONSTRAINT roles_rolepe_updated_by_id_230fb2c22bb3f144_fk_users_mfluser_id FOREIGN KEY (updated_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: roles_rolepermissions_role_id_6bdb3c93582a822f_fk_roles_role_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY roles_rolepermissions
    ADD CONSTRAINT roles_rolepermissions_role_id_6bdb3c93582a822f_fk_roles_role_id FOREIGN KEY (role_id) REFERENCES roles_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: roles_userro_created_by_id_4f51d03d107e0881_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY roles_userroles
    ADD CONSTRAINT roles_userro_created_by_id_4f51d03d107e0881_fk_users_mfluser_id FOREIGN KEY (created_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: roles_userro_updated_by_id_255bfc0a6dbaca1e_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY roles_userroles
    ADD CONSTRAINT roles_userro_updated_by_id_255bfc0a6dbaca1e_fk_users_mfluser_id FOREIGN KEY (updated_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: roles_userroles_role_id_2e3e2aac88fc39c3_fk_roles_role_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY roles_userroles
    ADD CONSTRAINT roles_userroles_role_id_2e3e2aac88fc39c3_fk_roles_role_id FOREIGN KEY (role_id) REFERENCES roles_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: roles_userroles_user_id_61d523501c441db2_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY roles_userroles
    ADD CONSTRAINT roles_userroles_user_id_61d523501c441db2_fk_users_mfluser_id FOREIGN KEY (user_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_inchar_created_by_id_64f8a00a1fc12532_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY users_inchargecounties
    ADD CONSTRAINT users_inchar_created_by_id_64f8a00a1fc12532_fk_users_mfluser_id FOREIGN KEY (created_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_inchar_updated_by_id_53a0c25f77c9066f_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY users_inchargecounties
    ADD CONSTRAINT users_inchar_updated_by_id_53a0c25f77c9066f_fk_users_mfluser_id FOREIGN KEY (updated_by_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_inchargeco_county_id_1c29d7c09dba1974_fk_common_county_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY users_inchargecounties
    ADD CONSTRAINT users_inchargeco_county_id_1c29d7c09dba1974_fk_common_county_id FOREIGN KEY (county_id) REFERENCES common_county(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_inchargecount_user_id_5e9bff1097b26ff_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY users_inchargecounties
    ADD CONSTRAINT users_inchargecount_user_id_5e9bff1097b26ff_fk_users_mfluser_id FOREIGN KEY (user_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_mflu_permission_id_29700e6653e8b3a3_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY users_mfluser_user_permissions
    ADD CONSTRAINT users_mflu_permission_id_29700e6653e8b3a3_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_mfluser_contact_id_5adb1182d28fc075_fk_common_contact_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY users_mfluser
    ADD CONSTRAINT users_mfluser_contact_id_5adb1182d28fc075_fk_common_contact_id FOREIGN KEY (contact_id) REFERENCES common_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_mfluser_county_id_1fb76a68adf3cdc0_fk_common_county_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY users_mfluser
    ADD CONSTRAINT users_mfluser_county_id_1fb76a68adf3cdc0_fk_common_county_id FOREIGN KEY (county_id) REFERENCES common_county(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_mfluser_g_mfluser_id_69d27377dc80c821_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY users_mfluser_groups
    ADD CONSTRAINT users_mfluser_g_mfluser_id_69d27377dc80c821_fk_users_mfluser_id FOREIGN KEY (mfluser_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_mfluser_groups_group_id_582fb9b474b49ae0_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY users_mfluser_groups
    ADD CONSTRAINT users_mfluser_groups_group_id_582fb9b474b49ae0_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_mfluser_u_mfluser_id_696a5a4e507dcf09_fk_users_mfluser_id; Type: FK CONSTRAINT; Schema: public; Owner: mfl
--

ALTER TABLE ONLY users_mfluser_user_permissions
    ADD CONSTRAINT users_mfluser_u_mfluser_id_696a5a4e507dcf09_fk_users_mfluser_id FOREIGN KEY (mfluser_id) REFERENCES users_mfluser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--


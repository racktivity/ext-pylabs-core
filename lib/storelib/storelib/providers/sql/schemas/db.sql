--
-- PostgreSQL database dump
--

-- Started on 2011-04-05 13:58:42 EET

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

--
-- TOC entry 304 (class 2612 OID 50521)
-- Name: plpgsql; Type: PROCEDURAL LANGUAGE; Schema: -; Owner: -
--

CREATE PROCEDURAL LANGUAGE plpgsql;


SET search_path = public, pg_catalog;

--
-- TOC entry 19 (class 1255 OID 50686)
-- Dependencies: 304 3
-- Name: get_grouped_range(text[], integer, integer, integer, character varying); Type: FUNCTION; Schema: public; Owner: -
--
CREATE OR REPLACE FUNCTION store_create(storeid varchar(128)) RETURNS void as $$
BEGIN
	EXECUTE 'CREATE SCHEMA "' || storeid || '";';
	EXECUTE 'CREATE TABLE "' || storeid || '"."values" ("timestamp" integer, "value" numeric);';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION store_exists(storeid varchar(128)) RETURNS integer as $$
DECLARE
	e int;
BEGIN
	SELECT count(storeid) INTO e from pg_tables where schemaname = storeid;
	RETURN e;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION store_destroy(storeid varchar(128)) RETURNS void as $$
BEGIN
	IF store_exists(storeid) > 0 THEN
		EXECUTE 'DROP SCHEMA "' || storeid || '" CASCADE;';
	END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION store_save(storeid varchar(128), t integer, v numeric) RETURNS void as $$
BEGIN
	EXECUTE 'INSERT INTO "' || storeid || '"."values" values ($1, $2)'
		USING t, v;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION store_get(storeid varchar(128), t integer) RETURNS numeric as $$
DECLARE
	v numeric;
BEGIN
	EXECUTE 'SELECT avg("value") from "' || storeid || '"."values" where "timestamp" = $1'
		INTO v USING t;
	RETURN v;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION store_get_between(storeid varchar(128), starttime integer, endtime integer, func varchar(10)) RETURNS numeric as $$
DECLARE
	v numeric;
BEGIN
	EXECUTE 'SELECT ' || func || '("value") from "' || storeid || '"."values" where "timestamp" >= $1 and "timestamp" <= $2'
		INTO v USING starttime, endtime;
	RETURN v;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_grouped_range(dsids text[], resolution integer, starttime integer, endtime integer, groupfunction character varying) RETURNS SETOF record
    LANGUAGE plpgsql
    AS $_$
DECLARE
	array_len int;
	dsid text;

	sql text;
	startt integer;
	endt integer;
	rangeend integer;

	aggregatedvalue numeric;
	data record;
	boundries record;
BEGIN
	/*
	sql := 'SELECT min("timestamp"), max("timestamp") FROM "' || dsid || '"."values"';
	EXECUTE sql INTO boundries;
	
	IF starttime < boundries.min THEN
		startt := boundries.min;
	ELSE
		startt := starttime;
	END IF;
	IF endtime > boundries.max THEN
		endt := boundries.max;
	ELSE
		endt := endtime;
	END IF;
	*/
	startt := starttime;
	endt := endtime;
	array_len := array_upper(dsids, 1);

	WHILE startt < endt + resolution LOOP
		rangeend := startt + resolution;
		aggregatedvalue := NULL;
		FOR i IN 1 .. array_len LOOP
			dsid := dsids[i];
			sql := 'select 0 as "timestamp", avg("value") as "value" from "' || dsid || '"."values" where "timestamp" >= $1 and "timestamp" < $2';
			EXECUTE sql INTO data USING startt, rangeend;
			
			IF data.value IS NULL THEN
				CONTINUE;
			ELSEIF aggregatedvalue IS NULL THEN
				aggregatedvalue = data.value;
				CONTINUE;
			END IF;
			
			CASE groupfunction
				WHEN 'add' THEN
					raise notice 'Adding %, %', aggregatedvalue , data.value;
					aggregatedvalue := aggregatedvalue + data.value;
				WHEN 'avg' THEN
					aggregatedvalue := (aggregatedvalue + data.value) / 2;
				WHEN 'min' THEN
					aggregatedvalue := numeric_smaller(aggregatedvalue, data.value);
				WHEN 'max' THEN
					aggregatedvalue := numeric_larger(aggregatedvalue, data.value);
			END CASE;
			
		END LOOP;
		data.timestamp := startt;
		data.value = aggregatedvalue;
		return next data;
		startt := rangeend;
	END LOOP;
	RETURN;
END;
$_$;


--
-- TOC entry 20 (class 1255 OID 50687)
-- Dependencies: 3 304
-- Name: get_range(character varying, integer, integer, integer, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE OR REPLACE FUNCTION get_range(dsid character varying, resolution integer, starttime integer, endtime integer, aggregationfunction character varying) RETURNS SETOF record
    LANGUAGE plpgsql
    AS $_$
DECLARE
	sql text;
	-- aggrgvalue numeric;
	
	startt integer;
	endt integer;
	rangeend integer;
	
	data record;
	boundries record;
BEGIN
	/*
	sql := 'SELECT min("timestamp"), max("timestamp") FROM "' || dsid || '"."values"';
	EXECUTE sql INTO boundries;
	
	IF starttime < boundries.min THEN
		startt := boundries.min;
	ELSE
		startt := starttime;
	END IF;
	IF endtime > boundries.max THEN
		endt := boundries.max;
	ELSE
		endt := endtime;
	END IF;
	*/
	startt := starttime;
	endt := endtime;
	
	WHILE startt < endt + resolution LOOP
		rangeend := startt + resolution;
		sql := 'select 0 as "timestamp", ' || aggregationfunction || '("value") as "value" from "' || dsid || '"."values" where "timestamp" >= $1 and "timestamp" < $2';
		-- raise notice 'Statement: % (%,%)', sql, startt, rangeend;
		EXECUTE sql INTO data USING startt, rangeend;
		data.timestamp := startt;
		return next data;
		startt := rangeend;
	END LOOP;
	RETURN;
END;
$_$;


-- Function: get_grouped_latest(text[], integer, character varying)

-- DROP FUNCTION get_grouped_latest(text[], integer, character varying);

CREATE OR REPLACE FUNCTION get_grouped_latest(dsids text[], now_time integer, groupfunction character varying)
  RETURNS SETOF record 
  LANGUAGE plpgsql
  AS $_$
DECLARE
	sql text;
	startt integer;
	aggregatedvalue numeric;
	data record;
	boundries record;
	array_len int;
	dsid text;
BEGIN

	array_len := array_upper(dsids, 1);
	startt := now_time;
	aggregatedvalue := NULL;
	FOR i IN 1 .. array_len LOOP
		dsid := dsids[i];
		sql := 'select 0 as "timestamp", avg("value") as "value" from "' || dsid || '"."values" where "timestamp" = $1';
		EXECUTE sql INTO data USING startt;
			
		IF data.value IS NULL THEN
			CONTINUE;
		ELSEIF aggregatedvalue IS NULL THEN
			aggregatedvalue = data.value;
			CONTINUE;
		END IF;
			
		CASE groupfunction
			WHEN 'add' THEN
				raise notice 'Adding %, %', aggregatedvalue , data.value;
				aggregatedvalue := aggregatedvalue + data.value;
			WHEN 'avg' THEN
				aggregatedvalue := (aggregatedvalue + data.value) / 2;
			WHEN 'min' THEN
				aggregatedvalue := numeric_smaller(aggregatedvalue, data.value);
			WHEN 'max' THEN
				aggregatedvalue := numeric_larger(aggregatedvalue, data.value);
			END CASE;
			
	END LOOP;
	data.timestamp := now();
	data.value = aggregatedvalue;
	return next data;
	RETURN;
END;
$_$;

--
-- TOC entry 1772 (class 0 OID 0)
-- Dependencies: 3
-- Name: public; Type: ACL; Schema: -; Owner: -
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2011-04-05 13:58:42 EET

--
-- PostgreSQL database dump complete
--


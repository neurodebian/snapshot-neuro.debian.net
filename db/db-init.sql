REVOKE ALL ON DATABASE "snapshotdb" FROM public;
GRANT ALL ON DATABASE "snapshotdb" TO "snapshot";
GRANT CONNECT, TEMPORARY ON DATABASE "snapshotdb" TO PUBLIC;

REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO "snapshot";
GRANT USAGE ON SCHEMA public TO PUBLIC;


-- next, create the debversion types:
\i /usr/share/postgresql/8.4/contrib/debversion.sql

-- and the perl language
CREATE LANGUAGE plperl;
CREATE LANGUAGE plpgsql;

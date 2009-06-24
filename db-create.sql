-- ####################################################################
-- the filesystem
-- ####################################################################
CREATE TABLE archive (
	archive_id	SERIAL	PRIMARY KEY,
	name		VARCHAR(80)	NOT NULL,
	UNIQUE(name)
);

CREATE TABLE mirrorrun (
	mirrorrun_id	SERIAL		PRIMARY KEY,
	archive_id	INTEGER		NOT NULL REFERENCES archive(archive_id),
	run		TIMESTAMP	NOT NULL
);

CREATE TABLE node (
	node_id		SERIAL		PRIMARY KEY,
	parent		INTEGER		NOT NULL,
	first		INTEGER		NOT NULL REFERENCES mirrorrun(mirrorrun_id),
	last		INTEGER		NOT NULL REFERENCES mirrorrun(mirrorrun_id)
);
-- FIXME: add a trigger that checks that first->archive_id == last->archive_id

CREATE VIEW node_with_ts AS
	SELECT node_id,
	       parent,
	       first_run.run AS first_run,
	       first_run.archive_id,
	       last_run.run AS last_run
	FROM node,
	     (SELECT * FROM mirrorrun) AS first_run,
	     (SELECT * FROM mirrorrun) AS last_run
	WHERE first_run.mirrorrun_id=node.first
	  AND last_run.mirrorrun_id=node.last;


CREATE TABLE directory (
	directory_id	SERIAL		PRIMARY KEY,
	path		VARCHAR(250)	NOT NULL,
	node_id		INTEGER		REFERENCES node(node_id)
);

ALTER TABLE node ADD FOREIGN KEY (parent) REFERENCES directory(directory_id) DEFERRABLE INITIALLY DEFERRED;

CREATE TABLE file (
	file_id		SERIAL		PRIMARY KEY,
	name		VARCHAR(128)	NOT NULL,
	size		INTEGER		NOT NULL,
	hash		CHAR(40)	NOT NULL,
	node_id		INTEGER		REFERENCES node(node_id)
);

CREATE TABLE symlink (
	symlink_id	SERIAL		PRIMARY KEY,
	name		VARCHAR(128)	NOT NULL,
	target		VARCHAR(250)	NOT NULL,
	node_id		INTEGER		REFERENCES node(node_id)
);


CREATE INDEX node_idx_parent ON node(parent);
CREATE INDEX directory_idx_path ON directory(path);
CREATE INDEX file_idx_name ON file(name);
CREATE INDEX file_idx_node_id ON file(node_id);
CREATE INDEX symlink_idx_name ON symlink(name);



CREATE TYPE readdir_result AS (filetype char, name VARCHAR(128), node_id INTEGER, digest CHAR(40));
CREATE OR REPLACE FUNCTION readdir(in_directory VARCHAR, in_mirrorrun_id integer) RETURNS SETOF readdir_result AS $$
DECLARE
	mirrorrun_run timestamp;
	dir_id integer;
	arc_id integer;
BEGIN
	SELECT run, archive_id INTO mirrorrun_run, arc_id FROM mirrorrun WHERE mirrorrun_id = in_mirrorrun_id;
	SELECT directory_id INTO dir_id
	   FROM directory JOIN node_with_ts ON directory.node_id = node_with_ts.node_id
	   WHERE path=in_directory
	     AND node_with_ts.archive_id = arc_id
	     AND first_run <= mirrorrun_run
	     AND last_run  >= mirrorrun_run;
	RETURN QUERY
		SELECT 'd'::CHAR, substring(path, '[^/]*$')::VARCHAR(128), node_with_ts.node_id, NULL
		  FROM directory NATURAL JOIN node_with_ts
		  WHERE parent=dir_id
		    AND directory_id <> parent
		    AND first_run <= mirrorrun_run
		    AND last_run  >= mirrorrun_run
		UNION ALL
		SELECT '-'::CHAR, name, node_with_ts.node_id, file.hash
		  FROM file NATURAL JOIN node_with_ts
		  WHERE parent=dir_id
		    AND first_run <= mirrorrun_run
		    AND last_run  >= mirrorrun_run
		UNION ALL
		SELECT 'l'::CHAR, name, node_with_ts.node_id, NULL
		  FROM symlink NATURAL JOIN node_with_ts
		  WHERE parent=dir_id
		    AND first_run <= mirrorrun_run
		    AND last_run  >= mirrorrun_run;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_file_from_mirrorrun_with_path(in_mirrorrun_id integer, in_directory VARCHAR, in_filename VARCHAR) RETURNS CHAR(40) AS $$
DECLARE
	mirrorrun_run timestamp;
	dir_id integer;
	arc_id integer;
	result_hash CHAR(40);
BEGIN
	SELECT run, archive_id INTO mirrorrun_run, arc_id FROM mirrorrun WHERE mirrorrun_id = in_mirrorrun_id;
	SELECT directory_id INTO dir_id
	   FROM directory JOIN node_with_ts ON directory.node_id = node_with_ts.node_id
	   WHERE path=in_directory
	     AND node_with_ts.archive_id = arc_id
	     AND first_run <= mirrorrun_run
	     AND last_run  >= mirrorrun_run;
	SELECT hash INTO result_hash
		  FROM file JOIN node_with_ts ON file.node_id = node_with_ts.node_id
		  WHERE parent=dir_id
			AND first_run <= mirrorrun_run
			AND last_run  >= mirrorrun_run
			AND name = in_filename;
	RETURN result_hash;
END;
$$ LANGUAGE plpgsql;

-- returns a digest of a file with the given path,
-- but only if it was first seen in mirrorrun_id.
-- just existing in that mirrorrun is not sufficient.
CREATE OR REPLACE FUNCTION get_file_from_mirrorrun_with_path_first(in_mirrorrun_id integer, in_directory VARCHAR, in_filename VARCHAR) RETURNS CHAR(40) AS $$
DECLARE
	dir_id integer;
	result_hash CHAR(40);
BEGIN
	SELECT directory_id INTO dir_id
	   FROM directory JOIN node ON directory.node_id = node.node_id
	   WHERE path=in_directory
	     AND in_mirrorrun_id = node.first;
	SELECT hash INTO result_hash
		  FROM file JOIN node ON file.node_id = node.node_id
		  WHERE parent=dir_id
			AND in_mirrorrun_id = node.first
			AND name = in_filename;
	RETURN result_hash;
END;
$$ LANGUAGE plpgsql;




-- ####################################################################
-- packages
-- ####################################################################
CREATE TABLE indexed_mirrorrun (
	mirrorrun_id	INTEGER		PRIMARY KEY REFERENCES mirrorrun(mirrorrun_id),
	source		VARCHAR(10)
);

-- we try to keep the filesystem part independent from this
CREATE TABLE srcpkg (
	srcpkg_id	SERIAL		PRIMARY KEY,
	name		VARCHAR(128)	NOT NULL,
	version		DEBVERSION	NOT NULL
);
CREATE TABLE binpkg (
	binpkg_id	SERIAL		PRIMARY KEY,
	name		VARCHAR(128)	NOT NULL,
	version		DEBVERSION	NOT NULL,
	srcpkg_id	INTEGER		NOT NULL REFERENCES srcpkg(srcpkg_id)
);
CREATE INDEX srcpkg_idx_name ON srcpkg(name);
CREATE INDEX binpkg_idx_name ON binpkg(name);

CREATE TABLE file_srcpkg_mapping (
	srcpkg_id	INTEGER		NOT NULL REFERENCES srcpkg(srcpkg_id),
	-- hash is not unique, it might exist in different archives (e.g. archive.d.o and ftp.d.o)
	-- also, it cannot REFERENCES file(hash) since hash is not unique in the file table either
	hash		CHAR(40)	NOT NULL,
	UNIQUE(srcpkg_id, hash)
);
CREATE INDEX file_srcpkg_mapping_idx_srcpkg_id ON file_srcpkg_mapping(srcpkg_id);
CREATE INDEX file_srcpkg_mapping_idx_hash ON file_srcpkg_mapping(hash);

CREATE TABLE file_binpkg_mapping (
	binpkg_id	INTEGER		NOT NULL REFERENCES binpkg(binpkg_id),
	-- hash is not unique, it might exist in different archives (e.g. archive.d.o and ftp.d.o)
	-- also, it cannot REFERENCES file(hash) since hash is not unique in the file table either
	hash		CHAR(40)	NOT NULL,
	architecture	VARCHAR(16)	NOT NULL,
	UNIQUE(binpkg_id, hash)
);
CREATE INDEX file_binpkg_mapping_idx_binpkg_id ON file_binpkg_mapping(binpkg_id);
CREATE INDEX file_binpkg_mapping_idx_hash ON file_binpkg_mapping(hash);

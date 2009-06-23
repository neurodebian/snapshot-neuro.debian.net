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



-- proof of concept function
-- drop FUNCTION readdir (integer, timestamp);
-- CREATE FUNCTION readdir(p integer, ts timestamp) RETURNS SETOF VARCHAR(128) AS $$
-- BEGIN
--         RETURN QUERY
--                 SELECT substring(path, '[^/]*$')::VARCHAR(128) 
--                   FROM directory NATURAL JOIN node_with_ts
--                   WHERE parent=p
--                     AND directory_id <> parent
--                     AND first_run <= ts
--                     AND last_run  >= ts
--                 UNION ALL
--                 SELECT name 
--                   FROM file NATURAL JOIN node_with_ts
--                   WHERE parent=p
--                     AND first_run <= ts
--                     AND last_run  >= ts
--                 UNION ALL
--                 SELECT name
--                   FROM symlink NATURAL JOIN node_with_ts
--                   WHERE parent=p
--                     AND first_run <= ts
--                     AND last_run  >= ts;
-- END;
-- $$ LANGUAGE plpgsql;





-- ####################################################################
-- packages
-- ####################################################################
CREATE TABLE indexed_mirrorrun (
	mirrorrun_id	INTEGER		NOT NULL REFERENCES mirrorrun(mirrorrun_id),
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
	file_id		INTEGER		NOT NULL REFERENCES file(file_id),
	srcpkg_id	INTEGER		NOT NULL REFERENCES srcpkg(srcpkg_id),
	UNIQUE(file_id)
);
CREATE INDEX file_srcpkg_mapping_idx_srcpkg_id ON file_srcpkg_mapping(srcpkg_id);

CREATE TABLE file_binpkg_mapping (
	file_id		INTEGER		NOT NULL REFERENCES file(file_id),
	binpkg_id	INTEGER		NOT NULL REFERENCES binpkg(binpkg_id),
	architecture	VARCHAR(16)	NOT NULL,
	UNIQUE(file_id)
);
CREATE INDEX file_binpkg_mapping_idx_binpkg_id ON file_binpkg_mapping(binpkg_id);


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


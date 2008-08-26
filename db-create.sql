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

CREATE TABLE directory (
	directory_id	SERIAL		PRIMARY KEY,
	path		VARCHAR(250)	NOT NULL,
	node_id		INTEGER		REFERENCES node(node_id)
);

ALTER TABLE node ADD FOREIGN KEY (parent) REFERENCES directory(directory_id) DEFERRABLE INITIALLY DEFERRED;

CREATE TABLE file (
	file_id		SERIAL		PRIMARY KEY,
	name		VARCHAR(128)	NOT NULL,
	hash		CHAR(40)	NOT NULL,
	node_id		INTEGER		REFERENCES node(node_id)
);

CREATE TABLE symlink (
	symlink_id	SERIAL		PRIMARY KEY,
	name		VARCHAR(128)	NOT NULL,
	target		VARCHAR(250)	NOT NULL,
	node_id		INTEGER		REFERENCES node(node_id)
);

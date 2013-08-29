#!/usr/bin/python
#
# Copyright (c) 2009 Peter Palfrader
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

def upgrade(db):
    """Actually return symlink targets"""
    db.execute("""
        CREATE OR REPLACE FUNCTION dirtree(in_mirrorrun_id integer) RETURNS SETOF dirtree_result AS $$
        DECLARE
            mirrorrun_run timestamp;
            arc_id integer;
        BEGIN
            SELECT run, archive_id INTO mirrorrun_run, arc_id FROM mirrorrun WHERE mirrorrun_id = in_mirrorrun_id;
            RETURN QUERY
                WITH RECURSIVE

                subdirs(first, path, directory_id) AS
                ( SELECT node_with_ts.first, path, directory_id
                    FROM directory NATURAL JOIN node_with_ts
                    WHERE path='/'
                      AND first_run <= mirrorrun_run
                      AND last_run  >= mirrorrun_run
                      AND archive_id = arc_id
                UNION ALL
                  SELECT node_with_ts2.first, directory.path, directory.directory_id
                    FROM directory NATURAL JOIN node_with_ts2
                    JOIN subdirs ON node_with_ts2.parent = subdirs.directory_id
                    WHERE node_with_ts2.parent <> directory.directory_id
                      AND first_run <= mirrorrun_run
                      AND last_run  >= mirrorrun_run
                )

                SELECT first, NULL AS size, 'd'::CHAR AS filetype, path, NULL::VARCHAR(128) AS name, NULL::CHAR(40) AS hash, NULL::VARCHAR(250) AS target
                    FROM subdirs
                UNION ALL
                  SELECT node_with_ts2.first, size, '-'::CHAR, path, name, hash, NULL::VARCHAR(250) AS target
                     FROM file NATURAL JOIN node_with_ts2
                     JOIN subdirs ON subdirs.directory_id = node_with_ts2.parent
                   WHERE first_run <= mirrorrun_run
                     AND last_run  >= mirrorrun_run
                UNION ALL
                  SELECT node_with_ts2.first, NULL as size, 'l'::CHAR, path, name, NULL::CHAR(40) AS hash, target
                     FROM symlink NATURAL JOIN node_with_ts2
                     JOIN subdirs ON subdirs.directory_id = node_with_ts2.parent
                   WHERE first_run <= mirrorrun_run
                     AND last_run  >= mirrorrun_run
                ;
        END
        $$ LANGUAGE plpgsql;
        """)


    db.execute("UPDATE config SET value='15' WHERE name='db_revision' AND value='14'")

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

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
    # XXX sample sample sample XXX
    # XXX replace when you do the first real db change XXX
    pass
    #db.execute("DROP FUNCTION readdir(VARCHAR, INTEGER)")
    #db.execute("DROP TYPE readdir_result")
    #db.execute("""
    #    CREATE TYPE readdir_result AS (filetype char, name VARCHAR(128), node_id INTEGER, digest CHAR(40));
    #    """)
    #db.execute("""
    #    CREATE OR REPLACE FUNCTION readdir(in_directory VARCHAR, in_mirrorrun_id integer) RETURNS SETOF readdir_result AS $$
    #    DECLARE
    #        mirrorrun_run timestamp;
    #        dir_id integer;
    #        arc_id integer;
    #    BEGIN
    #        SELECT run, archive_id INTO mirrorrun_run, arc_id FROM mirrorrun WHERE mirrorrun_id = in_mirrorrun_id;
    #        SELECT directory_id INTO dir_id
    #           FROM directory JOIN node_with_ts ON directory.node_id = node_with_ts.node_id
    #           WHERE path=in_directory
    #             AND node_with_ts.archive_id = arc_id
    #             AND first_run <= mirrorrun_run
    #             AND last_run  >= mirrorrun_run;
    #        RETURN QUERY
    #            SELECT 'd'::CHAR, substring(path, '[^/]*$')::VARCHAR(128), node_with_ts.node_id, NULL
    #              FROM directory NATURAL JOIN node_with_ts
    #              WHERE parent=dir_id
    #                AND directory_id <> parent
    #                AND first_run <= mirrorrun_run
    #                AND last_run  >= mirrorrun_run
    #            UNION ALL
    #            SELECT '-'::CHAR, name, node_with_ts.node_id, file.hash
    #              FROM file NATURAL JOIN node_with_ts
    #              WHERE parent=dir_id
    #                AND first_run <= mirrorrun_run
    #                AND last_run  >= mirrorrun_run
    #            UNION ALL
    #            SELECT 'l'::CHAR, name, node_with_ts.node_id, NULL
    #              FROM symlink NATURAL JOIN node_with_ts
    #              WHERE parent=dir_id
    #                AND first_run <= mirrorrun_run
    #                AND last_run  >= mirrorrun_run;
    #    END;
    #    $$ LANGUAGE plpgsql;
    #    """)
    #
    #db.execute("UPDATE config SET value='2' WHERE name='db_revision' AND value='1'")

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

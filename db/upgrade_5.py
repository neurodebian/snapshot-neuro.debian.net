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
    """* Create a cheaper version of the node_with_ts view that
         does not pull in archive information.
       * Create get_file_from_path_at()
       * Drop get_file_from_mirrorrun_with_path()
       * Drop get_file_from_mirrorrun_with_path_first()"""
    db.execute("""
        CREATE VIEW node_with_ts2 AS
            SELECT *,
                (SELECT run FROM mirrorrun WHERE mirrorrun_id=node.first) AS first_run,
                (SELECT run FROM mirrorrun WHERE mirrorrun_id=node.last) AS last_run
            FROM node;
        """)
    db.execute('GRANT SELECT ON node_with_ts2 TO public')
    db.execute("""
        CREATE FUNCTION get_file_from_path_at(in_archive_id integer, in_run TIMESTAMP, in_directory VARCHAR, in_filename VARCHAR) RETURNS CHAR(40) AS $$
        DECLARE
                result_hash CHAR(40);
        BEGIN
                SELECT hash INTO result_hash
                          FROM file JOIN node_with_ts2 ON file.node_id = node_with_ts2.node_id

                          WHERE (SELECT path FROM directory WHERE directory.directory_id = node_with_ts2.parent) = in_directory
                                AND (SELECT archive_id FROM mirrorrun WHERE mirrorrun.mirrorrun_id = node_with_ts2.first) = in_archive_id
                                AND first_run <= in_run
                                AND last_run  >= in_run
                                AND name = in_filename;
                RETURN result_hash;
        END;
        $$ LANGUAGE plpgsql;
        """)

    db.execute('DROP FUNCTION get_file_from_mirrorrun_with_path (integer, character varying, character varying)')
    db.execute('DROP FUNCTION get_file_from_mirrorrun_with_path_first (integer, character varying, character varying)')

    db.execute("UPDATE config SET value='5' WHERE name='db_revision' AND value='4'")

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

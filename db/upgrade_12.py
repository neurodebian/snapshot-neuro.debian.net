#!/usr/bin/python
#
# Copyright (c) 2010 Peter Palfrader
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
    """Create removal logs"""

    db.execute("""
        CREATE TABLE removal_log (
            removal_log_id    SERIAL          PRIMARY KEY,
            when              TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
            reason            TEXT
        )
    """)
    db.execute("""
        CREATE TABLE removal_affects (
            removal_affects_id  SERIAL          PRIMARY KEY,
            removal_log_id      INTEGER         NOT NULL REFERENCES removal_log(removal_log_id),
            hash                CHAR(40)        NOT NULL
        )
    """)
    db.execute('GRANT SELECT ON removal_log TO public')
    db.execute('GRANT SELECT ON removal_affects TO public')
    db.execute("UPDATE config SET value='12' WHERE name='db_revision' AND value='11'")

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

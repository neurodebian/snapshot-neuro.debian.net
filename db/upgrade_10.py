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
    """Add a farm_journal table"""

    # This table can help with speeding up syncs of them farm, since we keep
    # track of which files we added since the last sync run.
    db.execute("""
        CREATE TABLE farm_journal (
            farm_journal_id   SERIAL          PRIMARY KEY,
            added             TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
            hash              CHAR(40)        NOT NULL
        )
    """)
    db.execute('CREATE INDEX farm_journal_idx_added ON farm_journal(added)')
    db.execute("UPDATE config SET value='10' WHERE name='db_revision' AND value='9'")

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

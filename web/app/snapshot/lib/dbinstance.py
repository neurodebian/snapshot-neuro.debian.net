## snapshot.debian.org - web frontend
#
# Copyright (c) 2009, 2010 Peter Palfrader
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

import psycopg2.extras
import time

class DBInstance:
    MAX_ERR = 10

    def __init__(self, pool):
        self.pool = pool
        self.conn = pool.getconn()

    def _reopen(self, delay=0.0):
        if not self.conn.closed:
            self.pool.putconn(self.conn, close=True)
        time.sleep(delay)
        self.conn = self.pool.getconn()

    def wrap(self, call, *args, **kw):
        delay = 0.0
        for i in xrange(0, self.MAX_ERR):
            try:
                return call(*args, **kw)
            except (psycopg2.OperationalError, psycopg2.InterfaceError):
                try:
                    self._reopen(delay)
                except:
                    pass
                delay += 0.1
        return call(*args, **kw)

    def _execute(self, *args, **kw):
        c = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        c.execute(*args, **kw)
        return c
    def _query(self, *args, **kw):
        c = self.execute(*args, **kw)
        rows = c.fetchall()
        c.close()
        return rows
    def _query_one(self, *args, **kw):
        all = self.query(*args, **kw)
        if len(all) > 1:
            raise 'Got more than one return in query_one'
        if len(all) == 0:
            return None
        return all[0]

    def execute(self, *args, **kw):
        return self.wrap(self._execute, *args, **kw)
    def query(self, *args, **kw):
        return self.wrap(self._query, *args, **kw)
    def query_one(self, *args, **kw):
        return self.wrap(self._query_one, *args, **kw)

    def close(self):
        try:
            self.execute('ROLLBACK').close()
            self.pool.putconn(self.conn)
        except (psycopg2.OperationalError, psycopg2.InterfaceError):
            if not self.conn.closed:
                self.pool.putconn(self.conn, close=True)

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

import psycopg2.extras

class DBInstance:
    def __init__(self, pool):
        self.pool = pool
        self.conn = pool.getconn()

    def execute(self, *args, **kw):
        c = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        c.execute(*args, **kw)
        return c

    def query(self, *args, **kw):
        c = self.execute(*args, **kw)
        rows = c.fetchall()
        c.close()
        return rows

    def close(self):
        self.execute('ROLLBACK').close()
        self.pool.putconn(self.conn)

    def query_one(self, *args, **kw):
        all = self.query(*args, **kw)
        if len(all) > 1:
            raise 'Got more than one return in query_one'
        if len(all) == 0:
            return None
        return all[0]

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

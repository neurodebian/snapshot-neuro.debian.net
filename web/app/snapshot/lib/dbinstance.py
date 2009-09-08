import psycopg2.extras

class DBInstance:
    def __init__(self, pool):
        self.conn = pool.connection()

    def execute(self, *args, **kw):
        c = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        c.execute(*args, **kw)
        return c

    def query(self, *args, **kw):
        c = self.execute(*args, **kw)
        rows = c.fetchall()
        c.close
        return rows

    def close(self):
        self.conn.close()

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

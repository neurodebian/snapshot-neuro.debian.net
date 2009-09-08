import logging
import psycopg2.extras

from snapshot.lib.base import *

log = logging.getLogger(__name__)

class RootController(BaseController):

    def index(self):
        # Return a rendered template
        #   return render('/some/template.mako')
        # or, Return a response
        conn = g.pool.connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        #cur = conn.cursor()
        cur.execute("SELECT name FROM archive ORDER BY name")
        c.rows = cur.fetchall()
        cur.close()
        conn.close()

        return render('/root.mako')

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

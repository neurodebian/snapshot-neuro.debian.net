import logging
from snapshot.lib.dbinstance import DBInstance
from snapshot.lib.base import *
import paste.httpexceptions

log = logging.getLogger(__name__)

class ArchiveController(BaseController):
    def root(self, environ):
        if environ['PATH_INFO'][-1:] == "/":
            return redirect_to("../")
        else:
            return redirect_to("../")

    def archive_base(self, environ, archive):
        db = DBInstance(g.pool)
        c.rows = db.query("""
            SELECT extract(year from run) AS year, extract(month from run) AS month
              FROM mirrorrun JOIN archive ON mirrorrun.archive_id=archive.archive_id
              WHERE archive.name=%(name)s
              GROUP BY year, month
              ORDER BY year, month""",
            { 'name': archive })
        db.close()

        if len(c.rows) == 0:
            e = paste.httpexceptions.HTTPNotFound()
            raise e

        return render('/archive.mako')

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

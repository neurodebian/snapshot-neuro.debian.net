import logging

from pylons import request, response, session, tmpl_context as c, g
from pylons.controllers.util import abort, redirect_to

from snapshot.lib.base import BaseController, render

from snapshot.lib.dbinstance import DBInstance

log = logging.getLogger(__name__)

class RootController(BaseController):
    def index(self):
        try:
            db = DBInstance(g.pool)
            c.names = g.shm.archives_get_list(db)
            c.srcstarts = g.shm.packages_get_name_starts()
            return render('/root.mako')
        finally:
            db.close()

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

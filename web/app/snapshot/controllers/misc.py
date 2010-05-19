import logging

from pylons import request, response, session, tmpl_context as c, g, config
from pylons.controllers.util import abort, redirect_to

from snapshot.lib.base import BaseController, render

from snapshot.lib.dbinstance import DBInstance
from snapshot.lib.control_helpers import *

log = logging.getLogger(__name__)

class MiscController(BaseController):
    def trace(self):
        db = None
        try:
            db = DBInstance(g.pool)
            set_expires(int(config['app_conf']['expires.root']))

            last = g.shm.get_last_mirrorrun(db)

            content = []
            content.append("%s\n"%(last.ctime()))
            content.append("# Above timestamp is timestamp of latest mirrrorrun\n")

            response.content_type = 'text/plain'
            return content
        finally:
            if not db is None: db.close()

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

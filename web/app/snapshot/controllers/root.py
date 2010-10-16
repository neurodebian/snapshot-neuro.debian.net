import logging

from pylons import request, response, session, tmpl_context as c, g, config
from pylons.controllers.util import abort, redirect_to

from snapshot.lib.base import BaseController, render

from snapshot.lib.dbinstance import DBInstance
from snapshot.lib.control_helpers import *

log = logging.getLogger(__name__)

class RootController(BaseController):
    def index(self):
        db = None
        try:
            db = DBInstance(g.pool)
            c.names = link_quote_array(g.shm.archives_get_list(db))
            c.srcstarts = link_quote_array(g.shm.packages_get_name_starts(db))
            c.binstarts = link_quote_array(g.shm.packages_get_name_starts(db, get_binary=True))
            set_expires(int(config['app_conf']['expires.root']))
            return render('/root-nd.mako')
        finally:
            if not db is None: db.close()


    def _build_crumbs(self, page=None):
        crumbs = []

        url = urllib.quote(request.environ.get('SCRIPT_NAME')) + "/"
        crumbs.append( { 'url': url, 'name': config['app_conf']['snapshot.domain'] });

        if not page is None:
            crumbs.append( { 'url': None, 'name': page, 'sep': '' });

        return crumbs


    def oldnews(self):
        set_expires(int(config['app_conf']['expires.root']))
        c.breadcrumbs = self._build_crumbs('older news')
        return render('/misc-oldnews-nd.mako')

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

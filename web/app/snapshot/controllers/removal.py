import logging

from pylons import request, response, session, tmpl_context as c, g, config
from pylons.controllers.util import abort, redirect_to, etag_cache

from snapshot.lib.base import BaseController, render

from snapshot.lib.dbinstance import DBInstance
from snapshot.lib.control_helpers import *
import os.path
import re
import urllib

log = logging.getLogger(__name__)

class RemovalController(BaseController):
    db = None

    def _db(self):
        if self.db is None:
            self.db = DBInstance(g.pool)
        return self.db

    def _db_close(self):
        if not self.db is None:
            self.db.close()

    def _build_crumbs(self, entry=None):
        crumbs = []

        url = urllib.quote(request.environ.get('SCRIPT_NAME')) + "/"
        crumbs.append( { 'url': url, 'name': 'snapshot.debian.org', 'sep': '|' });

        url += 'removal/'
        crumbs.append( { 'url': url, 'name': 'removal' });

        if not entry is None:
            entry=str(entry)
            url += urllib.quote(entry)
            crumbs.append( { 'url': url, 'name': entry, 'sep': '' });

        crumbs[-1]['url'] = None
        return crumbs

    def root(self):
        try:
            set_expires(int(config['app_conf']['expires.removal']))
            removals = g.shm.removal_get_list(self._db())

            c.removals = removals
            c.breadcrumbs = self._build_crumbs()
            return render('/removal-list.mako')
        finally:
            self._db_close()

    def one(self, id):
        try:
            try:
                id = int(id)
            except ValueError:
                abort(404, 'No such log')

            set_expires(int(config['app_conf']['expires.removal.one']))

            removal = g.shm.removal_get_one(self._db(), id)
            files = g.shm.removal_get_affected(self._db(), id)

            fileinfo = {}
            for hash in files:
                fileinfo[hash] = g.shm.packages_get_file_info(self._db(), hash)
            for hash in fileinfo:
                fileinfo[hash] = map(lambda fi: dict(fi), fileinfo[hash])
                for fi in fileinfo[hash]:
                    fi['dirlink'] = build_url_archive(fi['archive_name'], fi['run'], fi['path'])
                    fi['link'] = build_url_archive(fi['archive_name'], fi['run'], os.path.join(fi['path'], fi['name']), isadir=False )

            files.sort(key=lambda a: (fileinfo[a][0]['name'], a)) # reproducible file order

            c.removal = removal
            c.files = files
            c.fileinfo = fileinfo
            c.breadcrumbs = self._build_crumbs(id)
            c.title = 'Removal log #%d'%(id)
            return render('/removal-list-one.mako')
        finally:
            self._db_close()



# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

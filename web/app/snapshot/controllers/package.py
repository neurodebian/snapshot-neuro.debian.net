import logging

from pylons import request, response, session, tmpl_context as c, g
from pylons.controllers.util import abort, redirect_to

from snapshot.lib.base import BaseController, render

from snapshot.lib.dbinstance import DBInstance
from snapshot.lib.control_helpers import *
import os.path

log = logging.getLogger(__name__)

class PackageController(BaseController):
    db = None

    def _db(self):
        if self.db is None:
            self.db = DBInstance(g.pool)
        return self.db

    def _db_close(self):
        if not self.db is None:
            self.db.close()

    def _build_crumbs(self, srcpkg=None, version=None):
        crumbs = []

        url = request.environ.get('SCRIPT_NAME') + "/"
        crumbs.append( { 'url': url, 'name': 'snapshot.debian.org' });

        if srcpkg:
            url += 'package/' + srcpkg + '/'
            crumbs.append( { 'url': url, 'name': srcpkg });

            if version:
                url += version + '/'
                crumbs.append( { 'url': url, 'name': version });

        crumbs[-1]['url'] = None
        return crumbs

    def root(self):
        if not 'src' in request.params:
            return redirect_to("../")
        return redirect_to(unicode_encode(request.params['src'] + "/"))


    def source(self, source):
        try:
            sourceversions = g.shm.packages_get_source_versions(self._db(), source)

            if len(sourceversions) == 0:
                abort(404)

            c.src = source
            c.sourceversions = sourceversions
            c.breadcrumbs = self._build_crumbs(source)
            return render('/package-source.mako')
        finally:
            self._db_close()

    def source_version(self, source, version):
        try:
            sourcefiles = g.shm.packages_get_source_files(self._db(), source, version)
            if len(sourcefiles) == 0:
                # XXX maybe we have no sources but binaries?
                abort(404)

            binpkgs = g.shm.packages_get_binpkgs(self._db(), source, version)
            binpkgs = map(lambda b: { 'name':      b['name'],
                                      'version':   b['version'],
                                      'binpkg_id': b['binpkg_id'] }, binpkgs) # real dict, not psycopg2 thing
            binhashes = []
            for binpkg in binpkgs:
                binpkg['files'] = g.shm.packages_get_binary_files_from_id(self._db(), binpkg['binpkg_id'])
                binhashes += binpkg['files']

            fileinfo = {}
            for hash in sourcefiles + binhashes:
                fileinfo[hash] = g.shm.packages_get_file_info(self._db(), hash)
            for hash in fileinfo:
                fileinfo[hash] = map(lambda fi: dict(fi), fileinfo[hash]) # copy fileinfo into a real dict, not a psycopg2 pseudo dict
                for fi in fileinfo[hash]:
                    fi['dirlink'] = build_url_archive(fi['archive_name'], fi['run'], fi['path'])
                    fi['link'] = build_url_archive(fi['archive_name'], fi['run'], os.path.join(fi['path'], fi['name']), isadir=False )

            sourcefiles.sort(key=lambda a: (fileinfo[a][0]['name'], a)) # reproducible file order

            c.src = source
            c.version = version
            c.sourcefiles = sourcefiles
            c.binpkgs = binpkgs
            c.fileinfo = fileinfo
            c.breadcrumbs = self._build_crumbs(source, version)
            return render('/package-source-one.mako')
        finally:
            self._db_close()


# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

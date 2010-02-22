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

class PackageController(BaseController):
    db = None

    def _db(self):
        if self.db is None:
            self.db = DBInstance(g.pool)
        return self.db

    def _db_close(self):
        if not self.db is None:
            self.db.close()

    def _build_crumbs(self, srcpkg=None, version=None, start=None):
        crumbs = []

        url = urllib.quote(request.environ.get('SCRIPT_NAME')) + "/"
        crumbs.append( { 'url': url, 'name': 'snapshot.debian.org' });

        if not start:
            if srcpkg.startswith('lib') and len(srcpkg) >= 4:
                start = srcpkg[0:4]
            else:
                start = srcpkg[0:1]

        url += 'package/'
        crumbs.append( { 'url': url + '?cat=%s'%urllib.quote(start), 'name': start+'*' } )

        if not srcpkg is None:
            url += urllib.quote(srcpkg) + '/'
            crumbs.append( { 'url': url, 'name': srcpkg });

            if version:
                url += urllib.quote(version) + '/'
                crumbs.append( { 'url': url, 'name': version });

        crumbs[-1]['url'] = None
        return crumbs

    def root(self):
        if 'src' in request.params:
            return redirect_to(unicode_encode(request.params['src'] + "/"))
        elif 'cat' in request.params:
            try:
                #etag_cache( g.shm.packages_get_etag(self._db()) )
                set_expires(int(config['app_conf']['expires.package.root_cat']))

                start = request.params['cat']
                pkgs = g.shm.packages_get_name_starts_with(self._db(), start)
                if pkgs is None:
                    abort(404, 'No source packages in this category.')
                c.start = start
                c.packages = link_quote_array(pkgs)
                c.breadcrumbs = self._build_crumbs(start=start)
                c.title = '%s*'%(start)
                return render('/package-list-packages.mako')
            finally:
                self._db_close()
        else:
            return redirect_to("../")

    def source(self, source):
        try:
            #etag_cache( g.shm.packages_get_etag(self._db()) )
            set_expires(int(config['app_conf']['expires.package.source']))

            sourceversions = g.shm.packages_get_source_versions(self._db(), source)

            if len(sourceversions) == 0:
                abort(404, 'No such source package')

            c.src = source
            c.sourceversions = link_quote_array(sourceversions)
            c.breadcrumbs = self._build_crumbs(source)
            c.title = source
            return render('/package-source.mako')
        finally:
            self._db_close()

    def _attribute_escape(self, a):
        return re.sub('[^a-zA-Z0-9_.-]', lambda m: ':%x:'%(ord(m.group())), a)

    def source_version(self, source, version):
        try:
            #etag_cache( g.shm.packages_get_etag(self._db()) )
            set_expires(int(config['app_conf']['expires.package.source_version']))

            sourcefiles = g.shm.packages_get_source_files(self._db(), source, version)
            binpkgs = g.shm.packages_get_binpkgs(self._db(), source, version)

            # we may have binaries without sources.
            if len(sourcefiles) == 0 and len(binpkgs) == 0:
                abort(404, 'No source or binary packages foun')

            binpkgs = map(lambda b: { 'name':      b['name'],
                                      'version':   b['version'],
                                      'escaped_name': self._attribute_escape(b['name']),
                                      'escaped_version': self._attribute_escape(b['version']),
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
            c.title = '%s (%s)'%(source, version)
            return render('/package-source-one.mako')
        finally:
            self._db_close()


# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

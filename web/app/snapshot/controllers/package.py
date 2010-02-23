import logging

from pylons import request, response, session, tmpl_context as c, g, config
from pylons.controllers.util import abort, redirect_to, etag_cache

from snapshot.lib.base import BaseController, render

from snapshot.lib.dbinstance import DBInstance
from snapshot.lib.control_helpers import *
import os.path
import re
import urllib
from pylons.decorators import jsonify
#import simplejson

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
                abort(404, 'No source or binary packages found')

            binpkgs = map(lambda b: dict(b), binpkgs)
            binhashes = []
            for binpkg in binpkgs:
                binpkg['escaped_name'] = self._attribute_escape(binpkg['name'])
                binpkg['escaped_version'] = self._attribute_escape(binpkg['version'])
                binpkg['files'] = map(lambda x: x['hash'], g.shm.packages_get_binary_files_from_id(self._db(), binpkg['binpkg_id']))
                binhashes += binpkg['files']

            fileinfo = {}
            for hash in sourcefiles + binhashes:
                fileinfo[hash] = g.shm.packages_get_file_info(self._db(), hash)
            for hash in fileinfo:
                fileinfo[hash] = map(lambda fi: dict(fi), fileinfo[hash])
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





    def _get_fileinfo_for_mr(self, hashes):
        r = {}
        for hash in hashes:
            fileinfo = map(lambda x: dict(x), g.shm.packages_get_file_info(self._db(), hash))
            for fi in fileinfo:
                fi['run'] = rfc3339_timestamp(fi['run'])
            r[hash] = fileinfo
        return r

    @jsonify
    def mr_list(self):
        try:
            set_expires(int(config['app_conf']['expires.package.mr.list']))
            pkgs = g.shm.packages_get_all(self._db())
            return { '_comment': "foo",
                     'result': map(lambda x: { 'package': x }, pkgs) }
        finally:
            self._db_close()

    @jsonify
    def mr_source(self, source):
        try:
            set_expires(int(config['app_conf']['expires.package.mr.source']))
            sourceversions = g.shm.packages_get_source_versions(self._db(), source)
            if len(sourceversions) == 0: abort(404, 'No such source package')
            return { '_comment': "foo",
                     'package': source,
                     'result': map(lambda x: { 'version': x }, sourceversions) }
        finally:
            self._db_close()

    @jsonify
    def mr_source_version_srcfiles(self, source, version):
        try:
            set_expires(int(config['app_conf']['expires.package.mr.source_version']))
            sourcefiles = g.shm.packages_get_source_files(self._db(), source, version)
            if len(sourcefiles) == 0: abort(404, 'No such source package or no sources found')
            r = { '_comment': "foo",
                     'package': source,
                     'version': version,
                     'result': map(lambda x: { 'hash': x }, sourcefiles) }
            if ('fileinfo' in request.params) and (request.params['fileinfo'] == '1'):
                r['fileinfo'] = self._get_fileinfo_for_mr(sourcefiles)
            return r
        finally:
            self._db_close()

    @jsonify
    def mr_source_version_binpackages(self, source, version):
        try:
            set_expires(int(config['app_conf']['expires.package.mr.source_version']))
            binpkgs = g.shm.packages_get_binpkgs(self._db(), source, version)
            if len(binpkgs) == 0: abort(404, 'No such source package or no binary packages found')
            binpkgs = map(lambda b: { 'name':      b['name'],
                                      'version':   b['version'] }, binpkgs)
            return { '_comment': "foo",
                     'package': source,
                     'version': version,
                     'result': binpkgs }
        finally:
            self._db_close()

    @jsonify
    def mr_source_version_binfiles(self, source, version, binary, binary_version):
        try:
            set_expires(int(config['app_conf']['expires.package.mr.source_version']))
            binfiles = g.shm.packages_get_binary_files_from_packagenames(self._db(), source, version, binary, binary_version)
            if len(binfiles) == 0: abort(404, 'No such package or no binary files found')
            binfiles = map(lambda b: dict(b), binfiles)
            r = { '_comment': "foo",
                     'package': source,
                     'version': version,
                     'binary': binary,
                     'binary_version': binary_version,
                     'result': binfiles }
            if ('fileinfo' in request.params) and (request.params['fileinfo'] == '1'):
                r['fileinfo'] = self._get_fileinfo_for_mr(map(lambda x: x['hash'], binfiles))
            return r
        finally:
            self._db_close()

    @jsonify
    def mr_source_version_allfiles(self, source, version):
        try:
            set_expires(int(config['app_conf']['expires.package.mr.source_version']))
            sourcefiles = g.shm.packages_get_source_files(self._db(), source, version)
            binpkgs = g.shm.packages_get_binpkgs(self._db(), source, version)
            # we may have binaries without sources.
            if len(sourcefiles) == 0 and len(binpkgs) == 0:
                abort(404, 'No source or binary packages found')
            binpkgs = map(lambda b: dict(b), binpkgs)

            binhashes = []
            for binpkg in binpkgs:
                binpkg['files'] = map(lambda x: dict(x), g.shm.packages_get_binary_files_from_id(self._db(), binpkg['binpkg_id']))
                del binpkg['binpkg_id']
                binhashes += map(lambda x: x['hash'], binpkg['files'])

            r = { '_comment': "foo",
                     'package': source,
                     'version': version,
                     'result': { 'source': sourcefiles, 'binaries': binpkgs }
                   }
            if ('fileinfo' in request.params) and (request.params['fileinfo'] == '1'):
                r['fileinfo'] = self._get_fileinfo_for_mr(sourcefiles + binhashes)
            return r
        finally:
            self._db_close()



# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

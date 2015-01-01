## snapshot.debian.org - web frontend
#
# Copyright (c) 2009, 2010, 2015 Peter Palfrader
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging

from pylons import request, response, session, tmpl_context as c, app_globals, config
from pylons.controllers.util import abort, redirect, etag_cache

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
            self.db = DBInstance(app_globals.pool)
        return self.db

    def _db_close(self):
        if not self.db is None:
            self.db.close()

    def _build_crumbs(self, pkg=None, version=None, start=None, is_binary=False):
        crumbs = []

        url = urllib.quote(request.environ.get('SCRIPT_NAME')) + "/"
        crumbs.append( { 'url': url, 'name': app_globals.domain, 'sep': '|' });

        if is_binary:
            crumbs.append( { 'url': None, 'name': 'binary package:', 'sep': '' });
        else:
            crumbs.append( { 'url': None, 'name': 'source package:', 'sep': '' });

        if not start:
            if pkg.startswith('lib') and len(pkg) >= 4:
                start = pkg[0:4]
            else:
                start = pkg[0:1]

        if is_binary:
            url += 'binary/'
        else:
            url += 'package/'
        crumbs.append( { 'url': url + '?cat=%s'%urllib.quote(start), 'name': start+'*' } )

        if not pkg is None:
            url += urllib.quote(pkg) + '/'
            crumbs.append( { 'url': url, 'name': pkg });

            if version:
                url += urllib.quote(version) + '/'
                crumbs.append( { 'url': url, 'name': version });

        crumbs[-1]['url'] = None
        return crumbs

    def _ensure_ascii(self, string):
        # Package names are ascii.
        # Check that before passing it on to postgres since the DB
        # will just whine about not being able to convert the string
        # anyway.
        # If the passed string is not ascii, then the package name
        # simply does not exist.
        try:
            string.encode('ascii')
        except UnicodeEncodeError:
            abort(404, 'No such package')


    def root(self):
        if 'src' in request.params:
            set_expires(int(config['app_conf']['expires.package.root_cat']))
            url = url_quote(request.params['src'] + "/")
            return redirect(url)
        elif 'cat' in request.params:
            try:
                #etag_cache( app_globals.shm.packages_get_etag(self._db()) )
                set_expires(int(config['app_conf']['expires.package.root_cat']))

                start = request.params['cat']
                pkgs = app_globals.shm.packages_get_name_starts_with(self._db(), start)
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
            set_expires(int(config['app_conf']['expires.package.root_cat']))
            return redirect("../")

    def source(self, source):
        self._ensure_ascii(source)
        try:
            #etag_cache( app_globals.shm.packages_get_etag(self._db()) )
            set_expires(int(config['app_conf']['expires.package.source']))

            sourceversions = app_globals.shm.packages_get_source_versions(self._db(), source)

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
        self._ensure_ascii(source)
        try:
            #etag_cache( app_globals.shm.packages_get_etag(self._db()) )
            set_expires(int(config['app_conf']['expires.package.source_version']))

            sourcefiles = app_globals.shm.packages_get_source_files(self._db(), source, version)
            binpkgs = app_globals.shm.packages_get_binpkgs_from_source(self._db(), source, version)

            # we may have binaries without sources.
            if len(sourcefiles) == 0 and len(binpkgs) == 0:
                abort(404, 'No source or binary packages found')

            binpkgs = map(lambda b: dict(b), binpkgs)
            binhashes = []
            for binpkg in binpkgs:
                binpkg['escaped_name'] = self._attribute_escape(binpkg['name'])
                binpkg['escaped_version'] = self._attribute_escape(binpkg['version'])
                binpkg['files'] = map(lambda x: x['hash'], app_globals.shm.packages_get_binary_files_from_id(self._db(), binpkg['binpkg_id']))
                binhashes += binpkg['files']

            fileinfo = {}
            for hash in sourcefiles + binhashes:
                fileinfo[hash] = app_globals.shm.packages_get_file_info(self._db(), hash)
            for hash in fileinfo:
                fileinfo[hash] = map(lambda fi: dict(fi), fileinfo[hash])
                for fi in fileinfo[hash]:
                    fi['dirlink'] = build_url_archive(fi['archive_name'], fi['run'], fi['path'])
                    fi['link'] = build_url_archive(fi['archive_name'], fi['run'], os.path.join(fi['path'], fi['name']), isadir=False )

            sourcefiles.sort(key=lambda a: (fileinfo[a][0]['name'], a) if len(fileinfo[a]) > 0 else (None,a)) # reproducible file order

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

    def binary_root(self):
        if 'bin' in request.params:
            set_expires(int(config['app_conf']['expires.package.root_cat']))
            url = url_quote(request.params['bin'] + "/")
            return redirect(url)
        elif 'cat' in request.params:
            try:
                #etag_cache( app_globals.shm.packages_get_etag(self._db()) )
                set_expires(int(config['app_conf']['expires.package.root_cat']))

                start = request.params['cat']
                pkgs = app_globals.shm.packages_get_name_starts_with(self._db(), start, get_binary=True)
                if pkgs is None:
                    abort(404, 'No binary packages in this category.')
                c.start = start
                c.packages = link_quote_array(pkgs)
                c.breadcrumbs = self._build_crumbs(start=start, is_binary=True)
                c.title = '%s*'%(start)
                return render('/package-binary-list-packages.mako')
            finally:
                self._db_close()
        else:
            set_expires(int(config['app_conf']['expires.package.root_cat']))
            return redirect("../")

    def binary(self, binary):
        self._ensure_ascii(binary)
        try:

            #etag_cache( app_globals.shm.packages_get_etag(self._db()) )
            set_expires(int(config['app_conf']['expires.package.source']))

            binaryversions = app_globals.shm.packages_get_binary_versions_by_name(self._db(), binary)

            if len(binaryversions) == 0:
                abort(404, 'No such binary package')

            binaryversions = map(lambda b: dict(b), binaryversions)
            for b in binaryversions:
                b['link'] = url_quote('../../package/%s/%s/'%(b['source'], b['version']))
                b['escaped_name'] = self._attribute_escape(b['name'])
                b['escaped_binary_version'] = self._attribute_escape(b['binary_version'])

            c.binary = binary
            c.binaryversions = binaryversions
            c.breadcrumbs = self._build_crumbs(binary, is_binary=True)
            c.title = binary
            return render('/package-binary.mako')
        finally:
            self._db_close()


    def _get_fileinfo_for_mr_one(self, hash):
        fileinfo = map(lambda x: dict(x), app_globals.shm.packages_get_file_info(self._db(), hash))
        for fi in fileinfo:
            fi['first_seen'] = rfc3339_timestamp(fi['run'])
            del fi['run']
        return fileinfo

    def _get_fileinfo_for_mr(self, hashes):
        r = {}
        for hash in hashes:
            r[hash] = self._get_fileinfo_for_mr_one(hash)
        return r

    @jsonify
    def mr_list(self):
        try:
            set_expires(int(config['app_conf']['expires.package.mr.list']))
            pkgs = app_globals.shm.packages_get_all(self._db())
            return { '_comment': "foo",
                     'result': map(lambda x: { 'package': x }, pkgs) }
        finally:
            self._db_close()

    @jsonify
    def mr_source(self, source):
        try:
            set_expires(int(config['app_conf']['expires.package.mr.source']))
            sourceversions = app_globals.shm.packages_get_source_versions(self._db(), source)
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
            sourcefiles = app_globals.shm.packages_get_source_files(self._db(), source, version)
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
            binpkgs = app_globals.shm.packages_get_binpkgs_from_source(self._db(), source, version)
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
            binfiles = app_globals.shm.packages_get_binary_files_from_packagenames(self._db(), source, version, binary, binary_version)
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
            sourcefiles = app_globals.shm.packages_get_source_files(self._db(), source, version)
            binpkgs = app_globals.shm.packages_get_binpkgs_from_source(self._db(), source, version)
            # we may have binaries without sources.
            if len(sourcefiles) == 0 and len(binpkgs) == 0:
                abort(404, 'No source or binary packages found')
            binpkgs = map(lambda b: dict(b), binpkgs)

            binhashes = []
            for binpkg in binpkgs:
                binpkg['files'] = map(lambda x: dict(x), app_globals.shm.packages_get_binary_files_from_id(self._db(), binpkg['binpkg_id']))
                del binpkg['binpkg_id']
                binhashes += map(lambda x: x['hash'], binpkg['files'])

            r = { '_comment': "foo",
                  'package': source,
                  'version': version,
                  'result': { 'source': map(lambda x: { 'hash': x }, sourcefiles), 'binaries': binpkgs }
                   }
            if ('fileinfo' in request.params) and (request.params['fileinfo'] == '1'):
                r['fileinfo'] = self._get_fileinfo_for_mr(sourcefiles + binhashes)
            return r
        finally:
            self._db_close()

    @jsonify
    def mr_binary(self, binary):
        try:
            set_expires(int(config['app_conf']['expires.package.mr.source']))
            binaryversions = app_globals.shm.packages_get_binary_versions_by_name(self._db(), binary)
            binaryversions = map(lambda b: dict(b), binaryversions)
            if len(binaryversions) == 0: abort(404, 'No such binary package')
            r = { '_comment': "foo",
                  'binary': binary,
                  'result': binaryversions }
            return r
        finally:
            self._db_close()

    @jsonify
    def mr_binary_version_binfiles(self, binary, binary_version):
        try:
            binfiles = app_globals.shm.packages_get_binary_files(self._db(), binary, binary_version)
            if len(binfiles) == 0: abort(404, 'No such package or no binary files found')
            binfiles = map(lambda b: dict(b), binfiles)
            r = { '_comment': "foo",
                  'binary': binary,
                  'binary_version': binary_version,
                  'result': binfiles }
            if ('fileinfo' in request.params) and (request.params['fileinfo'] == '1'):
                r['fileinfo'] = self._get_fileinfo_for_mr(map(lambda x: x['hash'], binfiles))
            return r
        finally:
            self._db_close()

    @jsonify
    def mr_fileinfo(self, hash):
        if not re.match('[0-9a-f]{40}$', hash): # match matches only at start of string
            abort(404, 'Invalid hash format.')

        try:
            return { '_comment': "foo",
                     'hash': hash,
                     'result': self._get_fileinfo_for_mr_one(hash) }
            return r
        finally:
            self._db_close()



# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

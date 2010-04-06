import logging

from pylons import request, response, session, tmpl_context as c, g, config
from pylons.controllers.util import abort, redirect_to, etag_cache

from snapshot.lib.base import BaseController, render

from snapshot.lib.dbinstance import DBInstance
from snapshot.lib.control_helpers import *

import os.path
import re
import mimetypes
import error
import errno
from paste.request import construct_url
from paste.fileapp import FileApp
from paste.httpexceptions import HTTPMovedPermanently

import wsgiref.handlers
import time
import urllib

log = logging.getLogger(__name__)

expires_file = datetime.timedelta(seconds = int(config['app_conf']['expires.archive.file']))

class SnapshotFileApp(FileApp):
    def __init__(self, path, digest, filename=None):
        h = {}
        if not filename is None:
            (type, encoding) = mimetypes.guess_type(filename)
            if not type is None:
                h['Content-Type'] = type
            if not encoding is None:
                h['Content-Encoding'] = encoding
        expires = datetime.datetime.now() + datetime.timedelta(seconds = int(config['app_conf']['expires.archive.file']))
        h['Expires'] = wsgiref.handlers.format_date_time( time.mktime( expires.timetuple() ))
        h['Cache-Control'] = 'public, max-age=%d'%int(config['app_conf']['expires.archive.file'])

        FileApp.__init__(self, path, **h)

        self.digest = digest

    def calculate_etag(self):
        return self.digest

class ArchiveController(BaseController):
    db = None

    def _db(self):
        if self.db is None:
            self.db = DBInstance(g.pool)
        return self.db

    def _db_close(self):
        if not self.db is None:
            self.db.close()


    def root(self):
        return redirect_to("../")

    def archive_base(self, archive):
        try:
            #etag_cache( g.shm.mirrorruns_get_etag(self._db(), archive) )
            set_expires(int(config['app_conf']['expires.archive.index']))

            if 'year' in request.params and 'month' in request.params:
                y = request.params['year']
                m = request.params['month']
                return self._archive_ym(archive, y, m)

            yearmonths = g.shm.mirrorruns_get_yearmonths_from_archive(self._db(), archive)

            if yearmonths is None:
                abort(404, 'Archive "%s" does not exist'%(archive))

            c.yearmonths = yearmonths
            c.archive = archive
            c.breadcrumbs = self._build_crumbs(archive)
            c.title = archive
            return render('/archive.mako')
        finally:
            self._db_close()

    def _archive_ym(self, archive, year, month):
        try:
            if not re.match('\d{4}$', year): # match matches only at start of string
                abort(404, 'Year "%s" is not valid.'%(year))
            if not re.match('\d{1,2}$', month): # match matches only at start of string
                abort(404, 'Month "%s" is not valid.'%(month))

            runs = g.shm.mirrorruns_get_runs_from_archive_ym(self._db(), archive, year, month)
            if runs is None:
                abort(404, 'Archive "%s" does not exist'%(archive))
            if len(runs) == 0:
                abort(404, 'Found no mirrorruns for archive %s in %s-%s.'%(archive, year, month))

            c.archive = archive
            c.year = year
            c.month = "%02d"%(int(month))
            c.breadcrumbs = self._build_crumbs(archive, year=int(year), month=int(month))
            c.runs = map(lambda r:
                            { 'run'   : r['run'],
                              # make a machine readable version of a timestamp
                              'run_mr': rfc3339_timestamp(r['run'])
                            }, runs)
            c.title = '%s:%s-%02d'%(archive, year, int(month))
            return render('/archive-runs.mako')
        finally:
            self._db_close()

    def _regular_file(self, digest, visiblepath=None):
        try:
            realpath = g.shm.get_filepath(self._db(), digest)
            fa = SnapshotFileApp(realpath, digest, visiblepath)
            return fa(request.environ, self.start_response)
        except os.error, error:
            if (error.errno == errno.ENOENT):
                abort(404, "Ooops, we do not have a file with digest %s altho we should.  You might want to report this."%(stat['digest']))
            elif (error.errno == errno.EACCESS):
                abort(403, "Ooops, cannot read file with digest %s.  Maybe this file is not redistributable and this was done on purpose.  If in doubt report this."%(stat['digest']))
            else:
                raise

    # XXX: make this use control_helpers build_url_archive
    def _build_crumbs(self, archive, run=None, path=None, year=None, month=None):
        crumbs = []

        url = request.environ.get('SCRIPT_NAME') + "/"
        crumbs.append( { 'url': url, 'name': 'snapshot.debian.org' });

        url += 'archive/' + archive + "/"
        crumbs.append( { 'url': url, 'name': archive, 'sep': '' });

        if run:
            if not year is None or not month is None:
                raise "Cannot set both run and year/month"
            year = run['run'].year
            month = run['run'].month

        if not year is None and not month is None:
            ym = (year, month)
            crumbs.append( { 'url': url+"?year=%d&month=%d"%ym, 'name': '(%d-%02d)'%ym });

        if run:
            url += rfc3339_timestamp(run['run']) + '/'
            crumbs.append( { 'url': url, 'name': run['run'] });

            if path and path != '/':
                for path_element in path.strip('/').split('/'):
                    url += path_element + '/'
                    crumbs.append( { 'url': url, 'name': path_element });

        crumbs[-1]['url'] = None

        return crumbs

    def _dir_helper(self, archive, run, stat):
        realpath = os.path.join('/archive', archive, rfc3339_timestamp(run['run']), stat['path'].strip('/'), '')
        if realpath != request.environ['PATH_INFO']:
            request.environ['PATH_INFO'] = realpath
            url = construct_url(request.environ)
            raise HTTPMovedPermanently(url)

        list = g.shm.mirrorruns_readdir(self._db(), run['mirrorrun_id'], stat['path'])
        list = map(lambda b: dict(b), list)
        for e in list:
            e['quoted_name'] = urllib.quote(e['name'])
            if not e['target'] is None:
                e['quoted_target'] = urllib.quote(e['target'])
        if stat['path'] != '/':
            list = [ { 'filetype': 'd', 'name': '..', 'quoted_name': '..', 'first_run': None, 'last_run': None } ] + list

        node_info = g.shm.mirrorruns_get_first_last_from_node(self._db(), stat['node_id'])
        neighbors = g.shm.mirrorruns_get_neighbors(self._db(), run['mirrorrun_id'])
        neighbors_change = g.shm.mirrorruns_get_neighbors_change(self._db(), run['archive_id'], run['run'], stat['directory_id']) 

        c.run = run
        c.readdir = list
        c.nav = {
          'first':       node_info['first_run'],
          'prev_change': neighbors_change['prev'],
          'prev':        neighbors['prev'],
          'next':        neighbors['next'],
          'next_change': neighbors_change['next'],
          'last':        node_info['last_run'] }

        for key in c.nav.keys():
            if not c.nav[key] is None:
                c.nav[key+'_link'] = os.path.join('/archive', archive, rfc3339_timestamp(c.nav[key]), stat['path'].strip('/'), '')

        c.breadcrumbs = self._build_crumbs(archive, run, stat['path'])
        set_expires(int(config['app_conf']['expires.archive.dir']))
        c.title = '%s:%s (%s)'%(archive, stat['path'], run['run'])
        return render('/archive-dir.mako')


    def _dateok(self, date):
        if re.match('\d{8}$', date):
            try:
                time.strptime(date, "%Y%m%d")
                return True
            except ValueError:
                pass

        if re.match('\d{8}T\d{6}Z', date):
            try:
                time.strptime(date, "%Y%m%dT%H%M%SZ")
                return True
            except ValueError:
                pass

        if date == "now": return True
        return False

    def dir(self, archive, date, url):
        try:
            #etag_cache( g.shm.mirrorruns_get_etag(self._db(), archive) )

            if not self._dateok(date):
                abort(404, 'Invalid date string - nothing to be found here.')

            run = g.shm.mirrorruns_get_mirrorrun_at(self._db(), archive, date)
            if run is None:
                abort(404, 'No mirrorrun found at this date.')

            stat = g.shm.mirrorruns_stat(self._db(), run['mirrorrun_id'], '/'+url)
            if stat is None:
                abort(404, 'No such file or directory.')

            if stat['filetype'] == 'd':
                return self._dir_helper(archive, run, stat)
            elif stat['filetype'] == '-':
                return self._regular_file(stat['digest'], stat['path'])
        finally:
            self._db_close()


    def file(self, hash):
        if re.match('[0-9a-f]{40}$', hash): # match matches only at start of string
            return self._regular_file(hash)
        else:
            abort(404, 'Invalid hash format.')

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

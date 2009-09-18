import logging
from snapshot.lib.dbinstance import DBInstance
from snapshot.lib.base import *
from paste.fileapp import FileApp
import paste.httpexceptions
import os.path
import re
import mimetypes
import error
import errno

log = logging.getLogger(__name__)

class ArchiveController(BaseController):
    def _urlify_timestamp(self, ts):
        return ts.strftime('%Y%m%dT%H%M%S')

    def root(self):
        if request.environ.get('PATH_INFO')[-1:] == "/":
            return redirect_to("../")
        else:
            return redirect_to("./")

    def archive_base(self, archive):
        if 'year' in request.params and 'month' in request.params:
            y = request.params['year']
            m = request.params['month']
            return self._archive_ym(archive, y, m)

        yearmonths = g.shm.mirrorruns_get_yearmonths_from_archive(archive)

        if yearmonths is None:
            abort(404)

        c.yearmonths = yearmonths
        c.archive = archive
        c.breadcrumbs = self._build_crumbs(archive)
        return render('/archive.mako')

    def _archive_ym(self, archive, year, month):
        if not re.match('\d{4}$', year): # match matches only at start of string
            abort(404)
        if not re.match('\d{1,2}$', month): # match matches only at start of string
            abort(404)

        runs = g.shm.mirrorruns_get_runs_from_archive_ym(archive, year, month)
        if runs is None:
            abort(404)

        c.archive = archive
        c.year = year
        c.month = "%02d"%(int(month))
        c.breadcrumbs = self._build_crumbs(archive, year=int(year), month=int(month))
        c.runs = map(lambda r:
                        { 'run'   : r['run'],
                          # make a machine readable version of a timestamp
                          'run_mr': self._urlify_timestamp(r['run'])
                        }, runs)
        return render('/archive-runs.mako')

    def unicode_encode(self, path):
        if isinstance(path, unicode):
            return path.encode('utf-8')
        else:
            return path


    def _regular_file(self, stat):
        path = g.shm.get_filepath(stat['digest'])
        try:
            (type, encoding) = mimetypes.guess_type(stat['path'])
            h = {}
            if not type is None:
                h['Content-Type'] = type
            if not encoding is None:
                h['Content-Encoding'] = encoding
            fa = FileApp(path, **h);
            return fa(request.environ, self.start_response)
        except os.error, error:
            if (error.errno == errno.ENOENT):
                abort(404)
            elif (error.errno != errno.EACCESS):
                abort(403)
            else:
                raise

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
            url += self._urlify_timestamp(run['run']) + '/'
            crumbs.append( { 'url': url, 'name': run['run'] });

            if path and path != '/':
                for path_element in path.strip('/').split('/'):
                    url += path_element + '/'
                    crumbs.append( { 'url': url, 'name': path_element });

        crumbs[-1]['url'] = None

        return crumbs


    def _dir_helper(self, archive, run, stat):
        realpath = os.path.join('/archive', archive, self._urlify_timestamp(run['run']), stat['path'].strip('/'), '')
        if realpath != request.environ.get('PATH_INFO'):
            return redirect_to(self.unicode_encode(realpath))

        list = g.shm.mirrorruns_readdir(run['mirrorrun_id'], stat['path'])
        if stat['path'] != '/':
            list = [ { 'filetype': 'd', 'name': '..', 'first_run': None, 'last_run': None } ] + list

        node_info = g.shm.mirrorruns_get_first_last_from_node(stat['node_id'])
        neighbors = g.shm.mirrorruns_get_neighbors(run['mirrorrun_id'])

        c.run = run
        c.readdir = list
        c.nav = {
          'first': node_info['first_run'],
          'prev': neighbors['prev'],
          'next': neighbors['next'],
          'last': node_info['last_run'] }

        # XXX add links and stuff.
        c.breadcrumbs = self._build_crumbs(archive, run, stat['path'])
        return render('/archive-dir.mako')

    def dir(self, archive, date, url):
        run = g.shm.mirrorruns_get_mirrorrun_at(archive, date)
        if run is None:
            abort(404)

        stat = g.shm.mirrorruns_stat(run['mirrorrun_id'], '/'+url)
        if stat is None:
            abort(404)

        if stat['filetype'] == 'd':
            return self._dir_helper(archive, run, stat)
        elif stat['filetype'] == '-':
            return self._regular_file(stat)

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

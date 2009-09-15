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
        return render('/archive.mako')

    def _archive_ym(self, archive, year, month):
        if not re.match('\d{4}$', year): # match matches only at start of string
            abort(404)
        if not re.match('\d{1,2}$', month): # match matches only at start of string
            abort(404)

        runs = g.shm.mirrorruns_get_runs_from_archive_ym(archive, year, month)
        if runs is None:
            abort(404)

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
            print path
            fa = FileApp(path, **h);
            return fa(request.environ, self.start_response)
        except os.error, error:
            if (error.errno == errno.ENOENT):
                abort(404)
            elif (error.errno != errno.EACCESS):
                abort(403)
            else:
                raise

    def _dir_helper(self, archive, run, stat):
        realpath = os.path.join('/archive', archive, self._urlify_timestamp(run['run']), stat['path'].strip('/'), '')
        if realpath != request.environ.get('PATH_INFO'):
            return redirect_to(self.unicode_encode(realpath))
        list = g.shm.mirrorruns_readdir(run['mirrorrun_id'], stat['path'])
        if stat['path'] != '/':
            list = [ { 'filetype': 'd', 'name': '..' } ] + list
        c.readdir = list
        c.neighbors = g.shm.mirrorruns_get_neighbors(run['mirrorrun_id'])

        # XXX add links and stuff.
        c.breadcrumbs = realpath.rstrip('/').split('/')

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

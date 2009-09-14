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

        c.runs = runs
        return render('/archive-runs.mako')

    def unicode_encode(self, path):
        if isinstance(path, unicode):
            return path.encode('utf-8')
        else:
            return path

    def dir(self, archive, date, url):
        run = g.shm.mirrorruns_get_mirrorrun_at(archive, date)
        if run is None:
            abort(404)

        url = "/" + url

        stat = g.shm.mirrorruns_stat(run['mirrorrun_id'], url)
        print "url: "+url
        print "stat: ", stat

        if stat is None:
            abort(404)

        if stat['filetype'] == 'd':
            if url != "/" and url != stat['path']+'/':
                # XXX this will blow up once stat does symlink resolving
                return redirect_to(self.unicode_encode(os.path.basename(url))+"/")
            c.readdir = g.shm.mirrorruns_readdir(run['mirrorrun_id'], stat['path'])

            c.msg = "url: %s"%url
            c.msg += " stat: %s"% stat

            c.breadcrumbs = [ 'archive', archive, run['run_hr'] ] + url.split('/')
            return render('/archive-dir.mako')
        elif stat['filetype'] == '-':
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

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

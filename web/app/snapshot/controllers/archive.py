import logging
from snapshot.lib.dbinstance import DBInstance
from snapshot.lib.base import *
import paste.httpexceptions
import re

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

    def dir(self, archive, date, url):
        run = g.shm.mirrorruns_get_mirrorrun_at(archive, date)
        if run is None:
            abort(404)
        c.breadcrumbs = [ 'archive', archive, run['run_hr'] ] + url.split('/')
        return render('/archive-dir.mako')

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

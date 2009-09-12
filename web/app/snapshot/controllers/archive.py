import logging
from snapshot.lib.dbinstance import DBInstance
from snapshot.lib.base import *
import paste.httpexceptions
import re

log = logging.getLogger(__name__)

class ArchiveController(BaseController):
    def root(self, environ):
        if environ['PATH_INFO'][-1:] == "/":
            return redirect_to("../")
        else:
            return redirect_to("../")

    def archive_base(self, environ, archive):
        if 'year' in request.params and 'month' in request.params:
            y = request.params['year']
            m = request.params['month']
            return self.archive_ym(environ, archive, y, m)

        yearmonths = g.shm.mirrorruns_get_yearmonths_from_archive(archive)

        if yearmonths is None:
            abort(404)

        c.yearmonths = yearmonths
        return render('/archive.mako')

    def archive_ym(self, environ, archive, year, month):
        if not re.match('\d{4}$', year): # match matches only at start of string
            abort(404)
        if not re.match('\d{2}$', month): # match matches only at start of string
            abort(404)

        runs = g.shm.mirrorruns_get_runs_from_archive_ym(archive, year, month)

        if runs is None:
            abort(404)

        c.runs = runs
        return render('/archive-runs.mako')

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

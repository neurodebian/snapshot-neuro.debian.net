import logging
from snapshot.lib.dbinstance import DBInstance
from snapshot.lib.base import *
import paste.httpexceptions

log = logging.getLogger(__name__)

class ArchiveController(BaseController):
    def root(self, environ):
        if environ['PATH_INFO'][-1:] == "/":
            return redirect_to("../")
        else:
            return redirect_to("../")

    def archive_base(self, environ, archive):
        yearmonths = g.shm.mirrorruns_get_yearmonths_from_archive(archive)

        if yearmonths is None:
            response.status_code = 404
            return render('/archive.mako')

        c.yearmonths = yearmonths
        return render('/archive.mako')

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

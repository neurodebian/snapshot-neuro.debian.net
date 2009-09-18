import logging
from snapshot.lib.dbinstance import DBInstance
from snapshot.lib.base import *
from paste.fileapp import FileApp
import paste.httpexceptions
import os.path

log = logging.getLogger(__name__)

class PackageController(BaseController):
    def unicode_encode(self, path):
        if isinstance(path, unicode):
            return path.encode('utf-8')
        else:
            return path

    def ensure_directory(self):
        if not request.environ.get('PATH_INFO')[-1:] == "/":
            return redirect_to(os.path.basename(request.environ.get('PATH_INFO'))+"/")

    def root(self):
        self.ensure_directory()
        if not 'src' in request.params:
            return redirect_to("../")
        return redirect_to(self.unicode_encode(request.params['src'] + "/"))


    def source(self, source):
        self.ensure_directory()

        sourceversions = g.shm.packages_get_source_versions(source)

        if len(sourceversions) == 0:
            abort(404)

        c.src = source
        c.sourceversions = sourceversions
        return render('/package-source.mako')

    def source_version(self, source, version):
        self.ensure_directory()

        hashes = g.shm.packages_get_source_files(source, version)

        if len(hashes) == 0:
            abort(404)

        c.src = source
        c.sourceversions = hashes
        return render('/package-source.mako')


# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

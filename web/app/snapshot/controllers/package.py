import logging
from snapshot.lib.dbinstance import DBInstance
from snapshot.lib.base import *
from paste.fileapp import FileApp
import paste.httpexceptions
import os.path
from snapshot.lib.control_helpers import *

log = logging.getLogger(__name__)

class PackageController(BaseController):

    def root(self):
        ensure_directory()
        if not 'src' in request.params:
            return redirect_to("../")
        return redirect_to(unicode_encode(request.params['src'] + "/"))


    def source(self, source):
        ensure_directory()

        sourceversions = g.shm.packages_get_source_versions(source)

        if len(sourceversions) == 0:
            abort(404)

        c.src = source
        c.sourceversions = sourceversions
        return render('/package-source.mako')

    def source_version(self, source, version):
        ensure_directory()

        hashes = g.shm.packages_get_source_files(source, version)

        if len(hashes) == 0:
            abort(404)

        fileinfo = {}
        for hash in hashes:
            fileinfo[hash] = g.shm.packages_get_file_info(hash)
            # XXX what if we got zero rows?  handle that somehow...

        hashes.sort(key=lambda a: (fileinfo[a][0]['name'], a))

        for hash in fileinfo:
            fileinfo[hash] = map(lambda fi: dict(fi), fileinfo[hash]) # copy fileinfo into a real dict, not a psycopg2 pseudo dict
            for fi in fileinfo[hash]:
                fi['dirlink'] = build_url_archive(fi['archive_name'], fi['run'], fi['path'])
                fi['link'] = build_url_archive(fi['archive_name'], fi['run'], os.path.join(fi['path'], fi['name']), isadir=False )

        c.src = source
        c.version = version
        c.sourcefiles = hashes
        c.fileinfo = fileinfo
        return render('/package-source-one.mako')


# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

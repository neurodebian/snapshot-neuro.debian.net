from snapshot.lib.dbinstance import DBInstance
import os.path
import hashlib
from pylons.decorators.cache import beaker_cache

class SnapshotModel:
    def __init__(self, farmpath, pool):
        self.farmpath = farmpath

    def archives_get_list(self, db):
        rows = db.query("SELECT name FROM archive ORDER BY name")
        return map(lambda x: x['name'], rows)

    def mirrorruns_get_yearmonths_from_archive(self, db, archive):
        result = None

        rows = db.query("""SELECT archive_id FROM archive WHERE archive.name=%(name)s""",
            { 'name': archive })

        if len(rows) != 0:
            archive_id = rows[0]['archive_id']

            rows = db.query("""
                SELECT extract(year from run)::INTEGER AS year,
                       extract(month from run)::INTEGER AS month
                  FROM mirrorrun
                  WHERE mirrorrun.archive_id=%(archive_id)s
                  GROUP BY year, month
                  ORDER BY year, month""",
                { 'archive_id': archive_id })

            # make an array like thus:
            #  - year: nnnn
            #    months:
            #      - nn
            #      - nn
            #  - year: nnnn
            #    months:
            #      - nn
            #      - nn
            #      - nn
            result = []
            for row in rows:
                y, m = row['year'], row['month']
                if len(result) == 0 or result[-1]['year'] != y:
                    result.append( { 'year': y, 'months': [] } )
                result[-1]['months'].append(m)

        return result

    def mirrorruns_get_runs_from_archive_ym(self, db, archive, year, month):
        result = None

        rows = db.query("""SELECT archive_id FROM archive WHERE archive.name=%(name)s""",
            { 'name': archive })

        if len(rows) != 0:
            archive_id = rows[0]['archive_id']

            result = db.query("""
                SELECT run
                  FROM mirrorrun
                  WHERE mirrorrun.archive_id=%(archive_id)s
                    AND extract(year from run) = %(year)s
                    AND extract(month from run) = %(month)s
                  ORDER BY run""",
                { 'archive_id': archive_id,
                  'year': year,
                  'month': month })

        return result

    def mirrorruns_get_mirrorrun_at(self, db, archive, datespec):
        result = None

        rows = db.query("""
                SELECT run, mirrorrun_id, mirrorrun.archive_id
                  FROM mirrorrun JOIN archive ON mirrorrun.archive_id = archive.archive_id
                  WHERE archive.name=%(archive)s
                    AND mirrorrun.run <= %(datespec)s
                  ORDER BY run DESC
                  LIMIT 1""",
                { 'archive': archive,
                  'datespec': datespec })
        if len(rows) != 0:
            result = rows[0]

        return result

    #@beaker_cache(expire=600, cache_response=False, type='memory', key='archive')
    #def mirrorruns_get_etag(self, db, archive):
    #    """We use this result as an identifier for the state of the system,
    #       returning this value as a HTTP ETag token for client side caching
    #       purposes."""
    #    # XXX it might be nice to hash the state of the application
    #    # (code, templates) into this as well.
    #    key = hashlib.sha1()
    #    cursor = None
    #    try:
    #        cursor = db.execute("""SELECT mirrorrun_uuid
    #                               FROM mirrorrun
    #                               WHERE archive_id = (SELECT archive_id FROM archive WHERE name=%(archive)s)
    #                               ORDER BY mirrorrun_uuid""",
    #                            { 'archive': archive })
    #        while True:
    #            n = cursor.fetchone()
    #            if n is None:
    #                break
    #            key.update(n['mirrorrun_uuid'])
    #
    #        return key.hexdigest()
    #    finally:
    #        if not cursor is None:
    #            cursor.close()

    #@beaker_cache(expire=600, cache_response=False, type='memory', key=None)
    #def packages_get_etag(self, db):
    #    """We use this result as an identifier for the state of the system,
    #       returning this value as a HTTP ETag token for client side caching
    #       purposes."""
    #    # XXX it might be nice to hash the state of the application
    #    # (code, templates) into this as well.
    #    key = hashlib.sha1()
    #    cursor = None
    #    try:
    #        cursor = db.execute("""SELECT mirrorrun_uuid
    #                               FROM mirrorrun JOIN indexed_mirrorrun ON mirrorrun.mirrorrun_id = indexed_mirrorrun.mirrorrun_id
    #                               ORDER BY mirrorrun_uuid""")
    #        while True:
    #            n = cursor.fetchone()
    #            if n is None:
    #                break
    #            key.update(n['mirrorrun_uuid'])
    #
    #        return key.hexdigest()
    #    finally:
    #        if not cursor is None:
    #            cursor.close()

    #def mirrorruns_get_last_mirrorrun(self, db, archive):
    #    row = db.query_one("""
    #            SELECT max(run)::TIMESTAMP WITH TIME ZONE AS run
    #              FROM mirrorrun
    #              WHERE archive_id=(SELECT archive_id FROM archive WHERE name=%(archive)s)
    #              """,
    #            { 'archive': archive } )
    #    if row is None:
    #        return None
    #
    #    return row['run']

    def mirrorruns_get_neighbors(self, db, mirrorrun_id):
        result = db.query_one("""
            SELECT this.run,
                 (SELECT run FROM mirrorrun
                  WHERE mirrorrun.archive_id = this.archive_id
                    AND run > this.run
                  ORDER BY run
                  LIMIT 1) AS next,
                 (SELECT run FROM mirrorrun
                  WHERE mirrorrun.archive_id = this.archive_id
                    AND run < this.run
                  ORDER BY run DESC
                  LIMIT 1) AS prev
            FROM mirrorrun AS this
            WHERE mirrorrun_id=%(mirrorrun_id)s
              """,
            { 'mirrorrun_id': mirrorrun_id })
        return result

    def mirrorruns_get_neighbors_change(self, db, archive_id, mirrorrun_run, directory_id):
        """Retrun the date of the previous and next mirrorrun where anything
           actually changed in this directory"""
        result = db.query_one("""
            SELECT prev.prev, next.next FROM

                    (SELECT min(next.next) AS next FROM
                     (  SELECT min(first_run) AS next from node_with_ts2 where parent = %(directory_id)s and first_run > %(mirrorrun_run)s
                      UNION ALL
                        SELECT min(run) AS next FROM mirrorrun WHERE archive_id=%(archive_id)s AND run > (SELECT min(last_run) AS next from node_with_ts2 where parent = %(directory_id)s and last_run >= %(mirrorrun_run)s)
                     ) AS next) AS next,

                    (SELECT max(prev.prev) AS prev FROM
                     (  SELECT max(run) AS prev FROM mirrorrun WHERE archive_id=%(archive_id)s AND run < (SELECT max(first_run) AS prev from node_with_ts2 where parent = %(directory_id)s and first_run <= %(mirrorrun_run)s)
                      UNION ALL
                        SELECT max(last_run) AS prev from node_with_ts2 where parent = %(directory_id)s and last_run < %(mirrorrun_run)s
                     ) AS prev) AS prev

              """,
            { 'mirrorrun_run': mirrorrun_run,
              'archive_id': archive_id,
              'directory_id': directory_id })
        return result

    def _strip_multi_slash(self, str):
        old = str
        while True:
            str = str.replace('//', '/')
            if str == old: break
            old = str
        return str

    def mirrorruns_stat(self, db, mirrorrun_id, path):
        """'stats' a path in a given mirrorrun.  Will return None if the path doesn't exist.
           If it does exist it will do (recursive) symlink resolving and return a dict
           with either file or dir information.
           XXX no idea what it does on danling or cyclic symlinks yet"""
        result = None

        path = path.rstrip('/')
        path = self._strip_multi_slash(path)
        if path == "":
            path = '/'

        stat = db.query_one("""SELECT filetype, path, directory_id, node_id, digest, size FROM stat(%(path)s, %(mirrorrun_id)s)""",
                { 'mirrorrun_id': mirrorrun_id,
                  'path': path } )

        if stat['filetype'] is None:
            return None

        return stat

    def mirrorruns_get_first_last_from_node(self, db, node_id):

        first_last = db.query_one("""SELECT first_run, last_run
                                     FROM node_with_ts2
                                     WHERE node_id=%(node_id)s""",
                { 'node_id': node_id } )

        return first_last

    def mirrorruns_readdir(self, db, mirrorrun_id, path):

        readdir = db.query("""SELECT filetype, name, digest, size, target, first_run, last_run
                              FROM readdir(%(path)s, %(mirrorrun_id)s)
                              JOIN node_with_ts2
                                ON readdir.node_id = node_with_ts2.node_id
                              ORDER BY name""",
                { 'mirrorrun_id': mirrorrun_id,
                  'path': path } )

        return readdir

    def get_filepath(self, digest):
        prefix1 = digest[0:2]
        prefix2 = digest[2:4]
        return os.path.join(self.farmpath, prefix1, prefix2, digest)

    def packages_get_source_versions(self, db, source):
        rows = db.query("""SELECT version FROM srcpkg WHERE name=%(source)s ORDER BY version DESC""",
                { 'source': source } )

        return map(lambda x: x['version'], rows)

    def packages_get_source_files(self, db, source, version):
        rows = db.query("""SELECT hash
                           FROM file_srcpkg_mapping
                               JOIN srcpkg
                               ON srcpkg.srcpkg_id=file_srcpkg_mapping.srcpkg_id
                           WHERE name=%(source)s AND version=%(version)s""",
                { 'source': source,
                  'version': version} )

        return map(lambda x: x['hash'], rows)

    def packages_get_binpkgs_from_source(self, db, source, version):
        rows = db.query("""SELECT name, version, binpkg_id
                           FROM binpkg
                             WHERE srcpkg_id = (SELECT srcpkg_id FROM srcpkg WHERE name=%(source)s AND version=%(version)s)
                           ORDER BY name, version""",
                { 'source': source,
                  'version': version} )
        return rows

    def packages_get_binary_versions_by_name(self, db, binary):
        rows = db.query("""SELECT binpkg.name AS name, binpkg.version AS binary_version, srcpkg.name AS source, srcpkg.version AS version
                           FROM binpkg
                               JOIN srcpkg
                               ON binpkg.srcpkg_id=srcpkg.srcpkg_id
                           WHERE binpkg.name=%(binary)s
                           ORDER BY binpkg.version""",
                { 'binary': binary} )
        return rows

    def packages_get_binary_files_from_id(self, db, binpkg_id):
        rows = db.query("""SELECT hash, architecture
                           FROM file_binpkg_mapping
                           WHERE binpkg_id=%(binpkg_id)s
                           ORDER BY architecture""",
                { 'binpkg_id': binpkg_id } )
        return rows

    def packages_get_binary_files_from_packagenames(self, db, source, version, binary, binary_version):
        rows = db.query("""SELECT file_binpkg_mapping.architecture, file_binpkg_mapping.hash
                           FROM file_binpkg_mapping
                                JOIN binpkg ON file_binpkg_mapping.binpkg_id = binpkg.binpkg_id
                           WHERE binpkg.srcpkg_id = (SELECT srcpkg_id FROM srcpkg WHERE name=%(source)s AND version=%(version)s)
                                 AND binpkg.name = %(binary)s
                                 AND binpkg.version = %(binary_version)s
                           """,
                { 'source': source,
                  'version': version,
                  'binary': binary,
                  'binary_version': binary_version } )
        return rows

    def packages_get_file_info(self, db, hash):
        rows = db.query("""SELECT
                             file.name,
                             file.size,
                             mirrorrun.run,
                             archive.name as archive_name,
                             directory.path
                           FROM file
                             JOIN node ON file.node_id = node.node_id
                             JOIN mirrorrun ON node.first = mirrorrun.mirrorrun_id
                             JOIN archive ON mirrorrun.archive_id = archive.archive_id
                             JOIN directory ON node.parent = directory.directory_id
                           WHERE hash=%(hash)s
                           ORDER BY run""",
                        { 'hash': hash } )
        return rows

    @beaker_cache(expire=600, cache_response=False, type='memory', key=None)
    def packages_get_name_starts(self, db):
        rows = db.query("""SELECT DISTINCT substring( name FROM 1 FOR 1 ) AS start FROM srcpkg
                           UNION ALL
                           SELECT DISTINCT substring( name FROM 1 FOR 4 ) AS start FROM srcpkg WHERE name LIKE 'lib_%%'
                           ORDER BY start""")
        return map(lambda x: x['start'], rows)

    def packages_get_name_starts_with(self, db, start):
        if not start in self.packages_get_name_starts(db):
            return None
        if start == "l":
            rows = db.query("""SELECT DISTINCT name FROM srcpkg WHERE name LIKE %(start)s AND NOT (name LIKE 'lib_%%') ORDER BY name""",
                            {'start': start+"%" })
        else:
            rows = db.query("""SELECT DISTINCT name FROM srcpkg WHERE name LIKE %(start)s ORDER BY name""",
                            {'start': start+"%" })
        return map(lambda x: x['name'], rows)

    def packages_get_all(self, db):
        rows = db.query("""SELECT DISTINCT name FROM srcpkg""")
        return map(lambda x: x['name'], rows)

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

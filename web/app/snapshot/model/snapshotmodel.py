from snapshot.lib.dbinstance import DBInstance

class SnapshotModel:
    def __init__(self, pool):
        self.pool = pool

    def archives_get_list(self):
        db = DBInstance(self.pool)
        rows = db.query("SELECT name FROM archive ORDER BY name")
        db.close()
        return map(lambda x: x['name'], rows)

    def mirrorruns_get_yearmonths_from_archive(self, archive):
        db = DBInstance(self.pool)
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
                if len(result) == 0 or len[-1]['year'] != y:
                    result.append( { 'year': y, 'months': [] } )
                result[-1]['months'].append(m)

        db.close()
        return result

    def mirrorruns_get_runs_from_archive_ym(self, archive, year, month):
        db = DBInstance(self.pool)
        result = None

        rows = db.query("""SELECT archive_id FROM archive WHERE archive.name=%(name)s""",
            { 'name': archive })

        if len(rows) != 0:
            archive_id = rows[0]['archive_id']

            result = db.query("""
                SELECT to_char(run, 'YYYYMMDD"T"HH24MISS') AS run, run as run_hr
                  FROM mirrorrun
                  WHERE mirrorrun.archive_id=%(archive_id)s
                    AND extract(year from run) = %(year)s
                    AND extract(month from run) = %(month)s
                  ORDER BY run""",
                { 'archive_id': archive_id,
                  'year': year,
                  'month': month })

        db.close()
        return result

    def mirrorruns_get_mirrorrun_at(self, archive, datespec):
        db = DBInstance(self.pool)
        result = None

        rows = db.query("""
                SELECT run as run_hr, mirrorrun_id
                  FROM mirrorrun JOIN archive ON mirrorrun.archive_id = archive.archive_id
                  WHERE archive.name=%(archive)s
                    AND mirrorrun.run <= %(datespec)s
                  ORDER BY run DESC
                  LIMIT 1""",
                { 'archive': archive,
                  'datespec': datespec })
        if len(rows) != 0:
            result = rows[0]

        db.close()
        return result

    def _strip_multi_slash(self, str):
        old = str
        while True:
            str = str.replace('//', '/')
            if str == old: break
            old = str
        return str

    def mirrorruns_stat(self, mirrorrun_id, path):
        """'stats' a path in a given mirrorrun.  Will return None if the path doesn't exist.
           If it does exist it will do (recursive) symlink resolving and return a dict
           with either file or dir information.
           XXX no idea what it does on danling or cyclic symlinks yet"""
        db = DBInstance(self.pool)
        result = None

        path = path.rstrip('/')
        path = self._strip_multi_slash(path)
        if path == "":
            path = '/'

        stat = db.query_one("""SELECT filetype, path, directory_id, node_id, digest, size FROM stat(%(path)s, %(mirrorrun_id)s)""",
                { 'mirrorrun_id': mirrorrun_id,
                  'path': path } )
        db.close();

        if stat['filetype'] is None:
            return None

        return stat

    def mirrorruns_readdir(self, mirrorrun_id, path):
        db = DBInstance(self.pool)

        readdir = db.query("""SELECT filetype, name, digest, size FROM readdir(%(path)s, %(mirrorrun_id)s) ORDER BY name""",
                { 'mirrorrun_id': mirrorrun_id,
                  'path': path } )
        db.close();

        return readdir

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

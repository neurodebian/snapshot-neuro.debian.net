"""The application's Globals object"""
from pylons import config
import psycopg2
import psycopg2.pool
from snapshot.model.snapshotmodel import SnapshotModel
import yaml

class Globals(object):

    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        app_conf = config['app_conf']

        db_config = {}
        for key in filter(lambda e: e.startswith("snapshot.db."), app_conf.keys()):
            newkey = key.replace("snapshot.db.", '', 1)
            db_config[newkey] = app_conf[key]

        self.pool = psycopg2.pool.ThreadedConnectionPool(5, 20, **db_config)
        self.shm = SnapshotModel(app_conf['snapshot.farmpath'], self.pool)

        default_expires = {}
        default_expires['expires.package.mr.list'] = 300
        default_expires['expires.package.mr.source'] = 300
        default_expires['expires.package.mr.source_version'] = 300
        default_expires['expires.root'] = 1800

        for key in default_expires:
            if not key in config['app_conf']: config['app_conf'][key] = default_expires[key]

        try:
            self.thishost = open('/etc/hostname').read()
        except:
            self.thishost = 'unknown'

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

"""The application's Globals object"""
from pylons import config
import psycopg2
from DBUtils.PooledDB import PooledDB
from snapshot.model.snapshotmodel import SnapshotModel
import yaml

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application
    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the 'g'
        variable
        """
        app_conf = config['app_conf']

        conffile = app_conf['snapshot.conf']
        self.snap_conf = yaml.load(open(conffile).read())
        self.pool = PooledDB(psycopg2, 5, **self.snap_conf['db-ro'])
        self.shm = SnapshotModel(self.snap_conf['snapshot']['farmpath'])

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

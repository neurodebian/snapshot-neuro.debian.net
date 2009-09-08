"""The application's Globals object"""
from pylons import config
import psycopg2
import psycopg2.extras
from DBUtils.PooledDB import PooledDB


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
        self.pool = PooledDB(psycopg2, int(app_conf['dbpool.size']), database=app_conf['dbpool.database'])

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

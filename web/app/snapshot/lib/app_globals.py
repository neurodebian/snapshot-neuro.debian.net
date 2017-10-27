## snapshot.debian.org - web frontend
#
# Copyright (c) 2009, 2010 Peter Palfrader
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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

        self.pool = psycopg2.pool.ThreadedConnectionPool(5, 10, **db_config)
        self.shm = SnapshotModel(app_conf['snapshot.farmpath'], self.pool)

        defaults = {}
        defaults['expires.package.mr.list'] = 300
        defaults['expires.package.mr.source'] = 300
        defaults['expires.package.mr.source_version'] = 300
        defaults['expires.root'] = 1800

        defaults['expires.removal'] = 1800
        defaults['expires.removal.one'] = 3600

        defaults['snapshot.domain'] = 'snapshot-neuro.debian.net'
        defaults['snapshot.masterdomain'] = 'snapshot.debian.org'

        for key in defaults:
            if not key in config['app_conf']: config['app_conf'][key] = defaults[key]

        try:
            self.thishost = open('/etc/hostname').read()
        except:
            self.thishost = 'unknown'

        # Some global constants bound for easy access
        self.domain = config['app_conf']['snapshot.domain']
        self.masterdomain = config['app_conf']['snapshot.masterdomain']

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

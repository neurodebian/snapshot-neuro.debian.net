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

import logging

from pylons import request, response, session, tmpl_context as c, app_globals, config
from pylons.controllers.util import abort

from snapshot.lib.base import BaseController, render

from snapshot.lib.dbinstance import DBInstance
from snapshot.lib.control_helpers import *

log = logging.getLogger(__name__)

class MiscController(BaseController):
    def trace(self):
        db = None
        try:
            db = DBInstance(app_globals.pool)
            set_expires(int(config['app_conf']['expires.root']))

            last = app_globals.shm.get_last_mirrorrun(db)

            content = []
            content.append("%s\n"%(last.ctime()))
            content.append("# Above timestamp is timestamp of latest mirrrorrun\n")

            response.content_type = 'text/plain'
            return content
        finally:
            if not db is None: db.close()

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

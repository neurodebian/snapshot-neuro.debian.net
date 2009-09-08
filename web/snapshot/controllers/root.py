import logging

from snapshot.lib.base import *

log = logging.getLogger(__name__)

class RootController(BaseController):

    def index(self):
        # Return a rendered template
        #   return render('/some/template.mako')
        # or, Return a response
        c.rows = [ 'debian', 'debian-security' ]
        return render('/root.mako')

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

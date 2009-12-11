#!/usr/bin/python

import site
site.addsitedir("/srv/snapshot.debian.org/web-app/lib/python2.5/site-packages")

from paste.deploy import loadapp
application = loadapp('config:/srv/snapshot.debian.org/etc/web-app.ini')

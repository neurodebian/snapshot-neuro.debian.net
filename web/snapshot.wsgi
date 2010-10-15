#!/usr/bin/python

import site
from os.path import join
from distutils.sysconfig import get_python_lib

domain = "snapshot-neuro.debian.net"
topdir = join("/srv", domain)

site.addsitedir(get_python_lib(prefix=join(topdir, 'web-app')))

from paste.deploy import loadapp
application = loadapp('config:' + join(topdir, 'etc', 'web-app.ini'))

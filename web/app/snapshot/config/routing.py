## snapshot.debian.org - web frontend
#
# Copyright (c) 2009, 2010, 2015 Peter Palfrader
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

"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    map.connect('/', controller='root', action='index')
    map.connect('/oldnews', controller='root', action='oldnews')

    map.connect('/archive/', controller='archive', action='root')
    map.connect('/archive/{archive}/', controller='archive', action='archive_base')
    map.connect('/archive/{archive}/{date}/', controller='archive', action='dir', url='/')
    map.connect('/archive/{archive}/{date}/*url', controller='archive', action='dir')

    map.connect('/package/', controller='package', action='root')
    map.connect('/package/{source}/', controller='package', action='source')
    map.connect('/package/{source}/{version}/', controller='package', action='source_version')

    map.connect('/binary/', controller='package', action='binary_root')
    map.connect('/binary/{binary}/', controller='package', action='binary')

    map.connect('/mr/package/', controller='package', action='mr_list')
    map.connect('/mr/package/{source}/', controller='package', action='mr_source')
    map.connect('/mr/package/{source}/{version}/srcfiles', controller='package', action='mr_source_version_srcfiles')
    map.connect('/mr/package/{source}/{version}/binpackages', controller='package', action='mr_source_version_binpackages')
    map.connect('/mr/package/{source}/{version}/binfiles/{binary}/{binary_version}', controller='package', action='mr_source_version_binfiles')
    map.connect('/mr/package/{source}/{version}/allfiles', controller='package', action='mr_source_version_allfiles')

    map.connect('/mr/binary/{binary}/', controller='package', action='mr_binary')
    map.connect('/mr/binary/{binary}/{binary_version}/binfiles', controller='package', action='mr_binary_version_binfiles')

    map.connect('/file/{hash}', controller='archive', action='file')
    map.connect('/mr/file/{hash}/info', controller='package', action='mr_fileinfo')

    map.connect('/removal/', controller='removal', action='root')
    map.connect('/removal/{id}', controller='removal', action='one')

    map.connect('/project/trace/%s' % config['app_conf']['snapshot.masterdomain'], controller='misc', action='trace')

    #map.connect('/{controller}/{action}')
    #map.connect('/{controller}/{action}/{id}')

    return map

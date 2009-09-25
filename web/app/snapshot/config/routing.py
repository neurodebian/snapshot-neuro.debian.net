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

    map.connect('/archive/', controller='archive', action='root')
    map.connect('/archive/{archive}/', controller='archive', action='archive_base')
    map.connect('/archive/{archive}/{date}/', controller='archive', action='dir', url='/')
    map.connect('/archive/{archive}/{date}/*url', controller='archive', action='dir')

    map.connect('/package/', controller='package', action='root')
    map.connect('/package/{source}', controller='package', action='source')
    map.connect('/package/{source}/{version}', controller='package', action='source_version')


    #map.connect('/{controller}/{action}')
    #map.connect('/{controller}/{action}/{id}')

    return map

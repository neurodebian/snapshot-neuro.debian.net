import logging
from snapshot.lib.dbinstance import DBInstance
from pylons import request, response
from paste.request import construct_url
from paste.httpexceptions import HTTPMovedPermanently
import datetime
from webob.exc import HTTPNotModified

def urlify_timestamp(ts):
    return ts.strftime('%Y%m%dT%H%M%S')

def build_url_archive(archive, ts=None, path=None, isadir=True):
    crumbs = []

    url = request.environ.get('SCRIPT_NAME') + "/"
    url += 'archive/' + archive + "/"

    if not ts:
        return url

    url += urlify_timestamp(ts) + '/'

    if not path:
        return url

    if path != '/':
        for path_element in path.strip('/').split('/'):
            url += path_element + '/'

    if not isadir:
        url = url.rstrip('/')

    return url

def build_url_archive_ym_list(archive, year, month):
    url = build_url_archive(archive)
    ym = (year, month)
    url += "?year=%d&month=%d"%ym
    return url

def unicode_encode(path):
    if isinstance(path, unicode):
        return path.encode('utf-8')
    else:
        return path

def modified_since(last_mod):
    if last_mod is None:
        return

    if last_mod.tzinfo is None:
        raise "*sigh* - how do I set tzinfo to UTC on a naive datetime object?"
        # last_mod = last_mod.replace(tzinfo=0)

    if_since = None
    if request.if_modified_since:
        print "if mod since:",  request.if_modified_since
        if_since = request.if_modified_since
    elif request.if_unmodified_since:
        print "if unmod since:",  request.if_unmodified_since
        if_since = request.if_unmodified_since

    if if_since and (last_mod <= if_since):
        print "need not send"
        raise HTTPNotModified()

    response.last_modified = last_mod

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

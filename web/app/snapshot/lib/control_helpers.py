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
from snapshot.lib.dbinstance import DBInstance
from pylons import request, response
from paste.request import construct_url
from paste.httpexceptions import HTTPMovedPermanently
import datetime
from webob.exc import HTTPNotModified
import urllib

def rfc3339_timestamp(ts):
    return ts.strftime('%Y%m%dT%H%M%SZ')

def build_url_archive(archive, ts=None, path=None, isadir=True):
    crumbs = []

    url = request.environ.get('SCRIPT_NAME') + "/"
    url += 'archive/' + archive + "/"
    url = urllib.quote(url)

    if not ts:
        return url

    url += rfc3339_timestamp(ts) + '/'

    if not path:
        return url

    if path != '/':
        for path_element in path.strip('/').split('/'):
            url += urllib.quote(path_element) + '/'

    if not isadir:
        url = url.rstrip('/')

    return url

def build_url_archive_ym_list(archive, year, month):
    url = build_url_archive(archive)
    ym = (year, month)
    url += "?year=%d&month=%d"%ym
    return url

def url_quote(s):
    if isinstance(s, unicode):
        s = s.encode('utf-8')
    return urllib.quote(s)

def set_expires(max_age):
    response.expires = datetime.datetime.now() + datetime.timedelta(seconds = max_age);
    response.cache_control = 'public, max-age=%d'%max_age
    response.pragma = None

def link_quote_array(a):
    return map(lambda x: { 'raw':    x,
                           'quoted': urllib.quote(x) }, a)

#def modified_since(last_mod):
#    if last_mod is None:
#        return
#
#    if last_mod.tzinfo is None:
#        raise "*sigh* - how do I set tzinfo to UTC on a naive datetime object?"
#        # last_mod = last_mod.replace(tzinfo=0)
#
#    if_since = None
#    if request.if_modified_since:
#        print "if mod since:",  request.if_modified_since
#        if_since = request.if_modified_since
#    elif request.if_unmodified_since:
#        print "if unmod since:",  request.if_unmodified_since
#        if_since = request.if_unmodified_since
#
#    if if_since and (last_mod <= if_since):
#        print "need not send"
#        raise HTTPNotModified()
#
#    response.last_modified = last_mod

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:

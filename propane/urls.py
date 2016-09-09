# coding=utf-8
from __future__ import absolute_import, print_function

import posixpath
from urllib import urlencode

# noinspection PyUnresolvedReferences
from six.moves.urllib.parse import parse_qsl, urlsplit, urlunsplit

__author__ = 'Tyler Butler <tyler@tylerbutler.com>'

try:
    # noinspection PyUnresolvedReferences
    from propane.flask.urls import *
except ImportError:
    pass


def remove_query_parameters(url, params=None, case_sensitive=False):
    def is_in(to_check, iterable, cs):
        if cs:
            return to_check in iterable
        else:
            return to_check.upper().lower() in iterable

    pieces = list(urlsplit(url))
    if params is None:
        pieces[3] = ''
    else:
        if not case_sensitive:
            params[:] = [p.upper().lower() for p in params]
        query = parse_qsl(pieces[3])
        query[:] = [(param, value) for param, value in query if not is_in(param, params, case_sensitive)]
        pieces[3] = urlencode(query, doseq=True)
    return urlunsplit(pieces)


def urljoin(url1, *url2):
    # This method is necessary because sometimes urlparse.urljoin simply doesn't work correctly
    # when joining URL fragments.
    return posixpath.join(url1, *url2)

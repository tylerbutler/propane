# coding=utf-8
from __future__ import absolute_import
from urllib import urlencode
from urlparse import parse_qsl, urlsplit, urlunsplit

__author__ = 'Tyler Butler <tyler@tylerbutler.com>'

try:
    # noinspection PyUnresolvedReferences
    from propane.flask.urls import absolute_url_for, is_local_url
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

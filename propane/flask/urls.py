# coding=utf-8
from urlparse import urlsplit, urlunsplit
from flask import request, url_for

__author__ = 'Tyler Butler <tyler@tylerbutler.com>'


def absolute_url_for(view, **kwargs):
    relative_url = url_for(view, **kwargs)
    relative_url_pieces = list(urlsplit(relative_url))
    relative_url_pieces[0], relative_url_pieces[1], _, _, _ = urlsplit(request.url_root)
    absolute_url = urlunsplit(relative_url_pieces)
    return absolute_url


def is_local_url(url_to_check):
    current_netloc = urlsplit(request.url_root).netloc
    check_netloc = urlsplit(url_to_check).netloc
    return current_netloc == check_netloc

# coding=utf-8
from __future__ import absolute_import, print_function

# noinspection PyPackageRequirements,PyUnresolvedReferences
from six.moves.urllib.parse import urlsplit

__author__ = 'Tyler Butler <tyler@tylerbutler.com>'

try:
    # noinspection PyPackageRequirements,PyUnresolvedReferences
    from flask import request, url_for
except ImportError:
    print("Flask is required but cannot be imported.")
    raise


def absolute_url_for(view, **kwargs):
    absolute_url = url_for(view, _external=True, **kwargs)
    return absolute_url


def is_local_url(url_to_check):
    current_netloc = urlsplit(request.url_root).netloc
    check_netloc = urlsplit(url_to_check).netloc
    return current_netloc == check_netloc

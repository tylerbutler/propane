# coding=utf-8
from path import path

__author__ = 'Tyler Butler <tyler@tylerbutler.com>'

def ensure_path_exists(p):
    """
    Ensures a given path *p* exists.

    If a path to a file is passed in, then the path to the file will be checked.
    """
    if path(p).ext:
        path(p).dirname().makedirs_p()
    else:
        path(p).makedirs_p()
    return p



# coding=utf-8
import time

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


def timestamp_to_ticks(t=None):
    """
    Convert a Python time into Ticks, equivalent to .NET's DateTime.Ticks value.
    :param t: the time to convert
    :return: the time in ticks
    """
    if t is None:
        t = time.time()
    return int(t * (10 ** 7)) + 621355968000000000

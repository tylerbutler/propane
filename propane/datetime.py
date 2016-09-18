# coding=utf-8
from __future__ import absolute_import, print_function

import time


__author__ = 'Tyler Butler <tyler@tylerbutler.com>'


def timestamp_to_ticks(t=None):
    """
    Convert a Python time into Ticks, equivalent to .NET's DateTime.Ticks value.

    :param t: the time to convert
    :return: the time in ticks
    """
    if t is None:
        t = time.time()
    return int(t * (10 ** 7)) + 621355968000000000

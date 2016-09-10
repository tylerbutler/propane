# coding=utf-8
from __future__ import absolute_import, print_function

import pprint


__author__ = 'Tyler Butler <tyler@tylerbutler.com>'


pprinter = pprint.PrettyPrinter()


# noinspection PyBroadException
def log_object(obj):
    try:
        return pprinter.pformat(obj)
    except Exception:
        return str(obj)

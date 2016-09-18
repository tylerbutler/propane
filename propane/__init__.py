# coding=utf-8
from __future__ import absolute_import, print_function

__author__ = 'Tyler Butler <tyler@tylerbutler.com>'


def version():
    from setuptools_scm import get_version
    return get_version(root='..', relative_to=__file__)

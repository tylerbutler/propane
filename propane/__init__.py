# coding=utf-8
import os

__author__ = 'Tyler Butler <tyler@tylerbutler.com>'

try:
    from propane._version import version
except ImportError:
    from propane.distribution import update_version_py

    update_version_py(version_path=os.path.dirname(__file__))
    try:
        from propane._version import version
    except ImportError:
        raise

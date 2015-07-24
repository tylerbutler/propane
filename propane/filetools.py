# coding=utf-8
import base64
import hashlib

from path import path

__author__ = 'Tyler Butler <tyler@tylerbutler.com>'


def calc_sha(obj):
    """Calculates the base64-encoded SHA hash of a file."""
    try:
        pathfile = path(obj)
    except UnicodeDecodeError:
        pathfile = None
    sha = hashlib.sha256()

    try:
        if pathfile and pathfile.exists():
            return base64.b64encode(pathfile.read_hash('SHA256'))
    except TypeError:
        # likely a bytestring
        if isinstance(obj, basestring):
            pass
        else:
            raise

    if isinstance(obj, basestring):
        sha.update(obj)
    elif hasattr(obj, 'read'):
        while True:
            d = obj.read(8192)
            if not d:
                break
            sha.update(d)
    else:
        return None

    r = sha.digest()
    r = base64.b64encode(r)
    return r

# coding=utf-8
import base64, hashlib, re
from path import path

__author__ = 'Tyler Butler <tyler@tylerbutler.com>'

def space_out_camel_case(stringAsCamelCase):
    """
    Adds spaces to a camel case string.  Failure to space out string returns the original string.

    >>> space_out_camel_case('DMLSServicesOtherBSTextLLC')
    'DMLS Services Other BS Text LLC'
    """
    pattern = re.compile(r'([A-Z][A-Z][a-z])|([a-z][A-Z])')

    if stringAsCamelCase is None:
        return None

    return pattern.sub(lambda m: m.group()[:1] + " " + m.group()[1:], stringAsCamelCase)
